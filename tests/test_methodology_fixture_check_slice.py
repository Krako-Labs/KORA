from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.evaluate_methodology_fixture_checks import (
    DEFAULT_FIXTURE,
    evaluate_methodology_fixture_checks,
)


def test_methodology_fixture_check_slice_counts_public_safe_fixture() -> None:
    summary = evaluate_methodology_fixture_checks(DEFAULT_FIXTURE)

    assert summary["ok"] is True
    assert summary["total_items"] == 14
    assert summary["checked_items"] == 12
    assert summary["passed_checks"] == 12
    assert summary["failed_checks"] == 0
    assert summary["skipped_items"] == 2
    assert summary["check_type_counts"] == {
        "exact_list": 2,
        "exact_number": 2,
        "exact_object": 2,
        "exact_string": 2,
        "field_schema": 2,
        "required_keys": 2,
    }
    assert summary["claim_scope"] == "fixture_only"
    assert summary["public_safe"] is True


def test_methodology_fixture_check_slice_cli_outputs_deterministic_json() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_methodology_fixture_checks.py",
            "--fixture",
            str(DEFAULT_FIXTURE),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    summary = json.loads(completed.stdout)
    assert list(summary["check_type_counts"]) == [
        "exact_list",
        "exact_number",
        "exact_object",
        "exact_string",
        "field_schema",
        "required_keys",
    ]
    assert summary["checked_items"] == 12
    assert summary["failures"] == []
    assert "does_not_call_providers" in summary["non_claims"]
    assert "does_not_prove_output_quality" in summary["non_claims"]


def test_methodology_fixture_check_slice_cli_reports_actionable_failure(tmp_path: Path) -> None:
    fixture = json.loads(DEFAULT_FIXTURE.read_text(encoding="utf-8"))
    fixture["items"][4]["observed_output"] = {"ticket_id": "ticket-005"}
    failed_fixture = tmp_path / "failed-methodology-fixture.json"
    failed_fixture.write_text(json.dumps(fixture), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_methodology_fixture_checks.py",
            "--fixture",
            str(failed_fixture),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    summary = json.loads(completed.stdout)
    assert summary["ok"] is False
    assert summary["failed_checks"] == 1
    assert summary["failures"][0]["id"] == "methodology-check-005"
    assert "missing required keys" in summary["failures"][0]["reason"]
    assert "priority" in summary["failures"][0]["reason"]


def test_methodology_fixture_check_slice_cli_fails_on_malformed_fixture(tmp_path: Path) -> None:
    fixture = json.loads(DEFAULT_FIXTURE.read_text(encoding="utf-8"))
    del fixture["items"][0]["public_safe"]
    malformed_fixture = tmp_path / "malformed-methodology-fixture.json"
    malformed_fixture.write_text(json.dumps(fixture), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_methodology_fixture_checks.py",
            "--fixture",
            str(malformed_fixture),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    summary = json.loads(completed.stdout)
    assert summary["ok"] is False
    assert "missing fields" in summary["error"]
