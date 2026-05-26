from __future__ import annotations

import argparse
import json
import math
import time
import urllib.request
from pathlib import Path
from statistics import mean
from typing import Any


SCENARIO_PROFILES: dict[str, list[dict[str, str]]] = {
    "smoke": [
        {
            "id": "outage-renewal-risk",
            "customer": "Acme Corp",
            "message": "Our production system is down again and we are considering canceling our renewal.",
        }
    ],
    "expanded": [
        {
            "id": "outage-renewal-risk",
            "customer": "Acme Corp",
            "message": "Our production system is down again and we are considering canceling our renewal.",
        },
        {
            "id": "executive-summary-followup-a",
            "customer": "Acme Corp",
            "message": "Prepare an executive summary for the outage and include the promised escalation path.",
        },
        {
            "id": "executive-summary-followup-b",
            "customer": "Acme Corp",
            "message": "Prepare an executive summary for the outage and include the promised escalation path.",
        },
        {
            "id": "memory-heavy-context",
            "customer": "Acme Corp",
            "message": "Use prior commitments, stakeholder preferences, open incidents, and billing SLA context to draft next-step actions.",
        },
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run baseline vs IRIS endpoint benchmark")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--scenario-profile", choices=sorted(SCENARIO_PROFILES.keys()), default="smoke")
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


def p50(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(0.50 * len(ordered)) - 1)
    return ordered[index]


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


def repeated_query_savings(latency_by_message: dict[str, list[float]]) -> dict[str, float | int]:
    first_values: list[float] = []
    repeated_values: list[float] = []
    for values in latency_by_message.values():
        if len(values) < 2:
            continue
        first_values.append(values[0])
        repeated_values.extend(values[1:])

    if not first_values or not repeated_values:
        return {
            "repeated_query_samples": 0,
            "first_query_runtime_latency_ms_avg": 0.0,
            "repeated_query_runtime_latency_ms_avg": 0.0,
            "repeated_query_latency_savings_pct": 0.0,
        }

    first_avg = mean(first_values)
    repeated_avg = mean(repeated_values)
    savings_pct = 0.0 if first_avg <= 0 else ((first_avg - repeated_avg) / first_avg) * 100.0
    return {
        "repeated_query_samples": len(repeated_values),
        "first_query_runtime_latency_ms_avg": round(first_avg, 2),
        "repeated_query_runtime_latency_ms_avg": round(repeated_avg, 2),
        "repeated_query_latency_savings_pct": round(savings_pct, 2),
    }


def summarize(values: list[float]) -> dict[str, float]:
    if not values:
        return {
            "latency_ms_avg": 0.0,
            "latency_ms_p50": 0.0,
            "latency_ms_p95": 0.0,
            "runtime_latency_ms_avg": 0.0,
            "runtime_latency_ms_p50": 0.0,
            "runtime_latency_ms_p95": 0.0,
            "retrieval_latency_ms_avg": 0.0,
            "llm_latency_ms_avg": 0.0,
            "prompt_tokens_avg": 0.0,
            "completion_tokens_avg": 0.0,
            "total_tokens_avg": 0.0,
        }
    return {
        "latency_ms_avg": round(mean(values), 2),
        "latency_ms_p50": round(p50(values), 2),
        "latency_ms_p95": round(p95(values), 2),
        "runtime_latency_ms_avg": 0.0,
        "runtime_latency_ms_p50": 0.0,
        "runtime_latency_ms_p95": 0.0,
        "retrieval_latency_ms_avg": 0.0,
        "llm_latency_ms_avg": 0.0,
        "prompt_tokens_avg": 0.0,
        "completion_tokens_avg": 0.0,
        "total_tokens_avg": 0.0,
    }


def run() -> int:
    args = parse_args()
    scenarios = SCENARIO_PROFILES[args.scenario_profile]

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
    baseline_runtime_latency_by_message: dict[str, list[float]] = {}
    iris_runtime_latency_by_message: dict[str, list[float]] = {}
    baseline_retrieval_signals: list[float] = []
    iris_retrieval_signals: list[float] = []
    baseline_tool_signals: list[float] = []
    iris_tool_signals: list[float] = []
    baseline_duplicate_retrieval_signals: list[float] = []
    iris_duplicate_retrieval_signals: list[float] = []
    baseline_shared_memory_hits = 0
    iris_shared_memory_hits = 0

    scenario_metrics: dict[str, dict[str, list[float]]] = {
        scenario["id"]: {
            "baseline_latencies": [],
            "baseline_prompt_tokens": [],
            "baseline_completion_tokens": [],
            "baseline_total_tokens": [],
            "baseline_runtime_latencies": [],
            "baseline_retrieval_latencies": [],
            "baseline_llm_latencies": [],
            "baseline_retrieval_signals": [],
            "baseline_tool_signals": [],
            "baseline_duplicate_retrieval_signals": [],
            "baseline_shared_memory_hits": [],
            "iris_latencies": [],
            "iris_prompt_tokens": [],
            "iris_completion_tokens": [],
            "iris_total_tokens": [],
            "iris_runtime_latencies": [],
            "iris_retrieval_latencies": [],
            "iris_llm_latencies": [],
            "iris_retrieval_signals": [],
            "iris_tool_signals": [],
            "iris_duplicate_retrieval_signals": [],
            "iris_shared_memory_hits": [],
        }
        for scenario in scenarios
    }

    for _ in range(args.iterations):
        for scenario in scenarios:
            message_key = str(scenario["message"]).strip().lower()
            payload = {
                "customer": scenario["customer"],
                "message": scenario["message"],
            }
            baseline_ms, baseline_result = call_json(f"{args.base_url}/api/run/baseline", payload)
            iris_ms, iris_result = call_json(f"{args.base_url}/api/run/iris", payload)

            baseline_latencies.append(baseline_ms)
            iris_latencies.append(iris_ms)

            baseline_metrics = baseline_result.get("metrics", {})
            iris_metrics = iris_result.get("metrics", {})

            baseline_prompt_token_value, baseline_completion_token_value, baseline_total_token_value = extract_token_triplet(baseline_metrics)
            iris_prompt_token_value, iris_completion_token_value, iris_total_token_value = extract_token_triplet(iris_metrics)
            baseline_runtime_latency, baseline_retrieval_latency, baseline_llm_latency = extract_latency_components(baseline_metrics)
            iris_runtime_latency, iris_retrieval_latency, iris_llm_latency = extract_latency_components(iris_metrics)
            baseline_signals = extract_context_signals(baseline_result)
            iris_signals = extract_context_signals(iris_result)
            baseline_hit, baseline_exact_hit, baseline_semantic_hit = extract_cache_hit_flags(baseline_signals)
            iris_hit, iris_exact_hit, iris_semantic_hit = extract_cache_hit_flags(iris_signals)
            baseline_retrieval_signal_value, baseline_tool_signal_value, baseline_duplicate_retrieval_value, baseline_shared_memory_hit = extract_coordination_metrics(baseline_metrics, baseline_signals)
            iris_retrieval_signal_value, iris_tool_signal_value, iris_duplicate_retrieval_value, iris_shared_memory_hit = extract_coordination_metrics(iris_metrics, iris_signals)

            baseline_prompt_tokens.append(baseline_prompt_token_value)
            iris_prompt_tokens.append(iris_prompt_token_value)
            baseline_completion_tokens.append(baseline_completion_token_value)
            iris_completion_tokens.append(iris_completion_token_value)
            baseline_total_tokens.append(baseline_total_token_value)
            iris_total_tokens.append(iris_total_token_value)
            baseline_runtime_latencies.append(baseline_runtime_latency)
            iris_runtime_latencies.append(iris_runtime_latency)
            baseline_retrieval_latencies.append(baseline_retrieval_latency)
            iris_retrieval_latencies.append(iris_retrieval_latency)
            baseline_llm_latencies.append(baseline_llm_latency)
            iris_llm_latencies.append(iris_llm_latency)
            baseline_cache_hits += 1 if baseline_hit else 0
            iris_cache_hits += 1 if iris_hit else 0
            baseline_cache_exact_hits += 1 if baseline_exact_hit else 0
            iris_cache_exact_hits += 1 if iris_exact_hit else 0
            baseline_cache_semantic_hits += 1 if baseline_semantic_hit else 0
            iris_cache_semantic_hits += 1 if iris_semantic_hit else 0

            baseline_runtime_latency_by_message.setdefault(message_key, []).append(baseline_runtime_latency)
            iris_runtime_latency_by_message.setdefault(message_key, []).append(iris_runtime_latency)
            baseline_retrieval_signals.append(baseline_retrieval_signal_value)
            iris_retrieval_signals.append(iris_retrieval_signal_value)
            baseline_tool_signals.append(baseline_tool_signal_value)
            iris_tool_signals.append(iris_tool_signal_value)
            baseline_duplicate_retrieval_signals.append(baseline_duplicate_retrieval_value)
            iris_duplicate_retrieval_signals.append(iris_duplicate_retrieval_value)
            baseline_shared_memory_hits += 1 if baseline_shared_memory_hit else 0
            iris_shared_memory_hits += 1 if iris_shared_memory_hit else 0

            per_scenario = scenario_metrics[scenario["id"]]
            per_scenario["baseline_latencies"].append(baseline_ms)
            per_scenario["baseline_prompt_tokens"].append(baseline_prompt_token_value)
            per_scenario["baseline_completion_tokens"].append(baseline_completion_token_value)
            per_scenario["baseline_total_tokens"].append(baseline_total_token_value)
            per_scenario["baseline_runtime_latencies"].append(baseline_runtime_latency)
            per_scenario["baseline_retrieval_latencies"].append(baseline_retrieval_latency)
            per_scenario["baseline_llm_latencies"].append(baseline_llm_latency)
            per_scenario["baseline_retrieval_signals"].append(baseline_retrieval_signal_value)
            per_scenario["baseline_tool_signals"].append(baseline_tool_signal_value)
            per_scenario["baseline_duplicate_retrieval_signals"].append(baseline_duplicate_retrieval_value)
            per_scenario["baseline_shared_memory_hits"].append(1.0 if baseline_shared_memory_hit else 0.0)
            per_scenario["iris_latencies"].append(iris_ms)
            per_scenario["iris_prompt_tokens"].append(iris_prompt_token_value)
            per_scenario["iris_completion_tokens"].append(iris_completion_token_value)
            per_scenario["iris_total_tokens"].append(iris_total_token_value)
            per_scenario["iris_runtime_latencies"].append(iris_runtime_latency)
            per_scenario["iris_retrieval_latencies"].append(iris_retrieval_latency)
            per_scenario["iris_llm_latencies"].append(iris_llm_latency)
            per_scenario["iris_retrieval_signals"].append(iris_retrieval_signal_value)
            per_scenario["iris_tool_signals"].append(iris_tool_signal_value)
            per_scenario["iris_duplicate_retrieval_signals"].append(iris_duplicate_retrieval_value)
            per_scenario["iris_shared_memory_hits"].append(1.0 if iris_shared_memory_hit else 0.0)

    scenario_breakdown: dict[str, dict[str, Any]] = {}
    for scenario in scenarios:
        scenario_id = scenario["id"]
        metrics = scenario_metrics[scenario_id]

        baseline_summary = summarize(metrics["baseline_latencies"])
        baseline_summary["prompt_tokens_avg"] = round(mean(metrics["baseline_prompt_tokens"]), 2) if metrics["baseline_prompt_tokens"] else 0.0
        baseline_summary["completion_tokens_avg"] = round(mean(metrics["baseline_completion_tokens"]), 2) if metrics["baseline_completion_tokens"] else 0.0
        baseline_summary["total_tokens_avg"] = round(mean(metrics["baseline_total_tokens"]), 2) if metrics["baseline_total_tokens"] else 0.0
        baseline_summary["runtime_latency_ms_avg"] = avg_or_zero(metrics["baseline_runtime_latencies"])
        baseline_summary["runtime_latency_ms_p50"] = round(p50(metrics["baseline_runtime_latencies"]), 2)
        baseline_summary["runtime_latency_ms_p95"] = round(p95(metrics["baseline_runtime_latencies"]), 2)
        baseline_summary["retrieval_latency_ms_avg"] = avg_or_zero(metrics["baseline_retrieval_latencies"])
        baseline_summary["llm_latency_ms_avg"] = avg_or_zero(metrics["baseline_llm_latencies"])
        baseline_summary["retrieval_signals_avg"] = avg_or_zero(metrics["baseline_retrieval_signals"])
        baseline_summary["tool_signals_avg"] = avg_or_zero(metrics["baseline_tool_signals"])
        baseline_summary["duplicate_retrieval_signals_avg"] = avg_or_zero(metrics["baseline_duplicate_retrieval_signals"])
        baseline_summary["shared_memory_hit_rate_pct"] = avg_or_zero(metrics["baseline_shared_memory_hits"]) * 100.0

        iris_summary = summarize(metrics["iris_latencies"])
        iris_summary["prompt_tokens_avg"] = round(mean(metrics["iris_prompt_tokens"]), 2) if metrics["iris_prompt_tokens"] else 0.0
        iris_summary["completion_tokens_avg"] = round(mean(metrics["iris_completion_tokens"]), 2) if metrics["iris_completion_tokens"] else 0.0
        iris_summary["total_tokens_avg"] = round(mean(metrics["iris_total_tokens"]), 2) if metrics["iris_total_tokens"] else 0.0
        iris_summary["runtime_latency_ms_avg"] = avg_or_zero(metrics["iris_runtime_latencies"])
        iris_summary["runtime_latency_ms_p50"] = round(p50(metrics["iris_runtime_latencies"]), 2)
        iris_summary["runtime_latency_ms_p95"] = round(p95(metrics["iris_runtime_latencies"]), 2)
        iris_summary["retrieval_latency_ms_avg"] = avg_or_zero(metrics["iris_retrieval_latencies"])
        iris_summary["llm_latency_ms_avg"] = avg_or_zero(metrics["iris_llm_latencies"])
        iris_summary["retrieval_signals_avg"] = avg_or_zero(metrics["iris_retrieval_signals"])
        iris_summary["tool_signals_avg"] = avg_or_zero(metrics["iris_tool_signals"])
        iris_summary["duplicate_retrieval_signals_avg"] = avg_or_zero(metrics["iris_duplicate_retrieval_signals"])
        iris_summary["shared_memory_hit_rate_pct"] = avg_or_zero(metrics["iris_shared_memory_hits"]) * 100.0

        scenario_breakdown[scenario_id] = {
            "customer": scenario["customer"],
            "message": scenario["message"],
            "baseline": baseline_summary,
            "iris": iris_summary,
        }

    baseline_repeated_query = repeated_query_savings(baseline_runtime_latency_by_message)
    iris_repeated_query = repeated_query_savings(iris_runtime_latency_by_message)
    total_requests_per_mode = args.iterations * len(scenarios)

    result = {
        "iterations": args.iterations,
        "base_url": args.base_url,
        "scenario_profile": args.scenario_profile,
        "scenario_count": len(scenarios),
        "total_requests_per_mode": total_requests_per_mode,
        "scenario_order": [scenario["id"] for scenario in scenarios],
        "baseline": {
            "latency_ms_avg": round(mean(baseline_latencies), 2),
            "latency_ms_p50": round(p50(baseline_latencies), 2),
            "latency_ms_p95": round(p95(baseline_latencies), 2),
            "runtime_latency_ms_avg": avg_or_zero(baseline_runtime_latencies),
            "runtime_latency_ms_p50": round(p50(baseline_runtime_latencies), 2),
            "runtime_latency_ms_p95": round(p95(baseline_runtime_latencies), 2),
            "retrieval_latency_ms_avg": avg_or_zero(baseline_retrieval_latencies),
            "llm_latency_ms_avg": avg_or_zero(baseline_llm_latencies),
            "retrieval_signals_avg": avg_or_zero(baseline_retrieval_signals),
            "tool_signals_avg": avg_or_zero(baseline_tool_signals),
            "duplicate_retrieval_signals_avg": avg_or_zero(baseline_duplicate_retrieval_signals),
            "shared_memory_hits": baseline_shared_memory_hits,
            "shared_memory_hit_rate_pct": round((baseline_shared_memory_hits / total_requests_per_mode) * 100.0, 2) if total_requests_per_mode else 0.0,
            "cache_hits": baseline_cache_hits,
            "cache_exact_hits": baseline_cache_exact_hits,
            "cache_semantic_hits": baseline_cache_semantic_hits,
            "cache_hit_rate_pct": round((baseline_cache_hits / total_requests_per_mode) * 100.0, 2) if total_requests_per_mode else 0.0,
            "repeated_query_samples": baseline_repeated_query["repeated_query_samples"],
            "first_query_runtime_latency_ms_avg": baseline_repeated_query["first_query_runtime_latency_ms_avg"],
            "repeated_query_runtime_latency_ms_avg": baseline_repeated_query["repeated_query_runtime_latency_ms_avg"],
            "repeated_query_latency_savings_pct": baseline_repeated_query["repeated_query_latency_savings_pct"],
            "prompt_tokens_avg": round(mean(baseline_prompt_tokens), 2),
            "completion_tokens_avg": round(mean(baseline_completion_tokens), 2),
            "total_tokens_avg": round(mean(baseline_total_tokens), 2),
        },
        "iris": {
            "latency_ms_avg": round(mean(iris_latencies), 2),
            "latency_ms_p50": round(p50(iris_latencies), 2),
            "latency_ms_p95": round(p95(iris_latencies), 2),
            "runtime_latency_ms_avg": avg_or_zero(iris_runtime_latencies),
            "runtime_latency_ms_p50": round(p50(iris_runtime_latencies), 2),
            "runtime_latency_ms_p95": round(p95(iris_runtime_latencies), 2),
            "retrieval_latency_ms_avg": avg_or_zero(iris_retrieval_latencies),
            "llm_latency_ms_avg": avg_or_zero(iris_llm_latencies),
            "retrieval_signals_avg": avg_or_zero(iris_retrieval_signals),
            "tool_signals_avg": avg_or_zero(iris_tool_signals),
            "duplicate_retrieval_signals_avg": avg_or_zero(iris_duplicate_retrieval_signals),
            "shared_memory_hits": iris_shared_memory_hits,
            "shared_memory_hit_rate_pct": round((iris_shared_memory_hits / total_requests_per_mode) * 100.0, 2) if total_requests_per_mode else 0.0,
            "cache_hits": iris_cache_hits,
            "cache_exact_hits": iris_cache_exact_hits,
            "cache_semantic_hits": iris_cache_semantic_hits,
            "cache_hit_rate_pct": round((iris_cache_hits / total_requests_per_mode) * 100.0, 2) if total_requests_per_mode else 0.0,
            "repeated_query_samples": iris_repeated_query["repeated_query_samples"],
            "first_query_runtime_latency_ms_avg": iris_repeated_query["first_query_runtime_latency_ms_avg"],
            "repeated_query_runtime_latency_ms_avg": iris_repeated_query["repeated_query_runtime_latency_ms_avg"],
            "repeated_query_latency_savings_pct": iris_repeated_query["repeated_query_latency_savings_pct"],
            "prompt_tokens_avg": round(mean(iris_prompt_tokens), 2),
            "completion_tokens_avg": round(mean(iris_completion_tokens), 2),
            "total_tokens_avg": round(mean(iris_total_tokens), 2),
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
        "scenario_breakdown": scenario_breakdown,
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
