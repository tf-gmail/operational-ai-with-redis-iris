from __future__ import annotations

from typing import Any


_ARCHITECTURE_NODES: list[dict[str, Any]] = [
    {
        "id": "user",
        "label": "User",
        "category": "user",
        "shortDescription": "Starts the workflow with an operational question or escalation.",
        "responsibilities": ["submit request", "compare baseline and IRIS outcomes"],
        "beforeIRIS": ["repeats context in every session"],
        "afterIRIS": ["benefits from shared state and shorter prompts"],
        "demoValue": ["anchors the request flow", "makes contrast easy to explain"],
    },
    {
        "id": "frontend",
        "label": "Frontend",
        "category": "frontend",
        "shortDescription": "Displays the dashboard, replay events, metrics, and learning mode views.",
        "responsibilities": ["render UI", "show live events", "explain architecture"],
        "beforeIRIS": ["can only show fragmented tool output"],
        "afterIRIS": ["can visualize shared context and live state"],
        "demoValue": ["presentation layer", "educational entry point"],
    },
    {
        "id": "backend_api",
        "label": "Backend API",
        "category": "orchestrator",
        "shortDescription": "Accepts requests, exposes runtime endpoints, and serves learning payloads.",
        "responsibilities": ["accept REST requests", "publish replay APIs", "serve learning data"],
        "beforeIRIS": ["mostly forwards requests to workflow handlers"],
        "afterIRIS": ["also exposes stateful operational APIs and explainers"],
        "demoValue": ["integration point for UI and agents"],
    },
    {
        "id": "langgraph",
        "label": "LangGraph Orchestrator",
        "category": "orchestrator",
        "shortDescription": "Coordinates workflow steps and agent sequencing.",
        "responsibilities": ["route execution", "maintain graph state", "combine outputs"],
        "beforeIRIS": ["coordinates agents without durable shared operational state"],
        "afterIRIS": ["operates on compact context assembled by IRIS"],
        "demoValue": ["shows orchestration is distinct from storage"],
    },
    {
        "id": "support_agent",
        "label": "Support Agent",
        "category": "agent",
        "shortDescription": "Focuses on ticket state, customer pain, and escalation urgency.",
        "responsibilities": ["review support tickets", "summarize active customer issues"],
        "demoValue": ["illustrates domain-specific reasoning"],
    },
    {
        "id": "incident_agent",
        "label": "Incident Agent",
        "category": "agent",
        "shortDescription": "Interprets outage and service-health context.",
        "responsibilities": ["inspect incidents", "track mitigation status"],
        "demoValue": ["connects incident timelines to customer impact"],
    },
    {
        "id": "account_agent",
        "label": "Account Agent",
        "category": "agent",
        "shortDescription": "Frames renewal risk and stakeholder management concerns.",
        "responsibilities": ["assess ARR risk", "surface renewal context"],
        "demoValue": ["connects ops issues to revenue risk"],
    },
    {
        "id": "billing_agent",
        "label": "Billing Agent",
        "category": "agent",
        "shortDescription": "Adds contract, SLA, and credit implications.",
        "responsibilities": ["surface SLA obligations", "highlight billing actions"],
        "demoValue": ["broadens explanation beyond incidents"],
    },
    {
        "id": "escalation_agent",
        "label": "Escalation Agent",
        "category": "agent",
        "shortDescription": "Produces executive-ready coordination output.",
        "responsibilities": ["draft action plan", "prepare executive summary"],
        "demoValue": ["shows cross-agent coordination outcome"],
    },
    {
        "id": "context_retriever",
        "label": "Context Retriever",
        "category": "redis",
        "shortDescription": "Assembles the compact operational packet that agents use.",
        "responsibilities": ["resolve customer state", "load incidents and tickets", "merge memory"],
        "beforeIRIS": ["replaced by repeated local lookups"],
        "afterIRIS": ["centralizes retrieval across Redis capabilities"],
        "demoValue": ["makes IRIS feel like a real context layer"],
    },
    {
        "id": "redis_agent_memory",
        "label": "Redis Agent Memory",
        "category": "redis",
        "shortDescription": "Stores durable short-term and cross-session customer memory.",
        "responsibilities": ["recall promises", "persist new notes"],
        "demoValue": ["explains continuity and personalization"],
    },
    {
        "id": "redis_search",
        "label": "Redis Search",
        "category": "redis",
        "shortDescription": "Finds structured customer, ticket, and incident state.",
        "responsibilities": ["filter operational records", "support exact retrieval"],
        "demoValue": ["shows why IRIS is more than document retrieval"],
    },
    {
        "id": "redis_vector_search",
        "label": "Redis Vector Search",
        "category": "redis",
        "shortDescription": "Finds semantically similar incidents and cases.",
        "responsibilities": ["retrieve similar incidents", "support semantic context"],
        "demoValue": ["shows semantic reasoning without external model dependencies"],
    },
    {
        "id": "redis_streams",
        "label": "Redis Streams",
        "category": "redis",
        "shortDescription": "Persists and replays operational events for live awareness.",
        "responsibilities": ["capture live events", "support replay continuity"],
        "demoValue": ["explains real-time state updates"],
    },
    {
        "id": "redis_json",
        "label": "RedisJSON",
        "category": "redis",
        "shortDescription": "Stores shared customer, ticket, and incident records as operational state.",
        "responsibilities": ["persist structured data", "support low-latency access"],
        "demoValue": ["explains shared state storage layer"],
    },
    {
        "id": "semantic_cache",
        "label": "Semantic Cache",
        "category": "redis",
        "shortDescription": "Reuses repeated or similar answers to reduce latency and tokens.",
        "responsibilities": ["check repeated queries", "store reusable responses"],
        "demoValue": ["explains cost and latency reduction"],
    },
    {
        "id": "llm",
        "label": "LLM",
        "category": "llm",
        "shortDescription": "Generates the final grounded response from compact shared context.",
        "responsibilities": ["produce final answer", "use agent-provided context"],
        "demoValue": ["final reasoning stage"],
    },
    {
        "id": "metrics_collector",
        "label": "Metrics Collector",
        "category": "metrics",
        "shortDescription": "Captures latency, token, and retrieval signals for comparison views.",
        "responsibilities": ["record benchmark metrics", "feed UI visualizations"],
        "demoValue": ["supports measurable before/after proof"],
    },
]

