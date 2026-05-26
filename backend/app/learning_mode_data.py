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


def get_learning_maf_portability_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "mapping": [
            {
                "currentComponent": "LangGraph Orchestrator",
                "mafEquivalent": "Agent Workflow / Orchestrator",
                "portabilityNotes": "Graph flow and node boundaries map directly to workflow stages.",
                "effort": "low",
            },
            {
                "currentComponent": "Support, Incident, Account, Billing, Escalation Agents",
                "mafEquivalent": "Specialized Agents",
                "portabilityNotes": "Agent responsibilities remain unchanged; only runtime wrappers are adapted.",
                "effort": "medium",
            },
            {
                "currentComponent": "Context Retriever",
                "mafEquivalent": "Shared Context Service / Tool",
                "portabilityNotes": "Keep retrieval contract stable so MAF tools can call the same packet builder.",
                "effort": "medium",
            },
            {
                "currentComponent": "Redis Agent Memory",
                "mafEquivalent": "Agent Memory Provider",
                "portabilityNotes": "Memory keys and retention policy can stay intact with a thin adapter.",
                "effort": "low",
            },
            {
                "currentComponent": "Redis Search / Vector Search / Streams / JSON / Semantic Cache",
                "mafEquivalent": "Data + Retrieval + Event Tooling",
                "portabilityNotes": "Redis remains the operational context layer regardless of orchestration framework.",
                "effort": "low",
            },
            {
                "currentComponent": "Metrics Collector",
                "mafEquivalent": "Evaluation / Telemetry Pipeline",
                "portabilityNotes": "Carry over latency/token/memory/cache signals to keep before-after proof consistent.",
                "effort": "low",
            },
        ],
        "migrationPlan": [
            "Preserve current context-packet schema as a framework-neutral contract.",
            "Port orchestration edges from LangGraph to MAF workflow stages incrementally.",
            "Keep Redis context, memory, and cache APIs stable and only swap orchestration adapters.",
            "Run baseline-vs-IRIS parity checks after each migrated stage.",
            "Cut over only after response quality and metrics remain within expected thresholds.",
        ],
        "teachingSummary": "LangGraph orchestrates and Redis operationalizes. MAF migration mostly changes orchestration plumbing, not operational context strategy.",
    }


def get_learning_context_diff_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "baseline": {
            "title": "Baseline Context Assembly",
            "summary": "Each agent rebuilds context separately, increasing prompt size and inconsistency risk.",
            "packet": {
                "customer": {
                    "name": "Acme Corp",
                    "risk_level": "high",
                    "renewal_date": "2026-07-15",
                },
                "facts": [
                    "Open sev-1 ticket exists but has partial ownership metadata.",
                    "Incident status is fetched from a separate lookup path.",
                    "No unified event freshness marker is attached.",
                ],
                "memory": [
                    "No durable cross-session memory attached by default.",
                ],
                "events": [
                    "Recent deployment update may be missing or delayed in prompt assembly.",
                ],
                "prompt_shape": "broad and repetitive",
            },
        },
        "iris": {
            "title": "IRIS Shared Context Packet",
            "summary": "Context Retriever assembles one compact, shared packet for all agents before generation.",
            "packet": {
                "customer": {
                    "name": "Acme Corp",
                    "risk_level": "high",
                    "renewal_date": "2026-07-15",
                },
                "facts": [
                    "Customer, ticket, and incident state merged through Redis Search + JSON.",
                    "Active incident timeline and severity normalized before agent reasoning.",
                    "Freshness anchored by latest operational stream event.",
                ],
                "memory": [
                    "Customer was promised executive escalation if latency issues recur.",
                    "Acme prefers concise executive communication.",
                ],
                "events": [
                    "incident_update/mitigated replay event is included in live context.",
                ],
                "prompt_shape": "compact and targeted",
            },
        },
        "narrative": [
            "Baseline rebuilds context per agent. IRIS shares one context packet across agents.",
            "Baseline misses memory continuity by default. IRIS injects durable commitments and preferences.",
            "Baseline can drift on event freshness. IRIS anchors the packet on live operational stream updates.",
            "Result: lower prompt tokens, fewer retrieval calls, and more consistent final responses.",
        ],
        "delta": {
            "prompt_tokens": {
                "baseline": 2620,
                "iris": 1160,
                "change_pct": -55.7,
            },
            "retrieval_calls": {
                "baseline": "many per agent",
                "iris": "shared pre-assembled",
            },
            "memory_continuity": {
                "baseline": "weak",
                "iris": "strong",
            },
        },
    }


