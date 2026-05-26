from __future__ import annotations

import json
import os
from pathlib import Path
from time import perf_counter
from typing import Any

from app.context_layer import apply_redis_postprocessing, build_context_packet
from app.langgraph_pipeline import run_baseline_graph, run_iris_graph
from app.redis_iris_tools import RedisIRISTools
from app.runtime_state import get_runtime_state_store


_REDIS_TOOLS: RedisIRISTools | None = None
_BASELINE_LOCAL_MEMORY: dict[str, dict[str, Any]] = {}


def _token_estimate(text: str) -> int:
    # Lightweight deterministic estimate for instrumentation and UI comparisons.
    return max(1, len(text) // 4)


def _enrich_runtime_metrics(
    result: dict[str, Any],
    *,
    message: str,
    started_at: float,
    mode: str,
) -> dict[str, Any]:
    elapsed_ms = int((perf_counter() - started_at) * 1000)

    existing_metrics = result.get("metrics", {})
    metrics = dict(existing_metrics) if isinstance(existing_metrics, dict) else {}

    summary = str(result.get("summary", ""))
    prompt_tokens_observed = _token_estimate(message)
    completion_tokens_observed = _token_estimate(summary)

    signals = list(result.get("context_signals", []))
    retrieval_signal_count = sum(1 for signal in signals if "retrieval" in str(signal) or "search" in str(signal))
    tools_signal_count = sum(1 for signal in signals if str(signal).startswith("redis-") or "vector" in str(signal))

    # Deterministic latency decomposition for benchmark trendability.
    retrieval_latency_ms_estimated = retrieval_signal_count * 12
    llm_latency_ms_estimated = max(20, completion_tokens_observed // 2)
    orchestration_latency_ms_estimated = max(0, elapsed_ms - retrieval_latency_ms_estimated - llm_latency_ms_estimated)

    metrics["runtime_latency_ms"] = elapsed_ms
    metrics["retrieval_latency_ms_estimated"] = retrieval_latency_ms_estimated
    metrics["llm_latency_ms_estimated"] = llm_latency_ms_estimated
    metrics["orchestration_latency_ms_estimated"] = orchestration_latency_ms_estimated
    metrics["prompt_tokens_observed"] = prompt_tokens_observed
    metrics["completion_tokens_observed"] = completion_tokens_observed
    metrics["retrieval_signals"] = retrieval_signal_count
    metrics["tool_signals"] = tools_signal_count

    if mode == "baseline":
        metrics["instrumentation_mode"] = "baseline-runtime"
    else:
        metrics["instrumentation_mode"] = "iris-runtime"

    result["metrics"] = metrics
    signals.append("runtime-metrics-enriched")
    signals.append(f"runtime-latency-ms={elapsed_ms}")
    result["context_signals"] = signals
    return result


def get_redis_tools() -> RedisIRISTools | None:
    global _REDIS_TOOLS
    if _REDIS_TOOLS is not None:
        return _REDIS_TOOLS

    try:
        tools = RedisIRISTools()
        if not tools.available():
            return None
        _REDIS_TOOLS = tools
        return _REDIS_TOOLS
    except Exception:
        return None


def _default_seed() -> dict[str, Any]:
    return {
        "customer": {
            "name": "Acme Corp",
            "arr": 480000,
            "renewal_date": "2026-07-15",
            "risk_level": "high",
            "health_score": 41,
        },
        "stakeholders": [
            {
                "name": "Jordan Lee",
                "role": "VP Engineering",
                "preference": "Executive summaries first",
            }
        ],
        "incidents": [
            {
                "incident_id": "inc-2026-0412",
                "service": "search-api",
                "status": "investigating",
                "summary": "Search API p95 latency exceeded 1.8s after deployment.",
                "updated_at": "2026-05-26T08:00:00Z",
            }
        ],
        "tickets": [
            {
                "ticket_id": "tkt-009182",
                "severity": "sev-1",
                "summary": "Customer reports repeated outages and renewal concern.",
            }
        ],
        "memories": [
            "Customer was promised executive escalation if latency issues recur.",
            "Acme prefers concise executive communication over verbose technical detail.",
        ],
        "usage": {
            "trend": "declining",
            "adoption_change_30d": -0.11,
        },
    }


def load_acme_seed() -> dict[str, Any]:
    explicit = os.getenv("ACME_SEED_PATH")
    candidate_paths = []
    if explicit:
        candidate_paths.append(Path(explicit))

    candidate_paths.extend(
        [
            Path(__file__).resolve().parent / "seed_data" / "acme_seed.json",
            Path(__file__).resolve().parents[2] / "data" / "acme_seed.json",
        ]
    )

    for path in candidate_paths:
        try:
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

    return _default_seed()


def run_baseline_workflow(customer: str, message: str) -> dict[str, Any]:
    seed = load_acme_seed()
    started_at = perf_counter()
    shared_state = get_runtime_state_store()
    using_shared_state = shared_state is not None

    session = None
    if shared_state is not None:
        session = shared_state.load_baseline_session(customer)

    if session is None:
        session = _BASELINE_LOCAL_MEMORY.setdefault(
            customer,
            {
                "history": [],
                "turn_count": 0,
                "last_summary": "",
            },
        )

    history = list(session.get("history", []))[-6:]
    local_state = {
        "turn_count": int(session.get("turn_count", 0)),
        "last_summary": str(session.get("last_summary", "")),
    }

    result = run_baseline_graph(
        customer=customer,
        message=message,
        seed=seed,
        local_history=history,
        local_state=local_state,
    )

    updated_history = history + [
        {"role": "user", "message": message},
        {"role": "assistant", "summary": str(result.get("summary", ""))},
    ]
    session["history"] = updated_history[-12:]
    session["turn_count"] = int(local_state["turn_count"]) + 1
    session["last_summary"] = str(result.get("summary", ""))

    if shared_state is not None:
        shared_state.save_baseline_session(customer, session)

    baseline_signals = list(result.get("context_signals", []))
    baseline_signals.append("baseline-local-memory-write")
    if using_shared_state:
        baseline_signals.append("baseline-shared-state-read")
        baseline_signals.append("baseline-shared-state-write")
    else:
        baseline_signals.append("baseline-local-memory-fallback")
    result["context_signals"] = baseline_signals
    return _enrich_runtime_metrics(result, message=message, started_at=started_at, mode="baseline")


def run_iris_workflow(
    customer: str,
    message: str,
    recent_events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    seed = load_acme_seed()
    started_at = perf_counter()

    tools = get_redis_tools()
    if tools is not None:
        try:
            cached = tools.get_cached_response(customer, message)
            if cached is not None:
                cached_signals = list(cached.get("context_signals", []))
                cached_signals.append("redis-langcache-hit")
                cached["context_signals"] = cached_signals
                return _enrich_runtime_metrics(cached, message=message, started_at=started_at, mode="iris")
        except Exception:
            pass

    context_packet = build_context_packet(
        customer=customer,
        message=message,
        base_seed=seed,
        recent_events=recent_events,
        tools=tools,
    )
    seed = context_packet.seed

    result = run_iris_graph(
        customer=customer,
        message=message,
        seed=seed,
        recent_events=context_packet.recent_events,
    )

    merged_signals = list(result.get("context_signals", []))
    merged_signals.extend(context_packet.context_signals)
    result["context_signals"] = merged_signals

    result["context_signals"].extend(
        apply_redis_postprocessing(
            tools=tools,
            customer=customer,
            customer_id=context_packet.customer_id,
            message=message,
            result=result,
        )
    )

    return _enrich_runtime_metrics(result, message=message, started_at=started_at, mode="iris")
