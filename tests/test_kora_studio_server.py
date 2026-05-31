from __future__ import annotations

import json
import os
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest
from http.server import ThreadingHTTPServer

from kora.studio_server import (
    DEFAULT_STUDIO_HOST,
    DEFAULT_STUDIO_PORT,
    create_studio_request_handler,
    get_studio_url,
    get_studio_health_payload,
    get_studio_server_status,
    get_studio_status_payload,
    is_allowed_studio_host,
    open_studio_browser,
    render_studio_placeholder_html,
    render_studio_server_status_text,
    run_studio_server,
)
from kora.studio_harness_runs import clear_local_harness_run_records

APPROVED_BOOST_MESSAGE = "Less waiting. Better answers. No hardware upgrade."
TECHNICAL_EXPLANATION = (
    "KORA Boost handles simple work through fast paths and saves model power "
    "for the tasks that need it."
)


def test_import_does_not_start_server_or_require_api_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert os.environ.get("OPENAI_API_KEY") is None
    assert os.environ.get("ANTHROPIC_API_KEY") is None
    assert DEFAULT_STUDIO_HOST == "127.0.0.1"
    assert DEFAULT_STUDIO_PORT == 8765


def test_allowed_studio_hosts_are_local_only() -> None:
    assert is_allowed_studio_host("127.0.0.1") is True
    assert is_allowed_studio_host("localhost") is True
    assert is_allowed_studio_host("0.0.0.0") is False
    assert is_allowed_studio_host("::1") is False


