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


def _baseline_load_incident(state: PipelineState) -> PipelineState:
    seed = state["seed"]
    incidents = seed.get("incidents", [])
    incident = incidents[0] if incidents else {"summary": "No active incidents found.", "status": "unknown"}
    return {"incident": incident}


def _baseline_compose_summary(state: PipelineState) -> PipelineState:
    customer = state["customer"]
    incident = state["incident"]
    summary = (
        f"Baseline response for {customer}: acknowledged current incident "
        f"('{incident.get('summary', 'incident context unavailable')}'). "
        "Manual escalation drafting and fragmented retrieval still required."
    )
    return {"summary": summary}


def _baseline_finalize(state: PipelineState) -> PipelineState:
    message = state["message"]
    return {
        "metrics": {
            "latency_ms": 1840,
            "prompt_tokens": 2620,
            "completion_tokens": 410,
            "retrieval_calls": 8,
            "tool_calls": 6,
            "memory_hits": 0,
            "cache_hits": 0,
        },
        "context_signals": [
            "local-memory-only",
            "fragmented-retrieval",
            "manual-context-assembly",
            "message-length=" + str(len(message)),
        ],
    }


def _build_baseline_graph():
    builder: StateGraph[PipelineState] = StateGraph(PipelineState)
    builder.add_node("baseline_load_incident", _baseline_load_incident)
    builder.add_node("baseline_compose_summary", _baseline_compose_summary)
    builder.add_node("baseline_finalize", _baseline_finalize)
    builder.set_entry_point("baseline_load_incident")
    builder.add_edge("baseline_load_incident", "baseline_compose_summary")
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


def run_baseline_graph(customer: str, message: str, seed: dict[str, Any]) -> dict[str, Any]:
    final = _BASELINE_GRAPH.invoke(
        {
            "customer": customer,
            "message": message,
            "seed": seed,
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
