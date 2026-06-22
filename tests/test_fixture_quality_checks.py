from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.evaluate_fixture_quality_checks import DEFAULT_FIXTURE, evaluate_quality_checks


def test_fixture_quality_checks_counts_public_safe_seed() -> None:
    summary = evaluate_quality_checks(DEFAULT_FIXTURE)

    assert summary["ok"] is True
    assert summary["total_items"] == 6
    assert summary["checked_items"] == 4
    assert summary["passed_checks"] == 4
    assert summary["failed_checks"] == 0
    assert summary["skipped_items"] == 1
    assert summary["gated_items"] == 1
    assert summary["check_type_counts"] == {
        "exact": 2,
        "schema": 1,
        "structured_equivalent": 1,
    }
    assert summary["claim_scope"] == "fixture_only"
    assert summary["public_safe"] is True


def test_fixture_quality_checks_cli_outputs_deterministic_json() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_fixture_quality_checks.py",
            "--fixture",
            str(DEFAULT_FIXTURE),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    summary = json.loads(completed.stdout)
    assert list(summary["check_type_counts"]) == ["exact", "schema", "structured_equivalent"]
    assert summary["checked_items"] == 4
    assert "does_not_call_providers" in summary["non_claims"]
    assert "does_not_prove_output_quality" in summary["non_claims"]


def test_fixture_quality_checks_cli_fails_on_failed_check(tmp_path: Path) -> None:
    fixture = json.loads(DEFAULT_FIXTURE.read_text(encoding="utf-8"))
    fixture["items"][0]["observed_output"] = "account_update"
    failed_fixture = tmp_path / "failed-quality-fixture.json"
    failed_fixture.write_text(json.dumps(fixture), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_fixture_quality_checks.py",
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


def test_fixture_quality_checks_cli_fails_on_malformed_fixture(tmp_path: Path) -> None:
    fixture = json.loads(DEFAULT_FIXTURE.read_text(encoding="utf-8"))
    del fixture["items"][0]["public_safe"]
    malformed_fixture = tmp_path / "malformed-quality-fixture.json"
    malformed_fixture.write_text(json.dumps(fixture), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_fixture_quality_checks.py",
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
