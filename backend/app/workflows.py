from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from app.langgraph_pipeline import run_baseline_graph, run_iris_graph
from app.redis_iris_tools import RedisIRISTools, merge_seed_with_redis


_REDIS_TOOLS: RedisIRISTools | None = None


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
    return run_baseline_graph(customer=customer, message=message, seed=seed)


def run_iris_workflow(
    customer: str,
    message: str,
    recent_events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    seed = load_acme_seed()

    tools = get_redis_tools()
    if tools is not None:
        try:
            cached = tools.get_cached_response(customer, message)
            if cached is not None:
                cached_signals = list(cached.get("context_signals", []))
                cached_signals.append("redis-langcache-hit")
                cached["context_signals"] = cached_signals
                return cached
        except Exception:
            pass

    redis_signals: list[str] = []
    customer_id: str | None = None

    if tools is not None:
        try:
            context = tools.retrieve_context(customer)
            seed = merge_seed_with_redis(seed, context)
            customer_id = context.customer_id

            if context.customer:
                redis_signals.append("redis-context-retriever-customer")
            if context.incidents or context.tickets:
                redis_signals.append("redis-context-retriever-operational")
            if context.similar_incidents:
                redis_signals.append("redis-vector-similar-incidents")
            if context.memories:
                redis_signals.append("redis-agent-memory-hit")
            if context.retrieval_backend.startswith("ft.search"):
                redis_signals.append("redis-ft-search-context")
        except Exception:
            redis_signals.append("redis-context-unavailable")

    result = run_iris_graph(
        customer=customer,
        message=message,
        seed=seed,
        recent_events=recent_events,
    )

    merged_signals = list(result.get("context_signals", []))
    merged_signals.extend(redis_signals)
    result["context_signals"] = merged_signals

    if tools is not None:
        try:
            if customer_id:
                tools.append_memory(customer_id, f"customer-message:{message}")
                result["context_signals"].append("redis-agent-memory-write")
            tools.set_cached_response(customer, message, result)
            result["context_signals"].append("redis-langcache-store")
        except Exception:
            result["context_signals"].append("redis-postprocessing-unavailable")

    return result
