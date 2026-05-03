from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


SUPPORTED_MODES = {"dry-run"}


def load_workload(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        workload = json.load(handle)

    tasks = workload.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("workload must contain a 'tasks' list")

    return workload


def build_dry_run_result(workload: dict[str, Any], workload_path: Path) -> dict[str, Any]:
    tasks = workload["tasks"]
    category_counts = Counter()
    requires_model_true = 0
    requires_model_false = 0

    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise ValueError(f"task at index {index} must be an object")

        category = task.get("category")
        if not isinstance(category, str) or not category:
            raise ValueError(f"task at index {index} must contain a non-empty category")
        category_counts[category] += 1

        requires_model = task.get("requires_model")
        if requires_model is True:
            requires_model_true += 1
        elif requires_model is False:
            requires_model_false += 1
        else:
            raise ValueError(f"task at index {index} must contain boolean requires_model")

    return {
        "benchmark_name": workload.get("name", workload_path.stem),
        "mode": "dry-run",
        "workload_path": str(workload_path),
        "total_tasks": len(tasks),
        "category_counts": dict(sorted(category_counts.items())),
        "requires_model_true": requires_model_true,
        "requires_model_false": requires_model_false,
        "status": "ok",
        "notes": [
            "Dry-run only: no direct baseline execution was performed.",
            "Dry-run only: no KORA-controlled execution was performed.",
        ],
    }


def write_result(result: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")


def run_dry_run(workload_path: Path, output_path: Path) -> dict[str, Any]:
    workload = load_workload(workload_path)
    result = build_dry_run_result(workload, workload_path)
    write_result(result, output_path)
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run KORA benchmark skeleton modes.")
    parser.add_argument("--workload", required=True, help="Path to workload JSON")
    parser.add_argument("--output", required=True, help="Path for result JSON")
    parser.add_argument("--mode", required=True, choices=sorted(SUPPORTED_MODES), help="Benchmark mode")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    workload_path = Path(args.workload)
    output_path = Path(args.output)

    if args.mode == "dry-run":
        result = run_dry_run(workload_path, output_path)
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "benchmark_name": result["benchmark_name"],
                    "mode": result["mode"],
                    "total_tasks": result["total_tasks"],
                    "output": str(output_path),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    raise ValueError(f"unsupported mode: {args.mode}")


if __name__ == "__main__":
    raise SystemExit(main())
