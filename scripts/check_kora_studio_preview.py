#!/usr/bin/env python3
"""Local-only smoke check for the KORA Studio preview server.

This helper checks an already-running localhost Studio preview. It does not
start services, call providers, download models, execute models, or scan local
model directories.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Callable
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "http://127.0.0.1:8765"
UrlOpen = Callable[..., Any]


class SmokeCheckError(RuntimeError):
    """Raised when the local preview smoke check fails."""


def _normalise_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def _require_local_url(base_url: str) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise SmokeCheckError("KORA Studio smoke check only accepts http://127.0.0.1 or http://localhost URLs.")


def _read_url(base_url: str, path: str, *, timeout: float, opener: UrlOpen = urlopen) -> tuple[int, str, str]:
    url = f"{_normalise_base_url(base_url)}{path}"
    try:
        with opener(url, timeout=timeout) as response:
            status = int(getattr(response, "status", 0))
            content_type = str(response.headers.get("Content-Type", ""))
            body = response.read().decode("utf-8")
    except URLError as exc:
        raise SmokeCheckError(f"Unable to reach {url}: {exc}") from exc
    except OSError as exc:
        raise SmokeCheckError(f"Unable to read {url}: {exc}") from exc
    return status, content_type, body


def _post_json(
    base_url: str,
    path: str,
    payload: dict[str, Any],
    *,
    timeout: float,
    opener: UrlOpen = urlopen,
) -> tuple[int, str, str]:
    url = f"{_normalise_base_url(base_url)}{path}"
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with opener(request, timeout=timeout) as response:
            status = int(getattr(response, "status", 0))
            content_type = str(response.headers.get("Content-Type", ""))
            body = response.read().decode("utf-8")
    except URLError as exc:
        raise SmokeCheckError(f"Unable to reach {url}: {exc}") from exc
    except OSError as exc:
        raise SmokeCheckError(f"Unable to read {url}: {exc}") from exc
    return status, content_type, body


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeCheckError(message)


def check_preview(base_url: str = DEFAULT_BASE_URL, *, timeout: float = 2.0, opener: UrlOpen = urlopen) -> list[str]:
    """Check local KORA Studio preview endpoints and return human-readable results."""

    base_url = _normalise_base_url(base_url)
    _require_local_url(base_url)

    results: list[str] = []

    health_status, health_content_type, health_body = _read_url(base_url, "/health", timeout=timeout, opener=opener)
    _require(health_status == 200, f"/health returned HTTP {health_status}")
    _require("application/json" in health_content_type, "/health did not return JSON")
    health = json.loads(health_body)
    _require(health.get("server") == "local-only", "/health does not report local-only server mode")
    _require(health.get("provider_calls_enabled") is False, "/health does not report provider calls disabled")
    _require(health.get("cloud_sync_enabled") is False, "/health does not report cloud sync disabled")
    results.append("/health ok")

    status_code, status_content_type, status_body = _read_url(base_url, "/status", timeout=timeout, opener=opener)
    _require(status_code == 200, f"/status returned HTTP {status_code}")
    _require("application/json" in status_content_type, "/status did not return JSON")
    status = json.loads(status_body)
    required_status_fields = {
        "studio_status",
        "launch_boundary",
        "system_profile",
        "model_capability_estimate",
        "runtime_status",
        "installed_models_summary",
        "model_catalog_status",
        "recommended_models",
        "setup_guidance_status",
        "disabled_action_state",
        "execution_viewer_status",
        "local_harness_status",
        "local_harness_sample_run",
        "local_harness_comparison",
        "comparison_counters",
        "standard_vs_kora_comparison_status",
        "report_viewer_status",
        "report_viewer_placeholder",
        "provider_calls_enabled",
        "cloud_sync_enabled",
        "claim_boundaries",
    }
    missing_fields = sorted(required_status_fields - set(status))
    _require(not missing_fields, f"/status missing fields: {', '.join(missing_fields)}")
    _require(status.get("provider_calls_enabled") is False, "/status does not report provider calls disabled")
    _require(status.get("cloud_sync_enabled") is False, "/status does not report cloud sync disabled")
    _require(status["disabled_action_state"].get("download_connected") is False, "/status reports download connected")
    _require(status["disabled_action_state"].get("run_connected") is False, "/status reports run connected")
    _require(
        status["disabled_action_state"].get("model_execution_connected") is False,
        "/status reports model execution connected",
    )
    _require(status.get("execution_viewer_status") == "fixture_mock_scaffold", "/status execution viewer is not fixture")
    _require(
        status["local_harness_status"].get("status") == "local_deterministic_harness_available",
        "/status local harness is not available",
    )
    _require(
        status["local_harness_status"].get("run_trigger_status") == "api_endpoint_connected",
        "/status local harness run trigger is not connected",
    )
    _require(
        status["local_harness_status"].get("approved_request_ids_only") is True,
        "/status does not restrict harness trigger to approved request IDs",
    )
    _require(
        status["local_harness_status"].get("model_execution_connected") is False,
        "/status local harness reports model execution connected",
    )
    _require(status["local_harness_sample_run"].get("status") == "completed", "/status local harness sample is not completed")
    _require(
        status["local_harness_comparison"].get("comparison_source") == "local_harness_summary",
        "/status local harness comparison source is not harness summary",
    )
    _require(status["comparison_counters"].get("kora_model_calls") == 0, "/status comparison reports KORA model calls")
    _require(
        status.get("standard_vs_kora_comparison_status") == "fixture_mock_scaffold",
        "/status comparison is not fixture",
    )
    _require(
        status.get("report_viewer_status") in {"fixture_metadata_placeholder", "local_harness_summary_placeholder"},
        "/status report viewer is not placeholder",
    )
    _require(
        status["report_viewer_placeholder"].get("report_source") == "local_harness_summary",
        "/status report source is not local harness summary",
    )
    _require(
        status["report_viewer_placeholder"].get("arbitrary_local_file_scan_enabled") is False,
        "/status report viewer scans arbitrary local files",
    )
    _require(
        status["report_viewer_placeholder"].get("file_export_enabled") is False,
        "/status report viewer reports file export enabled",
    )
    _require(
        status["report_viewer_placeholder"].get("file_written") is False,
        "/status report viewer reports a file was written",
    )
    results.append("/status ok")

    run_status, run_content_type, run_body = _post_json(
        base_url,
        "/api/harness/run",
        {"request_id": "local-harness-json-required-fields-001"},
        timeout=timeout,
        opener=opener,
    )
    _require(run_status == 200, f"/api/harness/run returned HTTP {run_status}")
    _require("application/json" in run_content_type, "/api/harness/run did not return JSON")
    run = json.loads(run_body)
    _require(run.get("run_status") == "completed", "/api/harness/run did not complete local harness run")
    _require(run.get("request_id") == "local-harness-json-required-fields-001", "/api/harness/run returned wrong request")
    _require(run.get("provider_calls_enabled") is False, "/api/harness/run reports provider calls enabled")
    _require(run.get("cloud_sync_enabled") is False, "/api/harness/run reports cloud sync enabled")
    _require(run.get("model_execution_connected") is False, "/api/harness/run reports model execution connected")
    _require(run.get("download_connected") is False, "/api/harness/run reports download connected")
    _require(run.get("generated_events"), "/api/harness/run did not return generated events")
    _require(run.get("generated_counters", {}).get("kora_model_calls") == 0, "/api/harness/run reports KORA model calls")
    results.append("/api/harness/run ok")

    run_id = str(run.get("run_id", ""))
    _require(run_id, "/api/harness/run did not return run_id")
    retrieved_status, retrieved_content_type, retrieved_body = _read_url(
        base_url,
        f"/api/harness/run/{run_id}",
        timeout=timeout,
        opener=opener,
    )
    _require(retrieved_status == 200, f"/api/harness/run/<run_id> returned HTTP {retrieved_status}")
    _require("application/json" in retrieved_content_type, "/api/harness/run/<run_id> did not return JSON")
    retrieved_run = json.loads(retrieved_body)
    _require(retrieved_run.get("run_id") == run_id, "/api/harness/run/<run_id> returned wrong run")
    _require(retrieved_run.get("model_execution_connected") is False, "/api/harness/run/<run_id> reports model execution")
    results.append("/api/harness/run/<run_id> ok")

    events_status, events_content_type, events_body = _read_url(
        base_url,
        f"/api/harness/events?run_id={run_id}",
        timeout=timeout,
        opener=opener,
    )
    _require(events_status == 200, f"/api/harness/events returned HTTP {events_status}")
    _require("application/json" in events_content_type, "/api/harness/events did not return JSON")
    events_payload = json.loads(events_body)
    _require(events_payload.get("run_id") == run_id, "/api/harness/events returned wrong run")
    _require(events_payload.get("event_count") == len(events_payload.get("events", [])), "/api/harness/events count mismatch")
    _require(events_payload.get("sse_connected") is False, "/api/harness/events reports SSE connected")
    _require(events_payload.get("model_execution_connected") is False, "/api/harness/events reports model execution")
    results.append("/api/harness/events ok")

    sse_status, sse_content_type, sse_body = _read_url(
        base_url,
        f"/api/harness/sse?run_id={run_id}",
        timeout=timeout,
        opener=opener,
    )
    _require(sse_status == 200, f"/api/harness/sse returned HTTP {sse_status}")
    _require("text/event-stream" in sse_content_type, "/api/harness/sse did not return an SSE content type")
    _require("event: stream_started" in sse_body, "/api/harness/sse missing stream_started event")
    _require("event: harness_stage" in sse_body, "/api/harness/sse missing harness_stage events")
    _require("event: stream_completed" in sse_body, "/api/harness/sse missing stream_completed event")
    _require(run_id in sse_body, "/api/harness/sse returned wrong run")
    _require("model_token_streaming_connected" in sse_body, "/api/harness/sse missing model token boundary")
    _require("provider output" not in sse_body.lower(), "/api/harness/sse appears to stream provider output")
    results.append("/api/harness/sse ok")

    root_status, root_content_type, root_body = _read_url(base_url, "/", timeout=timeout, opener=opener)
    _require(root_status == 200, f"/ returned HTTP {root_status}")
    _require("text/html" in root_content_type, "/ did not return HTML")
    required_html_markers = [
        'data-kora-final-ui-shell="true"',
        "KORA Studio left mini rail",
        "New task",
        "Search tasks",
        "Local workspace",
        "Cloud sync disabled",
        "Search or select open-source LLM",
        "KORA Studio top bar",
        "KORA Studio centered composer",
        "What do you want to work on?",
        "Choose a local model once. KORA keeps routing details out of the way.",
        "Ask KORA...",
        "Provider calls disabled",
        "Model execution not connected yet",
        "KORA Studio right details drawer scaffold",
        "Inspector · local preview",
        'data-kora-drawer-section="runtime-status"',
        'data-kora-drawer-section="selected-model"',
        'data-kora-drawer-section="catalog-vs-installed"',
        'data-kora-drawer-section="route-trace"',
        'data-kora-drawer-section="generated-counters"',
        'data-kora-drawer-section="report-metadata"',
        'data-kora-drawer-section="claim-boundaries"',
        "Selection does not install or run a model",
        "Route trace",
        "Generated harness events only.",
        "Report metadata",
        "File export:",
        "File written:",
        "Claim boundaries",
        "legacy-preview",
        "Launch / Local-only Status",
        "Your Computer",
        "Model Capability Estimate",
        "Runtime Status",
        "Catalog vs Installed",
        "Setup Guidance",
        "Disabled Download/Run Actions",
        "KORA Boost Boundary",
        "Local Harness Preview",
        "local_deterministic_harness_available",
        "local-harness-json-required-fields-001",
        "Local deterministic harness comparison",
        "Local Harness Summary Report",
        "Execution Viewer",
        "Standard Mode vs KORA Boost",
        "Report Viewer Placeholder",
        "Local Harness Report",
        "Report Metadata Preview",
        "Report metadata preview only",
        "Report Boundary",
        "Local deterministic harness output only",
        "Not production evidence",
        "No file export in this preview",
        "File export: disabled",
        "File written: false",
        "Approved Request Selector",
        "Interactive approved request selector",
        "Approved local harness requests only",
        "Approved request only",
        "Selected request preview",
        "Selector state is browser-local in-memory page state only",
        "Selected run state",
        "Generated local harness output only",
        "Selected Run Error State",
        "kora-run-error-state",
        "Retry Last Approved Request",
        "kora-retry-last-approved-request-button",
        "kora-last-approved-request-id",
        "Retry uses the last approved request only",
        "The local harness endpoint was unavailable",
        "The local response could not be parsed",
        "Local Run History",
        "kora-local-run-history",
        "kora-run-history-count",
        "Clear Local Run History",
        "kora-clear-run-history-button",
        "Browser-local run history",
        "Page-memory only",
        "Clears on refresh",
        "kora-active-history-run-id",
        "History cards show compact counters from generated harness output only",
        "Compact counters: avoided_model_calls=",
        "Active selected local run",
        "Selected in page",
        "Cleared browser-local preview state only",
        "No backend records, files, report exports, or server endpoints were deleted",
        "Generated Event Stream",
        "kora-sse-status",
        "kora-sse-fallback-used",
        "kora-sse-error",
        "Fallback to local events endpoint available",
        "No provider streaming",
        "new EventSource(`/api/harness/sse?run_id=${encodeURIComponent(selectedRunId)}`)",
        "Selected Run Event Timeline",
        "kora-selected-run-events",
        "kora-selected-events-status",
        "No selected run events loaded yet",
        "Selected Run Counters",
        "kora-selected-run-counters",
        "kora-selected-counters-status",
        "Selected Run: Standard Mode vs KORA Boost",
        "kora-selected-run-comparison",
        "kora-selected-comparison-status",
        "Not production telemetry",
        "Not production cost evidence",
        "Selected Run Report Metadata",
        "kora-selected-run-report-metadata",
        "kora-selected-report-status",
        "Report metadata preview only",
        "No file export",
        "No file writing",
        "kora-run-local-harness-button",
        "data-kora-request-id",
        'fetch("/api/harness/run"',
        "fetch(`/api/harness/events?run_id=${encodeURIComponent(selectedRunId)}`)",
        "api_endpoint_connected",
        "Run Local Harness",
        "Approved deterministic sample requests only",
        "No arbitrary prompt execution",
        "Generated harness events only",
        "Model-needed boundary returns",
        "Generated Event Timeline",
        "Generated local harness events only",
        "Not model token streaming",
        "No provider output",
        "Generated Counters",
        "Local Harness Comparison boundary",
        "Comparison is generated from local deterministic harness output",
        "This is not production cost evidence",
        "This is local preview/demo data, not production evidence",
        "/api/harness/events",
        "/api/harness/sse",
        "Provider calls: disabled",
        "Cloud sync: disabled",
        "No model is downloaded",
        "No model is executed",
    ]
    missing_markers = [marker for marker in required_html_markers if marker not in root_body]
    _require(not missing_markers, f"/ missing markers: {', '.join(missing_markers)}")
    _require("Download now" not in root_body, "/ includes an active download phrase")
    _require("Run now" not in root_body, "/ includes an active run phrase")
    _require("Install now" not in root_body, "/ includes an active install phrase")
    results.append("/ ok")

    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smoke-check an already-running local KORA Studio preview.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Local Studio base URL.")
    parser.add_argument("--timeout", type=float, default=2.0, help="Per-request timeout in seconds.")
    args = parser.parse_args(argv)

    try:
        results = check_preview(args.base_url, timeout=args.timeout)
    except SmokeCheckError as exc:
        print(f"KORA Studio preview smoke check failed: {exc}", file=sys.stderr)
        return 1

    print("KORA Studio preview smoke check passed.")
    for result in results:
        print(f"- {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
