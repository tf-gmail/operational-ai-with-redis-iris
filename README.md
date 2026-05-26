# operational-ai-with-redis-iris

Production-style multi-agent customer operations demo using LangGraph + Redis IRIS patterns.

## Current Status

This repository is in active build-out. The first milestone focuses on:

- Foundation scaffolding
- Docker Compose service skeleton
- Minimal frontend/backend services
- Redis Stack availability for JSON, Search, Vector, and Streams

## Quick Start

1. Copy env template:

   cp .env.example .env

2. Start services:

   ./scripts/dev-up.sh

3. Stop services:

   ./scripts/dev-down.sh

If your machine supports only legacy Compose, the scripts automatically use `docker-compose`.

4. Open apps:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs
- Redis Insight (if enabled by image): http://localhost:8001

## Redis Capability Verification

After Redis is running, verify required features:

python backend/scripts/verify_redis_stack.py --host localhost --port 6379

If your local Python is externally managed (PEP 668), run verification inside the backend container instead:

docker-compose exec -T backend python scripts/verify_redis_stack.py --host redis --port 6379

If Docker commands fail, make sure the Docker daemon (or Colima runtime) is started.

For Azure Managed Redis TLS validation, you can use a secure URL directly:

python backend/scripts/verify_redis_stack.py --url rediss://<host>:6380 --username <username> --password <password>

Optional TLS env vars supported by backend and verification script:

- REDIS_URL (preferred for hosted Redis)
- REDIS_HOST / REDIS_PORT / REDIS_DB
- REDIS_USERNAME / REDIS_PASSWORD
- REDIS_TLS / REDIS_TLS_INSECURE
- REDIS_TLS_CA_CERT / REDIS_TLS_CLIENT_CERT / REDIS_TLS_CLIENT_KEY

Runtime state TTL env vars for stateless backend scaling:

- BASELINE_STATE_TTL_SECONDS (default: 86400)
- REPLAY_STATE_TTL_SECONDS (default: 14400)

## Kubernetes Readiness Check

Run a shared-state readiness check against a running backend:

python3 backend/scripts/check_scaling_readiness.py --base-url http://localhost:8000

Optional local multi-replica smoke test:

docker compose up -d --scale backend=2
python3 backend/scripts/check_scaling_readiness.py --base-url http://localhost:8000

## Azure Compatibility Validation (EPIC 7 Task 7.3)

Validate Redis module coverage and backend runtime compatibility for Azure Managed Redis:

python3 backend/scripts/validate_azure_compatibility.py --base-url http://localhost:8000 --url rediss://<host>:6380 --username <username> --password <password>

Local non-TLS smoke mode (for local Redis Stack only):

python3 backend/scripts/validate_azure_compatibility.py --base-url http://localhost:8000 --host localhost --port 6379 --allow-non-tls

## Benchmark Harness (v1)

Run baseline vs IRIS endpoint benchmark and save report:

python3 benchmarks/run_benchmark.py --base-url http://localhost:8000 --iterations 5 --output benchmarks/reports/latest.json

## Synthetic Customer Dataset Generator

Generate deterministic multi-entity fixture data (customers, stakeholders, tickets, incidents):

python3 data/generate_customers.py --count 1000 --output data/customers_seed.json

## Redis IRIS Tooling (RDI + Context Retriever + Agent Memory + LangCache)

The backend now wires all four Redis IRIS tools in the IRIS run path:

- RDI-style continuous sync loop: periodically ingests synthetic dataset into RedisJSON keys.
- Redis Context Retriever: resolves customer, incident, and ticket context from shared state using FT.SEARCH indexes.
- Redis Agent Memory: reads and writes per-customer memory across requests.
- Redis LangCache: caches repeated query responses with TTL.

IRIS also includes a vector-based similar-incident retrieval path built on Redis vector search indexes
using deterministic local pseudo-embeddings for incident summaries.

Framework-agnostic context layer boundary:

- backend/app/context_layer.py contains Redis-backed context packet assembly and Redis post-processing helpers.
- Orchestration code in backend/app/workflows.py consumes context packets and remains decoupled from Redis retrieval internals.
- This separation is designed for EPIC 8 MAF portability so the same Redis context layer can be reused outside LangGraph.

Shared state contract boundary:

- backend/app/state_contracts.py defines framework-agnostic contracts for memory records, event records, and retrieval request/response payloads.
- Event publish/read paths in backend/app/main.py normalize runtime events through the shared event contract.
- Context retrieval in backend/app/context_layer.py emits a retrieval API contract summary for orchestration-independent consumers.