_ARCHITECTURE_EDGES: list[dict[str, str]] = [
    {"id": "e-user-frontend", "source": "user", "target": "frontend", "kind": "request"},
    {"id": "e-frontend-backend", "source": "frontend", "target": "backend_api", "kind": "request"},
    {"id": "e-backend-langgraph", "source": "backend_api", "target": "langgraph", "kind": "orchestration"},
    {"id": "e-langgraph-context", "source": "langgraph", "target": "context_retriever", "kind": "context"},
    {"id": "e-context-json", "source": "context_retriever", "target": "redis_json", "kind": "lookup"},
    {"id": "e-context-search", "source": "context_retriever", "target": "redis_search", "kind": "lookup"},
    {"id": "e-context-vector", "source": "context_retriever", "target": "redis_vector_search", "kind": "lookup"},
    {"id": "e-context-memory", "source": "context_retriever", "target": "redis_agent_memory", "kind": "memory"},
    {"id": "e-context-streams", "source": "context_retriever", "target": "redis_streams", "kind": "events"},
    {"id": "e-context-cache", "source": "context_retriever", "target": "semantic_cache", "kind": "cache"},
    {"id": "e-langgraph-support", "source": "langgraph", "target": "support_agent", "kind": "agent"},
    {"id": "e-langgraph-incident", "source": "langgraph", "target": "incident_agent", "kind": "agent"},
    {"id": "e-langgraph-account", "source": "langgraph", "target": "account_agent", "kind": "agent"},
    {"id": "e-langgraph-billing", "source": "langgraph", "target": "billing_agent", "kind": "agent"},
    {"id": "e-langgraph-escalation", "source": "langgraph", "target": "escalation_agent", "kind": "agent"},
    {"id": "e-escalation-llm", "source": "escalation_agent", "target": "llm", "kind": "generation"},
    {"id": "e-llm-metrics", "source": "llm", "target": "metrics_collector", "kind": "metrics"},
    {"id": "e-metrics-frontend", "source": "metrics_collector", "target": "frontend", "kind": "display"},
]

