from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from app.redis_iris_tools import RedisContext


class MemoryRecordContract(TypedDict):
    customer_id: str
    scope: Literal["short", "long", "derived"]
    kind: str
    text: str
    rank: int


class EventRecordContract(TypedDict, total=False):
    event_id: str
    timestamp: str
    event_type: str
    status: str
    customer: str
    message: str | None
    source: str
    replay: dict[str, Any]
    redis_stream_id: str


class RetrievalRequestContract(TypedDict):
    customer: str
    query_text: str
    memory_limit: int


class RetrievalResponseContract(TypedDict):
    customer_id: str | None
    retrieval_backend: str
    used_filters: list[str]
    incidents_count: int
    tickets_count: int
    timeline_events_count: int
    similar_incidents_count: int
    memories: list[MemoryRecordContract]


def parse_memory_kind(memory_text: str) -> str:
    if ":" in memory_text:
        prefix = memory_text.split(":", 1)[0].strip().lower()
        if prefix:
            return prefix
    return "note"


def to_memory_record_contract(
    *,
    customer_id: str,
    memory_text: str,
    scope: Literal["short", "long", "derived"],
    rank: int,
) -> MemoryRecordContract:
    return {
        "customer_id": customer_id,
        "scope": scope,
        "kind": parse_memory_kind(memory_text),
        "text": memory_text,
        "rank": rank,
    }


def to_event_record_contract(event: dict[str, Any]) -> EventRecordContract:
    contract: EventRecordContract = {
        "event_id": str(event.get("event_id", "")),
        "timestamp": str(event.get("timestamp", "")),
        "event_type": str(event.get("event_type", "unknown")),
        "status": str(event.get("status", "unknown")),
        "customer": str(event.get("customer", "unknown")),
        "message": event.get("message"),
        "source": str(event.get("source", "unknown")),
    }

    replay = event.get("replay")
    if isinstance(replay, dict):
        contract["replay"] = replay

    stream_id = event.get("redis_stream_id")
    if stream_id:
        contract["redis_stream_id"] = str(stream_id)

    return contract


def _derive_used_filters(query_text: str) -> list[str]:
    lowered = query_text.lower()
    filters: list[str] = []

    if any(token in lowered for token in ["sev-1", "sev-2", "sev1", "sev2", "critical", "high"]):
        filters.append("severity")

    if any(
        token in lowered
        for token in [
            "investigating",
            "mitigated",
            "resolved",
            "open",
            "closed",
            "monitoring",
            "rollback",
        ]
    ):
        filters.append("status")

    if any(token in lowered for token in ["search-api", "billing-api", "identity-api", "events-api", "sync-worker"]):
        filters.append("service")

    return filters


def build_retrieval_contract(
    *,
    context: "RedisContext",
    request: RetrievalRequestContract,
) -> RetrievalResponseContract:
    customer_id = context.customer_id
    memory_records: list[MemoryRecordContract] = []
    for idx, memory_text in enumerate(context.memories):
        if not memory_text:
            continue
        memory_records.append(
            to_memory_record_contract(
                customer_id=customer_id or "unknown",
                memory_text=memory_text,
                scope="derived",
                rank=idx,
            )
        )

    return {
        "customer_id": customer_id,
        "retrieval_backend": str(context.retrieval_backend),
        "used_filters": _derive_used_filters(request["query_text"]),
        "incidents_count": len(context.incidents),
        "tickets_count": len(context.tickets),
        "timeline_events_count": len(context.timeline_events),
        "similar_incidents_count": len(context.similar_incidents),
        "memories": memory_records[: max(1, request["memory_limit"])],
    }
