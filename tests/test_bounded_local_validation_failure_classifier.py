from __future__ import annotations

import json
from pathlib import Path

from scripts import classify_bounded_local_validation_failure as classifier
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


def _failed_report(command_index: int, command: list[str] | None = None) -> dict:
    report = _report("failed")
    report["steps"] = report["steps"][: command_index + 1]
    report["steps"][-1]["status"] = "failed"
    report["steps"][-1]["return_code"] = 3
    if command is not None:
        report["steps"][-1]["command"] = command
    return report


def _write(tmp_path: Path, report: dict) -> Path:
    path = tmp_path / "report.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    return path


def test_classifies_all_passed() -> None:
    code, result = classifier.classify_report(_report(), "kora-local-core")

    assert code == 0
    assert result["category"] == "all_passed"


def test_classifies_dry_run_only() -> None:
    code, result = classifier.classify_report(_report("dry-run"), "kora-local-core")

    assert code == 0
    assert result["category"] == "dry_run_only"


def test_classifies_fixture_quality_evaluator_failure() -> None:
    code, result = classifier.classify_report(_failed_report(0), "kora-local-core")

    assert code == 0
    assert result["category"] == "fixture_quality_failure"


def test_classifies_fixture_quality_test_failure() -> None:
    code, result = classifier.classify_report(_failed_report(1), "kora-local-core")

    assert code == 0
    assert result["category"] == "fixture_quality_failure"


def test_classifies_representativeness_failure() -> None:
    code, result = classifier.classify_report(_failed_report(2), "kora-local-core")

    assert code == 0
    assert result["category"] == "representativeness_failure"


def test_classifies_markdown_link_failure() -> None:
    code, result = classifier.classify_report(_failed_report(3), "kora-local-core")

    assert code == 0
    assert result["category"] == "markdown_link_failure"


def test_classifies_diff_check_failure() -> None:
    code, result = classifier.classify_report(_failed_report(4), "kora-local-core")

    assert code == 0
    assert result["category"] == "diff_check_failure"


def test_classifies_full_pytest_failure() -> None:
    code, result = classifier.classify_report(_failed_report(5), "kora-local-core")

    assert code == 0
    assert result["category"] == "full_pytest_failure"


def test_classifies_unknown_step_failure() -> None:
    code, result = classifier.classify_report(
        _failed_report(1, ["python3", "scripts/custom_check.py"]),
        "kora-local-core",
    )

    assert code == 0
    assert result["category"] == "unknown_step_failure"


def test_unsupported_profile_returns_nonzero() -> None:
    report = _report()
    report["profile"] = "other"

    code, result = classifier.classify_report(report, "kora-local-core")

    assert code == 1
    assert result["category"] == "unsupported_profile"


def test_malformed_steps_returns_nonzero() -> None:
    report = _report()
    report["steps"] = "not-a-list"

    code, result = classifier.classify_report(report, "kora-local-core")

    assert code == 1
    assert result["category"] == "malformed_report"


def test_malformed_json_main_returns_nonzero(tmp_path: Path, capsys) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")

    code = classifier.main([str(path), "--profile", "kora-local-core"])
    output = json.loads(capsys.readouterr().out)

    assert code == 1
    assert output["category"] == "malformed_report"


def test_main_never_executes_report_commands(tmp_path: Path, monkeypatch) -> None:
    report = _failed_report(0, ["python3", "-c", "raise SystemExit(99)"])
    path = _write(tmp_path, report)

    def fail_if_called(*args, **kwargs):
        raise AssertionError("classifier must not execute report commands")

    monkeypatch.setattr("subprocess.run", fail_if_called)

    assert classifier.main([str(path), "--profile", "kora-local-core"]) == 0


def test_module_does_not_import_subprocess() -> None:
    assert "subprocess" not in classifier.__dict__
