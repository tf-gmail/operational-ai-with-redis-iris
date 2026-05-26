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

## Working Rule

This document must be updated immediately when a task is completed.

## Immediate Next-Action Queue

1. Add MAF portability mapping panel in Learning Mode (EPIC 9 future-scope).
2. Add presenter auto-tour mode with timed highlights (EPIC 9 future-scope).
3. Add side-by-side context packet diff view between baseline and IRIS (EPIC 9 enhancement).
4. Add narrated metrics storytelling mode for executive demo pacing (EPIC 9 enhancement).
5. Add audience Q and A mode with pre-mapped architecture answers (EPIC 9 enhancement).

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

Status: IN PROGRESS

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
- Tailwind and shadcn/ui integration are still pending.

---

# EPIC 2 — Synthetic Enterprise Data Engine

## Goal

Build a realistic operational enterprise dataset.

---

## Tasks

### Task 2.1 — Customer Generator

Status: IN PROGRESS

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

---

### Task 2.2 — Stakeholder Generator

Generate:

- executives
- engineers
- support contacts
- preferences
- sentiment

Acceptance Criteria:

- customer-linked stakeholders exist
- realistic communication patterns

---

### Task 2.3 — Support Ticket Generator

Generate:

- tickets
- escalations
- summaries
- severity
- timelines

Acceptance Criteria:

- recurring incident patterns exist
- ticket relationships exist

---

### Task 2.4 — Incident Generator

Status: IN PROGRESS

Generate:

- outages
- service degradation
- deployment failures
- timelines

Acceptance Criteria:

- incidents evolve over time
- incidents affect customers

Progress Notes:

- Incident generator now emits status progression timelines (investigating -> mitigated -> monitoring/resolved).
- High-volatility scenarios now include recurring investigation transitions via recurrence_count.

---

### Task 2.5 — Usage Generator

Generate:

- product usage
- declining trends
- adoption metrics
- anomalies

Acceptance Criteria:

- risk scenarios emerge naturally

---

### Task 2.6 — Memory Generator

Generate:

- previous escalations
- promises
- frustrations
- preferences

Acceptance Criteria:

- memory continuity scenarios exist

---

### Task 2.7 — Event Stream Generator

Status: IN PROGRESS

Generate:

- support events
- incident updates
- customer messages
- deployment events

Acceptance Criteria:

- replayable streams exist

Progress Notes:

- Dataset generator now emits replayable operational event stream entries under event_stream.
- Event stream entries are generated from ticket and incident timeline transitions for deterministic replay flows.
- Backend replay APIs now discover and execute server-owned templates aligned with replayable stream semantics.

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

Implement:

- naive memory
- chat history injection
- local session state

Acceptance Criteria:

- memory works only within session

---

### Task 3.3 — Baseline Retrieval Layer

Implement:

- local JSON retrieval
- simple keyword retrieval
- fake vector retrieval

Acceptance Criteria:

- baseline works but is inefficient

---

### Task 3.4 — Metrics Instrumentation

Capture:

- latency
- tokens
- tool calls
- retrieval counts

Acceptance Criteria:

- metrics visible in UI

---

# EPIC 4 — Redis IRIS Integration

## Goal

Introduce Redis IRIS capabilities incrementally.

---

## Tasks

### Task 4.1 — RedisJSON Operational State

Status: IN PROGRESS

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

Status: IN PROGRESS

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

---

### Task 4.5 — Shared Operational Context

Status: IN PROGRESS

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

---

### Task 4.6 — Redis Streams

Status: IN PROGRESS

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

---

### Task 4.7 — Semantic Cache

Status: IN PROGRESS

Implement:

- repeated summary caching
- embedding similarity cache

Acceptance Criteria:

- repeated queries faster
- token reduction visible

Progress Notes:

- Added LangCache-style response cache in backend/app/redis_iris_tools.py with TTL-based storage.
- Wired IRIS workflow in backend/app/workflows.py to return cache hits early and write back cache entries on completion.

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

Status: IN PROGRESS

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

---

### Task 5.4 — Before vs After Toggle

Implement:

- baseline mode
- IRIS mode

Acceptance Criteria:

- same workflow runs in both modes
- differences measurable

---

### Task 5.5 — Replay Events UI

Status: IN PROGRESS

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

---

# EPIC 6 — Benchmarking and Proof

## Goal

Prove Redis IRIS improvements quantitatively.

---

## Tasks

### Task 6.1 — Benchmark Harness

Status: IN PROGRESS

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

---

### Task 6.2 — Token Measurement

Measure:

- prompt tokens
- completion tokens
- total tokens

Acceptance Criteria:

- token reduction measurable

---

### Task 6.3 — Latency Measurement

Measure:

- p50
- p95
- retrieval latency
- LLM latency

Acceptance Criteria:

- latency reductions visible

---

### Task 6.4 — Cache Effectiveness

Measure:

- cache hit rate
- repeated query savings

Acceptance Criteria:

- semantic cache value visible

---

### Task 6.5 — Multi-Agent Coordination Metrics

Measure:

- duplicate retrievals
- shared memory hits
- tool call reductions

Acceptance Criteria:

- coordination improvements visible

---

# EPIC 7 — Azure Readiness

## Goal

Prepare architecture for Azure Managed Redis and MAF.

---

## Tasks

### Task 7.1 — Redis Abstraction Layer

Implement:

- centralized Redis client
- env-based config
- TLS support

Acceptance Criteria:

- local and Azure Redis compatible

---

### Task 7.2 — Kubernetes Readiness

Implement:

- stateless backend
- Redis-backed state
- scaling tests

Acceptance Criteria:

- multiple replicas work

---

### Task 7.3 — Azure Compatibility Validation

Validate:

- Search
- JSON
- vectors
- Streams
- TLS

Acceptance Criteria:

- architecture deployable to AMR

---

# EPIC 8 — Microsoft Agent Framework Portability

## Goal

Prepare future MAF migration.

---

## Tasks

### Task 8.1 — Framework-Agnostic Context Layer

Ensure:

- Redis layer independent of LangGraph
- orchestration separated cleanly

Acceptance Criteria:

- Redis APIs reusable in MAF

---

### Task 8.2 — Shared State Contracts

Define:

- memory schema
- event schema
- retrieval APIs

Acceptance Criteria:

- contracts framework-agnostic

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

