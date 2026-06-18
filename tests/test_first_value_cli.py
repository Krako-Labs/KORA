from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

from kora.cli import main as cli_main


def test_pyproject_registers_kora_console_script() -> None:
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert data["project"]["scripts"]["kora"] == "kora.cli:main"


def _run_kora(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.pop("OPENAI_API_KEY", None)
    env.pop("ANTHROPIC_API_KEY", None)
    return subprocess.run(
        [sys.executable, "-m", "kora", *args],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def test_top_level_help_lists_first_value_commands() -> None:
    completed = _run_kora("--help")

    assert completed.returncode == 0
    assert "inspect" in completed.stdout
    assert "compare" in completed.stdout
    assert "doctor" in completed.stdout
    assert "proxy-demo" in completed.stdout
    assert "run" in completed.stdout
    assert "report" in completed.stdout


def test_first_value_command_help_works() -> None:
    for command in ("inspect", "compare", "doctor", "proxy-demo", "run", "report"):
        completed = _run_kora(command, "--help")
        assert completed.returncode == 0
        assert command in completed.stdout


def test_inspect_command_success_path_writes_json(tmp_path: Path) -> None:
    json_out = tmp_path / "inspect.json"
    completed = _run_kora("inspect", "--json-out", str(json_out))

    assert completed.returncode == 0
    assert "KORA Inspect" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["schema_version"] == "kora_inspect_v0"
    assert saved["works_without_provider_credentials"] is True
    assert saved["works_without_gpu"] is True
    assert saved["network_required"] is False
    assert "provider" in saved["step"]["available_execution_paths"]


def test_compare_command_success_path_writes_json(tmp_path: Path) -> None:
    json_out = tmp_path / "compare.json"
    completed = _run_kora("compare", "--json-out", str(json_out))

    assert completed.returncode == 0
    assert "KORA Compare" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    opportunities = saved["step"]["avoided_execution_opportunities"]
    assert saved["schema_version"] == "kora_compare_v0"
    assert opportunities["count"] == 11
    assert opportunities["rate"] == 11 / 18


def test_run_command_without_example_runs_first_value_path(tmp_path: Path) -> None:
    json_out = tmp_path / "run.json"
    completed = _run_kora("run", "--json-out", str(json_out))

    assert completed.returncode == 0
    assert "KORA Run" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["schema_version"] == "kora_run_v0"
    assert saved["step"]["total_requests"] == 18
    assert saved["step"]["provider_calls_performed"] is False
    assert saved["step"]["gpu_execution_performed"] is False


def test_run_command_with_example_remains_compatible() -> None:
    completed = _run_kora("run", "hello_kora", "--", "--offline")

    assert completed.returncode == 0
    assert "hello" in completed.stdout.lower()


def test_report_command_generates_json_and_markdown(tmp_path: Path) -> None:
    json_out = tmp_path / "report.json"
    md_out = tmp_path / "report.md"
    completed = _run_kora("report", "--json-out", str(json_out), "--md-out", str(md_out))

    assert completed.returncode == 0
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    markdown = md_out.read_text(encoding="utf-8")
    assert saved["schema_version"] == "krk_five_minute_first_value_v0"
    assert saved["official_cli_commands"] == [
        "kora inspect",
        "kora compare",
        "kora run",
        "kora report",
    ]
    assert "Official CLI Commands" in markdown


def test_demo_script_compatibility(tmp_path: Path) -> None:
    json_out = tmp_path / "demo.json"
    md_out = tmp_path / "demo.md"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/kora_five_minute_demo.py",
            "--json-out",
            str(json_out),
            "--md-out",
            str(md_out),
            "--repo-commit",
            "test-commit",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["final_classification"] == "FIVE_MINUTE_FIRST_VALUE_PATH_MEASURED"


def test_cli_main_report_direct_call(tmp_path: Path) -> None:
    json_out = tmp_path / "direct.json"
    md_out = tmp_path / "direct.md"

    assert cli_main(["report", "--json-out", str(json_out), "--md-out", str(md_out)]) == 0
    assert json_out.exists()
    assert md_out.exists()
