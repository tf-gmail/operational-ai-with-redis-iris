# Productionizing LangGraph Agents with Redis IRIS

# Complete Execution Plan

## Vision

Build a production-style multi-agent customer operations system using:

- LangGraph
- Redis IRIS concepts
- Redis Search
- RedisJSON
- Redis Streams
- Redis Agent Memory
- Semantic caching
- Shared operational context

The project demonstrates:

1. Why current agentic stacks break in production
2. Why operational context matters more than simple RAG
3. How Redis IRIS improves LangGraph-based systems
4. How agents become stateful through shared operational context
5. How the architecture later ports to Microsoft Agent Framework (MAF)

---

# Execution Tracker

## Current Sprint (Sprint 1)

Goal: deliver the first runnable end-to-end foundation with visible Baseline vs IRIS path stubs.

### Sprint 1 Checklist

- [x] Create top-level repository structure
- [x] Add CI skeleton
- [x] Add Docker Compose skeleton (frontend, backend, redis)
- [x] Add minimal backend service with health endpoint
- [x] Add minimal frontend shell with backend health check
- [x] Add cross-platform local dev startup scripts
- [x] Add Redis capability verification script
- [x] Verify Docker Compose runtime end-to-end
- [x] Add first baseline request endpoint
- [x] Add first IRIS request endpoint
- [x] Add initial Baseline vs IRIS comparison cards in frontend shell

## Current Execution Plan (Live Events Slice)

1. Add backend WebSocket endpoint for live operational events.
2. Add backend event injection endpoint for demo/replay controls.
3. Add frontend live events panel with WebSocket client.
4. Add lightweight UI controls to inject sample events.
5. Validate runtime behavior and record evidence in this document.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Orchestration + Seed + Benchmark Slice)

1. Move baseline and IRIS response construction into dedicated orchestration handlers.
2. Add deterministic Acme seed dataset in data/ for repeatable local demos.
3. Wire backend endpoints to use orchestration handlers and seed data.
4. Add a first benchmark harness script for baseline vs IRIS endpoint comparisons.
5. Run runtime and syntax checks; record outcomes in this document.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (CI + Dataset Generator + Graph Starter Slice)

1. Add CI smoke workflow commands for container-based Redis verification and benchmark execution.
2. Add deterministic customer dataset generator script and generated multi-customer fixture.
3. Introduce a backend graph-style node pipeline module to start replacing orchestration stubs.
4. Wire backend workflows to use graph-style pipeline execution for baseline and IRIS paths.
5. Run syntax/runtime checks and update this tracker with completion evidence.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (CI Trigger Split + Linked Data + Full LangGraph Slice)

1. Split CI into quick smoke and extended performance scenarios with separate triggers.
2. Expand synthetic data generation to emit linked customers, stakeholders, tickets, and incidents.
3. Replace custom graph-style pipeline with full LangGraph StateGraph nodes and edges.
4. Wire workflow handlers to the LangGraph runtime and remove custom pipeline dependency.
5. Run syntax/runtime/benchmark checks and update this tracker with completion evidence.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Replay Controls + Event Templates + Timeline Slice)

1. Add replay controls UI with play, pause, next-step, and reset behavior.
2. Add multiple event templates for operational replay scenarios.
3. Add playback timeline visualization with pending/active/completed step states.
4. Wire timeline actions to live event injection endpoint and WebSocket feed.
5. Run frontend/runtime checks and update this tracker with completion evidence.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Benchmark Trend Snapshots + Regression Gate Slice)

1. Add benchmark trend snapshot script that appends timestamped metrics from latest benchmark outputs.
2. Add regression gate script with configurable thresholds for latency and token regressions.
3. Add baseline snapshot artifact used by regression checks in CI and local runs.
4. Wire smoke CI flow to generate trend snapshot and enforce regression gate.
5. Run validation checks and update this tracker with completion evidence.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Concurrent-Session Benchmark Slice)

1. Add concurrent benchmark harness script with configurable worker and round counts.
2. Capture latency/token/error metrics for baseline and IRIS under concurrent load.
3. Add output artifact path for concurrent benchmark reports.
4. Wire extended CI flow to execute concurrent benchmark scenario.
5. Run validation checks and update this tracker with completion evidence.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Epic 4 Core Tools Integration Slice)

Epic/Task Reference:

- EPIC 4 — Redis IRIS Integration
- Task 4.1 — RedisJSON Operational State
- Task 4.4 — Redis Agent Memory
- Task 4.5 — Shared Operational Context
- Task 4.7 — Semantic Cache

1. Add backend Redis IRIS tooling module for RDI-style continuous data sync, context retrieval, agent memory, and LangCache behavior.
2. Wire IRIS workflow path to use Redis Context Retriever and Agent Memory enrichment before graph execution.
3. Wire IRIS workflow path to use Redis LangCache for response reuse on repeated prompts.
4. Add API endpoints for RDI sync/status control to keep generated data continuously integrated.
5. Run validation checks and update tracker evidence + Epic 4 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (FT.SEARCH Context + Timeline Progression Slice)

Epic/Task Reference:

- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.4 — Incident Generator
- Task 2.7 — Event Stream Generator
- EPIC 4 — Redis IRIS Integration
- Task 4.2 — Redis Search
- Task 4.5 — Shared Operational Context

1. Extend synthetic generator with timeline progression and recurring incident/ticket state transitions.
2. Emit replayable operational event stream entries from generated ticket/incident timelines.
3. Add Redis FT.SEARCH indexing for customer, ticket, and incident operational state.
4. Switch IRIS context retriever from key-list lookups to FT.SEARCH-based retrieval paths.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Backend Replay API + Template Discovery Slice)

Epic/Task Reference:

- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.7 — Event Stream Generator
- EPIC 4 — Redis IRIS Integration
- Task 4.6 — Redis Streams
- EPIC 5 — Modern UI and UX
- Task 5.5 — Replay Events UI

1. Add backend replay template catalog module to centralize server-owned replay scenarios.
2. Add backend API endpoints to discover replay templates and execute replay timelines from server side.
3. Persist manually injected and replay-generated events into Redis Streams for operational event continuity.
4. Add replay run lifecycle endpoints (status + cancel) for timeline execution observability.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Benchmark Trend Visualization Slice)

Epic/Task Reference:

- EPIC 5 — Modern UI and UX
- Task 5.3 — Metrics Visualization
- Task 5.1 — Main Dashboard Layout
- EPIC 6 — Benchmarking and Proof
- Task 6.1 — Benchmark Harness

1. Add backend benchmark trend history API endpoint for dashboard consumption.
2. Add frontend benchmark trend panel that visualizes baseline vs IRIS trend snapshots.
3. Add trend KPI summaries for latency and token deltas from latest snapshot.
4. Integrate trend panel into main dashboard shell with responsive layout behavior.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Regression Threshold Profiles Slice)

Epic/Task Reference:

- EPIC 6 — Benchmarking and Proof
- Task 6.1 — Benchmark Harness
- Task 6.2 — Token Measurement
- Task 6.3 — Latency Measurement

1. Add strict/normal/lenient threshold profiles to regression gate policy.
2. Keep per-metric CLI overrides for latency, p95, and prompt-token thresholds.
3. Wire smoke CI regression gate to use explicit profile policy.
4. Update runbook docs with profile usage examples.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (CI Benchmark Artifact Upload Slice)

Epic/Task Reference:

- EPIC 6 — Benchmarking and Proof
- Task 6.1 — Benchmark Harness

1. Add CI artifact upload step for smoke benchmark outputs.
2. Add CI artifact upload step for extended and concurrent benchmark outputs.
3. Include trend-history snapshot file in uploaded artifact bundles.
4. Keep upload steps resilient with always-run behavior for easier failure triage.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Vector Similar-Incident Retrieval Slice)

Epic/Task Reference:

- EPIC 4 — Redis IRIS Integration
- Task 4.3 — Redis Vector Search
- Task 4.5 — Shared Operational Context

1. Add deterministic incident embedding generation for local vector retrieval without external model dependencies.
2. Add Redis vector index and per-incident vector records during RDI sync.
3. Add IRIS context retrieval path that queries similar incidents via KNN vector search.
4. Wire IRIS workflow signals to expose vector retrieval usage in runtime context signals.
5. Run validation checks and update tracker evidence + Epic 4 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Frontend Replay API Wiring Slice)

Epic/Task Reference:

- EPIC 5 — Modern UI and UX
- Task 5.5 — Replay Events UI
- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.7 — Event Stream Generator

1. Replace frontend-local replay templates with backend template discovery from /api/replay/templates.
2. Wire replay step execution controls to /api/replay/execute (mode=step).
3. Wire replay play action to /api/replay/execute (mode=full).
4. Keep timeline rendering based on backend templates and surface replay execution status in the panel.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Replay Run Polling + Cancel Controls Slice)

Epic/Task Reference:

- EPIC 5 — Modern UI and UX
- Task 5.5 — Replay Events UI
- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.7 — Event Stream Generator
- EPIC 4 — Redis IRIS Integration
- Task 4.6 — Redis Streams

1. Add frontend replay-run state model and run_id tracking for server-owned full replay runs.
2. Add polling loop against GET /api/replay/runs/{run_id} and map run progress to timeline status.
3. Add cancel control wired to POST /api/replay/runs/{run_id}/cancel.
4. Keep step replay action compatible while full replay run polling is active/inactive.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Page Shell + Navigation Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.1 — Add Learning Mode Page
- EPIC 5 — Modern UI and UX
- Task 5.1 — Main Dashboard Layout

1. Add frontend learning route shell at frontend/app/learning/page.tsx with architecture-overview placeholders.
2. Add visible navigation entry from main demo screen to /learning.
3. Keep learning shell responsive and aligned with existing dashboard visual style.
4. Add initial explanatory content blocks for architecture nodes and next implementation slices.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Architecture API Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.2 — Implement React Flow Diagram
- Task 9.3 — Implement Before/After Toggle
- Task 9.4 — Implement Step-by-Step Playback

1. Add backend learning-mode data model for architecture nodes, edges, and explanatory flow steps.
2. Add GET /api/learning/architecture to expose node and edge payloads for diagram consumers.
3. Add GET /api/learning/flow/baseline and GET /api/learning/flow/iris for explanatory execution sequences.
4. Keep payloads aligned with planned learning-mode frontend data model for diagram and playback use.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Diagram Shell Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.2 — Implement React Flow Diagram
- Task 9.5 — Component Inspector Content

1. Add frontend diagram component that renders backend learning architecture nodes and edges in an interactive graph view.
2. Add clickable node selection with a side-panel inspector for role, responsibilities, and before/after context.
3. Wire frontend learning page to load GET /api/learning/architecture and pass payloads into the diagram shell.
4. Keep the learning layout responsive while preserving the existing Learning Mode route and summary sections.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Before/After Toggle Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.3 — Implement Before/After Toggle
- Task 9.2 — Implement React Flow Diagram

1. Wire Learning Mode page to load baseline and IRIS flow payloads from GET /api/learning/flow/baseline and GET /api/learning/flow/iris.
2. Add Baseline, IRIS, and Comparison controls directly in the interactive architecture diagram.
3. Apply mode-specific node and edge highlighting so baseline emphasizes fragmented paths and IRIS emphasizes shared-context paths.
4. Surface mode-specific explanatory context in the inspector so the same component can be explained through before/after lenses.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Step Playback Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.4 — Implement Step-by-Step Playback
- Task 9.3 — Implement Before/After Toggle

1. Add playback controls (play, pause, next, previous, reset) to the Learning Mode architecture view.
2. Bind playback state to baseline, IRIS, and comparison modes so each mode advances through flow steps.
3. Use activeNodes and activeEdges from the current flow step to highlight only the currently active architecture path.
4. Surface the current step title, index, and description in the playback toolbar.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Inspector Payload Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.5 — Component Inspector Content
- Task 9.4 — Implement Step-by-Step Playback

1. Add backend component-level inspector payload model for all architecture nodes.
2. Add backend endpoint GET /api/learning/component/{component_id} for targeted inspector retrieval.
3. Wire frontend inspector panel to fetch component payloads when a node is selected.
4. Expand inspector sections with role, what-it-does, what-it-does-not-do, before/after value, and presenter talk track.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Context + Metrics Education Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.6 — Context Packet Viewer
- Task 9.7 — Metrics Education Panel

1. Add backend learning endpoints for latest context packet and metrics-education payloads.
2. Wire Learning Mode page to load context packet and metrics-education payloads from backend.
3. Add context packet viewer UI sections for structured facts, memory hits, semantic matches, live events, and prompt estimate.
4. Add metrics education panel UI with baseline vs IRIS snapshot plus plain-language explanation cards.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Guided Demo Overlay Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.8 — Guided Demo Script Overlay

1. Add optional guided-demo overlay controls to Learning Mode architecture toolbar.
2. Implement six scripted presenter steps matching the accepted demo narrative.
3. Bind guided steps to diagram mode and step focus so presenters can move through the story quickly.
4. Add visual styling for guided overlay panel and step navigation controls.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode MAF Portability Mapping Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.9 — MAF Portability Mapping Panel

1. Add backend learning payload and endpoint for MAF portability mapping.
2. Wire Learning Mode page to load the MAF portability payload.
3. Add portability mapping panel with current-component to MAF-equivalent table.
4. Add migration sequence section for presenter guidance.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Presenter Auto-Tour Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.10 — Presenter Auto-Tour Mode

1. Add timed auto-tour controls to the Guided Demo overlay for presenter-led playback.
2. Implement interval-driven guided-step progression with safe stop behavior at the final step.
3. Keep auto-tour synchronized with mode, flow step focus, and component selection highlights.
4. Add UI metadata for tour speed and active/inactive tour state visibility.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Context Diff Narrative Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.11 — Baseline-vs-IRIS Context Diff Narrative

