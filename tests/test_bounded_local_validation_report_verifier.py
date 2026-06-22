from __future__ import annotations

import json
from pathlib import Path

from scripts import verify_bounded_local_validation_report as verifier
from scripts.run_bounded_local_validation import REPORT_SCHEMA


APPROVED_COMMANDS = [
    ["python3", "scripts/evaluate_fixture_quality_checks.py"],
    ["python3", "-m", "pytest", "tests/test_fixture_quality_checks.py"],
    [
        "python3",
        "-m",
        "pytest",
        "tests/test_representativeness_seed.py",
        "tests/test_representativeness_route_only_evaluator.py",
    ],
    ["python3", "scripts/check_markdown_links_goal082b.py"],
    ["git", "diff", "--check"],
    ["python3", "-m", "pytest"],
]


def _report(status: str = "passed", final_status: str = "passed") -> dict:
    return {
        "report_schema": REPORT_SCHEMA,
        "profile": "kora-local-core",
        "final_status": final_status,
        "repo_root": "/repo",
        "steps": [
            {
                "name": f"step {index}",
                "command": command,
                "return_code": 0 if status != "skipped/dry-run" else None,
                "status": status,
            }
            for index, command in enumerate(APPROVED_COMMANDS, 1)
        ],
    }


def _write_json(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "report.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_valid_passed_report_verifies_successfully() -> None:
    errors = verifier.verify_report(_report(), "kora-local-core")

    assert errors == []


def test_valid_dry_run_report_verifies_successfully() -> None:
    report = _report(status="skipped/dry-run", final_status="dry-run")

    errors = verifier.verify_report(report, "kora-local-core")

    assert errors == []


def test_unknown_profile_fails() -> None:
    errors = verifier.verify_report(_report(), "unknown-profile")

    assert errors
    assert "unsupported profile" in errors[0]


def test_missing_top_level_field_fails() -> None:
    report = _report()
    del report["steps"]

    errors = verifier.verify_report(report, "kora-local-core")

    assert "missing top-level field: steps" in errors


def test_command_list_mismatch_fails() -> None:
    report = _report()
    report["steps"][2]["command"] = ["python3", "-m", "pytest"]

    errors = verifier.verify_report(report, "kora-local-core")

    assert any("command mismatch" in error for error in errors)


def test_invalid_status_fails() -> None:
    report = _report()
    report["steps"][0]["status"] = "unknown"

    errors = verifier.verify_report(report, "kora-local-core")

    assert any("invalid status" in error for error in errors)


def test_failed_report_fails_by_default() -> None:
    report = _report()
    report["final_status"] = "failed"
    report["steps"][1]["status"] = "failed"
    report["steps"][1]["return_code"] = 2

    errors = verifier.verify_report(report, "kora-local-core")

    assert any("--allow-failed" in error for error in errors)


def test_failed_report_passes_with_allow_failed() -> None:
    report = _report()
    report["final_status"] = "failed"
    report["steps"][1]["status"] = "failed"
    report["steps"][1]["return_code"] = 2

    errors = verifier.verify_report(report, "kora-local-core", allow_failed=True)

    assert errors == []


def test_malformed_json_fails(tmp_path: Path) -> None:
    path = tmp_path / "malformed.json"
    path.write_text("{", encoding="utf-8")

    report, errors = verifier._load_report(path)

    assert report is None
    assert errors
    assert "invalid JSON" in errors[0]


def test_verifier_rejects_arbitrary_or_unsupported_profiles() -> None:
    report = _report()
    report["profile"] = "shell-anything"

    errors = verifier.verify_report(report, "shell-anything")

    assert errors
    assert "unsupported profile" in errors[0]


def test_cli_success_and_failure_paths(tmp_path: Path, capsys) -> None:
    valid = _write_json(tmp_path, _report())
    assert verifier.main([str(valid), "--profile", "kora-local-core"]) == 0
    assert "passed:" in capsys.readouterr().out

    invalid = _write_json(tmp_path, {"profile": "kora-local-core"})
    assert verifier.main([str(invalid), "--profile", "kora-local-core"]) == 1
    assert "failed:" in capsys.readouterr().out
