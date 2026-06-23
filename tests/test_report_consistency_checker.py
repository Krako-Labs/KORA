from __future__ import annotations

import json
from pathlib import Path

from scripts import check_report_consistency as checker


VALID_REPORT = """# Group 112 PR Approval and Report Consistency

## Base And Branch

- branch: `codex/group112-approval-report-consistency`
- PR: `https://github.com/Krako-Labs/KORA/pull/264`

## Risk And Final Classification

- risk level: low
- final status classification: `merge-ready`

## Validation Results

All validation passed.

## Approval Packet

Claim-boundary audit: no output-quality proof or production proof added.
Forbidden-action audit: no provider calls, no report-command execution, no releases.
"""

VALID_BREADCRUMB = """# Open This First

Group 112 current work.

- branch: `codex/group112-approval-report-consistency`
- open PR: [#264 Group 112](https://github.com/Krako-Labs/KORA/pull/264)
"""


def _write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_report_and_breadcrumbs_pass(tmp_path: Path) -> None:
    report = _write(tmp_path, "group112_report.md", VALID_REPORT)
    breadcrumb = _write(tmp_path, "OPEN_THIS_FIRST.md", VALID_BREADCRUMB)

    result = checker.validate_consistency(report, [breadcrumb])

    assert result["ok"] is True
    assert result["group_id"] == "Group 112"


def test_missing_report_id_fails(tmp_path: Path) -> None:
    report = _write(tmp_path, "group112_report.md", VALID_REPORT.replace("Group 112", "Group 999"))

    result = checker.validate_consistency(report, [])

    assert result["ok"] is False
    assert "report missing id: Group 112" in result["errors"]


def test_pr_mismatch_fails_when_present(tmp_path: Path) -> None:
    report = _write(tmp_path, "group112_report.md", VALID_REPORT)
    breadcrumb = _write(
        tmp_path,
        "REVIEW_HUB.md",
        VALID_BREADCRUMB.replace("/pull/264", "/pull/999"),
    )

    result = checker.validate_consistency(report, [breadcrumb])

    assert result["ok"] is False
    assert any("PR URL mismatch" in error for error in result["errors"])


def test_branch_mismatch_fails_when_present(tmp_path: Path) -> None:
    report = _write(tmp_path, "group112_report.md", VALID_REPORT)
    breadcrumb = _write(
        tmp_path,
        "OPEN_THIS_FIRST.md",
        VALID_BREADCRUMB.replace("codex/group112-approval-report-consistency", "codex/other"),
    )

    result = checker.validate_consistency(report, [breadcrumb])

    assert result["ok"] is False
    assert any("branch mismatch" in error for error in result["errors"])


def test_unrelated_current_branch_does_not_mismatch_historical_group(tmp_path: Path) -> None:
    report = _write(tmp_path, "group112_report.md", VALID_REPORT)
    breadcrumb = _write(
        tmp_path,
        "OPEN_THIS_FIRST.md",
        """# Open This First

- active verification branch: `codex/group113-next-work`

## History

Group 112 completed the consistency checker.
- branch: `codex/group112-approval-report-consistency`
- PR: https://github.com/Krako-Labs/KORA/pull/264
""",
    )

    result = checker.validate_consistency(report, [breadcrumb])

    assert result["ok"] is True


def test_missing_final_status_classification_fails(tmp_path: Path) -> None:
    report = _write(
        tmp_path,
        "group112_report.md",
        VALID_REPORT.replace("- final status classification: `merge-ready`\n", ""),
    )

    result = checker.validate_consistency(report, [])

    assert result["ok"] is False
    assert "report missing valid final status classification" in result["errors"]


def test_missing_validation_language_fails(tmp_path: Path) -> None:
    report = _write(
        tmp_path,
        "group112_report.md",
        VALID_REPORT.replace("## Validation Results\n\nAll validation passed.\n", ""),
    )

    result = checker.validate_consistency(report, [])

    assert result["ok"] is False
    assert "report missing validation results language" in result["errors"]


def test_missing_claim_boundary_language_fails(tmp_path: Path) -> None:
    report = _write(
        tmp_path,
        "group112_report.md",
        VALID_REPORT.replace("Claim-boundary audit: no output-quality proof or production proof added.\n", ""),
    )

    result = checker.validate_consistency(report, [])

    assert result["ok"] is False
    assert "report missing claim-boundary language" in result["errors"]


def test_json_output_works(tmp_path: Path) -> None:
    report = _write(tmp_path, "group112_report.md", VALID_REPORT)
    breadcrumb = _write(tmp_path, "OPEN_THIS_FIRST.md", VALID_BREADCRUMB)
    json_out = tmp_path / "consistency.json"

    exit_code = checker.main([str(report), "--breadcrumb", str(breadcrumb), "--json-out", str(json_out)])

    data = json.loads(json_out.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert data["ok"] is True
    assert data["pr_url"] == "https://github.com/Krako-Labs/KORA/pull/264"


def test_checker_does_not_mutate_files(tmp_path: Path) -> None:
    report = _write(tmp_path, "group112_report.md", VALID_REPORT)
    breadcrumb = _write(tmp_path, "OPEN_THIS_FIRST.md", VALID_BREADCRUMB)
    before_report = report.read_text(encoding="utf-8")
    before_breadcrumb = breadcrumb.read_text(encoding="utf-8")

    assert checker.main([str(report), "--breadcrumb", str(breadcrumb)]) == 0

    assert report.read_text(encoding="utf-8") == before_report
    assert breadcrumb.read_text(encoding="utf-8") == before_breadcrumb