1. Add backend learning payload for baseline-vs-IRIS context packet comparison.
2. Add backend endpoint for context diff narrative retrieval in Learning Mode.
3. Wire Learning Mode page to load context diff payload alongside existing learning datasets.
4. Add side-by-side context narrative panel showing what changes from baseline to IRIS.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Metrics Storytelling Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Enhancement — Narrated Metrics Storytelling Mode for Executive Demo Pacing

1. Add backend learning payload for narrated metrics storytelling chapters and pacing hints.
2. Add backend endpoint for metrics storytelling payload retrieval in Learning Mode.
3. Add frontend narrated storytelling playback controls (play, pause, next, previous, reset).
4. Add a storytelling panel with chapter narrative, KPI focus, and executive talk-track guidance.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Audience Q and A Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Enhancement — Audience Q and A Mode with Pre-Mapped Architecture Answers

1. Add backend learning payload for curated audience questions and mapped architecture answers.
2. Add backend endpoint for Learning Mode Q and A payload retrieval.
3. Add frontend Q and A interaction component with selectable questions and quick category context.
4. Add Learning Mode panel that presents pre-mapped answers tied to architecture components.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Exportable Summary Handout Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Enhancement — Exportable Learning Summary Handout for Stakeholder Follow-up

1. Add backend learning payload for a concise stakeholder handout summary.
2. Add backend endpoint for Learning Mode handout payload retrieval.
3. Add frontend handout panel that renders summary sections and key proof points.
4. Add export action to download the handout as JSON for follow-up sharing.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Presenter Annotation Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Enhancement — Presenter Annotation Mode for Technical vs Executive Talk Tracks

1. Add backend learning payload for presenter annotations with technical and executive track variants.
2. Add backend endpoint for Learning Mode presenter annotation payload retrieval.
3. Add frontend presenter annotation panel with track toggle and section-level talk tracks.
4. Integrate presenter annotation mode into Learning Mode and preserve responsive behavior.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Guided Fallback Script Cards Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Enhancement — Guided Fallback Script Cards for Offline/No-Live-Event Demos

1. Add backend learning payload for fallback script cards covering common demo interruption scenarios.
2. Add backend endpoint for Learning Mode fallback script card retrieval.
3. Add frontend fallback script cards panel with quick scenario selection and narrator-ready script text.
4. Integrate fallback script cards panel into Learning Mode with responsive layout parity.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Architecture Quiz Checkpoints Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Enhancement — Architecture Quiz Checkpoints for Audience Engagement Between Demo Chapters

1. Add backend learning payload for chapter-aligned architecture quiz checkpoints with answer explanations.
2. Add backend endpoint for Learning Mode quiz checkpoint payload retrieval.
3. Add frontend quiz checkpoint component with question navigation, answer selection, and reveal flow.
4. Integrate quiz checkpoint panel into Learning Mode with responsive layout parity.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Learning Mode Live Q and A Answer Anchors Slice)

Epic/Task Reference:

- EPIC 9 — Learning Mode and Interactive Architecture Explorer
- Task 9.12 — Live Q and A Answer Anchors

1. Add backend learning payload for chapter-aware Q and A anchor links and presenter guidance.
2. Add backend endpoint for Learning Mode Q and A anchor payload retrieval.
3. Add frontend anchor panel that lists quick-jump answers mapped to Learning Mode sections.
4. Integrate anchor panel and section IDs into Learning Mode with responsive layout parity.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Frontend Framework Hardening Slice)

Epic/Task Reference:

- EPIC 1 — Project Foundation
- Task 1.4 — Setup Frontend Framework

1. Add TailwindCSS foundation dependencies and configuration files in frontend.
2. Wire Tailwind layers into global styling while preserving existing visual language.
3. Add a lightweight theme toggle to support dark-mode and light-mode switching.
4. Integrate theme controls into dashboard shell without breaking Learning Mode layout behavior.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Frontend shadcn Starter Components Slice)

Epic/Task Reference:

- EPIC 1 — Project Foundation
- Task 1.4 — Setup Frontend Framework

1. Add baseline utility dependencies required for shadcn/ui-style component composition.
2. Add shared frontend utility helper for className composition.
3. Add starter shadcn-style UI primitives (button and card) in the frontend component library.
4. Integrate starter UI primitives into the home dashboard shell without changing runtime behavior.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Stakeholder Generator Communication Patterns Slice)

Epic/Task Reference:

- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.2 — Stakeholder Generator

1. Extend stakeholder generator schema with communication-pattern fields and deterministic sentiment dynamics.
2. Update deterministic Acme stakeholders to include the same communication-pattern fields.
3. Regenerate the seeded dataset artifact with updated stakeholder schema.
4. Validate generator runtime and output shape for stakeholder-linked communication fields.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Support Ticket Relationship Modeling Slice)

Epic/Task Reference:

- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.3 — Support Ticket Generator

1. Extend synthetic support-ticket records with deterministic relationship fields (origin, parent/escalation link, and incident linkage).
2. Wire generator flow so tickets can reference same-customer incidents for realistic escalation paths.
3. Update deterministic Acme ticket records to include the same relationship schema.
4. Regenerate seeded dataset and validate ticket relationship fields and generator metadata.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Usage Trend and Anomaly Modeling Slice)

Epic/Task Reference:

- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.5 — Usage Generator

1. Extend customer generator output with deterministic usage/adoption snapshot fields.
2. Add monthly usage trend history with declining-growth patterns and anomaly flags.
3. Update deterministic Acme customer seed record with usage and anomaly fields.
4. Regenerate seeded dataset and validate usage/anomaly fields and generator metadata.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Customer Memory Continuity Modeling Slice)

Epic/Task Reference:

- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.6 — Memory Generator

1. Extend customer generator output with deterministic memory-continuity fields for prior escalations, promises, frustrations, and communication preferences.
2. Add historical memory timeline entries that can seed continuity scenarios across sessions.
3. Update deterministic Acme customer seed record with memory continuity fields and history.
4. Regenerate seeded dataset and validate memory fields and generator metadata.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Event Stream Expansion and Replay Fidelity Slice)

Epic/Task Reference:

- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.7 — Event Stream Generator

1. Expand generated event stream payloads beyond ticket/incident status updates.
2. Add deterministic support events, customer messages, and deployment events in replayable format.
3. Keep stream ordering deterministic and customer-linked for timeline playback.
4. Regenerate seeded dataset and validate event type coverage and generator metadata.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Incident Impact and Deployment-Failure Modeling Slice)

Epic/Task Reference:

- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.4 — Incident Generator

1. Extend incident generator schema with deterministic customer-impact and deployment-failure context fields.
2. Keep incident timelines deterministic while enriching records with impact-oriented metadata.
3. Update deterministic Acme incident seed record to include the same schema additions.
4. Regenerate seeded dataset and validate incident impact fields and generator metadata.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Customer Profile and Contract Distribution Hardening Slice)

Epic/Task Reference:

- EPIC 2 — Synthetic Enterprise Data Engine
- Task 2.1 — Customer Generator

1. Extend customer generator schema with deterministic profile dimensions (industry, region, and account tier).
2. Add deterministic contract metadata for each customer to strengthen operational realism.
3. Update deterministic Acme seed customer to include the same profile and contract schema.
4. Regenerate seeded dataset and validate customer profile and contract field coverage with generator metadata.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Baseline Local Memory and Session Continuity Slice)

Epic/Task Reference:

- EPIC 3 — Baseline LangGraph System
- Task 3.2 — Local Memory

1. Add naive in-process local memory store for baseline sessions keyed by customer.
2. Pass chat-history snippets and baseline session state into baseline graph execution.
3. Surface local-memory continuity signals in baseline responses while keeping scope session-local only.
4. Run validation checks with repeated baseline calls to confirm in-session memory behavior.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Baseline Retrieval Layer Hardening Slice)

Epic/Task Reference:

- EPIC 3 — Baseline LangGraph System
- Task 3.3 — Baseline Retrieval Layer

1. Add baseline local JSON retrieval over seed entities for customer, ticket, incident, and stakeholder context.
2. Add simple keyword retrieval path that scores seed snippets against the active prompt.
3. Add deterministic fake vector retrieval path for pseudo-semantic matching without external embeddings.
4. Wire retrieval outputs into baseline graph summary and context signals while preserving intentionally inefficient behavior.
5. Run validation checks and update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Baseline Runtime Metrics Instrumentation Slice)

Epic/Task Reference:

- EPIC 3 — Baseline LangGraph System
- Task 3.4 — Metrics Instrumentation

1. Add runtime latency instrumentation around baseline and IRIS workflow execution paths.
2. Add deterministic derived token and retrieval/tool metric enrichments from runtime payloads.
3. Include explicit instrumentation signals so downstream UI and benchmark consumers can distinguish modeled vs observed metrics.
4. Validate metrics payload shape via repeated workflow calls for both baseline and IRIS paths.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (RedisJSON Operational Entity Hardening Slice)

Epic/Task Reference:

- EPIC 4 — Redis IRIS Integration
- Task 4.1 — RedisJSON Operational State

1. Extend RDI sync to persist contract and usage entities as first-class RedisJSON documents linked to customers.
2. Extend RDI sync status reporting with contract/usage sync counters for observability.
3. Extend context retrieval and merge paths to include RedisJSON contract/usage payloads in operational context.
4. Run validation checks for compile integrity and RedisJSON sync/report payload shape.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (FT.SEARCH Query Filtering and Timeline Context Slice)

Epic/Task Reference:

- EPIC 4 — Redis IRIS Integration
- Task 4.2 — Redis Search

1. Extend Redis FT.SEARCH retrieval to support query-driven filters for severity, status, and service hints.
2. Add deterministic retrieval-hint parsing from user query text and expose retrieval filter usage in context metadata.
3. Add timeline-oriented operational context assembly from ticket and incident records.
4. Validate compile integrity and retrieval-hint behavior with focused checks.
5. Update tracker evidence + Epic task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Redis Agent Memory Extraction and Recall Hardening Slice)

Epic/Task Reference:

- EPIC 4 — Redis IRIS Integration
- Task 4.4 — Redis Agent Memory

1. Add deterministic memory extraction for reusable customer-preference and commitment facts.
2. Extend Redis memory storage to separate short-term turn memory from durable long-term memory.
3. Add query-aware memory retrieval scoring so relevant memory is prioritized in shared context.
4. Wire IRIS post-processing to write extracted memory facts and add memory-layer runtime signals.
5. Run validation checks and update tracker evidence + Epic 4 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Shared Workflow State and Context Continuity Slice)

Epic/Task Reference:

- EPIC 4 — Redis IRIS Integration
- Task 4.5 — Shared Operational Context

1. Extend Redis shared context payload to include persisted shared workflow state per customer.
2. Add Redis helpers to read/write shared workflow state with deterministic bounded payload fields.
3. Merge shared workflow state into IRIS seed/context so follow-up turns reuse consistent state.
4. Wire IRIS post-processing to persist latest shared workflow state and emit shared-state runtime signals.
5. Run validation checks and update tracker evidence + Epic 4 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Redis Streams Reactivity Hardening Continuation Slice)

Epic/Task Reference:

- EPIC 4 — Redis IRIS Integration
- Task 4.6 — Redis Streams

1. Add Redis stream-read helpers to retrieve recent operational events for a customer or global context.
2. Merge persisted Redis stream events with in-memory event-bus snapshots for IRIS runtime context.
3. Ensure event ordering favors most-recent events so IRIS event context is deterministic after restarts.
4. Emit explicit runtime signals for stream-event context availability and event counts.
5. Run validation checks and update tracker evidence + Epic 4 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Semantic Cache Similarity and Hit-Signal Hardening Slice)

Epic/Task Reference:

- EPIC 4 — Redis IRIS Integration
- Task 4.7 — Semantic Cache

1. Extend Redis cache retrieval to support similarity-based cache lookup fallback for near-duplicate prompts.
2. Add bounded per-customer cache-key index maintenance to keep semantic lookup deterministic and efficient.
3. Preserve exact-cache behavior while returning semantic cache hits with explicit runtime traceability.
4. Add semantic cache hit signaling in IRIS runtime path for visibility in metrics and UI context signals.
5. Run validation checks and update tracker evidence + Epic 4 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Runtime Metrics Visualization Continuation Slice)

Epic/Task Reference:

- EPIC 5 — Modern UI and UX
- Task 5.3 — Metrics Visualization

1. Add a dedicated runtime metrics panel component for baseline vs IRIS request metrics.
2. Visualize key runtime dimensions (latency, prompt tokens, memory hits, cache hits) side-by-side.
3. Add compact comparative charts for retrieval and tool signal intensity for immediate before/after reading.
4. Integrate the new metrics panel into the main dashboard layout with responsive behavior.
5. Run validation checks and update tracker evidence + Epic 5 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Before-vs-After Toggle Implementation Slice)

Epic/Task Reference:

- EPIC 5 — Modern UI and UX
- Task 5.4 — Before vs After Toggle

1. Add a dashboard-level before/after mode toggle component with Baseline, IRIS, and side-by-side comparison modes.
2. Reuse the same workflow outputs for both modes so baseline and IRIS remain directly comparable per request.
3. Surface measurable differences (latency, tokens, retrieval/tool calls) as explicit delta indicators.
4. Integrate the toggle panel into the main dashboard flow with responsive layout behavior.
5. Run validation checks and update tracker evidence + Epic 5 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Replay Events UI Completion Slice)

Epic/Task Reference:

- EPIC 5 — Modern UI and UX
- Task 5.5 — Replay Events UI

