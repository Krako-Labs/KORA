from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


SUPPORTED_MODES = {"direct-baseline", "dry-run", "kora-controlled"}


def load_workload(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        workload = json.load(handle)

    tasks = workload.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("workload must contain a 'tasks' list")

    return workload


def summarize_workload(workload: dict[str, Any]) -> dict[str, Any]:
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
        "total_tasks": len(tasks),
        "category_counts": dict(sorted(category_counts.items())),
        "requires_model_true": requires_model_true,
        "requires_model_false": requires_model_false,
    }


def build_dry_run_result(workload: dict[str, Any], workload_path: Path) -> dict[str, Any]:
    summary = summarize_workload(workload)

    return {
        "benchmark_name": workload.get("name", workload_path.stem),
        "mode": "dry-run",
        "workload_path": str(workload_path),
        **summary,
        "status": "ok",
        "notes": [
            "Dry-run only: no direct baseline execution was performed.",
            "Dry-run only: no KORA-controlled execution was performed.",
        ],
    }


def build_direct_baseline_result(workload: dict[str, Any], workload_path: Path) -> dict[str, Any]:
    summary = summarize_workload(workload)

    return {
        "benchmark_name": workload.get("name", workload_path.stem),
        "mode": "direct-baseline",
        "workload_path": str(workload_path),
        **summary,
        "simulated_model_invocations": summary["total_tasks"],
        "deterministic_tasks_sent_to_model": summary["requires_model_false"],
        "fallback_candidate_tasks_sent_to_model": summary["requires_model_true"],
        "status": "ok",
        "notes": [
            "Simulated naive baseline: every task is counted as one model invocation.",
            "No real model calls or external APIs were used.",
            "No KORA-controlled execution was performed.",
        ],
    }


def build_kora_controlled_result(workload: dict[str, Any], workload_path: Path) -> dict[str, Any]:
    summary = summarize_workload(workload)
    direct_baseline_invocations = summary["total_tasks"]
    simulated_model_invocations = summary["requires_model_true"]
    avoided_invocations = direct_baseline_invocations - simulated_model_invocations
    avoided_rate = avoided_invocations / direct_baseline_invocations if direct_baseline_invocations else 0.0

    return {
        "benchmark_name": workload.get("name", workload_path.stem),
        "mode": "kora-controlled",
        "workload_path": str(workload_path),
        **summary,
        "deterministic_resolutions": summary["requires_model_false"],
        "fallback_candidates": summary["requires_model_true"],
        "simulated_model_invocations": simulated_model_invocations,
        "avoided_model_invocations_vs_direct_baseline": avoided_invocations,
        "avoided_model_invocation_rate": avoided_rate,
        "status": "ok",
        "notes": [
            "Simulated deterministic-first KORA-controlled mode based on workload metadata.",
            "Tasks with requires_model=false are counted as deterministic resolutions.",
            "Tasks with requires_model=true are counted as fallback/model-invocation candidates.",
            "No real model calls, external APIs, or full KORA runtime integration were used.",
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


def run_direct_baseline(workload_path: Path, output_path: Path) -> dict[str, Any]:
    workload = load_workload(workload_path)
    result = build_direct_baseline_result(workload, workload_path)
    write_result(result, output_path)
    return result


def run_kora_controlled(workload_path: Path, output_path: Path) -> dict[str, Any]:
    workload = load_workload(workload_path)
    result = build_kora_controlled_result(workload, workload_path)
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
    elif args.mode == "direct-baseline":
        result = run_direct_baseline(workload_path, output_path)
    elif args.mode == "kora-controlled":
        result = run_kora_controlled(workload_path, output_path)
    else:
        raise ValueError(f"unsupported mode: {args.mode}")

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


if __name__ == "__main__":
    raise SystemExit(main())
