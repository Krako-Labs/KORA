import subprocess
import sys
from pathlib import Path

from kora.validation_report import render_local_validation_markdown


def _summary() -> dict[str, object]:
    return {
        "mode": "customer_support_triage_local_validation",
        "report_type": "local_no_network_validation_packet",
        "generated_at": "2026-05-09T00:00:00Z",
        "offline": True,
        "no_network": True,
        "no_provider_call": True,
        "fail_closed_status": "not_applicable_successful_local_adapter",
        "adapter": "local_validation",
        "workload_id": "customer_support_triage_synthetic_v1",
        "provider": "local_validation",
        "model": "deterministic-local",
        "privacy_class": "synthetic",
        "total_requests": 12,
        "baseline_model_calls": 12,
        "kora_model_calls": 4,
        "avoided_model_calls": 8,
        "avoided_model_call_rate": 2 / 3,
        "deterministic_routes": 8,
        "model_escalations": 4,
        "validation_pass_count": 12,
        "validation_fail_count": 0,
        "error_count": 0,
        "fallback_count": 0,
        "input_tokens_total": 50,
        "output_tokens_total": 50,
        "api_cost_evidence": False,
        "production_benchmark_evidence": False,
        "energy_evidence": False,
        "provider_fixture_dry_run_contract": {
            "fixture_contract_status": "passed",
            "fixture_version": "0.1",
            "provider_label": "local_validation",
            "model_label": "deterministic-local",
            "mode": "dry_run",
            "request_id": "customer_support_triage_local_validation_report",
            "baseline_candidate_events": 12,
            "kora_routed_events": 4,
            "avoided_model_call_events": 8,
            "provider_attempted_events": 0,
            "provider_blocked_events": 0,
            "no_network": True,
            "no_provider_call": True,
            "contains_real_provider_response": False,
            "contains_customer_data": False,
            "contains_secret_material": False,
            "notes": ["Synthetic metadata only."],
        },
        "command": "python3 -m kora run customer_support_triage_synthetic -- --offline",
        "notes": ["Synthetic workload only."],
    }


def test_render_local_validation_markdown_includes_core_sections() -> None:
    markdown = render_local_validation_markdown(_summary())

    assert "# Local No-Network Validation Report" in markdown
    assert "## Report Metadata" in markdown
    assert "## Summary" in markdown
    assert "## Counters" in markdown
    assert "## Adapter Selection Result" in markdown
    assert "## Provider Fixture Dry-Run Contract" in markdown
    assert "## Boundary" in markdown
    assert "## Interpretation" in markdown
    assert "## Explicit Non-Claims" in markdown
    assert "## Reproduction" in markdown
    assert "## Notes" in markdown


def test_render_local_validation_markdown_includes_required_counters() -> None:
    markdown = render_local_validation_markdown(_summary())

    assert "| `total_requests` | 12 |" in markdown
    assert "| `baseline_model_calls` | 12 |" in markdown
    assert "| `kora_model_calls` | 4 |" in markdown
    assert "| `avoided_model_calls` | 8 |" in markdown
    assert "| `avoided_model_call_rate` | 0.6667 |" in markdown
    assert "| `input_tokens_total` | 50 |" in markdown
    assert "| `output_tokens_total` | 50 |" in markdown


def test_render_local_validation_markdown_includes_report_packet_fields() -> None:
    markdown = render_local_validation_markdown(_summary())

    assert "- Report type: `local_no_network_validation_packet`" in markdown
    assert "- Adapter kind: `local_validation`" in markdown
    assert "- Provider label: `local_validation`" in markdown
    assert "- Model label: `deterministic-local`" in markdown
    assert "- Offline: `yes`" in markdown
    assert "- No network: `yes`" in markdown
    assert "- No real provider call: `yes`" in markdown
    assert "- Baseline candidate events: `12`" in markdown
    assert "- KORA routed events: `4`" in markdown
    assert "- Avoided model-call events: `8`" in markdown
    assert "- Fixture contract status: `passed`" in markdown
    assert "- No network: `yes`" in markdown
    assert "- No provider call: `yes`" in markdown
    assert "- Provider attempted events: `0`" in markdown


def test_render_local_validation_markdown_is_claim_safe() -> None:
    markdown = render_local_validation_markdown(_summary())

    assert "local no-network validation" in markdown
    assert "deterministic local validation adapter" in markdown
    assert "not real provider validation" in markdown
    assert "real API-cost reduction evidence" in markdown
    assert "production validation" in markdown
    assert "energy-reduction evidence" in markdown
    assert "raw prompts" in markdown
    assert "raw provider responses" in markdown
    assert "private user data" in markdown
    assert "no production cost reduction proof" in markdown
    assert "no real API-cost reduction proof" in markdown
    assert "no energy reduction evidence" in markdown


def test_render_local_validation_markdown_does_not_emit_raw_payloads() -> None:
    markdown = render_local_validation_markdown(_summary())

    assert "raw_prompt" not in markdown
    assert "raw_response" not in markdown
    assert "OPENAI_API_KEY" not in markdown
    assert "ANTHROPIC_API_KEY" not in markdown
    assert "reduces real API costs" not in markdown
    assert "reduces production AI costs" not in markdown
    assert "reduces energy consumption" not in markdown


def test_customer_support_example_writes_markdown_report(tmp_path: Path) -> None:
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
            "--report-md",
            str(report_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    report = report_path.read_text(encoding="utf-8")
    assert "# Local No-Network Validation Report" in report
    assert "| `total_requests` | 12 |" in report
    assert "| `kora_model_calls` | 4 |" in report
    assert "customer_support_triage_local_validation" in report
    assert "local_validation" in report
    assert "## Provider Fixture Dry-Run Contract" in report
    assert "- Adapter kind: `local_validation`" in report
    assert "- No network: `yes`" in report
    assert "- No provider call: `yes`" in report
    assert "no real API-cost reduction proof" in report


def test_real_model_call_example_writes_markdown_report(tmp_path: Path) -> None:
    report_path = tmp_path / "local_validation.md"

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kora",
            "run",
            "model_call_counter_fixture",
            "--",
            "--offline",
            "--report-md",
            str(report_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    report = report_path.read_text(encoding="utf-8")
    assert "# Local No-Network Validation Report" in report
    assert "| `total_requests` | 10 |" in report
    assert "| `kora_model_calls` | 4 |" in report
    assert "local_no_network_model_call_validation" in report
    assert "deterministic-local" in report
    assert "## Adapter Selection Result" in report
    assert "## Explicit Non-Claims" in report
