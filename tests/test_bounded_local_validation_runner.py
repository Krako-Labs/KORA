from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts import run_bounded_local_validation as runner


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


def test_supported_profile_contains_exact_approved_commands_in_order() -> None:
    steps = runner.PROFILES["kora-local-core"]

    assert [step.argv for step in steps] == APPROVED_COMMANDS


def test_unknown_profile_fails() -> None:
    exit_code, report = runner.build_report("unknown-profile")

    assert exit_code != 0
    assert report["final_status"] == "failed"
    assert report["steps"] == []
    assert "unknown profile" in report["error"]


def test_dry_run_does_not_execute_subprocess_commands(monkeypatch) -> None:
    def fail_if_called(*args, **kwargs):
        raise AssertionError("subprocess.run should not be called during dry-run")

    monkeypatch.setattr(runner.subprocess, "run", fail_if_called)

    exit_code, report = runner.build_report("kora-local-core", dry_run=True)

    assert exit_code == 0
    assert report["final_status"] == "dry-run"
    assert [step["status"] for step in report["steps"]] == ["skipped/dry-run"] * 6
    assert [step["return_code"] for step in report["steps"]] == [None] * 6


def test_successful_run_records_all_steps_passed(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    exit_code, report = runner.build_report("kora-local-core")

    assert exit_code == 0
    assert report["final_status"] == "passed"
    assert calls == APPROVED_COMMANDS
    assert [step["status"] for step in report["steps"]] == ["passed"] * 6
    assert [step["return_code"] for step in report["steps"]] == [0] * 6


def test_failing_step_stops_later_steps(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        return_code = 3 if len(calls) == 2 else 0
        return subprocess.CompletedProcess(argv, return_code)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    exit_code, report = runner.build_report("kora-local-core")

    assert exit_code == 3
    assert report["final_status"] == "failed"
    assert calls == APPROVED_COMMANDS[:2]
    assert [step["status"] for step in report["steps"]] == ["passed", "failed"]


def test_json_output_contains_profile_final_status_and_steps(tmp_path: Path) -> None:
    report = {
        "profile": "kora-local-core",
        "final_status": "passed",
        "repo_root": "/repo",
        "steps": [{"name": "one", "command": ["python3"], "return_code": 0, "status": "passed"}],
    }
    json_out = tmp_path / "report.json"

    runner.write_reports(report, json_out=json_out, md_out=None)

    written = json.loads(json_out.read_text(encoding="utf-8"))
    assert written["profile"] == "kora-local-core"
    assert written["final_status"] == "passed"
    assert written["steps"] == report["steps"]


def test_markdown_output_contains_profile_and_step_names(tmp_path: Path) -> None:
    report = {
        "profile": "kora-local-core",
        "final_status": "dry-run",
        "repo_root": "/repo",
        "steps": [
            {
                "name": "fixture quality check evaluator",
                "command": ["python3", "scripts/evaluate_fixture_quality_checks.py"],
                "return_code": None,
                "status": "skipped/dry-run",
            }
        ],
    }
    md_out = tmp_path / "report.md"

    runner.write_reports(report, json_out=None, md_out=md_out)

    text = md_out.read_text(encoding="utf-8")
    assert "profile: `kora-local-core`" in text
    assert "fixture quality check evaluator" in text


def test_commands_are_argv_lists_not_shell_strings() -> None:
    for steps in runner.PROFILES.values():
        for step in steps:
            assert isinstance(step.argv, list)
            assert step.argv
            assert all(isinstance(part, str) for part in step.argv)
