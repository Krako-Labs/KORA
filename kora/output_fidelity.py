"""Baseline equivalence and output fidelity evaluation for KRK matrix fixtures."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from kora.matrix_evaluator import load_matrix, repo_commit
from kora.route_selectivity_metrics import (
    ROUTES,
    krk_dry_run_policy,
    route_request_from_item,
    validate_matrix_item,
)

CLAIM_LEVEL = "baseline_equivalence_output_fidelity_measured"
FINAL_CLASSIFICATION = "BASELINE_EQUIVALENCE_OUTPUT_FIDELITY_MEASURED"
COMPARISON_CATEGORIES = (
    "exact_match",
    "structured_equivalent",
    "semantic_equivalent_stubbed_or_rule_based",
    "degraded",
    "failed",
)
CLAIM_BOUNDARY = (
    "Public fixture-derived baseline equivalence and output fidelity evidence only. "
    "This output uses deterministic rule-based comparison against committed public matrix "
    "fixtures. It does not claim production proof, production cost reduction, customer "
    "savings, energy reduction, broad workload superiority, real API/GPU cost reduction, "
    "semantic-model-judge validation, provider superiority, H100 superiority, or production readiness."
)


def _rate(count: int, total: int) -> float:
    return count / total if total else 0.0


def _baseline_output(item: dict[str, Any]) -> dict[str, Any]:
    oracle = item["oracle_labels"]
    return {
        "output_contract": "public_matrix_expected_route_contract_v0",
        "workload_profile": str(item["workload_profile"]),
        "workload_class": str(item["workload_class"]),
        "route": str(oracle["expected_route"]),
        "status": "success",
        "normalized_result_key": (
            f"{item['workload_profile']}::{item['workload_class']}::"
            f"{oracle['expected_route']}::expected"
        ),
    }


def _krk_output(item: dict[str, Any], selected_route: str, acceptable: bool) -> dict[str, Any]:
    return {
        "output_contract": "public_matrix_krk_routed_contract_v0",
        "workload_profile": str(item["workload_profile"]),
        "workload_class": str(item["workload_class"]),
        "route": selected_route,
        "status": "success" if acceptable else "degraded",
        "normalized_result_key": (
            f"{item['workload_profile']}::{item['workload_class']}::{selected_route}::krk"
        ),
    }


def compare_outputs(item: dict[str, Any]) -> dict[str, Any]:
    """Compare public fixture-derived baseline output with KRK-routed output."""

    validate_matrix_item(item)
    request = route_request_from_item(item)
    decision = krk_dry_run_policy(request)
    expected_route = str(item["oracle_labels"]["expected_route"])
    acceptable_routes = [str(route) for route in item["oracle_labels"]["acceptable_routes"]]
    disallowed_routes = [str(route) for route in item["oracle_labels"]["disallowed_routes"]]
    selected_route = decision.selected_route
    acceptable = selected_route in acceptable_routes
    unsafe = selected_route in disallowed_routes
    baseline = _baseline_output(item)
    krk = _krk_output(item, selected_route, acceptable)

    if selected_route == expected_route and acceptable:
        category = "exact_match"
        fidelity_status = "acceptable"
        comparison_basis = "exact_route_and_public_fixture_contract_match"
    elif acceptable and not unsafe:
        category = "structured_equivalent"
        fidelity_status = "acceptable"
        comparison_basis = "alternate_public_oracle_acceptable_route"
    elif selected_route in ROUTES:
        category = "degraded"
        fidelity_status = "degraded"
        comparison_basis = "selected_route_not_public_oracle_acceptable"
    else:
        category = "failed"
        fidelity_status = "failed"
        comparison_basis = "selected_route_not_supported"

    return {
        "request_id": str(item["request_id"]),
        "workload_profile": str(item["workload_profile"]),
        "workload_class": str(item["workload_class"]),
        "baseline_route": expected_route,
        "krk_route": selected_route,
        "comparison_category": category,
        "fidelity_status": fidelity_status,
        "comparison_basis": comparison_basis,
        "baseline_success": baseline["status"] == "success",
        "krk_success": krk["status"] == "success",
        "route_changed": selected_route != expected_route,
        "route_change_acceptable": selected_route != expected_route and acceptable and not unsafe,
        "semantic_model_judge_used": False,
        "provider_call_performed": False,
        "gpu_execution_performed": False,
        "baseline_output_record_type": baseline["output_contract"],
        "krk_output_record_type": krk["output_contract"],
        "error": None,
    }


def _empty_route_summary(route: str) -> dict[str, Any]:
    return {
        "route": route,
        "total": 0,
        "baseline_success_count": 0,
        "krk_success_count": 0,
        "exact_match_count": 0,
        "structured_equivalent_count": 0,
        "semantic_equivalent_count": 0,
        "degraded_count": 0,
        "failed_count": 0,
        "acceptable_output_rate": 0.0,
        "degradation_rate": 0.0,
        "failure_rate": 0.0,
    }


def _route_summary(route: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    summary = _empty_route_summary(route)
    summary["total"] = len(records)
    summary["baseline_success_count"] = sum(int(record["baseline_success"]) for record in records)
    summary["krk_success_count"] = sum(int(record["krk_success"]) for record in records)
    summary["exact_match_count"] = sum(
        int(record["comparison_category"] == "exact_match") for record in records
    )
    summary["structured_equivalent_count"] = sum(
        int(record["comparison_category"] == "structured_equivalent") for record in records
    )
    summary["semantic_equivalent_count"] = sum(
        int(record["comparison_category"] == "semantic_equivalent_stubbed_or_rule_based")
        for record in records
    )
    summary["degraded_count"] = sum(
        int(record["comparison_category"] == "degraded") for record in records
    )
    summary["failed_count"] = sum(int(record["comparison_category"] == "failed") for record in records)
    acceptable_count = (
        summary["exact_match_count"]
        + summary["structured_equivalent_count"]
        + summary["semantic_equivalent_count"]
    )
    total = int(summary["total"])
    summary["acceptable_output_rate"] = _rate(acceptable_count, total)
    summary["degradation_rate"] = _rate(int(summary["degraded_count"]), total)
    summary["failure_rate"] = _rate(int(summary["failed_count"]), total)
    return summary


def evaluate_output_fidelity(
    matrix_paths: list[Path],
    *,
    command: str | None = None,
    repo_commit_value: str | None = None,
) -> dict[str, Any]:
    sources: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    profile_counts: Counter[str] = Counter()
    category_counts: Counter[str] = Counter({category: 0 for category in COMPARISON_CATEGORIES})

    for matrix_path in matrix_paths:
        matrix = load_matrix(matrix_path)
        profile_id = str(matrix["profile_id"])
        items = matrix["items"]
        sources.append(
            {
                "matrix_file": matrix_path.as_posix(),
                "profile_id": profile_id,
                "schema_version": matrix["schema_version"],
                "item_count": len(items),
            }
        )
        for item in items:
            request_id = str(item.get("request_id", ""))
            try:
                record = compare_outputs(item)
                records.append(record)
                profile_counts[record["workload_profile"]] += 1
                category_counts[record["comparison_category"]] += 1
            except Exception as exc:  # noqa: BLE001 - item-level fidelity error.
                errors.append({"request_id": request_id, "error": str(exc)})
                record = {
                    "request_id": request_id,
                    "workload_profile": str(item.get("workload_profile", "")),
                    "workload_class": str(item.get("workload_class", "")),
                    "baseline_route": None,
                    "krk_route": None,
                    "comparison_category": "failed",
                    "fidelity_status": "failed",
                    "comparison_basis": "evaluation_error",
                    "baseline_success": False,
                    "krk_success": False,
                    "route_changed": False,
                    "route_change_acceptable": False,
                    "semantic_model_judge_used": False,
                    "provider_call_performed": False,
                    "gpu_execution_performed": False,
                    "baseline_output_record_type": None,
                    "krk_output_record_type": None,
                    "error": str(exc),
                }
                records.append(record)
                category_counts["failed"] += 1

    total = len(records)
    baseline_success_count = sum(int(record["baseline_success"]) for record in records)
    krk_success_count = sum(int(record["krk_success"]) for record in records)
    exact_count = category_counts["exact_match"]
    structured_count = category_counts["structured_equivalent"]
    semantic_count = category_counts["semantic_equivalent_stubbed_or_rule_based"]
    degraded_count = category_counts["degraded"]
    failed_count = category_counts["failed"]
    acceptable_count = exact_count + structured_count + semantic_count
    route_changed_count = sum(int(record["route_changed"]) for record in records)
    acceptable_route_changed_count = sum(int(record["route_change_acceptable"]) for record in records)

    records_by_route: dict[str, list[dict[str, Any]]] = {route: [] for route in ROUTES}
    for record in records:
        route = record["krk_route"]
        if route in records_by_route:
            records_by_route[route].append(record)

    return {
        "schema_version": "krk_output_fidelity_evaluation_v0",
        "final_classification": FINAL_CLASSIFICATION,
        "claim_level": CLAIM_LEVEL,
        "execution_mode": "local_deterministic_fixture_rule_based",
        "comparison_categories": list(COMPARISON_CATEGORIES),
        "total_evaluated_items": total,
        "baseline_success_count": baseline_success_count,
        "krk_success_count": krk_success_count,
        "exact_match_count": exact_count,
        "structured_equivalent_count": structured_count,
        "semantic_equivalent_count": semantic_count,
        "degraded_count": degraded_count,
        "failed_count": failed_count,
        "metrics": {
            "exact_match_rate": _rate(exact_count, total),
            "acceptable_output_rate": _rate(acceptable_count, total),
            "degradation_rate": _rate(degraded_count, total),
            "failure_rate": _rate(failed_count, total),
        },
        "baseline_vs_krk_delta": {
            "route_changed_count": route_changed_count,
            "route_changed_acceptable_count": acceptable_route_changed_count,
            "route_changed_degraded_count": route_changed_count - acceptable_route_changed_count,
            "baseline_success_minus_krk_success": baseline_success_count - krk_success_count,
            "output_failures_added_by_krk": max(failed_count - len(errors), 0),
        },
        "profile_counts": dict(profile_counts),
        "per_route_summary": {
            route: _route_summary(route, route_records)
            for route, route_records in records_by_route.items()
        },
        "sources": sources,
        "item_results": records,
        "errors": errors,
        "live_execution": {
            "provider_calls_performed": False,
            "gpu_execution_performed": False,
            "semantic_model_judge_used": False,
        },
        "methodology": {
            "baseline_definition": "public fixture oracle expected route and deterministic expected output contract",
            "krk_routed_output_definition": "KRK dry-run route decision mapped to a deterministic public output contract",
            "comparison_rule": (
                "exact_match requires the same expected and KRK route; structured_equivalent "
                "requires a different KRK route that is listed as acceptable by the public oracle; "
                "semantic_equivalent_stubbed_or_rule_based is reserved and remains zero without a model judge."
            ),
        },
        "reproducibility": {
            "repo_commit": repo_commit_value if repo_commit_value is not None else repo_commit(),
            "command": command or "",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _format_metric(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def render_markdown_summary(result: dict[str, Any]) -> str:
    route_rows = [
        "| {route} | {total} | {exact_match_count} | {structured_equivalent_count} | "
        "{semantic_equivalent_count} | {degraded_count} | {failed_count} | {acceptable_output_rate:.4f} |".format(
            **summary
        )
        for summary in result["per_route_summary"].values()
    ]
    source_rows = [
        f"| `{source['profile_id']}` | `{source['matrix_file']}` | `{source['item_count']}` |"
        for source in result["sources"]
    ]
    metrics = result["metrics"]
    lines = [
        "# KRK Output Fidelity Summary v0",
        "",
        "Status: generated baseline-equivalence and output-fidelity evidence.",
        "",
        "This summary compares deterministic public fixture baseline outputs with KRK-routed outputs using rule-based comparison only. It does not use provider calls, GPU execution, private logs, or a semantic model judge.",
        "",
        "## Run Summary",
        "",
        f"- final classification: `{result['final_classification']}`",
        f"- claim level: `{result['claim_level']}`",
        f"- execution mode: `{result['execution_mode']}`",
        f"- total evaluated items: `{result['total_evaluated_items']}`",
        f"- baseline success count: `{result['baseline_success_count']}`",
        f"- KRK success count: `{result['krk_success_count']}`",
        f"- exact match count: `{result['exact_match_count']}`",
        f"- structured equivalent count: `{result['structured_equivalent_count']}`",
        f"- semantic equivalent count: `{result['semantic_equivalent_count']}`",
        f"- degraded count: `{result['degraded_count']}`",
        f"- failed count: `{result['failed_count']}`",
        f"- exact match rate: `{_format_metric(metrics['exact_match_rate'])}`",
        f"- acceptable output rate: `{_format_metric(metrics['acceptable_output_rate'])}`",
        f"- degradation rate: `{_format_metric(metrics['degradation_rate'])}`",
        f"- failure rate: `{_format_metric(metrics['failure_rate'])}`",
        "",
        "## Workload Sources",
        "",
        "| Profile | Matrix file | Items |",
        "| --- | --- | ---: |",
        *source_rows,
        "",
        "## Per-Route Fidelity",
        "",
        "| KRK route | Total | Exact | Structured equivalent | Semantic equivalent | Degraded | Failed | Acceptable output rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        *route_rows,
        "",
        "## Baseline vs KRK Delta",
        "",
        f"- route changed count: `{result['baseline_vs_krk_delta']['route_changed_count']}`",
        f"- acceptable route changed count: `{result['baseline_vs_krk_delta']['route_changed_acceptable_count']}`",
        f"- route changed degraded count: `{result['baseline_vs_krk_delta']['route_changed_degraded_count']}`",
        f"- baseline success minus KRK success: `{result['baseline_vs_krk_delta']['baseline_success_minus_krk_success']}`",
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
    parser = argparse.ArgumentParser(description="Evaluate KRK baseline equivalence and output fidelity.")
    parser.add_argument("--matrix", action="append", required=True, help="KRK matrix JSON fixture path")
    parser.add_argument("--json-out", required=True, help="output path for JSON summary")
    parser.add_argument("--md-out", required=True, help="output path for Markdown summary")
    parser.add_argument("--repo-commit", help="override repo commit metadata")
    args = parser.parse_args(argv)

    command = "python3 scripts/run_krk_output_fidelity.py " + " ".join(
        [f"--matrix {path}" for path in args.matrix]
    )
    command = f"{command} --json-out {args.json_out} --md-out {args.md_out}"
    if args.repo_commit:
        command = f"{command} --repo-commit {args.repo_commit}"
    result = evaluate_output_fidelity(
        [Path(path) for path in args.matrix],
        command=command,
        repo_commit_value=args.repo_commit,
    )
    write_outputs(result, json_out=Path(args.json_out), md_out=Path(args.md_out))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
