from __future__ import annotations

import subprocess
import shutil
from pathlib import Path

from scripts import check_source_install_readiness as readiness


def test_editable_install_command_uses_local_repo_path() -> None:
    repo_root = Path("/tmp/kora-repo")
    venv_dir = Path("/tmp/kora-venv")

    command = readiness.build_install_command(
        repo_root=repo_root,
        venv_dir=venv_dir,
        install_mode="editable",
    )

    assert command.argv[-2:] == ["-e", str(repo_root)]
    assert "pip" in command.argv
    assert "pypi" not in " ".join(command.argv).lower()


def test_source_install_command_uses_local_repo_path_without_editable_flag() -> None:
    repo_root = Path("/tmp/kora-repo")
    venv_dir = Path("/tmp/kora-venv")

    command = readiness.build_install_command(
        repo_root=repo_root,
        venv_dir=venv_dir,
        install_mode="source",
    )

    assert command.argv[-1] == str(repo_root)
    assert "-e" not in command.argv


def test_check_commands_cover_import_module_cli_entrypoint_and_smoke() -> None:
    commands = readiness.build_check_commands(
        repo_root=Path("/tmp/kora-repo"),
        venv_dir=Path("/tmp/kora-venv"),
    )

    labels = [command.label for command in commands]
    assert labels == [
        "import kora",
        "python -m kora availability",
        "kora CLI entry point availability",
        "no-provider command smoke",
    ]
    assert commands[0].argv[-1] == "import kora; print(kora.__name__)"
    assert commands[1].argv[-3:] == ["-m", "kora", "--help"]
    assert commands[2].argv[-1] == "--help"
    assert commands[3].argv[-2:] == ["examples", "list"]


def test_success_summary_contains_required_markers(tmp_path: Path) -> None:
    def passing_runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, 0, stdout="ok", stderr="")

    exit_code, report = readiness.run_readiness_check(
        repo_root=tmp_path,
        runner=passing_runner,
        python_executable="python3",
    )
    text = readiness.render_text_summary(report)

    assert exit_code == 0
    assert report["install_mode"] == "editable"
    assert report["total_checks"] == 6
    assert report["passed_checks"] == 6
    assert "install mode used: editable" in text
    assert "import check result: passed" in text
    assert "python -m kora availability check result: passed" in text
    assert "kora CLI availability check result: passed" in text
    assert "command smoke result: passed" in text


def test_boundary_text_is_explicit() -> None:
    note = readiness.BOUNDARY_NOTE

    assert "local source installation only" in note
    assert "does not check PyPI installation" in note
    assert "publish a package" in note
    assert "claim getkora is published" in note
    assert "install-from-PyPI support" in note


def test_install_failure_returns_nonzero_and_skips_later_checks(tmp_path: Path) -> None:
    calls: list[list[str]] = []

    def runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(argv)
        if len(calls) == 2:
            return subprocess.CompletedProcess(argv, 9, stdout="", stderr="install failed")
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    exit_code, report = readiness.run_readiness_check(
        repo_root=tmp_path,
        runner=runner,
        python_executable="python3",
    )
    text = readiness.render_text_summary(report)

    assert exit_code == 1
    assert report["final_status"] == "failed"
    assert report["failed_checks"] == 1
    assert len(calls) == 2
    assert "import check result: not-run" in text
    assert report["steps"][1]["stderr_tail"] == "install failed"


def test_subprocess_invocations_use_shell_false(tmp_path: Path) -> None:
    seen_kwargs: list[dict[str, object]] = []

    def runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        seen_kwargs.append(kwargs)
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    readiness.run_readiness_check(
        repo_root=tmp_path,
        runner=runner,
        python_executable="python3",
    )

    assert seen_kwargs
    assert all(kwargs["shell"] is False for kwargs in seen_kwargs)
    assert all(kwargs["check"] is False for kwargs in seen_kwargs)


def test_keep_temp_reports_debug_path(tmp_path: Path) -> None:
    def passing_runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")

    exit_code, report = readiness.run_readiness_check(
        repo_root=tmp_path,
        keep_temp=True,
        runner=passing_runner,
        python_executable="python3",
    )
    text = readiness.render_text_summary(report)

    assert exit_code == 0
    assert report["temp_preserved_for_debug"] is True
    assert report["cleanup_performed"] is False
    assert "debug temp preserved:" in text
    shutil.rmtree(str(report["temp_root"]), ignore_errors=True)