1. Add replay-speed control in the frontend panel and pass selected speed to backend replay execution.
2. Add replay-run progress visualization so playback advancement is visible immediately.
3. Improve replay status metadata display for active run state and step completion.
4. Keep step replay compatibility and responsive layout behavior after UI enhancements.
5. Run validation checks and update tracker evidence + Epic 5 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Benchmark Harness Scenario Matrix Slice)

Epic/Task Reference:

- EPIC 6 — Benchmarking and Proof
- Task 6.1 — Benchmark Harness

1. Add scenario-profile support in the benchmark harness for baseline smoke and expanded workload modes.
2. Add deterministic scenario matrix coverage for repeated-query and memory-heavy workflow prompts.
3. Preserve existing top-level benchmark metric fields while appending per-scenario breakdown output.
4. Wire extended CI benchmark run to use the expanded scenario profile for wider benchmark evidence.
5. Run validation checks and update tracker evidence + Epic 6 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Token Measurement Metrics Expansion Slice)

Epic/Task Reference:

- EPIC 6 — Benchmarking and Proof
- Task 6.2 — Token Measurement

1. Extend benchmark harness token extraction to capture prompt, completion, and total token values from runtime metrics.
2. Preserve existing prompt-token output fields while appending completion-token and total-token averages for compatibility-safe expansion.
3. Extend scenario breakdown and concurrent benchmark outputs to include the same token triplet.
4. Run validation checks for benchmark scripts and CLI output shape.
5. Update tracker evidence + Epic 6 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Latency Measurement Depth Expansion Slice)

Epic/Task Reference:

- EPIC 6 — Benchmarking and Proof
- Task 6.3 — Latency Measurement

1. Extend runtime metrics to expose deterministic latency decomposition fields for retrieval and LLM phases.
2. Extend benchmark harness outputs with latency p50 and runtime-latency summaries in addition to existing p95 fields.
3. Extend benchmark outputs with retrieval-latency and llm-latency averages derived from runtime metrics.
4. Preserve existing latency fields used by regression checks while appending the new latency metrics.
5. Run validation checks and update tracker evidence + Epic 6 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Cache Effectiveness Proof Slice)

Epic/Task Reference:

- EPIC 6 — Benchmarking and Proof
- Task 6.4 — Cache Effectiveness

1. Extend benchmark harness response parsing to capture cache-hit signals (exact and semantic) from runtime context signals.
2. Add top-level cache hit rate metrics for baseline and IRIS benchmark outputs.
3. Add repeated-query runtime-latency savings metrics so cache value is visible over repeated prompts.
4. Preserve existing benchmark metric fields used by regression scripts while appending cache-effectiveness fields.
5. Run validation checks and update tracker evidence + Epic 6 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Multi-Agent Coordination Metrics Slice)

Epic/Task Reference:

- EPIC 6 — Benchmarking and Proof
- Task 6.5 — Multi-Agent Coordination Metrics

1. Extend benchmark metric parsing to capture retrieval and tool signal counts from runtime metrics.
2. Add duplicate-retrieval and shared-memory-hit summaries derived from runtime signals.
3. Add baseline-vs-IRIS coordination comparison metrics for retrieval/tool reduction visibility.
4. Preserve existing benchmark metric fields used by trend/regression consumers while appending coordination metrics.
5. Run validation checks and update tracker evidence + Epic 6 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Redis Abstraction Layer Slice)

Epic/Task Reference:

- EPIC 7 — Azure Readiness
- Task 7.1 — Redis Abstraction Layer

1. Add a centralized Redis client abstraction with a shared env-driven configuration model.
2. Support both REDIS_URL and host/port/password inputs for local and Azure compatibility.
3. Add TLS-aware configuration paths (including rediss and explicit TLS flags) for Azure Managed Redis.
4. Refactor Redis tooling/runtime config surfaces to use the centralized abstraction while preserving current behavior.
5. Run validation checks and update tracker evidence + Epic 7 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Kubernetes Readiness Slice)

Epic/Task Reference:

- EPIC 7 — Azure Readiness
- Task 7.2 — Kubernetes Readiness

1. Remove replica-local runtime dependence from baseline session state by introducing Redis-backed baseline session storage.
2. Add Redis-backed replay run-state persistence so run status is visible across backend replicas.
3. Add cross-replica cancellation signaling for replay runs using shared Redis run-state updates.
4. Add a lightweight scaling-readiness check script for stateless backend + Redis-backed state behavior.
5. Run validation checks and update tracker evidence + Epic 7 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Azure Compatibility Validation Slice)

Epic/Task Reference:

- EPIC 7 — Azure Readiness
- Task 7.3 — Azure Compatibility Validation

1. Add a dedicated Azure compatibility validation script that checks Redis Search, JSON, vector search, Streams, and TLS configuration requirements.
2. Validate backend runtime compatibility signals from /api/config for Redis tool availability and TLS posture.
3. Add runbook commands for Azure Managed Redis validation and local non-TLS smoke mode.
4. Run validation checks for updated scripts and docs.
5. Update tracker evidence + queue to the next Epic task.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Framework-Agnostic Context Layer Slice)

Epic/Task Reference:

- EPIC 8 — Microsoft Agent Framework Portability
- Task 8.1 — Framework-Agnostic Context Layer

1. Introduce a dedicated framework-agnostic context layer module that assembles Redis-backed customer context and merged operational events without LangGraph dependencies.
2. Refactor IRIS workflow orchestration to consume the context layer output instead of embedding context assembly logic directly in workflow functions.
3. Move Redis post-processing helpers for memory and shared-workflow state updates into the context layer so orchestration remains thin and reusable.
4. Add runbook note documenting the new context layer boundary for future MAF reuse.
5. Run validation checks and update tracker evidence + Epic 8 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Shared State Contracts Slice)

Epic/Task Reference:

- EPIC 8 — Microsoft Agent Framework Portability
- Task 8.2 — Shared State Contracts

1. Add framework-agnostic shared state contract definitions for memory records, operational events, and retrieval request/response payloads.
2. Wire contract normalization helpers into event publishing/retrieval paths so runtime event payloads conform to one shared schema.
3. Wire retrieval contract assembly into the context layer so context retrieval outputs are represented by a reusable API contract.
4. Add runbook notes documenting where shared contracts live and how future orchestration frameworks should consume them.
5. Run validation checks and update tracker evidence + Epic 8 task notes.

Execution Status:

- [x] Step 1 complete
- [x] Step 2 complete
- [x] Step 3 complete
- [x] Step 4 complete
- [x] Step 5 complete

## Current Execution Plan (Migration Documentation Slice)

Epic/Task Reference:

- EPIC 8 — Microsoft Agent Framework Portability
- Task 8.3 — Migration Documentation

1. Create a dedicated migration documentation artifact covering LangGraph node mapping to equivalent MAF orchestration patterns.
2. Document how framework-agnostic context layer and shared contracts are reused without refactoring Redis internals.
3. Add a phased migration sequence with readiness gates and rollback considerations.
4. Link migration documentation from the primary runbook for discoverability.
5. Run validation checks and update tracker evidence + Epic 8 task notes.

Execution Status:

- [ ] Step 1 pending
- [ ] Step 2 pending
- [ ] Step 3 pending
- [ ] Step 4 pending
- [ ] Step 5 pending

## Working Rule

This document must be updated immediately when a task is completed.

## Immediate Next-Action Queue

1. Start migration documentation mapping (EPIC 8 Task 8.3).

## Progress Log

### 2026-05-26