def get_learning_metrics_storytelling_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "chapters": [
            {
                "id": "story-1",
                "title": "Set the baseline cost profile",
                "narrative": "Start with baseline latency and token cost to anchor the business problem.",
                "focusMetric": "baseline_cost",
                "kpi": {
                    "label": "Baseline Prompt Tokens",
                    "value": 2620,
                    "unit": "tokens",
                },
                "talkTrack": "Explain that repeated context assembly inflates prompt size before any quality gain.",
            },
            {
                "id": "story-2",
                "title": "Introduce IRIS context compression",
                "narrative": "Show how one shared context packet replaces multiple repeated retrieval passes.",
                "focusMetric": "prompt_reduction",
                "kpi": {
                    "label": "Prompt Token Reduction",
                    "value": 55.7,
                    "unit": "%",
                },
                "talkTrack": "Emphasize that this reduction comes from better context shaping, not lower answer quality.",
            },
            {
                "id": "story-3",
                "title": "Quantify latency impact",
                "narrative": "Compare baseline and IRIS latency to make responsiveness gains visible.",
                "focusMetric": "latency_delta",
                "kpi": {
                    "label": "Latency Avg Delta",
                    "value": -4.43,
                    "unit": "ms",
                },
                "talkTrack": "Frame this as user-facing speed plus lower compute time per request.",
            },
            {
                "id": "story-4",
                "title": "Show continuity and reuse",
                "narrative": "Close with memory and cache readiness as compounding efficiency multipliers.",
                "focusMetric": "continuity",
                "kpi": {
                    "label": "Memory Hits",
                    "value": "0 -> 2",
                    "unit": "per run",
                },
                "talkTrack": "Highlight that durable memory turns repeat interactions into faster, more consistent outcomes.",
            },
        ],
        "pacing": {
            "defaultStepMs": 3500,
            "recommendedAudience": "executive",
            "presentationHint": "Use auto-play for board-level demos and manual step mode for technical Q and A.",
        },
    }


def get_learning_qa_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "questions": [
            {
                "id": "qa-1",
                "category": "architecture",
                "question": "Where does LangGraph end and Redis IRIS begin?",
                "answer": "LangGraph orchestrates sequence and agent routing. Redis IRIS provides shared operational context through search, memory, vectors, streams, JSON, and cache.",
                "mappedComponents": ["langgraph", "context_retriever", "redis_search", "redis_agent_memory"],
            },
            {
                "id": "qa-2",
                "category": "performance",
                "question": "Why are tokens and latency lower with IRIS?",
                "answer": "IRIS assembles one compact context packet before agent reasoning, reducing repeated retrieval and duplicated prompt content.",
                "mappedComponents": ["context_retriever", "semantic_cache", "metrics_collector"],
            },
            {
                "id": "qa-3",
                "category": "reliability",
                "question": "How does the system stay aligned with live operational changes?",
                "answer": "Redis Streams and shared context retrieval keep incident and event updates synchronized before response generation.",
                "mappedComponents": ["redis_streams", "context_retriever", "incident_agent"],
            },
            {
                "id": "qa-4",
                "category": "portability",
                "question": "Can this architecture move to MAF without redesigning data strategy?",
                "answer": "Yes. Orchestration plumbing changes, but Redis context contracts, memory strategy, and retrieval interfaces stay intact.",
                "mappedComponents": ["langgraph", "context_retriever", "redis_json", "metrics_collector"],
            },
            {
                "id": "qa-5",
                "category": "operations",
                "question": "What makes this more production-ready than vector-only RAG?",
                "answer": "It combines structured state, semantic retrieval, durable memory, live events, and caching in one shared operational context layer.",
                "mappedComponents": ["redis_search", "redis_vector_search", "redis_agent_memory", "redis_streams", "semantic_cache"],
            },
        ],
        "presenterHint": "Start with architecture questions, then move to performance and portability based on audience depth.",
    }


def get_learning_summary_handout_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "title": "Operational AI with Redis IRIS - Learning Summary",
        "audience": "Stakeholders, platform leaders, and customer operations teams",
        "generatedFor": "Post-demo follow-up",
        "sections": [
            {
                "id": "summary-1",
                "heading": "Core Story",
                "points": [
                    "Before: agents coordinate through prompts and fragmented retrieval.",
                    "After: agents coordinate through shared operational context with Redis IRIS.",
                    "LangGraph orchestrates workflows while Redis IRIS operationalizes context and memory.",
                ],
            },
            {
                "id": "summary-2",
                "heading": "Measured Outcomes",
                "points": [
                    "Prompt tokens reduced from 2620 to 1160 (-55.7%).",
                    "Average latency improved by 4.43 ms in benchmark snapshots.",
                    "Memory continuity improved from weak session-local behavior to durable cross-session recall.",
                ],
            },
            {
                "id": "summary-3",
                "heading": "Operational Capabilities",
                "points": [
                    "Redis Search and RedisJSON provide precise structured context retrieval.",
                    "Redis Vector Search adds similar-incident context for semantic grounding.",
                    "Redis Streams keeps agents aligned with live operational events.",
                    "Semantic cache reduces repeated LLM cost and response latency.",
                ],
            },
            {
                "id": "summary-4",
                "heading": "Portability and Next Steps",
                "points": [
                    "The context contract can migrate to MAF with minimal data-layer redesign.",
                    "Next enhancements: annotation modes, fallback scripts, and quiz checkpoints.",
                    "Recommendation: continue with production hardening and broader benchmark scenarios.",
                ],
            },
        ],
        "takeaways": [
            "Shared operational state outperforms prompt-only coordination in production-like workloads.",
            "IRIS improves consistency, efficiency, and real-time awareness across multi-agent workflows.",
            "The architecture is explainable to both technical and executive audiences through Learning Mode.",
        ],
        "exportMeta": {
            "format": "json",
            "filename": "learning-summary-handout.json",
            "version": "1.0",
        },
    }


