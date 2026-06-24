from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts import check_first_run_cli_smoke as smoke


EXPECTED_COMMANDS = [
    ["python3", "-m", "kora", "doctor", "examples/kora_doctor/customer_support_workload.json"],
    ["python3", "-m", "kora", "doctor", "--all", "examples/kora_doctor/"],
    ["python3", "-m", "kora", "proxy-demo", "examples/openai_compatible_proxy/requests.json"],
    ["python3", "examples/deterministic_classification/run.py"],
    ["python3", "examples/cache_reuse/run.py"],
    ["python3", "examples/rag_routing/run.py"],
    ["python3", "examples/agent_workflow_optimization/run.py"],
]


def test_default_command_list_includes_expected_offline_commands() -> None:
    commands = smoke.SMOKE_PROFILES["first-run-cli-core"]
    assert [command.argv for command in commands] == EXPECTED_COMMANDS


def test_command_records_use_structured_argv_lists() -> None:
    _, report = smoke.build_report("first-run-cli-core", dry_run=True)
    for command in report["commands"]:
        assert isinstance(command["argv"], list)
        assert all(isinstance(part, str) for part in command["argv"])


def test_dry_run_does_not_execute_subprocess_commands() -> None:
    def forbidden_runner(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise AssertionError("dry-run must not execute subprocess commands")

    exit_code, report = smoke.build_report(
        "first-run-cli-core",
        dry_run=True,
        runner=forbidden_runner,
    )

    assert exit_code == 0
    assert report["final_status"] == "planned"
    assert report["summary"]["planned_commands"] == len(EXPECTED_COMMANDS)


def test_unknown_profile_fails_closed() -> None:
    exit_code, report = smoke.build_report("unknown-profile")
    assert exit_code == 2
    assert report["final_status"] == "failed"
    assert report["commands"] == []
    assert "first-run-cli-core" in report["supported_profiles"]


def test_json_output_works(tmp_path: Path) -> None:
    json_out = tmp_path / "smoke.json"
    exit_code = smoke.main(["--dry-run", "--json-out", str(json_out)])

    assert exit_code == 0
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["profile"] == "first-run-cli-core"
    assert saved["summary"]["total_commands"] == len(EXPECTED_COMMANDS)


def test_markdown_output_works(tmp_path: Path) -> None:
    md_out = tmp_path / "smoke.md"
    exit_code = smoke.main(["--dry-run", "--md-out", str(md_out)])

    assert exit_code == 0
    text = md_out.read_text(encoding="utf-8")
    assert "# First-Run CLI Smoke Report" in text
    assert "kora doctor single workload" in text


def test_failure_result_returns_nonzero_and_stops_by_default() -> None:
    calls: list[list[str]] = []

    def failing_runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 7, stdout="bad", stderr="failed")

    exit_code, report = smoke.build_report("first-run-cli-core", runner=failing_runner)

    assert exit_code == 7
    assert report["final_status"] == "failed"
    assert len(calls) == 1
    assert report["commands"][0]["status"] == "failed"
    assert report["commands"][0]["stderr_tail"] == "failed"


def test_continue_on_failure_runs_remaining_commands() -> None:
    calls: list[list[str]] = []

    def failing_runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 1, stdout="", stderr="")

    exit_code, report = smoke.build_report(
        "first-run-cli-core",
        runner=failing_runner,
        continue_on_failure=True,
    )

    assert exit_code == 1
    assert len(calls) == len(EXPECTED_COMMANDS)
    assert report["summary"]["failed_commands"] == len(EXPECTED_COMMANDS)


def test_success_result_returns_zero() -> None:
    def passing_runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")

    exit_code, report = smoke.build_report("first-run-cli-core", runner=passing_runner)

    assert exit_code == 0
    assert report["final_status"] == "passed"
    assert report["summary"]["passed_commands"] == len(EXPECTED_COMMANDS)


def test_runner_invocation_uses_shell_false() -> None:
    seen_kwargs: list[dict[str, object]] = []

    def passing_runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        seen_kwargs.append(kwargs)
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    smoke.build_report("first-run-cli-core", runner=passing_runner)

    assert seen_kwargs
    assert all(kwargs["shell"] is False for kwargs in seen_kwargs)


def test_script_source_does_not_use_shell_true_or_external_command_config() -> None:
    source = Path(smoke.__file__).read_text(encoding="utf-8")
    assert "shell=True" not in source
    assert "yaml" not in source
    assert "tomllib" not in source
    assert "config" not in source.lower()


def test_output_paths_are_optional(capsys) -> None:
    exit_code = smoke.main(["--dry-run"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "final_status: planned" in captured.out


def test_script_does_not_mutate_repo_files_during_tests(tmp_path: Path) -> None:
    before = {path.name for path in smoke.REPO_ROOT.iterdir()}
    json_out = tmp_path / "smoke.json"
    md_out = tmp_path / "smoke.md"

    smoke.main(["--dry-run", "--json-out", str(json_out), "--md-out", str(md_out)])

    after = {path.name for path in smoke.REPO_ROOT.iterdir()}
    assert after == before
    assert json_out.exists()
    assert md_out.exists()
