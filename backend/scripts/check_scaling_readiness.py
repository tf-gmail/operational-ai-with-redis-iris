#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


def _request_json(base_url: str, path: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url=url, data=data, method=method, headers=headers)
    with urlopen(request, timeout=10) as response:
        body = response.read().decode("utf-8")
    return json.loads(body)


def _fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def _check_baseline_shared_state(base_url: str, customer: str) -> int:
    first = _request_json(
        base_url,
        "/api/run/baseline",
        method="POST",
        payload={
            "customer": customer,
            "message": "Initial continuity check for shared state.",
        },
    )
    second = _request_json(
        base_url,
        "/api/run/baseline",
        method="POST",
        payload={
            "customer": customer,
            "message": "Follow-up continuity check for shared state.",
        },
    )

    first_signals = set(first.get("context_signals", []))
    second_signals = set(second.get("context_signals", []))

    if "baseline-shared-state-write" not in first_signals and "baseline-shared-state-write" not in second_signals:
        return _fail("Shared baseline state write signal missing; Redis-backed baseline storage is not active.")

    if "session-local-memory-hit" not in second_signals:
        return _fail("Second baseline run did not report session memory hit; continuity failed.")

    print("PASS: Baseline continuity uses shared Redis-backed state.")
    return 0


def _check_replay_shared_state(base_url: str, timeout_seconds: int) -> int:
    run_start = _request_json(
        base_url,
        "/api/replay/execute",
        method="POST",
        payload={
            "template_id": "degradation-recovery",
            "mode": "full",
            "speed_multiplier": 20.0,
        },
    )

    run = run_start.get("run", {})
    run_id = str(run.get("run_id", ""))
    if not run_id:
        return _fail("Replay execution did not return a run_id.")

    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        status_payload = _request_json(base_url, f"/api/replay/runs/{run_id}")
        if status_payload.get("status") != "ok":
            return _fail(f"Replay run status endpoint returned: {status_payload}")

        run_state = status_payload.get("run", {})
        current = str(run_state.get("status", ""))
        if current in {"completed", "cancelled", "error"}:
            if "executor" not in run_state:
                return _fail("Replay run state missing executor marker for replica attribution.")
            print(f"PASS: Replay run state persisted with status '{current}'.")
            return 0

        time.sleep(0.5)

    return _fail(f"Replay run {run_id} did not complete within {timeout_seconds} seconds.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Kubernetes readiness signals for Redis-backed stateless backend.")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Backend API base URL.")
    parser.add_argument("--customer", default="Acme Corp", help="Customer key used for baseline continuity checks.")
    parser.add_argument("--timeout-seconds", type=int, default=30, help="Timeout for replay status completion.")
    args = parser.parse_args()

    try:
        config = _request_json(args.base_url, "/api/config")
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return _fail(f"Unable to reach backend config endpoint: {exc}")

    if str(config.get("redis_tools_enabled", "false")).lower() != "true":
        return _fail("Redis tools are disabled; shared-state scaling checks require Redis connectivity.")

    print("INFO: Redis tools are enabled; running shared-state checks.")

    try:
        baseline_status = _check_baseline_shared_state(args.base_url, args.customer)
        if baseline_status != 0:
            return baseline_status

        replay_status = _check_replay_shared_state(args.base_url, args.timeout_seconds)
        if replay_status != 0:
            return replay_status
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        return _fail(f"Request failed during readiness checks: {exc}")

    print("PASS: Kubernetes readiness checks succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
