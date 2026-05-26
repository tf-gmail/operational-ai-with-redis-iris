from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

from app.langgraph_pipeline import run_baseline_graph, run_iris_graph
from app.redis_iris_tools import RedisIRISTools, merge_seed_with_redis


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

    baseline_signals = list(result.get("context_signals", []))
    baseline_signals.append("baseline-local-memory-write")
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

    redis_signals: list[str] = []
    customer_id: str | None = None
    combined_recent_events = list(recent_events or [])

    if tools is not None:
        try:
            context = tools.retrieve_context(customer, query_text=message)
            seed = merge_seed_with_redis(seed, context)
            customer_id = context.customer_id

            stream_events = tools.get_recent_operational_events(customer=customer, limit=20)
            if stream_events:
                redis_signals.append("redis-streams-context-hit")
                redis_signals.append(f"redis-streams-context-count={len(stream_events)}")
            else:
                redis_signals.append("redis-streams-context-empty")

            event_map: dict[str, dict[str, Any]] = {}
            for event in combined_recent_events + stream_events:
                if not isinstance(event, dict):
                    continue
                event_id = str(event.get("redis_stream_id") or event.get("event_id") or "")
                key = event_id or f"{event.get('event_type', '')}:{event.get('status', '')}:{event.get('timestamp', '')}"
                event_map[key] = event

            combined_recent_events = sorted(
                event_map.values(),
                key=lambda row: str(row.get("timestamp", "")),
                reverse=True,
            )[:30]

            if context.customer:
                redis_signals.append("redis-context-retriever-customer")
            if context.incidents or context.tickets:
                redis_signals.append("redis-context-retriever-operational")
            if context.similar_incidents:
                redis_signals.append("redis-vector-similar-incidents")
            if context.memories:
                redis_signals.append("redis-agent-memory-hit")
            if context.workflow_state:
                redis_signals.append("redis-shared-workflow-state-hit")
            if context.retrieval_backend.startswith("ft.search"):
                redis_signals.append("redis-ft-search-context")
        except Exception:
            redis_signals.append("redis-context-unavailable")

    result = run_iris_graph(
        customer=customer,
        message=message,
        seed=seed,
        recent_events=combined_recent_events,
    )

    merged_signals = list(result.get("context_signals", []))
    merged_signals.extend(redis_signals)
    result["context_signals"] = merged_signals

    if tools is not None:
        try:
            if customer_id:
                tools.append_memory(customer_id, f"customer-message:{message}")
                result["context_signals"].append("redis-agent-memory-write")

                extracted_facts = tools.extract_memory_facts(
                    customer_message=message,
                    response_summary=str(result.get("summary", "")),
                )
                if extracted_facts:
                    for fact in extracted_facts:
                        tools.append_memory(customer_id, fact, kind="long")
                    result["context_signals"].append("redis-agent-memory-extract")
                    result["context_signals"].append(
                        f"redis-agent-memory-longterm-write={len(extracted_facts)}"
                    )

                prior_state = tools.get_shared_workflow_state(customer_id) or {}
                next_turn = int(prior_state.get("turn_count", 0)) + 1
                tools.set_shared_workflow_state(
                    customer_id,
                    {
                        "turn_count": next_turn,
                        "last_mode": "iris",
                        "last_message": message,
                        "last_summary": str(result.get("summary", "")),
                        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    },
                )
                result["context_signals"].append("redis-shared-workflow-state-write")
                result["context_signals"].append(f"redis-shared-workflow-turn={next_turn}")
            tools.set_cached_response(customer, message, result)
            result["context_signals"].append("redis-langcache-store")
        except Exception:
            result["context_signals"].append("redis-postprocessing-unavailable")

    return _enrich_runtime_metrics(result, message=message, started_at=started_at, mode="iris")
