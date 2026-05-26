from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append benchmark metrics to trend history")
    parser.add_argument(
        "--reports",
        nargs="+",
        default=[
            "benchmarks/reports/latest.json",
            "benchmarks/reports/ci-latest.json",
            "benchmarks/reports/ci-extended.json",
        ],
    )
    parser.add_argument("--history", default="benchmarks/reports/trend-history.json")
    parser.add_argument("--source", default="manual")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def build_entry(report_name: str, payload: dict[str, Any], source: str) -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "report": report_name,
        "iterations": payload.get("iterations"),
        "baseline": payload.get("baseline", {}),
        "iris": payload.get("iris", {}),
    }


def run() -> int:
    args = parse_args()

    history_path = Path(args.history)
    history_path.parent.mkdir(parents=True, exist_ok=True)

    existing: list[dict[str, Any]] = []
    if history_path.exists():
        existing = json.loads(history_path.read_text(encoding="utf-8"))

    appended = 0
    for report in args.reports:
        report_path = Path(report)
        payload = load_json(report_path)
        if payload is None:
            continue

        existing.append(build_entry(report_path.name, payload, args.source))
        appended += 1

    # Keep only the latest 300 snapshots to cap file growth.
    existing = existing[-300:]

    history_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    print(f"Trend snapshots appended: {appended}")
    print(f"Saved: {history_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
