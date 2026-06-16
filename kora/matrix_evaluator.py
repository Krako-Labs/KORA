"""Dry-run evaluator for KRK route-selectivity matrix fixtures."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from kora.route_selectivity_metrics import CLAIM_BOUNDARY, POLICIES, evaluate_items


def load_matrix(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("matrix file must contain a JSON object")
    if data.get("schema_version") != "krk_routing_matrix_alpha_v0":
        raise ValueError("unsupported schema_version")
    if not isinstance(data.get("profile_id"), str):
        raise ValueError("matrix file missing profile_id")
    if not isinstance(data.get("items"), list):
        raise ValueError("matrix file missing items list")
    return data


def repo_commit() -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return completed.stdout.strip()


def evaluate_matrix(
    path: Path,
    *,
    policy_id: str = "KRK",
    command: str | None = None,
    repo_commit_value: str | None = None,
) -> dict[str, Any]:
    matrix = load_matrix(path)
    try:
        policy = POLICIES[policy_id]
    except KeyError as exc:
        available = ", ".join(sorted(POLICIES))
        raise ValueError(f"unknown policy {policy_id!r}; available policies: {available}") from exc

    result = evaluate_items(
        matrix["items"],
        profile_id=str(matrix["profile_id"]),
        policy=policy,
    )
    result["source"] = {
        "matrix_file": str(path.as_posix()),
        "schema_version": matrix["schema_version"],
        "description": matrix.get("description", ""),
    }
    result["reproducibility"] = {
        "repo_commit": repo_commit_value if repo_commit_value is not None else repo_commit(),
        "profile_file": str(path.as_posix()),
        "policy_id": result["policy_id"],
        "policy_version": result["policy_version"],
        "formula_version": "cwgd_v0",
        "command": command or "",
    }
    return result


def _format_metric(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def render_markdown_summary(result: dict[str, Any]) -> str:
    metrics = result["metrics"]
    route_rows = [
        f"| `{route}` | `{count}` |"
        for route, count in result["route_counts"].items()
    ]
    fallback_rows = [
        f"| `{kind}` | `{count}` |"
        for kind, count in result["fallback_counts"].items()
    ]
    metric_names = [
        "exact_route_accuracy",
        "acceptable_route_rate",
        "unsafe_misroute_rate",
        "gpu_false_positive_count",
        "gpu_false_negative_count",
        "cache_hit_correctness_rate",
        "safety_fallback_rate",
        "failure_fallback_rate",
        "error_count",
        "error_percentage",
        "compute_weighted_gpu_demand",
    ]
    metric_rows = [
        f"| `{name}` | `{_format_metric(metrics.get(name))}` |"
        for name in metric_names
    ]
    lines = [
        f"# KRK Route-Selectivity Metrics - {result['profile_id']}",
        "",
        "Status: dry-run route-selectivity evidence.",
        "",
        "This report evaluates route choices against independent oracle labels in committed matrix fixtures. It does not require GPU access or provider calls.",
        "",
        "## Run Metadata",
        "",
        f"- profile: `{result['profile_id']}`",
        f"- policy: `{result['policy_id']}`",
        f"- policy version: `{result['policy_version']}`",
        f"- total requests: `{result['total_requests']}`",
        f"- claim level: `{result['claim_level']}`",
        f"- source matrix: `{result['source']['matrix_file']}`",
        f"- repo commit: `{result['reproducibility']['repo_commit']}`",
        "",
        "## Route Distribution",
        "",
        "| Route | Count |",
        "| --- | ---: |",
        *route_rows,
        "",
        "## Correctness Metrics",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        *metric_rows,
        "",
        "## Fallback Metrics",
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
    parser = argparse.ArgumentParser(description="Evaluate KRK route-selectivity matrix fixtures.")
    parser.add_argument("--matrix", required=True, help="path to KRK matrix JSON fixture")
    parser.add_argument("--policy", default="KRK", choices=sorted(POLICIES), help="dry-run route policy")
    parser.add_argument("--json-out", required=True, help="output path for metrics JSON")
    parser.add_argument("--md-out", required=True, help="output path for Markdown summary")
    parser.add_argument("--repo-commit", help="override repo commit metadata for deterministic committed examples")
    args = parser.parse_args(argv)

    command = (
        "python3 -m kora.matrix_evaluator "
        f"--matrix {args.matrix} --policy {args.policy} "
        f"--json-out {args.json_out} --md-out {args.md_out}"
    )
    if args.repo_commit:
        command = f"{command} --repo-commit {args.repo_commit}"
    result = evaluate_matrix(
        Path(args.matrix),
        policy_id=args.policy,
        command=command,
        repo_commit_value=args.repo_commit,
    )
    write_outputs(result, json_out=Path(args.json_out), md_out=Path(args.md_out))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
