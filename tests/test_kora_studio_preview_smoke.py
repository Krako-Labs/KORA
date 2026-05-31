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
            data-kora-component="shell-layout"
            data-kora-component="left-rail"
            data-kora-component="boundary-strip"
            data-kora-component="top-model-selector"
            data-kora-component="composer"
            data-kora-component="approved-request-selector"
            data-kora-component="selected-run-summary"
            data-kora-component="selected-run-event-timeline"
            data-kora-component="selected-run-counters"
            data-kora-component="selected-run-comparison"
            data-kora-component="selected-run-report-metadata"
            data-kora-component="right-details-drawer"
            data-kora-component="run-history"
            data-kora-component="retry-error-state"
            data-kora-component="generated-event-stream-status"
            data-kora-component="legacy-compatibility-reference"
            data-kora-final-ui-shell="true"
            data-kora-v1-preview-readiness="shell-first-boundary-consolidation"
            data-kora-v1-shell-local-only-status="visible"
            data-kora-v1-1-shell-only-hardening="active"
            data-kora-v1-1-shell-only-coverage="boundaries,drawer-diagnostics,selected-run,legacy-secondary"
            <details class="legacy-preview"
            data-kora-responsive-shell="mobile-overlay-ready"
            data-kora-mobile-visual-qa="v0.9"
            data-kora-mobile-breakpoint="max-width-760"
            data-kora-mobile-qa-surfaces="left-rail,model-selector,composer,right-drawer,boundary-pills"
            data-kora-mobile-no-overlap-contract="true"
            data-kora-keyboard-focus-pass="true"
            data-kora-focus-visible-controls="shell-and-harness"
            KORA Studio left mini rail
            data-kora-mobile-rail="collapsed-overlay"
            data-kora-rail-open="false"
            kora-left-rail
            data-kora-rail-state
            kora-left-rail-toggle
            aria-controls="kora-left-rail"
            data-kora-rail-toggle
            kora-left-rail-close
            data-kora-rail-close
            setLeftRailOpen
            isSmallRailViewport
            Open left rail
            Close left rail
            New task
            Search tasks
            Local workspace
            Cloud sync disabled
            Search or select open-source LLM
            data-kora-model-selector="local-catalog-scaffold"
            data-kora-mobile-selector="compact-overlay-menu"
            data-kora-model-selection-state="catalog-estimate-only"
            aria-describedby="kora-model-selector-boundary"
            kora-model-selector-boundary
            data-kora-model-selector-menu="true"
            data-kora-model-selected-estimate="true"
            data-kora-model-selected-label="catalog-estimate-only"
            data-kora-model-selection-status="selected-estimate"
            aria-selected="true"
            data-kora-model-option-state="catalog-estimate-only"
            Catalog-only estimate selected
            Selected local fit estimate; catalog-only state
            Catalog estimate option; not installed or executed by selection
            data-kora-model-option="true"
            Selected estimate: Example mini local model
            Catalog suggestions are local static examples, not installed models
            Selecting a model here does not install, download, or execute it
            Selection does not install, download, or execute this model
            Recommended local catalog options shown:
            KORA Studio top bar
            KORA Studio centered composer
            What do you want to work on?
            Choose a local model once. KORA keeps routing details out of the way.
            Ask KORA...
            kora-composer-run-local-harness-button
            Composer action uses the selected approved local harness request only
            Composer selected-run summary
            kora-composer-selected-run-summary
            kora-composer-request-id
            kora-composer-run-status
            kora-composer-run-id
            data-kora-shell-selected-run-surface="v1.0"
            data-kora-shell-selected-run-coverage="timeline,counters,comparison,report-metadata"
            data-kora-v1-1-selected-run-polish="shell-drawer-status"
            Selected run details
            kora-shell-selected-timeline-status
            kora-shell-selected-counters-status
            kora-shell-selected-comparison-status
            kora-shell-selected-report-status
            Shell selected-run surface mirrors generated local harness output only
            Details drawer mirrors the same selected-run status so legacy preview is not required for normal inspection
            Provider calls disabled
            Model execution not connected yet
            data-kora-shell-local-only-boundary="v1.0"
            data-kora-shell-boundary-coverage="provider,cloud,download,model-execution,report-export"
            Cloud sync disabled
            Downloads disabled
            Report export disabled
            Shell-first boundary: approved local harness requests only
            no report file export or writing
            KORA Studio right details drawer scaffold
            data-kora-mobile-drawer="right-overlay"
            Inspector · local preview
            data-kora-drawer-section="runtime-status"
            data-kora-drawer-section="selected-model"
            data-kora-drawer-section="catalog-vs-installed"
            data-kora-drawer-section="route-trace"
            data-kora-drawer-section="generated-counters"
            data-kora-drawer-section="selected-run-surfaces"
            data-kora-drawer-selected-run-coverage="timeline,counters,comparison,report-metadata"
            data-kora-v1-1-drawer-selected-run-polish="primary-diagnostics"
            kora-drawer-selected-run-id
            kora-drawer-selected-timeline-status
            kora-drawer-selected-counters-status
            kora-drawer-selected-comparison-status
            kora-drawer-selected-report-status
            Drawer selected-run diagnostics mirror shell state for normal inspection
            data-kora-drawer-section="report-metadata"
            data-kora-drawer-section="claim-boundaries"
            data-kora-drawer-boundary-coverage="provider,cloud,download,model-execution,report-export,private-scan,runtime-list"
            Selection does not install or run a model
            Route trace
            Generated harness events only.
            Not production telemetry
            Not production cost evidence
            Report metadata
            File export:
            File written:
            Claim boundaries
            No private model directory scanning
            No runtime model list commands
            legacy-preview
            data-kora-legacy-preview-mode="compatibility-collapsed"
            data-kora-legacy-preview-default="collapsed"
            data-kora-legacy-preview-role="developer-compatibility-scaffold"
            data-kora-v1-1-legacy-secondary="developer-reference-only"
            data-kora-v1-1-legacy-first-run-required="false"
            data-kora-v1-1-legacy-boundary="secondary-reference-only"
            Legacy detailed preview compatibility scaffold
            Collapsed by default
            The final shell and Details drawer above are the primary local preview
            not required for first-run understanding
            Developer reference only
            This compatibility scaffold remains local-only and secondary
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
            data-kora-keyboard-selectable-request="true"
            Select approved local harness request local-harness-json-required-fields-001
            aria-pressed="false"
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
            kora-active-history-run-id
            History cards show compact counters from generated harness output only
            Compact counters: avoided_model_calls=
            Active selected local run
            Selected in page
            Cleared browser-local preview state only
            No backend records, files, report exports, or server endpoints were deleted
            getShellAccessibilityState
            setShellSelectedRunSurfaceState
            window.koraStudioAccessibilityState
            window.koraStudioScriptStatus
            status: "ready"
            keyboard_focus_pass
            left_rail_expanded
            details_drawer_expanded
            Generated Event Stream
            kora-sse-status
            kora-sse-fallback-used
            kora-sse-error
            Fallback to local events endpoint available
            No provider streaming
            new EventSource(`/api/harness/sse?run_id=${encodeURIComponent(selectedRunId)}`)
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
            kora-details-drawer-toggle
            aria-controls="kora-details-drawer"
            aria-expanded="false"
            kora-details-drawer-close
            data-kora-drawer-close
            data-kora-drawer-state
            setDetailsDrawerOpen
            event.key === "Escape"
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
        "/ v1.0 shell-first ok",
        "/ v1.1 shell-only ok",
        "/ v1.2 component markers ok",
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