def get_learning_presenter_annotations_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "title": "Presenter Annotation Mode",
        "defaultTrack": "executive",
        "tracks": [
            {
                "id": "executive",
                "label": "Executive",
                "description": "Business-impact framing focused on risk, cost, and stakeholder outcomes.",
                "sections": [
                    {
                        "id": "exec-1",
                        "topic": "Architecture Difference",
                        "talkTrack": "Baseline pipelines reassemble context repeatedly. IRIS uses one shared operational context layer that improves consistency and response quality.",
                        "focusMetrics": ["prompt_tokens", "latency_ms_avg"],
                    },
                    {
                        "id": "exec-2",
                        "topic": "Operational Readiness",
                        "talkTrack": "Live event awareness and memory continuity reduce escalation noise and improve customer trust in high-risk scenarios.",
                        "focusMetrics": ["memory_hits", "cache_hits"],
                    },
                    {
                        "id": "exec-3",
                        "topic": "Investment Narrative",
                        "talkTrack": "The same Redis context strategy is portable to MAF, so this investment supports both current delivery and future platform alignment.",
                        "focusMetrics": ["portability_risk", "migration_effort"],
                    },
                ],
            },
            {
                "id": "technical",
                "label": "Technical",
                "description": "Implementation framing focused on retrieval paths, context contracts, and orchestration boundaries.",
                "sections": [
                    {
                        "id": "tech-1",
                        "topic": "Flow Composition",
                        "talkTrack": "LangGraph handles orchestration and edge transitions. Context Retriever builds packet state using Redis Search, JSON, vectors, streams, and memory adapters.",
                        "focusMetrics": ["retrieval_calls", "context_packet_size"],
                    },
                    {
                        "id": "tech-2",
                        "topic": "State and Recall",
                        "talkTrack": "Agent memory and semantic cache reduce repeated tool invocations while preserving continuity across sessions and agents.",
                        "focusMetrics": ["memory_hits", "cache_hits", "tool_calls"],
                    },
                    {
                        "id": "tech-3",
                        "topic": "Portability Contract",
                        "talkTrack": "Keep the context packet schema and Redis interfaces stable, then swap orchestration adapters for MAF migration with minimal data-plane disruption.",
                        "focusMetrics": ["contract_stability", "adapter_effort"],
                    },
                ],
            },
        ],
        "presenterHint": "Use executive track for business stakeholders first, then switch to technical track for implementation Q and A.",
    }


def get_learning_fallback_scripts_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "title": "Guided Fallback Script Cards",
        "defaultScenarioId": "fallback-1",
        "scenarios": [
            {
                "id": "fallback-1",
                "label": "No live stream updates",
                "trigger": "Live incident events are not arriving during the demo.",
                "script": [
                    "We are switching to fallback mode while keeping the architecture view unchanged.",
                    "In production, Redis Streams supplies this event feed. Here I will use the prepared timeline snapshot.",
                    "Focus on the same outcome: shared context freshness and synchronized agent decisions.",
                ],
                "recommendedPanel": "Context Diff Narrative",
            },
            {
                "id": "fallback-2",
                "label": "Replay API unavailable",
                "trigger": "Replay execution endpoint is temporarily unavailable.",
                "script": [
                    "We can continue with pre-scripted progression cards that mirror the same operational steps.",
                    "Each step still maps to Redis context retrieval, memory continuity, and cache-aware response generation.",
                    "This keeps the business and architecture narrative consistent without relying on live controls.",
                ],
                "recommendedPanel": "Metrics Storytelling Mode",
            },
            {
                "id": "fallback-3",
                "label": "Backend latency spike",
                "trigger": "Response latency is temporarily high in the environment.",
                "script": [
                    "We will use benchmark snapshots captured from stable runs to compare baseline and IRIS behavior.",
                    "The important point is directional proof: IRIS reduces prompt bloat and retrieval duplication.",
                    "After the session, we can reproduce the run with full telemetry for trace-level inspection.",
                ],
                "recommendedPanel": "Exportable Learning Summary Handout",
            },
            {
                "id": "fallback-4",
                "label": "Frontend interaction issue",
                "trigger": "Interactive controls or diagram gestures are degraded during presentation.",
                "script": [
                    "I will continue in narrated mode using static checkpoints from the same architecture model.",
                    "LangGraph orchestration boundaries and Redis IRIS responsibilities remain identical.",
                    "This fallback preserves learning objectives while we avoid relying on transient UI behavior.",
                ],
                "recommendedPanel": "Presenter Annotation Mode",
            },
        ],
        "presenterHint": "Use fallback cards only when a live dependency is unstable; keep the core before-vs-after narrative unchanged.",
    }


