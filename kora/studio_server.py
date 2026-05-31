"""Local-only KORA Studio server skeleton."""

from __future__ import annotations

import html
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse

from kora.studio_drawer_render import render_right_details_drawer
from kora.studio_execution_fixture import get_execution_viewer_fixture_summary, get_standard_vs_kora_status_fields
from kora.studio_harness_comparison import get_local_harness_comparison_status_fields
from kora.studio_harness_events import LOCAL_HARNESS_EVENT_CLAIM_BOUNDARY, build_local_harness_events
from kora.studio_harness_requests import get_local_harness_request_summary, get_local_harness_requests
from kora.studio_harness_runs import (
    LOCAL_HARNESS_RUN_CLAIM_BOUNDARY,
    format_local_harness_sse,
    get_local_harness_run_record,
    get_local_harness_run_events,
    get_local_harness_run_store_status,
    trigger_local_harness_run,
)
from kora.studio_model_catalog import MODEL_CATALOG_CLAIM_BOUNDARY, SETUP_GUIDANCE_PATH, recommend_catalog_models
from kora.studio_report_viewer import get_report_viewer_status_fields
from kora.studio_runtime_status import get_runtime_status, summarize_installed_models
from kora.studio_script_render import render_studio_javascript
from kora.studio_style_render import render_studio_css
from kora.studio_selected_run_render import (
    render_selected_run_detail_panels,
    render_selected_run_state_panel,
    render_selected_run_summary_panel,
)
from kora.studio_shell_render import render_shell_layout
from kora.studio_status import get_studio_status
from kora.studio_system_profile import estimate_model_capability, get_system_profile

DEFAULT_STUDIO_HOST = "127.0.0.1"
DEFAULT_STUDIO_PORT = 8765
ALLOWED_STUDIO_HOSTS = {"127.0.0.1", "localhost"}
SETUP_GUIDANCE_CLAIM_BOUNDARY = (
    "Setup guidance is informational in this scaffold. Disabled actions point to guidance, not to an active "
    "installer. No model is downloaded, no model is executed, no provider call is made, and cloud routes remain "
    "disabled by default."
)