- Completed repository scaffold and top-level architecture folders.
- Added CI workflow skeleton.
- Added Docker Compose with frontend, backend, and Redis Stack.
- Added backend FastAPI shell and health/config endpoints.
- Added frontend Next.js shell with backend health indicator.
- Created root README and environment template.
- Added local helper scripts: scripts/dev-up.sh and scripts/dev-down.sh.
- Added backend/scripts/verify_redis_stack.py to validate JSON/Search/Vector/Streams.
- Validated compose configuration parsing with docker-compose config.
- Blocker discovered: Docker daemon not reachable at unix:///Users/thomas.findelkind/.colima/default/docker.sock.
- Validated Python syntax for backend app and Redis verification script.
- Validated shell syntax for local dev helper scripts.
- Added first baseline endpoint: POST /api/run/baseline.
- Added first IRIS endpoint: POST /api/run/iris.
- Added frontend comparison cards that render baseline and IRIS metrics side by side.
- Started Colima runtime and confirmed Docker server availability.
- Successfully started frontend/backend/redis via ./scripts/dev-up.sh -d.
- Verified backend runtime endpoints (/health, /api/run/baseline, /api/run/iris) and frontend HTTP availability.
- Updated backend image to include scripts/ for in-container validation workflows.
- Fixed Redis verifier MODULE LIST parsing bug for Redis response compatibility.
- Executed in-container Redis verification with all checks passing: Connectivity, Modules, RedisJSON, RediSearch, Vector Search, Streams.
- Added backend live-event interfaces: GET /api/events/recent, POST /api/events/inject, WS /ws/events.
- Added frontend live events panel with WebSocket client and event injection action.
- Rebuilt backend/frontend containers and validated event injection + retrieval behavior.
- Added backend orchestration handlers in backend/app/workflows.py and wired /api/run/baseline + /api/run/iris to use them.
- Added deterministic Acme seed dataset at data/acme_seed.json and backend/app/seed_data/acme_seed.json.
- Added first benchmark harness script at benchmarks/run_benchmark.py.
- Generated initial benchmark report at benchmarks/reports/latest.json (5 iterations).
- Verified updated runtime responses and Python syntax checks for main workflow and benchmark files.
- Upgraded CI workflow from placeholder to container-based smoke verification for backend + redis.
- Added deterministic customer generator script at data/generate_customers.py.
- Completed EPIC 9 enhancement: guided fallback script cards for offline/no-live-event demos.
- Added backend endpoint GET /api/learning/fallback-scripts and integrated Learning Mode fallback panel UI.
- Validated fallback scripts endpoint with FastAPI TestClient and confirmed frontend build success after integration.
- Completed EPIC 9 enhancement: architecture quiz checkpoints for audience engagement between demo chapters.
- Added backend endpoint GET /api/learning/quiz-checkpoints and integrated Learning Mode quiz checkpoint panel UI.
- Validated quiz checkpoint endpoint with FastAPI TestClient and confirmed frontend build success after integration.
- Completed EPIC 9 Task 9.12: live Q and A answer anchors for rapid presenter navigation.
- Added backend endpoint GET /api/learning/qa-anchors and integrated Learning Mode anchor jump panel UI.
- Validated Q and A anchors endpoint with FastAPI TestClient and confirmed frontend build success after integration.
- Completed EPIC 1 Task 1.4 slice: Tailwind foundation and theme toggle integration in frontend.
- Added Tailwind/PostCSS config files and theme toggle control in home dashboard shell.
- Validated frontend build success after Tailwind plugin compatibility fix and framework hardening changes.
- Completed EPIC 1 Task 1.4 continuation: shadcn/ui starter components and baseline usage integration.
- Added shared className utility helper and shadcn-style button/card primitives in frontend component library.
- Validated frontend build success after shadcn starter component integration.
- Generated multi-customer fixture at data/customers_seed.json (1000 customers).
- Added backend graph-style node pipeline module at backend/app/graph_pipeline.py.
- Wired backend workflows to graph-style pipeline execution for baseline and IRIS modes.
- Re-ran runtime endpoint checks and refreshed benchmark outputs at benchmarks/reports/latest.json and benchmarks/reports/ci-latest.json.
- Split CI workflow into smoke and extended scenarios with trigger separation and ci-extended report output.
- Expanded dataset generator to emit linked stakeholders, tickets, and incidents with deterministic Acme-linked records.
- Migrated orchestration runtime to full LangGraph StateGraph nodes/edges at backend/app/langgraph_pipeline.py.
- Updated backend workflows to use LangGraph runtime and removed custom graph-style pipeline dependency.
- Re-ran syntax/runtime checks and refreshed benchmark outputs at latest, ci-latest, and ci-extended report paths.
- Added replay controls panel with play/pause/next/reset in frontend live events panel.
- Added multiple operational event templates and timeline state visualization (pending/active/completed).
- Wired timeline playback to event injection endpoint so replayed steps stream through existing WebSocket feed.
- Added benchmark trend snapshot script at benchmarks/update_trend_snapshot.py.
- Added regression gate script and baseline artifact at benchmarks/check_regression.py and benchmarks/reports/regression-baseline.json.
- Wired CI smoke flow to append trend snapshots and enforce regression gate thresholds.
- Validated trend snapshot append and regression checks locally with passing gate results.
- Added concurrent benchmark harness at benchmarks/run_concurrent_benchmark.py with worker/round configuration.
- Added concurrent benchmark report output at benchmarks/reports/concurrent-latest.json.
- Wired extended CI flow to run concurrent benchmark scenario and append it to trend history.
- Validated concurrent benchmark run with zero errors for baseline and IRIS modes.
- Added Redis IRIS tools module at backend/app/redis_iris_tools.py for RDI-style sync, context retrieval, agent memory, and LangCache.
- Wired IRIS runtime path in backend/app/workflows.py to retrieve shared context, write agent memory, and store/reuse LangCache responses.
- Added backend lifecycle + API controls for RDI in backend/app/main.py: GET /api/rdi/status and POST /api/rdi/sync-now.
- Mounted dataset volume into backend container at docker-compose.yml so RDI can continuously ingest generated data from /data/customers_seed.json.
- Validated live backend responses include Redis integration signals (for example redis-langcache-store after first run).
- Expanded synthetic dataset timeline progression in data/generate_customers.py with ticket and incident state transitions.
- Added replayable generated event stream output at data/customers_seed.json -> event_stream.
- Added Redis FT.SEARCH indexes for customer, ticket, and incident retrieval in backend/app/redis_iris_tools.py.
- Switched IRIS context retrieval path to FT.SEARCH-based lookup and observed redis-ft-search-context signal in runtime responses.
- Added backend replay template catalog at backend/app/replay_templates.py for server-driven timeline scenarios.
- Added backend replay APIs in backend/app/main.py: GET /api/replay/templates, POST /api/replay/execute, GET /api/replay/runs/{run_id}, POST /api/replay/runs/{run_id}/cancel.
- Added Redis Streams write-through for manual and replay events via append_operational_event in backend/app/redis_iris_tools.py.
- Validated replay API behavior with local FastAPI TestClient checks for template discovery, step execution, and full-run lifecycle endpoints.
- Noted transient external Docker registry connectivity failures while rebuilding backend image during validation; local in-process API validation completed successfully.
- Added backend benchmark trend endpoint in backend/app/main.py: GET /api/benchmarks/trends.
- Added frontend benchmark trend panel at frontend/components/benchmark-trend-panel.tsx with KPI cards and baseline-vs-IRIS trend lines.
- Wired main dashboard in frontend/app/page.tsx to load trend snapshots and render benchmark trend visualization.
- Added responsive trend panel styling in frontend/app/globals.css for dashboard integration.
- Added strict/normal/lenient profile policy in benchmarks/check_regression.py for latency, p95 latency, and prompt-token regression gating.
- Kept per-metric threshold override flags so profile defaults can still be tuned per run.
- Wired CI smoke regression gate to use explicit strict profile policy in .github/workflows/ci.yml.
- Added smoke CI artifact upload for benchmark-smoke-reports (ci-latest + trend-history) in .github/workflows/ci.yml.
- Added extended CI artifact upload for benchmark-extended-reports (ci-extended + concurrent-latest + trend-history) in .github/workflows/ci.yml.
- Added deterministic pseudo-embedding generation and Redis vector index wiring for incidents in backend/app/redis_iris_tools.py.
- Added vector KNN similar-incident retrieval path in IRIS context retrieval with runtime signal redis-vector-similar-incidents.
- Replaced frontend-local replay template source with backend discovery API usage in frontend/components/live-events-panel.tsx.
- Wired replay controls to backend /api/replay/execute for step and full execution modes with panel status updates.
- Added replay run-status polling in frontend live events panel against GET /api/replay/runs/{run_id} for server-owned full replay lifecycle visibility.
- Added replay cancel control in frontend live events panel wired to POST /api/replay/runs/{run_id}/cancel and surfaced cancellation status in panel metadata.
- Added Learning Mode route shell at frontend/app/learning/page.tsx with architecture overview cards and planned flow sections.
- Added main dashboard navigation entry to Learning Mode from frontend/app/page.tsx.
- Added backend learning-mode architecture endpoint at GET /api/learning/architecture with node and edge payloads for diagram consumers.
- Added backend learning-mode flow endpoints at GET /api/learning/flow/baseline and GET /api/learning/flow/iris for baseline vs IRIS explanation.
- Added frontend Learning Mode architecture diagram component with React Flow rendering, clickable nodes, and side-panel inspector wiring to GET /api/learning/architecture.
- Validated frontend build after Learning Mode diagram integration: npm run build (success).
- Added Learning Mode Baseline/IRIS/Comparison toggle controls with mode-specific node/edge highlighting driven by flow payloads.
- Added mode-aware inspector lens copy so each selected component can be contrasted in baseline vs IRIS context.
- Added Learning Mode playback controls (play/pause/next/previous/reset) and step metadata display in the architecture toolbar.
- Bound per-step activeNodes and activeEdges to diagram highlighting for baseline, IRIS, and comparison step progression.
- Validated frontend build after Learning Mode step playback integration: npm run build (success).
- Added backend component-level inspector payloads and API endpoint GET /api/learning/component/{component_id}.
- Wired Learning Mode inspector to fetch node-specific payloads and render role, capabilities, constraints, before/after value, and talk track sections.
- Validated backend + frontend checks after Learning Mode inspector payload integration.
- Added backend learning endpoints GET /api/learning/context-packet and GET /api/learning/metrics-education.
- Added Learning Mode context packet viewer UI for structured facts, memory hits, semantic matches, live events, and prompt estimate.
- Added Learning Mode metrics education panel with baseline-vs-IRIS metric snapshots and non-engineer explanation cards.
- Validated backend endpoint checks and frontend build after Task 9.6 and Task 9.7 integration.
- Added optional guided demo overlay controls to Learning Mode architecture toolbar for presenter-led walkthroughs.
- Added six scripted guided steps aligned to Task 9.8 acceptance narrative and linked them to mode/step focus behavior.
- Validated frontend build after Task 9.8 guided overlay integration.
- Added backend endpoint GET /api/learning/maf-portability and teaching payload for framework portability mapping.
- Added Learning Mode MAF portability panel with component mapping table and staged migration sequence.
- Validated backend endpoint checks and frontend build after Task 9.9 portability integration.
- Added Learning Mode presenter auto-tour controls with timed guided-step progression and automatic stop at final guided step.
- Added auto-tour status and speed metadata in Guided Demo overlay for presenter pacing visibility.
- Validated frontend build after Task 9.10 presenter auto-tour integration.
- Added backend context diff teaching payload and endpoint GET /api/learning/context-diff for baseline-versus-IRIS packet comparison.
- Added Learning Mode side-by-side context diff narrative panel with delta storytelling for prompt shape, retrieval path, and memory continuity.
- Validated backend endpoint checks and frontend build after Task 9.11 context diff integration.
- Added backend endpoint GET /api/learning/metrics-storytelling with narrated chapter payload and pacing hints.
- Added Learning Mode narrated metrics storytelling panel with play, pause, next, previous, and reset controls for executive pacing.
- Validated backend endpoint checks and frontend build after metrics storytelling enhancement integration.
- Added backend endpoint GET /api/learning/audience-qa with curated audience questions and pre-mapped architecture answers.
- Added Learning Mode Audience Q and A panel with category filtering, question selection, and mapped component chips.
- Validated backend endpoint checks and frontend build after audience Q and A enhancement integration.
- Added backend endpoint GET /api/learning/summary-handout with stakeholder-facing summary sections, proof points, and export metadata.
- Added Learning Mode exportable summary handout panel with section rendering and JSON download action for follow-up sharing.
- Validated backend endpoint checks and frontend build after exportable handout enhancement integration.
- Added backend endpoint GET /api/learning/presenter-annotations with executive and technical presenter track payloads.
- Added Learning Mode presenter annotation panel with track toggle and topic-level speaking prompts.
- Validated backend endpoint checks and frontend build after presenter annotation enhancement integration.
- Completed EPIC 2 Task 2.2: enriched stakeholder generator with deterministic communication patterns and sentiment dynamics.
- Added stakeholder communication fields in generated data: preferred_channel, update_cadence, communication_style, timezone, and response_sla_hours.
- Regenerated data/customers_seed.json and validated generator metadata version 3 with communication fields present in stakeholder records.
- Completed EPIC 2 Task 2.3: enriched support ticket generator with deterministic relationship modeling and incident-linked escalation paths.
- Added ticket relationship fields in generated data: origin, related_incident_id, and escalates_ticket_id.
- Regenerated data/customers_seed.json and validated generator metadata version 4 with ticket relationship fields present and populated.
- Completed EPIC 2 Task 2.5: enriched customer usage generator with deterministic adoption trends and anomaly modeling.
- Added usage fields in generated customer data: seats_provisioned, active_seats, adoption_rate_pct, monthly_active_trend, and anomalies.
- Regenerated data/customers_seed.json and validated generator metadata version 5 with usage trend and anomaly fields present.
- Completed EPIC 2 Task 2.6: enriched customer memory generator with deterministic continuity fields and historical memory events.
- Added memory fields in generated customer data: escalation_count, open_commitment, promise, frustration, preference, and memory_timeline.
- Regenerated data/customers_seed.json and validated generator metadata version 6 with memory continuity fields present.
- Completed EPIC 2 Task 2.7: expanded event stream generator with deterministic replay coverage beyond ticket/incident status updates.
- Added event stream coverage for support_note, customer_message, and deployment_event while preserving ticket_update and incident_update events.
- Regenerated data/customers_seed.json and validated generator metadata version 7 with event stream type coverage present.
- Completed EPIC 2 Task 2.4: enriched incident generator with deterministic customer-impact and deployment-failure context fields.
- Added incident impact fields in generated data: impact_scope, customer_impact (affected_seats, affected_revenue_usd, downtime_minutes, renewal_risk_delta), and deployment_context (deployment_id, track, triggered_by_deployment, root_cause).
- Regenerated data/customers_seed.json and validated generator metadata version 8 with incident impact schema coverage present.
- Completed EPIC 2 Task 2.1: hardened customer generator with deterministic profile dimensions and contract metadata for realistic operational distribution.
- Added customer profile fields in generated data: industry, region, account_tier, and contract (contract_id, term_months, billing_model, next_invoice_date, auto_renew, sla_tier).
- Regenerated data/customers_seed.json and validated generator metadata version 9 with customer distribution telemetry present.
- Completed EPIC 3 Task 3.2: added session-local baseline memory continuity with naive in-process chat history and state reuse.
- Wired baseline workflow to inject prior turn snippets and session turn state into baseline graph execution for same-session continuity.
- Validated repeated baseline runs with cold-to-hit transition signals (session-local-memory-cold -> session-local-memory-hit) and session-turn-index progression.
- Completed EPIC 3 Task 3.3: added baseline retrieval layer with local JSON, keyword scoring, and deterministic fake-vector matching.
- Wired baseline graph retrieval outputs into summary composition and context signals while preserving intentionally inefficient retrieval behavior.
- Validated baseline runtime signals for baseline-keyword-retrieval-hit, baseline-fake-vector-hit, baseline-documents-scanned, and retained session-local-memory-hit continuity on repeated calls.
- Completed EPIC 3 Task 3.4: added runtime metrics instrumentation across baseline and IRIS workflow execution paths.
- Added derived runtime metrics fields in workflow responses: runtime_latency_ms, prompt_tokens_observed, completion_tokens_observed, retrieval_signals, tool_signals, and instrumentation_mode.
- Validated baseline and IRIS runtime payloads include runtime metrics enrichment and runtime-latency-ms context signals.
- Completed EPIC 4 Task 4.1 hardening: added first-class RedisJSON persistence for customer-linked contract and usage entities.
- Extended RDI sync observability counters with synced_contracts and synced_usage in Redis status payloads.
- Extended Redis context merge path to hydrate customer.contract and customer.usage from RedisJSON retrieval when available.
- Completed EPIC 4 Task 4.2 hardening: extended FT.SEARCH context retrieval with query-driven filters for severity, status, and service hints.
- Added deterministic retrieval-hint parsing and timeline context assembly from incident and ticket timeline records.
- Validated retrieval hint parsing and timeline assembly behavior with focused checks and compile integrity validation.
- Completed EPIC 4 Task 4.4 hardening: added deterministic memory extraction for customer preference, commitment, renewal-risk, and operational-risk facts.
- Extended Redis memory layer with short-term and long-term list separation plus query-aware memory retrieval prioritization.
- Wired IRIS post-processing to persist extracted long-term memory facts and emit memory extraction/write runtime signals.
- Validated memory extraction behavior and compile integrity checks for updated Redis tools and workflow paths.
- Completed EPIC 4 Task 4.5 hardening: extended shared operational context with persisted Redis workflow state per customer.
- Added shared workflow-state read/write helpers and bounded context payload fields for consistent cross-turn hydration.
- Wired IRIS context retrieval and post-processing paths to consume and persist shared workflow state with explicit runtime signals.
- Validated shared workflow-state persistence and memory prioritization behavior with focused stub-client checks and compile integrity validation.
- Completed EPIC 4 Task 4.6 hardening: added Redis stream-read retrieval for recent operational events with customer filtering.
- Wired IRIS runtime to merge persisted Redis stream events with in-memory bus events and enforce most-recent-first event ordering.
- Added explicit stream reactivity runtime signals for stream hit/empty state and stream event counts.
- Validated stream event retrieval/filtering behavior and compile integrity checks for updated Redis stream integration paths.
- Completed EPIC 4 Task 4.7 hardening: added similarity-based semantic cache fallback for near-duplicate prompts.
- Added bounded per-customer cache key indexing to support deterministic semantic lookup over recent entries.
- Added explicit cache hit traceability signals for exact and semantic hits, including similarity score telemetry.
- Validated exact-hit and semantic-hit cache behavior with focused stub-client checks and compile integrity validation.
- Completed EPIC 5 Task 5.4: added dashboard before-vs-after mode toggle with Baseline, IRIS, and side-by-side comparison views.
- Reused same workflow outputs for both modes and added measurable deltas for latency, prompt tokens, retrieval calls, and tool calls.
- Validated frontend build success after before-vs-after toggle integration.
- Completed EPIC 5 Task 5.5 continuation: added replay playback speed control and wired selected speed into backend full-run execution.
- Added replay progress visualization (completed steps + progress bar) and enriched event metadata with source indicators.
- Validated frontend build success after replay-events UI completion slice.
- Completed EPIC 6 Task 6.1: expanded benchmark harness with scenario profiles for smoke and memory-heavy/repeated-query coverage.
- Added per-scenario benchmark breakdown output while preserving existing top-level baseline/iris metric fields for regression compatibility.
- Updated extended CI benchmark execution to run with --scenario-profile expanded and validated benchmark script syntax/CLI flags.
- Completed EPIC 6 Task 6.2: expanded token measurement to include prompt, completion, and total token averages in benchmark outputs.
- Updated both standard and concurrent benchmark harness scripts to report token triplets for baseline and IRIS while keeping existing prompt token fields.
- Validated benchmark script syntax and CLI behavior after token measurement expansion.
- Completed EPIC 6 Task 6.3: expanded latency measurement with p50, p95, runtime latency summaries, and retrieval/LLM latency averages.
- Added deterministic latency decomposition fields in backend runtime instrumentation for retrieval, LLM, and orchestration phases.
- Preserved existing latency_ms_avg and latency_ms_p95 benchmark fields for compatibility with regression gating.
- Completed EPIC 6 Task 6.4: expanded cache-effectiveness proof with cache hit rate and repeated-query savings metrics.
- Added cache-hit signal parsing and cache hit rate reporting (overall, exact, and semantic) in standard and concurrent benchmark harness outputs.
- Added repeated-query runtime latency savings output in standard benchmark reports to make semantic cache impact explicit.
- Completed EPIC 6 Task 6.5: expanded multi-agent coordination metrics with retrieval signal, tool signal, and duplicate retrieval visibility.
- Added shared-memory hit reporting from runtime context signals (agent memory and shared-workflow state hits) in standard and concurrent benchmark outputs.
- Added baseline-vs-IRIS coordination comparison fields for retrieval/tool/duplicate-retrieval reduction and shared-memory-hit delta visibility.
- Completed EPIC 7 Task 7.1: added centralized Redis client abstraction with shared env-driven configuration.
- Added REDIS_URL + host/port/password compatibility and TLS-aware settings for local and Azure Redis connectivity.
- Updated backend runtime config surface and Redis capability verification docs/script for Azure Managed Redis TLS workflows.

