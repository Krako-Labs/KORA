"""Runtime-integrated dry-run evaluator for KRK route selectivity."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from kora.matrix_evaluator import load_matrix, repo_commit
from kora.route_selectivity_metrics import (
    FALLBACK_CLASSES,
    ROUTES,
    RouteDecision,
    RouteRequest,
    krk_dry_run_policy,
    route_request_from_item,
    validate_matrix_item,
)

CLAIM_LEVEL = "runtime_integrated_dry_run_route_selectivity_measured"
CLAIM_BOUNDARY = (
    "Runtime-integrated dry-run route-selectivity evidence only. This output records "
    "request-to-route-to-dry-run-executor evidence records without provider calls, GPU "
    "execution, production traffic, production savings, customer savings, infrastructure "
    "savings, H100 superiority, provider superiority, or production-readiness claims."
)

EXECUTOR_IDS = {
    "deterministic": "deterministic_dry_run_executor_v0",
    "cache": "cache_dry_run_executor_v0",
    "CPU": "cpu_dry_run_executor_v0",
    "provider": "provider_dry_run_executor_v0",
    "GPU": "gpu_dry_run_executor_v0",
    "fallback": "fallback_dry_run_executor_v0",
}


def _rate(count: int, total: int) -> float:
    return count / total if total else 0.0


def _fallback_classification(decision: RouteDecision) -> str | None:
    if decision.selected_route != "fallback":
        return None
    classification = decision.fallback_classification or "unknown_fallback"
    if classification not in FALLBACK_CLASSES:
        return "unknown_fallback"
    return classification


def execute_dry_run_route(request: RouteRequest, decision: RouteDecision) -> dict[str, Any]:
    """Execute the selected route through a public-safe dry-run executor."""

    if decision.selected_route not in EXECUTOR_IDS:
        raise ValueError(f"unsupported selected_route: {decision.selected_route}")
    return {
        "request_id": request.request_id,
        "executor_id": EXECUTOR_IDS[decision.selected_route],
        "executor_route": decision.selected_route,
        "execution_status": "dry_run_success",
        "dry_run": True,
        "provider_call_performed": False,
        "gpu_execution_performed": False,
        "output_record_type": "public_safe_dry_run_evidence_record",
    }


def _evaluate_item(item: dict[str, Any]) -> dict[str, Any]:
    validate_matrix_item(item)
    request = route_request_from_item(item)
    decision = krk_dry_run_policy(request)
    execution = execute_dry_run_route(request, decision)
    oracle = item["oracle_labels"]
    selected = decision.selected_route
    expected = str(oracle["expected_route"])
    acceptable_routes = [str(route) for route in oracle["acceptable_routes"]]
    disallowed_routes = [str(route) for route in oracle["disallowed_routes"]]
    acceptable = selected in acceptable_routes
    unsafe = selected in disallowed_routes
    fallback_classification = _fallback_classification(decision)
    return {
        "request_id": request.request_id,
        "workload_profile": request.workload_profile,
        "workload_class": request.workload_class,
        "selected_route": selected,
        "expected_route": expected,
        "acceptable": acceptable,
        "unsafe_misroute": unsafe,
        "decision_reason": decision.decision_reason,
        "fallback_classification": fallback_classification,
        "executor_id": execution["executor_id"],
        "executor_route": execution["executor_route"],
        "execution_status": execution["execution_status"],
        "dry_run": execution["dry_run"],
        "provider_call_performed": execution["provider_call_performed"],
        "gpu_execution_performed": execution["gpu_execution_performed"],
        "error": None,
    }


def evaluate_runtime_routes(
    matrix_paths: list[Path],
    *,
    command: str | None = None,
    repo_commit_value: str | None = None,
) -> dict[str, Any]:
    route_counts: Counter[str] = Counter({route: 0 for route in ROUTES})
    executor_counts: Counter[str] = Counter({route: 0 for route in ROUTES})
    fallback_counts: Counter[str] = Counter({kind: 0 for kind in FALLBACK_CLASSES})
    profile_counts: Counter[str] = Counter()
    evidence_records: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    exact_matches = 0
    acceptable_matches = 0
    unsafe_misroutes = 0
    dry_run_successes = 0

    sources: list[dict[str, Any]] = []
    for matrix_path in matrix_paths:
        matrix = load_matrix(matrix_path)
        profile_id = str(matrix["profile_id"])
        items = matrix["items"]
        sources.append(
            {
                "matrix_file": str(matrix_path.as_posix()),
                "profile_id": profile_id,
                "schema_version": matrix["schema_version"],
                "item_count": len(items),
            }
        )
        for item in items:
            request_id = str(item.get("request_id", ""))
            try:
                record = _evaluate_item(item)
                evidence_records.append(record)
                selected = record["selected_route"]
                route_counts[selected] += 1
                executor_counts[record["executor_route"]] += 1
                profile_counts[record["workload_profile"]] += 1
                exact_matches += int(selected == record["expected_route"])
                acceptable_matches += int(record["acceptable"])
                unsafe_misroutes += int(record["unsafe_misroute"])
                dry_run_successes += int(record["execution_status"] == "dry_run_success")
                fallback_classification = record["fallback_classification"]
                if fallback_classification:
                    fallback_counts[fallback_classification] += 1
            except Exception as exc:  # noqa: BLE001 - surfaced as item-level evidence error.
                errors.append({"request_id": request_id, "error": str(exc)})
                evidence_records.append(
                    {
                        "request_id": request_id,
                        "workload_profile": str(item.get("workload_profile", "")),
                        "workload_class": str(item.get("workload_class", "")),
                        "selected_route": None,
                        "expected_route": None,
                        "acceptable": False,
                        "unsafe_misroute": False,
                        "decision_reason": None,
                        "fallback_classification": None,
                        "executor_id": None,
                        "executor_route": None,
                        "execution_status": "dry_run_error",
                        "dry_run": True,
                        "provider_call_performed": False,
                        "gpu_execution_performed": False,
                        "error": str(exc),
                    }
                )

    total = len(evidence_records)
    error_count = len(errors)
    return {
        "schema_version": "krk_runtime_integrated_route_evaluation_v0",
        "claim_level": CLAIM_LEVEL,
        "claim_boundary": CLAIM_BOUNDARY,
        "workflow": [
            "request",
            "KRK route decision",
            "route-specific dry-run executor",
            "evidence record",
            "route-selectivity scoring",
            "report",
        ],
        "execution_mode": "runtime_integrated_dry_run",
        "provider_calls_performed": False,
        "gpu_execution_performed": False,
        "policy_id": "KRK",
        "policy_version": "krk_dry_run_v0",
        "total_requests": total,
        "profile_counts": dict(profile_counts),
        "route_counts": dict(route_counts),
        "executor_counts": dict(executor_counts),
        "fallback_counts": dict(fallback_counts),
        "metrics": {
            "exact_route_accuracy": _rate(exact_matches, total),
            "acceptable_route_rate": _rate(acceptable_matches, total),
            "unsafe_misroute_rate": _rate(unsafe_misroutes, total),
            "safety_fallback_rate": _rate(fallback_counts["safety_fallback"], total),
            "failure_fallback_rate": _rate(fallback_counts["failure_fallback"], total),
            "error_count": error_count,
            "error_percentage": _rate(error_count, total),
            "dry_run_execution_success_rate": _rate(dry_run_successes, total),
            "evidence_records_created": total,
        },
        "sources": sources,
        "evidence_records": evidence_records,
        "errors": errors,
        "reproducibility": {
            "repo_commit": repo_commit_value if repo_commit_value is not None else repo_commit(),
            "command": command or "",
        },
    }


def _format_metric(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def render_markdown_summary(result: dict[str, Any]) -> str:
    metrics = result["metrics"]
    route_rows = [f"| `{route}` | `{count}` |" for route, count in result["route_counts"].items()]
    executor_rows = [
        f"| `{route}` | `{count}` |" for route, count in result["executor_counts"].items()
    ]
    fallback_rows = [
        f"| `{kind}` | `{count}` |" for kind, count in result["fallback_counts"].items()
    ]
    metric_names = [
        "exact_route_accuracy",
        "acceptable_route_rate",
        "unsafe_misroute_rate",
        "safety_fallback_rate",
        "failure_fallback_rate",
        "error_count",
        "error_percentage",
        "dry_run_execution_success_rate",
        "evidence_records_created",
    ]
    metric_rows = [f"| `{name}` | `{_format_metric(metrics[name])}` |" for name in metric_names]
    source_rows = [
        f"| `{source['profile_id']}` | `{source['matrix_file']}` | `{source['item_count']}` |"
        for source in result["sources"]
    ]
    lines = [
        "# KRK Runtime-Integrated Route Evaluation v0",
        "",
        "Status: generated runtime-integrated dry-run route-selectivity evidence.",
        "",
        "This report runs public matrix requests through a dry-run workflow path: request, KRK route decision, route-specific dry-run executor, evidence record, route-selectivity scoring, and report.",
        "",
        "No provider calls or GPU execution were performed.",
        "",
        "## Run Metadata",
        "",
        f"- claim level: `{result['claim_level']}`",
        f"- execution mode: `{result['execution_mode']}`",
        f"- policy: `{result['policy_id']}`",
        f"- policy version: `{result['policy_version']}`",
        f"- total requests: `{result['total_requests']}`",
        f"- provider calls performed: `{str(result['provider_calls_performed']).lower()}`",
        f"- GPU execution performed: `{str(result['gpu_execution_performed']).lower()}`",
        f"- evidence records created: `{metrics['evidence_records_created']}`",
        f"- repo commit: `{result['reproducibility']['repo_commit']}`",
        "",
        "## Sources",
        "",
        "| Profile | Matrix file | Items |",
        "| --- | --- | ---: |",
        *source_rows,
        "",
        "## Route Counts",
        "",
        "| Route | Count |",
        "| --- | ---: |",
        *route_rows,
        "",
        "## Executor Counts",
        "",
        "| Executor route | Count |",
        "| --- | ---: |",
        *executor_rows,
        "",
        "## Metrics",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        *metric_rows,
        "",
        "## Fallback Counts",
        "",
        "| Fallback class | Count |",
        "| --- | ---: |",
        *fallback_rows,
        "",
        "## Claim Boundary",
        "",
        CLAIM_BOUNDARY,
        "",
    ]
    return "\n".join(lines)


def write_outputs(result: dict[str, Any], *, json_out: Path, md_out: Path) -> None:
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_out.write_text(render_markdown_summary(result), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a runtime-integrated dry-run KRK route evaluation."
    )
    parser.add_argument("--matrix", action="append", required=True, help="KRK matrix fixture path")
    parser.add_argument("--json-out", required=True, help="output path for evidence JSON")
    parser.add_argument("--md-out", required=True, help="output path for Markdown summary")
    parser.add_argument("--repo-commit", help="override repo commit metadata")
    args = parser.parse_args(argv)

    command_parts = ["python3 -m kora.runtime_route_evaluator"]
    for matrix in args.matrix:
        command_parts.extend(["--matrix", matrix])
    command_parts.extend(["--json-out", args.json_out, "--md-out", args.md_out])
    if args.repo_commit:
        command_parts.extend(["--repo-commit", args.repo_commit])
    command = " ".join(command_parts)
    result = evaluate_runtime_routes(
        [Path(matrix) for matrix in args.matrix],
        command=command,
        repo_commit_value=args.repo_commit,
    )
    write_outputs(result, json_out=Path(args.json_out), md_out=Path(args.md_out))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
