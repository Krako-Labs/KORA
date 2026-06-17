from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


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


def test_kora_doctor_help_is_available() -> None:
    completed = _run_kora("doctor", "--help")

    assert completed.returncode == 0
    assert "workload JSON path" in completed.stdout
    assert "--all" in completed.stdout


def test_kora_doctor_single_workload_uses_existing_doctor_logic(tmp_path: Path) -> None:
    json_out = tmp_path / "doctor.json"
    report_md = tmp_path / "doctor.md"

    completed = _run_kora(
        "doctor",
        "examples/kora_doctor/workloads/customer_support_workload.json",
        "--json-out",
        str(json_out),
        "--report-md",
        str(report_md),
    )

    assert completed.returncode == 0
    assert "KORA Doctor Example" in completed.stdout
    assert "Workload: kora_doctor_customer_support_workload_v0" in completed.stdout
    assert "Provider calls actually made: 0" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["mode"] == "kora_doctor_example"
    assert saved["workload_id"] == "kora_doctor_customer_support_workload_v0"
    assert saved["total_tasks"] == 6
    assert saved["deterministic_candidates"] == 4
    assert saved["provider_needed_candidates"] == 2
    assert saved["provider_calls_actually_made"] == 0
    assert report_md.read_text(encoding="utf-8") == completed.stdout


def test_kora_doctor_single_workload_accepts_friendly_example_path() -> None:
    completed = _run_kora("doctor", "examples/kora_doctor/customer_support_workload.json")

    assert completed.returncode == 0
    assert "Workload: kora_doctor_customer_support_workload_v0" in completed.stdout
    assert "Avoided simulated provider/model invocations: 4" in completed.stdout


def test_kora_doctor_aggregate_mode_uses_workload_directory(tmp_path: Path) -> None:
    json_out = tmp_path / "doctor_pack.json"

    completed = _run_kora(
        "doctor",
        "--all",
        "examples/kora_doctor/",
        "--json-out",
        str(json_out),
    )

    assert completed.returncode == 0
    assert "KORA Doctor Report Pack" in completed.stdout
    assert "Workloads: 4" in completed.stdout
    assert "Provider calls actually made: 0" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["mode"] == "kora_doctor_report_pack"
    assert saved["workload_count"] == 4
    assert saved["total_tasks"] == 25
    assert saved["deterministic_candidates"] == 16
    assert saved["provider_needed_candidates"] == 9
    assert saved["provider_calls_actually_made"] == 0