---

# Core Strategic Message

## BEFORE

```text
Agents coordinate through prompts.
```

## AFTER

```text
Agents coordinate through shared operational state.
```

---

# Demo Narrative

## Baseline System

The baseline system represents a typical modern agentic architecture:

```text
LangGraph
+ Vector DB
+ local memory
+ multiple retrieval layers
+ custom orchestration
+ repeated context assembly
```

Problems:

- fragmented memory
- stale context
- repeated retrieval
- token explosion
- duplicated orchestration
- no shared operational state
- difficult scaling
- weak real-time awareness

---

## Redis IRIS System

The IRIS system introduces:

```text
LangGraph
+ Redis IRIS Context Layer
```

Redis IRIS provides:

- shared memory
- real-time context
- operational state
- semantic retrieval
- structured retrieval
- semantic cache
- streams/events
- cross-agent coordination

Result:

- lower latency
- fewer tokens
- fewer tool calls
- stronger memory
- shared state
- live operational awareness
- scalable architecture

---

# Final Use Case

## AI Customer Operations Team

A customer writes:

```text
"Our production system is down again and we are considering canceling our renewal."
```

The system coordinates multiple agents:

| Agent | Responsibility |
|---|---|
| Support Agent | Tickets, escalations, customer sentiment |
| Incident Agent | Outages, deployments, service health |
| Account Agent | Renewals, ARR, stakeholder management |
| Billing Agent | Contracts, SLAs, credits |
| Escalation Agent | Executive summary and action plan |

All agents share operational context through Redis IRIS.

---

# UX and UI Vision

## UI Goals

The UI must feel:

- modern
- operational
- realtime
- enterprise-grade
- visually understandable
- benchmark-oriented
- presentation-ready

The UI is CRITICAL.

The UI must clearly visualize:

- before vs after
- context retrieval
- memory
- streams/events
- shared state
- latency reduction
- token reduction
- cache hits
- agent coordination

---

# Recommended UI Stack

## Frontend

Recommended:

```text
Next.js
TypeScript
TailwindCSS
shadcn/ui
Framer Motion
```

Why:

- modern enterprise feel
- fast iteration
- beautiful dashboards
- responsive layout
- streaming UI support
- easy charts and panels

---

## Backend

```text
Python
FastAPI
LangGraph
Redis
```

---

## Communication

```text
REST + WebSockets
```

WebSockets are important for:

- live metrics
- stream replay
- realtime updates
- event visualization

---

# UI Layout

# Main Demo Screen

The main screen should contain:

## Left Panel

### Customer Timeline

Shows:

- tickets
- incidents
- escalations
- deployment events
- customer messages
- billing events

Live updating.

---

## Center Panel

### Agent Conversation / Coordination

Shows:

- user request
- agent reasoning summaries
- support findings
- incident findings
- account findings
- billing findings
- escalation summary

This panel demonstrates:

- multi-agent coordination
- shared memory
- operational awareness

---

## Right Panel

### Metrics Dashboard

Shows:

- latency
- token usage
- memory hits
- cache hits
- retrieval count
- tool calls
- Redis operations
- vector search operations
- stream events processed

MOST IMPORTANT:

### BEFORE vs AFTER comparison cards.

---

# Additional Screens

## Context Explorer

Visualize:

- operational state
- memory entries
- Redis keys
- timelines
- relationships
- semantic retrieval

---

## Replay Events Screen

Allows:

- replaying outage events
- injecting customer messages
- changing account risk
- generating incident updates

This demonstrates realtime operational awareness.

---

## Benchmark Dashboard

Visualize:

- baseline latency
- IRIS latency
- token reduction
- memory hit rate
- cache hit rate
- scaling behavior
- concurrent sessions

Charts:

- p50 latency
- p95 latency
- token usage over time
- retrieval latency
- cache effectiveness

---

# Demo UX Flow

## Demo Step 1 — Baseline System

User says:

```text
Our production system is down again and we are considering canceling.
```

Baseline:

- large prompt
- repeated retrieval
- weak memory
- many tool calls
- slower answer

UI shows:

- high token count
- many retrievals
- fragmented context
- no shared memory

---

## Demo Step 2 — Teach Memory

User:

```text
Remember that Acme prefers executive summaries and was promised escalation if latency issues happen again.
```

IRIS stores:

- durable memory
- stakeholder preferences
- escalation commitment

---

## Demo Step 3 — New Session

User:

```text
Prepare a response for Acme.
```

Baseline:

- forgets previous promise

IRIS:

- recalls escalation commitment
- recalls stakeholder preferences
- tailors response

UI highlights:

- memory hit
- lower tokens
- shorter prompt
- faster response

---

## Demo Step 4 — Live Event Replay

Inject event:

```json
{
  "event_type": "incident_update",
  "status": "mitigated"
}
```

IRIS:

- updates timeline
- updates context
- informs agents

Baseline:

- stale state

UI highlights:

- stream event
- state change
- realtime context refresh

---

## Demo Step 5 — Cache Demonstration

User asks same executive summary again.

IRIS:

- cache hit
- reduced latency
- reduced tokens

UI highlights:

- semantic cache hit
- response time reduction

---

## Demo Step 6 — Multi-Agent Coordination

User:

```text
Create an internal action plan.
```

All agents coordinate through:

- shared memory
- shared context
- shared state

UI highlights:

- coordinated workflow
- no duplicated retrieval
- consistent information

---

# Implementation Strategy

The project MUST be built incrementally.

DO NOT start with the final architecture.

The value of Redis IRIS only becomes visible through contrast.

---

# EPICS

# EPIC 1 — Project Foundation

## Goal

Create the repository and local development environment.

---

## Tasks

### Task 1.1 — Create Repository Structure

Status: DONE (2026-05-26)

Deliverables:

- frontend/
- backend/
- graph/
- iris/
- baseline/
- data/
- benchmarks/
- docs/

Acceptance Criteria:

- repo builds locally
- linting works
- CI skeleton exists

Completion Notes:

- Created required top-level folders.
- Added root README and setup guidance.
- Added CI skeleton workflow at .github/workflows/ci.yml.
- Remaining acceptance checks (build/lint) will be validated as part of Task 1.2 runtime verification.

---

### Task 1.2 — Setup Docker Compose

Status: DONE (2026-05-26)

Services:

- frontend
- backend
- redis

Acceptance Criteria:

```text
Docker compose up starts everything.
```

Progress Notes:

- Added docker-compose.yml with frontend, backend, and redis services.
- Added Dockerfiles for frontend and backend.
- Added scripts/dev-up.sh and scripts/dev-down.sh to support docker-compose and docker compose.
- Compose config validates successfully with docker-compose config.
- Runtime verified successfully via ./scripts/dev-up.sh -d after starting Colima.
- Service status validated with docker-compose ps for frontend/backend/redis.

---

### Task 1.3 — Setup Redis

Status: DONE (2026-05-26)

Requirements:

- RedisJSON
- RediSearch
- Vector Search
- Streams support

Acceptance Criteria:

- Redis indexes can be created
- vector search works
- JSON docs work

Progress Notes:

- Redis Stack service is defined in Docker Compose.
- Added backend/scripts/verify_redis_stack.py for JSON/Search/Vector/Streams checks.
- Added backend image support to run verification script inside container.
- Verified JSON/Search/Vector/Streams successfully with:
  docker-compose exec -T backend python scripts/verify_redis_stack.py --host redis --port 6379

---

### Task 1.4 — Setup Frontend Framework

Status: DONE (2026-05-26)

Requirements:

- Next.js
- Tailwind
- shadcn/ui
- dark mode
- responsive layout

Acceptance Criteria:

- dashboard shell exists
- routing works
- websocket client works

Progress Notes:

- Added Next.js TypeScript app shell.
- Added first dashboard placeholder screen and global styling.
- Added live events panel with browser WebSocket client connected to backend WS endpoint.
- Added UI event injection action to demonstrate realtime update flow.
- Added TailwindCSS foundation dependencies and configuration files in frontend.
- Added global Tailwind layer wiring and a lightweight light/dark theme toggle in the home dashboard shell.
- Added shadcn/ui starter baseline with shared className helper and starter button/card primitives.
- Integrated starter shadcn-style components into the home dashboard shell.

---

# EPIC 2 — Synthetic Enterprise Data Engine

## Goal

Build a realistic operational enterprise dataset.

---

## Tasks

### Task 2.1 — Customer Generator

Status: DONE

Generate:

- 1000+ customers
- ARR
- renewal dates
- health scores
- account owners

Acceptance Criteria:

- realistic customer distribution
- seeded Acme Corp scenario

Progress Notes:

- Added deterministic seeded Acme scenario dataset at data/acme_seed.json.
- Current dataset supports repeatable local demos and orchestration handler behavior.
- Added deterministic generator script at data/generate_customers.py.
- Generated data/customers_seed.json with 1000 customers and realistic distribution fields.
- Expanded generator output to include linked stakeholders, tickets, and incidents with customer IDs.
- Added deterministic Acme-linked stakeholder/ticket/incident records for repeatable escalation demos.
- Added deterministic customer profile dimensions across generated records: industry, region, and account_tier.
- Added deterministic contract metadata across generated records: contract_id, term_months, billing_model, next_invoice_date, auto_renew, and sla_tier.
- Updated deterministic Acme customer seed with profile and contract schema and regenerated data/customers_seed.json with generator version 9 metadata.

---

### Task 2.2 — Stakeholder Generator

Status: DONE

Generate:

- executives
- engineers
- support contacts
- preferences
- sentiment

Acceptance Criteria:

- customer-linked stakeholders exist
- realistic communication patterns

Progress Notes:

- Expanded stakeholder generator in data/generate_customers.py with deterministic communication-pattern attributes and weighted sentiment based on customer health/risk context.
- Added communication fields for seeded Acme stakeholders to keep deterministic demo records schema-aligned with generated stakeholders.
- Regenerated data/customers_seed.json with updated stakeholder schema and generator version 3 metadata.

---

### Task 2.3 — Support Ticket Generator

Status: DONE

Generate:

- tickets
- escalations
- summaries
- severity
- timelines

Acceptance Criteria:

- recurring incident patterns exist
- ticket relationships exist

Progress Notes:

- Expanded ticket generator in data/generate_customers.py to emit deterministic relationship fields for origin type, linked incident reference, and escalation parent ticket reference.
- Wired ticket generation order to use same-customer incident outputs so incident-followup and executive-escalation tickets can be linked deterministically.
- Updated deterministic Acme ticket records with incident and escalation relationship fields and regenerated data/customers_seed.json with generator version 4 metadata.

---

### Task 2.4 — Incident Generator

Status: DONE

Generate:

- outages
- service degradation
- deployment failures
- timelines

Acceptance Criteria:

- incidents evolve over time
- incidents affect customers

Progress Notes:

- Incident generator now emits deterministic customer-impact and deployment-failure context fields for each incident.
- Added incident-level impact_scope plus customer_impact payload (affected_seats, affected_revenue_usd, downtime_minutes, renewal_risk_delta).
- Added deployment_context payload (deployment_id, track, triggered_by_deployment, root_cause) while preserving timeline progression and recurrence_count behavior.
- Updated deterministic Acme incident seed record to include the same incident impact and deployment context schema, and regenerated data/customers_seed.json with generator version 8 metadata.

---

### Task 2.5 — Usage Generator

Status: DONE

Generate:

- product usage
- declining trends
- adoption metrics
- anomalies

Acceptance Criteria:

- risk scenarios emerge naturally

Progress Notes:

- Expanded customer generator output with deterministic usage/adoption fields including seats_provisioned, active_seats, adoption_rate_pct, monthly_active_trend, and anomalies.
- Added trend modeling rules that surface declining adoption and anomaly patterns aligned to risk level and health context.
- Updated deterministic Acme customer record with declining usage trend and anomaly signals, and regenerated data/customers_seed.json with generator version 5 metadata.

