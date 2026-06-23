from __future__ import annotations

import json
from pathlib import Path

from scripts import verify_bounded_local_validation_report as verifier


APPROVED_COMMANDS = verifier.APPROVED_COMMANDS["kora-local-core"]


def _report(status: str = "passed") -> dict:
    step_status = "skipped/dry-run" if status == "dry-run" else "passed"
    return_code = None if status == "dry-run" else 0
    return {
        "profile": "kora-local-core",
        "final_status": status,
        "repo_root": str(verifier.REPO_ROOT),
        "steps": [
            {
                "name": f"step {index}",
                "command": command,
                "return_code": return_code,
                "status": step_status,
            }
            for index, command in enumerate(APPROVED_COMMANDS, start=1)
        ],
    }


def _write(tmp_path: Path, report: dict) -> Path:
    path = tmp_path / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return path


def test_passed_report_is_valid() -> None:
    assert verifier.validate_report(_report(), "kora-local-core") == []


def test_dry_run_report_is_valid() -> None:
    assert verifier.validate_report(_report("dry-run"), "kora-local-core") == []


def test_failed_report_requires_allow_failed() -> None:
    report = _report("failed")
    report["steps"] = report["steps"][:2]
    report["steps"][-1]["status"] = "failed"
    report["steps"][-1]["return_code"] = 7

    errors = verifier.validate_report(report, "kora-local-core")

    assert "failed report requires --allow-failed" in errors


def test_failed_report_with_approved_prefix_is_valid_when_allowed() -> None:
    report = _report("failed")
    report["steps"] = report["steps"][:3]
    report["steps"][-1]["status"] = "failed"
    report["steps"][-1]["return_code"] = 2

    assert verifier.validate_report(report, "kora-local-core", allow_failed=True) == []


def test_missing_required_top_level_field_fails() -> None:
    report = _report()
    del report["steps"]

    errors = verifier.validate_report(report, "kora-local-core")

    assert "missing top-level field: steps" in errors


def test_profile_mismatch_fails() -> None:
    report = _report()
    report["profile"] = "other"

    errors = verifier.validate_report(report, "kora-local-core")

    assert "profile mismatch: expected kora-local-core, got other" in errors


def test_repo_root_mismatch_fails() -> None:
    report = _report()
    report["repo_root"] = "/tmp/not-kora"

    errors = verifier.validate_report(report, "kora-local-core")

    assert any(error.startswith("repo_root mismatch:") for error in errors)


def test_command_mismatch_fails() -> None:
    report = _report()
    report["steps"][1]["command"] = ["python3", "-m", "pytest", "tests/test_other.py"]

    errors = verifier.validate_report(report, "kora-local-core")

    assert "step commands do not match the approved command list" in errors


def test_invalid_step_status_fails() -> None:
    report = _report()
    report["steps"][0]["status"] = "pending"

    errors = verifier.validate_report(report, "kora-local-core")

    assert "step 0 invalid status: pending" in errors


def test_passed_step_requires_zero_return_code() -> None:
    report = _report()
    report["steps"][0]["return_code"] = 1

    errors = verifier.validate_report(report, "kora-local-core")

    assert "step 0 passed status requires return_code 0" in errors


def test_skipped_step_requires_null_return_code() -> None:
    report = _report("dry-run")
    report["steps"][0]["return_code"] = 0

    errors = verifier.validate_report(report, "kora-local-core")

    assert "step 0 skipped/dry-run status requires null return_code" in errors


def test_failed_report_without_failed_step_fails() -> None:
    report = _report("failed")

    errors = verifier.validate_report(report, "kora-local-core", allow_failed=True)

    assert "failed report must include a failed step" in errors


def test_load_report_rejects_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")

    report, errors = verifier.load_report(path)

    assert report is None
    assert errors[0].startswith("invalid JSON:")


def test_main_never_executes_report_commands(tmp_path: Path, monkeypatch) -> None:
    report = _report()
    report["steps"][0]["command"] = ["python3", "-c", "raise SystemExit(99)"]
    path = _write(tmp_path, report)

    def fail_if_called(*args, **kwargs):
        raise AssertionError("verifier must not execute report commands")

    monkeypatch.setattr(verifier, "APPROVED_COMMANDS", {"kora-local-core": APPROVED_COMMANDS})
    monkeypatch.setattr("subprocess.run", fail_if_called)

    assert verifier.main([str(path), "--profile", "kora-local-core"]) == 1


def test_module_does_not_import_subprocess() -> None:
    assert "subprocess" not in verifier.__dict__
