# EPIC 8 Task 8.3 - LangGraph to MAF Migration Guide

## Purpose

This document defines a clear migration path from the current LangGraph-based orchestration to Microsoft Agent Framework (MAF) while preserving Redis IRIS capabilities and shared-state contracts.

## Current Architecture Boundary

The codebase already isolates reusable runtime layers:

- Orchestration layer:
  - LangGraph execution entry points in backend/app/workflows.py
- Framework-agnostic context layer:
  - Redis-backed context packet assembly in backend/app/context_layer.py
- Shared state contracts:
  - Memory, event, and retrieval payload contracts in backend/app/state_contracts.py
- Redis IRIS runtime tools:
  - Retrieval, memory, streams, cache, and sync in backend/app/redis_iris_tools.py

These boundaries allow orchestration replacement without Redis-layer rewrites.

## LangGraph to MAF Mapping

| Current LangGraph Component | Current Location | MAF Equivalent Pattern | Migration Note |
| --- | --- | --- | --- |
| Graph entry execution (baseline/iris) | backend/app/workflows.py | Agent orchestration entry handler | Keep API endpoints stable and swap orchestration implementation behind handler boundary. |
| Baseline graph pipeline | backend/app/langgraph_pipeline.py | MAF baseline workflow/toolchain | Preserve baseline behavior as control path for benchmark continuity. |
| IRIS graph pipeline | backend/app/langgraph_pipeline.py | MAF IRIS workflow/toolchain | Keep context packet and signal semantics unchanged to protect observability. |
| Context packet assembly | backend/app/context_layer.py | Shared context preprocessor service/module | Reuse as-is; do not embed framework-specific objects in context packet schema. |
| Retrieval/memory/cache tools | backend/app/redis_iris_tools.py | Shared tool adapters invoked by MAF orchestration | Reuse the same Redis API surface and key schema. |
| Event publish/read normalization | backend/app/main.py + backend/app/state_contracts.py | Event contract adapter in MAF runtime I/O boundary | Keep event contract stable to avoid frontend and replay regressions. |
| Shared runtime state store | backend/app/runtime_state.py | Shared state adapter used by MAF run manager | Reuse keys and TTL behavior to maintain multi-replica continuity. |

## Redis Reuse Strategy

### Reuse without rewrites

Keep these modules framework-neutral and unchanged during orchestration migration:

- backend/app/redis_iris_tools.py
- backend/app/context_layer.py
- backend/app/state_contracts.py
- backend/app/runtime_state.py

### Contract-first integration

MAF orchestration should consume and emit existing contracts:

- Retrieval contracts from state_contracts.py
- Event contracts from state_contracts.py
- Context packets from context_layer.py

### Compatibility guarantees

Preserve the following for benchmark, UI, and replay stability:

- Existing context_signals naming conventions
- Existing /api/run/baseline and /api/run/iris response shape
- Existing replay event schema and timeline metadata
- Existing Redis key patterns and TTL defaults

## Phased Migration Sequence

1. Phase 0 - Baseline freeze
- Lock current API payload contracts and runtime signal names.
- Capture benchmark snapshots before orchestration migration.

2. Phase 1 - Dual orchestration adapter
- Introduce a runtime switch for LangGraph vs MAF orchestration behind workflows.py.
- Keep context_layer and redis_iris_tools as common dependencies.

3. Phase 2 - Parity validation
- Run baseline and IRIS parity checks on summaries, signals, and metrics shape.
- Execute replay and scaling-readiness scripts against both orchestration modes.

4. Phase 3 - Cutover
- Set MAF orchestration as default runtime path.
- Keep fallback switch to LangGraph during rollout window.

5. Phase 4 - Stabilization
- Monitor benchmark regressions and shared-state continuity.
- Remove temporary dual-mode toggles only after parity confidence is established.

## Readiness Gates

Migration can proceed only when all gates pass:

- Contract gate: no breaking changes in state_contracts.py payloads.
- Runtime gate: context signals and metrics fields remain compatibility-safe.
- Replay gate: replay execution/status/cancel behavior remains consistent.
- Scale gate: shared-state continuity passes cross-replica checks.
- Azure gate: Redis Search/JSON/Vector/Streams/TLS validation remains green.

## Rollback Strategy

If parity fails during cutover:

- Re-enable LangGraph orchestration via runtime switch.
- Keep Redis context/state layers unchanged.
- Compare contract-level diffs for failing payloads.
- Re-run parity suite before next MAF promotion attempt.

## Validation Checklist

- Verify no contract regressions in backend/app/state_contracts.py.
- Verify context packet build path remains framework-agnostic.
- Verify replay and event schemas are unchanged for frontend consumers.
- Verify benchmark outputs preserve existing top-level fields.
- Verify Azure compatibility script remains green for deployment posture.