---

### Task 2.6 — Memory Generator

Status: DONE

Generate:

- previous escalations
- promises
- frustrations
- preferences

Acceptance Criteria:

- memory continuity scenarios exist

Progress Notes:

- Expanded customer generator output with deterministic memory_profile fields that model prior escalations, promises, frustrations, and communication preference continuity.
- Added historical memory timeline entries per customer to seed cross-session continuity scenarios.
- Updated deterministic Acme customer seed with continuity memory profile and regenerated data/customers_seed.json with generator version 6 metadata.

---

### Task 2.7 — Event Stream Generator

Status: DONE

Generate:

- support events
- incident updates
- customer messages
- deployment events

Acceptance Criteria:

- replayable streams exist

Progress Notes:

- Expanded event stream generation in data/generate_customers.py to emit deterministic support_note, customer_message, and deployment_event entries in addition to ticket_update and incident_update events.
- Kept event payloads customer-linked and globally time-sorted to preserve replay timeline determinism.
- Regenerated data/customers_seed.json with generator version 7 metadata and validated multi-type event stream coverage.

---

# EPIC 3 — Baseline LangGraph System

## Goal

Implement the intentionally limited baseline.

---

## Tasks

### Task 3.1 — Baseline Graph

Status: IN PROGRESS

Implement:

- support agent
- incident agent
- account agent
- billing agent
- escalation agent

Acceptance Criteria:

- agents coordinate successfully
- no Redis dependencies

Progress Notes:

- Added baseline orchestration handler at backend/app/workflows.py.
- Endpoint /api/run/baseline now uses handler-based response assembly.
- Added graph-style node pipeline module at backend/app/graph_pipeline.py.
- Migrated baseline and IRIS path execution to LangGraph StateGraph runtime at backend/app/langgraph_pipeline.py.
- Workflow handlers now execute through compiled LangGraph nodes/edges entry points.

---

### Task 3.2 — Local Memory

Status: DONE

Implement:

- naive memory
- chat history injection
- local session state

Acceptance Criteria:

- memory works only within session

Progress Notes:

- Added naive in-process baseline session memory store in backend/app/workflows.py keyed by customer.
- Baseline workflow now passes local_history and local_state payloads into backend/app/langgraph_pipeline.py for same-session continuity hints.
- Baseline graph now emits session-local-memory-cold / session-local-memory-hit and session-turn-index context signals.
- Validated same-session behavior with repeated baseline workflow calls showing cold first turn, hit on second turn, and summary continuity note reuse.

---

### Task 3.3 — Baseline Retrieval Layer

Status: DONE

Implement:

- local JSON retrieval
- simple keyword retrieval
- fake vector retrieval

Acceptance Criteria:

- baseline works but is inefficient

Progress Notes:

- Added baseline local JSON retrieval pass in backend/app/langgraph_pipeline.py that scans customer, incident, ticket, and stakeholder seed snippets.
- Added simple keyword retrieval scoring and deterministic fake-vector retrieval scoring paths over local seed snippets without external embedding dependencies.
- Wired retrieval outcomes into baseline summary narrative and context signals (baseline-json-retrieval, baseline-keyword-retrieval-hit/empty, baseline-fake-vector-hit/empty, baseline-documents-scanned).
- Validated runtime behavior with repeated baseline calls and confirmed retrieval signals and continuity behavior in baseline responses.

---

### Task 3.4 — Metrics Instrumentation

Status: DONE

Capture:

- latency
- tokens
- tool calls
- retrieval counts

Acceptance Criteria:

- metrics visible in UI

Progress Notes:

- Added workflow-level runtime instrumentation in backend/app/workflows.py for both baseline and IRIS execution paths using perf_counter-based latency measurement.
- Added deterministic derived metrics for observed token estimates, retrieval signal counts, tool signal counts, and instrumentation_mode markers.
- Added runtime instrumentation context signals (runtime-metrics-enriched and runtime-latency-ms=*) for downstream UI and benchmark consumption.
- Validated baseline and IRIS workflow responses include runtime metrics enrichment fields and instrumentation signals.

---

# EPIC 4 — Redis IRIS Integration

## Goal

Introduce Redis IRIS capabilities incrementally.

---

## Tasks

### Task 4.1 — RedisJSON Operational State

Status: DONE

Move:

- customers
- incidents
- tickets
- contracts
- usage

into Redis.

Acceptance Criteria:

- structured retrieval works
- latency measured

Progress Notes:

- Added RDI-style RedisJSON sync in backend/app/redis_iris_tools.py to move customers, tickets, and incidents into Redis JSON keys.
- Added customer-to-entity linkage keys for incident and ticket retrieval.
- Added container data mount in docker-compose.yml so generated data/customers_seed.json is available to backend at /data/customers_seed.json.
- Added first-class RedisJSON sync for contract:{customer_id} and usage:{customer_id} entities with customer linkage keys.
- Extended Redis sync status payload to include synced_contracts and synced_usage counters for operational observability.
- Extended Redis context and merge path so customer contract and usage data are hydrated from RedisJSON into shared operational context payloads.

---

### Task 4.2 — Redis Search

Status: IN PROGRESS

Implement:

- structured search
- filtering
- timelines

Acceptance Criteria:

- operational retrieval faster than baseline

Progress Notes:

- Added FT.SEARCH indexes for customer, ticket, and incident JSON documents in backend/app/redis_iris_tools.py.
- IRIS context retriever now resolves customer/ticket/incident context through FT.SEARCH-driven lookups.

---

### Task 4.3 — Redis Vector Search

Status: IN PROGRESS

Implement embeddings for:

- ticket summaries
- incidents
- memory
- customer notes

Acceptance Criteria:

- similar incidents retrievable

Progress Notes:

- Added deterministic incident pseudo-embedding generation in backend/app/redis_iris_tools.py to support local vector retrieval without model-service dependencies.
- Added Redis vector index idx:incident_vectors and incident_vec:* records during RDI sync.
- IRIS context retrieval now runs KNN vector search for similar incidents and returns similar_incidents context payload.
- IRIS workflow now surfaces redis-vector-similar-incidents in context_signals when vector results are found.

---

### Task 4.4 — Redis Agent Memory

Status: DONE (2026-05-26)

Implement:

- short-term memory
- long-term memory
- memory extraction
- memory retrieval

Acceptance Criteria:

- cross-session recall works
- cross-agent recall works

Progress Notes:

- Added Redis agent memory read/write in backend/app/redis_iris_tools.py via memory:<customer_id> lists.
- Wired IRIS workflow in backend/app/workflows.py to read prior memory during context retrieval and append new memory per request.
- Added deterministic memory-fact extraction in backend/app/redis_iris_tools.py for preference, commitment, renewal-risk, and operational-risk continuity facts.
- Added short-term and long-term Redis memory key separation (memory:<customer_id> and memory:long:<customer_id>) with bounded deduplicated storage.
- Added query-aware memory retrieval ranking so relevant durable memories are prioritized for shared context hydration.
- Wired IRIS workflow post-processing to persist extracted long-term memory facts and emit redis-agent-memory-extract plus long-term write signal counters.

---

### Task 4.5 — Shared Operational Context

Status: DONE (2026-05-26)

Implement:

- shared customer state
- shared workflow state
- shared timelines

Acceptance Criteria:

- agents share consistent context

Progress Notes:

- Added Redis Context Retriever implementation in backend/app/redis_iris_tools.py for customer + incident + ticket retrieval.
- Wired IRIS workflow enrichment in backend/app/workflows.py using retrieved shared operational context before LangGraph execution.
- Added runtime signal redis-ft-search-context in backend/app/workflows.py to confirm FT.SEARCH context path usage.
- Added shared workflow-state persistence in backend/app/redis_iris_tools.py via workflow_state:<customer_id> keys with bounded payload shape.
- Extended Redis context hydration and merge path to include shared_workflow_state in IRIS seed payloads for cross-turn continuity.
- Wired IRIS workflow runtime to emit redis-shared-workflow-state-hit, redis-shared-workflow-state-write, and redis-shared-workflow-turn signals.

---

### Task 4.6 — Redis Streams

Status: DONE (2026-05-26)

Implement:

- live updates
- replay events
- operational events

Acceptance Criteria:

- live UI updates work
- agents react to events

Progress Notes:

- Added Redis Streams append helper in backend/app/redis_iris_tools.py (events:operational) for operational event persistence.
- Wired event publishing path in backend/app/main.py so manual injections and replay-generated events are both published to WS subscribers and written to Redis Streams.
- Added server-driven replay run endpoints for execution/status/cancel to support stream-aware operational playback.
- Added Redis stream-read helper in backend/app/redis_iris_tools.py to retrieve recent operational events from events:operational with optional customer filtering.
- Wired IRIS workflow in backend/app/workflows.py to merge stream-backed events with event-bus snapshots for resilient context hydration after restarts.
- Added stream reactivity runtime signals in backend/app/workflows.py: redis-streams-context-hit/empty and redis-streams-context-count=*.

---

### Task 4.7 — Semantic Cache

Status: DONE (2026-05-26)

Implement:

- repeated summary caching
- embedding similarity cache

Acceptance Criteria:

- repeated queries faster
- token reduction visible

Progress Notes:

- Added LangCache-style response cache in backend/app/redis_iris_tools.py with TTL-based storage.
- Wired IRIS workflow in backend/app/workflows.py to return cache hits early and write back cache entries on completion.
- Extended Redis cache retrieval in backend/app/redis_iris_tools.py with similarity fallback across bounded per-customer cache indexes.
- Added exact-hit and semantic-hit trace signals (redis-langcache-exact-hit, redis-langcache-semantic-hit, redis-langcache-similarity=*).
- Preserved backward-compatible reads for legacy direct cache payloads while storing wrapped payloads for semantic lookup metadata.

---

# EPIC 5 — Modern UI and UX

## Goal

Build a presentation-grade operational AI dashboard.

---

## Tasks

### Task 5.1 — Main Dashboard Layout

Implement:

- three-column layout
- timeline panel
- agent coordination panel
- metrics panel

Acceptance Criteria:

- responsive layout
- polished design

Progress Notes:

- Main page now includes a benchmark trend panel section that spans wider dashboard space on desktop and collapses cleanly on mobile.

---

### Task 5.2 — Agent Visualization

Show:

- active agent
- retrievals
- handoffs
- shared memory usage

Acceptance Criteria:

- coordination visually understandable

---

### Task 5.3 — Metrics Visualization

Status: DONE (2026-05-26)

Implement:

- token charts
- latency charts
- memory hit charts
- cache hit charts

Acceptance Criteria:

- before/after visible immediately

Progress Notes:

- Added benchmark trend visualization panel with baseline vs IRIS latency/token trends in frontend/components/benchmark-trend-panel.tsx.
- Added latest snapshot KPI summaries for latency average, p95 latency, prompt tokens, and computed IRIS improvement percentages.
- Metrics panel is sourced from trend-history snapshots via backend endpoint GET /api/benchmarks/trends.
- Added runtime metrics panel in frontend/components/runtime-metrics-panel.tsx for live baseline-vs-IRIS request-level instrumentation.
- Added comparative bars and improvement indicators for runtime latency, prompt tokens, memory hits, cache hits, retrieval signals, and tool signals.
- Integrated runtime metrics panel into frontend/app/page.tsx to make before/after signals visible immediately on each dashboard refresh.

---

### Task 5.4 — Before vs After Toggle

Status: DONE (2026-05-26)

Implement:

- baseline mode
- IRIS mode

Acceptance Criteria:

- same workflow runs in both modes
- differences measurable

Progress Notes:

- Added before/after toggle panel in frontend/components/before-after-toggle-panel.tsx with Baseline mode, IRIS mode, and side-by-side comparison mode.
- Integrated toggle panel into frontend/app/page.tsx and removed static duplicated baseline/IRIS cards in favor of mode-based viewing.
- Added measurable delta indicators for latency, prompt tokens, retrieval calls, and tool calls derived from the same request run outputs.

---

### Task 5.5 — Replay Events UI

Status: DONE (2026-05-26)

Implement:

- replay controls
- inject events
- stream playback

Acceptance Criteria:

- realtime updates visible

Progress Notes:

- Added replay controls to frontend live events panel with play, pause, next-step, and reset actions.
- Added three event templates for degradation recovery, renewal risk, and deployment regression scenarios.
- Added timeline view showing pending, active, and completed playback steps.
- Replayed steps are injected via existing /api/events/inject endpoint and observed through WS /ws/events updates.
- Added backend template discovery and server-driven replay execution APIs to support migration from frontend-local templates to backend-owned replay orchestration.
- Frontend replay panel now loads templates from GET /api/replay/templates instead of static local template definitions.
- Frontend replay controls now execute server-driven replays through POST /api/replay/execute (step and full modes).
- Frontend replay panel now polls GET /api/replay/runs/{run_id} to reflect backend run progress and timeline advancement.
- Frontend replay panel now includes cancel control wired to POST /api/replay/runs/{run_id}/cancel for active full replay runs.
- Added runtime metrics visualization panel comparing baseline vs IRIS live request instrumentation.
- Added side-by-side charts for latency, prompt tokens, memory hits, cache hits, retrieval signals, and tool signals.
- Integrated runtime metrics panel into dashboard and validated responsive rendering in production build.
- Added replay playback-speed selector (0.5x to 10x) in frontend/components/live-events-panel.tsx and wired selected speed to replay run execution payload.
- Added replay progress indicator and completed-step counters so stream playback advancement is visible in realtime.
- Added source metadata display for received events to distinguish manual, replay-template, and stream-originated updates.

---

# EPIC 6 — Benchmarking and Proof

