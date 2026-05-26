import asyncio
import json
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from app.learning_mode_data import (
    get_learning_architecture_payload,
    get_learning_component_payload,
    get_learning_context_diff_payload,
    get_learning_context_packet_payload,
    get_learning_flow_payload,
    get_learning_fallback_scripts_payload,
    get_learning_maf_portability_payload,
    get_learning_metrics_education_payload,
    get_learning_metrics_storytelling_payload,
    get_learning_presenter_annotations_payload,
    get_learning_quiz_checkpoints_payload,
    get_learning_qa_anchors_payload,
    get_learning_qa_payload,
    get_learning_summary_handout_payload,
)
from app.redis_client import get_redis_connection_config
from app.redis_iris_tools import RDISyncLoop
from app.replay_templates import ReplayTemplate, get_replay_template, list_replay_templates
from app.runtime_state import get_runtime_state_store
from app.state_contracts import to_event_record_contract
from app.workflows import get_redis_tools
from app.workflows import run_baseline_workflow, run_iris_workflow


app = FastAPI(title="operational-ai-with-redis-iris", version="0.1.0")


def _default_trend_history_path() -> Path:
    return Path(__file__).resolve().parents[2] / "benchmarks" / "reports" / "trend-history.json"


def _load_trend_history(limit: int = 100) -> list[dict[str, Any]]:
    explicit = os.getenv("BENCHMARK_TREND_HISTORY_PATH")
    history_path = Path(explicit) if explicit else _default_trend_history_path()
    if not history_path.exists():
        return []

    try:
        payload = json.loads(history_path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            return []
        return payload[-limit:]
    except Exception:
        return []


class RunRequest(BaseModel):
    customer: str = Field(default="Acme Corp")
    message: str


class RunResult(BaseModel):
    mode: str
    summary: str
    metrics: dict[str, float | int]
    context_signals: list[str]


class EventPayload(BaseModel):
    event_type: str
    status: str
    customer: str = Field(default="Acme Corp")
    message: str | None = None


class ReplayExecuteRequest(BaseModel):
    template_id: str
    mode: Literal["full", "step"] = "full"
    step_index: int | None = None
    customer_override: str | None = None
    speed_multiplier: float = Field(default=1.0, gt=0.0, le=20.0)


class EventBus:
    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue[dict[str, Any]]] = set()
        self._history: list[dict[str, Any]] = []
        self._lock = asyncio.Lock()

    async def subscribe(self) -> asyncio.Queue[dict[str, Any]]:
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        async with self._lock:
            self._subscribers.add(queue)
        return queue

    async def unsubscribe(self, queue: asyncio.Queue[dict[str, Any]]) -> None:
        async with self._lock:
            self._subscribers.discard(queue)

    async def publish(self, event: dict[str, Any]) -> None:
        async with self._lock:
            self._history.append(event)
            self._history = self._history[-50:]
            subscribers = list(self._subscribers)

        for queue in subscribers:
            await queue.put(event)

    async def recent(self) -> list[dict[str, Any]]:
        async with self._lock:
            return list(self._history)


event_bus = EventBus()
rdi_sync_loop: RDISyncLoop | None = None


async def publish_operational_event(event: dict[str, Any]) -> dict[str, Any]:
    event = to_event_record_contract(event)
    tools = get_redis_tools()
    if tools is not None:
        try:
            stream_id = tools.append_operational_event(event)
            if stream_id:
                event["redis_stream_id"] = stream_id
        except Exception:
            pass
    await event_bus.publish(event)
    return event


async def get_recent_operational_events(limit: int = 50) -> list[dict[str, Any]]:
    local_events = await event_bus.recent()
    tools = get_redis_tools()
    if tools is None:
        return local_events[-limit:]

    try:
        stream_events = tools.get_recent_operational_events(customer=None, limit=limit)
    except Exception:
        return local_events[-limit:]

    merged: dict[str, dict[str, Any]] = {}
    for event in local_events + stream_events:
        if not isinstance(event, dict):
            continue
        event = to_event_record_contract(event)
        event_id = str(event.get("redis_stream_id") or event.get("event_id") or "")
        key = event_id or f"{event.get('event_type', '')}:{event.get('status', '')}:{event.get('timestamp', '')}"
        merged[key] = event

    return sorted(merged.values(), key=lambda row: str(row.get("timestamp", "")), reverse=True)[:limit]