def test_get_studio_server_status_fields() -> None:
    status = get_studio_server_status()

    assert status["ok"] is True
    assert status["service"] == "kora-studio"
    assert status["status"] == "preview"
    assert status["studio_status"]["service"] == "kora-studio"
    assert status["studio_status"]["status"] == "preview"
    assert status["studio_status"]["implementation"] == "local_server_skeleton"
    assert status["studio_status"]["positioning"] == "local-first AI Task Execution Router workspace"
    assert status["studio_status"]["v0_2_status"]["milestone"] == "v0.2"
    assert status["studio_status"]["v0_2_status"]["readiness"] == "local_preview_demo_ready"
    assert "local preview/demo readiness milestone" in status["studio_status"]["v0_2_status"]["claim_boundary"]
    assert status["v0_2_status"] == status["studio_status"]["v0_2_status"]
    assert status["v0_1_readiness_status"] == "local_fixture_demo_ready"
    assert "Report Viewer Placeholder" in status["v0_1_demo_surfaces"]
    assert "local fixture-backed AI Task Execution Router demo scaffold" in status["v0_1_claim_boundary"]
    assert status["server"] == "local-only"
    assert status["host"] == "127.0.0.1"
    assert status["port"] == 8765
    assert status["launch_boundary"] == {
        "host": "127.0.0.1",
        "port": 8765,
        "url": "http://127.0.0.1:8765/",
        "server": "local-only",
        "allowed_hosts": ["127.0.0.1", "localhost"],
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "browser_launch_available": True,
        "api_key_required": False,
        "claim_boundary": (
            "The Studio preview is localhost-only by default. Provider calls and cloud sync are disabled, "
            "and no API key is required for the default local preview."
        ),
    }
    assert status["provider_calls_enabled"] is False
    assert status["cloud_sync_enabled"] is False
    assert status["system_profile"]["default_host"] == "127.0.0.1"
    assert status["system_profile"]["default_port"] == 8765
    assert status["system_profile"]["provider_calls_enabled"] is False
    assert status["system_profile"]["cloud_sync_enabled"] is False
    assert status["model_capability_estimate"]["recommended_local_chat_tier"]
    assert "estimates until validated" in status["model_capability_estimate"]["claim_boundary"]
    assert status["model_catalog_status"] == "static_local_scaffold"
    assert status["recommended_models"]
    first_model = status["recommended_models"][0]
    assert first_model["download_action_enabled"] is False
    assert first_model["run_action_enabled"] is False
    assert first_model["download_action_label"] == "Download not connected yet"
    assert first_model["run_action_label"] == "Run not connected yet"
    assert first_model["disabled_actions_route_to_guidance"] is True
    assert first_model["setup_guidance_path"] == "docs/kora-studio/kora-studio-runtime-setup-guidance.md"
    assert "estimates until validated" in status["model_catalog_claim_boundary"]
    assert "Download and execution are not connected yet" in status["model_catalog_claim_boundary"]
    assert status["runtime_status"]
    first_runtime = status["runtime_status"][0]
    assert first_runtime["service_reachable"] is False
    assert first_runtime["service_check_status"] == "not_checked"
    assert first_runtime["service_url"] == "http://127.0.0.1:11434/"
    assert first_runtime["service_probe_timeout_ms"] <= 500
    assert "localhost-only check" in first_runtime["service_probe_claim_boundary"]
    assert first_runtime["installed_model_detection_enabled"] is False
    assert first_runtime["installed_model_detection_status"] == "not_connected"
    assert first_runtime["installed_models_count"] == 0
    assert status["installed_models_summary"]["detection_status"] == "not_connected"
    assert status["installed_models_summary"]["installed_model_detection_status"] == "not_connected"
    assert status["installed_models_summary"]["installed_model_detection_enabled"] is False
    assert status["installed_models_summary"]["installed_models_count"] == 0
    assert "Catalog examples are not the same as installed models" in status["catalog_runtime_distinction"]
    assert status["setup_guidance_status"] == "informational_scaffold"
    assert status["setup_guidance_url"] == "docs/kora-studio/kora-studio-runtime-setup-guidance.md"
    assert status["disabled_actions_route_to_guidance"] is True
    assert status["disabled_action_state"] == {
        "download_connected": False,
        "run_connected": False,
        "model_execution_connected": False,
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "disabled_actions_route_to_guidance": True,
        "setup_guidance_url": "docs/kora-studio/kora-studio-runtime-setup-guidance.md",
        "claim_boundary": (
            "Download and run actions remain disabled until explicitly connected. Disabled actions point to "
            "informational setup guidance, not to an active installer or model runner."
        ),
    }
    assert "not to an active installer" in status["setup_guidance_claim_boundary"]
    assert status["local_harness_status"]["status"] == "local_deterministic_harness_available"
    assert status["local_harness_status"]["event_source_status"] == "generated_events_available"
    assert status["local_harness_status"]["run_trigger_status"] == "api_endpoint_connected"
    assert status["local_harness_status"]["run_trigger_endpoint"] == "/api/harness/run"
    assert status["local_harness_status"]["run_retrieval_endpoint"] == "/api/harness/run/{run_id}"
    assert status["local_harness_status"]["events_endpoint"] == "/api/harness/events?run_id=<id>"
    assert status["local_harness_status"]["events_endpoint_status"] == "generated_events_retrieval_connected"
    assert status["local_harness_status"]["sse_endpoint"] == "/api/harness/sse?run_id=<id>"
    assert status["local_harness_status"]["sse_endpoint_status"] == "generated_events_stream_connected"
    assert status["local_harness_status"]["approved_request_ids_only"] is True
    assert status["local_harness_status"]["arbitrary_prompt_execution_connected"] is False
    assert status["local_harness_status"]["sample_request_count"] == 5
    assert status["local_harness_status"]["provider_calls_enabled"] is False
    assert status["local_harness_status"]["cloud_sync_enabled"] is False
    assert status["local_harness_status"]["model_execution_connected"] is False
    assert status["local_harness_status"]["download_connected"] is False
    assert status["local_harness_run_store"]["run_store_status"] == "in_memory_local_only"
    assert status["local_harness_run_store"]["persistence_enabled"] is False
    assert status["local_harness_run_store"]["provider_calls_enabled"] is False
    assert status["local_harness_run_store"]["model_execution_connected"] is False
    assert "approved synthetic deterministic request IDs" in status["local_harness_run_claim_boundary"]
    assert status["local_harness_request_summary"]["local_harness_request_count"] == 5
    assert status["local_harness_requests"][0]["request_id"] == "local-harness-json-required-fields-001"
    assert status["local_harness_sample_run"]["request_id"] == "local-harness-json-required-fields-001"
    assert status["local_harness_sample_run"]["events"][0]["stage_id"] == "request_received"
    assert status["local_harness_sample_run"]["events"][-1]["stage_id"] == "final_counters"
    assert status["local_harness_counters"]["baseline_model_calls"] == 1
    assert status["local_harness_counters"]["kora_model_calls"] == 0
    assert status["local_harness_counters"]["avoided_model_calls"] == 1
    assert "synthetic deterministic requests" in status["local_harness_claim_boundary"]
    assert status["local_harness_comparison_status"] == "local_deterministic_harness_generated"
    assert status["local_harness_comparison"]["comparison_source"] == "local_harness_summary"
    assert status["comparison_counters"]["baseline_model_calls"] == 1
    assert status["comparison_counters"]["kora_model_calls"] == 0
    assert status["comparison_counters"]["avoided_model_calls"] == 1
    assert "local deterministic harness data" in status["comparison_claim_boundary"]
    assert status["execution_viewer_status"] == "fixture_mock_scaffold"
    assert status["execution_viewer_fixture_event_count"] == 6
    assert status["execution_viewer_fixture_events"][0]["stage_id"] == "request_received"
    assert status["execution_viewer_fixture_events"][-1]["stage_id"] == "final_counters"
    assert status["execution_viewer_fixture_events"][-1]["counters_snapshot"]["avoided_model_calls"] == 1
    assert "local fixture/mock data" in status["execution_viewer_claim_boundary"]
    assert status["model_execution_connected"] is False
    assert status["download_connected"] is False
    assert status["standard_vs_kora_comparison_status"] == "fixture_mock_scaffold"
    assert status["standard_vs_kora_metrics"]["baseline_model_calls"] == 1
    assert status["standard_vs_kora_metrics"]["kora_model_calls"] == 0
    assert status["standard_vs_kora_metrics"]["avoided_model_calls"] == 1
    assert status["standard_vs_kora_metrics"]["deterministic_routes"] == 1
    assert status["standard_vs_kora_metrics"]["model_escalations"] == 0
    assert status["standard_vs_kora_metrics"]["validation_pass_count"] == 1
    assert len(status["standard_vs_kora_metric_cards"]) == 6
    assert "fixture/mock comparison" in status["standard_vs_kora_claim_boundary"]
    assert status["report_viewer_status"] == "local_harness_summary_placeholder"
    assert status["report_viewer_placeholder"]["report_source"] == "local_harness_summary"
    assert status["report_viewer_placeholder"]["report_fixture_path"] == (
        "docs/kora-studio/fixtures/report-viewer-metadata.sample.json"
    )
    assert status["report_viewer_placeholder"]["arbitrary_local_file_scan_enabled"] is False
    assert status["report_viewer_placeholder"]["upload_enabled"] is False
    assert status["report_viewer_placeholder"]["generated_report_commit_enabled"] is False
    assert status["report_viewer_placeholder"]["file_export_enabled"] is False
    assert status["report_viewer_placeholder"]["file_written"] is False
    assert status["report_viewer_placeholder"]["model_execution_connected"] is False
    assert status["report_viewer_placeholder"]["production_evidence_claim"] is False
    assert status["report_viewer_placeholder"]["cost_claim_enabled"] is False
    assert status["report_viewer_placeholder"]["energy_claim_enabled"] is False
    assert status["report_viewer_placeholder"]["counters"] == status["local_harness_counters"]
    assert status["report_viewer_placeholder"]["counters"]["avoided_model_calls"] == 1
    assert status["report_export_status"] == "placeholder_not_connected"
    assert status["report_export_placeholder"]["export_action_enabled"] is False
    assert "local summary metadata only" in status["report_viewer_claim_boundary"]
    assert set(status["claim_boundaries"]) == {
        "studio",
        "launch",
        "model_capability",
        "model_catalog",
        "runtime_setup_guidance",
        "disabled_actions",
        "execution_viewer",
        "standard_vs_kora",
        "report_viewer",
        "local_harness",
        "local_harness_run",
        "local_harness_comparison",
    }
    assert "not a production release" in status["claim_boundaries"]["studio"]
    assert "localhost-only" in status["claim_boundaries"]["launch"]
    assert "estimates until validated" in status["claim_boundaries"]["model_capability"]
    assert "Download and execution are not connected yet" in status["claim_boundaries"]["model_catalog"]
    assert "No model is downloaded" in status["claim_boundaries"]["runtime_setup_guidance"]
    assert "remain disabled" in status["claim_boundaries"]["disabled_actions"]
    assert "local fixture/mock data" in status["claim_boundaries"]["execution_viewer"]
    assert "fixture/mock comparison" in status["claim_boundaries"]["standard_vs_kora"]
    assert "local summary metadata only" in status["claim_boundaries"]["report_viewer"]
    assert "synthetic deterministic requests" in status["claim_boundaries"]["local_harness"]
    assert "approved synthetic deterministic request IDs" in status["claim_boundaries"]["local_harness_run"]
    assert "local deterministic harness data" in status["claim_boundaries"]["local_harness_comparison"]
    assert status["first_run_section_order"] == [
        "Launch/local-only status",
        "Your Computer",
        "Model Capability Estimate",
        "Runtime Status",
        "Catalog vs Installed",
        "Setup Guidance",
        "Disabled Download/Run Actions",
        "KORA Boost Boundary",
        "Local Harness Preview",
        "Execution Viewer",
        "Standard Mode vs KORA Boost",
        "Report Viewer Placeholder",
    ]
    assert status["browser_launch_available"] is True
    assert status["ollama_calls_enabled"] is False
    assert status["local_runtime_required"] is False
    assert status["no_server_side_provider_calls"] is True
    assert status["docs_path"] == "docs/kora-studio/README.md"
    assert status["fixtures_path"] == "docs/kora-studio/fixtures/"
    assert status["kora_boost_message"] == APPROVED_BOOST_MESSAGE
    assert status["kora_boost_technical_explanation"] == TECHNICAL_EXPLANATION


