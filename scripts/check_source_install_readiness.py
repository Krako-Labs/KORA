from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_TAIL_LIMIT = 2000
BOUNDARY_NOTE = (
    "Boundary: this checks local source installation only; it does not check PyPI "
    "installation, publish a package, claim getkora is published, or claim "
    "install-from-PyPI support."
)


@dataclass(frozen=True)
class ReadinessCommand:
    label: str
    argv: list[str]
    cwd: Path


@dataclass(frozen=True)
class ReadinessStep:
    label: str
    status: str
    return_code: int
    elapsed_seconds: float
    stdout_tail: str = ""
    stderr_tail: str = ""


Runner = Callable[..., subprocess.CompletedProcess[str]]
Clock = Callable[[], float]


def _tail_text(value: str | None) -> str:
    if not value:
        return ""
    if len(value) <= OUTPUT_TAIL_LIMIT:
        return value
    return value[-OUTPUT_TAIL_LIMIT:]


def _venv_python(venv_dir: Path) -> Path:
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _venv_entry_point(venv_dir: Path, name: str) -> Path:
    if sys.platform == "win32":
        return venv_dir / "Scripts" / f"{name}.exe"
    return venv_dir / "bin" / name


def build_install_command(
    *,
    repo_root: Path,
    venv_dir: Path,
    install_mode: str,
) -> ReadinessCommand:
    if install_mode == "editable":
        install_args = ["install", "-e", str(repo_root)]
    elif install_mode == "source":
        install_args = ["install", str(repo_root)]
    else:
        raise ValueError(f"unsupported install mode: {install_mode}")

    return ReadinessCommand(
        label=f"{install_mode} source install",
        argv=[str(_venv_python(venv_dir)), "-m", "pip", *install_args],
        cwd=repo_root,
    )


def build_check_commands(*, repo_root: Path, venv_dir: Path) -> list[ReadinessCommand]:
    python_path = _venv_python(venv_dir)
    kora_entry = _venv_entry_point(venv_dir, "kora")
    return [
        ReadinessCommand(
            label="import kora",
            argv=[str(python_path), "-c", "import kora; print(kora.__name__)"],
            cwd=repo_root,
        ),
        ReadinessCommand(
            label="python -m kora availability",
            argv=[str(python_path), "-m", "kora", "--help"],
            cwd=repo_root,
        ),
        ReadinessCommand(
            label="kora CLI entry point availability",
            argv=[str(kora_entry), "--help"],
            cwd=repo_root,
        ),
        ReadinessCommand(
            label="no-provider command smoke",
            argv=[str(kora_entry), "examples", "list"],
            cwd=repo_root,
        ),
    ]


def _run_command(
    command: ReadinessCommand,
    *,
    runner: Runner,
    clock: Clock,
) -> ReadinessStep:
    start = clock()
    completed = runner(
        command.argv,
        cwd=command.cwd,
        shell=False,
        check=False,
        text=True,
        capture_output=True,
    )
    elapsed = clock() - start
    return ReadinessStep(
        label=command.label,
        status="passed" if completed.returncode == 0 else "failed",
        return_code=int(completed.returncode),
        elapsed_seconds=round(elapsed, 3),
        stdout_tail=_tail_text(completed.stdout),
        stderr_tail=_tail_text(completed.stderr),
    )


def _step_to_dict(step: ReadinessStep) -> dict[str, object]:
    return {
        "label": step.label,
        "status": step.status,
        "return_code": step.return_code,
        "elapsed_seconds": step.elapsed_seconds,
        "stdout_tail": step.stdout_tail,
        "stderr_tail": step.stderr_tail,
    }


