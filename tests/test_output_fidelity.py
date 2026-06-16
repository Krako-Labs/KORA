from __future__ import annotations

import json
from pathlib import Path

from kora.output_fidelity import (
    CLAIM_BOUNDARY,
    CLAIM_LEVEL,
    FINAL_CLASSIFICATION,
    compare_outputs,
    evaluate_output_fidelity,
    main,
    render_markdown_summary,
)
from kora.matrix_evaluator import load_matrix


MATRIX_PATHS = [
    Path("examples/workloads/krk-mixed-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-cache-heavy-routing-matrix-alpha.json"),
    Path("examples/workloads/krk-adversarial-routing-matrix-alpha.json"),
]


def _item_by_request_id(request_id: str) -> dict:
    for path in MATRIX_PATHS:
        for item in load_matrix(path)["items"]:
            if item["request_id"] == request_id:
                return item
    raise AssertionError(f"missing fixture item: {request_id}")


def test_compare_outputs_marks_exact_match_for_same_route() -> None:
    record = compare_outputs(_item_by_request_id("mixed-001"))

    assert record["comparison_category"] == "exact_match"
    assert record["fidelity_status"] == "acceptable"
    assert record["baseline_route"] == "deterministic"
    assert record["krk_route"] == "deterministic"
    assert record["provider_call_performed"] is False
    assert record["gpu_execution_performed"] is False


def test_compare_outputs_marks_structured_equivalence_for_acceptable_route_change() -> None:
    record = compare_outputs(_item_by_request_id("adv-003"))

    assert record["comparison_category"] == "structured_equivalent"
    assert record["fidelity_status"] == "acceptable"
    assert record["baseline_route"] == "CPU"
    assert record["krk_route"] == "provider"
    assert record["route_changed"] is True
    assert record["route_change_acceptable"] is True
    assert record["semantic_model_judge_used"] is False


def test_evaluate_output_fidelity_aggregates_public_profiles() -> None:
    result = evaluate_output_fidelity(MATRIX_PATHS, repo_commit_value="test-commit")

    assert result["schema_version"] == "krk_output_fidelity_evaluation_v0"
    assert result["final_classification"] == FINAL_CLASSIFICATION
    assert result["claim_level"] == CLAIM_LEVEL
    assert result["total_evaluated_items"] == 18
    assert result["baseline_success_count"] == 18
    assert result["krk_success_count"] == 18
    assert result["exact_match_count"] == 17
    assert result["structured_equivalent_count"] == 1
    assert result["semantic_equivalent_count"] == 0
    assert result["degraded_count"] == 0
    assert result["failed_count"] == 0
    assert result["metrics"]["exact_match_rate"] == 17 / 18
    assert result["metrics"]["acceptable_output_rate"] == 1.0
    assert result["metrics"]["degradation_rate"] == 0.0
    assert result["metrics"]["failure_rate"] == 0.0
    assert result["baseline_vs_krk_delta"]["route_changed_count"] == 1
    assert result["baseline_vs_krk_delta"]["route_changed_acceptable_count"] == 1
    assert result["per_route_summary"]["provider"]["structured_equivalent_count"] == 1
    assert result["per_route_summary"]["fallback"]["exact_match_count"] == 4
    assert result["live_execution"]["provider_calls_performed"] is False
    assert result["live_execution"]["gpu_execution_performed"] is False
    assert "oracle_labels" not in json.dumps(result["item_results"])


def test_render_markdown_summary_includes_reviewer_boundary() -> None:
    result = evaluate_output_fidelity(MATRIX_PATHS, repo_commit_value="test-commit")
    markdown = render_markdown_summary(result)

    assert "# KRK Output Fidelity Summary v0" in markdown
    assert "Per-Route Fidelity" in markdown
    assert "semantic model judge" in markdown
    assert CLAIM_BOUNDARY in markdown
    assert "production cost reduction" in markdown


def test_output_fidelity_cli_writes_json_and_markdown(tmp_path: Path) -> None:
    json_out = tmp_path / "fidelity.json"
    md_out = tmp_path / "fidelity.md"
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
    assert saved["final_classification"] == FINAL_CLASSIFICATION
    assert saved["total_evaluated_items"] == 18
    assert "# KRK Output Fidelity Summary v0" in markdown
