from __future__ import annotations

import json
from pathlib import Path

from kora.runtime_route_evaluator import (
    CLAIM_LEVEL,
    evaluate_runtime_routes,
    execute_dry_run_route,
    main,
    render_markdown_summary,
)
from kora.route_selectivity_metrics import RouteDecision, RouteRequest


MATRIX_PATHS = [
    Path("examples/workloads/krk-mixed-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-cache-heavy-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-adversarial-routing-matrix-alpha.json"),
]


def test_execute_dry_run_route_never_calls_provider_or_gpu() -> None:
    request = RouteRequest(
        request_id="req-1",
        workload_profile="test",
        workload_class="provider-like",
        router_visible_metadata={},
    )
    decision = RouteDecision("provider", "KRK", "krk_dry_run_v0", "test")

    record = execute_dry_run_route(request, decision)

    assert record["executor_id"] == "provider_dry_run_executor_v0"
    assert record["execution_status"] == "dry_run_success"
    assert record["provider_call_performed"] is False
    assert record["gpu_execution_performed"] is False


def test_evaluate_runtime_routes_aggregates_four_public_profiles() -> None:
    result = evaluate_runtime_routes(MATRIX_PATHS, repo_commit_value="test-commit")

    assert result["schema_version"] == "krk_runtime_integrated_route_evaluation_v0"
    assert result["claim_level"] == CLAIM_LEVEL
    assert result["total_requests"] == 18
    assert result["route_counts"] == {
        "deterministic": 2,
        "cache": 3,
        "CPU": 2,
        "provider": 3,
        "GPU": 4,
        "fallback": 4,
    }
    assert result["executor_counts"] == result["route_counts"]
    assert result["metrics"]["exact_route_accuracy"] == 17 / 18
    assert result["metrics"]["acceptable_route_rate"] == 1.0
    assert result["metrics"]["unsafe_misroute_rate"] == 0.0
    assert result["metrics"]["dry_run_execution_success_rate"] == 1.0
    assert result["metrics"]["evidence_records_created"] == 18
    assert result["metrics"]["error_count"] == 0
    assert result["provider_calls_performed"] is False
    assert result["gpu_execution_performed"] is False
    assert "oracle_labels" not in json.dumps(result["evidence_records"])


def test_render_markdown_summary_includes_runtime_workflow_boundary() -> None:
    result = evaluate_runtime_routes(MATRIX_PATHS, repo_commit_value="test-commit")
    markdown = render_markdown_summary(result)

    assert "# KRK Runtime-Integrated Route Evaluation v0" in markdown
    assert "route-specific dry-run executor" in markdown
    assert "No provider calls or GPU execution were performed." in markdown
    assert "production savings" in markdown


def test_runtime_route_evaluator_cli_writes_outputs(tmp_path: Path) -> None:
    json_out = tmp_path / "runtime.json"
    md_out = tmp_path / "runtime.md"
    argv: list[str] = []
    for matrix_path in MATRIX_PATHS:
        argv.extend(["--matrix", str(matrix_path)])
    argv.extend([
        "--json-out",
        str(json_out),
        "--md-out",
        str(md_out),
        "--repo-commit",
        "test-commit",
    ])

    exit_code = main(argv)

    assert exit_code == 0
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    markdown = md_out.read_text(encoding="utf-8")
    assert saved["claim_level"] == CLAIM_LEVEL
    assert saved["total_requests"] == 18
    assert "# KRK Runtime-Integrated Route Evaluation v0" in markdown