def run_readiness_check(
    *,
    repo_root: Path = REPO_ROOT,
    install_mode: str = "editable",
    keep_temp: bool = False,
    runner: Runner = subprocess.run,
    clock: Clock = time.perf_counter,
    python_executable: str = sys.executable,
) -> tuple[int, dict[str, object]]:
    repo_root = repo_root.resolve()
    temp_root = Path(tempfile.mkdtemp(prefix="kora-source-install-"))
    venv_dir = temp_root / "venv"
    steps: list[ReadinessStep] = []
    exit_code = 0
    cleanup_performed = False

    try:
        create_venv = ReadinessCommand(
            label="create isolated virtual environment",
            argv=[python_executable, "-m", "venv", str(venv_dir)],
            cwd=repo_root,
        )
        create_step = _run_command(create_venv, runner=runner, clock=clock)
        steps.append(create_step)
        if create_step.return_code != 0:
            exit_code = 1

        if exit_code == 0:
            install_step = _run_command(
                build_install_command(repo_root=repo_root, venv_dir=venv_dir, install_mode=install_mode),
                runner=runner,
                clock=clock,
            )
            steps.append(install_step)
            if install_step.return_code != 0:
                exit_code = 1

        if exit_code == 0:
            for command in build_check_commands(repo_root=repo_root, venv_dir=venv_dir):
                step = _run_command(command, runner=runner, clock=clock)
                steps.append(step)
                if step.return_code != 0:
                    exit_code = 1
                    break
    finally:
        if not keep_temp:
            shutil.rmtree(temp_root, ignore_errors=True)
            cleanup_performed = True

    return exit_code, _build_report(
        repo_root,
        temp_root,
        install_mode,
        keep_temp,
        cleanup_performed,
        steps,
    )


def _build_report(
    repo_root: Path,
    temp_root: Path,
    install_mode: str,
    keep_temp: bool,
    cleanup_performed: bool,
    steps: Sequence[ReadinessStep],
) -> dict[str, object]:
    failed = sum(1 for step in steps if step.status == "failed")
    passed = sum(1 for step in steps if step.status == "passed")
    final_status = "failed" if failed else "passed"
    return {
        "repo_root": str(repo_root),
        "temp_root": str(temp_root),
        "install_mode": install_mode,
        "final_status": final_status,
        "total_checks": len(steps),
        "passed_checks": passed,
        "failed_checks": failed,
        "cleanup_performed": cleanup_performed,
        "temp_preserved_for_debug": keep_temp,
        "boundary_note": BOUNDARY_NOTE,
        "steps": [_step_to_dict(step) for step in steps],
    }


def render_text_summary(report: dict[str, object]) -> str:
    lines = [
        "KORA Source-Install Readiness Check",
        f"install mode used: {report['install_mode']}",
        f"final status: {report['final_status']}",
        f"checks: {report['passed_checks']} passed / {report['failed_checks']} failed / {report['total_checks']} total",
    ]
    steps = list(report["steps"])
    for step_obj in steps:
        step = dict(step_obj)
        lines.append(f"- {step['status']}: {step['label']} ({step['return_code']})")
    import_result = _status_for_label(steps, "import kora")
    module_cli_result = _status_for_label(steps, "python -m kora availability")
    entry_cli_result = _status_for_label(steps, "kora CLI entry point availability")
    smoke_result = _status_for_label(steps, "no-provider command smoke")
    lines.extend(
        [
            f"import check result: {import_result}",
            f"python -m kora availability check result: {module_cli_result}",
            f"kora CLI availability check result: {entry_cli_result}",
            f"command smoke result: {smoke_result}",
            str(report["boundary_note"]),
        ]
    )
    if report["temp_preserved_for_debug"]:
        lines.append(f"debug temp preserved: {report['temp_root']}")
    return "\n".join(lines)


def _status_for_label(steps: Sequence[object], label: str) -> str:
    for step_obj in steps:
        step = dict(step_obj)
        if step["label"] == label:
            return str(step["status"])
    return "not-run"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check local KORA source-install readiness in an isolated temporary virtual environment."
        )
    )
    parser.add_argument(
        "--install-mode",
        choices=["editable", "source"],
        default="editable",
        help="Install mode to use for the local source tree. Defaults to editable.",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Preserve the temporary environment for debugging instead of cleaning it up.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    exit_code, report = run_readiness_check(
        install_mode=args.install_mode,
        keep_temp=args.keep_temp,
    )
    print(render_text_summary(report))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
