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


def p50(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(0.50 * len(ordered)) - 1)
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


def _as_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def extract_token_triplet(metrics: dict[str, object]) -> tuple[float, float, float]:
    prompt_tokens = _as_float(metrics.get("prompt_tokens", metrics.get("prompt_tokens_observed", 0)))
    completion_tokens = _as_float(metrics.get("completion_tokens", metrics.get("completion_tokens_observed", 0)))
    total_tokens = _as_float(metrics.get("total_tokens", prompt_tokens + completion_tokens))
    return prompt_tokens, completion_tokens, total_tokens


def extract_latency_components(metrics: dict[str, object]) -> tuple[float, float, float]:
    runtime_latency = _as_float(metrics.get("runtime_latency_ms", 0))
    retrieval_latency = _as_float(metrics.get("retrieval_latency_ms_estimated", 0))
    llm_latency = _as_float(metrics.get("llm_latency_ms_estimated", 0))
    return runtime_latency, retrieval_latency, llm_latency


def avg_or_zero(values: list[float]) -> float:
    return round(mean(values), 2) if values else 0.0


def extract_context_signals(result: dict[str, object]) -> list[str]:
    raw = result.get("context_signals", [])
    if not isinstance(raw, list):
        return []
    return [str(signal) for signal in raw]


def extract_cache_hit_flags(signals: list[str]) -> tuple[bool, bool, bool]:
    is_exact = any(signal == "redis-langcache-exact-hit" for signal in signals)
    is_semantic = any(signal == "redis-langcache-semantic-hit" for signal in signals)
    is_hit = any(signal.startswith("redis-langcache-hit") for signal in signals) or is_exact or is_semantic
    return is_hit, is_exact, is_semantic


def extract_coordination_metrics(metrics: dict[str, object], signals: list[str]) -> tuple[float, float, float, bool]:
    retrieval_signals = _as_float(metrics.get("retrieval_signals", 0))
    tool_signals = _as_float(metrics.get("tool_signals", 0))
    duplicate_retrieval_signals = max(0.0, retrieval_signals - 1.0)
    shared_memory_hit = any(
        signal in {"redis-agent-memory-hit", "redis-shared-workflow-state-hit"}
        for signal in signals
    )
    return retrieval_signals, tool_signals, duplicate_retrieval_signals, shared_memory_hit


def reduction_pct(baseline_value: float, iris_value: float) -> float:
    if baseline_value <= 0:
        return 0.0
    return round(((baseline_value - iris_value) / baseline_value) * 100.0, 2)