def test_health_and_status_payloads_are_claim_safe() -> None:
    health = get_studio_health_payload()
    status = get_studio_status_payload()

    assert health == {
        "ok": True,
        "service": "kora-studio",
        "status": "preview",
        "server": "local-only",
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "browser_launch_available": True,
    }
    assert status["provider_calls_enabled"] is False
    assert status["cloud_sync_enabled"] is False
    assert "system_profile" in status
    assert "model_capability_estimate" in status
    assert "recommended_models" in status
    assert status["model_catalog_status"] == "static_local_scaffold"
    assert "runtime_status" in status
    assert "installed_models_summary" in status
    assert status["installed_models_summary"]["installed_model_detection_enabled"] is False
    assert status["setup_guidance_status"] == "informational_scaffold"
    assert status["disabled_actions_route_to_guidance"] is True
    assert status["execution_viewer_status"] == "fixture_mock_scaffold"
    assert status["execution_viewer_fixture_event_count"] == 6
    assert status["local_harness_status"]["status"] == "local_deterministic_harness_available"
    assert status["local_harness_status"]["run_trigger_status"] == "api_endpoint_connected"
    assert status["local_harness_requests"]
    assert status["local_harness_sample_run"]["status"] == "completed"
    assert status["local_harness_counters"]["avoided_model_calls"] == 1
    assert status["local_harness_status"]["model_execution_connected"] is False
    assert status["local_harness_comparison_status"] == "local_deterministic_harness_generated"
    assert status["comparison_counters"]["avoided_model_calls"] == 1
    assert status["local_harness_comparison"]["model_execution_connected"] is False
    assert status["model_execution_connected"] is False
    assert status["standard_vs_kora_comparison_status"] == "fixture_mock_scaffold"
    assert status["standard_vs_kora_metrics"]["avoided_model_calls"] == 1
    assert status["report_viewer_status"] == "local_harness_summary_placeholder"
    assert status["report_viewer_placeholder"]["report_source"] == "local_harness_summary"
    assert status["report_export_status"] == "placeholder_not_connected"
    assert status["no_server_side_provider_calls"] is True
    assert status["kora_boost_message"] == APPROVED_BOOST_MESSAGE


def test_status_payload_exposes_v0_2_contract_fields() -> None:
    status = get_studio_status_payload()

    required_top_level_fields = {
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
        "execution_viewer_fixture_events",
        "local_harness_status",
        "local_harness_run_store",
        "local_harness_requests",
        "local_harness_sample_run",
        "local_harness_counters",
        "local_harness_claim_boundary",
        "local_harness_run_claim_boundary",
        "local_harness_comparison_status",
        "local_harness_comparison",
        "comparison_counters",
        "comparison_claim_boundary",
        "standard_vs_kora_comparison_status",
        "standard_vs_kora_comparison",
        "standard_vs_kora_metrics",
        "report_viewer_status",
        "report_viewer_placeholder",
        "provider_calls_enabled",
        "cloud_sync_enabled",
        "claim_boundaries",
        "first_run_section_order",
    }
    assert required_top_level_fields <= set(status)

    assert status["studio_status"]["v0_2_status"]["first_run_section_order"] == status["first_run_section_order"]
    assert status["launch_boundary"]["provider_calls_enabled"] is False
    assert status["launch_boundary"]["cloud_sync_enabled"] is False
    assert status["disabled_action_state"]["download_connected"] is False
    assert status["disabled_action_state"]["run_connected"] is False
    assert status["disabled_action_state"]["model_execution_connected"] is False
    assert status["execution_viewer_status"] == "fixture_mock_scaffold"
    assert status["standard_vs_kora_comparison_status"] == "fixture_mock_scaffold"
    assert status["report_viewer_status"] == "local_harness_summary_placeholder"
    assert status["provider_calls_enabled"] is False
    assert status["cloud_sync_enabled"] is False