RDI control endpoints:

- GET http://localhost:8000/api/rdi/status
- POST http://localhost:8000/api/rdi/sync-now

Recommended local loop for continuously refreshed operational data:

1. Regenerate dataset:

python3 data/generate_customers.py --count 1000 --output data/customers_seed.json

2. Trigger immediate sync:

curl -X POST http://localhost:8000/api/rdi/sync-now

3. Run IRIS query and inspect context signals for Redis tool usage:

curl -sS -X POST http://localhost:8000/api/run/iris -H 'Content-Type: application/json' -d '{"customer":"Acme Corp","message":"Please summarize current incident and next actions"}'

Look for vector retrieval signal when similar incidents are found:

- redis-vector-similar-incidents

## CI Benchmark Reports

Quick smoke benchmark output:

python3 benchmarks/run_benchmark.py --base-url http://localhost:8000 --iterations 3 --output benchmarks/reports/ci-latest.json

Extended benchmark output:

python3 benchmarks/run_benchmark.py --base-url http://localhost:8000 --iterations 20 --output benchmarks/reports/ci-extended.json

Concurrent-session benchmark output:

python3 benchmarks/run_concurrent_benchmark.py --base-url http://localhost:8000 --workers 8 --rounds 5 --output benchmarks/reports/concurrent-latest.json

Trend snapshot append (history file):

python3 benchmarks/update_trend_snapshot.py --reports benchmarks/reports/latest.json benchmarks/reports/ci-latest.json benchmarks/reports/ci-extended.json --source local

Trend history API for frontend visualization:

GET http://localhost:8000/api/benchmarks/trends

Regression gate check against baseline snapshot:

python3 benchmarks/check_regression.py --current benchmarks/reports/ci-latest.json --baseline benchmarks/reports/regression-baseline.json

Regression gate profile selection (strict, normal, lenient):

python3 benchmarks/check_regression.py --profile strict --current benchmarks/reports/ci-latest.json --baseline benchmarks/reports/regression-baseline.json

Optional per-metric overrides (override profile defaults):

python3 benchmarks/check_regression.py --profile normal --max-latency-regression-pct 20 --max-p95-regression-pct 20 --max-token-regression-pct 8 --current benchmarks/reports/ci-latest.json --baseline benchmarks/reports/regression-baseline.json

## Replay Controls

The Live Events card now includes replay controls with multiple event templates and timeline playback.

Use Play, Pause, Next Step, and Reset to inject timeline events into the existing WS stream.

Backend replay API (server-driven timeline execution + template discovery):

- GET http://localhost:8000/api/replay/templates
- POST http://localhost:8000/api/replay/execute
- GET http://localhost:8000/api/replay/runs/{run_id}
- POST http://localhost:8000/api/replay/runs/{run_id}/cancel

Frontend replay controls are now wired to backend template discovery and execute APIs:

- template list source: GET /api/replay/templates
- next-step replay action: POST /api/replay/execute (mode=step)
- play replay action: POST /api/replay/execute (mode=full)
- active run status polling: GET /api/replay/runs/{run_id}
- active run cancel action: POST /api/replay/runs/{run_id}/cancel

Replay and manual-injection events are also appended to Redis Streams via events:operational.

## Learning Mode APIs

Learning Mode backend payloads now expose architecture and explanatory flow data for the upcoming diagram UI:

- GET http://localhost:8000/api/learning/architecture
- GET http://localhost:8000/api/learning/flow/baseline
- GET http://localhost:8000/api/learning/flow/iris
- GET http://localhost:8000/api/learning/component/{component_id}
- GET http://localhost:8000/api/learning/context-packet
- GET http://localhost:8000/api/learning/context-diff
- GET http://localhost:8000/api/learning/metrics-education
- GET http://localhost:8000/api/learning/metrics-storytelling
- GET http://localhost:8000/api/learning/maf-portability
- GET http://localhost:8000/api/learning/audience-qa
- GET http://localhost:8000/api/learning/summary-handout
- GET http://localhost:8000/api/learning/presenter-annotations
- GET http://localhost:8000/api/learning/fallback-scripts
- GET http://localhost:8000/api/learning/quiz-checkpoints
- GET http://localhost:8000/api/learning/qa-anchors

## Repository Structure

- frontend: Next.js UI shell
- backend: FastAPI API shell
- graph: LangGraph orchestration code
- iris: Redis IRIS context layer
- baseline: Baseline non-Redis implementation
- data: Synthetic data generators and fixtures
- benchmarks: Measurement harness and reports
- docs: Planning and architecture documentation
