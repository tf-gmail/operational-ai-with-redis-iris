from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, StateGraph


class PipelineState(TypedDict, total=False):
    customer: str
    message: str
    seed: dict[str, Any]
    recent_events: list[dict[str, Any]]
    incident: dict[str, Any]
    memory: str
    latest_event: dict[str, Any] | None
    event_note: str
    summary: str
    metrics: dict[str, Any]
    context_signals: list[str]
    local_history: list[dict[str, Any]]
    local_state: dict[str, Any]
    retrieval_context: dict[str, Any]


def _baseline_load_incident(state: PipelineState) -> PipelineState:
    seed = state["seed"]
    incidents = seed.get("incidents", [])
    incident = incidents[0] if incidents else {"summary": "No active incidents found.", "status": "unknown"}
    return {"incident": incident}


def _tokenize(text: str) -> set[str]:
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return {part for part in cleaned.split() if len(part) >= 3}


def _baseline_build_seed_documents(seed: dict[str, Any]) -> list[dict[str, str]]:
    docs: list[dict[str, str]] = []
    customer = seed.get("customer", {})
    if isinstance(customer, dict):
        docs.append(
            {
                "id": "customer-profile",
                "text": (
                    f"Customer {customer.get('name', '')} risk {customer.get('risk_level', '')} "
                    f"health {customer.get('health_score', '')} arr {customer.get('arr', '')} "
                    f"renewal {customer.get('renewal_date', '')}."
                ),
            }
        )

    for idx, incident in enumerate(seed.get("incidents", [])[:8]):
        if not isinstance(incident, dict):
            continue
        docs.append(
            {
                "id": f"incident-{idx + 1}",
                "text": (
                    f"Incident {incident.get('incident_id', '')} {incident.get('service', '')} "
                    f"status {incident.get('status', '')} summary {incident.get('summary', '')}."
                ),
            }
        )

    for idx, ticket in enumerate(seed.get("tickets", [])[:8]):
        if not isinstance(ticket, dict):
            continue
        docs.append(
            {
                "id": f"ticket-{idx + 1}",
                "text": (
                    f"Ticket {ticket.get('ticket_id', '')} severity {ticket.get('severity', '')} "
                    f"summary {ticket.get('summary', '')}."
                ),
            }
        )

    for idx, stakeholder in enumerate(seed.get("stakeholders", [])[:6]):
        if not isinstance(stakeholder, dict):
            continue
        docs.append(
            {
                "id": f"stakeholder-{idx + 1}",
                "text": (
                    f"Stakeholder {stakeholder.get('name', '')} role {stakeholder.get('role', '')} "
                    f"preference {stakeholder.get('preference', '')}."
                ),
            }
        )

    return docs


def _baseline_retrieve_context(state: PipelineState) -> PipelineState:
    seed = state.get("seed", {})
    message = state.get("message", "")

    documents = _baseline_build_seed_documents(seed)
    message_tokens = _tokenize(str(message))

    keyword_scored: list[dict[str, Any]] = []
    vector_scored: list[dict[str, Any]] = []

    for document in documents:
        doc_text = document["text"]
        doc_tokens = _tokenize(doc_text)
        overlap = message_tokens.intersection(doc_tokens)
        keyword_score = len(overlap)
        if keyword_score > 0:
            keyword_scored.append(
                {
                    "id": document["id"],
                    "score": keyword_score,
                    "snippet": doc_text,
                }
            )

        denom = max((len(message_tokens) * len(doc_tokens)) ** 0.5, 1.0)
        vector_score = round(len(overlap) / denom, 4)
        if vector_score > 0:
            vector_scored.append(
                {
                    "id": document["id"],
                    "score": vector_score,
                    "snippet": doc_text,
                }
            )

    keyword_hits = sorted(keyword_scored, key=lambda item: (-item["score"], item["id"]))[:4]
    vector_hits = sorted(vector_scored, key=lambda item: (-item["score"], item["id"]))[:3]

    json_slice = {
        "customer": seed.get("customer", {}),
        "incidents": seed.get("incidents", [])[:2],
        "tickets": seed.get("tickets", [])[:2],
        "stakeholders": seed.get("stakeholders", [])[:2],
    }

    return {
        "retrieval_context": {
            "json_slice": json_slice,
            "keyword_hits": keyword_hits,
            "vector_hits": vector_hits,
            "documents_scanned": len(documents),
        }
    }