## Goal

Prove Redis IRIS improvements quantitatively.

---

## Tasks

### Task 6.1 — Benchmark Harness

Status: DONE (2026-05-26)

Simulate:

- repeated queries
- concurrent sessions
- memory-heavy workflows

Acceptance Criteria:

- repeatable benchmarks

Progress Notes:

- Added benchmark harness script at benchmarks/run_benchmark.py.
- Generated first report at benchmarks/reports/latest.json.
- Added CI smoke benchmark output path at benchmarks/reports/ci-latest.json.
- CI workflow now runs benchmark smoke checks after health and Redis capability verification.
- Added extended benchmark output path at benchmarks/reports/ci-extended.json.
- CI now supports quick smoke and extended performance scenarios with split triggers.
- Added trend snapshot appender at benchmarks/update_trend_snapshot.py with history output file.
- Added regression gate checker at benchmarks/check_regression.py with threshold controls.
- Added baseline snapshot at benchmarks/reports/regression-baseline.json for CI smoke comparison.
- Added strict/normal/lenient regression profile policy with optional per-metric overrides in benchmarks/check_regression.py.
- Added concurrent-session benchmark harness at benchmarks/run_concurrent_benchmark.py.
- Added concurrent benchmark output path at benchmarks/reports/concurrent-latest.json.
- Added frontend benchmark trend visualization integrated into the dashboard shell from trend-history snapshots.
- Added CI artifact upload bundles for smoke and extended benchmark outputs in .github/workflows/ci.yml.
- Added scenario-profile support in benchmarks/run_benchmark.py with smoke and expanded workload modes.
- Added deterministic scenario matrix coverage for repeated-query and memory-heavy prompt flows with per-scenario benchmark breakdown output.
- Updated extended CI benchmark run to execute run_benchmark.py with --scenario-profile expanded.

---

### Task 6.2 — Token Measurement

Status: DONE (2026-05-26)

Measure:

- prompt tokens
- completion tokens
- total tokens

Acceptance Criteria:

- token reduction measurable

Progress Notes:

- Expanded benchmarks/run_benchmark.py to extract and report prompt_tokens_avg, completion_tokens_avg, and total_tokens_avg for baseline and IRIS modes.
- Expanded per-scenario benchmark breakdown output with the same token triplet so token reductions are visible by workload shape.
- Expanded benchmarks/run_concurrent_benchmark.py to include prompt/completion/total token averages under concurrent load.
- Preserved existing prompt_tokens_avg fields for compatibility with existing regression and visualization consumers.

---

### Task 6.3 — Latency Measurement

Status: DONE (2026-05-26)

Measure:

- p50
- p95
- retrieval latency
- LLM latency

Acceptance Criteria:

- latency reductions visible

Progress Notes:

- Expanded benchmarks/run_benchmark.py with latency_ms_p50 while preserving existing latency_ms_avg and latency_ms_p95 outputs used by regression checks.
- Added runtime latency summaries (runtime_latency_ms_avg, runtime_latency_ms_p50, runtime_latency_ms_p95) from runtime instrumentation metrics.
- Added retrieval_latency_ms_avg and llm_latency_ms_avg reporting for baseline and IRIS benchmarks in both standard and concurrent harness scripts.
- Expanded backend runtime instrumentation in backend/app/workflows.py with deterministic retrieval/LLM/orchestration latency decomposition fields.

---

### Task 6.4 — Cache Effectiveness

Status: DONE (2026-05-26)

Measure:

- cache hit rate
- repeated query savings

Acceptance Criteria:

- semantic cache value visible

Progress Notes:

- Expanded benchmarks/run_benchmark.py to parse cache-hit context signals and report cache_hits, cache_exact_hits, cache_semantic_hits, and cache_hit_rate_pct.
- Added repeated-query runtime latency savings metrics in standard benchmark output (first-query vs repeated-query runtime latency averages and savings percentage).
- Expanded benchmarks/run_concurrent_benchmark.py with cache hit metrics and cache hit rate reporting under concurrent load.
- Preserved existing latency/token benchmark fields used by regression gate and trend consumers.

---

### Task 6.5 — Multi-Agent Coordination Metrics

Status: DONE (2026-05-26)

Measure:

- duplicate retrievals
- shared memory hits
- tool call reductions

Acceptance Criteria:

- coordination improvements visible

Progress Notes:

- Expanded benchmarks/run_benchmark.py to extract retrieval_signals and tool_signals from runtime metrics and report duplicate_retrieval_signals_avg.
- Added shared_memory_hits and shared_memory_hit_rate_pct from runtime context signals (redis-agent-memory-hit and redis-shared-workflow-state-hit).
- Added coordination_comparison output in standard and concurrent harness reports for retrieval/tool/duplicate-retrieval reductions plus shared-memory-hit-rate delta.
- Preserved existing benchmark output fields used by regression checks and trend consumers while appending coordination metrics.

---

# EPIC 7 — Azure Readiness

## Goal

Prepare architecture for Azure Managed Redis and MAF.

---

## Tasks

### Task 7.1 — Redis Abstraction Layer

Status: DONE (2026-05-26)

Implement:

- centralized Redis client
- env-based config
- TLS support

Acceptance Criteria:

- local and Azure Redis compatible

Progress Notes:

- Added centralized Redis connection abstraction in backend/app/redis_client.py with a single env-driven configuration model and reusable client factory.
- Added REDIS_URL support alongside REDIS_HOST/REDIS_PORT/REDIS_DB and optional REDIS_USERNAME/REDIS_PASSWORD inputs for compatibility across local and hosted Redis.
- Added TLS-aware Redis configuration support (REDIS_TLS, REDIS_TLS_INSECURE, and optional cert paths), including rediss URL auto-detection for Azure Managed Redis.
- Refactored Redis tool initialization in backend/app/redis_iris_tools.py and runtime config output in backend/app/main.py to use centralized Redis connection settings.
- Expanded backend/scripts/verify_redis_stack.py and .env.example to support REDIS_URL and TLS validation workflows for Azure compatibility checks.

---

### Task 7.2 — Kubernetes Readiness

Status: DONE (2026-05-26)

Implement:

- stateless backend
- Redis-backed state
- scaling tests

Acceptance Criteria:

- multiple replicas work

Progress Notes:

- Added Redis-backed runtime state adapter in backend/app/runtime_state.py with TTL-based persistence for baseline session continuity and replay run-state visibility.
- Refactored baseline runtime flow in backend/app/workflows.py to read/write customer continuity session state from Redis when available, with explicit fallback signals when Redis is unavailable.
- Refactored replay manager in backend/app/main.py to persist run lifecycle updates to shared Redis state and expose cross-replica run visibility via GET /api/replay/runs/{run_id}.
- Added cross-replica replay cancellation signaling by writing cancellation_requested status into shared state and honoring it during replay execution loops.
- Added backend/scripts/check_scaling_readiness.py plus README runbook guidance to validate stateless + Redis-backed scaling behavior, including baseline continuity and replay status checks.

---

### Task 7.3 — Azure Compatibility Validation

Status: DONE (2026-05-26)

Validate:

- Search
- JSON
- vectors
- Streams
- TLS

Acceptance Criteria:

- architecture deployable to AMR

Progress Notes:

- Added backend/scripts/validate_azure_compatibility.py to validate Redis capability coverage (RediSearch, RedisJSON, vector search, Streams) and TLS posture for Azure readiness.
- Added backend runtime compatibility verification in the same script against GET /api/config for redis_tools_enabled and redis_tls signaling.
- Added Azure Managed Redis validation runbook commands and local non-TLS smoke-mode instructions in README.md.
- Reused centralized Redis connection inputs (URL/host/port/credentials/TLS cert settings) so validation aligns with deployment runtime configuration.
- Completed syntax/diagnostic validation for updated task artifacts and recorded queue progression to EPIC 8 Task 8.1.

---

# EPIC 8 — Microsoft Agent Framework Portability

## Goal

Prepare future MAF migration.

---

## Tasks

### Task 8.1 — Framework-Agnostic Context Layer

Status: DONE (2026-05-26)

Ensure:

- Redis layer independent of LangGraph
- orchestration separated cleanly

Acceptance Criteria:

- Redis APIs reusable in MAF

Progress Notes:

- Added backend/app/context_layer.py as a framework-agnostic context packet module that assembles Redis-backed seed/context and merged operational events without LangGraph dependencies.
- Refactored IRIS orchestration in backend/app/workflows.py to consume context packets from the context layer rather than embedding Redis context assembly in workflow logic.
- Moved Redis post-processing behavior (agent-memory writes, extracted long-term facts, shared workflow-state updates, cache-store signaling) into context-layer helpers.
- Added README architecture boundary notes describing how context_layer.py is reusable for future MAF orchestration.
- Completed compile/diagnostic validation for the refactor and advanced queue to EPIC 8 Task 8.2.

---

### Task 8.2 — Shared State Contracts

Status: DONE (2026-05-26)

Define:

- memory schema
- event schema
- retrieval APIs

Acceptance Criteria:

- contracts framework-agnostic

Progress Notes:

- Added backend/app/state_contracts.py with framework-agnostic contracts for memory records, event records, and retrieval request/response payloads.
- Added contract normalization helpers for event payloads and memory records, plus retrieval contract assembly helpers decoupled from orchestration framework concerns.
- Wired backend/app/main.py event publish/read paths to normalize payloads using the shared event contract before stream writes and event-bus fanout.
- Wired backend/app/context_layer.py to emit retrieval API contract summaries alongside context packets and context signals.
- Added README contract boundary documentation and advanced queue to EPIC 8 Task 8.3 after compile/diagnostic validation.

---

### Task 8.3 — Migration Documentation

Document:

- LangGraph node mapping
- equivalent MAF orchestration
- Redis reuse strategy

Acceptance Criteria:

- migration path clear

---

# EPIC 9 — Learning Mode and Interactive Architecture Explorer

## Goal

Add a dedicated learning mode that explains how the system works internally.

This is a critical part of the demo.

The demo should not only show that Redis IRIS improves the agentic app.

It should also teach:

- what happens behind the scenes
- which component does what
- how data flows through the system
- why Redis matters
- where LangGraph ends and IRIS begins
- why the IRIS architecture is different from a classic vector database stack

---

## Learning Mode Positioning

The learning mode should answer one question clearly:

```text
What actually happens when a user asks an agentic app a question?
```

And then contrast:

```text
What happens without IRIS?
```

versus:

```text
What happens with IRIS?
```

---

# Learning Mode UI Concept

## Main Feature

An interactive architecture diagram with clickable components.

Recommended implementation:

```text
React Flow
+ Next.js
+ Tailwind
+ shadcn/ui
+ Framer Motion
```

React Flow is recommended because it supports:

- draggable nodes
- animated edges
- clickable components
- graph layouts
- zoom/pan
- step-by-step visual flows
- custom node rendering

---

# Learning Mode Screens

## Screen 1 — Architecture Overview

High-level diagram:

```text
User
  -> Frontend
  -> FastAPI Backend
  -> LangGraph Orchestrator
  -> Agents
  -> Redis IRIS Context Layer
  -> LLM
```

Clickable components:

- User request
- Frontend
- Backend API
- LangGraph
- Support Agent
- Incident Agent
- Account Agent
- Billing Agent
- Escalation Agent
- Redis Agent Memory
- Redis Search
- Redis Vector Search
- Redis Streams
- RedisJSON
- Semantic Cache
- LLM
- Metrics Layer

---

## Screen 2 — Before IRIS Data Flow

Show the baseline data flow:

```text
User Request
  -> LangGraph
  -> Agent 1 -> local JSON / fake DB
  -> Agent 2 -> separate retrieval
  -> Agent 3 -> local memory
  -> LLM
  -> Response
```

Highlight problems visually:

- repeated retrieval
- duplicated context
- stale data
- prompt bloat
- no shared memory
- many tool calls
- weak cross-session state

Use red or warning indicators.

---

## Screen 3 — With Redis IRIS Data Flow

Show the improved flow:

```text
User Request
  -> LangGraph
  -> IRIS Context Retriever
  -> Redis Search / JSON / Vector / Memory / Streams / Cache
  -> Compact Context Packet
  -> Agents
  -> LLM
  -> Response
  -> Save Memory / Update State / Cache Result
```

Highlight benefits visually:

- shared context
- fewer retrievals
- compact prompt
- memory hit
- cache hit
- live event update
- consistent state

Use green success indicators.

---

## Screen 4 — Step-by-Step Execution Playback

A presenter should be able to click:

```text
Play Request Flow
```

Then the UI animates each step:

1. User submits request
2. Backend receives request
3. LangGraph classifies intent
4. Context Retriever extracts entities
5. Redis Search retrieves structured customer state
6. Redis Vector Search retrieves similar incidents
7. Redis Agent Memory retrieves prior commitments
8. Redis Streams provides latest incident events
9. Semantic cache checks for repeated query
10. Compact context packet is created
11. Agents collaborate using shared context
12. LLM generates grounded response
13. Memory is updated
14. Metrics are recorded
15. UI displays final answer

---

## Screen 5 — Component Inspector

When the user clicks a component, show a side panel.

Example component details:

### LangGraph Orchestrator

Role:

```text
Controls the workflow and decides which agent runs next.
```

What it does:

- routes requests
- maintains graph state
- coordinates agents
- invokes tools
- combines outputs

What it does NOT do:

- store long-term operational context
- provide low-latency shared memory
- index business data
- cache semantic responses

---

### Redis IRIS Context Layer

Role:

```text
Provides the shared operational context used by agents.
```

What it does:

- stores customer state
- stores memory
- retrieves structured data
- retrieves semantic matches
- handles live events
- supports caching
- provides low-latency access