_BASELINE_FLOW: list[dict[str, Any]] = [
    {
        "id": "baseline-1",
        "title": "User submits request",
        "description": "The request enters the system without shared operational memory.",
        "activeNodes": ["user", "frontend", "backend_api"],
        "activeEdges": ["e-user-frontend", "e-frontend-backend"],
    },
    {
        "id": "baseline-2",
        "title": "LangGraph coordinates local retrieval",
        "description": "The orchestrator routes work, but each agent still depends on repeated local context assembly.",
        "activeNodes": ["backend_api", "langgraph", "support_agent", "incident_agent"],
        "activeEdges": ["e-backend-langgraph", "e-langgraph-support", "e-langgraph-incident"],
        "metricChanges": {"retrieval_calls": "+many", "memory_hits": 0},
    },
    {
        "id": "baseline-3",
        "title": "LLM receives larger fragmented prompt",
        "description": "Without shared context services, prompt size and duplication increase.",
        "activeNodes": ["account_agent", "billing_agent", "escalation_agent", "llm"],
        "activeEdges": ["e-langgraph-account", "e-langgraph-billing", "e-langgraph-escalation", "e-escalation-llm"],
        "metricChanges": {"prompt_size": "large", "cache_hit": "none"},
    },
    {
        "id": "baseline-4",
        "title": "Metrics show weaker efficiency",
        "description": "The UI can show the result, but latency and token counts remain higher.",
        "activeNodes": ["llm", "metrics_collector", "frontend"],
        "activeEdges": ["e-llm-metrics", "e-metrics-frontend"],
        "metricChanges": {"latency_ms": "higher", "prompt_tokens": "higher"},
    },
]

_IRIS_FLOW: list[dict[str, Any]] = [
    {
        "id": "iris-1",
        "title": "User submits request",
        "description": "The request enters the same UI and backend surface, ready for IRIS enrichment.",
        "activeNodes": ["user", "frontend", "backend_api"],
        "activeEdges": ["e-user-frontend", "e-frontend-backend"],
    },
    {
        "id": "iris-2",
        "title": "Context Retriever assembles shared state",
        "description": "Redis-backed services combine structured search, memory, vector search, streams, and cache checks.",
        "activeNodes": [
            "backend_api",
            "langgraph",
            "context_retriever",
            "redis_json",
            "redis_search",
            "redis_vector_search",
            "redis_agent_memory",
            "redis_streams",
            "semantic_cache",
        ],
        "activeEdges": [
            "e-backend-langgraph",
            "e-langgraph-context",
            "e-context-json",
            "e-context-search",
            "e-context-vector",
            "e-context-memory",
            "e-context-streams",
            "e-context-cache",
        ],
        "metricChanges": {"retrieval_calls": "fewer", "memory_hits": "+1", "cache_check": "performed"},
        "contextPreview": {
            "customer": "Acme Corp",
            "memory": ["Customer was promised executive escalation if latency issues recur."],
            "active_incidents": ["Search API p95 latency exceeded 1.8s after deployment."],
            "similar_incidents": ["Comparable latency incident retrieved via vector search."],
        },
    },
    {
        "id": "iris-3",
        "title": "Agents collaborate on compact context",
        "description": "Agents reason over a shared packet instead of rebuilding separate views.",
        "activeNodes": [
            "support_agent",
            "incident_agent",
            "account_agent",
            "billing_agent",
            "escalation_agent",
            "llm",
        ],
        "activeEdges": ["e-langgraph-support", "e-langgraph-incident", "e-langgraph-account", "e-langgraph-billing", "e-langgraph-escalation", "e-escalation-llm"],
        "metricChanges": {"prompt_size": "compact", "shared_state": "enabled"},
    },
    {
        "id": "iris-4",
        "title": "Metrics capture lower-cost outcome",
        "description": "The UI can now explain why latency and token counts drop in the IRIS path.",
        "activeNodes": ["llm", "metrics_collector", "frontend"],
        "activeEdges": ["e-llm-metrics", "e-metrics-frontend"],
        "metricChanges": {"latency_ms": "lower", "prompt_tokens": "lower", "cache_hit": "possible"},
    },
]

_COMPONENT_DETAIL_OVERRIDES: dict[str, dict[str, Any]] = {
    "langgraph": {
        "whatItDoesNotDo": [
            "store long-term operational context",
            "maintain low-latency shared memory by itself",
            "replace Redis Search, Vector, Streams, or JSON capabilities",
        ]
    },
    "context_retriever": {
        "whatItDoesNotDo": [
            "replace agent reasoning",
            "decide final customer messaging",
            "store durable memory without Redis backends",
        ]
    },
    "semantic_cache": {
        "whatItDoesNotDo": [
            "replace grounding on fresh incident context",
            "apply when query semantics are materially different",
        ]
    },
}