def _baseline_compose_summary(state: PipelineState) -> PipelineState:
    customer = state["customer"]
    incident = state["incident"]
    local_history = state.get("local_history", [])
    local_state = state.get("local_state", {})
    prior_turns = int(local_state.get("turn_count", 0))
    retrieval_context = state.get("retrieval_context", {})
    keyword_hits = retrieval_context.get("keyword_hits", [])
    vector_hits = retrieval_context.get("vector_hits", [])

    continuity_note = "No prior baseline session context found."
    if local_history:
        latest_user_message = ""
        for item in reversed(local_history):
            if item.get("role") == "user":
                latest_user_message = str(item.get("message", ""))
                break
        if latest_user_message:
            continuity_note = f"Reused local session memory from prior prompt: '{latest_user_message}'."
        else:
            continuity_note = "Reused local session memory from prior turns."

    retrieval_note = "Local retrieval found limited overlap."
    if keyword_hits:
        top_keyword = keyword_hits[0]
        retrieval_note = (
            f"Keyword retrieval top hit: {top_keyword.get('id')} "
            f"(score={top_keyword.get('score')})."
        )

    if vector_hits:
        top_vector = vector_hits[0]
        retrieval_note += (
            f" Fake-vector top hit: {top_vector.get('id')} "
            f"(score={top_vector.get('score')})."
        )

    summary = (
        f"Baseline response for {customer}: acknowledged current incident "
        f"('{incident.get('summary', 'incident context unavailable')}'). "
        f"Manual escalation drafting and fragmented retrieval still required. {retrieval_note} {continuity_note} "
        f"Session turn index: {prior_turns + 1}."
    )
    return {"summary": summary}


def _baseline_finalize(state: PipelineState) -> PipelineState:
    message = state["message"]
    local_history = state.get("local_history", [])
    local_state = state.get("local_state", {})
    prior_turns = int(local_state.get("turn_count", 0))
    memory_hits = 1 if local_history else 0
    retrieval_context = state.get("retrieval_context", {})
    keyword_hits = retrieval_context.get("keyword_hits", [])
    vector_hits = retrieval_context.get("vector_hits", [])
    docs_scanned = int(retrieval_context.get("documents_scanned", 0))

    return {
        "metrics": {
            "latency_ms": 1840,
            "prompt_tokens": 2620,
            "completion_tokens": 410,
            "retrieval_calls": 10,
            "tool_calls": 7,
            "memory_hits": memory_hits,
            "cache_hits": 0,
        },
        "context_signals": [
            "local-memory-only",
            "fragmented-retrieval",
            "manual-context-assembly",
            "baseline-json-retrieval",
            "baseline-keyword-retrieval-hit" if keyword_hits else "baseline-keyword-retrieval-empty",
            "baseline-fake-vector-hit" if vector_hits else "baseline-fake-vector-empty",
            "baseline-documents-scanned=" + str(docs_scanned),
            "message-length=" + str(len(message)),
            "session-local-memory-hit" if memory_hits else "session-local-memory-cold",
            "session-turn-index=" + str(prior_turns + 1),
        ],
    }


def _build_baseline_graph():
    builder: StateGraph[PipelineState] = StateGraph(PipelineState)
    builder.add_node("baseline_load_incident", _baseline_load_incident)
    builder.add_node("baseline_retrieve_context", _baseline_retrieve_context)
    builder.add_node("baseline_compose_summary", _baseline_compose_summary)
    builder.add_node("baseline_finalize", _baseline_finalize)
    builder.set_entry_point("baseline_load_incident")
    builder.add_edge("baseline_load_incident", "baseline_retrieve_context")
    builder.add_edge("baseline_retrieve_context", "baseline_compose_summary")
    builder.add_edge("baseline_compose_summary", "baseline_finalize")
    builder.add_edge("baseline_finalize", END)
    return builder.compile()


