"""Five-minute first-value workflow for public-safe KORA/KRK evidence."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from kora.matrix_evaluator import load_matrix, repo_commit
from kora.output_fidelity import evaluate_output_fidelity
from kora.route_selectivity_metrics import ROUTES
from kora.runtime_route_evaluator import evaluate_runtime_routes

CLAIM_LEVEL = "five_minute_first_value_public_safe_demo"
FINAL_CLASSIFICATION = "FIVE_MINUTE_FIRST_VALUE_PATH_MEASURED"
DEFAULT_MATRIX_PATHS = [
    Path("examples/workloads/krk-mixed-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-cache-heavy-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-adversarial-routing-matrix-alpha.json"),
]
CLAIM_BOUNDARY = (
    "Five-minute first-value workflow evidence only. This output demonstrates a local "
    "inspect, compare, run, and report path over committed public fixtures. It does not "
    "claim production adoption, production readiness, production cost reduction, customer "
    "savings, provider superiority, H100 superiority, broad workload superiority, or real "
    "API/GPU cost reduction."
)


def _rate(count: int, total: int) -> float:
    return count / total if total else 0.0


def _profile_sources(matrix_paths: list[Path]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for matrix_path in matrix_paths:
        matrix = load_matrix(matrix_path)
        sources.append(
            {
                "profile_id": str(matrix["profile_id"]),
                "matrix_file": matrix_path.as_posix(),
                "item_count": len(matrix["items"]),
                "description": str(matrix.get("description", "")),
            }
        )
    return sources


def _build_inspect_step(matrix_paths: list[Path]) -> dict[str, Any]:
    sources = _profile_sources(matrix_paths)
    return {
        "step_id": "inspect",
        "title": "Inspect available KORA execution paths",
        "status": "completed",
        "available_execution_paths": list(ROUTES),
        "routable_workload_profiles": [source["profile_id"] for source in sources],
        "total_fixture_items": sum(int(source["item_count"]) for source in sources),
        "environment_summary": {
            "python_version": platform.python_version(),
            "provider_credentials_required": False,
            "gpu_required": False,
            "network_required": False,
            "execution_mode": "local_public_fixture_dry_run",
        },
    }


def _build_compare_step(runtime_result: dict[str, Any]) -> dict[str, Any]:
    total = int(runtime_result["total_requests"])
    route_counts = dict(runtime_result["route_counts"])
    non_provider_gpu_routes = ("deterministic", "cache", "CPU", "fallback")
    local_or_guardrail_count = sum(int(route_counts.get(route, 0)) for route in non_provider_gpu_routes)
    provider_or_gpu_count = int(route_counts.get("provider", 0)) + int(route_counts.get("GPU", 0))
    return {
        "step_id": "compare",
        "title": "Compare direct path with KRK-routed path",
        "status": "completed",
        "direct_path": {
            "description": "single model-candidate path for every public fixture item",
            "candidate_invocations": total,
        },
        "krk_routed_path": {
            "route_counts": route_counts,
            "provider_or_gpu_route_count": provider_or_gpu_count,
            "local_or_guardrail_route_count": local_or_guardrail_count,
        },
        "avoided_execution_opportunities": {
            "count": local_or_guardrail_count,
            "rate": _rate(local_or_guardrail_count, total),
            "definition": "items routed to deterministic, cache, CPU, or fallback paths instead of provider/GPU-class paths",
        },
    }


def _build_run_step(runtime_result: dict[str, Any]) -> dict[str, Any]:
    metrics = runtime_result["metrics"]
    return {
        "step_id": "run",
        "title": "Run public-safe KRK fixture workflow",
        "status": "completed",
        "total_requests": runtime_result["total_requests"],
        "route_counts": runtime_result["route_counts"],
        "executor_counts": runtime_result["executor_counts"],
        "dry_run_execution_success_rate": metrics["dry_run_execution_success_rate"],
        "unsafe_misroute_rate": metrics["unsafe_misroute_rate"],
        "error_count": metrics["error_count"],
        "provider_calls_performed": runtime_result["provider_calls_performed"],
        "gpu_execution_performed": runtime_result["gpu_execution_performed"],
    }


def _build_report_step(output_fidelity_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "step_id": "report",
        "title": "Generate route and output-fidelity summary",
        "status": "completed",
        "total_evaluated_items": output_fidelity_result["total_evaluated_items"],
        "exact_match_count": output_fidelity_result["exact_match_count"],
        "structured_equivalent_count": output_fidelity_result["structured_equivalent_count"],
        "degraded_count": output_fidelity_result["degraded_count"],
        "failed_count": output_fidelity_result["failed_count"],
        "acceptable_output_rate": output_fidelity_result["metrics"]["acceptable_output_rate"],
    }


def build_five_minute_first_value(
    matrix_paths: list[Path] | None = None,
    *,
    command: str | None = None,
    repo_commit_value: str | None = None,
) -> dict[str, Any]:
    paths = matrix_paths or DEFAULT_MATRIX_PATHS
    runtime_result = evaluate_runtime_routes(paths, repo_commit_value=repo_commit_value)
    output_fidelity_result = evaluate_output_fidelity(paths, repo_commit_value=repo_commit_value)
    steps = [
        _build_inspect_step(paths),
        _build_compare_step(runtime_result),
        _build_run_step(runtime_result),
        _build_report_step(output_fidelity_result),
    ]
    route_counts = dict(runtime_result["route_counts"])
    profile_counts = Counter()
    for source in _profile_sources(paths):
        profile_counts[source["profile_id"]] += int(source["item_count"])

    return {
        "schema_version": "krk_five_minute_first_value_v0",
        "final_classification": FINAL_CLASSIFICATION,
        "claim_level": CLAIM_LEVEL,
        "workflow_name": "KORA Five-Minute First Value Path",
        "first_value_definition": "fresh clone to local inspect, compare, run, and report over public fixtures",
        "step_count": len(steps),
        "commands_required": 1,
        "required_user_decisions": 0,
        "estimated_time_to_first_value_minutes": 5,
        "estimated_time_to_first_value_label": "approximately five minutes",
        "works_without_provider_credentials": True,
        "works_without_gpu": True,
        "network_required": False,
        "total_fixture_items": runtime_result["total_requests"],
        "route_counts": route_counts,
        "profile_counts": dict(profile_counts),
        "onboarding_metrics": {
            "step_count": len(steps),
            "commands_required": 1,
            "required_user_decisions": 0,
            "estimated_time_to_first_value_minutes": 5,
            "generated_outputs": 2,
        },
        "evidence_summary": {
            "runtime_total_requests": runtime_result["total_requests"],
            "dry_run_execution_success_rate": runtime_result["metrics"]["dry_run_execution_success_rate"],
            "unsafe_misroute_rate": runtime_result["metrics"]["unsafe_misroute_rate"],
            "output_total_evaluated_items": output_fidelity_result["total_evaluated_items"],
            "output_exact_match_count": output_fidelity_result["exact_match_count"],
            "output_structured_equivalent_count": output_fidelity_result["structured_equivalent_count"],
            "output_degraded_count": output_fidelity_result["degraded_count"],
            "output_failed_count": output_fidelity_result["failed_count"],
            "acceptable_output_rate": output_fidelity_result["metrics"]["acceptable_output_rate"],
        },
        "steps": steps,
        "generated_outputs": {
            "json_summary": "docs/evidence/generated/krk-goal070a-five-minute-first-value-summary-v0.json",
            "markdown_summary": "docs/evidence/generated/krk-goal070a-five-minute-first-value-summary-v0.md",
        },
        "source": {
            "matrix_files": [path.as_posix() for path in paths],
            "reuse": [
                "kora.runtime_route_evaluator.evaluate_runtime_routes",
                "kora.output_fidelity.evaluate_output_fidelity",
            ],
        },
        "reproducibility": {
            "repo_commit": repo_commit_value if repo_commit_value is not None else repo_commit(),
            "command": command or "",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def render_markdown_summary(result: dict[str, Any]) -> str:
    route_rows = [
        f"| `{route}` | `{count}` |"
        for route, count in result["route_counts"].items()
    ]
    step_rows = [
        f"| `{step['step_id']}` | {step['title']} | `{step['status']}` |"
        for step in result["steps"]
    ]
    lines = [
        "# KORA Five-Minute First Value Summary v0",
        "",
        "Status: generated public-safe first-value workflow summary.",
        "",
        "This summary records a local inspect, compare, run, and report workflow over committed public KRK fixtures. It requires no provider credentials, no GPU, and no network access.",
        "",
        "## First-Value Metrics",
        "",
        f"- final classification: `{result['final_classification']}`",
        f"- claim level: `{result['claim_level']}`",
        f"- step count: `{result['step_count']}`",
        f"- commands required: `{result['commands_required']}`",
        f"- required user decisions: `{result['required_user_decisions']}`",
        f"- estimated time to first value: `{result['estimated_time_to_first_value_label']}`",
        f"- works without provider credentials: `{str(result['works_without_provider_credentials']).lower()}`",
        f"- works without GPU: `{str(result['works_without_gpu']).lower()}`",
        f"- network required: `{str(result['network_required']).lower()}`",
        "",
        "## Workflow Steps",
        "",
        "| Step | Purpose | Status |",
        "| --- | --- | --- |",
        *step_rows,
        "",
        "## Route Summary",
        "",
        "| Route | Count |",
        "| --- | ---: |",
        *route_rows,
        "",
        "## Evidence Summary",
        "",
        f"- runtime total requests: `{result['evidence_summary']['runtime_total_requests']}`",
        f"- dry-run execution success rate: `{result['evidence_summary']['dry_run_execution_success_rate']:.4f}`",
        f"- unsafe misroute rate: `{result['evidence_summary']['unsafe_misroute_rate']:.4f}`",
        f"- output exact match count: `{result['evidence_summary']['output_exact_match_count']}`",
        f"- output structured equivalent count: `{result['evidence_summary']['output_structured_equivalent_count']}`",
        f"- output degraded count: `{result['evidence_summary']['output_degraded_count']}`",
        f"- output failed count: `{result['evidence_summary']['output_failed_count']}`",
        f"- acceptable output rate: `{result['evidence_summary']['acceptable_output_rate']:.4f}`",
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
    parser = argparse.ArgumentParser(description="Run the KORA five-minute first-value workflow.")
    parser.add_argument("--matrix", action="append", help="KRK matrix JSON fixture path")
    parser.add_argument("--json-out", required=True, help="output path for JSON summary")
    parser.add_argument("--md-out", required=True, help="output path for Markdown summary")
    parser.add_argument("--repo-commit", help="override repo commit metadata")
    args = parser.parse_args(argv)

    matrix_paths = [Path(path) for path in args.matrix] if args.matrix else DEFAULT_MATRIX_PATHS
    command = "python3 scripts/kora_five_minute_demo.py "
    if args.matrix:
        command += " ".join(f"--matrix {path}" for path in args.matrix) + " "
    command += f"--json-out {args.json_out} --md-out {args.md_out}"
    if args.repo_commit:
        command += f" --repo-commit {args.repo_commit}"

    result = build_five_minute_first_value(
        matrix_paths,
        command=command,
        repo_commit_value=args.repo_commit,
    )
    write_outputs(result, json_out=Path(args.json_out), md_out=Path(args.md_out))
    print(render_markdown_summary(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
