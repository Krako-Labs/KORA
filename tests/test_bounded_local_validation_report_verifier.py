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


def _report(status: str = "passed") -> dict:
    return {
        "report_schema": REPORT_SCHEMA,
        "profile": "kora-local-core",
        "final_status": status,
        "repo_root": "/tmp/kora",
        "steps": [
            {
                "name": f"step {index}",
                "command": command,
                "return_code": None if status == "dry-run" else 0,
                "status": "skipped/dry-run" if status == "dry-run" else "passed",
            }
            for index, command in enumerate(APPROVED_COMMANDS, start=1)
        ],
    }


def _write(tmp_path: Path, report: dict) -> Path:
    path = tmp_path / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return path


def test_valid_passed_report_verifies_successfully(tmp_path: Path) -> None:
    path = _write(tmp_path, _report("passed"))

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=False)

    assert ok is True
    assert errors == []


def test_valid_dry_run_report_verifies_successfully(tmp_path: Path) -> None:
    path = _write(tmp_path, _report("dry-run"))

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=False)

    assert ok is True
    assert errors == []


def test_unknown_profile_fails(tmp_path: Path) -> None:
    report = _report("passed")
    report["profile"] = "unknown"
    path = _write(tmp_path, report)

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=False)

    assert ok is False
    assert any("profile" in error for error in errors)


def test_missing_top_level_field_fails(tmp_path: Path) -> None:
    report = _report("passed")
    del report["steps"]
    path = _write(tmp_path, report)

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=False)

    assert ok is False
    assert any("missing top-level field" in error for error in errors)


def test_command_list_mismatch_fails(tmp_path: Path) -> None:
    report = _report("passed")
    report["steps"][1]["command"] = ["python3", "-m", "pytest", "tests/test_other.py"]
    path = _write(tmp_path, report)

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=False)

    assert ok is False
    assert "step command list does not match approved kora-local-core command list" in errors


def test_invalid_status_fails(tmp_path: Path) -> None:
    report = _report("passed")
    report["steps"][0]["status"] = "pending"
    path = _write(tmp_path, report)

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=False)

    assert ok is False
    assert any("invalid status" in error for error in errors)


def test_failed_report_fails_by_default(tmp_path: Path) -> None:
    report = _report("passed")
    report["final_status"] = "failed"
    report["steps"][-1]["status"] = "failed"
    report["steps"][-1]["return_code"] = 1
    path = _write(tmp_path, report)

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=False)

    assert ok is False
    assert "failed report requires --allow-failed" in errors


def test_failed_report_passes_with_allow_failed(tmp_path: Path) -> None:
    report = _report("passed")
    report["final_status"] = "failed"
    report["steps"][-1]["status"] = "failed"
    report["steps"][-1]["return_code"] = 1
    path = _write(tmp_path, report)

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=True)

    assert ok is True
    assert errors == []


def test_failed_runner_prefix_report_passes_with_allow_failed(tmp_path: Path) -> None:
    report = _report("passed")
    report["final_status"] = "failed"
    report["steps"] = report["steps"][:2]
    report["steps"][-1]["status"] = "failed"
    report["steps"][-1]["return_code"] = 2
    path = _write(tmp_path, report)

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=True)

    assert ok is True
    assert errors == []


def test_malformed_json_fails(tmp_path: Path) -> None:
    path = tmp_path / "report.json"
    path.write_text("{not-json", encoding="utf-8")

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=False)

    assert ok is False
    assert any("malformed JSON" in error for error in errors)


def test_verifier_rejects_arbitrary_requested_profile(tmp_path: Path) -> None:
    path = _write(tmp_path, _report("passed"))

    ok, errors = verifier.verify_report(path, "arbitrary-profile", allow_failed=False)

    assert ok is False
    assert any("unsupported profile" in error for error in errors)


def test_argv_field_is_accepted(tmp_path: Path) -> None:
    report = _report("passed")
    for step in report["steps"]:
        step["argv"] = step.pop("command")
    path = _write(tmp_path, report)

    ok, errors = verifier.verify_report(path, "kora-local-core", allow_failed=False)

    assert ok is True
    assert errors == []