def _iris_load_context(state: PipelineState) -> PipelineState:
    seed = state["seed"]
    incidents = seed.get("incidents", [])
    memories = seed.get("memories", [])
    incident = incidents[0] if incidents else {"summary": "No active incidents found.", "status": "unknown"}
    memory = str(memories[0]) if memories else "No persistent customer memory available."
    return {
        "incident": incident,
        "memory": memory,
    }


def _iris_apply_event_context(state: PipelineState) -> PipelineState:
    recent_events = state.get("recent_events", [])
    latest_event = recent_events[0] if recent_events else None

    event_note = "no live event"
    if latest_event is not None:
        event_note = f"latest event {latest_event.get('event_type')}={latest_event.get('status')}"

    return {
        "latest_event": latest_event,
        "event_note": event_note,
    }


def _iris_compose_summary(state: PipelineState) -> PipelineState:
    customer = state["customer"]
    incident = state["incident"]
    memory = state["memory"]
    event_note = state["event_note"]
    summary = (
        f"IRIS response for {customer}: executive-ready escalation prepared using "
        f"shared operational context, memory ('{memory}'), and incident state "
        f"('{incident.get('status', 'unknown')}'). {event_note}."
    )
    return {"summary": summary}


def _iris_finalize(state: PipelineState) -> PipelineState:
    message = state["message"]
    latest_event = state.get("latest_event")
    return {
        "metrics": {
            "latency_ms": 760,
            "prompt_tokens": 1160,
            "completion_tokens": 330,
            "retrieval_calls": 4,
            "tool_calls": 3,
            "memory_hits": 2,
            "cache_hits": 1 if "summary" in message.lower() else 0,
        },
        "context_signals": [
            "shared-operational-context",
            "memory-hit",
            "semantic-cache-check",
            "live-event-aware" if latest_event else "no-live-event-yet",
        ],
    }


def _build_iris_graph():
    builder: StateGraph[PipelineState] = StateGraph(PipelineState)
    builder.add_node("iris_load_context", _iris_load_context)
    builder.add_node("iris_apply_event_context", _iris_apply_event_context)
    builder.add_node("iris_compose_summary", _iris_compose_summary)
    builder.add_node("iris_finalize", _iris_finalize)
    builder.set_entry_point("iris_load_context")
    builder.add_edge("iris_load_context", "iris_apply_event_context")
    builder.add_edge("iris_apply_event_context", "iris_compose_summary")
    builder.add_edge("iris_compose_summary", "iris_finalize")
    builder.add_edge("iris_finalize", END)
    return builder.compile()


_BASELINE_GRAPH = _build_baseline_graph()
_IRIS_GRAPH = _build_iris_graph()


def run_baseline_graph(
    customer: str,
    message: str,
    seed: dict[str, Any],
    local_history: list[dict[str, Any]] | None = None,
    local_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    final = _BASELINE_GRAPH.invoke(
        {
            "customer": customer,
            "message": message,
            "seed": seed,
            "local_history": local_history or [],
            "local_state": local_state or {},
        }
    )
    return {
        "summary": final["summary"],
        "metrics": final["metrics"],
        "context_signals": final["context_signals"],
    }


def run_iris_graph(
    customer: str,
    message: str,
    seed: dict[str, Any],
    recent_events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    final = _IRIS_GRAPH.invoke(
        {
            "customer": customer,
            "message": message,
            "seed": seed,
            "recent_events": recent_events or [],
        }
    )
    return {
        "summary": final["summary"],
        "metrics": final["metrics"],
        "context_signals": final["context_signals"],
    }