StatusProvider = Callable[[], dict[str, Any]]
BrowserOpener = Callable[[str], bool]


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
        "<div class=\"model-selector-option\" data-kora-model-option=\"true\" "
        "data-kora-model-option-state=\"catalog-estimate-only\" aria-selected=\"false\" tabindex=\"0\">"
        f"<strong>{html.escape(str(model.get('display_name', 'Unknown model')), quote=True)}</strong>"
        "<span>Catalog estimate option; not installed or executed by selection.</span>"
        f"<span>{html.escape(str(model.get('model_id', 'unknown')), quote=True)}</span>"
        f"<span>{html.escape(str(model.get('candidate_type', 'needs_validation')), quote=True)}</span>"
        f"<span>{html.escape(str(model.get('estimated_memory_gb', 'unknown')), quote=True)} GB estimate</span>"
        f"<span>Installed: {html.escape('true' if model.get('installed_locally') is True else 'false', quote=True)}</span>"
        "</div>"
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
        "<div class=\"card\">"
        "<h3>Run Local Harness</h3>"
        f"<p><code>{html.escape(str(request.get('request_id', 'unknown')), quote=True)}</code></p>"
        f"<p>{html.escape(str(request.get('input_text', 'Approved local sample request.')), quote=True)}</p>"
        f"<p>Family: {html.escape(str(request.get('task_family', 'unknown')), quote=True)}</p>"
        f"<p>Route: {html.escape(str(request.get('expected_route_class', 'unknown')), quote=True)}</p>"
        f"<p>Model-needed boundary: {html.escape(str(request.get('expected_model_needed', False)), quote=True)}</p>"
        "<p><span class=\"badge\">Approved deterministic sample requests only</span></p>"
        "</div>"
        for request in local_harness_requests
    )
    selector_preview_request = local_harness_requests[0] if local_harness_requests else {}
    selector_preview_id = html.escape(str(selector_preview_request.get("request_id", "unknown")), quote=True)
    selector_preview_text = html.escape(str(selector_preview_request.get("input_text", "No approved request selected.")), quote=True)
    selector_preview_route = html.escape(str(selector_preview_request.get("expected_route_class", "unknown")), quote=True)
    selector_preview_model_needed = html.escape(str(selector_preview_request.get("expected_model_needed", "unknown")), quote=True)
    local_harness_requests_json = json.dumps(local_harness_requests, sort_keys=True).replace("</", "<\\/")
    local_harness_selector_items = "".join(
        "<div class=\"card\">"
        "<h3>Selector option</h3>"
        f"<button class=\"request-option\" type=\"button\" data-kora-keyboard-selectable-request=\"true\" aria-pressed=\"false\" aria-label=\"Select approved local harness request {html.escape(str(request.get('request_id', 'unknown')), quote=True)}\" data-kora-request-id=\"{html.escape(str(request.get('request_id', 'unknown')), quote=True)}\">"
        f"{html.escape(str(request.get('request_id', 'unknown')), quote=True)}"
        "</button>"
        f"<p>{html.escape(str(request.get('input_text', 'Approved local sample request.')), quote=True)}</p>"
        f"<p>Route class: {html.escape(str(request.get('expected_route_class', 'unknown')), quote=True)}</p>"
        f"<p>Model-needed boundary: {html.escape(str(request.get('expected_model_needed', False)), quote=True)}</p>"
        "<p><span class=\"badge\">Approved local harness requests only</span></p>"
        "</div>"
        for request in local_harness_requests
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
          <div class=\"shell-boundary-strip\" data-kora-component=\"boundary-strip\" data-kora-shell-local-only-boundary=\"v1.0\" data-kora-shell-boundary-coverage=\"provider,cloud,download,model-execution,report-export\">
            <div class=\"shell-boundary-pills\">
              <span class=\"shell-pill cyan\">Local preview only</span>
              <span class=\"shell-pill\">Provider calls disabled</span>
              <span class=\"shell-pill\">Cloud sync disabled</span>
              <span class=\"shell-pill\">Downloads disabled</span>
              <span class=\"shell-pill amber\">Model execution not connected yet</span>
              <span class=\"shell-pill\">Report export disabled</span>
            </div>
            <p>Shell-first boundary: approved local harness requests only. No arbitrary prompt execution, no provider calls, no cloud sync, no downloads, no model execution, and no report file export or writing.</p>
          </div>
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
    legacy_preview_html = """  <details class=\"legacy-preview\" aria-label=\"Detailed local preview compatibility scaffolds\" data-kora-component=\"legacy-compatibility-reference\" data-kora-legacy-preview-mode=\"compatibility-collapsed\" data-kora-legacy-preview-default=\"collapsed\" data-kora-legacy-preview-role=\"developer-compatibility-scaffold\" data-kora-v1-1-legacy-secondary=\"developer-reference-only\" data-kora-v1-1-legacy-first-run-required=\"false\">
    <summary aria-label=\"Open legacy detailed preview compatibility scaffold\">
      <div class=\"legacy-preview-summary\">
        <div><strong>Legacy detailed preview compatibility scaffold</strong><span>Collapsed by default. The final shell and Details drawer above are the primary local preview; this developer reference is not required for first-run understanding.</span></div>
        <span class=\"legacy-preview-summary-badge\">Developer reference only</span>
      </div>
    </summary>
    <p class=\"legacy-preview-summary\" data-kora-v1-1-legacy-boundary=\"secondary-reference-only\">This compatibility scaffold remains local-only and secondary. It does not enable model execution, provider calls, downloads, cloud sync, report export, or report writing.</p>
    <div class=\"legacy-preview-content\">"""
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
  <link rel=\"icon\" href=\"data:,\">
  <style>{render_studio_css().rstrip("\n")}
  </style>
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

    <section aria-label=\"Launch Local-only Status\" style=\"margin-top: 18px;\">
      <h2>Launch / Local-only Status</h2>
      <div class=\"grid\">
        <div class=\"status-card card\"><h3>Server</h3><p class=\"status-value\">Server: local</p><p>Bound to the local Studio skeleton.</p></div>
        <div class=\"status-card card\"><h3>Provider Calls</h3><p class=\"status-value disabled\">Provider calls: disabled</p><p>No remote provider requests are made.</p></div>
        <div class=\"status-card card\"><h3>Cloud Sync</h3><p class=\"status-value disabled\">Cloud sync: disabled</p><p>No cloud sync is performed.</p></div>
        <div class=\"status-card card\"><h3>Model Runtime</h3><p class=\"status-value disabled\">Model/runtime integration: not connected</p><p>Future runtime work must distinguish physically runnable local models from workflow-usable models.</p></div>
        <div class=\"status-card card\"><h3>Browser Launch</h3><p class=\"status-value\">Browser launch: available</p><p>The CLI opens the local page by default; use <code>--no-browser</code> to suppress it.</p></div>
        <div class=\"status-card card\"><h3>Ollama</h3><p class=\"status-value disabled\">Ollama integration: not connected</p><p>No Ollama model calls happen here.</p></div>
      </div>
      <div class=\"card\" style=\"margin-top: 16px;\"><h3>First-run order</h3><ol>{section_order_items}</ol></div>
    </section>

    <div class=\"section-stack\">
      <section>
        <h2>Your Computer</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>System Profile</h3><p>OS: {os_name}</p><p>Machine: {machine}</p><p>Memory: {memory_text} ({memory_status})</p></div>
          <div class=\"card\"><h3>Local Runtime Detection</h3><p>Ollama: {ollama_status}</p><p>llama.cpp: {llama_cpp_status}</p><p>No runtime APIs are called by this preview.</p></div>
        </div>
      </section>

      <section>
        <h2>Model Capability Estimate</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Estimated local model tier</h3><p>{recommended_tier}</p><p>{physical_notes}</p></div>
          <div class=\"card\"><h3>Workflow feasibility</h3><p>{workflow_notes}</p><p>{claim_boundary}</p></div>
        </div>
      </section>

      <section>
        <h2>Runtime Status</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Runtime detected</h3><p>{runtime_name}: {runtime_detected}</p><p>Runtime executable detection is local-only.</p></div>
          <div class=\"card\"><h3>Service reachability</h3><p>Runtime reachable: {service_status}</p><p>Service URL: {service_url}</p><p>Service reachability is a localhost-only check.</p><p>No model execution occurs during this check.</p><p>{service_boundary}</p></div>
          <div class=\"card\"><h3>Installed model detection</h3><p>Detection enabled: {installed_enabled}</p><p>Detection method: {installed_method}</p><p>Installed model detection is not connected yet.</p></div>
        </div>
      </section>

      <section>
        <h2>Catalog vs Installed</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Catalog examples</h3><p>{catalog_status}</p><p>Catalog examples are curated examples, not installed models.</p></div>
          <div class=\"card\"><h3>Physically runnable local candidates</h3><p>{local_candidate_name}</p><p>{local_candidate_note}</p></div>
          <div class=\"card\"><h3>Larger-model workflow candidates</h3><p>{workflow_candidate_name}</p><p>{workflow_candidate_note}</p></div>
          <div class=\"card\"><h3>Installed locally</h3><p>Installed model detection: {installed_status}</p><p>Installed count: {installed_count}</p><p>No private model directories are scanned.</p><p>No runtime model list command is called by default.</p></div>
          <div class=\"card\"><h3>Catalog boundary</h3><p>{catalog_boundary}</p><p>{installed_boundary}</p></div>
        </div>
      </section>

      <section>
        <h2>Setup Guidance</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Guidance status</h3><p>{setup_guidance_status}</p><p>Disabled actions point to guidance, not to an active installer.</p><p><code>{setup_guidance_url}</code></p></div>
          <div class=\"card\"><h3>Setup boundary</h3><p>No model is downloaded.</p><p>No model is executed.</p><p>No provider call is made.</p><p>Provider/cloud routes are disabled by default.</p></div>
          <div class=\"card\"><h3>Runtime readiness</h3><p>Runtime executable detection is not model execution readiness.</p><p>Catalog examples are not installed models.</p><p>{setup_guidance_boundary}</p></div>
        </div>
      </section>

      <section>
        <h2>Disabled Download/Run Actions</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Download action</h3><p><span class=\"badge\">{local_download_label}</span></p><p>{local_download_reason}</p><p>Download remains disabled until explicitly connected.</p></div>
          <div class=\"card\"><h3>Run action</h3><p><span class=\"badge\">{local_run_label}</span></p><p>{local_run_reason}</p><p>Run remains disabled until explicitly connected.</p></div>
          <div class=\"card\"><h3>Action boundary</h3><p>Download and run actions remain disabled.</p><p>{local_action_boundary}</p><p>No install, download, or model execution action is active in this preview.</p></div>
        </div>
      </section>

      <section>
        <h2>KORA Boost Boundary</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Standard Mode</h3><p>Standard Mode sends every step to the model.</p><p>In this preview, model execution is not connected.</p></div>
          <div class=\"card\"><h3>KORA Boost</h3><p>KORA Boost routes deterministic and structured tasks to CPU/local fast paths first.</p><p>Larger-model workflows may become more practical when deterministic work avoids the model path.</p></div>
          <div class=\"card\"><h3>Boundary</h3><p>KORA does not remove model memory requirements.</p><p>Provider/cloud routes are disabled by default.</p></div>
        </div>
      </section>

      <section>
        <h2>Local Harness Preview</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Harness status</h3><p>{local_harness_status_text}</p><p>Event source: {local_harness_event_source}</p><p>Run trigger: {local_harness_run_trigger}</p><p>Available sample requests: {local_harness_request_count}</p></div>
          <div class=\"card\"><h3>Sample request</h3><p><code>{sample_request_id}</code></p><p>{sample_input}</p><p>Family: {sample_family}</p><p>Expected route: {sample_route}</p><p>Validation: {sample_validation}</p><p>Model needed: {sample_model_needed}</p></div>
          <div class=\"card\"><h3>Boundary</h3><p>{local_harness_boundary}</p><p>Model-needed boundaries do not execute models in this milestone.</p><p>No provider call, download, or cloud sync is connected.</p></div>
        </div>
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\" data-kora-component=\"approved-request-selector\"><h3>Approved Request Selector</h3><p>Interactive approved request selector.</p><p>Approved local harness requests only.</p><p>Approved request only.</p><p>No arbitrary prompt execution.</p><p>No model execution.</p><p>No provider calls.</p><p>No downloads.</p><p>Local deterministic harness data only.</p></div>
          <div class=\"card\"><h3>Selected request preview</h3><p><code id=\"kora-selected-request-id\">{selector_preview_id}</code></p><p id=\"kora-selected-request-text\">{selector_preview_text}</p><p>Route class: <span id=\"kora-selected-request-route\">{selector_preview_route}</span></p><p>Model-needed boundary: <span id=\"kora-selected-request-model-needed\">{selector_preview_model_needed}</span></p><p>Selector state is browser-local in-memory page state only.</p></div>
          <div class=\"card\"><h3>Run Local Harness</h3><p><span class=\"badge\">Approved request only</span></p><button class=\"action-button\" type=\"button\" id=\"kora-run-local-harness-button\">Run Local Harness</button><p>Calls <code>POST /api/harness/run</code> with the selected approved <code>request_id</code> only.</p><p>No arbitrary prompt text is sent.</p></div>
        </div>
        <div class=\"grid\" style=\"margin-top: 16px;\">{local_harness_selector_items}</div>
{selected_run_state_html}
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\" data-kora-component=\"retry-error-state\"><h3>Selected Run Error State</h3><p id=\"kora-run-error-state\">No selected-run error.</p><p>Retry uses the last approved request only.</p><p>No model execution was attempted.</p><p>Provider calls remain disabled.</p><p>No downloads are connected.</p></div>
          <div class=\"card\"><h3>Retry Last Approved Request</h3><p>Last approved request: <code id=\"kora-last-approved-request-id\">{selector_preview_id}</code></p><p>Retry available: <span id=\"kora-retry-available\">false</span></p><button class=\"action-button\" type=\"button\" id=\"kora-retry-last-approved-request-button\" disabled>Retry Last Approved Request</button><p>Retry calls only <code>POST /api/harness/run</code> with the last approved <code>request_id</code>.</p><p>No arbitrary prompt execution.</p></div>
        </div>
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\" data-kora-component=\"run-history\"><h3>Local Run History</h3><p>Browser-local run history.</p><p>Page-memory only.</p><p>Clears on refresh.</p><p>Active selected run: <code id=\"kora-active-history-run-id\">none</code></p><p>History cards show compact counters from generated harness output only.</p><p>Local deterministic harness output only.</p><p>No model execution. No provider calls. No downloads.</p><p>History count: <span id=\"kora-run-history-count\">0</span></p><p id=\"kora-run-history-status\">Run an approved local harness request to add browser-local history.</p></div>
          <div class=\"card\"><h3>Clear Local Run History</h3><button class=\"action-button\" type=\"button\" id=\"kora-clear-run-history-button\">Clear Local Run History</button><p>Clears browser-local preview state only.</p><p>Resets selected-run UI, selected events, selected counters, selected comparison, selected report metadata, and page-memory history.</p><p>Does not remove server run records, reports, files, backend records, or generated harness endpoints.</p><p>No persistence, no cloud sync, no file export, no file writing, and no backend delete call.</p></div>
        </div>
        <div class=\"grid\" id=\"kora-local-run-history\" aria-live=\"polite\"></div>
{selected_run_detail_panels_html}
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\"><h3>Run Local Harness action state</h3><p><span class=\"badge\">Run Local Harness</span></p><p>The browser button calls only the local harness run endpoint for an approved request id.</p><p>Use <code>POST /api/harness/run</code> with an approved <code>request_id</code>.</p><p>Generated harness events only.</p></div>
          <div class=\"card\"><h3>Trigger boundary</h3><p>Approved deterministic sample requests only.</p><p>No arbitrary prompt execution.</p><p>No model execution.</p><p>No provider calls.</p><p>No downloads.</p><p>This is local preview/demo data, not production evidence.</p></div>
          <div class=\"card\"><h3>Result surfaces</h3><p><code>GET /api/harness/run/&lt;run_id&gt;</code></p><p><code>GET /api/harness/events?run_id=&lt;id&gt;</code></p><p><code>GET /api/harness/sse?run_id=&lt;id&gt;</code></p><p>Model-needed boundary returns <code>execution_not_connected</code>.</p></div>
        </div>
        <div class=\"grid\" style=\"margin-top: 16px;\">{local_harness_trigger_items}</div>
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\"><h3>Available local deterministic sample requests</h3><ul>{local_harness_request_items}</ul></div>
          <div class=\"card\"><h3>Harness event stages</h3><ul>{local_harness_event_items}</ul></div>
        </div>
        <div class=\"card\" style=\"margin-top: 16px;\"><h3>Generated Event Timeline</h3><p>Generated local harness events only. Not model token streaming. No model execution. No provider output.</p></div>
        <div class=\"grid\">{local_harness_timeline_items}</div>
        <div class=\"card\" style=\"margin-top: 16px;\"><h3>Generated Counters</h3><p>Generated counters come from local deterministic harness output only. No cost or energy conversion is performed.</p></div>
        <div class=\"grid\">{local_harness_counter_items}</div>
      </section>

      <section>
        <h2>Execution Viewer</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Fixture status</h3><p>{execution_status}</p><p>Fixture/mock events only.</p><p>No real model execution.</p><p>No provider calls.</p><p>No model downloads.</p></div>
          <div class=\"card\"><h3>Event schema</h3><p>Schema fields: {execution_schema_count}</p><p>Fixture events: {execution_event_count}</p><p>{execution_boundary}</p></div>
          <div class=\"card\"><h3>Fixture stages</h3><ul>{execution_event_items}</ul></div>
        </div>
        <div class=\"workflow\" style=\"margin-top: 16px;\">
          <div class=\"step\"><p class=\"step-number\">01</p><h3>Request received</h3><p>Local fixture request is received by the Execution Viewer scaffold.</p></div>
          <div class=\"step\"><p class=\"step-number\">02</p><h3>Deterministic route check</h3><p>Fixture route selection checks deterministic code before the model path.</p></div>
          <div class=\"step\"><p class=\"step-number\">03</p><h3>Structured lookup and validation pass</h3><p>Fixture structured lookup succeeds and validation passes.</p></div>
          <div class=\"step\"><p class=\"step-number\">04</p><h3>Model fallback skipped / Final counters</h3><p>Fixture counters show the model path skipped after validation. No runtime execution occurs on this page.</p></div>
        </div>
      </section>

      <section>
        <h2>Standard Mode vs KORA Boost</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Comparison status</h3><p>{standard_vs_kora_status}</p><p>Local deterministic harness comparison.</p><p>No model execution occurs.</p></div>
          <div class=\"card\"><h3>Standard Mode</h3><p>{standard_route_summary}</p><p>Model call counted in fixture baseline: 1</p></div>
          <div class=\"card\"><h3>KORA Boost</h3><p>{kora_route_summary}</p><p>Model call counted in fixture KORA path: 0</p></div>
          <div class=\"card\"><h3>Local Harness Comparison boundary</h3><p>{standard_vs_kora_boundary}</p><p>Comparison is generated from local deterministic harness output.</p><p>This is not production cost evidence.</p><p>This does not execute a model.</p><p>No cost or energy claim is made.</p></div>
        </div>
        <div class=\"grid\">{standard_vs_kora_metric_items}</div>
      </section>

      <section>
        <h2>Report Viewer Placeholder</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Local Harness Report</h3><p>{report_viewer_status}</p><p>{report_title}</p><p>Source: {report_source}</p><p>Local deterministic harness output only.</p></div>
          <div class=\"card\"><h3>Report Metadata Preview</h3><p>Report metadata preview only.</p><p>Run: <code>{report_sample_run_id}</code></p><p>Request: <code>{report_sample_request_id}</code></p><p>Event count: {report_event_count}</p><p>Comparison summary: {report_comparison_status}</p></div>
          <div class=\"card\"><h3>File export status</h3><p>Export placeholder</p><p>{report_export_status}</p><p><span class=\"badge\">{report_export_label}</span></p><p>File export: {report_file_export_enabled}</p><p>File written: {report_file_written}</p><p>No file export in this preview.</p><p>{report_export_reason}</p><p>{report_export_boundary}</p></div>
          <div class=\"card\"><h3>Report Boundary</h3><p>{report_boundary}</p><p>Not production evidence.</p><p>No model execution.</p><p>No provider calls.</p><p>No cloud sync.</p><p>No new benchmark evidence is created.</p></div>
        </div>
        <div class=\"grid\">
          <div class=\"card\"><h3>Local-only boundary</h3><p>No arbitrary local file scan is performed.</p><p>No cloud upload is connected.</p><p>No provider calls are made.</p><p>Local harness summary only.</p><p>Report source path: <code>{report_path_display}</code></p><p>Fixture metadata path: <code>{report_fixture_path}</code></p></div>
          <div class=\"card\"><h3>Report sections</h3><ul>{report_sections}</ul></div>
          <div class=\"card\"><h3>Boundary warnings</h3><ul>{report_warnings}</ul></div>
        </div>
        <div class=\"grid\">{report_counter_items}</div>
      </section>

      <section>
        <h2>Endpoint Panel</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3><a href=\"/health\">/health</a></h3><p>Returns local health status JSON for the preview server.</p></div>
          <div class=\"card\"><h3><a href=\"/status\">/status</a></h3><p>Returns local preview status, system profile, model capability estimate, KORA Boost copy, docs paths, and fixture paths.</p></div>
          <div class=\"card\"><h3>/api/harness/run</h3><p>POST accepts only approved local deterministic sample request IDs and returns generated local harness events. Arbitrary prompt execution is not connected.</p></div>
          <div class=\"card\"><h3>/api/harness/run/&lt;run_id&gt;</h3><p>GET returns an in-memory local harness run record if it exists. No persistence, provider call, download, or model execution is connected.</p></div>
          <div class=\"card\"><h3>/api/harness/events?run_id=&lt;id&gt;</h3><p>GET returns generated harness events for an existing local run. This is not SSE, not model token streaming, and not model output.</p></div>
          <div class=\"card\"><h3>/api/harness/sse?run_id=&lt;id&gt;</h3><p>GET streams generated harness events as Server-Sent Events. It streams no model tokens, provider output, or model output.</p></div>
        </div>
      </section>

      <section>
        <h2>Limitations Panel</h2>
        <ul>
          <li>No full frontend yet</li>
          <li>No provider calls</li>
          <li>No model/runtime integration yet</li>
          <li>Browser launch is local-only and can be disabled with <code>--no-browser</code></li>
          <li>No Ollama integration</li>
          <li>No production/API-cost/energy claims</li>
          <li>No claim that KORA removes model memory requirements</li>
          <li>External/provider/distributed routes disabled by default</li>
        </ul>
      </section>

      <section>
        <h2>Local References</h2>
        <ul>
          <li><code>{docs_path}</code></li>
          <li><code>{fixtures_path}</code></li>
        </ul>
      </section>
    </div>

    <p class=\"footer\">Local-only skeleton. Claim-safe AI Task Execution Router preview; KORA does not make large models smaller or remove memory requirements.</p>
    </div>
  </details>
  <script type=\"application/json\" id=\"kora-approved-requests-data\">{local_harness_requests_json}</script>
  <script>{render_studio_javascript().rstrip("\n")}
  </script>
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
