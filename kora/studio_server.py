"""Local-only KORA Studio server skeleton."""

from __future__ import annotations

import html
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable
from urllib.parse import parse_qs, unquote, urlparse

from kora.studio_drawer_render import render_right_details_drawer
from kora.studio_execution_fixture import get_execution_viewer_fixture_summary, get_standard_vs_kora_status_fields
from kora.studio_harness_comparison import get_local_harness_comparison_status_fields
from kora.studio_harness_display_render import (
    render_execution_viewer_section,
    render_local_harness_preview_section,
    render_report_viewer_placeholder_section,
    render_standard_vs_kora_section,
)
from kora.studio_harness_events import LOCAL_HARNESS_EVENT_CLAIM_BOUNDARY, build_local_harness_events
from kora.studio_harness_requests import get_local_harness_request_summary, get_local_harness_requests
from kora.studio_harness_request_render import (
    render_local_harness_request_selector_panels,
    render_local_harness_selector_item,
    render_local_harness_trigger_item,
    render_local_harness_trigger_reference_panels,
)
from kora.studio_harness_runs import (
    LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
    format_local_harness_sse,
    get_local_harness_run_record,
    get_local_harness_run_events,
    get_local_harness_run_store_status,
    trigger_local_harness_run,
)
from kora.studio_legacy_render import render_legacy_preview_opening
from kora.studio_model_catalog import MODEL_CATALOG_CLAIM_BOUNDARY, SETUP_GUIDANCE_PATH, recommend_catalog_models
from kora.studio_model_runtime_render import (
    render_catalog_installed_section,
    render_disabled_actions_section,
    render_model_capability_section,
    render_model_selector_option,
    render_runtime_status_section,
    render_setup_guidance_section,
    render_system_profile_section,
)
from kora.studio_reference_render import render_reference_panels
from kora.studio_report_viewer import get_report_viewer_status_fields
from kora.studio_runtime_status import get_runtime_status, summarize_installed_models
from kora.studio_script_render import render_studio_javascript
from kora.studio_style_render import render_studio_css
from kora.studio_run_state_render import render_run_state_history_panels
from kora.studio_selected_run_render import (
    render_selected_run_detail_panels,
    render_selected_run_state_panel,
    render_selected_run_summary_panel,
)
from kora.studio_shell_render import render_shell_layout
from kora.studio_status_boundary_render import (
    render_kora_boost_boundary_section,
    render_launch_local_status_section,
    render_shell_boundary_strip,
)
from kora.studio_status import get_studio_status
from kora.studio_system_profile import estimate_model_capability, get_system_profile

DEFAULT_STUDIO_HOST = "127.0.0.1"
DEFAULT_STUDIO_PORT = 8765
ALLOWED_STUDIO_HOSTS = {"127.0.0.1", "localhost"}
STUDIO_CSS_ASSET_PATH = "/studio-assets/studio.css"
STUDIO_JAVASCRIPT_ASSET_PATH = "/studio-assets/studio.js"
STUDIO_LOCAL_PREVIEW_CSP = (
    "default-src 'none'; "
    "base-uri 'none'; "
    "object-src 'none'; "
    "frame-ancestors 'none'; "
    "form-action 'none'; "
    "style-src 'self'; "
    "script-src 'self'; "
    "connect-src 'self'"
)
SETUP_GUIDANCE_CLAIM_BOUNDARY = (
    "Setup guidance is informational in this scaffold. Disabled actions point to guidance, not to an active "
    "installer. No model is downloaded, no model is executed, no provider call is made, and cloud routes remain "
    "disabled by default."
)

StatusProvider = Callable[[], dict[str, Any]]
BrowserOpener = Callable[[str], bool]


def get_studio_asset_path_status(path: str) -> tuple[str | None, int]:
    """Return the allowed Studio asset key and status code for an asset path."""

    decoded_path = unquote(path)
    decoded_twice_path = unquote(decoded_path)
    if (
        ".." in decoded_path
        or ".." in decoded_twice_path
        or "\\" in decoded_path
        or "\\" in decoded_twice_path
        or path.startswith("/studio-assets//")
        or decoded_path.startswith("/studio-assets//")
        or decoded_twice_path.startswith("/studio-assets//")
    ):
        return None, 400
    if decoded_path in {"/studio-assets", "/studio-assets/"}:
        return None, 404
    if decoded_path == STUDIO_CSS_ASSET_PATH:
        return "studio.css", 200
    if decoded_path == STUDIO_JAVASCRIPT_ASSET_PATH:
        return "studio.js", 200
    if decoded_path.startswith("/studio-assets/"):
        return None, 404
    return None, 404


def get_studio_css_asset_path_status(path: str) -> tuple[str | None, int]:
    """Return the allowed Studio asset key and status code for backward-compatible tests."""

    return get_studio_asset_path_status(path)


def is_allowed_studio_host(host: str) -> bool:
    """Return whether a Studio server host is explicitly local-only."""

    return host in ALLOWED_STUDIO_HOSTS