def test_render_studio_server_status_text_includes_boundaries() -> None:
    text = render_studio_server_status_text(get_studio_server_status())

    assert "Launching KORA Studio" in text
    assert "Local URL:" in text
    assert "http://127.0.0.1:8765/" in text
    assert "Local-only" in text
    assert "Provider calls: disabled" in text
    assert "Cloud sync: disabled" in text
    assert "Press Ctrl+C to stop" in text


def test_render_studio_server_status_text_includes_no_browser_state() -> None:
    text = render_studio_server_status_text(get_studio_server_status(), open_browser=False)

    assert "Local URL:" in text
    assert "http://127.0.0.1:8765/" in text
    assert "Browser launch: disabled by --no-browser." in text


def test_render_studio_server_status_text_includes_browser_failure_fallback() -> None:
    text = render_studio_server_status_text(
        get_studio_server_status(),
        open_browser=True,
        browser_opened=False,
    )

    assert "Browser launch failed. Open this URL manually:" in text
    assert "http://127.0.0.1:8765/" in text


def test_open_studio_browser_is_mockable_and_failure_safe() -> None:
    opened_urls: list[str] = []

    assert open_studio_browser("http://127.0.0.1:8765/", lambda url: (opened_urls.append(url), False)[1]) is False
    assert opened_urls == ["http://127.0.0.1:8765/"]

    def raise_error(url: str) -> bool:
        raise RuntimeError(f"cannot open {url}")

    assert open_studio_browser("http://127.0.0.1:8765/", raise_error) is False
    assert open_studio_browser("http://127.0.0.1:8765/", lambda url: True) is True


