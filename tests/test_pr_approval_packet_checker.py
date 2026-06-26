from __future__ import annotations

import json
from pathlib import Path

from scripts import check_pr_approval_packet as checker


VALID_PACKET = """# Report

Decision needed: review and decide whether to merge.
Risk level: low.
Final status classification: `merge-ready`.
Changed files: scripts/check.py and tests/test_check.py.
Validation summary: all checks passed.
Repair attempts: 0.
Failures encountered: none.
Self-review summary: scope and boundaries checked.
Claim-boundary audit: no output-quality proof or production proof added.
Forbidden-action audit: no provider calls, no report-command execution, no releases.
Uncertainty notes: none.
workflow recommendation: Merge.
Albert action options: Merge / Request R1 / Stop / CTO Review.
"""


def _write(tmp_path: Path, text: str = VALID_PACKET) -> Path:
    path = tmp_path / "packet.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_packet_passes() -> None:
    result = checker.validate_packet(VALID_PACKET)

    assert result["ok"] is True
    assert result["risk_level"] == "low"
    assert result["final_status_classification"] == "merge-ready"


def test_missing_required_field_fails() -> None:
    text = VALID_PACKET.replace("Decision needed: review and decide whether to merge.\n", "")

    result = checker.validate_packet(text)

    assert result["ok"] is False
    assert "missing required field: decision needed" in result["errors"]


def test_invalid_final_status_fails() -> None:
    text = VALID_PACKET.replace("`merge-ready`", "`done`")

    result = checker.validate_packet(text)

    assert result["ok"] is False
    assert "invalid final status classification: `done`." in result["errors"]


def test_invalid_risk_level_fails() -> None:
    text = VALID_PACKET.replace("Risk level: low.", "Risk level: urgent.")

    result = checker.validate_packet(text)

    assert result["ok"] is False
    assert "invalid risk level: urgent." in result["errors"]


def test_missing_albert_action_options_fails() -> None:
    text = VALID_PACKET.replace("Merge / Request R1 / Stop / CTO Review", "Merge / Stop")

    result = checker.validate_packet(text)

    assert result["ok"] is False
    assert "missing Albert action option: Request R1" in result["errors"]
    assert "missing Albert action option: CTO Review" in result["errors"]


def test_missing_claim_boundary_audit_fails() -> None:
    text = VALID_PACKET.replace(
        "Claim-boundary audit: no output-quality proof or production proof added.\n",
        "",
    )

    result = checker.validate_packet(text)

    assert result["ok"] is False
    assert "missing required field: claim-boundary audit" in result["errors"]


def test_json_output_works(tmp_path: Path) -> None:
    packet_path = _write(tmp_path)
    json_out = tmp_path / "packet-check.json"

    exit_code = checker.main([str(packet_path), "--json-out", str(json_out)])

    data = json.loads(json_out.read_text(encoding="utf-8"))
    assert exit_code == 0
    assert data["ok"] is True
    assert data["final_status_classification"] == "merge-ready"


def test_require_merge_ready_fails_for_other_status() -> None:
    text = VALID_PACKET.replace("`merge-ready`", "`needs-cto-review`")

    result = checker.validate_packet(text, require_merge_ready=True)

    assert result["ok"] is False
    assert "--require-merge-ready requires final status classification: merge-ready" in result["errors"]


def test_checker_does_not_mutate_files(tmp_path: Path) -> None:
    packet_path = _write(tmp_path)
    before = packet_path.read_text(encoding="utf-8")

    assert checker.main([str(packet_path)]) == 0

    assert packet_path.read_text(encoding="utf-8") == before
