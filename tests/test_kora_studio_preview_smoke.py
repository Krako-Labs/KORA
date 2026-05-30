from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_kora_studio_preview.py"
SPEC = importlib.util.spec_from_file_location("check_kora_studio_preview", SCRIPT_PATH)
assert SPEC is not None
smoke = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(smoke)


class FakeHeaders(dict[str, str]):
    def get(self, key: str, default: str = "") -> str:
        return super().get(key, default)


class FakeResponse:
    def __init__(self, *, status: int, content_type: str, body: str) -> None:
        self.status = status
        self.headers = FakeHeaders({"Content-Type": content_type})
        self._body = body.encode("utf-8")

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        return None

    def read(self) -> bytes:
        return self._body


def _fake_opener(url: object, timeout: float) -> FakeResponse:
    assert timeout == 0.5
    if hasattr(url, "full_url"):
        request_url = str(getattr(url, "full_url"))
        if request_url.endswith("/api/harness/run"):
            return FakeResponse(
                status=200,
                content_type="application/json; charset=utf-8",
                body=json.dumps(
                    {
                        "run_status": "completed",
                        "run_id": "local-harness-trigger-test",
                        "request_id": "local-harness-json-required-fields-001",
                        "provider_calls_enabled": False,
                        "cloud_sync_enabled": False,
                        "model_execution_connected": False,
                        "download_connected": False,
                        "generated_events": [{"stage_id": "request_received"}],
                        "generated_counters": {"kora_model_calls": 0},
                    }
                ),
            )
        raise AssertionError(f"unexpected request URL: {request_url}")
    assert isinstance(url, str)
    if url.endswith("/health"):
        return FakeResponse(
            status=200,
            content_type="application/json; charset=utf-8",
            body=json.dumps(
                {
                    "server": "local-only",
                    "provider_calls_enabled": False,
                    "cloud_sync_enabled": False,
                }
            ),
        )
    if url.endswith("/status"):
        return FakeResponse(
            status=200,
            content_type="application/json; charset=utf-8",
            body=json.dumps(
                {
                    "studio_status": {},
                    "launch_boundary": {},
                    "system_profile": {},
                    "model_capability_estimate": {},
                    "runtime_status": [],
                    "installed_models_summary": {},
                    "model_catalog_status": "static_local_scaffold",
                    "recommended_models": [],
                    "setup_guidance_status": "informational_scaffold",
                    "disabled_action_state": {
                        "download_connected": False,
                        "run_connected": False,
                        "model_execution_connected": False,
                    },
                    "execution_viewer_status": "fixture_mock_scaffold",
                    "local_harness_status": {
                        "status": "local_deterministic_harness_available",
                        "run_trigger_status": "api_endpoint_connected",
                        "approved_request_ids_only": True,
                        "model_execution_connected": False,
                    },
                    "local_harness_sample_run": {"status": "completed"},
                    "local_harness_comparison": {"comparison_source": "local_harness_summary"},
                    "comparison_counters": {"kora_model_calls": 0},
                    "standard_vs_kora_comparison_status": "fixture_mock_scaffold",
                    "report_viewer_status": "local_harness_summary_placeholder",
                    "report_viewer_placeholder": {
                        "report_source": "local_harness_summary",
                        "arbitrary_local_file_scan_enabled": False,
                        "file_export_enabled": False,
                        "file_written": False,
                    },
                    "provider_calls_enabled": False,
                    "cloud_sync_enabled": False,
                    "claim_boundaries": {},
                }
            ),
        )
    if url.endswith("/api/harness/run/local-harness-trigger-test"):
        return FakeResponse(
            status=200,
            content_type="application/json; charset=utf-8",
            body=json.dumps(
                {
                    "run_id": "local-harness-trigger-test",
                    "model_execution_connected": False,
                }
            ),
        )
    if url.endswith("/api/harness/events?run_id=local-harness-trigger-test"):
        return FakeResponse(
            status=200,
            content_type="application/json; charset=utf-8",
            body=json.dumps(
                {
                    "run_id": "local-harness-trigger-test",
                    "event_count": 1,
                    "events": [{"stage_id": "request_received"}],
                    "sse_connected": False,
                    "model_execution_connected": False,
                }
            ),
        )
    if url.endswith("/api/harness/sse?run_id=local-harness-trigger-test"):
        return FakeResponse(
            status=200,
            content_type="text/event-stream; charset=utf-8",
            body=(
                "event: stream_started\n"
                'data: {"run_id":"local-harness-trigger-test","model_token_streaming_connected":false}\n\n'
                "event: harness_stage\n"
                'data: {"run_id":"local-harness-trigger-test","stage_id":"request_received"}\n\n'
                "event: stream_completed\n"
                'data: {"run_id":"local-harness-trigger-test","model_token_streaming_connected":false}\n\n'
            ),
        )
    if url.endswith("/"):
        return FakeResponse(
            status=200,
            content_type="text/html; charset=utf-8",
            body="""
            Launch / Local-only Status
            Your Computer
            Model Capability Estimate
            Runtime Status
            Catalog vs Installed
            Setup Guidance
            Disabled Download/Run Actions
            KORA Boost Boundary
            Local Harness Preview
            local_deterministic_harness_available
            local-harness-json-required-fields-001
            Local deterministic harness comparison
            Local Harness Summary Report
            Execution Viewer
            Standard Mode vs KORA Boost
            Report Viewer Placeholder
            Local Harness Report
            Report Metadata Preview
            Report metadata preview only
            Report Boundary
            Local deterministic harness output only
            Not production evidence
            No file export in this preview
            File export: disabled
            File written: false
            Approved Request Selector
            Interactive approved request selector
            Approved local harness requests only
            Approved request only
            Selected request preview
            Selector state is browser-local in-memory page state only
            Selected run state
            Generated local harness output only
            Selected Run Error State
            kora-run-error-state
            Retry Last Approved Request
            kora-retry-last-approved-request-button
            kora-last-approved-request-id
            Retry uses the last approved request only
            The local harness endpoint was unavailable
            The local response could not be parsed
            Local Run History
            kora-local-run-history
            kora-run-history-count
            Clear Local Run History
            kora-clear-run-history-button
            Browser-local run history
            Page-memory only
            Clears on refresh
            Cleared browser-local preview state only
            Selected Run Event Timeline
            kora-selected-run-events
            kora-selected-events-status
            No selected run events loaded yet
            Selected Run Counters
            kora-selected-run-counters
            kora-selected-counters-status
            Selected Run: Standard Mode vs KORA Boost
            kora-selected-run-comparison
            kora-selected-comparison-status
            Not production telemetry
            Not production cost evidence
            Selected Run Report Metadata
            kora-selected-run-report-metadata
            kora-selected-report-status
            Report metadata preview only
            No file export
            No file writing
            kora-run-local-harness-button
            data-kora-request-id
            fetch("/api/harness/run"
            fetch(`/api/harness/events?run_id=${encodeURIComponent(selectedRunId)}`)
            api_endpoint_connected
            Run Local Harness
            Approved deterministic sample requests only
            No arbitrary prompt execution
            Generated harness events only
            Model-needed boundary returns
            Generated Event Timeline
            Generated local harness events only
            Not model token streaming
            No provider output
            Generated Counters
            Local Harness Comparison boundary
            Comparison is generated from local deterministic harness output
            This is not production cost evidence
            This is local preview/demo data, not production evidence
            /api/harness/events
            /api/harness/sse
            Provider calls: disabled
            Cloud sync: disabled
            No model is downloaded
            No model is executed
            """,
        )
    raise AssertionError(f"unexpected URL: {url}")


