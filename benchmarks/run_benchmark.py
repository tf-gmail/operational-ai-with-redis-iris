from __future__ import annotations

import argparse
import json
import math
import time
import urllib.request
from pathlib import Path
from statistics import mean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run baseline vs IRIS endpoint benchmark")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--output", default="benchmarks/reports/latest.json")
    return parser.parse_args()


def call_json(url: str, payload: dict[str, object]) -> tuple[float, dict[str, object]]:
    encoded = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, data=encoded, method="POST")
    req.add_header("Content-Type", "application/json")

    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=20) as response:
        body = response.read().decode("utf-8")
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    return elapsed_ms, json.loads(body)


def p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return ordered[index]


def run() -> int:
    args = parse_args()
    payload = {
        "customer": "Acme Corp",
        "message": "Our production system is down again and we are considering canceling our renewal.",
    }

    baseline_latencies: list[float] = []
    iris_latencies: list[float] = []
    baseline_tokens: list[float] = []
    iris_tokens: list[float] = []

    for _ in range(args.iterations):
        baseline_ms, baseline_result = call_json(f"{args.base_url}/api/run/baseline", payload)
        iris_ms, iris_result = call_json(f"{args.base_url}/api/run/iris", payload)

        baseline_latencies.append(baseline_ms)
        iris_latencies.append(iris_ms)

        baseline_metrics = baseline_result.get("metrics", {})
        iris_metrics = iris_result.get("metrics", {})

        baseline_tokens.append(float(baseline_metrics.get("prompt_tokens", 0)))
        iris_tokens.append(float(iris_metrics.get("prompt_tokens", 0)))

    result = {
        "iterations": args.iterations,
        "base_url": args.base_url,
        "baseline": {
            "latency_ms_avg": round(mean(baseline_latencies), 2),
            "latency_ms_p95": round(p95(baseline_latencies), 2),
            "prompt_tokens_avg": round(mean(baseline_tokens), 2),
        },
        "iris": {
            "latency_ms_avg": round(mean(iris_latencies), 2),
            "latency_ms_p95": round(p95(iris_latencies), 2),
            "prompt_tokens_avg": round(mean(iris_tokens), 2),
        },
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("Benchmark complete")
    print(json.dumps(result, indent=2))
    print(f"Saved: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
