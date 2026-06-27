import importlib.util
import os
import subprocess
import sys
from pathlib import Path


def _load_example_module():
    script_path = Path("examples/model_call_counter_fixture/run.py")
    spec = importlib.util.spec_from_file_location("model_call_counter_fixture_run", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load model_call_counter_fixture module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[str(spec.name)] = module
    spec.loader.exec_module(module)
    return module


def test_model_call_counter_fixture_summary_counts() -> None:
    module = _load_example_module()

    summary = module.build_model_call_counter_fixture_summary(offline=True)

    assert summary["ok"] is True
    assert summary["mode"] == "local_no_network_model_call_validation"
    assert summary["provider"] == "local_validation"
    assert summary["model"] == "deterministic-local"
    assert summary["total_requests"] == 10
    assert summary["baseline_model_calls"] == 10
    assert summary["kora_model_calls"] == 4
    assert summary["avoided_model_calls"] == 6
    assert summary["avoided_model_call_rate"] == 0.6
    assert summary["deterministic_routes"] == 6
    assert summary["model_escalations"] == 4
    assert summary["validation_pass_count"] == 10
    assert summary["validation_fail_count"] == 0
    assert summary["error_count"] == 0
    assert summary["fallback_count"] == 0


def test_model_call_counter_fixture_explicit_local_validation_counts() -> None:
    module = _load_example_module()

    summary = module.build_model_call_counter_fixture_summary(
        offline=True,
        adapter_kind="local_validation",
    )

    assert summary["provider"] == "local_validation"
    assert summary["model"] == "deterministic-local"
    assert summary["baseline_model_calls"] == 10
    assert summary["kora_model_calls"] == 4
    assert summary["avoided_model_calls"] == 6


def test_model_call_counter_fixture_explicit_local_runtime_counts() -> None:
    module = _load_example_module()

    summary = module.build_model_call_counter_fixture_summary(
        offline=True,
        adapter_kind="local_runtime",
    )

    assert summary["provider"] == "local_runtime"
    assert summary["model"] == "deterministic-local-runtime"
    assert summary["baseline_model_calls"] == 10
    assert summary["kora_model_calls"] == 4
    assert summary["avoided_model_calls"] == 6
    assert summary["validation_pass_count"] == 10


def test_model_call_counter_fixture_does_not_emit_raw_inputs_or_outputs() -> None:
    module = _load_example_module()

    summary = module.build_model_call_counter_fixture_summary(offline=True)

    assert summary["privacy_class"] == "synthetic"
    assert summary["raw_prompts_emitted"] is False
    assert summary["raw_responses_emitted"] is False
    assert "raw provider responses" in summary["notes"][-1]


def test_model_call_counter_fixture_requires_no_provider_environment(
    monkeypatch,
) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    module = _load_example_module()

    summary = module.build_model_call_counter_fixture_summary(offline=True)

    assert summary["ok"] is True
    assert "OPENAI_API_KEY" not in os.environ
    assert "ANTHROPIC_API_KEY" not in os.environ


def test_model_call_counter_fixture_rejects_non_offline_mode() -> None:
    module = _load_example_module()

    try:
        module.build_model_call_counter_fixture_summary(offline=False)
    except ValueError as exc:
        assert "--offline only" in str(exc)
    else:
        raise AssertionError("expected offline-only guard")


def test_model_call_counter_fixture_cli_runs() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "model_call_counter_fixture",
            "--",
            "--offline",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert '"mode": "local_no_network_model_call_validation"' in completed.stdout
    assert '"baseline_model_calls": 10' in completed.stdout
    assert '"kora_model_calls": 4' in completed.stdout


def test_model_call_counter_fixture_cli_explicit_local_validation_runs() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "model_call_counter_fixture",
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
    assert '"baseline_model_calls": 10' in completed.stdout
    assert '"kora_model_calls": 4' in completed.stdout


def test_model_call_counter_fixture_cli_explicit_local_runtime_runs() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "model_call_counter_fixture",
            "--",
            "--offline",
            "--adapter",
            "local_runtime",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert '"provider": "local_runtime"' in completed.stdout
    assert '"model": "deterministic-local-runtime"' in completed.stdout
    assert '"baseline_model_calls": 10' in completed.stdout
    assert '"kora_model_calls": 4' in completed.stdout


def test_model_call_counter_fixture_blocked_adapter_fails_closed(tmp_path: Path) -> None:
    report_path = tmp_path / "blocked.md"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "model_call_counter_fixture",
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
    assert "Return the current order status" not in completed.stderr
    assert not report_path.exists()


def test_model_call_counter_fixture_local_runtime_placeholder_fails_closed(
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "placeholder.md"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "model_call_counter_fixture",
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
    assert "Return the current order status" not in completed.stderr
    assert not report_path.exists()


def test_model_call_counter_fixture_unknown_adapter_lists_available_kinds() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "model_call_counter_fixture",
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


def test_model_call_counter_fixture_help_lists_available_adapter_kinds() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "model_call_counter_fixture",
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
