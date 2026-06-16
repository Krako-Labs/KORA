from __future__ import annotations

import json
from pathlib import Path

from kora.five_minute_first_value import (
    CLAIM_BOUNDARY,
    FINAL_CLASSIFICATION,
    build_five_minute_first_value,
    main,
    render_markdown_summary,
)


def test_build_five_minute_first_value_runs_without_provider_or_gpu() -> None:
    result = build_five_minute_first_value(repo_commit_value="test-commit")

    assert result["schema_version"] == "krk_five_minute_first_value_v0"
    assert result["final_classification"] == FINAL_CLASSIFICATION
    assert result["step_count"] == 4
    assert result["commands_required"] == 1
    assert result["required_user_decisions"] == 0
    assert result["works_without_provider_credentials"] is True
    assert result["works_without_gpu"] is True
    assert result["network_required"] is False
    assert result["total_fixture_items"] == 18
    assert result["route_counts"] == {
        "deterministic": 2,
        "cache": 3,
        "CPU": 2,
        "provider": 3,
        "GPU": 4,
        "fallback": 4,
    }
    assert result["evidence_summary"]["dry_run_execution_success_rate"] == 1.0
    assert result["evidence_summary"]["acceptable_output_rate"] == 1.0
    assert result["evidence_summary"]["output_exact_match_count"] == 17
    assert result["evidence_summary"]["output_structured_equivalent_count"] == 1


def test_compare_step_reports_avoided_execution_opportunities() -> None:
    result = build_five_minute_first_value(repo_commit_value="test-commit")
    compare_step = next(step for step in result["steps"] if step["step_id"] == "compare")

    assert compare_step["direct_path"]["candidate_invocations"] == 18
    assert compare_step["krk_routed_path"]["provider_or_gpu_route_count"] == 7
    assert compare_step["krk_routed_path"]["local_or_guardrail_route_count"] == 11
    assert compare_step["avoided_execution_opportunities"]["count"] == 11
    assert compare_step["avoided_execution_opportunities"]["rate"] == 11 / 18


def test_render_markdown_summary_includes_claim_boundary() -> None:
    result = build_five_minute_first_value(repo_commit_value="test-commit")
    markdown = render_markdown_summary(result)

    assert "# KORA Five-Minute First Value Summary v0" in markdown
    assert "inspect, compare, run, and report" in markdown
    assert "works without GPU: `true`" in markdown
    assert CLAIM_BOUNDARY in markdown
    assert "production adoption" in markdown


def test_five_minute_demo_cli_writes_report_files(tmp_path: Path) -> None:
    json_out = tmp_path / "first_value.json"
    md_out = tmp_path / "first_value.md"

    exit_code = main([
        "--json-out",
        str(json_out),
        "--md-out",
        str(md_out),
        "--repo-commit",
        "test-commit",
    ])

    assert exit_code == 0
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    markdown = md_out.read_text(encoding="utf-8")
    assert saved["final_classification"] == FINAL_CLASSIFICATION
    assert saved["onboarding_metrics"]["commands_required"] == 1
    assert "KORA Five-Minute First Value Summary" in markdown
