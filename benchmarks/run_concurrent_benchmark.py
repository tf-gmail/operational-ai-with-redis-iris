from __future__ import annotations

import argparse
import json
import math
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from statistics import mean
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run concurrent baseline vs IRIS benchmark")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--output", default="benchmarks/reports/concurrent-latest.json")
    return parser.parse_args()


def p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return ordered[index]


def call_json(url: str, payload: dict[str, object]) -> tuple[float, dict[str, Any]]:
    encoded = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url=url, data=encoded, method="POST")
    request.add_header("Content-Type", "application/json")

    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8")
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    return elapsed_ms, json.loads(body)


def run_mode_batch(base_url: str, mode: str, workers: int, payload: dict[str, object]) -> dict[str, Any]:
    endpoint = f"{base_url}/api/run/{mode}"

    latencies: list[float] = []
    prompt_tokens: list[float] = []
    errors = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(call_json, endpoint, payload) for _ in range(workers)]
        for future in as_completed(futures):
            try:
                elapsed_ms, result = future.result()
                latencies.append(elapsed_ms)
                metrics = result.get("metrics", {})
                prompt_tokens.append(float(metrics.get("prompt_tokens", 0)))
            except Exception:
                errors += 1

    return {
        "requests": workers,
        "errors": errors,
        "latencies": latencies,
        "prompt_tokens": prompt_tokens,
    }


def run() -> int:
    args = parse_args()
    if args.workers < 1:
        raise ValueError("workers must be >= 1")
    if args.rounds < 1:
        raise ValueError("rounds must be >= 1")

    payload = {
        "customer": "Acme Corp",
        "message": "Our production system is down again and we are considering canceling our renewal.",
    }

    baseline_latencies: list[float] = []
    iris_latencies: list[float] = []
    baseline_tokens: list[float] = []
    iris_tokens: list[float] = []
    baseline_errors = 0
    iris_errors = 0

    for _ in range(args.rounds):
        baseline_round = run_mode_batch(args.base_url, "baseline", args.workers, payload)
        iris_round = run_mode_batch(args.base_url, "iris", args.workers, payload)

        baseline_latencies.extend(baseline_round["latencies"])
        iris_latencies.extend(iris_round["latencies"])
        baseline_tokens.extend(baseline_round["prompt_tokens"])
        iris_tokens.extend(iris_round["prompt_tokens"])
        baseline_errors += int(baseline_round["errors"])
        iris_errors += int(iris_round["errors"])

    result = {
        "base_url": args.base_url,
        "workers": args.workers,
        "rounds": args.rounds,
        "total_requests_per_mode": args.workers * args.rounds,
        "baseline": {
            "errors": baseline_errors,
            "latency_ms_avg": round(mean(baseline_latencies), 2) if baseline_latencies else 0.0,
            "latency_ms_p95": round(p95(baseline_latencies), 2),
            "prompt_tokens_avg": round(mean(baseline_tokens), 2) if baseline_tokens else 0.0,
        },
        "iris": {
            "errors": iris_errors,
            "latency_ms_avg": round(mean(iris_latencies), 2) if iris_latencies else 0.0,
            "latency_ms_p95": round(p95(iris_latencies), 2),
            "prompt_tokens_avg": round(mean(iris_tokens), 2) if iris_tokens else 0.0,
        },
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("Concurrent benchmark complete")
    print(json.dumps(result, indent=2))
    print(f"Saved: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
