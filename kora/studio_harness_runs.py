"""Local-only run trigger scaffold for KORA Studio harness requests."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from kora.studio_harness_comparison import build_local_harness_comparison
from kora.studio_harness_events import LOCAL_HARNESS_EVENT_CLAIM_BOUNDARY, build_local_harness_events
from kora.studio_harness_requests import get_local_harness_request_by_id
from kora.studio_report_viewer import get_report_viewer_status_fields

LOCAL_HARNESS_RUN_CLAIM_BOUNDARY = (
    "Local harness runs are generated only from approved synthetic deterministic request IDs. They do not "
    "execute models, call providers, download models, scan private data, list runtime models, or prove "
    "production behavior."
)

_LOCAL_HARNESS_RUNS: dict[str, dict[str, Any]] = {}


def _counter_summary(counters: dict[str, Any]) -> dict[str, Any]:
    return {
        "total_requests": counters.get("total_requests", 0),
        "baseline_model_calls": counters.get("baseline_model_calls", 0),
        "kora_model_calls": counters.get("kora_model_calls", 0),
        "avoided_model_calls": counters.get("avoided_model_calls", 0),
        "deterministic_routes": counters.get("deterministic_routes", 0),
        "structured_lookup_routes": counters.get("structured_lookup_routes", 0),
        "policy_routes": counters.get("policy_routes", 0),
        "model_escalations": counters.get("model_escalations", 0),
        "validation_pass_count": counters.get("validation_pass_count", 0),
        "validation_fail_count": counters.get("validation_fail_count", 0),
    }


def _report_metadata_summary(
    *,
    report_fields: dict[str, Any],
    run_id: str,
    request_id: str,
    created_at: str,
    completed_at: str,
    event_count: int,
    counters: dict[str, Any],
    comparison_status: str,
    model_execution_status: str,
) -> dict[str, Any]:
    viewer = report_fields["report_viewer_placeholder"]
    export = report_fields["report_export_placeholder"]
    return {
        "report_status": viewer["report_status"],
        "report_viewer_status": report_fields["report_viewer_status"],
        "report_source": viewer["report_source"],
        "report_source_detail": "local deterministic harness output / fixture metadata",
        "run_id": run_id,
        "request_id": request_id,
        "created_at": created_at,
        "generated_at": completed_at,
        "event_count": event_count,
        "counter_summary": _counter_summary(counters),
        "comparison_summary_status": comparison_status,
        "model_execution_status": model_execution_status,
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "file_export_enabled": False,
        "file_written": False,
        "report_export_status": report_fields["report_export_status"],
        "export_action_enabled": export["export_action_enabled"],
        "writes_generated_reports": export["writes_generated_reports"],
        "uploads_reports": export["uploads_reports"],
        "commits_generated_reports": export["commits_generated_reports"],
        "arbitrary_local_file_scan_enabled": False,
        "upload_enabled": False,
        "generated_report_commit_enabled": False,
        "production_evidence_claim": False,
        "cost_claim_enabled": False,
        "energy_claim_enabled": False,
        "claim_boundary": report_fields["report_viewer_claim_boundary"],
        "export_claim_boundary": report_fields["report_export_claim_boundary"],
    }


def _selected_request_summary(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "request_id": request["request_id"],
        "input_text": request["input_text"],
        "task_family": request["task_family"],
        "expected_route_class": request["expected_route_class"],
        "expected_validation_result": request["expected_validation_result"],
        "expected_model_needed": request["expected_model_needed"],
        "claim_boundary": request["claim_boundary"],
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "model_execution_connected": False,
        "download_connected": False,
    }


def clear_local_harness_run_records() -> None:
    """Clear in-memory run records for tests."""

    _LOCAL_HARNESS_RUNS.clear()


def trigger_local_harness_run(request_id: str) -> dict[str, Any]:
    """Generate a local harness run for an approved deterministic sample request."""

    selected_request = get_local_harness_request_by_id(request_id)
    if selected_request is None:
        raise ValueError(f"Unknown approved local harness request id: {request_id}")

    created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    run_id = f"local-harness-trigger-{uuid4().hex}"
    harness_run = build_local_harness_events(selected_request, run_id=run_id)
    comparison = build_local_harness_comparison(selected_request)
    report_fields = get_report_viewer_status_fields(
        harness_run["counters_snapshot"],
        report_source="local_harness_summary",
    )
    generated_events = deepcopy(harness_run["events"])
    generated_counters = deepcopy(harness_run["counters_snapshot"])
    model_needed = bool(selected_request["expected_model_needed"])
    model_execution_status = "execution_not_connected" if model_needed else "not_needed"
    completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    event_count = len(generated_events)
    comparison_status = str(comparison["comparison_status"])
    report_metadata_summary = _report_metadata_summary(
        report_fields=report_fields,
        run_id=run_id,
        request_id=str(selected_request["request_id"]),
        created_at=created_at,
        completed_at=completed_at,
        event_count=event_count,
        counters=generated_counters,
        comparison_status=comparison_status,
        model_execution_status=model_execution_status,
    )

    run_record = {
        "ok": True,
        "run_id": run_id,
        "request_id": selected_request["request_id"],
        "run_status": "completed",
        "run_state": "completed",
        "created_at": created_at,
        "completed_at": completed_at,
        "selected_request": _selected_request_summary(selected_request),
        "generated_events": generated_events,
        "generated_counters": generated_counters,
        "comparison_summary": {
            "comparison_status": comparison["comparison_status"],
            "comparison_source": comparison["comparison_source"],
            "request_id": comparison["request_id"],
            "metrics": deepcopy(comparison["metrics"]),
            "comparison_counters": deepcopy(comparison["comparison_counters"]),
            "claim_boundary": comparison["claim_boundary"],
            "provider_calls_enabled": False,
            "cloud_sync_enabled": False,
            "model_execution_connected": False,
            "download_connected": False,
        },
        "report_metadata_summary": report_metadata_summary,
        "event_count": event_count,
        "model_needed_boundary_status": "execution_not_connected" if model_needed else "not_needed",
        "model_execution_status": model_execution_status,
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "model_execution_connected": False,
        "download_connected": False,
        "runtime_model_list_connected": False,
        "private_directory_scan_enabled": False,
        "error": None,
        "claim_boundary": LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
        "event_claim_boundary": LOCAL_HARNESS_EVENT_CLAIM_BOUNDARY,
    }
    _LOCAL_HARNESS_RUNS[run_id] = deepcopy(run_record)
    return deepcopy(run_record)


def get_local_harness_run_record(run_id: str) -> dict[str, Any] | None:
    """Return an in-memory local harness run record by id."""

    record = _LOCAL_HARNESS_RUNS.get(run_id)
    return deepcopy(record) if record is not None else None


def get_local_harness_run_events(run_id: str) -> dict[str, Any] | None:
    """Return generated event payload for an in-memory local harness run."""

    record = get_local_harness_run_record(run_id)
    if record is None:
        return None
    events = deepcopy(record["generated_events"])
    return {
        "ok": True,
        "run_id": record["run_id"],
        "request_id": record["request_id"],
        "run_status": record["run_status"],
        "event_count": len(events),
        "events": events,
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "model_execution_connected": False,
        "download_connected": False,
        "streaming_connected": False,
        "sse_connected": False,
        "claim_boundary": LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
        "event_claim_boundary": LOCAL_HARNESS_EVENT_CLAIM_BOUNDARY,
    }


def format_local_harness_sse(run_id: str) -> str | None:
    """Return a Server-Sent Events stream for generated local harness events."""

    record = get_local_harness_run_record(run_id)
    if record is None:
        return None

    def sse_event(event_name: str, payload: dict[str, Any]) -> str:
        return f"event: {event_name}\ndata: {json_dumps(payload)}\n\n"

    chunks = [
        sse_event(
            "stream_started",
            {
                "run_id": record["run_id"],
                "request_id": record["request_id"],
                "run_status": record["run_status"],
                "event_count": record["event_count"],
                "stream_type": "generated_local_harness_events",
                "provider_calls_enabled": False,
                "cloud_sync_enabled": False,
                "model_execution_connected": False,
                "download_connected": False,
                "model_token_streaming_connected": False,
                "claim_boundary": LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
            },
        )
    ]
    for event in record["generated_events"]:
        chunks.append(
            sse_event(
                "harness_stage",
                {
                    "run_id": record["run_id"],
                    "request_id": record["request_id"],
                    "stage_id": event["stage_id"],
                    "stage_name": event["stage_name"],
                    "route_class": event["route_class"],
                    "status": event["status"],
                    "event": event,
                    "provider_calls_enabled": False,
                    "cloud_sync_enabled": False,
                    "model_execution_connected": False,
                    "download_connected": False,
                    "model_token_streaming_connected": False,
                    "claim_boundary": LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
                },
            )
        )
    chunks.append(
        sse_event(
            "stream_completed",
            {
                "run_id": record["run_id"],
                "request_id": record["request_id"],
                "run_status": record["run_status"],
                "event_count": record["event_count"],
                "stream_type": "generated_local_harness_events",
                "provider_calls_enabled": False,
                "cloud_sync_enabled": False,
                "model_execution_connected": False,
                "download_connected": False,
                "model_token_streaming_connected": False,
                "claim_boundary": LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
            },
        )
    )
    return "".join(chunks)


def json_dumps(payload: dict[str, Any]) -> str:
    """Serialize SSE payload data deterministically."""

    import json

    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def get_local_harness_run_store_status() -> dict[str, Any]:
    """Return claim-safe in-memory run store metadata."""

    return {
        "run_store_status": "in_memory_local_only",
        "run_store_record_count": len(_LOCAL_HARNESS_RUNS),
        "persistence_enabled": False,
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "model_execution_connected": False,
        "download_connected": False,
        "claim_boundary": LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
    }
