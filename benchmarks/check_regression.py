from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROFILE_THRESHOLDS: dict[str, dict[str, float]] = {
    "strict": {
        "latency": 15.0,
        "p95": 15.0,
        "tokens": 5.0,
    },
    "normal": {
        "latency": 25.0,
        "p95": 25.0,
        "tokens": 10.0,
    },
    "lenient": {
        "latency": 40.0,
        "p95": 40.0,
        "tokens": 20.0,
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check benchmark regression against baseline")
    parser.add_argument("--current", default="benchmarks/reports/ci-latest.json")
    parser.add_argument("--baseline", default="benchmarks/reports/regression-baseline.json")
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILE_THRESHOLDS.keys()),
        default="normal",
        help="Threshold profile: strict, normal, lenient",
    )
    parser.add_argument(
        "--max-latency-regression-pct",
        type=float,
        default=None,
        help="Optional override for average latency threshold percentage",
    )
    parser.add_argument(
        "--max-p95-regression-pct",
        type=float,
        default=None,
        help="Optional override for p95 latency threshold percentage",
    )
    parser.add_argument(
        "--max-token-regression-pct",
        type=float,
        default=None,
        help="Optional override for prompt token threshold percentage",
    )
    return parser.parse_args()


def resolve_thresholds(args: argparse.Namespace) -> dict[str, float]:
    profile_thresholds = PROFILE_THRESHOLDS[args.profile]
    return {
        "latency": (
            args.max_latency_regression_pct
            if args.max_latency_regression_pct is not None
            else profile_thresholds["latency"]
        ),
        "p95": (
            args.max_p95_regression_pct
            if args.max_p95_regression_pct is not None
            else profile_thresholds["p95"]
        ),
        "tokens": (
            args.max_token_regression_pct
            if args.max_token_regression_pct is not None
            else profile_thresholds["tokens"]
        ),
    }


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def pct_change(current: float, baseline: float) -> float:
    if baseline == 0:
        return 0.0
    return ((current - baseline) / baseline) * 100.0


def run() -> int:
    args = parse_args()
    thresholds = resolve_thresholds(args)
    current = load_json(Path(args.current))
    baseline = load_json(Path(args.baseline))

    checks: list[tuple[str, float, float, float]] = []
    failures: list[str] = []

    print(
        "Using regression profile "
        f"'{args.profile}' with thresholds: "
        f"latency={thresholds['latency']:.2f}% "
        f"p95={thresholds['p95']:.2f}% "
        f"tokens={thresholds['tokens']:.2f}%"
    )

    for mode in ["baseline", "iris"]:
        cur_metrics = current.get(mode, {})
        base_metrics = baseline.get(mode, {})

        lat_delta = pct_change(float(cur_metrics.get("latency_ms_avg", 0)), float(base_metrics.get("latency_ms_avg", 0)))
        p95_delta = pct_change(float(cur_metrics.get("latency_ms_p95", 0)), float(base_metrics.get("latency_ms_p95", 0)))
        token_delta = pct_change(float(cur_metrics.get("prompt_tokens_avg", 0)), float(base_metrics.get("prompt_tokens_avg", 0)))

        checks.append((f"{mode}.latency_ms_avg", lat_delta, thresholds["latency"], float(cur_metrics.get("latency_ms_avg", 0))))
        checks.append((f"{mode}.latency_ms_p95", p95_delta, thresholds["p95"], float(cur_metrics.get("latency_ms_p95", 0))))
        checks.append((f"{mode}.prompt_tokens_avg", token_delta, thresholds["tokens"], float(cur_metrics.get("prompt_tokens_avg", 0))))

    for metric, delta, threshold, current_value in checks:
        print(f"{metric}: current={current_value}, regression={delta:.2f}%, threshold={threshold:.2f}%")
        if delta > threshold:
            failures.append(
                f"{metric} regression {delta:.2f}% exceeds threshold {threshold:.2f}%"
            )

    if failures:
        print("Regression gate failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Regression gate passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
