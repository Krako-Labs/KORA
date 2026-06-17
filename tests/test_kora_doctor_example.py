import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


def _load_example_module():
    script_path = Path("examples/kora_doctor/run.py")
    spec = importlib.util.spec_from_file_location("kora_doctor_run", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load kora_doctor module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[str(spec.name)] = module
    spec.loader.exec_module(module)
    return module


def test_kora_doctor_loads_workload() -> None:
    module = _load_example_module()

    workload = module.load_workload()

    assert workload["workload_id"] == "kora_doctor_sample_workload_v0"
    assert workload["privacy_class"] == "synthetic"
    assert len(workload["tasks"]) == 7
    assert len(workload["deterministic_rules"]) == 3
    assert len(workload["provider_needed_rules"]) == 2


def test_kora_doctor_summary_matches_expected_counters() -> None:
    module = _load_example_module()
    expected = json.loads(Path("examples/kora_doctor/expected_counters.json").read_text(encoding="utf-8"))

    summary = module.build_doctor_summary()
    projected = {key: summary[key] for key in expected}

    assert projected == expected
    assert summary["suggested_deterministic_handlers"] == [
        "cache_reuse",
        "classify_by_rules",
        "static_transform",
    ]
    assert summary["provider_model_fallback_recommended_for"] == [
        "ambiguous semantic judgment",
        "open-ended generation",
        "ambiguous doctor signal: open-ended generation",
    ]


def test_kora_doctor_uses_kora_task_graph_path() -> None:
    module = _load_example_module()

    summary = module.build_doctor_summary()
    first = summary["inspections"][0]

    assert first["kora_graph_id"] == "kora-doctor-doctor-001"
    assert first["task_id"] == "doctor_inspect"
    assert first["kora_event_count"] == 1
    assert first["selected_route"] == "doctor.det.classify_by_rules"
    assert first["suggested_handler"] == "classify_by_rules"


def test_kora_doctor_requires_no_provider_environment(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    module = _load_example_module()

    summary = module.build_doctor_summary()

    assert summary["ok"] is True
    assert summary["provider_calls_actually_made"] == 0
    assert "OPENAI_API_KEY" not in os.environ
    assert "ANTHROPIC_API_KEY" not in os.environ


def test_kora_doctor_report_is_concise_and_contains_required_sections() -> None:
    module = _load_example_module()

    report = module.render_text_report(module.build_doctor_summary())

    assert report.startswith("KORA Doctor Example\n")
    assert "Total tasks: 7" in report
    assert "Deterministic candidates: 4" in report
    assert "Provider-needed candidates: 3" in report
    assert "Suggested deterministic handlers:" in report
    assert "- classify_by_rules" in report
    assert "- cache_reuse" in report
    assert "- static_transform" in report
    assert "Provider/model fallback recommended for:" in report
    assert "- ambiguous semantic judgment" in report
    assert "- open-ended generation" in report
    assert "Provider calls actually made: 0" in report
    assert "Route rationale:" in report
    assert "Next-step recommendations:" in report
    assert "does not claim production diagnostic accuracy" in report


def test_kora_doctor_cli_runs_and_writes_outputs(tmp_path: Path) -> None:
    json_out = tmp_path / "doctor.json"
    report_md = tmp_path / "doctor.md"

    completed = subprocess.run(
        [
            sys.executable,
            "examples/kora_doctor/run.py",
            "--json-out",
            str(json_out),
            "--report-md",
            str(report_md),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "KORA Doctor Example" in completed.stdout
    assert "Total tasks: 7" in completed.stdout
    assert "Provider calls actually made: 0" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    report = report_md.read_text(encoding="utf-8")
    assert saved["mode"] == "kora_doctor_example"
    assert saved["provider_calls_actually_made"] == 0
    assert report == completed.stdout


def test_kora_doctor_runs_through_kora_example_runner() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "kora", "run", "kora_doctor"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "KORA Doctor Example" in completed.stdout
    assert "Deterministic candidates: 4" in completed.stdout


def test_kora_doctor_appears_in_example_listing() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "kora", "examples", "list"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "kora_doctor: offline doctor-style workload inspection example" in completed.stdout
