from __future__ import annotations

import json
from pathlib import Path

import pytest

from kora.matrix_evaluator import evaluate_matrix, load_matrix, main, render_markdown_summary


MIXED_MATRIX = Path("examples/workloads/krk-mixed-routing-matrix-alpha.json")


def test_load_matrix_accepts_existing_fixture() -> None:
    matrix = load_matrix(MIXED_MATRIX)

    assert matrix["schema_version"] == "krk_routing_matrix_alpha_v0"
    assert matrix["profile_id"] == "mixed-realistic"
    assert len(matrix["items"]) == 6


def test_load_matrix_rejects_invalid_schema(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"schema_version": "wrong", "profile_id": "x", "items": []}), encoding="utf-8")

    with pytest.raises(ValueError, match="unsupported schema_version"):
        load_matrix(path)


def test_evaluate_matrix_returns_public_safe_metrics() -> None:
    result = evaluate_matrix(MIXED_MATRIX, policy_id="KRK")

    assert result["schema_version"] == "krk_route_metrics_v0"
    assert result["profile_id"] == "mixed-realistic"
    assert result["policy_id"] == "KRK"
    assert result["policy_version"] == "krk_dry_run_v0"
    assert result["total_requests"] == 6
    assert set(result["route_counts"]) == {"deterministic", "cache", "CPU", "provider", "GPU", "fallback"}
    assert "oracle_labels" not in json.dumps(result["items"])
    assert result["metrics"]["error_count"] == 0
    assert result["claim_level"] == "dry_run_route_selectivity"


def test_render_markdown_summary_includes_claim_boundary() -> None:
    result = evaluate_matrix(MIXED_MATRIX, policy_id="KRK")
    markdown = render_markdown_summary(result)

    assert "# KRK Route-Selectivity Metrics - mixed-realistic" in markdown
    assert "| `exact_route_accuracy` |" in markdown
    assert "does not require GPU access or provider calls" in markdown
    assert "does not claim production" in markdown


def test_matrix_evaluator_cli_writes_json_and_markdown(tmp_path: Path) -> None:
    json_out = tmp_path / "metrics.json"
    md_out = tmp_path / "metrics.md"

    exit_code = main([
        "--matrix",
        str(MIXED_MATRIX),
        "--json-out",
        str(json_out),
        "--md-out",
        str(md_out),
    ])

    assert exit_code == 0
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    markdown = md_out.read_text(encoding="utf-8")
    assert saved["profile_id"] == "mixed-realistic"
    assert saved["metrics"]["error_count"] == 0
    assert "# KRK Route-Selectivity Metrics - mixed-realistic" in markdown