def run_mode_batch(base_url: str, mode: str, workers: int, payload: dict[str, object]) -> dict[str, Any]:
    endpoint = f"{base_url}/api/run/{mode}"

    latencies: list[float] = []
    prompt_tokens: list[float] = []
    completion_tokens: list[float] = []
    total_tokens: list[float] = []
    runtime_latencies: list[float] = []
    retrieval_latencies: list[float] = []
    llm_latencies: list[float] = []
    cache_hits = 0
    cache_exact_hits = 0
    cache_semantic_hits = 0
    retrieval_signals: list[float] = []
    tool_signals: list[float] = []
    duplicate_retrieval_signals: list[float] = []
    shared_memory_hits = 0
    errors = 0

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(call_json, endpoint, payload) for _ in range(workers)]
        for future in as_completed(futures):
            try:
                elapsed_ms, result = future.result()
                latencies.append(elapsed_ms)
                metrics = result.get("metrics", {})
                prompt_token_value, completion_token_value, total_token_value = extract_token_triplet(metrics)
                runtime_latency, retrieval_latency, llm_latency = extract_latency_components(metrics)
                signals = extract_context_signals(result)
                is_hit, is_exact_hit, is_semantic_hit = extract_cache_hit_flags(signals)
                retrieval_signal_value, tool_signal_value, duplicate_retrieval_value, shared_memory_hit = extract_coordination_metrics(metrics, signals)
                prompt_tokens.append(prompt_token_value)
                completion_tokens.append(completion_token_value)
                total_tokens.append(total_token_value)
                runtime_latencies.append(runtime_latency)
                retrieval_latencies.append(retrieval_latency)
                llm_latencies.append(llm_latency)
                cache_hits += 1 if is_hit else 0
                cache_exact_hits += 1 if is_exact_hit else 0
                cache_semantic_hits += 1 if is_semantic_hit else 0
                retrieval_signals.append(retrieval_signal_value)
                tool_signals.append(tool_signal_value)
                duplicate_retrieval_signals.append(duplicate_retrieval_value)
                shared_memory_hits += 1 if shared_memory_hit else 0
            except Exception:
                errors += 1

    return {
        "requests": workers,
        "errors": errors,
        "latencies": latencies,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "runtime_latencies": runtime_latencies,
        "retrieval_latencies": retrieval_latencies,
        "llm_latencies": llm_latencies,
        "cache_hits": cache_hits,
        "cache_exact_hits": cache_exact_hits,
        "cache_semantic_hits": cache_semantic_hits,
        "retrieval_signals": retrieval_signals,
        "tool_signals": tool_signals,
        "duplicate_retrieval_signals": duplicate_retrieval_signals,
        "shared_memory_hits": shared_memory_hits,
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
    baseline_prompt_tokens: list[float] = []
    iris_prompt_tokens: list[float] = []
    baseline_completion_tokens: list[float] = []
    iris_completion_tokens: list[float] = []
    baseline_total_tokens: list[float] = []
    iris_total_tokens: list[float] = []
    baseline_runtime_latencies: list[float] = []
    iris_runtime_latencies: list[float] = []
    baseline_retrieval_latencies: list[float] = []
    iris_retrieval_latencies: list[float] = []
    baseline_llm_latencies: list[float] = []
    iris_llm_latencies: list[float] = []
    baseline_cache_hits = 0
    iris_cache_hits = 0
    baseline_cache_exact_hits = 0
    iris_cache_exact_hits = 0
    baseline_cache_semantic_hits = 0
    iris_cache_semantic_hits = 0
    baseline_retrieval_signals: list[float] = []
    iris_retrieval_signals: list[float] = []
    baseline_tool_signals: list[float] = []
    iris_tool_signals: list[float] = []
    baseline_duplicate_retrieval_signals: list[float] = []
    iris_duplicate_retrieval_signals: list[float] = []
    baseline_shared_memory_hits = 0
    iris_shared_memory_hits = 0
    baseline_errors = 0
    iris_errors = 0

    for _ in range(args.rounds):
        baseline_round = run_mode_batch(args.base_url, "baseline", args.workers, payload)
        iris_round = run_mode_batch(args.base_url, "iris", args.workers, payload)

        baseline_latencies.extend(baseline_round["latencies"])
        iris_latencies.extend(iris_round["latencies"])
        baseline_prompt_tokens.extend(baseline_round["prompt_tokens"])
        iris_prompt_tokens.extend(iris_round["prompt_tokens"])
        baseline_completion_tokens.extend(baseline_round["completion_tokens"])
        iris_completion_tokens.extend(iris_round["completion_tokens"])
        baseline_total_tokens.extend(baseline_round["total_tokens"])
        iris_total_tokens.extend(iris_round["total_tokens"])
        baseline_runtime_latencies.extend(baseline_round["runtime_latencies"])
        iris_runtime_latencies.extend(iris_round["runtime_latencies"])
        baseline_retrieval_latencies.extend(baseline_round["retrieval_latencies"])
        iris_retrieval_latencies.extend(iris_round["retrieval_latencies"])
        baseline_llm_latencies.extend(baseline_round["llm_latencies"])
        iris_llm_latencies.extend(iris_round["llm_latencies"])
        baseline_cache_hits += int(baseline_round["cache_hits"])
        iris_cache_hits += int(iris_round["cache_hits"])
        baseline_cache_exact_hits += int(baseline_round["cache_exact_hits"])
        iris_cache_exact_hits += int(iris_round["cache_exact_hits"])
        baseline_cache_semantic_hits += int(baseline_round["cache_semantic_hits"])
        iris_cache_semantic_hits += int(iris_round["cache_semantic_hits"])
        baseline_retrieval_signals.extend(baseline_round["retrieval_signals"])
        iris_retrieval_signals.extend(iris_round["retrieval_signals"])
        baseline_tool_signals.extend(baseline_round["tool_signals"])
        iris_tool_signals.extend(iris_round["tool_signals"])
        baseline_duplicate_retrieval_signals.extend(baseline_round["duplicate_retrieval_signals"])
        iris_duplicate_retrieval_signals.extend(iris_round["duplicate_retrieval_signals"])
        baseline_shared_memory_hits += int(baseline_round["shared_memory_hits"])
        iris_shared_memory_hits += int(iris_round["shared_memory_hits"])
        baseline_errors += int(baseline_round["errors"])
        iris_errors += int(iris_round["errors"])

    total_requests_per_mode = args.workers * args.rounds

    result = {
        "base_url": args.base_url,
        "workers": args.workers,
        "rounds": args.rounds,
        "total_requests_per_mode": total_requests_per_mode,
        "baseline": {
            "errors": baseline_errors,
            "latency_ms_avg": round(mean(baseline_latencies), 2) if baseline_latencies else 0.0,
            "latency_ms_p50": round(p50(baseline_latencies), 2),
            "latency_ms_p95": round(p95(baseline_latencies), 2),
            "runtime_latency_ms_avg": avg_or_zero(baseline_runtime_latencies),
            "runtime_latency_ms_p50": round(p50(baseline_runtime_latencies), 2),
            "runtime_latency_ms_p95": round(p95(baseline_runtime_latencies), 2),
            "retrieval_latency_ms_avg": avg_or_zero(baseline_retrieval_latencies),
            "llm_latency_ms_avg": avg_or_zero(baseline_llm_latencies),
            "cache_hits": baseline_cache_hits,
            "cache_exact_hits": baseline_cache_exact_hits,
            "cache_semantic_hits": baseline_cache_semantic_hits,
            "cache_hit_rate_pct": round((baseline_cache_hits / total_requests_per_mode) * 100.0, 2) if total_requests_per_mode else 0.0,
            "retrieval_signals_avg": avg_or_zero(baseline_retrieval_signals),
            "tool_signals_avg": avg_or_zero(baseline_tool_signals),
            "duplicate_retrieval_signals_avg": avg_or_zero(baseline_duplicate_retrieval_signals),
            "shared_memory_hits": baseline_shared_memory_hits,
            "shared_memory_hit_rate_pct": round((baseline_shared_memory_hits / total_requests_per_mode) * 100.0, 2) if total_requests_per_mode else 0.0,
            "prompt_tokens_avg": round(mean(baseline_prompt_tokens), 2) if baseline_prompt_tokens else 0.0,
            "completion_tokens_avg": round(mean(baseline_completion_tokens), 2) if baseline_completion_tokens else 0.0,
            "total_tokens_avg": round(mean(baseline_total_tokens), 2) if baseline_total_tokens else 0.0,
        },
        "iris": {
            "errors": iris_errors,
            "latency_ms_avg": round(mean(iris_latencies), 2) if iris_latencies else 0.0,
            "latency_ms_p50": round(p50(iris_latencies), 2),
            "latency_ms_p95": round(p95(iris_latencies), 2),
            "runtime_latency_ms_avg": avg_or_zero(iris_runtime_latencies),
            "runtime_latency_ms_p50": round(p50(iris_runtime_latencies), 2),
            "runtime_latency_ms_p95": round(p95(iris_runtime_latencies), 2),
            "retrieval_latency_ms_avg": avg_or_zero(iris_retrieval_latencies),
            "llm_latency_ms_avg": avg_or_zero(iris_llm_latencies),
            "cache_hits": iris_cache_hits,
            "cache_exact_hits": iris_cache_exact_hits,
            "cache_semantic_hits": iris_cache_semantic_hits,
            "cache_hit_rate_pct": round((iris_cache_hits / total_requests_per_mode) * 100.0, 2) if total_requests_per_mode else 0.0,
            "retrieval_signals_avg": avg_or_zero(iris_retrieval_signals),
            "tool_signals_avg": avg_or_zero(iris_tool_signals),
            "duplicate_retrieval_signals_avg": avg_or_zero(iris_duplicate_retrieval_signals),
            "shared_memory_hits": iris_shared_memory_hits,
            "shared_memory_hit_rate_pct": round((iris_shared_memory_hits / total_requests_per_mode) * 100.0, 2) if total_requests_per_mode else 0.0,
            "prompt_tokens_avg": round(mean(iris_prompt_tokens), 2) if iris_prompt_tokens else 0.0,
            "completion_tokens_avg": round(mean(iris_completion_tokens), 2) if iris_completion_tokens else 0.0,
            "total_tokens_avg": round(mean(iris_total_tokens), 2) if iris_total_tokens else 0.0,
        },
        "coordination_comparison": {
            "retrieval_signal_reduction_pct": reduction_pct(avg_or_zero(baseline_retrieval_signals), avg_or_zero(iris_retrieval_signals)),
            "tool_signal_reduction_pct": reduction_pct(avg_or_zero(baseline_tool_signals), avg_or_zero(iris_tool_signals)),
            "duplicate_retrieval_reduction_pct": reduction_pct(
                avg_or_zero(baseline_duplicate_retrieval_signals),
                avg_or_zero(iris_duplicate_retrieval_signals),
            ),
            "shared_memory_hit_rate_delta_pct_points": round(
                ((iris_shared_memory_hits - baseline_shared_memory_hits) / total_requests_per_mode) * 100.0,
                2,
            ) if total_requests_per_mode else 0.0,
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