Why Redis matters:

- real-time state
- low latency
- shared memory
- streams
- search
- vectors
- operational data structures

---

### Redis Agent Memory

Role:

```text
Stores durable short-term and long-term memory for agents.
```

Examples:

- customer preferences
- prior promises
- escalation history
- analyst notes
- session summaries

Demo value:

- cross-session recall
- personalization
- reduced prompt size
- better continuity

---

### Redis Search

Role:

```text
Retrieves structured operational data using filters and full-text search.
```

Examples:

- open tickets for customer
- active incidents
- renewal date
- risk level
- SLA status

Demo value:

- precise retrieval
- fast filtering
- avoids dumping entire data into prompts

---

### Redis Vector Search

Role:

```text
Finds semantically similar context.
```

Examples:

- similar incidents
- similar customer complaints
- related support summaries
- relevant memories

Demo value:

- semantic retrieval beyond keywords
- similar-case reasoning
- better context relevance

---

### Redis Streams

Role:

```text
Carries live operational events.
```

Examples:

- incident update
- ticket escalation
- customer message
- deployment event
- usage anomaly

Demo value:

- real-time awareness
- live updates
- event-driven agent workflows

---

### Semantic Cache

Role:

```text
Reuses answers or context for repeated or similar queries.
```

Demo value:

- lower latency
- fewer LLM calls
- fewer tokens
- lower cost

---

## Screen 6 — Context Packet Viewer

Show the actual context packet sent to the LLM.

Example:

```json
{
  "customer": {
    "name": "Acme Corp",
    "risk_level": "high",
    "renewal_date": "2026-07-15"
  },
  "memory": [
    "Customer was promised executive escalation if latency issues recur."
  ],
  "active_incidents": [
    "search-api p95 latency elevated"
  ],
  "similar_incidents": [
    "Latency spike after deployment rollback in April"
  ],
  "recommended_actions": [
    "Escalate to executive sponsor",
    "Offer SLA credit review"
  ]
}
```

This is important because it proves:

```text
IRIS does not just retrieve documents.
IRIS assembles operational context.
```

---

## Screen 7 — Token and Latency Explanation

Explain why tokens go down.

Before IRIS:

```text
Full chat history + repeated ticket summaries + repeated account data + duplicated agent context
```

After IRIS:

```text
Relevant memory + compact customer facts + latest events + semantic cache
```

Show visual comparison:

| Area | Baseline | IRIS |
|---|---:|---:|
| Prompt size | large | compact |
| Retrieval calls | many | fewer |
| Memory recall | weak | strong |
| Cache use | none | yes |
| Context freshness | stale/manual | live |

---

# Interactive Diagram Requirements

## Nodes

Minimum required nodes:

```text
User
Frontend
Backend API
LangGraph Orchestrator
Support Agent
Incident Agent
Account Agent
Billing Agent
Escalation Agent
Context Retriever
Redis Agent Memory
Redis Search
Redis Vector Search
Redis Streams
RedisJSON
Semantic Cache
LLM
Metrics Collector
```

---

## Edges

Edges should represent:

- request flow
- context retrieval
- memory retrieval
- vector retrieval
- event updates
- LLM calls
- memory writes
- cache writes
- metrics writes

---

## Interaction States

Each node should support:

- idle
- active
- success
- warning
- cache-hit
- memory-hit
- error

---

## Animation Modes

Required:

```text
Manual Step Mode
Auto Play Mode
Before Mode
After Mode
Comparison Mode
```

---

# Learning Mode Data Model

Add a frontend-accessible explanation model:

```typescript
type ArchitectureNode = {
  id: string;
  label: string;
  category: "user" | "frontend" | "orchestrator" | "agent" | "redis" | "llm" | "metrics";
  shortDescription: string;
  responsibilities: string[];
  beforeIRIS?: string[];
  afterIRIS?: string[];
  demoValue: string[];
};
```

Add flow steps:

```typescript
type FlowStep = {
  id: string;
  title: string;
  description: string;
  activeNodes: string[];
  activeEdges: string[];
  metricChanges?: Record<string, number | string>;
  contextPreview?: unknown;
};
```

---

# Learning Mode API Endpoints

Add backend endpoints:

```text
GET /api/learning/architecture
GET /api/learning/flow/baseline
GET /api/learning/flow/iris
GET /api/learning/component/{component_id}
GET /api/learning/context-packet/latest
GET /api/learning/metrics/latest
```

---

# EPIC 9 Tasks

## Task 9.1 — Add Learning Mode Page

Status: IN PROGRESS

Create:

```text
frontend/app/learning/page.tsx
```

Acceptance Criteria:

- page loads
- shows architecture diagram shell
- navigation from main demo exists

Progress Notes:

- Added learning page shell at frontend/app/learning/page.tsx with architecture overview and implementation-ready section placeholders.
- Added navigation entry from main demo page to /learning in frontend/app/page.tsx.

---

## Task 9.2 — Implement React Flow Diagram

Status: DONE (2026-05-26)

Implement:

- nodes
- edges
- zoom/pan
- clickable nodes
- side panel

Acceptance Criteria:

- user can click each component
- side panel explains component role

Progress Notes:

- Added backend learning-mode architecture payload endpoint GET /api/learning/architecture with node and edge datasets shaped for diagram rendering.
- Added frontend interactive diagram shell wired to GET /api/learning/architecture with clickable nodes, zoom/pan controls, and inspector panel content.

---

## Task 9.3 — Implement Before/After Toggle

Status: DONE (2026-05-26)

Modes:

```text
Baseline
IRIS
Comparison
```

Acceptance Criteria:

- diagram changes by mode
- baseline shows fragmented architecture
- IRIS shows shared context layer

Progress Notes:

- Added backend flow payload endpoints GET /api/learning/flow/baseline and GET /api/learning/flow/iris to supply before/after explanatory data.
- Wired Learning Mode UI toggle controls for Baseline, IRIS, and Comparison and bound them to mode-specific node/edge rendering and summary text.

---

## Task 9.4 — Implement Step-by-Step Playback

Status: DONE (2026-05-26)

Controls:

- play
- pause
- next
- previous
- reset

Acceptance Criteria:

- request flow animates step by step
- active nodes and edges are highlighted

Progress Notes:

- Learning-mode flow payloads now include ordered activeNodes and activeEdges arrays to support future playback highlighting.
- Implemented playback controls in the Learning Mode diagram and wired step progression to mode-specific active node/edge highlighting.

---

## Task 9.5 — Component Inspector Content

Status: DONE (2026-05-26)

Write explanations for:

- LangGraph
- each agent
- Redis Memory
- Redis Search
- Redis Vector Search
- Redis Streams
- RedisJSON
- Semantic Cache
- LLM
- Metrics Collector

Acceptance Criteria:

- every component has a clear explanation
- each explanation includes before/after value

Progress Notes:

- Learning Mode diagram shell now surfaces node shortDescription, responsibilities, demoValue, and before/after context in a side-panel inspector.
- Added backend component-level inspector payloads and endpoint GET /api/learning/component/{component_id} for dynamic panel content.
- Learning Mode inspector now renders component role, what-it-does, what-it-does-not-do, before/after value, why Redis matters (when relevant), and demo talk track.

---

## Task 9.6 — Context Packet Viewer

Status: DONE (2026-05-26)

Display:

- latest context packet
- structured facts
- memory hits
- semantic matches
- live events
- prompt estimate

Acceptance Criteria:

- presenter can show what goes into the LLM

Progress Notes:

- Added backend endpoint GET /api/learning/context-packet with latest teaching packet payload.
- Added Learning Mode context packet viewer section showing customer snapshot, structured facts, memory hits, semantic matches, live events, and prompt estimate.

---

## Task 9.7 — Metrics Education Panel

Status: DONE (2026-05-26)

Explain:

- why tokens decrease
- why latency decreases
- why memory hits matter
- why cache hits matter
- why real-time state matters

Acceptance Criteria:

- metrics are understandable to non-engineers

Progress Notes:

- Added backend endpoint GET /api/learning/metrics-education with baseline-vs-IRIS teaching metrics.
- Added Learning Mode metrics education panel with plain-language explanations for token, latency, memory-hit, cache-hit, and real-time state impact.

---

## Task 9.8 — Guided Demo Script Overlay

Status: DONE (2026-05-26)

Add an optional guided overlay:

```text
Step 1: Submit customer outage request
Step 2: Watch baseline context assembly
Step 3: Switch to IRIS
Step 4: Observe memory retrieval
Step 5: Replay live incident event
Step 6: Observe updated response
```

Acceptance Criteria:

- presenter can run the learning demo without memorizing every detail

Progress Notes:

- Added optional Guided Demo overlay in Learning Mode with step-by-step presenter instructions.
- Implemented six scripted walkthrough steps and linked them to diagram mode/step focus so presenters can progress without memorized flow.

---

## Task 9.9 — MAF Portability Mapping Panel

Status: DONE (2026-05-26)

Display:

- current architecture components
- MAF equivalent building blocks
- portability notes and migration effort
- staged migration sequence

Acceptance Criteria:

- presenter can explain how this architecture ports to MAF without re-architecting Redis context strategy

Progress Notes:

- Added backend endpoint GET /api/learning/maf-portability with component mapping and migration plan payload.
- Added Learning Mode MAF portability panel with mapping table and migration steps for presenter walkthrough.

---

## Task 9.10 — Presenter Auto-Tour Mode

Status: DONE (2026-05-26)

Add presenter auto-tour mode with timed highlights:

```text
Timed guided-step progression
+ focus-node highlight transitions
+ mode/step synchronization
+ tour status visibility
```

Acceptance Criteria:

- presenter can run the architecture walkthrough hands-free with paced, timed highlights

Progress Notes:

- Added timed auto-tour controls to Learning Mode Guided Demo with start/stop behavior and final-step auto-stop.
- Kept auto-tour synchronized with guided step mode switching, flow-step focus, and node highlight selection.
- Added guided overlay tour status metadata and cadence visibility for presenter pacing.

---

## Task 9.11 — Baseline-vs-IRIS Context Diff Narrative

Status: DONE (2026-05-26)

Display side-by-side context narrative:

```text
Baseline context assembly
vs
IRIS shared context packet
```

Acceptance Criteria:

- presenter can explain exactly what context changes between baseline and IRIS and why response quality and efficiency improve

Progress Notes:

- Added backend endpoint GET /api/learning/context-diff with baseline and IRIS packet snapshots, narrative deltas, and comparison metrics.
- Added Learning Mode Context Diff Narrative panel with side-by-side packet cards and presenter-ready delta callouts.

---

## Enhancement — Narrated Metrics Storytelling Mode

Status: DONE (2026-05-26)

Deliver narrated pacing flow:

```text
chaptered KPI narrative
+ timed playback
+ executive talk track prompts
```

Acceptance Criteria:

- presenter can run a metrics-focused story sequence with clear pacing and chapter-by-chapter business messaging

Progress Notes:

- Added backend endpoint GET /api/learning/metrics-storytelling with chapter narratives, KPI highlights, and default pacing metadata.
- Added interactive Learning Mode storytelling panel with chapter playback controls and presenter hints.

---

## Enhancement — Audience Q and A Mode with Pre-Mapped Architecture Answers

Status: DONE (2026-05-26)

Deliver live audience answer support:

```text
curated audience questions
+ pre-mapped architecture answers
+ category-driven quick navigation
```

Acceptance Criteria:

- presenter can rapidly answer common architecture, performance, reliability, portability, and operations questions using pre-mapped guided responses

Progress Notes:

- Added backend endpoint GET /api/learning/audience-qa with curated questions, mapped component anchors, and presenter sequencing hint.
- Added interactive Learning Mode Audience Q and A panel with category tabs, question picker, and mapped component chips.

---

## Enhancement — Exportable Learning Summary Handout for Stakeholder Follow-up

Status: DONE (2026-05-26)

Deliver post-demo handout support:

```text
stakeholder summary sections
+ measurable proof points
+ exportable follow-up artifact
```

Acceptance Criteria:

- presenter can provide a concise, exportable follow-up handout summarizing architecture outcomes and business impact

Progress Notes:

- Added backend endpoint GET /api/learning/summary-handout with handout sections, takeaways, and export metadata.
- Added Learning Mode handout panel with stakeholder summary rendering and JSON download action.

---

## Enhancement — Presenter Annotation Mode for Technical vs Executive Talk Tracks

Status: DONE (2026-05-26)

Deliver role-aware presenter guidance:

```text
technical and executive tracks
+ topic-level speaking prompts
+ audience-adaptive demo narration
```

Acceptance Criteria:

- presenter can switch between executive and technical narration modes without leaving the Learning Mode flow

Progress Notes:

- Added backend endpoint GET /api/learning/presenter-annotations with dual-track presenter annotations and section focus metrics.
- Added Learning Mode presenter annotation panel with track switching and topic-level talk tracks.

---

# Learning Mode Acceptance Criteria

The learning mode is complete when a viewer can answer:

1. What does LangGraph do?
2. What does Redis IRIS do?
3. Why is Redis needed?
4. What data flows through the system?
5. Why is the IRIS version faster or cheaper?
6. Why does shared memory matter?
7. Why is this better than a vector DB-only architecture?
8. How would this later port to MAF?

---

# Updated Final Success Criteria

The project is successful if the audience understands:

## BEFORE

```text
Current agentic systems coordinate through prompts and fragmented retrieval.
```

## AFTER

```text
Redis IRIS provides shared operational context for stateful multi-agent systems.
```

And:

```text
LangGraph orchestrates.
Redis IRIS operationalizes.
```

That is the entire story.