def _build_event(
    event_type: str,
    status: str,
    customer: str,
    message: str | None,
    source: str,
    replay_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event: dict[str, Any] = {
        "event_id": f"evt-{datetime.now(timezone.utc).timestamp()}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "status": status,
        "customer": customer,
        "message": message,
        "source": source,
    }
    if replay_metadata:
        event["replay"] = replay_metadata
    return to_event_record_contract(event)


class ReplayManager:
    def __init__(self) -> None:
        self._runs: dict[str, dict[str, Any]] = {}
        self._tasks: dict[str, asyncio.Task[None]] = {}
        self._lock = asyncio.Lock()
        self._state_store = get_runtime_state_store()

    def _persist_run_state(self, run_state: dict[str, Any]) -> None:
        if self._state_store is None:
            return
        self._state_store.save_replay_run(run_state)

    def _load_shared_run_state(self, run_id: str) -> dict[str, Any] | None:
        if self._state_store is None:
            return None
        return self._state_store.load_replay_run(run_id)

    def _mark_cancellation_requested(self, run_state: dict[str, Any]) -> dict[str, Any]:
        if run_state.get("status") == "running":
            run_state["status"] = "cancellation_requested"
        self._persist_run_state(run_state)
        return run_state

    def _is_cancellation_requested(self, run_id: str) -> bool:
        shared = self._load_shared_run_state(run_id)
        if not shared:
            return False
        return str(shared.get("status", "")) == "cancellation_requested"

    async def execute(self, payload: ReplayExecuteRequest) -> dict[str, Any]:
        template = get_replay_template(payload.template_id)
        if template is None:
            return {
                "status": "not_found",
                "details": f"Unknown replay template: {payload.template_id}",
            }

        if payload.mode == "step":
            if payload.step_index is None:
                return {
                    "status": "invalid",
                    "details": "step_index is required when mode=step",
                }
            return await self._execute_single_step(template, payload)

        return await self._execute_full_run(template, payload)

    async def _execute_single_step(
        self,
        template: ReplayTemplate,
        payload: ReplayExecuteRequest,
    ) -> dict[str, Any]:
        step_index = int(payload.step_index or 0)
        if step_index < 0 or step_index >= len(template.steps):
            return {
                "status": "invalid",
                "details": f"step_index out of range: {step_index}",
            }

        step = template.steps[step_index]
        run_id = f"replay-step-{uuid4().hex[:10]}"
        customer = payload.customer_override or template.customer

        event = _build_event(
            event_type=step.event_type,
            status=step.status,
            customer=customer,
            message=step.message,
            source="replay-step",
            replay_metadata={
                "run_id": run_id,
                "template_id": template.id,
                "template_name": template.name,
                "step_index": step_index,
                "step_label": step.label,
                "total_steps": len(template.steps),
            },
        )
        await publish_operational_event(event)

        return {
            "status": "ok",
            "mode": "step",
            "run_id": run_id,
            "template_id": template.id,
            "published_event": event,
        }

    async def _execute_full_run(
        self,
        template: ReplayTemplate,
        payload: ReplayExecuteRequest,
    ) -> dict[str, Any]:
        run_id = f"replay-{uuid4().hex[:12]}"
        customer = payload.customer_override or template.customer
        run_state = {
            "run_id": run_id,
            "template_id": template.id,
            "template_name": template.name,
            "status": "running",
            "customer": customer,
            "executor": os.getenv("HOSTNAME", "local"),
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
            "step_count": len(template.steps),
            "last_step_index": -1,
            "published_events": [],
        }

        async with self._lock:
            self._runs[run_id] = run_state
        self._persist_run_state(run_state)

        task = asyncio.create_task(self._run_template(run_id, template, customer, payload.speed_multiplier))
        async with self._lock:
            self._tasks[run_id] = task

        return {
            "status": "accepted",
            "mode": "full",
            "run": run_state,
        }

    async def _run_template(
        self,
        run_id: str,
        template: ReplayTemplate,
        customer: str,
        speed_multiplier: float,
    ) -> None:
        try:
            for step_index, step in enumerate(template.steps):
                if self._is_cancellation_requested(run_id):
                    raise asyncio.CancelledError()

                delay_seconds = (step.delay_ms / 1000.0) / speed_multiplier
                await asyncio.sleep(delay_seconds)

                if self._is_cancellation_requested(run_id):
                    raise asyncio.CancelledError()

                event = _build_event(
                    event_type=step.event_type,
                    status=step.status,
                    customer=customer,
                    message=step.message,
                    source="replay-template",
                    replay_metadata={
                        "run_id": run_id,
                        "template_id": template.id,
                        "template_name": template.name,
                        "step_index": step_index,
                        "step_label": step.label,
                        "total_steps": len(template.steps),
                    },
                )
                await publish_operational_event(event)

                async with self._lock:
                    run_state = self._runs.get(run_id)
                    if run_state is None:
                        return
                    run_state["last_step_index"] = step_index
                    run_state["published_events"].append(event)
                    self._persist_run_state(run_state)

            async with self._lock:
                run_state = self._runs.get(run_id)
                if run_state is not None:
                    run_state["status"] = "completed"
                    run_state["completed_at"] = datetime.now(timezone.utc).isoformat()
                    self._persist_run_state(run_state)
        except asyncio.CancelledError:
            async with self._lock:
                run_state = self._runs.get(run_id)
                if run_state is not None:
                    run_state["status"] = "cancelled"
                    run_state["completed_at"] = datetime.now(timezone.utc).isoformat()
                    self._persist_run_state(run_state)
            raise
        except Exception:
            async with self._lock:
                run_state = self._runs.get(run_id)
                if run_state is not None:
                    run_state["status"] = "error"
                    run_state["completed_at"] = datetime.now(timezone.utc).isoformat()
                    self._persist_run_state(run_state)
        finally:
            async with self._lock:
                self._tasks.pop(run_id, None)

    async def get_run(self, run_id: str) -> dict[str, Any] | None:
        async with self._lock:
            run = self._runs.get(run_id)
            if run is None:
                shared = self._load_shared_run_state(run_id)
                if shared is None:
                    return None
                return dict(shared)
            return dict(run)

    async def cancel_run(self, run_id: str) -> dict[str, Any]:
        async with self._lock:
            task = self._tasks.get(run_id)
            if task is None:
                run = self._runs.get(run_id)
                if run is None:
                    shared = self._load_shared_run_state(run_id)
                    if shared is None:
                        return {"status": "not_found", "details": f"Unknown run_id: {run_id}"}
                    shared = self._mark_cancellation_requested(shared)
                    return {"status": "accepted", "details": f"Cancellation requested for {run_id}", "run": shared}
                run = self._mark_cancellation_requested(run)
                return {"status": "accepted", "details": f"Cancellation requested for {run_id}", "run": run}

            run = self._runs.get(run_id)
            if run is not None:
                self._mark_cancellation_requested(run)
            task.cancel()
        return {"status": "accepted", "details": f"Cancellation requested for {run_id}"}


replay_manager = ReplayManager()


@app.on_event("startup")
async def startup() -> None:
    global rdi_sync_loop
    tools = get_redis_tools()
    if tools is None:
        return

    rdi_sync_loop = RDISyncLoop(tools)
    await rdi_sync_loop.start()


@app.on_event("shutdown")
async def shutdown() -> None:
    global rdi_sync_loop
    if rdi_sync_loop is None:
        return
    await rdi_sync_loop.stop()
    rdi_sync_loop = None


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "backend",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/modes")
def modes() -> dict[str, list[str]]:
    return {"modes": ["baseline", "iris"]}


@app.get("/api/config")
def config() -> dict[str, str]:
    redis_tools = get_redis_tools()
    redis_config = get_redis_connection_config()
    return {
        **redis_config.public_config(),
        "redis_tools_enabled": "true" if redis_tools is not None else "false",
    }


@app.get("/api/rdi/status")
def rdi_status() -> dict[str, Any]:
    tools = get_redis_tools()
    if tools is None:
        return {
            "status": "unavailable",
            "details": "Redis is not reachable; RDI sync loop is disabled.",
        }
    return {
        "status": "ok",
        "details": tools.rdi_status(),
    }


@app.post("/api/rdi/sync-now")
def rdi_sync_now() -> dict[str, Any]:
    tools = get_redis_tools()
    if tools is None:
        return {
            "status": "unavailable",
            "details": "Redis is not reachable; sync did not run.",
        }
    return {
        "status": "ok",
        "details": tools.sync_once(),
    }


@app.post("/api/run/baseline", response_model=RunResult)
def run_baseline(payload: RunRequest) -> RunResult:
    result = run_baseline_workflow(payload.customer, payload.message)
    return RunResult(
        mode="baseline",
        summary=result["summary"],
        metrics=result["metrics"],
        context_signals=result["context_signals"],
    )


@app.post("/api/run/iris", response_model=RunResult)
async def run_iris(payload: RunRequest) -> RunResult:
    recent = await get_recent_operational_events(limit=50)
    result = run_iris_workflow(payload.customer, payload.message, recent_events=recent)
    return RunResult(
        mode="iris",
        summary=result["summary"],
        metrics=result["metrics"],
        context_signals=result["context_signals"],
    )


@app.get("/api/events/recent")
async def recent_events() -> dict[str, list[dict[str, Any]]]:
    return {"events": await get_recent_operational_events(limit=50)}


@app.post("/api/events/inject")
async def inject_event(payload: EventPayload) -> dict[str, Any]:
    event = _build_event(
        event_type=payload.event_type,
        status=payload.status,
        customer=payload.customer,
        message=payload.message,
        source="manual-injection",
    )
    await publish_operational_event(event)
    return {"status": "accepted", "event": event}


@app.get("/api/replay/templates")
def replay_templates() -> dict[str, list[dict[str, Any]]]:
    return {"templates": list_replay_templates()}


@app.post("/api/replay/execute")
async def replay_execute(payload: ReplayExecuteRequest) -> dict[str, Any]:
    return await replay_manager.execute(payload)


@app.get("/api/replay/runs/{run_id}")
async def replay_run_status(run_id: str) -> dict[str, Any]:
    run = await replay_manager.get_run(run_id)
    if run is None:
        return {"status": "not_found", "details": f"Unknown run_id: {run_id}"}
    return {"status": "ok", "run": run}


@app.post("/api/replay/runs/{run_id}/cancel")
async def replay_cancel(run_id: str) -> dict[str, Any]:
    return await replay_manager.cancel_run(run_id)


@app.get("/api/benchmarks/trends")
def benchmark_trends(limit: int = 100) -> dict[str, Any]:
    clamped_limit = max(1, min(limit, 500))
    entries = _load_trend_history(limit=clamped_limit)
    return {
        "status": "ok",
        "entries": entries,
        "count": len(entries),
    }


@app.get("/api/learning/architecture")
def learning_architecture() -> dict[str, Any]:
    return get_learning_architecture_payload()


@app.get("/api/learning/flow/{mode}")
def learning_flow(mode: str) -> dict[str, Any]:
    return get_learning_flow_payload(mode)


@app.get("/api/learning/component/{component_id}")
def learning_component(component_id: str) -> dict[str, Any]:
    return get_learning_component_payload(component_id)


@app.get("/api/learning/context-packet")
def learning_context_packet() -> dict[str, Any]:
    return get_learning_context_packet_payload()


@app.get("/api/learning/context-diff")
def learning_context_diff() -> dict[str, Any]:
    return get_learning_context_diff_payload()


@app.get("/api/learning/metrics-education")
def learning_metrics_education() -> dict[str, Any]:
    return get_learning_metrics_education_payload()


@app.get("/api/learning/metrics-storytelling")
def learning_metrics_storytelling() -> dict[str, Any]:
    return get_learning_metrics_storytelling_payload()


@app.get("/api/learning/audience-qa")
def learning_audience_qa() -> dict[str, Any]:
    return get_learning_qa_payload()


@app.get("/api/learning/summary-handout")
def learning_summary_handout() -> dict[str, Any]:
    return get_learning_summary_handout_payload()


@app.get("/api/learning/presenter-annotations")
def learning_presenter_annotations() -> dict[str, Any]:
    return get_learning_presenter_annotations_payload()


@app.get("/api/learning/fallback-scripts")
def learning_fallback_scripts() -> dict[str, Any]:
    return get_learning_fallback_scripts_payload()


@app.get("/api/learning/quiz-checkpoints")
def learning_quiz_checkpoints() -> dict[str, Any]:
    return get_learning_quiz_checkpoints_payload()


@app.get("/api/learning/qa-anchors")
def learning_qa_anchors() -> dict[str, Any]:
    return get_learning_qa_anchors_payload()


@app.get("/api/learning/maf-portability")
def learning_maf_portability() -> dict[str, Any]:
    return get_learning_maf_portability_payload()


@app.websocket("/ws/events")
async def events_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    queue = await event_bus.subscribe()

    try:
        await websocket.send_json(
            {
                "event_type": "connection",
                "status": "connected",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=10)
                await websocket.send_json(event)
            except asyncio.TimeoutError:
                await websocket.send_json(
                    {
                        "event_type": "heartbeat",
                        "status": "ok",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
    except WebSocketDisconnect:
        pass
    finally:
        await event_bus.unsubscribe(queue)
