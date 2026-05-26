from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from app.redis_iris_tools import RedisIRISTools, merge_seed_with_redis
from app.state_contracts import RetrievalRequestContract, RetrievalResponseContract, build_retrieval_contract


@dataclass
class ContextPacket:
    seed: dict[str, Any]
    recent_events: list[dict[str, Any]]
    context_signals: list[str]
    customer_id: str | None
    retrieval_api: RetrievalResponseContract | None


def _merge_recent_events(
    local_events: list[dict[str, Any]],
    stream_events: list[dict[str, Any]],
    limit: int = 30,
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for event in local_events + stream_events:
        if not isinstance(event, dict):
            continue
        event_id = str(event.get("redis_stream_id") or event.get("event_id") or "")
        key = event_id or f"{event.get('event_type', '')}:{event.get('status', '')}:{event.get('timestamp', '')}"
        merged[key] = event

    return sorted(merged.values(), key=lambda row: str(row.get("timestamp", "")), reverse=True)[:limit]


def build_context_packet(
    *,
    customer: str,
    message: str,
    base_seed: dict[str, Any],
    recent_events: list[dict[str, Any]] | None,
    tools: RedisIRISTools | None,
) -> ContextPacket:
    seed = dict(base_seed)
    merged_events = list(recent_events or [])
    signals: list[str] = []
    customer_id: str | None = None

    if tools is None:
        return ContextPacket(
            seed=seed,
            recent_events=merged_events,
            context_signals=signals,
            customer_id=customer_id,
            retrieval_api=None,
        )

    retrieval_api: RetrievalResponseContract | None = None

    try:
        context = tools.retrieve_context(customer, query_text=message)
        seed = merge_seed_with_redis(seed, context)
        customer_id = context.customer_id
        retrieval_request: RetrievalRequestContract = {
            "customer": customer,
            "query_text": message,
            "memory_limit": 5,
        }
        retrieval_api = build_retrieval_contract(context=context, request=retrieval_request)

        stream_events = tools.get_recent_operational_events(customer=customer, limit=20)
        if stream_events:
            signals.append("redis-streams-context-hit")
            signals.append(f"redis-streams-context-count={len(stream_events)}")
        else:
            signals.append("redis-streams-context-empty")

        merged_events = _merge_recent_events(merged_events, stream_events)

        if context.customer:
            signals.append("redis-context-retriever-customer")
        if context.incidents or context.tickets:
            signals.append("redis-context-retriever-operational")
        if context.similar_incidents:
            signals.append("redis-vector-similar-incidents")
        if context.memories:
            signals.append("redis-agent-memory-hit")
        if context.workflow_state:
            signals.append("redis-shared-workflow-state-hit")
        if context.retrieval_backend.startswith("ft.search"):
            signals.append("redis-ft-search-context")
        signals.append("retrieval-api-contract-v1")
    except Exception:
        signals.append("redis-context-unavailable")

    return ContextPacket(
        seed=seed,
        recent_events=merged_events,
        context_signals=signals,
        customer_id=customer_id,
        retrieval_api=retrieval_api,
    )


def apply_redis_postprocessing(
    *,
    tools: RedisIRISTools | None,
    customer: str,
    customer_id: str | None,
    message: str,
    result: dict[str, Any],
) -> list[str]:
    signals: list[str] = []
    if tools is None:
        return signals

    try:
        if customer_id:
            tools.append_memory(customer_id, f"customer-message:{message}")
            signals.append("redis-agent-memory-write")

            extracted_facts = tools.extract_memory_facts(
                customer_message=message,
                response_summary=str(result.get("summary", "")),
            )
            if extracted_facts:
                for fact in extracted_facts:
                    tools.append_memory(customer_id, fact, kind="long")
                signals.append("redis-agent-memory-extract")
                signals.append(f"redis-agent-memory-longterm-write={len(extracted_facts)}")

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
            signals.append("redis-shared-workflow-state-write")
            signals.append(f"redis-shared-workflow-turn={next_turn}")

        tools.set_cached_response(customer, message, result)
        signals.append("redis-langcache-store")
    except Exception:
        signals.append("redis-postprocessing-unavailable")

    return signals
