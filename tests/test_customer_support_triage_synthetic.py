import importlib.util
import os
import subprocess
import sys
from pathlib import Path


def _load_example_module():
    script_path = Path("examples/customer_support_triage_synthetic/run.py")
    spec = importlib.util.spec_from_file_location(
        "customer_support_triage_synthetic_run", script_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load customer_support_triage_synthetic module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[str(spec.name)] = module
    spec.loader.exec_module(module)
    return module


def test_customer_support_triage_synthetic_loads_workload() -> None:
    module = _load_example_module()

    workload = module.load_workload()

    assert workload["workload_id"] == "customer_support_triage_synthetic_v1"
    assert workload["privacy_class"] == "synthetic"
    assert len(workload["requests"]) == 12


def test_customer_support_triage_synthetic_summary_counts() -> None:
    module = _load_example_module()

    summary = module.build_customer_support_triage_synthetic_summary(offline=True)

    assert summary["ok"] is True
    assert summary["mode"] == "customer_support_triage_local_validation"
    assert summary["workload_id"] == "customer_support_triage_synthetic_v1"
    assert summary["privacy_class"] == "synthetic"
    assert summary["provider"] == "local_validation"
    assert summary["model"] == "deterministic-local"
    assert summary["total_requests"] == 12
    assert summary["baseline_model_calls"] == 12
    assert summary["kora_model_calls"] == 4
    assert summary["avoided_model_calls"] == 8
    assert round(summary["avoided_model_call_rate"], 4) == 0.6667
    assert summary["deterministic_routes"] == 8
    assert summary["model_escalations"] == 4
    assert summary["validation_pass_count"] == 12
    assert summary["validation_fail_count"] == 0
    assert summary["error_count"] == 0
    assert summary["fallback_count"] == 0


def test_customer_support_triage_synthetic_explicit_local_validation_counts() -> None:
    module = _load_example_module()

    summary = module.build_customer_support_triage_synthetic_summary(
        offline=True,
        adapter_kind="local_validation",
    )

    assert summary["provider"] == "local_validation"
    assert summary["model"] == "deterministic-local"
    assert summary["baseline_model_calls"] == 12
    assert summary["kora_model_calls"] == 4
    assert summary["avoided_model_calls"] == 8


def test_customer_support_triage_synthetic_explicit_local_runtime_counts() -> None:
    module = _load_example_module()

    summary = module.build_customer_support_triage_synthetic_summary(
        offline=True,
        adapter_kind="local_runtime",
    )

    assert summary["provider"] == "local_runtime"
    assert summary["model"] == "deterministic-local-runtime"
    assert summary["baseline_model_calls"] == 12
    assert summary["kora_model_calls"] == 4
    assert summary["avoided_model_calls"] == 8
    assert summary["validation_pass_count"] == 12


def test_customer_support_triage_synthetic_requires_no_provider_environment(
    monkeypatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    module = _load_example_module()

    summary = module.build_customer_support_triage_synthetic_summary(offline=True)

    assert summary["ok"] is True
    assert "OPENAI_API_KEY" not in os.environ
    assert "ANTHROPIC_API_KEY" not in os.environ


def test_customer_support_triage_synthetic_does_not_emit_raw_inputs_or_outputs() -> None:
    module = _load_example_module()

    summary = module.build_customer_support_triage_synthetic_summary(offline=True)

    assert summary["raw_prompts_emitted"] is False
    assert summary["raw_responses_emitted"] is False
    assert "raw provider responses" in summary["notes"][-1]


def test_customer_support_triage_synthetic_rejects_non_offline_mode() -> None:
    module = _load_example_module()

    try:
        module.build_customer_support_triage_synthetic_summary(offline=False)
    except ValueError as exc:
        assert "--offline only" in str(exc)
    else:
        raise AssertionError("expected offline-only guard")


def test_customer_support_triage_synthetic_cli_runs() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "customer_support_triage_synthetic",
            "--",
            "--offline",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert '"mode": "customer_support_triage_local_validation"' in completed.stdout
    assert '"baseline_model_calls": 12' in completed.stdout
    assert '"kora_model_calls": 4' in completed.stdout


def test_customer_support_triage_synthetic_cli_explicit_local_validation_runs() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "customer_support_triage_synthetic",
            "--",
            "--offline",
            "--adapter",
            "local_validation",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert '"provider": "local_validation"' in completed.stdout
    assert '"baseline_model_calls": 12' in completed.stdout
    assert '"kora_model_calls": 4' in completed.stdout


def test_customer_support_triage_synthetic_report_with_explicit_adapter(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "customer_support_validation.md"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "customer_support_triage_synthetic",
            "--",
            "--offline",
            "--adapter",
            "local_validation",
            "--report-md",
            str(report_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert report_path.exists()
    report = report_path.read_text(encoding="utf-8")
    assert "customer_support_triage_local_validation" in report
    assert "local_validation" in report
    assert "## Report Metadata" in report
    assert "## Adapter Selection Result" in report
    assert "## Provider Fixture Dry-Run Contract" in report
    assert "## Explicit Non-Claims" in report
    assert "- Adapter kind: `local_validation`" in report
    assert "- Local/no-network status: `yes`" in report
    assert "- Baseline candidate events: `12`" in report
    assert "- KORA routed events: `4`" in report
    assert "- Avoided model-call events: `8`" in report
    assert "no production cost reduction proof" in report
    assert "no real API-cost reduction proof" in report
    assert "no energy reduction evidence" in report
    assert "real API cost reduction" not in report
    assert "production cost reduction proof." not in report


def test_customer_support_triage_synthetic_report_with_local_runtime_adapter(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "customer_support_local_runtime.md"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "customer_support_triage_synthetic",
            "--",
            "--offline",
            "--adapter",
            "local_runtime",
            "--report-md",
            str(report_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert report_path.exists()
    report = report_path.read_text(encoding="utf-8")
    assert "customer_support_triage_local_validation" in report
    assert "local_runtime" in report
    assert "- Adapter kind: `local_runtime`" in report
    assert "- Provider label: `local_runtime`" in report
    assert "- Model label: `deterministic-local-runtime`" in report
    assert "- No network: `yes`" in report
    assert "- No provider call: `yes`" in report
    assert "- Provider attempted events: `0`" in report


def test_customer_support_triage_report_fixture_validation_failure_fails_closed(
    monkeypatch,
) -> None:
    module = _load_example_module()

    def fail_validation(_fixture):
        raise ValueError("fixture validation failed closed")

    monkeypatch.setattr(module, "validate_provider_fixture", fail_validation)

    try:
        module.build_customer_support_triage_synthetic_summary(
            offline=True,
            adapter_kind="local_runtime",
        )
    except ValueError as exc:
        assert "fixture validation failed closed" in str(exc)
    else:
        raise AssertionError("expected fixture validation failure")


def test_customer_support_triage_synthetic_blocked_adapter_fails_closed(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "blocked.md"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "customer_support_triage_synthetic",
            "--",
            "--offline",
            "--adapter",
            "blocked",
            "--report-md",
            str(report_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "Real model-call adapter is not configured" in completed.stderr
    assert "customer-support triage workload" not in completed.stderr
    assert not report_path.exists()


def test_customer_support_triage_synthetic_local_runtime_placeholder_fails_closed(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "placeholder.md"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "customer_support_triage_synthetic",
            "--",
            "--offline",
            "--adapter",
            "local_runtime_placeholder",
            "--report-md",
            str(report_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "Local runtime adapters are not implemented yet" in completed.stderr
    assert "No provider call was attempted" in completed.stderr
    assert "customer-support triage workload" not in completed.stderr
    assert not report_path.exists()


def test_customer_support_triage_synthetic_unknown_adapter_lists_available_kinds() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "customer_support_triage_synthetic",
            "--",
            "--offline",
            "--adapter",
            "remote_provider",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode != 0
    assert "invalid choice" in completed.stderr
    assert "local_validation" in completed.stderr
    assert "local_runtime" in completed.stderr
    assert "blocked" in completed.stderr
    assert "local_runtime_placeholder" in completed.stderr


def test_customer_support_triage_synthetic_help_lists_available_adapter_kinds() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "customer_support_triage_synthetic",
            "--",
            "--help",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "--adapter" in completed.stdout
    assert "local_validation" in completed.stdout
    assert "local_runtime" in completed.stdout
    assert "blocked" in completed.stdout
    assert "local_runtime_placeholder" in completed.stdout
