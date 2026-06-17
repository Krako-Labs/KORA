import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def _load_example_module():
    script_path = Path("examples/kora_doctor/run.py")
    spec = importlib.util.spec_from_file_location("kora_doctor_run_pack", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load kora_doctor module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[str(spec.name)] = module
    spec.loader.exec_module(module)
    return module


def _project(summary: dict, expected: dict) -> dict:
    return {key: summary[key] for key in expected}


def test_kora_doctor_sample_workload_paths_include_report_pack() -> None:
    module = _load_example_module()

    paths = module.sample_workload_paths()

    assert [path.name for path in paths] == [
        "workload.json",
        "customer_support_workload.json",
        "developer_workflow_workload.json",
        "document_intake_workload.json",
    ]


def test_kora_doctor_each_report_pack_workload_counts() -> None:
    module = _load_example_module()

    for path in module.sample_workload_paths():
        summary = module.build_doctor_summary(path)
        if path.name == "workload.json":
            assert summary["total_tasks"] == 7
            assert summary["deterministic_candidates"] == 4
            assert summary["provider_needed_candidates"] == 3
        else:
            assert summary["total_tasks"] == 6
            assert summary["deterministic_candidates"] == 4
            assert summary["provider_needed_candidates"] == 2
        assert summary["provider_calls_actually_made"] == 0
        assert summary["ok"] is True
        assert all(item["kora_event_count"] == 1 for item in summary["inspections"])


def test_kora_doctor_aggregate_report_pack_matches_expected_counters() -> None:
    module = _load_example_module()
    expected = json.loads(Path("examples/kora_doctor/expected_counters_all.json").read_text(encoding="utf-8"))

    summary = module.build_aggregate_summary()

    assert _project(summary, expected) == expected
    assert summary["workload_ids"] == [
        "kora_doctor_sample_workload_v0",
        "kora_doctor_customer_support_workload_v0",
        "kora_doctor_developer_workflow_workload_v0",
        "kora_doctor_document_intake_workload_v0",
    ]
    assert summary["suggested_deterministic_handlers"] == [
        "cache_reuse",
        "classify_by_rules",
        "static_transform",
    ]


def test_kora_doctor_aggregate_report_renders_markdown_style_summary() -> None:
    module = _load_example_module()

    report = module.render_text_report(module.build_aggregate_summary())

    assert report.startswith("KORA Doctor Report Pack\n")
    assert "Total tasks: 25" in report
    assert "Deterministic candidates: 16" in report
    assert "Provider-needed candidates: 9" in report
    assert "Workload counters:" in report
    assert "kora_doctor_customer_support_workload_v0" in report
    assert "Provider calls actually made: 0" in report
    assert "production proxy readiness" in report


def test_kora_doctor_all_cli_writes_report_pack_outputs(tmp_path: Path) -> None:
    json_out = tmp_path / "doctor_pack.json"
    report_md = tmp_path / "doctor_pack.md"

    completed = subprocess.run(
        [
            sys.executable,
            "examples/kora_doctor/run.py",
            "--all",
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
    assert "KORA Doctor Report Pack" in completed.stdout
    assert "Total tasks: 25" in completed.stdout
    saved = json.loads(json_out.read_text(encoding="utf-8"))
    assert saved["mode"] == "kora_doctor_report_pack"
    assert saved["provider_calls_actually_made"] == 0
    assert report_md.read_text(encoding="utf-8") == completed.stdout
