"""Local no-network customer-support triage validation example."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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

DEFAULT_WORKLOAD = Path("experiments/workloads/customer_support_triage_synthetic_v1.json")
CLAIM_BOUNDARY = (
    "This customer-support triage validation example uses synthetic data and local/"
    "no-network model-call events. It is not real provider validation, real API-cost "
    "validation, production validation, production cost reduction proof, broad "
    "workload superiority proof, or energy reduction evidence."
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _resolve_workload_path(path: Path) -> Path:
    if path.is_absolute():
        return path
    return _repo_root() / path


def load_workload(path: Path = DEFAULT_WORKLOAD) -> dict[str, Any]:
    workload_path = _resolve_workload_path(path)
    return json.loads(workload_path.read_text(encoding="utf-8"))


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


def _requests(workload: dict[str, Any]) -> list[dict[str, Any]]:
    requests = workload.get("requests")
    if not isinstance(requests, list):
        raise ValueError("customer-support triage workload must contain a requests list")
    return requests


def _model_request(item: dict[str, Any]) -> ModelCallRequest:
    return ModelCallRequest(
        request_id=str(item["request_id"]),
        prompt=str(item["input"]),
        privacy_class="synthetic",
        metadata={
            "route_class": item.get("route_class"),
            "expected_route": item.get("expected_route"),
            "validation_rule": item.get("validation_rule"),
        },
    )


def _run_direct_baseline(
    requests: list[dict[str, Any]],
    adapter: ModelCallAdapter,
) -> list[ModelCallResponse]:
    return [adapter.call(_model_request(item)) for item in requests]


def _validate_deterministic_route(item: dict[str, Any]) -> bool:
    return (
        item.get("expected_route") == "deterministic"
        and isinstance(item.get("deterministic_handler"), str)
        and bool(str(item.get("deterministic_handler")).strip())
        and isinstance(item.get("validation_rule"), str)
        and isinstance(item.get("expected_response_type"), str)
    )


def _validate_model_required_route(item: dict[str, Any], response: ModelCallResponse) -> bool:
    return (
        item.get("expected_route") == "model_required"
        and item.get("deterministic_handler") is None
        and response.model_calls == 1
        and bool(response.output)
    )


def _run_kora_controlled_path(
    requests: list[dict[str, Any]],
    adapter: ModelCallAdapter,
) -> tuple[list[ModelCallResponse], int, int, int, int, int, int]:
    model_responses: list[ModelCallResponse] = []
    deterministic_routes = 0
    model_escalations = 0
    validation_pass_count = 0
    validation_fail_count = 0
    error_count = 0
    fallback_count = 0

    for item in requests:
        try:
            expected_route = item.get("expected_route")
            if expected_route == "deterministic":
                deterministic_routes += 1
                if _validate_deterministic_route(item):
                    validation_pass_count += 1
                else:
                    validation_fail_count += 1
                continue

            if expected_route == "model_required":
                model_escalations += 1
                response = adapter.call(_model_request(item))
                model_responses.append(response)
                if _validate_model_required_route(item, response):
                    validation_pass_count += 1
                else:
                    validation_fail_count += 1
                continue

            fallback_count += 1
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
        fallback_count,
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
        "request_id": "customer_support_triage_local_validation_report",
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


def build_customer_support_triage_synthetic_summary(
    *,
    offline: bool = True,
    adapter_kind: str = LOCAL_VALIDATION_ADAPTER,
    workload_path: Path = DEFAULT_WORKLOAD,
) -> dict[str, Any]:
    if not offline:
        raise ValueError("customer_support_triage_synthetic supports --offline only")

    workload = load_workload(workload_path)
    requests = _requests(workload)
    baseline_adapter = _select_validation_adapter(adapter_kind)
    kora_adapter = _select_validation_adapter(adapter_kind)

    baseline_responses = _run_direct_baseline(requests, baseline_adapter)
    (
        kora_responses,
        deterministic_routes,
        model_escalations,
        validation_pass_count,
        validation_fail_count,
        error_count,
        fallback_count,
    ) = _run_kora_controlled_path(requests, kora_adapter)

    baseline_summary = ModelCallSummary.from_responses(baseline_responses)
    kora_summary = ModelCallSummary.from_responses(kora_responses, error_count=error_count)
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
        "mode": "customer_support_triage_local_validation",
        "offline": True,
        "no_network": True,
        "no_provider_call": True,
        "fail_closed_status": "not_applicable_successful_local_adapter",
        "workload_id": workload.get("workload_id"),
        "workload_path": str(workload_path),
        "privacy_class": workload.get("privacy_class"),
        "adapter": baseline_responses[0].metadata.get("adapter", adapter_kind),
        "provider": provider_label,
        "model": model_label,
        "total_requests": len(requests),
        "baseline_model_calls": baseline_summary.model_calls,
        "kora_model_calls": kora_summary.model_calls,
        "avoided_model_calls": avoided_model_calls,
        "avoided_model_call_rate": avoided_model_call_rate,
        "deterministic_routes": deterministic_routes,
        "model_escalations": model_escalations,
        "validation_pass_count": validation_pass_count,
        "validation_fail_count": validation_fail_count,
        "error_count": error_count,
        "fallback_count": fallback_count,
        "input_tokens_total": kora_summary.input_tokens_total,
        "output_tokens_total": kora_summary.output_tokens_total,
        "baseline_input_tokens_total": baseline_summary.input_tokens_total,
        "baseline_output_tokens_total": baseline_summary.output_tokens_total,
        "latency_total_ms": kora_summary.latency_total_ms,
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
            "python3 -m kora run customer_support_triage_synthetic -- "
            f"--offline --adapter {adapter_kind}"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "notes": [
            "Synthetic customer-support triage workload only.",
            "Direct baseline records selected local adapter model-call events for every request.",
            "KORA-controlled path validates deterministic routes without selected local adapter model-call events.",
            "Model-required routes use the selected local adapter through the provider-neutral boundary.",
            "No external APIs, network access, provider credentials, raw prompts, or raw provider responses are used.",
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the local no-network customer-support triage validation example."
    )
    parser.add_argument("--offline", action="store_true", help="required; run without network calls")
    parser.add_argument(
        "--workload",
        default=str(DEFAULT_WORKLOAD),
        help="Path to customer-support triage workload JSON.",
    )
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
        raise SystemExit("customer_support_triage_synthetic requires --offline.")

    try:
        summary = build_customer_support_triage_synthetic_summary(
            offline=True,
            adapter_kind=args.adapter,
            workload_path=Path(args.workload),
        )
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