def _build_component_details() -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}

    for node in _ARCHITECTURE_NODES:
        node_id = str(node["id"])
        category = str(node["category"])
        before_value = list(node.get("beforeIRIS") or ["Fragmented retrieval and local context assembly."])
        after_value = list(node.get("afterIRIS") or ["Uses shared operational context where applicable."])

        detail: dict[str, Any] = {
            "id": node_id,
            "label": node["label"],
            "category": category,
            "role": node["shortDescription"],
            "whatItDoes": list(node.get("responsibilities") or []),
            "whatItDoesNotDo": ["operate as a standalone full system without orchestration context"],
            "whyRedisMatters": [],
            "beforeValue": before_value,
            "afterValue": after_value,
            "demoTalkTrack": list(node.get("demoValue") or []),
        }

        if category == "redis":
            detail["whyRedisMatters"] = [
                "low-latency shared operational state",
                "consistent cross-agent context",
                "live update and retrieval capabilities",
            ]

        overrides = _COMPONENT_DETAIL_OVERRIDES.get(node_id)
        if overrides:
            detail.update(overrides)

        details[node_id] = detail

    return details


_COMPONENT_DETAILS = _build_component_details()


def get_learning_architecture_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "nodes": _ARCHITECTURE_NODES,
        "edges": _ARCHITECTURE_EDGES,
        "count": {
            "nodes": len(_ARCHITECTURE_NODES),
            "edges": len(_ARCHITECTURE_EDGES),
        },
    }


def get_learning_flow_payload(mode: str) -> dict[str, Any]:
    if mode == "baseline":
        steps = _BASELINE_FLOW
        summary = "Baseline path shows fragmented retrieval, repeated context assembly, and larger prompts."
    elif mode == "iris":
        steps = _IRIS_FLOW
        summary = "IRIS path shows shared operational context, compact context packets, and lower-cost execution."
    else:
        return {
            "status": "not_found",
            "details": f"Unknown learning flow mode: {mode}",
        }

    return {
        "status": "ok",
        "mode": mode,
        "summary": summary,
        "steps": steps,
        "count": len(steps),
    }


def get_learning_component_payload(component_id: str) -> dict[str, Any]:
    component = _COMPONENT_DETAILS.get(component_id)
    if component is None:
        return {
            "status": "not_found",
            "details": f"Unknown learning component: {component_id}",
        }

    return {
        "status": "ok",
        "component": component,
    }


def get_learning_context_packet_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "packet": {
            "customer": {
                "name": "Acme Corp",
                "arr": 480000,
                "renewal_date": "2026-07-15",
                "risk_level": "high",
                "health_score": 41,
            },
            "structured_facts": [
                "Search API p95 latency exceeded 1.8s after deployment.",
                "Active incident state: investigating.",
                "Open support ticket severity: sev-1.",
            ],
            "memory_hits": [
                "Customer was promised executive escalation if latency issues recur.",
                "Acme prefers concise executive communication.",
            ],
            "semantic_matches": [
                {
                    "incident_id": "inc-2026-0311",
                    "similarity": 0.88,
                    "summary": "Prior latency spike after search indexing rollout.",
                }
            ],
            "live_events": [
                {
                    "event_type": "deployment_event",
                    "status": "completed",
                    "message": "Replay control validation event.",
                }
            ],
            "prompt_estimate": {
                "baseline_prompt_tokens": 2620,
                "iris_prompt_tokens": 1160,
                "savings_tokens": 1460,
                "savings_pct": 55.7,
            },
        },
    }


def get_learning_metrics_education_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "metrics": {
            "baseline": {
                "latency_ms_avg": 6.61,
                "latency_ms_p95": 15.89,
                "prompt_tokens_avg": 2620,
                "memory_hits": 0,
                "cache_hits": 0,
            },
            "iris": {
                "latency_ms_avg": 2.18,
                "latency_ms_p95": 2.33,
                "prompt_tokens_avg": 1160,
                "memory_hits": 2,
                "cache_hits": 0,
            },
            "education": [
                {
                    "title": "Why tokens decrease",
                    "explanation": "IRIS sends a compact shared packet to the LLM instead of repeating context per agent.",
                },
                {
                    "title": "Why latency decreases",
                    "explanation": "Redis-backed retrieval avoids repeated assembly work and reduces orchestration overhead.",
                },
                {
                    "title": "Why memory hits matter",
                    "explanation": "Remembered commitments make responses immediately actionable without extra prompts.",
                },
                {
                    "title": "Why cache hits matter",
                    "explanation": "Repeated or similar questions can be answered faster and cheaper from semantic cache.",
                },
                {
                    "title": "Why real-time state matters",
                    "explanation": "Live events keep the answer aligned with what is happening right now, not stale snapshots.",
                },
            ],
        },
    }