def get_learning_quiz_checkpoints_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "title": "Architecture Quiz Checkpoints",
        "defaultCheckpointId": "quiz-1",
        "checkpoints": [
            {
                "id": "quiz-1",
                "chapter": "Before vs After Framing",
                "prompt": "Which layer is responsible for shared operational state across agents?",
                "options": [
                    "LangGraph orchestrator",
                    "Redis IRIS context layer",
                    "Frontend replay panel",
                    "Metrics storytelling controller",
                ],
                "correctOptionIndex": 1,
                "explanation": "LangGraph coordinates workflow transitions, while Redis IRIS provides the shared operational state used by all agents.",
                "relatedComponents": ["Context Retriever", "RedisJSON", "Redis Agent Memory"],
            },
            {
                "id": "quiz-2",
                "chapter": "Context Retrieval",
                "prompt": "What is the best reason prompt tokens decrease with IRIS enabled?",
                "options": [
                    "The user message is shortened before inference",
                    "The LLM runs with fewer output tokens only",
                    "IRIS assembles compact relevant context instead of repeating broad retrieval",
                    "Replay templates disable ticket and incident lookups",
                ],
                "correctOptionIndex": 2,
                "explanation": "IRIS composes a compact context packet from structured facts, memory, vectors, and events, reducing duplicated prompt material.",
                "relatedComponents": ["Redis Search", "Redis Vector Search", "Semantic Cache"],
            },
            {
                "id": "quiz-3",
                "chapter": "Live Operations",
                "prompt": "Which Redis capability keeps agents aware of latest incident updates during the demo?",
                "options": [
                    "Redis Streams",
                    "RedisJSON only",
                    "LangCache only",
                    "Benchmark trend history",
                ],
                "correctOptionIndex": 0,
                "explanation": "Redis Streams carries operational event updates that are consumed by the app and reflected in shared context.",
                "relatedComponents": ["Redis Streams", "Event Bus", "Live Events Panel"],
            },
        ],
        "presenterHint": "Use one checkpoint between chapters to keep the audience engaged and reinforce why IRIS changes outcomes.",
    }


def get_learning_qa_anchors_payload() -> dict[str, Any]:
    return {
        "status": "ok",
        "title": "Live Q and A Answer Anchors",
        "anchors": [
            {
                "id": "anchor-1",
                "question": "Where does LangGraph end and Redis IRIS begin?",
                "answerSummary": "LangGraph orchestrates workflow steps while IRIS assembles and serves shared operational context.",
                "sectionId": "architecture-overview",
                "targetLabel": "Architecture Overview",
            },
            {
                "id": "anchor-2",
                "question": "Why do tokens go down with IRIS?",
                "answerSummary": "IRIS sends compact context packets instead of repeated, broad retrieval payloads.",
                "sectionId": "context-diff-narrative",
                "targetLabel": "Context Diff Narrative",
            },
            {
                "id": "anchor-3",
                "question": "How do you prove memory continuity?",
                "answerSummary": "Use context packet memory hits and live event context to show cross-session recall.",
                "sectionId": "context-packet-viewer",
                "targetLabel": "Context Packet Viewer",
            },
            {
                "id": "anchor-4",
                "question": "What proves business impact quickly?",
                "answerSummary": "Walk through chapter KPIs that connect lower tokens and latency to operational outcomes.",
                "sectionId": "metrics-storytelling-mode",
                "targetLabel": "Metrics Storytelling Mode",
            },
            {
                "id": "anchor-5",
                "question": "How do we handle unstable live demo conditions?",
                "answerSummary": "Switch to guided fallback scripts while keeping architecture and outcomes narrative unchanged.",
                "sectionId": "guided-fallback-script-cards",
                "targetLabel": "Guided Fallback Script Cards",
            },
        ],
        "presenterHint": "Use anchors to jump to the strongest proof panel in under five seconds during audience interruptions.",
    }