def get_studio_server_status(host: str = DEFAULT_STUDIO_HOST, port: int = DEFAULT_STUDIO_PORT) -> dict[str, Any]:
    """Return static local server skeleton status without starting a server."""

    studio_status = get_studio_status()
    system_profile = get_system_profile(default_host=host, default_port=port)
    model_capability_estimate = estimate_model_capability(system_profile)
    runtime_status = get_runtime_status()
    installed_models_summary = summarize_installed_models(runtime_status)
    recommended_models = recommend_catalog_models(system_profile, model_capability_estimate, runtime_status)
    execution_viewer_fixture = get_execution_viewer_fixture_summary()
    standard_vs_kora_fixture = get_standard_vs_kora_status_fields()
    local_harness_requests = get_local_harness_requests()
    local_harness_request_summary = get_local_harness_request_summary()
    local_harness_sample_run = build_local_harness_events(local_harness_requests[0])
    local_harness_counters = dict(local_harness_sample_run["counters_snapshot"])
    local_harness_comparison = get_local_harness_comparison_status_fields(str(local_harness_requests[0]["request_id"]))
    report_viewer_fixture = get_report_viewer_status_fields(
        local_harness_counters,
        report_source="local_harness_summary",
    )
    local_harness_status = {
        "status": "local_deterministic_harness_available",
        "event_source_status": "generated_events_available",
        "run_trigger_status": "api_endpoint_connected",
        "run_trigger_endpoint": "/api/harness/run",
        "run_retrieval_endpoint": "/api/harness/run/{run_id}",
        "events_endpoint": "/api/harness/events?run_id=<id>",
        "events_endpoint_status": "generated_events_retrieval_connected",
        "sse_endpoint": "/api/harness/sse?run_id=<id>",
        "sse_endpoint_status": "generated_events_stream_connected",
        "approved_request_ids_only": True,
        "arbitrary_prompt_execution_connected": False,
        "sample_request_count": len(local_harness_requests),
        "sample_run_id": local_harness_sample_run["run_id"],
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "model_execution_connected": False,
        "download_connected": False,
        "claim_boundary": LOCAL_HARNESS_EVENT_CLAIM_BOUNDARY,
    }
    local_harness_run_store = get_local_harness_run_store_status()
    first_run_section_order = [
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
    launch_boundary = {
        "host": host,
        "port": port,
        "url": get_studio_url(host=host, port=port),
        "server": "local-only",
        "allowed_hosts": sorted(ALLOWED_STUDIO_HOSTS),
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "browser_launch_available": True,
        "api_key_required": False,
        "claim_boundary": (
            "The Studio preview is localhost-only by default. Provider calls and cloud sync are disabled, "
            "and no API key is required for the default local preview."
        ),
    }
    disabled_action_state = {
        "download_connected": False,
        "run_connected": False,
        "model_execution_connected": False,
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "disabled_actions_route_to_guidance": True,
        "setup_guidance_url": SETUP_GUIDANCE_PATH,
        "claim_boundary": (
            "Download and run actions remain disabled until explicitly connected. Disabled actions point to "
            "informational setup guidance, not to an active installer or model runner."
        ),
    }
    v0_2_status = {
        "milestone": "v0.2",
        "status": "first_run_preview",
        "readiness": "local_preview_demo_ready",
        "description": "Local first-run setup preview for the AI Task Execution Router demo.",
        "first_run_section_order": list(first_run_section_order),
        "claim_boundary": (
            "v0.2 is a local preview/demo readiness milestone, not a production release. Execution data is "
            "fixture/mock only until live harness wiring is implemented."
        ),
    }
    studio_status_block = {
        "service": "kora-studio",
        "status": "preview",
        "implementation": "local_server_skeleton",
        "positioning": "local-first AI Task Execution Router workspace",
        "v0_1_readiness_status": "local_fixture_demo_ready",
        "v0_2_status": v0_2_status,
    }
    claim_boundaries = {
        "studio": v0_2_status["claim_boundary"],
        "launch": launch_boundary["claim_boundary"],
        "model_capability": str(model_capability_estimate.get("claim_boundary", "")),
        "model_catalog": MODEL_CATALOG_CLAIM_BOUNDARY,
        "runtime_setup_guidance": SETUP_GUIDANCE_CLAIM_BOUNDARY,
        "disabled_actions": disabled_action_state["claim_boundary"],
        "execution_viewer": str(execution_viewer_fixture.get("execution_viewer_claim_boundary", "")),
        "standard_vs_kora": str(standard_vs_kora_fixture.get("standard_vs_kora_claim_boundary", "")),
        "report_viewer": str(report_viewer_fixture.get("report_viewer_claim_boundary", "")),
        "local_harness": LOCAL_HARNESS_EVENT_CLAIM_BOUNDARY,
        "local_harness_run": LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
        "local_harness_comparison": str(local_harness_comparison.get("comparison_claim_boundary", "")),
    }
    return {
        "ok": True,
        "service": "kora-studio",
        "status": "preview",
        "implementation": "local_server_skeleton",
        "studio_status": studio_status_block,
        "launch_boundary": launch_boundary,
        "v0_2_status": v0_2_status,
        "v0_1_readiness_status": "local_fixture_demo_ready",
        "v0_1_demo_surfaces": list(first_run_section_order),
        "v0_1_claim_boundary": (
            "KORA Studio v0.1 is a local fixture-backed AI Task Execution Router demo scaffold. It is not "
            "production-ready, does not execute models, does not download models, does not call providers, "
            "and does not enable cloud sync."
        ),
        "server": "local-only",
        "host": host,
        "port": port,
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "system_profile": system_profile.to_dict(),
        "model_capability_estimate": model_capability_estimate,
        "model_catalog_status": "static_local_scaffold",
        "recommended_models": recommended_models,
        "model_catalog_claim_boundary": MODEL_CATALOG_CLAIM_BOUNDARY,
        "runtime_status": runtime_status,
        "installed_models_summary": installed_models_summary,
        "catalog_runtime_distinction": (
            "Catalog examples are not the same as installed models. Installed model detection is not connected by "
            "default. Download and execution are not connected yet."
        ),
        "setup_guidance_status": "informational_scaffold",
        "setup_guidance_url": SETUP_GUIDANCE_PATH,
        "setup_guidance_claim_boundary": SETUP_GUIDANCE_CLAIM_BOUNDARY,
        "disabled_actions_route_to_guidance": True,
        "disabled_action_state": disabled_action_state,
        "local_harness_status": local_harness_status,
        "local_harness_run_store": local_harness_run_store,
        "local_harness_request_summary": local_harness_request_summary,
        "local_harness_requests": local_harness_requests,
        "local_harness_sample_run": local_harness_sample_run,
        "local_harness_counters": local_harness_counters,
        "local_harness_claim_boundary": LOCAL_HARNESS_EVENT_CLAIM_BOUNDARY,
        "local_harness_run_claim_boundary": LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
        **execution_viewer_fixture,
        **standard_vs_kora_fixture,
        **local_harness_comparison,
        **report_viewer_fixture,
        "claim_boundaries": claim_boundaries,
        "first_run_section_order": first_run_section_order,
        "browser_launch_available": True,
        "ollama_calls_enabled": False,
        "local_runtime_required": False,
        "no_server_side_provider_calls": True,
        "docs_path": studio_status["docs_path"],
        "fixtures_path": studio_status["fixtures_path"],
        "kora_boost_message": studio_status["kora_boost_message"],
        "kora_boost_technical_explanation": studio_status["kora_boost_technical_explanation"],
    }


def get_harness_run_error_payload(error: str, message: str, *, request_id: str | None = None) -> dict[str, Any]:
    """Return a claim-safe local harness run error response."""

    payload: dict[str, Any] = {
        "ok": False,
        "error": error,
        "message": message,
        "run_status": "failed",
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "model_execution_connected": False,
        "download_connected": False,
        "arbitrary_prompt_execution_connected": False,
        "claim_boundary": LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
    }
    if request_id is not None:
        payload["request_id"] = request_id
    return payload


def get_studio_health_payload() -> dict[str, Any]:
    """Return the /health response payload."""

    return {
        "ok": True,
        "service": "kora-studio",
        "status": "preview",
        "server": "local-only",
        "provider_calls_enabled": False,
        "cloud_sync_enabled": False,
        "browser_launch_available": True,
    }


def get_studio_status_payload(host: str = DEFAULT_STUDIO_HOST, port: int = DEFAULT_STUDIO_PORT) -> dict[str, Any]:
    """Return the /status response payload."""

    return get_studio_server_status(host=host, port=port)


def get_studio_url(host: str = DEFAULT_STUDIO_HOST, port: int = DEFAULT_STUDIO_PORT) -> str:
    """Return the local KORA Studio URL."""

    return f"http://{host}:{port}/"


def open_studio_browser(url: str, browser_opener: BrowserOpener = webbrowser.open) -> bool:
    """Open the Studio URL with a mockable browser opener."""

    try:
        return bool(browser_opener(url))
    except Exception:
        return False


def render_studio_server_status_text(
    status: dict[str, Any],
    *,
    open_browser: bool = True,
    browser_opened: bool | None = None,
) -> str:
    """Render local server skeleton startup status for CLI output."""

    url = get_studio_url(str(status["host"]), int(status["port"]))
    lines = [
        "Launching KORA Studio...",
        "",
        "Local URL:",
        url,
        "",
        "Mode:",
        "Local-only",
        "Provider calls: disabled",
        "Cloud sync: disabled",
        "",
        "Press Ctrl+C to stop.",
    ]
    if open_browser and browser_opened is False:
        lines.extend(["", "Browser launch failed. Open this URL manually:", url])
    elif not open_browser:
        lines.extend(["", "Browser launch: disabled by --no-browser."])
    return "\n".join(lines) + "\n"


def render_studio_placeholder_html(status: dict[str, Any]) -> str:
    """Render the static KORA Studio preview page."""

    docs_path = html.escape(str(status["docs_path"]), quote=True)
    fixtures_path = html.escape(str(status["fixtures_path"]), quote=True)
    boost_message = html.escape(str(status["kora_boost_message"]), quote=True)
    boost_explanation = html.escape(str(status["kora_boost_technical_explanation"]), quote=True)
    system_profile = status.get("system_profile", {})
    model_capability = status.get("model_capability_estimate", {})
    os_name = html.escape(str(system_profile.get("os_name", "unknown")), quote=True)
    machine = html.escape(str(system_profile.get("machine", "unknown")), quote=True)
    memory = system_profile.get("total_memory_gb")
    memory_text = "unknown" if memory is None else f"{memory} GB"
    memory_text = html.escape(memory_text, quote=True)
    memory_status = html.escape(str(system_profile.get("memory_detection_status", "unknown")), quote=True)
    ollama_status = "detected" if system_profile.get("ollama_detected") is True else "not detected"
    llama_cpp_status = "detected" if system_profile.get("llama_cpp_detected") is True else "not detected"
    recommended_tier = html.escape(
        str(model_capability.get("recommended_local_chat_tier", "unknown")),
        quote=True,
    )
    physical_notes = html.escape(
        str(model_capability.get("physically_runnable_model_notes", "Unknown until validated.")),
        quote=True,
    )
    workflow_notes = html.escape(
        str(model_capability.get("larger_model_workflow_notes", "")),
        quote=True,
    )
    claim_boundary = html.escape(
        str(model_capability.get("claim_boundary", "Recommendations are estimates until validated on this machine.")),
        quote=True,
    )
    recommended_models = status.get("recommended_models", [])
    catalog_status = html.escape(str(status.get("model_catalog_status", "static_local_scaffold")), quote=True)
    catalog_boundary = html.escape(
        str(status.get("model_catalog_claim_boundary", MODEL_CATALOG_CLAIM_BOUNDARY)),
        quote=True,
    )
    runnable_models = [
        item
        for item in recommended_models
        if isinstance(item, dict) and item.get("candidate_type") == "physically_runnable_local_candidate"
    ]
    workflow_models = [
        item
        for item in recommended_models
        if isinstance(item, dict) and item.get("candidate_type") == "larger_model_workflow_candidate"
    ]
    unknown_models = [
        item for item in recommended_models if isinstance(item, dict) and item.get("candidate_type") == "unknown_needs_validation"
    ]
    local_candidate = runnable_models[0] if runnable_models else (unknown_models[0] if unknown_models else {})
    workflow_candidate = workflow_models[0] if workflow_models else {}
    local_candidate_name = html.escape(str(local_candidate.get("display_name", "Unknown until validated")), quote=True)
    local_candidate_note = html.escape(
        str(local_candidate.get("recommendation_note", "Model recommendations are estimates until validated on this machine.")),
        quote=True,
    )
    local_candidate_id = html.escape(str(local_candidate.get("model_id", "unknown")), quote=True)
    local_candidate_type = html.escape(str(local_candidate.get("candidate_type", "unknown_needs_validation")), quote=True)
    local_candidate_memory = html.escape(str(local_candidate.get("estimated_memory_gb", "unknown")), quote=True)
    local_candidate_installed = "true" if local_candidate.get("installed_locally") is True else "false"
    local_candidate_installed = html.escape(local_candidate_installed, quote=True)
    model_selector_items = "".join(
        render_model_selector_option(
            display_name=html.escape(str(model.get("display_name", "Unknown model")), quote=True),
            model_id=html.escape(str(model.get("model_id", "unknown")), quote=True),
            candidate_type=html.escape(str(model.get("candidate_type", "needs_validation")), quote=True),
            estimated_memory_gb=html.escape(str(model.get("estimated_memory_gb", "unknown")), quote=True),
            installed_locally=html.escape("true" if model.get("installed_locally") is True else "false", quote=True),
        )
        for model in recommended_models
        if isinstance(model, dict)
    )
    model_selector_count = html.escape(str(len([model for model in recommended_models if isinstance(model, dict)])), quote=True)
    local_download_label = html.escape(str(local_candidate.get("download_action_label", "Download not connected yet")), quote=True)
    local_run_label = html.escape(str(local_candidate.get("run_action_label", "Run not connected yet")), quote=True)
    local_download_reason = html.escape(str(local_candidate.get("download_action_reason", "")), quote=True)
    local_run_reason = html.escape(str(local_candidate.get("run_action_reason", "")), quote=True)
    local_action_boundary = html.escape(
        str(
            local_candidate.get(
                "action_claim_boundary",
                "Model actions are disabled planning scaffolds. Catalog examples are not installed models.",
            )
        ),
        quote=True,
    )
    workflow_candidate_name = html.escape(str(workflow_candidate.get("display_name", "Larger workflow example")), quote=True)
    workflow_candidate_note = html.escape(
        str(
            workflow_candidate.get(
                "recommendation_note",
                "Larger-model workflows may become more practical when deterministic work avoids the model path.",
            )
        ),
        quote=True,
    )
    runtime_status = status.get("runtime_status", [])
    installed_summary = status.get("installed_models_summary", {})
    first_runtime = runtime_status[0] if isinstance(runtime_status, list) and runtime_status else {}
    runtime_name = html.escape(str(first_runtime.get("display_name", "Unknown runtime")), quote=True)
    runtime_detected = "detected" if first_runtime.get("executable_detected") is True else "not detected"
    service_status = html.escape(str(first_runtime.get("service_check_status", "not_checked")), quote=True)
    service_url = html.escape(str(first_runtime.get("service_url") or "not configured"), quote=True)
    service_boundary = html.escape(
        str(
            first_runtime.get(
                "service_probe_claim_boundary",
                "Service reachability is a localhost-only check. It does not execute models.",
            )
        ),
        quote=True,
    )
    installed_status = html.escape(str(installed_summary.get("detection_status", "not_checked")), quote=True)
    installed_enabled = (
        "enabled" if installed_summary.get("installed_model_detection_enabled") is True else "disabled"
    )
    installed_enabled = html.escape(installed_enabled, quote=True)
    installed_method = html.escape(str(installed_summary.get("installed_model_detection_method", "not_connected")), quote=True)
    installed_count = html.escape(str(installed_summary.get("installed_models_count", 0)), quote=True)
    installed_boundary = html.escape(
        str(
            installed_summary.get(
                "claim_boundary",
                "Installed model detection is local-only and disabled by default. Catalog examples are not installed models.",
            )
        ),
        quote=True,
    )
    setup_guidance_status = html.escape(str(status.get("setup_guidance_status", "informational_scaffold")), quote=True)
    setup_guidance_url = html.escape(str(status.get("setup_guidance_url", SETUP_GUIDANCE_PATH)), quote=True)
    setup_guidance_boundary = html.escape(
        str(status.get("setup_guidance_claim_boundary", SETUP_GUIDANCE_CLAIM_BOUNDARY)),
        quote=True,
    )
    execution_events = [
        item for item in status.get("execution_viewer_fixture_events", []) if isinstance(item, dict)
    ]
    execution_status = html.escape(str(status.get("execution_viewer_status", "fixture_mock_scaffold")), quote=True)
    execution_event_count = html.escape(str(status.get("execution_viewer_fixture_event_count", len(execution_events))), quote=True)
    execution_schema_count = html.escape(
        str(len(status.get("execution_viewer_event_schema_fields", []))),
        quote=True,
    )
    execution_boundary = html.escape(
        str(
            status.get(
                "execution_viewer_claim_boundary",
                "Execution Viewer events are local fixture/mock data and do not execute models.",
            )
        ),
        quote=True,
    )
    standard_vs_kora_status = html.escape(
        str(status.get("local_harness_comparison_status", status.get("standard_vs_kora_comparison_status", "fixture_mock_scaffold"))),
        quote=True,
    )
    standard_vs_kora_boundary = html.escape(
        str(
            status.get(
                "comparison_claim_boundary",
                status.get(
                    "standard_vs_kora_claim_boundary",
                    "Standard Mode vs KORA Boost comparison data is local fixture/mock data.",
                ),
            )
        ),
        quote=True,
    )
    comparison = status.get("local_harness_comparison") or status.get("standard_vs_kora_comparison", {})
    comparison_modes = comparison.get("modes", []) if isinstance(comparison, dict) else []
    standard_mode = next(
        (item for item in comparison_modes if isinstance(item, dict) and item.get("mode") == "standard"),
        {},
    )
    kora_mode = next(
        (item for item in comparison_modes if isinstance(item, dict) and item.get("mode") == "kora_boost"),
        {},
    )
    standard_route_summary = html.escape(str(standard_mode.get("route_summary", "")), quote=True)
    kora_route_summary = html.escape(str(kora_mode.get("route_summary", "")), quote=True)
    metric_cards = [
        item
        for item in (
            status.get("local_harness_comparison_metric_cards")
            or status.get("standard_vs_kora_metric_cards", [])
        )
        if isinstance(item, dict)
    ]
    standard_vs_kora_metric_items = "".join(
        "<div class=\"card\">"
        f"<h3>{html.escape(str(card.get('label', 'Metric')), quote=True)}</h3>"
        f"<p class=\"status-value\">{html.escape(str(card.get('value', 0)), quote=True)}</p>"
        f"<p>{html.escape(str(card.get('claim_safety_note', 'Local fixture/mock comparison data only.')), quote=True)}</p>"
        "</div>"
        for card in metric_cards
    )
    execution_event_items = "".join(
        "<li>"
        f"{html.escape(str(event.get('stage_name', 'Unknown stage')), quote=True)} "
        f"({html.escape(str(event.get('route_class', 'unknown')), quote=True)} / "
        f"{html.escape(str(event.get('status', 'unknown')), quote=True)})"
        "</li>"
        for event in execution_events
    )
    report_viewer = status.get("report_viewer_placeholder", {})
    report_export = status.get("report_export_placeholder", {})
    report_viewer_status = html.escape(str(status.get("report_viewer_status", "fixture_metadata_placeholder")), quote=True)
    report_title = html.escape(str(report_viewer.get("report_title", "Local report fixture")), quote=True)
    report_fixture_path = html.escape(str(report_viewer.get("report_fixture_path", "")), quote=True)
    report_path_display = html.escape(str(report_viewer.get("report_path_display", "not loaded")), quote=True)
    report_boundary = html.escape(str(status.get("report_viewer_claim_boundary", "")), quote=True)
    report_export_status = html.escape(str(status.get("report_export_status", "placeholder_not_connected")), quote=True)
    report_export_label = html.escape(str(report_export.get("export_action_label", "Export not connected yet")), quote=True)
    report_export_reason = html.escape(str(report_export.get("export_action_reason", "")), quote=True)
    report_export_boundary = html.escape(str(status.get("report_export_claim_boundary", "")), quote=True)
    report_source = html.escape(str(report_viewer.get("report_source", "local_harness_summary")), quote=True)
    report_comparison_status = html.escape(
        str(status.get("local_harness_comparison_status", "local_deterministic_harness_generated")),
        quote=True,
    )
    report_file_export_enabled = "enabled" if report_viewer.get("file_export_enabled") is True else "disabled"
    report_file_export_enabled = html.escape(report_file_export_enabled, quote=True)
    report_file_written = "true" if report_viewer.get("file_written") is True else "false"
    report_file_written = html.escape(report_file_written, quote=True)
    report_sections = "".join(
        f"<li>{html.escape(str(item), quote=True)}</li>"
        for item in report_viewer.get("sections", [])
    )
    report_warnings = "".join(
        f"<li>{html.escape(str(item), quote=True)}</li>"
        for item in report_viewer.get("boundary_warnings", [])
    )
    report_counters = report_viewer.get("counters", {}) if isinstance(report_viewer, dict) else {}
    report_counter_items = "".join(
        "<div class=\"card\">"
        f"<h3>{html.escape(str(key), quote=True)}</h3>"
        f"<p class=\"status-value\">{html.escape(str(value), quote=True)}</p>"
        "<p>Local deterministic harness output only.</p>"
        "</div>"
        for key, value in report_counters.items()
        if key in {"total_requests", "baseline_model_calls", "kora_model_calls", "avoided_model_calls"}
    )
    section_order_items = "".join(
        f"<li>{html.escape(str(item), quote=True)}</li>"
        for item in status.get(
            "first_run_section_order",
            [
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
            ],
        )
    )
    local_harness_status = status.get("local_harness_status", {})
    local_harness_requests = [
        item for item in status.get("local_harness_requests", []) if isinstance(item, dict)
    ]
    local_harness_sample_run = status.get("local_harness_sample_run", {})
    local_harness_counters = status.get("local_harness_counters", {})
    total_requests = html.escape(str(local_harness_counters.get("total_requests", 0)), quote=True)
    baseline_model_calls = html.escape(str(local_harness_counters.get("baseline_model_calls", 0)), quote=True)
    kora_model_calls = html.escape(str(local_harness_counters.get("kora_model_calls", 0)), quote=True)
    avoided_model_calls = html.escape(str(local_harness_counters.get("avoided_model_calls", 0)), quote=True)
    local_harness_status_text = html.escape(str(local_harness_status.get("status", "not_connected")), quote=True)
    local_harness_event_source = html.escape(str(local_harness_status.get("event_source_status", "not_connected")), quote=True)
    local_harness_run_trigger = html.escape(str(local_harness_status.get("run_trigger_status", "not_connected")), quote=True)
    local_harness_request_count = html.escape(
        str(local_harness_status.get("sample_request_count", len(local_harness_requests))),
        quote=True,
    )
    local_harness_boundary = html.escape(str(status.get("local_harness_claim_boundary", "")), quote=True)
    sample_request = local_harness_sample_run.get("request", {}) if isinstance(local_harness_sample_run, dict) else {}
    report_sample_run_id = html.escape(str(local_harness_sample_run.get("run_id", "local-harness-sample")), quote=True)
    report_sample_request_id = html.escape(
        str(local_harness_sample_run.get("request_id", sample_request.get("request_id", "unknown"))),
        quote=True,
    )
    report_event_count = html.escape(
        str(local_harness_sample_run.get("event_count", len(local_harness_sample_run.get("events", [])))),
        quote=True,
    )
    sample_request_id = html.escape(
        str(sample_request.get("request_id", local_harness_sample_run.get("request_id", "unknown"))),
        quote=True,
    )
    sample_input = html.escape(str(sample_request.get("input_text", "No sample request selected.")), quote=True)
    sample_family = html.escape(str(sample_request.get("task_family", "unknown")), quote=True)
    sample_route = html.escape(str(sample_request.get("expected_route_class", "unknown")), quote=True)
    sample_validation = html.escape(str(sample_request.get("expected_validation_result", "unknown")), quote=True)
    sample_model_needed = html.escape(str(sample_request.get("expected_model_needed", "unknown")), quote=True)
    local_harness_request_items = "".join(
        "<li>"
        f"{html.escape(str(request.get('request_id', 'unknown')), quote=True)} "
        f"({html.escape(str(request.get('task_family', 'unknown')), quote=True)} / "
        f"{html.escape(str(request.get('expected_route_class', 'unknown')), quote=True)})"
        "</li>"
        for request in local_harness_requests
    )
    local_harness_trigger_items = "".join(
        render_local_harness_trigger_item(
            request_id=html.escape(str(request.get("request_id", "unknown")), quote=True),
            input_text=html.escape(str(request.get("input_text", "Approved local sample request.")), quote=True),
            task_family=html.escape(str(request.get("task_family", "unknown")), quote=True),
            route_class=html.escape(str(request.get("expected_route_class", "unknown")), quote=True),
            model_needed=html.escape(str(request.get("expected_model_needed", False)), quote=True),
        )
        for request in local_harness_requests
    )
    selector_preview_request = local_harness_requests[0] if local_harness_requests else {}
    selector_preview_id = html.escape(str(selector_preview_request.get("request_id", "unknown")), quote=True)
    selector_preview_text = html.escape(str(selector_preview_request.get("input_text", "No approved request selected.")), quote=True)
    selector_preview_route = html.escape(str(selector_preview_request.get("expected_route_class", "unknown")), quote=True)
    selector_preview_model_needed = html.escape(str(selector_preview_request.get("expected_model_needed", "unknown")), quote=True)
    local_harness_requests_json = json.dumps(local_harness_requests, sort_keys=True).replace("</", "<\\/")
    local_harness_selector_items = "".join(
        render_local_harness_selector_item(
            request_id=html.escape(str(request.get("request_id", "unknown")), quote=True),
            input_text=html.escape(str(request.get("input_text", "Approved local sample request.")), quote=True),
            route_class=html.escape(str(request.get("expected_route_class", "unknown")), quote=True),
            model_needed=html.escape(str(request.get("expected_model_needed", False)), quote=True),
        )
        for request in local_harness_requests
    )
    local_harness_request_selector_html = render_local_harness_request_selector_panels(
        selector_preview_id=selector_preview_id,
        selector_preview_text=selector_preview_text,
        selector_preview_route=selector_preview_route,
        selector_preview_model_needed=selector_preview_model_needed,
        selector_items_html=local_harness_selector_items,
    )
    local_harness_trigger_reference_html = render_local_harness_trigger_reference_panels(
        trigger_items_html=local_harness_trigger_items,
    )
    local_harness_event_items = "".join(
        "<li>"
        f"{html.escape(str(event.get('stage_name', 'Unknown stage')), quote=True)} "
        f"({html.escape(str(event.get('route_class', 'unknown')), quote=True)} / "
        f"{html.escape(str(event.get('status', 'unknown')), quote=True)})"
        "</li>"
        for event in local_harness_sample_run.get("events", [])
        if isinstance(event, dict)
    )
    local_harness_timeline_items = "".join(
        "<div class=\"card\">"
        f"<h3>{html.escape(str(event.get('stage_name', 'Unknown stage')), quote=True)}</h3>"
        f"<p>Stage: <code>{html.escape(str(event.get('stage_id', 'unknown')), quote=True)}</code></p>"
        f"<p>Route class: {html.escape(str(event.get('route_class', 'unknown')), quote=True)}</p>"
        f"<p>Status: {html.escape(str(event.get('status', 'unknown')), quote=True)}</p>"
        f"<p>Model called: {html.escape(str(event.get('model_called', False)), quote=True)}</p>"
        f"<p>Deterministic route used: {html.escape(str(event.get('deterministic_route_used', False)), quote=True)}</p>"
        f"<p>Validation result: {html.escape(str(event.get('validation_result', 'not_applicable')), quote=True)}</p>"
        f"<p>Latency: {html.escape(str(event.get('latency_ms', 0)), quote=True)} ms</p>"
        "</div>"
        for event in local_harness_sample_run.get("events", [])
        if isinstance(event, dict)
    )
    local_harness_counter_items = "".join(
        "<div class=\"card\">"
        f"<h3>{html.escape(str(key), quote=True)}</h3>"
        f"<p class=\"status-value\">{html.escape(str(local_harness_counters.get(key, 0)), quote=True)}</p>"
        "<p>Local deterministic harness output.</p>"
        "</div>"
        for key in [
            "total_requests",
            "baseline_model_calls",
            "kora_model_calls",
            "avoided_model_calls",
            "deterministic_routes",
            "model_escalations",
            "validation_pass_count",
        ]
    )
    selected_run_summary_html = render_selected_run_summary_panel(selector_preview_id=selector_preview_id)
    selected_run_state_html = render_selected_run_state_panel()
    selected_run_detail_panels_html = render_selected_run_detail_panels()
    run_state_history_html = render_run_state_history_panels(selector_preview_id=selector_preview_id)
    shell_boundary_strip_html = render_shell_boundary_strip()
    launch_local_status_html = render_launch_local_status_section(section_order_items=section_order_items)
    system_profile_html = render_system_profile_section(
        os_name=os_name,
        machine=machine,
        memory_text=memory_text,
        memory_status=memory_status,
        ollama_status=ollama_status,
        llama_cpp_status=llama_cpp_status,
    )
    model_capability_html = render_model_capability_section(
        recommended_tier=recommended_tier,
        physical_notes=physical_notes,
        workflow_notes=workflow_notes,
        claim_boundary=claim_boundary,
    )
    runtime_status_html = render_runtime_status_section(
        runtime_name=runtime_name,
        runtime_detected=runtime_detected,
        service_status=service_status,
        service_url=service_url,
        service_boundary=service_boundary,
        installed_enabled=installed_enabled,
        installed_method=installed_method,
    )
    catalog_installed_html = render_catalog_installed_section(
        catalog_status=catalog_status,
        local_candidate_name=local_candidate_name,
        local_candidate_note=local_candidate_note,
        workflow_candidate_name=workflow_candidate_name,
        workflow_candidate_note=workflow_candidate_note,
        installed_status=installed_status,
        installed_count=installed_count,
        catalog_boundary=catalog_boundary,
        installed_boundary=installed_boundary,
    )
    setup_guidance_html = render_setup_guidance_section(
        setup_guidance_status=setup_guidance_status,
        setup_guidance_url=setup_guidance_url,
        setup_guidance_boundary=setup_guidance_boundary,
    )
    disabled_actions_html = render_disabled_actions_section(
        local_download_label=local_download_label,
        local_download_reason=local_download_reason,
        local_run_label=local_run_label,
        local_run_reason=local_run_reason,
        local_action_boundary=local_action_boundary,
    )
    kora_boost_boundary_html = render_kora_boost_boundary_section()
    local_harness_preview_html = render_local_harness_preview_section(
        local_harness_status_text=local_harness_status_text,
        local_harness_event_source=local_harness_event_source,
        local_harness_run_trigger=local_harness_run_trigger,
        local_harness_request_count=local_harness_request_count,
        sample_request_id=sample_request_id,
        sample_input=sample_input,
        sample_family=sample_family,
        sample_route=sample_route,
        sample_validation=sample_validation,
        sample_model_needed=sample_model_needed,
        local_harness_boundary=local_harness_boundary,
        request_selector_html=local_harness_request_selector_html,
        selected_run_state_html=selected_run_state_html,
        run_state_history_html=run_state_history_html,
        selected_run_detail_panels_html=selected_run_detail_panels_html,
        trigger_reference_html=local_harness_trigger_reference_html,
        local_harness_request_items=local_harness_request_items,
        local_harness_event_items=local_harness_event_items,
        local_harness_timeline_items=local_harness_timeline_items,
        local_harness_counter_items=local_harness_counter_items,
    )
    execution_viewer_html = render_execution_viewer_section(
        execution_status=execution_status,
        execution_schema_count=execution_schema_count,
        execution_event_count=execution_event_count,
        execution_boundary=execution_boundary,
        execution_event_items=execution_event_items,
    )
    standard_vs_kora_html = render_standard_vs_kora_section(
        standard_vs_kora_status=standard_vs_kora_status,
        standard_route_summary=standard_route_summary,
        kora_route_summary=kora_route_summary,
        standard_vs_kora_boundary=standard_vs_kora_boundary,
        standard_vs_kora_metric_items=standard_vs_kora_metric_items,
    )
    report_viewer_html = render_report_viewer_placeholder_section(
        report_viewer_status=report_viewer_status,
        report_title=report_title,
        report_source=report_source,
        report_sample_run_id=report_sample_run_id,
        report_sample_request_id=report_sample_request_id,
        report_event_count=report_event_count,
        report_comparison_status=report_comparison_status,
        report_export_status=report_export_status,
        report_export_label=report_export_label,
        report_file_export_enabled=report_file_export_enabled,
        report_file_written=report_file_written,
        report_export_reason=report_export_reason,
        report_export_boundary=report_export_boundary,
        report_boundary=report_boundary,
        report_path_display=report_path_display,
        report_fixture_path=report_fixture_path,
        report_sections=report_sections,
        report_warnings=report_warnings,
        report_counter_items=report_counter_items,
    )

    composer_html = f"""      <section class=\"composer-stage\" aria-label=\"KORA Studio centered composer\" data-kora-component=\"composer\">
        <div class=\"composer-panel\">
          <h1>What do you want to work on?</h1>
          <p class=\"subtitle\">Choose a local model once. KORA keeps routing details out of the way.</p>
          <div class=\"composer-box\" role=\"group\" aria-label=\"KORA composer scaffold\">
            <span>Ask KORA...</span>
            <button class=\"composer-submit\" type=\"button\" id=\"kora-composer-run-local-harness-button\" aria-label=\"Run approved local harness request\">↑</button>
          </div>
          <p class=\"composer-action-note\">Composer action uses the selected approved local harness request only. No arbitrary prompt execution, no model execution, no provider calls, and no downloads.</p>
{selected_run_summary_html}
          <div class=\"shell-selected-run-strip\" data-kora-shell-selected-run-surface=\"v1.0\" data-kora-shell-selected-run-coverage=\"timeline,counters,comparison,report-metadata\" data-kora-v1-1-selected-run-polish=\"shell-drawer-status\" aria-live=\"polite\">
            <h2>Selected run details</h2>
            <div class=\"shell-selected-run-grid\">
              <span>Timeline: <code id=\"kora-shell-selected-timeline-status\">not loaded</code></span>
              <span>Counters: <code id=\"kora-shell-selected-counters-status\">not loaded</code></span>
              <span>Comparison: <code id=\"kora-shell-selected-comparison-status\">not loaded</code></span>
              <span>Report: <code id=\"kora-shell-selected-report-status\">not loaded</code></span>
            </div>
            <p>Shell selected-run surface mirrors generated local harness output only. Details drawer mirrors the same selected-run status so legacy preview is not required for normal inspection. No model execution, provider calls, downloads, cloud sync, or report export is connected.</p>
          </div>
{shell_boundary_strip_html}
        </div>
      </section>"""
    details_drawer_html = render_right_details_drawer(
        runtime_name=runtime_name,
        runtime_detected=runtime_detected,
        service_status=service_status,
        local_candidate_name=local_candidate_name,
        catalog_status=catalog_status,
        installed_status=installed_status,
        installed_count=installed_count,
        sample_request_id=sample_request_id,
        sample_route=sample_route,
        sample_validation=sample_validation,
        total_requests=total_requests,
        baseline_model_calls=baseline_model_calls,
        kora_model_calls=kora_model_calls,
        avoided_model_calls=avoided_model_calls,
        report_viewer_status=report_viewer_status,
        report_source=report_source,
        report_file_export_enabled=report_file_export_enabled,
        report_file_written=report_file_written,
    )
    legacy_preview_html = render_legacy_preview_opening()
    shell_layout_html = render_shell_layout(
        local_candidate_name=local_candidate_name,
        local_candidate_id=local_candidate_id,
        local_candidate_type=local_candidate_type,
        local_candidate_memory=local_candidate_memory,
        local_candidate_installed=local_candidate_installed,
        model_selector_count=model_selector_count,
        model_selector_items=model_selector_items,
        composer_html=composer_html,
        details_drawer_html=details_drawer_html,
        legacy_preview_html=legacy_preview_html,
    )

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>KORA Studio</title>
  <link rel=\"stylesheet\" href=\"{STUDIO_CSS_ASSET_PATH}\">
</head>
<body>
{shell_layout_html}
    <header>
      <div class=\"topline\">
        <strong>Local Preview Scaffold</strong>
        <span class=\"badge\">Preview / Local-only</span>
      </div>
      <h1>KORA Studio</h1>
      <p class=\"subtitle\">A static AI Task Execution Router prototype for deterministic-first local workflow exploration. KORA Studio routes local AI workflows, not just local models.</p>
      <p class=\"boost\">{boost_message}</p>
      <p class=\"technical\">{boost_explanation}</p>
      <p class=\"technical\">Standard Mode sends every step to the model. KORA Boost routes deterministic and structured tasks to CPU/local fast paths first, so the model becomes one execution path, not the default path.</p>
    </header>

{launch_local_status_html}

    <div class=\"section-stack\">
{system_profile_html}
{model_capability_html}
{runtime_status_html}
{catalog_installed_html}
{setup_guidance_html}
{disabled_actions_html}

{kora_boost_boundary_html}

{local_harness_preview_html}

{execution_viewer_html}

{standard_vs_kora_html}

{report_viewer_html}

{render_reference_panels(docs_path=docs_path, fixtures_path=fixtures_path)}
    </div>

    <p class=\"footer\">Local-only skeleton. Claim-safe AI Task Execution Router preview; KORA does not make large models smaller or remove memory requirements.</p>
    </div>
  </details>
  <script type=\"application/json\" id=\"kora-approved-requests-data\">{local_harness_requests_json}</script>
  <script src=\"/studio-assets/studio.js\"></script>
</body>
</html>
"""


def create_studio_request_handler(status_provider: StatusProvider | None = None) -> type[BaseHTTPRequestHandler]:
    """Create a request handler class for the local Studio preview server."""

    provider = status_provider or get_studio_server_status

    class StudioRequestHandler(BaseHTTPRequestHandler):
        server_version = "KORAStudioPreview/0.1"

        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            return

        def _write_json(self, payload: dict[str, Any], status_code: int = 200) -> None:
            body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _write_html(self, html: str, status_code: int = 200) -> None:
            body = html.encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Security-Policy", STUDIO_LOCAL_PREVIEW_CSP)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _write_css(self, css: str, status_code: int = 200) -> None:
            body = css.encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _write_javascript(self, javascript: str, status_code: int = 200) -> None:
            body = javascript.encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _write_sse(self, stream: str, status_code: int = 200) -> None:
            body = stream.encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "close")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _read_json_body(self) -> dict[str, Any] | None:
            try:
                content_length = int(self.headers.get("Content-Length", "0") or "0")
            except ValueError:
                return None
            if content_length <= 0:
                return None
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return None
            return payload if isinstance(payload, dict) else None

        def do_GET(self) -> None:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            status = provider()
            if path.startswith("/studio-assets"):
                asset_key, asset_status = get_studio_asset_path_status(path)
                if asset_key == "studio.css":
                    self._write_css(render_studio_css())
                    return
                if asset_key == "studio.js":
                    self._write_javascript(render_studio_javascript())
                    return
                self._write_json({"ok": False, "error": "asset_not_found"}, status_code=asset_status)
                return
            if path == "/health":
                self._write_json(get_studio_health_payload())
                return
            if path == "/status":
                self._write_json(status)
                return
            if path == "/":
                self._write_html(render_studio_placeholder_html(status))
                return
            if path == "/api/harness/events":
                query = parse_qs(parsed_path.query)
                run_id = query.get("run_id", [""])[0]
                if not run_id:
                    self._write_json(
                        get_harness_run_error_payload(
                            "missing_run_id",
                            "GET /api/harness/events expects an existing local harness run_id query parameter.",
                        ),
                        status_code=400,
                    )
                    return
                events_payload = get_local_harness_run_events(run_id)
                if events_payload is None:
                    self._write_json(
                        get_harness_run_error_payload(
                            "run_not_found",
                            "No generated local harness events exist for this run_id.",
                        ),
                        status_code=404,
                    )
                    return
                self._write_json(events_payload)
                return
            if path == "/api/harness/sse":
                query = parse_qs(parsed_path.query)
                run_id = query.get("run_id", [""])[0]
                if not run_id:
                    self._write_json(
                        get_harness_run_error_payload(
                            "missing_run_id",
                            "GET /api/harness/sse expects an existing local harness run_id query parameter.",
                        ),
                        status_code=400,
                    )
                    return
                sse_stream = format_local_harness_sse(run_id)
                if sse_stream is None:
                    self._write_json(
                        get_harness_run_error_payload(
                            "run_not_found",
                            "No generated local harness SSE stream exists for this run_id.",
                        ),
                        status_code=404,
                    )
                    return
                self._write_sse(sse_stream)
                return
            if path.startswith("/api/harness/run/"):
                run_id = path.removeprefix("/api/harness/run/")
                run_record = get_local_harness_run_record(run_id)
                if run_record is None:
                    self._write_json(
                        get_harness_run_error_payload(
                            "run_not_found",
                            "No in-memory local harness run exists for this run_id.",
                        ),
                        status_code=404,
                    )
                    return
                self._write_json(run_record)
                return
            self._write_json({"ok": False, "error": "not_found"}, status_code=404)

        def do_POST(self) -> None:
            parsed_path = urlparse(self.path)
            if parsed_path.path != "/api/harness/run":
                self._write_json({"ok": False, "error": "post_not_supported"}, status_code=405)
                return
            payload = self._read_json_body()
            if payload is None:
                self._write_json(
                    get_harness_run_error_payload(
                        "invalid_json",
                        "POST /api/harness/run expects a JSON body with an approved request_id.",
                    ),
                    status_code=400,
                )
                return
            request_id = payload.get("request_id")
            if not isinstance(request_id, str) or not request_id:
                self._write_json(
                    get_harness_run_error_payload(
                        "invalid_request_id",
                        "POST /api/harness/run accepts only an approved local harness request_id string.",
                    ),
                    status_code=400,
                )
                return
            try:
                run_record = trigger_local_harness_run(request_id)
            except ValueError:
                self._write_json(
                    get_harness_run_error_payload(
                        "unknown_request_id",
                        "Only approved deterministic local harness sample request IDs can be triggered.",
                        request_id=request_id,
                    ),
                    status_code=404,
                )
                return
            self._write_json(run_record)

    return StudioRequestHandler


def run_studio_server(
    host: str = DEFAULT_STUDIO_HOST,
    port: int = DEFAULT_STUDIO_PORT,
    *,
    open_browser: bool = True,
    browser_opener: BrowserOpener = webbrowser.open,
) -> None:
    """Run the local-only KORA Studio preview server until interrupted."""

    if not is_allowed_studio_host(host):
        raise ValueError("KORA Studio server is local-only; use 127.0.0.1 or localhost.")

    status = get_studio_server_status(host=host, port=port)
    handler = create_studio_request_handler(lambda: get_studio_server_status(host=host, port=port))
    server = ThreadingHTTPServer((host, port), handler)
    browser_opened = open_studio_browser(get_studio_url(host, port), browser_opener) if open_browser else None
    try:
        print(
            render_studio_server_status_text(
                status,
                open_browser=open_browser,
                browser_opened=browser_opened,
            ),
            end="",
            flush=True,
        )
        server.serve_forever()
    except KeyboardInterrupt:
        print("KORA Studio local server stopped.", flush=True)
    finally:
        server.server_close()
