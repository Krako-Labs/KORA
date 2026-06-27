"""Local no-network model-call validation example.

This example exercises the provider-neutral model-call adapter boundary with
synthetic data only. It is intended to validate local model-call counters before
real local or remote provider adapters are added.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from kora.model_call import (
    DeterministicStubModelCallAdapter,
    DeterministicLocalRuntimeModelCallAdapter,
    LOCAL_VALIDATION_ADAPTER,
    ModelCallRequest,
    ModelCallResponse,
    ModelCallAdapter,
    ModelCallSummary,
    available_model_call_adapters,
    select_model_call_adapter,
)
from kora.provider_fixture import validate_provider_fixture
from kora.validation_report import render_local_validation_markdown

Route = Literal["deterministic", "model_required"]

CLAIM_BOUNDARY = (
    "This local/no-network validation example tests the measured model-call "
    "counter path. It is not real provider validation, real API-cost validation, "
    "production validation, production cost reduction proof, broad workload "
    "superiority proof, or energy reduction evidence."
)


@dataclass(frozen=True)
class SyntheticRequest:
    request_id: str
    input: str
    expected_route: Route
    expected_output: str | None
    privacy_class: str = "synthetic"


WORKLOAD: tuple[SyntheticRequest, ...] = (
    SyntheticRequest(
        request_id="req-001",
        input="Return the current order status label for delivered.",
        expected_route="deterministic",
        expected_output="status:delivered",
    ),
    SyntheticRequest(
        request_id="req-002",
        input="Normalize the refund-policy category.",
        expected_route="deterministic",
        expected_output="category:refund_policy",
    ),
    SyntheticRequest(
        request_id="req-003",
        input="Route a billing receipt request.",
        expected_route="deterministic",
        expected_output="route:billing_receipt",
    ),
    SyntheticRequest(
        request_id="req-004",
        input="Classify a password reset request.",
        expected_route="deterministic",
        expected_output="route:account_recovery",
    ),
    SyntheticRequest(
        request_id="req-005",
        input="Identify a shipping-address update.",
        expected_route="deterministic",
        expected_output="route:shipping_update",
    ),
    SyntheticRequest(
        request_id="req-006",
        input="Return a canned support-hours answer.",
        expected_route="deterministic",
        expected_output="answer:support_hours",
    ),
    SyntheticRequest(
        request_id="req-007",
        input="Draft a nuanced apology for a delayed enterprise shipment.",
        expected_route="model_required",
        expected_output=None,
    ),
    SyntheticRequest(
        request_id="req-008",
        input="Summarize an ambiguous customer escalation note.",
        expected_route="model_required",
        expected_output=None,
    ),
    SyntheticRequest(
        request_id="req-009",
        input="Generate a context-aware response for a billing dispute.",
        expected_route="model_required",
        expected_output=None,
    ),
    SyntheticRequest(
        request_id="req-010",
        input="Explain an edge-case refund decision in plain language.",
        expected_route="model_required",
        expected_output=None,
    ),
)


def _select_validation_adapter(kind: str) -> ModelCallAdapter:
    adapter = select_model_call_adapter(kind)
    if kind != LOCAL_VALIDATION_ADAPTER:
        adapter.call(
            ModelCallRequest(
                request_id="adapter-selection-check",
                prompt="",
                privacy_class="synthetic",
                metadata={"purpose": "adapter_selection_check"},
            )
        )
    if not isinstance(
        adapter,
        (DeterministicStubModelCallAdapter, DeterministicLocalRuntimeModelCallAdapter),
    ):
        supported = ", ".join(available_model_call_adapters())
        raise ValueError(f"Unsupported validation adapter {kind!r}. Supported: {supported}")
    return adapter


def _model_request(item: SyntheticRequest) -> ModelCallRequest:
    return ModelCallRequest(
        request_id=item.request_id,
        prompt=item.input,
        privacy_class=item.privacy_class,
        metadata={"expected_route": item.expected_route},
    )


def _run_direct_baseline(
    workload: tuple[SyntheticRequest, ...],
    adapter: ModelCallAdapter,
) -> list[ModelCallResponse]:
    return [adapter.call(_model_request(item)) for item in workload]


def _run_deterministic_handler(item: SyntheticRequest) -> str:
    if item.expected_output is None:
        raise ValueError(f"deterministic request {item.request_id} has no expected output")
    return item.expected_output


def _run_kora_controlled_path(
    workload: tuple[SyntheticRequest, ...],
    adapter: ModelCallAdapter,
) -> tuple[list[ModelCallResponse], int, int, int, int, int]:
    model_responses: list[ModelCallResponse] = []
    deterministic_routes = 0
    model_escalations = 0
    validation_pass_count = 0
    validation_fail_count = 0
    error_count = 0

    for item in workload:
        try:
            if item.expected_route == "deterministic":
                deterministic_routes += 1
                output = _run_deterministic_handler(item)
                if output == item.expected_output:
                    validation_pass_count += 1
                else:
                    validation_fail_count += 1
                continue

            model_escalations += 1
            response = adapter.call(_model_request(item))
            model_responses.append(response)
            if response.output:
                validation_pass_count += 1
            else:
                validation_fail_count += 1
        except Exception:
            error_count += 1

    return (
        model_responses,
        deterministic_routes,
        model_escalations,
        validation_pass_count,
        validation_fail_count,
        error_count,
    )


def _generated_at() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _provider_fixture_contract_fields(
    *,
    provider_label: str,
    model_label: str,
    baseline_candidate_events: int,
    kora_routed_events: int,
    avoided_model_call_events: int,
) -> dict[str, Any]:
    fixture = {
        "fixture_version": "0.1",
        "provider_label": provider_label,
        "model_label": model_label,
        "mode": "dry_run",
        "request_id": "real_model_call_local_validation_report",
        "baseline_candidate_events": baseline_candidate_events,
        "kora_routed_events": kora_routed_events,
        "avoided_model_call_events": avoided_model_call_events,
        "provider_attempted_events": 0,
        "provider_blocked_events": 0,
        "no_network": True,
        "no_provider_call": True,
        "contains_real_provider_response": False,
        "contains_customer_data": False,
        "contains_secret_material": False,
        "notes": [
            "Generated from aggregate local/no-network validation counters.",
            "No provider request, provider response, credential, or customer data is included.",
        ],
    }
    return validate_provider_fixture(fixture).report_fields()


def build_model_call_counter_fixture_summary(
    *,
    offline: bool = True,
    adapter_kind: str = LOCAL_VALIDATION_ADAPTER,
    workload: tuple[SyntheticRequest, ...] = WORKLOAD,
) -> dict[str, Any]:
    if not offline:
        raise ValueError("model_call_counter_fixture supports --offline only")

    baseline_adapter = _select_validation_adapter(adapter_kind)
    kora_adapter = _select_validation_adapter(adapter_kind)

    baseline_responses = _run_direct_baseline(workload, baseline_adapter)
    (
        kora_responses,
        deterministic_routes,
        model_escalations,
        validation_pass_count,
        validation_fail_count,
        error_count,
    ) = _run_kora_controlled_path(workload, kora_adapter)

    baseline_summary = ModelCallSummary.from_responses(baseline_responses)
    kora_summary = ModelCallSummary.from_responses(kora_responses, error_count=error_count)
    total_requests = len(workload)
    avoided_model_calls = baseline_summary.model_calls - kora_summary.model_calls
    avoided_model_call_rate = (
        avoided_model_calls / baseline_summary.model_calls
        if baseline_summary.model_calls
        else 0.0
    )
    provider_label = baseline_responses[0].provider
    model_label = baseline_responses[0].model

    return {
        "report_type": "local_no_network_validation_packet",
        "generated_at": _generated_at(),
        "ok": error_count == 0 and validation_fail_count == 0,
        "mode": "local_no_network_model_call_validation",
        "offline": True,
        "no_network": True,
        "no_provider_call": True,
        "fail_closed_status": "not_applicable_successful_local_adapter",
        "adapter": baseline_responses[0].metadata.get("adapter", adapter_kind),
        "provider": provider_label,
        "model": model_label,
        "total_requests": total_requests,
        "baseline_model_calls": baseline_summary.model_calls,
        "kora_model_calls": kora_summary.model_calls,
        "avoided_model_calls": avoided_model_calls,
        "avoided_model_call_rate": avoided_model_call_rate,
        "deterministic_routes": deterministic_routes,
        "model_escalations": model_escalations,
        "validation_pass_count": validation_pass_count,
        "validation_fail_count": validation_fail_count,
        "error_count": error_count,
        "fallback_count": 0,
        "input_tokens_total": kora_summary.input_tokens_total,
        "output_tokens_total": kora_summary.output_tokens_total,
        "baseline_input_tokens_total": baseline_summary.input_tokens_total,
        "baseline_output_tokens_total": baseline_summary.output_tokens_total,
        "latency_total_ms": kora_summary.latency_total_ms,
        "privacy_class": "synthetic",
        "raw_prompts_emitted": False,
        "raw_responses_emitted": False,
        "api_cost_evidence": False,
        "production_benchmark_evidence": False,
        "energy_evidence": False,
        "provider_fixture_dry_run_contract": _provider_fixture_contract_fields(
            provider_label=provider_label,
            model_label=model_label,
            baseline_candidate_events=baseline_summary.model_calls,
            kora_routed_events=kora_summary.model_calls,
            avoided_model_call_events=avoided_model_calls,
        ),
        "command": (
            "python3 -m kora run model_call_counter_fixture -- "
            f"--offline --adapter {adapter_kind}"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "notes": [
            "Synthetic workload only.",
            "Direct baseline records selected local adapter model-call events for every request.",
            "KORA-controlled path handles deterministic routes without selected local adapter model-call events.",
            "Model-required routes use the selected local adapter through the provider-neutral boundary.",
            "No external APIs, network access, provider credentials, raw prompts, or raw provider responses are used.",
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local no-network model-call validation example."
    )
    parser.add_argument("--offline", action="store_true", help="required; run without network calls")
    parser.add_argument(
        "--report-md",
        default=None,
        help="Optional path for a generated Markdown report.",
    )
    parser.add_argument(
        "--adapter",
        default=LOCAL_VALIDATION_ADAPTER,
        choices=available_model_call_adapters(),
        help="Model-call adapter kind for local validation.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.offline:
        raise SystemExit("model_call_counter_fixture requires --offline.")

    try:
        summary = build_model_call_counter_fixture_summary(offline=True, adapter_kind=args.adapter)
    except (RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    if args.report_md:
        report_path = Path(args.report_md)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_local_validation_markdown(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