def test_check_preview_uses_local_endpoints_only() -> None:
    results = smoke.check_preview("http://127.0.0.1:8765", timeout=0.5, opener=_fake_opener)

    assert results == [
        "/health ok",
        "/status ok",
        "/api/harness/run ok",
        "/api/harness/run/<run_id> ok",
        "/api/harness/events ok",
        "/api/harness/sse ok",
        "/ ok",
    ]


def test_check_preview_rejects_non_local_url() -> None:
    with pytest.raises(smoke.SmokeCheckError, match="only accepts"):
        smoke.check_preview("https://example.com", timeout=0.5, opener=_fake_opener)


def test_check_preview_fails_when_download_is_connected() -> None:
    def opener(url: str, timeout: float) -> FakeResponse:
        if url.endswith("/status"):
            response = _fake_opener(url, timeout)
            data = json.loads(response.read().decode("utf-8"))
            data["disabled_action_state"]["download_connected"] = True
            return FakeResponse(status=200, content_type="application/json", body=json.dumps(data))
        return _fake_opener(url, timeout)

    with pytest.raises(smoke.SmokeCheckError, match="download connected"):
        smoke.check_preview("http://localhost:8765", timeout=0.5, opener=opener)


def test_main_returns_failure_without_real_network() -> None:
    assert smoke.main(["--base-url", "https://example.com"]) == 1