def test_run_studio_server_opens_browser_by_default(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    opened_urls: list[str] = []
    created_servers: list[object] = []

    class FakeServer:
        def __init__(self, address: tuple[str, int], handler: object) -> None:
            self.address = address
            self.handler = handler
            created_servers.append(self)

        def serve_forever(self) -> None:
            raise KeyboardInterrupt

        def server_close(self) -> None:
            return None

    monkeypatch.setattr("kora.studio_server.ThreadingHTTPServer", FakeServer)

    run_studio_server(browser_opener=lambda url: opened_urls.append(url) is None or True)

    assert opened_urls == [get_studio_url()]
    assert created_servers
    assert getattr(created_servers[0], "address") == ("127.0.0.1", 8765)
    output = capsys.readouterr().out
    assert "Launching KORA Studio" in output
    assert "Provider calls: disabled" in output
    assert "Cloud sync: disabled" in output


def test_run_studio_server_no_browser_suppresses_browser_open(monkeypatch: pytest.MonkeyPatch) -> None:
    opened_urls: list[str] = []

    class FakeServer:
        def __init__(self, address: tuple[str, int], handler: object) -> None:
            self.address = address
            self.handler = handler

        def serve_forever(self) -> None:
            raise KeyboardInterrupt

        def server_close(self) -> None:
            return None

    monkeypatch.setattr("kora.studio_server.ThreadingHTTPServer", FakeServer)

    run_studio_server(open_browser=False, browser_opener=lambda url: opened_urls.append(url) is None or True)

    assert opened_urls == []


def test_request_handler_serves_health_status_and_placeholder() -> None:
    handler = create_studio_request_handler(lambda: get_studio_server_status(port=0))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    except PermissionError:
        pytest.skip("localhost binding is not available in this sandbox")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        with urllib.request.urlopen(f"{base_url}/health", timeout=2) as response:
            health = json.loads(response.read().decode("utf-8"))
        with urllib.request.urlopen(f"{base_url}/status", timeout=2) as response:
            status = json.loads(response.read().decode("utf-8"))
        with urllib.request.urlopen(f"{base_url}/", timeout=2) as response:
            html = response.read().decode("utf-8")
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()

    assert health["ok"] is True
    assert health["service"] == "kora-studio"
    assert status["server"] == "local-only"
    assert status["provider_calls_enabled"] is False
    assert status["cloud_sync_enabled"] is False
    assert "system_profile" in status
    assert "model_capability_estimate" in status
    assert "recommended_models" in status
    assert status["model_catalog_claim_boundary"]
    assert "runtime_status" in status
    assert status["installed_models_summary"]["installed_models_detected"] is False
    assert status["ollama_calls_enabled"] is False
    content_type = response.headers.get("Content-Type", "")

    assert "text/html" in content_type
    assert "KORA Studio" in html
    assert APPROVED_BOOST_MESSAGE in html
    assert "Preview / Local-only" in html
    assert "Local Preview Scaffold" in html
    assert "deterministic-first local workflow exploration" in html
    assert "/health" in html
    assert "/status" in html
    assert "/api/harness/run" in html
    assert "/api/harness/events" in html
    assert "/api/harness/sse" in html
    assert "not model token streaming" in html
    assert "Provider calls: disabled" in html
    assert "Cloud sync: disabled" in html
    assert "Your Computer" in html
    assert "Model Capability Estimate" in html
    assert "Catalog vs Installed" in html
    assert "Physically runnable local candidates" in html
    assert "Larger-model workflow candidates" in html
    assert "Model recommendations are estimates until validated on this machine" in html
    assert "Download and execution are not connected yet" in html
    assert "Download" in html
    assert "Run" in html
    assert "Disabled Download/Run Actions" in html
    assert "Download action" in html
    assert "Run action" in html
    assert "Download not connected yet" in html
    assert "Run not connected yet" in html
    assert "Setup Guidance" in html
    assert "Disabled actions point to guidance, not to an active installer" in html
    assert "No model is downloaded" in html
    assert "No model is executed" in html
    assert "Provider/cloud routes are disabled by default" in html
    assert "docs/kora-studio/kora-studio-runtime-setup-guidance.md" in html
    assert "Runtime Status" in html
    assert "Installed locally" in html
    assert "Service reachability is a localhost-only check" in html
    assert "No model execution occurs during this check" in html
    assert "Installed model detection is not connected yet" in html
    assert "No private model directories are scanned" in html
    assert "No runtime model list command is called by default" in html
    assert "Download and run actions remain disabled" in html
    assert "Catalog vs Installed" in html
    assert "Catalog examples are not installed models" in html
    assert "Estimated local model tier" in html
    assert "KORA Boost Boundary" in html
    assert "KORA does not remove RAM/VRAM/unified-memory requirements" in html
    assert "Local Harness Preview" in html
    assert "local_deterministic_harness_available" in html
    assert "generated_events_available" in html
    assert "api_endpoint_connected" in html
    assert "Run Local Harness" in html
    assert "Run Local Harness action state" in html
    assert "Approved deterministic sample requests only" in html
    assert "No arbitrary prompt execution" in html
    assert "Generated harness events only" in html
    assert "This is local preview/demo data, not production evidence" in html
    assert "execution_not_connected" in html
    assert "Available local deterministic sample requests" in html
    assert "local-harness-json-required-fields-001" in html
    assert "Expected route: deterministic_code" in html
    assert "Harness event stages" in html
    assert "Generated Event Timeline" in html
    assert "Generated local harness events only" in html
    assert "Not model token streaming" in html
    assert "No provider output" in html
    assert "Route class: input" in html
    assert "Status: completed" in html
    assert "Model called: False" in html
    assert "Deterministic route used:" in html
    assert "Validation result:" in html
    assert "Latency:" in html
    assert "Model-needed boundaries do not execute models in this milestone" in html
    assert "Local deterministic harness output" in html
    assert "Generated Counters" in html
    assert "Model/runtime integration: not connected" in html
    assert "Browser launch: available" in html
    assert "Ollama integration: not connected" in html
    assert "No production/API-cost/energy claims" in html
    assert "Report Viewer Placeholder" in html
    assert "Local Harness Summary Report" in html
    assert "docs/kora-studio/fixtures/report-viewer-metadata.sample.json" in html
    assert "No arbitrary local file scan is performed" in html
    assert "No cloud upload is connected" in html
    assert "Export not connected yet" in html
    assert "Local harness summary only" in html
    assert "No new benchmark evidence is created" in html
    assert "provider calls enabled" not in html.lower()
    assert "production cost reduction" not in html.lower()
    assert "real api-cost reduction" not in html.lower()
    assert "energy reduction" not in html.lower()


def test_request_handler_triggers_and_retrieves_local_harness_run() -> None:
    clear_local_harness_run_records()
    handler = create_studio_request_handler(lambda: get_studio_server_status(port=0))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    except PermissionError:
        pytest.skip("localhost binding is not available in this sandbox")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        request_body = json.dumps({"request_id": "local-harness-known-faq-001"}).encode("utf-8")
        request = urllib.request.Request(
            f"{base_url}/api/harness/run",
            data=request_body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=2) as response:
            run = json.loads(response.read().decode("utf-8"))

        with urllib.request.urlopen(f"{base_url}/api/harness/run/{run['run_id']}", timeout=2) as response:
            retrieved_run = json.loads(response.read().decode("utf-8"))
        with urllib.request.urlopen(f"{base_url}/api/harness/events?run_id={run['run_id']}", timeout=2) as response:
            events_payload = json.loads(response.read().decode("utf-8"))
        with urllib.request.urlopen(f"{base_url}/api/harness/sse?run_id={run['run_id']}", timeout=2) as response:
            sse_content_type = response.headers.get("Content-Type", "")
            sse_stream = response.read().decode("utf-8")
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()

    assert run["ok"] is True
    assert run["request_id"] == "local-harness-known-faq-001"
    assert run["run_status"] == "completed"
    assert run["created_at"].endswith("Z")
    assert run["completed_at"].endswith("Z")
    assert run["generated_events"][0]["stage_id"] == "request_received"
    assert run["generated_events"][-1]["stage_id"] == "final_counters"
    assert run["generated_counters"]["structured_lookup_routes"] == 1
    assert run["generated_counters"]["kora_model_calls"] == 0
    assert run["comparison_summary"]["metrics"]["avoided_model_calls"] == 1
    assert run["report_metadata_summary"]["report_source"] == "local_harness_summary"
    assert run["report_metadata_summary"]["report_source_detail"] == "local deterministic harness output / fixture metadata"
    assert run["report_metadata_summary"]["run_id"] == run["run_id"]
    assert run["report_metadata_summary"]["request_id"] == run["request_id"]
    assert run["report_metadata_summary"]["event_count"] == len(run["generated_events"])
    assert run["report_metadata_summary"]["counter_summary"]["structured_lookup_routes"] == 1
    assert run["report_metadata_summary"]["comparison_summary_status"] == "local_deterministic_harness_generated"
    assert run["report_metadata_summary"]["model_execution_status"] == "not_needed"
    assert run["report_metadata_summary"]["provider_calls_enabled"] is False
    assert run["report_metadata_summary"]["cloud_sync_enabled"] is False
    assert run["report_metadata_summary"]["file_export_enabled"] is False
    assert run["report_metadata_summary"]["file_written"] is False
    assert run["report_metadata_summary"]["export_action_enabled"] is False
    assert run["report_metadata_summary"]["production_evidence_claim"] is False
    assert "local summary metadata only" in run["report_metadata_summary"]["claim_boundary"]
    assert run["provider_calls_enabled"] is False
    assert run["cloud_sync_enabled"] is False
    assert run["model_execution_connected"] is False
    assert run["download_connected"] is False
    assert retrieved_run == run
    assert events_payload["run_id"] == run["run_id"]
    assert events_payload["request_id"] == run["request_id"]
    assert events_payload["run_status"] == "completed"
    assert events_payload["event_count"] == len(events_payload["events"])
    assert events_payload["events"] == run["generated_events"]
    assert events_payload["sse_connected"] is False
    assert events_payload["streaming_connected"] is False
    assert events_payload["model_execution_connected"] is False
    assert "text/event-stream" in sse_content_type
    assert "event: stream_started" in sse_stream
    assert "event: harness_stage" in sse_stream
    assert "event: stream_completed" in sse_stream
    assert run["run_id"] in sse_stream
    assert "request_received" in sse_stream
    assert "final_counters" in sse_stream
    assert "approved synthetic deterministic request IDs" in sse_stream
    assert "model_token_streaming_connected" in sse_stream
    assert sse_stream.index("event: stream_started") < sse_stream.index("event: harness_stage")
    assert sse_stream.index("stage_id\":\"request_received") < sse_stream.index("stage_id\":\"final_counters")


def test_request_handler_rejects_invalid_local_harness_run_request() -> None:
    clear_local_harness_run_records()
    handler = create_studio_request_handler(lambda: get_studio_server_status(port=0))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    except PermissionError:
        pytest.skip("localhost binding is not available in this sandbox")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        request_body = json.dumps({"request_id": "missing-request"}).encode("utf-8")
        request = urllib.request.Request(
            f"{base_url}/api/harness/run",
            data=request_body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with pytest.raises(urllib.error.HTTPError) as exc_info:
            urllib.request.urlopen(request, timeout=2)
        error_body = json.loads(exc_info.value.read().decode("utf-8"))

        with pytest.raises(urllib.error.HTTPError) as missing_run_exc:
            urllib.request.urlopen(f"{base_url}/api/harness/run/missing-run", timeout=2)
        missing_run_body = json.loads(missing_run_exc.value.read().decode("utf-8"))
        with pytest.raises(urllib.error.HTTPError) as missing_events_exc:
            urllib.request.urlopen(f"{base_url}/api/harness/events?run_id=missing-run", timeout=2)
        missing_events_body = json.loads(missing_events_exc.value.read().decode("utf-8"))
        with pytest.raises(urllib.error.HTTPError) as missing_sse_exc:
            urllib.request.urlopen(f"{base_url}/api/harness/sse?run_id=missing-run", timeout=2)
        missing_sse_body = json.loads(missing_sse_exc.value.read().decode("utf-8"))
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()

    assert exc_info.value.code == 404
    assert error_body["ok"] is False
    assert error_body["error"] == "unknown_request_id"
    assert error_body["request_id"] == "missing-request"
    assert error_body["run_status"] == "failed"
    assert error_body["provider_calls_enabled"] is False
    assert error_body["model_execution_connected"] is False

    assert missing_run_exc.value.code == 404
    assert missing_run_body["error"] == "run_not_found"
    assert missing_events_exc.value.code == 404
    assert missing_events_body["error"] == "run_not_found"
    assert missing_events_body["model_execution_connected"] is False
    assert missing_sse_exc.value.code == 404
    assert missing_sse_body["error"] == "run_not_found"
    assert missing_sse_body["model_execution_connected"] is False


def test_static_preview_html_content_is_safe_and_complete() -> None:
    html = render_studio_placeholder_html(get_studio_server_status())

    assert html.startswith("<!doctype html>")
    assert "KORA Studio" in html
    assert "data-kora-final-ui-shell=\"true\"" in html
    assert "KORA Studio left mini rail" in html
    assert "New task" in html
    assert "Search tasks" in html
    assert "Local workspace" in html
    assert "Cloud sync disabled" in html
    assert "Search or select open-source LLM" in html
    assert "KORA Studio top bar" in html
    assert "KORA Studio centered composer" in html
    assert "What do you want to work on?" in html
    assert "Choose a local model once. KORA keeps routing details out of the way." in html
    assert "Ask KORA..." in html
    assert "Provider calls disabled" in html
    assert "Model execution not connected yet" in html
    assert "KORA Studio right details drawer scaffold" in html
    assert "Inspector · local preview" in html
    assert "Route trace" in html
    assert "Report metadata" in html
    assert "Claim boundaries" in html
    assert "legacy-preview" in html
    assert "Local Preview Scaffold" in html
    assert "Preview / Local-only" in html
    assert APPROVED_BOOST_MESSAGE in html
    assert TECHNICAL_EXPLANATION in html
    assert "deterministic-first local workflow exploration" in html
    assert "Launch / Local-only Status" in html
    assert "First-run order" in html
    assert "Server: local" in html
    assert "Provider calls: disabled" in html
    assert "Cloud sync: disabled" in html
    assert "Your Computer" in html
    assert "Model Capability Estimate" in html
    assert "Catalog vs Installed" in html
    assert "Catalog examples" in html
    assert "static_local_scaffold" in html
    assert "Download and execution are not connected yet" in html
    assert "Disabled Download/Run Actions" in html
    assert "Download action" in html
    assert "Run action" in html
    assert "Download not connected yet" in html
    assert "Run not connected yet" in html
    assert "Setup Guidance" in html
    assert "Disabled actions point to guidance, not to an active installer" in html
    assert "No model is downloaded" in html
    assert "No model is executed" in html
    assert "Runtime Status" in html
    assert "Installed model detection" in html
    assert "Runtime executable detection is local-only" in html
    assert "Service reachability is a localhost-only check" in html
    assert "No model execution occurs during this check" in html
    assert "Installed model detection is not connected yet" in html
    assert "No private model directories are scanned" in html
    assert "No runtime model list command is called by default" in html
    assert "Download and run actions remain disabled" in html
    assert "Catalog examples are not installed models" in html
    assert "Estimated local model tier" in html
    assert "Unknown until validated" in html or "depending on runtime" in html
    assert "KORA does not remove RAM/VRAM/unified-memory requirements" in html
    assert "Local Harness Preview" in html
    assert "local_deterministic_harness_available" in html
    assert "generated_events_available" in html
    assert "Run trigger: api_endpoint_connected" in html
    assert "Approved Request Selector" in html
    assert "Interactive approved request selector" in html
    assert "Approved local harness requests only" in html
    assert "Approved request only" in html
    assert "Selected request preview" in html
    assert "Selector state is browser-local in-memory page state only" in html
    assert "id=\"kora-run-local-harness-button\"" in html
    assert "id=\"kora-selected-run-state\"" in html
    assert "Selected run state" in html
    assert "Selected Run Error State" in html
    assert "id=\"kora-run-error-state\"" in html
    assert "Retry Last Approved Request" in html
    assert "id=\"kora-retry-last-approved-request-button\"" in html
    assert "id=\"kora-last-approved-request-id\"" in html
    assert "Retry uses the last approved request only" in html
    assert "The local harness endpoint was unavailable" in html
    assert "The local response could not be parsed" in html
    assert "lastApprovedRequestId" in html
    assert "retryAvailable" in html
    assert "runError" in html
    assert "runLoading" in html
    assert "await runLocalHarness(lastApprovedRequestId)" in html
    assert "Local Run History" in html
    assert "Browser-local run history" in html
    assert "Page-memory only" in html
    assert "Clears on refresh" in html
    assert "Active selected run: <code id=\"kora-active-history-run-id\">none</code>" in html
    assert "History cards show compact counters from generated harness output only" in html
    assert "id=\"kora-local-run-history\"" in html
    assert "id=\"kora-run-history-count\"" in html
    assert "id=\"kora-run-history-status\"" in html
    assert "Clear Local Run History" in html
    assert "id=\"kora-clear-run-history-button\"" in html
    assert "Cleared browser-local preview state only" in html
    assert "Resets selected-run UI, selected events, selected counters, selected comparison, selected report metadata, and page-memory history" in html
    assert "No persistence, no cloud sync, no file export, no file writing, and no backend delete call" in html
    assert "let runHistory = []" in html
    assert "const runHistoryLimit = 5" in html
    assert "renderRunHistory" in html
    assert "selectRunFromHistory" in html
    assert "addRunToHistory" in html
    assert "clearLocalRunHistory" in html
    assert "data-kora-history-run-id" in html
    assert "Active selected local run" in html
    assert "Recent local run" in html
    assert "Compact counters: avoided_model_calls=" in html
    assert "aria-current" in html
    assert "Selected in page" in html
    assert "No backend records, files, report exports, or server endpoints were deleted" in html
    assert "get run_history()" in html
    assert "get selected_run_record()" in html
    assert "Generated Event Stream" in html
    assert "id=\"kora-sse-status\"" in html
    assert "id=\"kora-sse-fallback-used\"" in html
    assert "id=\"kora-sse-error\"" in html
    assert "Generated harness events only" in html
    assert "Not model token streaming" in html
    assert "No provider streaming" in html
    assert "Fallback to local events endpoint available" in html
    assert "let sseAvailable = typeof EventSource !== \"undefined\"" in html
    assert "let activeEventSource = null" in html
    assert "closeActiveEventSource" in html
    assert "connectGeneratedEventStream" in html
    assert "new EventSource(`/api/harness/sse?run_id=${encodeURIComponent(selectedRunId)}`)" in html
    assert "fetchSelectedEventsFallback" in html
    assert "eventSource.addEventListener(\"harness_stage\"" in html
    assert "eventSource.addEventListener(\"stream_completed\"" in html
    assert "get sse_status()" in html
    assert "get sse_fallback_used()" in html
    assert "Generated local harness output only" in html
    assert "Selected Run Event Timeline" in html
    assert "id=\"kora-selected-run-events\"" in html
    assert "id=\"kora-selected-events-status\"" in html
    assert "No selected run events loaded yet" in html
    assert "Events are fetched from <code>GET /api/harness/events?run_id=&lt;id&gt;</code>" in html
    assert "Selected Run Counters" in html
    assert "id=\"kora-selected-run-counters\"" in html
    assert "id=\"kora-selected-counters-status\"" in html
    assert "Run an approved local harness request to view selected-run counters" in html
    assert "Selected Run: Standard Mode vs KORA Boost" in html
    assert "id=\"kora-selected-run-comparison\"" in html
    assert "id=\"kora-selected-comparison-status\"" in html
    assert "Run an approved local harness request to view selected-run comparison" in html
    assert "Selected Run Report Metadata" in html
    assert "id=\"kora-selected-run-report-metadata\"" in html
    assert "id=\"kora-selected-report-status\"" in html
    assert "Run an approved local harness request to view selected-run report metadata" in html
    assert "Report metadata preview only" in html
    assert "No file export" in html
    assert "No file writing" in html
    assert "Generated local harness counters only" in html
    assert "Not production telemetry" in html
    assert "Not production cost evidence" in html
    assert "selectedRunId" in html
    assert "selectedRunEvents" in html
    assert "selectedRunCounters" in html
    assert "selectedRunComparison" in html
    assert "selectedRunReportMetadata" in html
    assert "data-kora-request-id" in html
    assert "Local deterministic harness data only" in html
    assert "Run Local Harness" in html
    assert "Run Local Harness action state" in html
    assert "The browser button calls only the local harness run endpoint for an approved request id" in html
    assert "Approved deterministic sample requests only" in html
    assert "No arbitrary prompt execution" in html
    assert "Generated harness events only" in html
    assert "This is local preview/demo data, not production evidence" in html
    assert "Model-needed boundary returns <code>execution_not_connected</code>" in html
    assert "Available sample requests: 5" in html
    assert "Available local deterministic sample requests" in html
    assert "local-harness-json-required-fields-001" in html
    assert "Harness event stages" in html
    assert "Generated Event Timeline" in html
    assert "Generated local harness events only" in html
    assert "Not model token streaming" in html
    assert "No provider output" in html
    assert "Route class: input" in html
    assert "Status: completed" in html
    assert "Model called: False" in html
    assert "Deterministic route used:" in html
    assert "Validation result:" in html
    assert "Latency:" in html
    assert "Model-needed boundaries do not execute models in this milestone" in html
    assert "Local deterministic harness output" in html
    assert "Generated Counters" in html
    assert "Standard Mode vs KORA Boost" in html
    assert "Local deterministic harness comparison" in html
    assert "Local Harness Comparison boundary" in html
    assert "Comparison is generated from local deterministic harness output" in html
    assert "This is not production cost evidence" in html
    assert "This does not execute a model" in html
    assert "local_deterministic_harness_generated" in html
    assert "Baseline model calls" in html
    assert "KORA model calls" in html
    assert "Avoided model calls" in html
    assert "Deterministic routes" in html
    assert "Model escalations" in html
    assert "Validation passes" in html
    assert "No cost or energy claim is made" in html
    assert "Model/runtime integration: not connected" in html
    assert "Browser launch: available" in html
    assert "Ollama integration: not connected" in html
    assert "Endpoint Panel" in html
    assert "/health" in html
    assert "/status" in html
    assert "/api/harness/run" in html
    assert "/api/harness/events" in html
    assert "/api/harness/sse" in html
    assert "It streams no model tokens" in html
    assert "Execution Viewer" in html
    assert "Fixture/mock events only" in html
    assert "No real model execution" in html
    assert "No provider calls" in html
    assert "No model downloads" in html
    assert "Request received" in html
    assert "Deterministic route check" in html
    assert "Structured lookup" in html
    assert "Validation pass" in html
    assert "Model fallback skipped" in html
    assert "Final counters" in html
    assert "No runtime execution occurs on this page" in html
    assert "Report Viewer Placeholder" in html
    assert "Local Harness Report" in html
    assert "Report Metadata Preview" in html
    assert "Report metadata preview only" in html
    assert "Report Boundary" in html
    assert "Local deterministic harness output only" in html
    assert "Not production evidence" in html
    assert "No file export in this preview" in html
    assert "File export: disabled" in html
    assert "File written: false" in html
    assert "Report metadata" in html
    assert "Export placeholder" in html
    assert "Boundary warnings" in html
    assert "No arbitrary local file scan is performed" in html
    assert "No cloud upload is connected" in html
    assert "Export not connected yet" in html
    assert "No new benchmark evidence is created" in html
    assert "Limitations Panel" in html
    assert "No production/API-cost/energy claims" in html
    assert "No full frontend yet" in html
    assert "Browser launch is local-only" in html
    assert "No provider calls" in html
    assert "No model/runtime integration yet" in html
    assert "No Ollama integration" in html
    assert "docs/kora-studio/README.md" in html
    assert "docs/kora-studio/fixtures/" in html
    assert "Local-only skeleton" in html
    assert "OPENAI_API_KEY" not in html
    assert "ANTHROPIC_API_KEY" not in html
    assert "provider calls enabled" not in html.lower()
    assert "download now" not in html.lower()
    assert "run now" not in html.lower()
    assert "install now" not in html.lower()
    assert "production cost reduction" not in html.lower()
    assert "real api-cost reduction" not in html.lower()
    assert "energy reduction" not in html.lower()
    assert "production report" not in html.lower()
    assert "cost reduction proven" not in html.lower()
    assert "real provider report" not in html.lower()
    assert "model output report" not in html.lower()
    assert "download report" not in html.lower()
    assert "export now" not in html.lower()
    assert "<script" in html.lower()
    assert "type=\"application/json\" id=\"kora-approved-requests-data\"" in html
    assert "fetch(\"/api/harness/run\"" in html
    assert "fetch(`/api/harness/events?run_id=${encodeURIComponent(selectedRunId)}`)" in html
    assert html.index("renderRunResponse(payload);") < html.index("await connectGeneratedEventStream();")
    assert "renderSelectedCounters(run.generated_counters" in html
    assert "renderSelectedComparison(run.comparison_summary" in html
    assert "renderSelectedReportMetadata(run.report_metadata_summary)" in html
    assert "JSON.stringify({request_id: requestId})" in html
    assert "Retry any prompt" not in html
    assert "Type a prompt" not in html
    assert "src=" not in html.lower()
    assert 'href="http' not in html.lower()
    assert "https://" not in html.lower()
    assert "localstorage" not in html.lower()
    assert "sessionstorage" not in html.lower()
    assert "indexeddb" not in html.lower()
    assert "fetch(\"/api/delete" not in html
    assert "fetch(\"/api/harness/delete" not in html
    assert "fetch(\"/api/harness/events" not in html
    assert "fetch(\"/api/harness/sse" not in html
    assert "new EventSource(\"http" not in html
    assert "new EventSource(\"/api/model" not in html
    assert "new EventSource(\"/api/provider" not in html
    assert "new EventSource(\"/api/download" not in html
    assert "fetch(\"/api/model" not in html
    assert "fetch(\"/api/provider" not in html
    assert "fetch(\"/api/download" not in html
    assert "fetch(\"/api/report" not in html
    assert "fetch(\"/api/export" not in html
    assert "fetch(\"/api/file" not in html
    assert "xmlhttprequest" not in html.lower()
    assert "navigator.sendbeacon" not in html.lower()
    assert "<input" not in html.lower()
    assert "<textarea" not in html.lower()
    assert "Run any prompt" not in html
    assert "Run model" not in html
    assert "Download model" not in html
    assert "Production benchmark" not in html

    ordered_sections = [
        "Launch / Local-only Status",
        "Your Computer",
        "Model Capability Estimate",
        "Runtime Status",
        "Catalog vs Installed",
        "Setup Guidance",
        "Disabled Download/Run Actions",
        "KORA Boost Boundary",
        "Local Harness Preview",
        "Execution Viewer",
        "Standard Mode vs KORA Boost",
        "Report Viewer Placeholder",
    ]
    positions = [html.index(f"<h2>{section}</h2>") for section in ordered_sections]
    assert positions == sorted(positions)


def test_runtime_setup_guidance_doc_is_claim_safe() -> None:
    doc = Path("docs/kora-studio/kora-studio-runtime-setup-guidance.md").read_text()

    assert "Setup guidance is informational in this scaffold" in doc
    assert "Disabled actions point to guidance, not to an active installer" in doc
    assert "No model is downloaded" in doc
    assert "No model is executed" in doc
    assert "No private model directories are scanned" in doc
    assert "No runtime model list command is called" in doc
    assert "No provider call is made" in doc
    assert "Provider and cloud routes are disabled by default" in doc
