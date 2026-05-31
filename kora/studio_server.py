"""Local-only KORA Studio server skeleton."""

from __future__ import annotations

import html
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse

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

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>KORA Studio</title>
  <link rel=\"icon\" href=\"data:,\">
  <style>
    :root {{
      color-scheme: dark;
      --bg: #071014;
      --panel: #0d1b22;
      --panel-2: #10242d;
      --panel-3: #0a171d;
      --text: #edf7fa;
      --muted: #9fb3bd;
      --cyan: #32d1e6;
      --amber: #f0b44c;
      --green: #57d68d;
      --line: #24424d;
    }}
    * {{ box-sizing: border-box; }}
    html {{
      overflow-x: hidden;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
      overflow-x: hidden;
    }}
    main {{
      width: min(1120px, calc(100% - 40px));
      margin: 0 auto;
      padding: 42px 0 34px;
    }}
    header {{
      border: 1px solid var(--line);
      background: linear-gradient(180deg, var(--panel), var(--panel-2));
      border-radius: 8px;
      padding: 28px;
    }}
    .topline {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 22px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      border: 1px solid var(--green);
      color: var(--green);
      border-radius: 999px;
      padding: 6px 12px;
      font-size: 13px;
      font-weight: 700;
      white-space: nowrap;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(34px, 6vw, 58px);
      letter-spacing: 0;
      line-height: 1.05;
    }}
    h2 {{
      margin: 0 0 14px;
      font-size: 20px;
      letter-spacing: 0;
    }}
    h3 {{
      margin: 0 0 6px;
      font-size: 15px;
      letter-spacing: 0;
    }}
    p {{ margin: 0; }}
    a {{ color: var(--cyan); }}
    code {{
      color: var(--amber);
      background: #071014;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 2px 6px;
      overflow-wrap: anywhere;
    }}
    .subtitle {{
      color: var(--muted);
      font-size: 17px;
      max-width: 760px;
    }}
    .boost {{
      color: var(--cyan);
      font-size: 24px;
      font-weight: 800;
      margin-top: 18px;
    }}
    .technical {{
      color: var(--muted);
      max-width: 820px;
      margin-top: 10px;
      font-size: 16px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-top: 18px;
    }}
    section, .card {{
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 8px;
      padding: 18px;
    }}
    .status-card {{
      min-height: 118px;
      background: var(--panel-3);
    }}
    .status-card p {{ color: var(--muted); }}
    .status-value {{
      color: var(--green);
      font-weight: 800;
      margin-top: 8px;
    }}
    .status-value.disabled {{ color: var(--amber); }}
    button {{
      font: inherit;
    }}
    .request-option, .action-button {{
      width: 100%;
      border: 1px solid var(--cyan);
      background: #071014;
      color: var(--text);
      border-radius: 8px;
      padding: 10px 12px;
      cursor: pointer;
      text-align: left;
      overflow-wrap: anywhere;
    }}
    .request-option:hover, .request-option[aria-pressed="true"], .action-button:hover {{
      border-color: var(--green);
      color: var(--green);
    }}
    .request-option:focus-visible,
    .action-button:focus-visible,
    .composer-submit:focus-visible {{
      outline: 2px solid var(--cyan);
      outline-offset: 3px;
    }}
    .action-button {{
      margin-top: 10px;
      text-align: center;
      font-weight: 800;
    }}
    .action-button:disabled {{
      border-color: var(--line);
      color: var(--muted);
      cursor: wait;
    }}
    .run-state {{
      border: 1px solid var(--line);
      background: var(--panel-3);
      border-radius: 8px;
      padding: 14px;
      margin-top: 10px;
    }}
    .workflow {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }}
    .step {{
      border: 1px solid var(--line);
      background: var(--panel-3);
      border-radius: 8px;
      padding: 14px;
      min-height: 130px;
    }}
    .step-number {{
      color: var(--cyan);
      font-size: 13px;
      font-weight: 800;
      margin-bottom: 8px;
    }}
    ul {{
      margin: 0;
      padding-left: 20px;
      color: var(--muted);
    }}
    li + li {{ margin-top: 8px; }}
    .section-stack {{
      display: grid;
      gap: 18px;
      margin-top: 18px;
    }}
    .footer {{
      color: var(--muted);
      border-top: 1px solid var(--line);
      margin-top: 22px;
      padding-top: 16px;
      font-size: 14px;
    }}
    .studio-shell {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: 260px minmax(0, 1fr);
      background: #080b10;
      border-bottom: 1px solid #1d2732;
      overflow: hidden;
    }}
    .studio-left-rail {{
      border-right: 1px solid #1d2732;
      background: #0c1016;
      padding: 26px 24px;
      display: flex;
      flex-direction: column;
      gap: 22px;
    }}
    .rail-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
    }}
    .rail-brand,
    .rail-action,
    .rail-item,
    .rail-footer {{
      display: flex;
      align-items: center;
      gap: 12px;
      color: var(--muted);
      font-size: 15px;
    }}
    .rail-brand {{
      color: var(--text);
      font-weight: 700;
    }}
    .rail-icon {{
      width: 18px;
      height: 18px;
      border: 1px solid #5a6678;
      border-radius: 5px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: var(--muted);
      flex: 0 0 auto;
    }}
    .rail-section-title {{
      color: #6d7788;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin: 8px 0 10px;
    }}
    .rail-list {{
      display: grid;
      gap: 14px;
    }}
    .rail-footer {{
      margin-top: auto;
      border-top: 1px solid #1d2732;
      padding-top: 18px;
      align-items: flex-start;
    }}
    .rail-footer strong {{
      color: var(--text);
      display: block;
      font-size: 14px;
    }}
    .rail-footer span {{
      color: #6d7788;
      display: block;
      font-size: 13px;
      margin-top: 2px;
    }}
    .studio-workspace {{
      min-width: 0;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }}
    .studio-topbar {{
      height: 82px;
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      gap: 18px;
      padding: 20px 36px;
    }}
    .rail-shell-button {{
      justify-self: start;
      visibility: hidden;
      border: 1px solid #334052;
      background: #151a22;
      color: var(--muted);
      border-radius: 999px;
      padding: 10px 16px;
      font-weight: 700;
    }}
    .rail-shell-button[aria-expanded="true"] {{
      border-color: var(--cyan);
      color: var(--text);
    }}
    .rail-close-button {{
      visibility: hidden;
      border: 1px solid #334052;
      background: #151a22;
      color: var(--muted);
      border-radius: 999px;
      width: 34px;
      height: 34px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      line-height: 1;
      flex: 0 0 auto;
    }}
    .rail-shell-button:focus-visible,
    .rail-close-button:focus-visible {{
      outline: 2px solid var(--cyan);
      outline-offset: 3px;
    }}
    .model-selector-shell {{
      justify-self: center;
      min-width: min(430px, 54vw);
      border: 1px solid #334052;
      background: #151a22;
      color: var(--muted);
      border-radius: 999px;
      padding: 0;
      font-size: 15px;
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
      position: relative;
    }}
    .model-selector-shell:focus-within {{
      border-color: var(--cyan);
      box-shadow: 0 0 0 3px rgba(117, 190, 255, 0.12), inset 0 1px 0 rgba(255,255,255,0.02);
    }}
    .model-selector-shell summary {{
      list-style: none;
      cursor: default;
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: center;
      gap: 10px;
      padding: 10px 18px;
    }}
    .model-selector-shell summary:focus-visible,
    .model-selector-option:focus-visible {{
      outline: 2px solid var(--cyan);
      outline-offset: 3px;
    }}
    .model-selector-shell summary::-webkit-details-marker {{
      display: none;
    }}
    .model-selector-title {{
      color: var(--text);
      display: block;
      font-size: 14px;
      font-weight: 700;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .model-selector-subtitle {{
      color: var(--muted);
      display: block;
      font-size: 12px;
      margin-top: 2px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .model-selector-chevron {{
      color: var(--muted);
      font-size: 16px;
    }}
    .model-selector-selected-label {{
      color: var(--cyan);
      display: block;
      font-size: 11px;
      font-weight: 800;
      margin-top: 4px;
      text-transform: uppercase;
    }}
    .model-selector-menu {{
      position: absolute;
      top: calc(100% + 10px);
      left: 0;
      right: 0;
      z-index: 4;
      border: 1px solid #334052;
      background: #11161e;
      border-radius: 18px;
      padding: 12px;
      box-shadow: 0 20px 55px rgba(0,0,0,0.45);
      max-height: min(560px, calc(100vh - 130px));
      overflow-y: auto;
    }}
    .model-selector-option {{
      border: 1px solid #293447;
      border-radius: 12px;
      padding: 10px 12px;
      margin-top: 8px;
      background: #171d27;
    }}
    .model-selector-option[aria-selected="true"] {{
      border-color: var(--cyan);
      background: #14202a;
      box-shadow: inset 3px 0 0 var(--cyan);
    }}
    .model-selector-option:first-child {{
      margin-top: 0;
    }}
    .model-selector-option span {{
      color: var(--muted);
      display: block;
      font-size: 12px;
      margin-top: 3px;
    }}
    .model-selector-boundary {{
      border-top: 1px solid #293447;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
      margin-top: 10px;
      padding-top: 10px;
    }}
    .details-shell-button {{
      justify-self: end;
      border: 1px solid #334052;
      background: #151a22;
      color: var(--muted);
      border-radius: 999px;
      padding: 10px 22px;
      font-weight: 700;
    }}
    .details-shell-button[aria-expanded="true"] {{
      border-color: var(--cyan);
      color: var(--text);
    }}
    .details-shell-button:focus-visible,
    .drawer-close-button:focus-visible {{
      outline: 2px solid var(--cyan);
      outline-offset: 3px;
    }}
    .composer-stage {{
      flex: 1;
      min-height: 620px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 36px;
    }}
    .composer-panel {{
      width: min(720px, 100%);
      text-align: center;
    }}
    .composer-panel h1 {{
      font-size: 56px;
      line-height: 1.12;
      margin-bottom: 18px;
    }}
    .composer-panel .subtitle {{
      margin: 0 auto;
      max-width: 560px;
    }}
    .composer-box {{
      margin: 64px auto 24px;
      border: 1px solid #334052;
      background: #171c25;
      border-radius: 30px;
      min-height: 92px;
      padding: 26px 76px 24px 30px;
      text-align: left;
      color: var(--muted);
      position: relative;
    }}
    .composer-submit {{
      position: absolute;
      right: 24px;
      top: 24px;
      width: 44px;
      height: 44px;
      border-radius: 999px;
      border: 0;
      background: #252d3a;
      color: var(--muted);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }}
    .composer-action-note {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
      margin: -8px auto 20px;
      max-width: 560px;
    }}
    .composer-action-note code {{
      color: var(--text);
      font-size: 12px;
    }}
    .composer-run-summary {{
      border: 1px solid #293447;
      background: rgba(17, 22, 30, 0.68);
      border-radius: 18px;
      color: var(--muted);
      display: grid;
      gap: 6px;
      margin: 0 auto 22px;
      max-width: 560px;
      padding: 12px 16px;
      text-align: left;
    }}
    .composer-run-summary strong {{
      color: var(--text);
    }}
    .composer-run-summary span {{
      color: var(--text);
    }}
    .shell-selected-run-strip {{
      border: 1px solid #293447;
      background: rgba(12, 16, 22, 0.64);
      border-radius: 16px;
      display: grid;
      gap: 8px;
      margin: -10px auto 20px;
      max-width: 620px;
      padding: 12px 14px;
      text-align: left;
    }}
    .shell-selected-run-strip h2 {{
      color: var(--text);
      font-size: 14px;
      margin: 0;
    }}
    .shell-selected-run-grid {{
      display: grid;
      gap: 8px;
      grid-template-columns: repeat(4, minmax(0, 1fr));
    }}
    .shell-selected-run-grid span {{
      border: 1px solid #293447;
      border-radius: 12px;
      color: var(--muted);
      font-size: 12px;
      padding: 8px 10px;
    }}
    .shell-selected-run-strip p {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
      margin: 0;
    }}
    .shell-boundary-pills {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
    }}
    .shell-boundary-strip {{
      border: 1px solid #293447;
      background: rgba(12, 16, 22, 0.72);
      border-radius: 16px;
      display: grid;
      gap: 10px;
      margin: 0 auto;
      max-width: 620px;
      padding: 12px 14px;
    }}
    .shell-boundary-strip p {{
      color: var(--muted);
      font-size: 12px;
      line-height: 1.5;
      margin: 0;
    }}
    .shell-pill {{
      border: 1px solid #293447;
      color: var(--muted);
      background: rgba(17, 22, 30, 0.72);
      border-radius: 999px;
      padding: 8px 14px;
      font-size: 13px;
    }}
    .shell-pill.cyan::before,
    .shell-pill.amber::before {{
      content: "";
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      margin-right: 8px;
      vertical-align: middle;
      background: var(--cyan);
    }}
    .shell-pill.amber::before {{
      background: var(--amber);
    }}
    .details-drawer-shell {{
      position: absolute;
      top: 88px;
      right: 24px;
      width: 380px;
      max-height: calc(100vh - 120px);
      overflow-y: auto;
      border: 1px solid var(--cyan);
      background: #11161e;
      border-radius: 20px;
      padding: 22px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.42);
      transform: translateX(calc(100% + 48px));
      opacity: 0.02;
      pointer-events: none;
      transition: transform 180ms ease, opacity 180ms ease;
      z-index: 5;
    }}
    .studio-workspace[data-kora-drawer-open="true"] .details-drawer-shell {{
      transform: translateX(0);
      opacity: 1;
      pointer-events: auto;
    }}
    .drawer-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 12px;
    }}
    .drawer-close-button {{
      border: 1px solid #334052;
      background: #151a22;
      color: var(--muted);
      border-radius: 999px;
      width: 34px;
      height: 34px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      line-height: 1;
    }}
    .details-drawer-shell h2 {{
      margin-bottom: 4px;
    }}
    .drawer-section-chip {{
      border: 1px solid #303a4a;
      background: #1a202a;
      border-radius: 10px;
      padding: 10px 12px;
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
    }}
    .drawer-section-block {{
      border: 1px solid #303a4a;
      background: #1a202a;
      border-radius: 12px;
      padding: 12px;
      margin-top: 12px;
      color: var(--muted);
      font-size: 13px;
    }}
    .drawer-section-block h3 {{
      color: var(--text);
      margin-bottom: 8px;
      font-size: 14px;
    }}
    .drawer-section-block p {{
      margin-top: 6px;
    }}
    .drawer-section-block code {{
      font-size: 12px;
    }}
    .drawer-boundary {{
      border-color: #784634;
      background: #1a1210;
    }}
    .legacy-preview {{
      width: min(1120px, calc(100% - 40px));
      margin: 0 auto;
      padding: 42px 0 34px;
    }}
    .legacy-preview summary {{
      border: 1px solid #293447;
      background: rgba(12, 16, 22, 0.86);
      border-radius: 18px;
      color: var(--text);
      cursor: pointer;
      list-style: none;
      padding: 18px 20px;
    }}
    .legacy-preview summary::-webkit-details-marker {{
      display: none;
    }}
    .legacy-preview-summary {{
      align-items: flex-start;
      display: flex;
      justify-content: space-between;
      gap: 18px;
    }}
    .legacy-preview-summary strong {{
      display: block;
      margin-bottom: 4px;
    }}
    .legacy-preview-summary span {{
      color: var(--muted);
      display: block;
      font-size: 13px;
      line-height: 1.5;
    }}
    .legacy-preview-summary-badge {{
      border: 1px solid #293447;
      border-radius: 999px;
      color: var(--muted);
      flex: 0 0 auto;
      font-size: 12px;
      padding: 6px 10px;
    }}
    .legacy-preview-content {{
      padding-top: 22px;
    }}
    @media (max-width: 760px) {{
      main {{ width: min(100% - 24px, 1120px); padding-top: 24px; }}
      .studio-shell {{ grid-template-columns: 1fr; }}
      .studio-left-rail {{
        position: absolute;
        z-index: 3;
        width: min(76vw, 280px);
        min-height: 100vh;
        transform: translateX(-100%);
        opacity: 0.16;
        pointer-events: none;
        transition: transform 180ms ease, opacity 180ms ease;
      }}
      .studio-shell[data-kora-rail-open="true"] .studio-left-rail {{
        transform: translateX(0);
        opacity: 1;
        pointer-events: auto;
      }}
      .studio-topbar {{
        grid-template-columns: auto minmax(0, 1fr) auto;
        gap: 8px;
        height: auto;
        min-height: 68px;
        padding: 14px 12px;
      }}
      .rail-shell-button {{
        visibility: visible;
        padding: 9px 12px;
        font-size: 12px;
      }}
      .rail-close-button {{
        visibility: visible;
      }}
      .model-selector-shell {{
        min-width: 0;
        width: 100%;
        font-size: 13px;
      }}
      .model-selector-shell summary {{
        padding: 9px 12px;
      }}
      .model-selector-title {{
        font-size: 12px;
      }}
      .model-selector-subtitle {{
        font-size: 11px;
      }}
      .model-selector-menu {{
        position: fixed;
        top: 72px;
        left: 12px;
        right: 12px;
        max-height: min(66vh, 460px);
      }}
      .details-shell-button {{
        padding: 9px 12px;
        font-size: 12px;
      }}
      .composer-stage {{
        min-height: calc(100vh - 68px);
        padding: 20px 18px;
      }}
      .composer-panel h1 {{
        font-size: 36px;
        line-height: 1.15;
      }}
      .composer-box {{
        border-radius: 24px;
        margin-top: 36px;
        min-height: 84px;
        padding: 22px 66px 22px 22px;
      }}
      .composer-submit {{
        right: 18px;
        top: 20px;
      }}
      .composer-run-summary {{
        font-size: 12px;
      }}
      .shell-selected-run-grid {{
        grid-template-columns: 1fr 1fr;
      }}
      .details-drawer-shell {{
        position: fixed;
        top: 72px;
        right: 12px;
        width: min(88vw, 380px);
        max-height: calc(100vh - 96px);
        transform: translateX(calc(100% + 24px));
      }}
      .shell-pill {{
        max-width: 100%;
        overflow-wrap: anywhere;
      }}
      header {{ padding: 20px; }}
      .topline {{ align-items: flex-start; flex-direction: column; }}
      .workflow {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class=\"studio-shell\" data-kora-component=\"shell-layout\" data-kora-final-ui-shell=\"true\" data-kora-v1-preview-readiness=\"shell-first-boundary-consolidation\" data-kora-v1-shell-local-only-status=\"visible\" data-kora-v1-1-shell-only-hardening=\"active\" data-kora-v1-1-shell-only-coverage=\"boundaries,drawer-diagnostics,selected-run,legacy-secondary\" data-kora-responsive-shell=\"mobile-overlay-ready\" data-kora-mobile-visual-qa=\"v0.9\" data-kora-mobile-breakpoint=\"max-width-760\" data-kora-mobile-qa-surfaces=\"left-rail,model-selector,composer,right-drawer,boundary-pills\" data-kora-mobile-no-overlap-contract=\"true\" data-kora-keyboard-focus-pass=\"true\" data-kora-focus-visible-controls=\"shell-and-harness\" data-kora-rail-open=\"false\">
    <aside class=\"studio-left-rail\" id=\"kora-left-rail\" aria-label=\"KORA Studio left mini rail\" data-kora-component=\"left-rail\" data-kora-mobile-rail=\"collapsed-overlay\" data-kora-rail-state=\"closed\" aria-hidden=\"false\" tabindex=\"-1\">
      <div class=\"rail-header\">
        <div class=\"rail-brand\"><span class=\"rail-icon\"></span>KORA Studio</div>
        <button class=\"rail-close-button\" type=\"button\" id=\"kora-left-rail-close\" aria-label=\"Close left rail\" data-kora-rail-close=\"true\">x</button>
      </div>
      <div class=\"rail-list\">
        <div class=\"rail-action\"><span class=\"rail-icon\">+</span>New task</div>
        <div class=\"rail-action\"><span class=\"rail-icon\">⌕</span>Search tasks</div>
      </div>
      <div>
        <p class=\"rail-section-title\">Projects</p>
        <div class=\"rail-list\">
          <div class=\"rail-item\"><span class=\"rail-icon\"></span>Local routing demo</div>
          <div class=\"rail-item\"><span class=\"rail-icon\"></span>Catalog fit notes</div>
        </div>
      </div>
      <div>
        <p class=\"rail-section-title\">Today</p>
        <div class=\"rail-list\">
          <div class=\"rail-item\"><span class=\"rail-icon\"></span>Qwen 2.5 fit estimate</div>
          <div class=\"rail-item\"><span class=\"rail-icon\"></span>Deterministic route draft</div>
          <div class=\"rail-item\"><span class=\"rail-icon\"></span>Report metadata preview</div>
        </div>
      </div>
      <div>
        <p class=\"rail-section-title\">Earlier</p>
        <div class=\"rail-list\">
          <div class=\"rail-item\"><span class=\"rail-icon\"></span>Claim boundary checklist</div>
          <div class=\"rail-item\"><span class=\"rail-icon\"></span>Picker taxonomy review</div>
        </div>
      </div>
      <div class=\"rail-footer\"><span class=\"rail-icon\">K</span><div><strong>Local workspace</strong><span>Cloud sync disabled</span></div></div>
    </aside>
    <div class=\"studio-workspace\">
      <div class=\"studio-topbar\" aria-label=\"KORA Studio top bar\">
        <button class=\"rail-shell-button\" type=\"button\" id=\"kora-left-rail-toggle\" aria-label=\"Open left rail\" aria-controls=\"kora-left-rail\" aria-expanded=\"false\" data-kora-rail-toggle=\"true\">Menu</button>
        <details class=\"model-selector-shell\" aria-label=\"Top model selector\" data-kora-component=\"top-model-selector\" data-kora-model-selector=\"local-catalog-scaffold\" data-kora-mobile-selector=\"compact-overlay-menu\" data-kora-model-selection-state=\"catalog-estimate-only\">
          <summary aria-describedby=\"kora-model-selector-boundary\">
            <span><span class=\"model-selector-title\">Search or select open-source LLM</span><span class=\"model-selector-subtitle\">Selected estimate: {local_candidate_name}</span><span class=\"model-selector-selected-label\" data-kora-model-selected-label=\"catalog-estimate-only\">Catalog-only estimate selected</span></span>
            <span class=\"model-selector-chevron\">⌄</span>
          </summary>
          <div class=\"model-selector-menu\" data-kora-model-selector-menu=\"true\">
            <p class=\"model-selector-boundary\" id=\"kora-model-selector-boundary\">Catalog suggestions are local static examples, not installed models. Selecting a model here does not install, download, or execute it.</p>
            <div class=\"model-selector-option\" data-kora-model-selected-estimate=\"true\" data-kora-model-selection-status=\"selected-estimate\" aria-selected=\"true\" tabindex=\"0\"><strong>{local_candidate_name}</strong><span>Selected local fit estimate; catalog-only state.</span><span>{local_candidate_id}</span><span>{local_candidate_type}</span><span>{local_candidate_memory} GB estimate</span><span>Installed: {local_candidate_installed}</span><span>Selection does not install, download, or execute this model.</span></div>
            <p class=\"model-selector-boundary\">Recommended local catalog options shown: {model_selector_count}</p>
            {model_selector_items}
          </div>
        </details>
        <button class=\"details-shell-button\" type=\"button\" id=\"kora-details-drawer-toggle\" aria-label=\"Open details drawer\" aria-controls=\"kora-details-drawer\" aria-expanded=\"false\" data-kora-drawer-toggle=\"true\">Details</button>
      </div>
      <section class=\"composer-stage\" aria-label=\"KORA Studio centered composer\" data-kora-component=\"composer\">
        <div class=\"composer-panel\">
          <h1>What do you want to work on?</h1>
          <p class=\"subtitle\">Choose a local model once. KORA keeps routing details out of the way.</p>
          <div class=\"composer-box\" role=\"group\" aria-label=\"KORA composer scaffold\">
            <span>Ask KORA...</span>
            <button class=\"composer-submit\" type=\"button\" id=\"kora-composer-run-local-harness-button\" aria-label=\"Run approved local harness request\">↑</button>
          </div>
          <p class=\"composer-action-note\">Composer action uses the selected approved local harness request only. No arbitrary prompt execution, no model execution, no provider calls, and no downloads.</p>
          <div class=\"composer-run-summary\" id=\"kora-composer-selected-run-summary\" data-kora-component=\"selected-run-summary\" aria-live=\"polite\">
            <strong>Composer selected-run summary</strong>
            <span>Request: <code id=\"kora-composer-request-id\">{selector_preview_id}</code></span>
            <span>Status: <code id=\"kora-composer-run-status\">not_started</code></span>
            <span>Run id: <code id=\"kora-composer-run-id\">not run yet</code></span>
            <span>Boundary: approved local harness request only</span>
          </div>
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
      </section>
      <aside class=\"details-drawer-shell\" id=\"kora-details-drawer\" aria-label=\"KORA Studio right details drawer scaffold\" data-kora-component=\"right-details-drawer\" data-kora-mobile-drawer=\"right-overlay\" data-kora-drawer-state=\"closed\" aria-hidden=\"true\" tabindex=\"-1\">
        <div class=\"drawer-header\">
          <div>
            <h2>Details</h2>
            <p class=\"subtitle\">Inspector · local preview</p>
          </div>
          <button class=\"drawer-close-button\" type=\"button\" id=\"kora-details-drawer-close\" aria-label=\"Close details drawer\" data-kora-drawer-close=\"true\">x</button>
        </div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"runtime-status\"><h3>Runtime status</h3><p>Local runtime: {runtime_name}</p><p>Runtime detected: {runtime_detected}</p><p>Service reachability: {service_status}</p><p>Model execution: not connected yet</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"selected-model\"><h3>Selected model</h3><p>Suggested estimate: {local_candidate_name}</p><p>Catalog candidate only; not installed unless detected.</p><p>Selection does not install or run a model.</p><p>Top selector: <code>Search or select open-source LLM</code></p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"catalog-vs-installed\"><h3>Catalog vs installed</h3><p>Catalog candidate: {local_candidate_name}</p><p>Catalog status: {catalog_status}</p><p>Installed detection: {installed_status}</p><p>Installed count: {installed_count}</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"route-trace\"><h3>Route trace</h3><p>Sample request: <code>{sample_request_id}</code></p><p>Expected route: {sample_route}</p><p>Validation: {sample_validation}</p><p>Generated harness events only.</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"generated-counters\"><h3>Generated counters</h3><p>Total requests: {total_requests}</p><p>Baseline model calls: {baseline_model_calls}</p><p>KORA model calls: {kora_model_calls}</p><p>Avoided model calls: {avoided_model_calls}</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"selected-run-surfaces\" data-kora-drawer-selected-run-coverage=\"timeline,counters,comparison,report-metadata\" data-kora-v1-1-drawer-selected-run-polish=\"primary-diagnostics\"><h3>Selected run surfaces</h3><p>Run id: <code id=\"kora-drawer-selected-run-id\">not run yet</code></p><p>Timeline: <span id=\"kora-drawer-selected-timeline-status\">not loaded</span></p><p>Counters: <span id=\"kora-drawer-selected-counters-status\">not loaded</span></p><p>Comparison: <span id=\"kora-drawer-selected-comparison-status\">not loaded</span></p><p>Report metadata: <span id=\"kora-drawer-selected-report-status\">not loaded</span></p><p>Drawer selected-run diagnostics mirror shell state for normal inspection: timeline availability, generated counters, local harness comparison, and report metadata preview.</p><p>Generated local harness output only. Not model token streaming. Not production telemetry. Not production cost evidence. Report metadata preview only. No file export or writing.</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"report-metadata\"><h3>Report metadata</h3><p>Report status: {report_viewer_status}</p><p>Report source: {report_source}</p><p>File export: {report_file_export_enabled}</p><p>File written: {report_file_written}</p></div>
        <div class=\"drawer-section-block drawer-boundary\" data-kora-drawer-section=\"claim-boundaries\" data-kora-drawer-boundary-coverage=\"provider,cloud,download,model-execution,report-export,private-scan,runtime-list\"><h3>Claim boundaries</h3><p>Local preview only.</p><p>No arbitrary prompt execution.</p><p>No model execution.</p><p>No provider calls.</p><p>No downloads.</p><p>No cloud sync.</p><p>No report file export or writing.</p><p>No private model directory scanning.</p><p>No runtime model list commands.</p></div>
      </aside>
    </div>
  </div>

  <details class=\"legacy-preview\" aria-label=\"Detailed local preview compatibility scaffolds\" data-kora-component=\"legacy-compatibility-reference\" data-kora-legacy-preview-mode=\"compatibility-collapsed\" data-kora-legacy-preview-default=\"collapsed\" data-kora-legacy-preview-role=\"developer-compatibility-scaffold\" data-kora-v1-1-legacy-secondary=\"developer-reference-only\" data-kora-v1-1-legacy-first-run-required=\"false\">
    <summary aria-label=\"Open legacy detailed preview compatibility scaffold\">
      <div class=\"legacy-preview-summary\">
        <div><strong>Legacy detailed preview compatibility scaffold</strong><span>Collapsed by default. The final shell and Details drawer above are the primary local preview; this developer reference is not required for first-run understanding.</span></div>
        <span class=\"legacy-preview-summary-badge\">Developer reference only</span>
      </div>
    </summary>
    <p class=\"legacy-preview-summary\" data-kora-v1-1-legacy-boundary=\"secondary-reference-only\">This compatibility scaffold remains local-only and secondary. It does not enable model execution, provider calls, downloads, cloud sync, report export, or report writing.</p>
    <div class=\"legacy-preview-content\">
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
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\"><h3>Selected run state</h3><p>Generated local harness output only.</p><div class=\"run-state\" id=\"kora-selected-run-state\" aria-live=\"polite\"><p>Status: <span id=\"kora-run-status\">not_started</span></p><p>Run id: <code id=\"kora-selected-run-id\">not run yet</code></p><p>Request id: <code id=\"kora-run-request-id\">not run yet</code></p><p>Event count: <span id=\"kora-run-event-count\">0</span></p><p>Model execution status: <span id=\"kora-run-model-execution-status\">not_connected</span></p><p>Provider calls: <span id=\"kora-run-provider-calls-enabled\">false</span></p><p>Cloud sync: <span id=\"kora-run-cloud-sync-enabled\">false</span></p><p>File export: <span id=\"kora-run-file-export-enabled\">false</span></p><p>Claim boundary: <span id=\"kora-run-claim-boundary\">No run has been generated yet.</span></p></div></div>
          <div class=\"card\"><h3>Interactive run boundary</h3><p>Model-needed boundary returns <code>execution_not_connected</code>.</p><p>No model execution was attempted.</p><p>Provider calls remain disabled.</p><p>No downloads.</p><p>Selected run state is local browser memory only.</p></div>
        </div>
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\" data-kora-component=\"retry-error-state\"><h3>Selected Run Error State</h3><p id=\"kora-run-error-state\">No selected-run error.</p><p>Retry uses the last approved request only.</p><p>No model execution was attempted.</p><p>Provider calls remain disabled.</p><p>No downloads are connected.</p></div>
          <div class=\"card\"><h3>Retry Last Approved Request</h3><p>Last approved request: <code id=\"kora-last-approved-request-id\">{selector_preview_id}</code></p><p>Retry available: <span id=\"kora-retry-available\">false</span></p><button class=\"action-button\" type=\"button\" id=\"kora-retry-last-approved-request-button\" disabled>Retry Last Approved Request</button><p>Retry calls only <code>POST /api/harness/run</code> with the last approved <code>request_id</code>.</p><p>No arbitrary prompt execution.</p></div>
        </div>
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\" data-kora-component=\"run-history\"><h3>Local Run History</h3><p>Browser-local run history.</p><p>Page-memory only.</p><p>Clears on refresh.</p><p>Active selected run: <code id=\"kora-active-history-run-id\">none</code></p><p>History cards show compact counters from generated harness output only.</p><p>Local deterministic harness output only.</p><p>No model execution. No provider calls. No downloads.</p><p>History count: <span id=\"kora-run-history-count\">0</span></p><p id=\"kora-run-history-status\">Run an approved local harness request to add browser-local history.</p></div>
          <div class=\"card\"><h3>Clear Local Run History</h3><button class=\"action-button\" type=\"button\" id=\"kora-clear-run-history-button\">Clear Local Run History</button><p>Clears browser-local preview state only.</p><p>Resets selected-run UI, selected events, selected counters, selected comparison, selected report metadata, and page-memory history.</p><p>Does not remove server run records, reports, files, backend records, or generated harness endpoints.</p><p>No persistence, no cloud sync, no file export, no file writing, and no backend delete call.</p></div>
        </div>
        <div class=\"grid\" id=\"kora-local-run-history\" aria-live=\"polite\"></div>
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\" data-kora-component=\"generated-event-stream-status\"><h3>Generated Event Stream</h3><p>Generated harness events only.</p><p>Not model token streaming.</p><p>No provider streaming.</p><p>No model execution.</p><p>Fallback to local events endpoint available.</p><p>Status: <span id=\"kora-sse-status\">idle</span></p><p>Fallback used: <span id=\"kora-sse-fallback-used\">false</span></p><p id=\"kora-sse-error\">No generated event stream error.</p></div>
        </div>
        <div class=\"card\" style=\"margin-top: 16px;\" data-kora-component=\"selected-run-event-timeline\"><h3>Selected Run Event Timeline</h3><p>Generated local harness events only. Not model token streaming. No model execution. No provider calls. No downloads.</p><p>Events are fetched from <code>GET /api/harness/events?run_id=&lt;id&gt;</code> after a successful approved local harness run.</p><p id=\"kora-selected-events-status\">No selected run events loaded yet.</p></div>
        <div class=\"grid\" id=\"kora-selected-run-events\" aria-live=\"polite\"></div>
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\" data-kora-component=\"selected-run-counters\"><h3>Selected Run Counters</h3><p>Generated local harness counters only. Not production telemetry. No model execution. No provider calls. No cost or energy claim.</p><p id=\"kora-selected-counters-status\">Run an approved local harness request to view selected-run counters.</p></div>
          <div class=\"card\" data-kora-component=\"selected-run-comparison\"><h3>Selected Run: Standard Mode vs KORA Boost</h3><p>Comparison is generated from approved local harness output. This is not production cost evidence. This does not execute a model.</p><p>Model-needed boundaries remain <code>execution_not_connected</code>.</p><p id=\"kora-selected-comparison-status\">Run an approved local harness request to view selected-run comparison.</p></div>
        </div>
        <div class=\"grid\" id=\"kora-selected-run-counters\" aria-live=\"polite\"></div>
        <div class=\"grid\" id=\"kora-selected-run-comparison\" aria-live=\"polite\"></div>
        <div class=\"card\" style=\"margin-top: 16px;\" data-kora-component=\"selected-run-report-metadata\"><h3>Selected Run Report Metadata</h3><p>Report metadata preview only. No file export. No file writing. Generated local harness output only.</p><p>No model execution. No provider calls. No cloud sync. Not production evidence.</p><p id=\"kora-selected-report-status\">Run an approved local harness request to view selected-run report metadata.</p></div>
        <div class=\"grid\" id=\"kora-selected-run-report-metadata\" aria-live=\"polite\"></div>
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
  <script>
    (function () {{
      window.koraStudioScriptStatus = {{status: "booting", error: ""}};
      window.addEventListener("error", (event) => {{
        window.koraStudioScriptStatus = {{status: "failed", error: event.message || "Unknown local preview script error."}};
      }});
      const dataElement = document.getElementById("kora-approved-requests-data");
      const approvedRequests = JSON.parse(dataElement ? dataElement.textContent || "[]" : "[]");
      const requestById = new Map(approvedRequests.map((request) => [request.request_id, request]));
      let selectedRequestId = approvedRequests.length ? approvedRequests[0].request_id : "";
      let selectedRunId = "";
      let selectedRunEvents = [];
      let selectedRunCounters = {{}};
      let selectedRunComparison = {{}};
      let selectedRunReportMetadata = {{}};
      let runLoading = false;
      let runError = "";
      let lastApprovedRequestId = selectedRequestId;
      let retryAvailable = false;
      let runHistory = [];
      const runHistoryLimit = 5;
      let sseAvailable = typeof EventSource !== "undefined";
      let sseStatus = "idle";
      let sseError = "";
      let sseEvents = [];
      let sseFallbackUsed = false;
      let activeEventSource = null;

      const text = (id, value) => {{
        const element = document.getElementById(id);
        if (element) {{
          element.textContent = String(value);
        }}
      }};

      const studioShell = document.querySelector(".studio-shell");
      const leftRail = document.getElementById("kora-left-rail");
      const leftRailToggle = document.getElementById("kora-left-rail-toggle");
      const leftRailClose = document.getElementById("kora-left-rail-close");
      const workspace = document.querySelector(".studio-workspace");
      const detailsDrawer = document.getElementById("kora-details-drawer");
      const detailsDrawerToggle = document.getElementById("kora-details-drawer-toggle");
      const detailsDrawerClose = document.getElementById("kora-details-drawer-close");

      const isSmallRailViewport = () => {{
        if (typeof window === "undefined" || typeof window.matchMedia !== "function") {{
          return false;
        }}
        return window.matchMedia("(max-width: 760px)").matches;
      }};

      const setLeftRailOpen = (open, options) => {{
        const shouldOpen = open === true;
        if (studioShell) {{
          studioShell.setAttribute("data-kora-rail-open", shouldOpen ? "true" : "false");
        }}
        if (leftRail) {{
          leftRail.setAttribute("data-kora-rail-state", shouldOpen ? "open" : "closed");
          leftRail.setAttribute("aria-hidden", !shouldOpen && isSmallRailViewport() ? "true" : "false");
        }}
        if (leftRailToggle) {{
          leftRailToggle.setAttribute("aria-expanded", shouldOpen ? "true" : "false");
          leftRailToggle.setAttribute("aria-label", shouldOpen ? "Close left rail" : "Open left rail");
        }}
        const shouldManageFocus = !options || options.manageFocus !== false;
        if (shouldManageFocus && shouldOpen && leftRailClose) {{
          leftRailClose.focus();
        }}
        if (shouldManageFocus && !shouldOpen && leftRailToggle) {{
          leftRailToggle.focus();
        }}
      }};

      if (leftRailToggle) {{
        leftRailToggle.addEventListener("click", () => {{
          const isOpen = leftRailToggle.getAttribute("aria-expanded") === "true";
          setLeftRailOpen(!isOpen);
        }});
      }}
      if (leftRailClose) {{
        leftRailClose.addEventListener("click", () => {{
          setLeftRailOpen(false);
        }});
      }}
      if (typeof window !== "undefined") {{
        window.addEventListener("resize", () => {{
          const isOpen = leftRailToggle && leftRailToggle.getAttribute("aria-expanded") === "true";
          setLeftRailOpen(isOpen, {{manageFocus: false}});
        }});
      }}

      const setDetailsDrawerOpen = (open, options) => {{
        const shouldOpen = open === true;
        if (workspace) {{
          workspace.setAttribute("data-kora-drawer-open", shouldOpen ? "true" : "false");
        }}
        if (detailsDrawer) {{
          detailsDrawer.setAttribute("data-kora-drawer-state", shouldOpen ? "open" : "closed");
          detailsDrawer.setAttribute("aria-hidden", shouldOpen ? "false" : "true");
        }}
        if (detailsDrawerToggle) {{
          detailsDrawerToggle.setAttribute("aria-expanded", shouldOpen ? "true" : "false");
          detailsDrawerToggle.setAttribute("aria-label", shouldOpen ? "Close details drawer" : "Open details drawer");
        }}
        const shouldManageFocus = !options || options.manageFocus !== false;
        if (shouldManageFocus && shouldOpen && detailsDrawerClose) {{
          detailsDrawerClose.focus();
        }}
        if (shouldManageFocus && !shouldOpen && detailsDrawerToggle) {{
          detailsDrawerToggle.focus();
        }}
      }};

      if (detailsDrawerToggle) {{
        detailsDrawerToggle.addEventListener("click", () => {{
          const isOpen = detailsDrawerToggle.getAttribute("aria-expanded") === "true";
          setDetailsDrawerOpen(!isOpen);
        }});
      }}
      if (detailsDrawerClose) {{
        detailsDrawerClose.addEventListener("click", () => {{
          setDetailsDrawerOpen(false);
        }});
      }}
      document.addEventListener("keydown", (event) => {{
        if (event.key === "Escape" && leftRail && leftRail.getAttribute("data-kora-rail-state") === "open") {{
          setLeftRailOpen(false);
        }}
        if (event.key === "Escape" && detailsDrawer && detailsDrawer.getAttribute("data-kora-drawer-state") === "open") {{
          setDetailsDrawerOpen(false);
        }}
      }});
      setLeftRailOpen(false, {{manageFocus: false}});
      setDetailsDrawerOpen(false, {{manageFocus: false}});

      const setButtonState = () => {{
        document.querySelectorAll("[data-kora-request-id]").forEach((button) => {{
          button.setAttribute("aria-pressed", button.getAttribute("data-kora-request-id") === selectedRequestId ? "true" : "false");
        }});
      }};

      const setRetryState = (available, message) => {{
        retryAvailable = available === true && requestById.has(lastApprovedRequestId);
        text("kora-run-error-state", message || "No selected-run error.");
        text("kora-last-approved-request-id", lastApprovedRequestId || "none");
        text("kora-retry-available", retryAvailable ? "true" : "false");
        const retryButton = document.getElementById("kora-retry-last-approved-request-button");
        if (retryButton) {{
          retryButton.disabled = !retryAvailable || runLoading;
        }}
      }};

      const setRunLoading = (loading) => {{
        runLoading = loading === true;
        const runButton = document.getElementById("kora-run-local-harness-button");
        const composerRunButton = document.getElementById("kora-composer-run-local-harness-button");
        const retryButton = document.getElementById("kora-retry-last-approved-request-button");
        if (runButton) {{
          runButton.disabled = runLoading;
        }}
        if (composerRunButton) {{
          composerRunButton.disabled = runLoading;
        }}
        if (retryButton) {{
          retryButton.disabled = runLoading || !retryAvailable;
        }}
      }};

      const setSseState = (status, error, fallbackUsed) => {{
        sseStatus = status || "idle";
        sseError = error || "";
        if (fallbackUsed !== undefined) {{
          sseFallbackUsed = fallbackUsed === true;
        }}
        text("kora-sse-status", sseStatus);
        text("kora-sse-error", sseError || "No generated event stream error.");
        text("kora-sse-fallback-used", sseFallbackUsed ? "true" : "false");
      }};

      const closeActiveEventSource = () => {{
        if (activeEventSource) {{
          activeEventSource.close();
          activeEventSource = null;
        }}
      }};

      const setShellSelectedRunSurfaceState = (updates) => {{
        const state = updates || {{}};
        if (state.run_id !== undefined) {{
          text("kora-drawer-selected-run-id", state.run_id || "not run yet");
        }}
        if (state.timeline !== undefined) {{
          text("kora-shell-selected-timeline-status", state.timeline);
          text("kora-drawer-selected-timeline-status", state.timeline);
        }}
        if (state.counters !== undefined) {{
          text("kora-shell-selected-counters-status", state.counters);
          text("kora-drawer-selected-counters-status", state.counters);
        }}
        if (state.comparison !== undefined) {{
          text("kora-shell-selected-comparison-status", state.comparison);
          text("kora-drawer-selected-comparison-status", state.comparison);
        }}
        if (state.report !== undefined) {{
          text("kora-shell-selected-report-status", state.report);
          text("kora-drawer-selected-report-status", state.report);
        }}
      }};

      const getShellAccessibilityState = () => {{
        return {{
          left_rail_state: leftRail ? leftRail.getAttribute("data-kora-rail-state") : "missing",
          left_rail_expanded: leftRailToggle ? leftRailToggle.getAttribute("aria-expanded") : "missing",
          details_drawer_state: detailsDrawer ? detailsDrawer.getAttribute("data-kora-drawer-state") : "missing",
          details_drawer_expanded: detailsDrawerToggle ? detailsDrawerToggle.getAttribute("aria-expanded") : "missing",
          model_selector_state: document.querySelector("[data-kora-model-selector]") ? document.querySelector("[data-kora-model-selector]").getAttribute("data-kora-model-selection-state") : "missing",
          selected_request_id: selectedRequestId || "none",
          keyboard_focus_pass: studioShell ? studioShell.getAttribute("data-kora-keyboard-focus-pass") : "missing"
        }};
      }};

      const renderSelectedRequest = () => {{
        const request = requestById.get(selectedRequestId);
        if (!request) {{
          text("kora-selected-request-id", "none");
          text("kora-composer-request-id", "none");
          text("kora-selected-request-text", "No approved request selected.");
          text("kora-selected-request-route", "unknown");
          text("kora-selected-request-model-needed", "unknown");
          return;
        }}
        text("kora-selected-request-id", request.request_id);
        text("kora-composer-request-id", request.request_id);
        text("kora-selected-request-text", request.input_text || "Approved local sample request.");
        text("kora-selected-request-route", request.expected_route_class || "unknown");
        text("kora-selected-request-model-needed", request.expected_model_needed === true ? "true" : "false");
        setButtonState();
      }};

      const renderRunError = (message) => {{
        runError = message || "Local harness run failed.";
        text("kora-run-status", "failed");
        text("kora-composer-run-status", "failed");
        text("kora-composer-run-id", "not available");
        text("kora-run-claim-boundary", `${{runError}} No model execution was attempted. Provider calls remain disabled. Try again or inspect the local server logs.`);
        setRetryState(true, `${{runError}} Retry uses the last approved request only. No model execution was attempted. Provider calls remain disabled.`);
        renderCountersUnavailable("Selected-run counters unavailable.");
        renderComparisonUnavailable("Selected-run comparison unavailable.");
        renderReportMetadataUnavailable("Selected-run report metadata unavailable.");
        setShellSelectedRunSurfaceState({{
          run_id: "not available",
          timeline: "unavailable",
          counters: "unavailable",
          comparison: "unavailable",
          report: "unavailable"
        }});
      }};

      const renderEventError = (message) => {{
        selectedRunEvents = [];
        runError = message || "Generated events unavailable for this local run.";
        text("kora-selected-events-status", `${{runError}} No model execution was attempted. Provider calls remain disabled.`);
        setRetryState(true, `${{runError}} Retry uses the last approved request only. No model execution was attempted. Provider calls remain disabled.`);
        const container = document.getElementById("kora-selected-run-events");
        if (container) {{
          container.replaceChildren();
        }}
        setShellSelectedRunSurfaceState({{timeline: "unavailable"}});
      }};

      const clearSelectedCards = (id) => {{
        const container = document.getElementById(id);
        if (container) {{
          container.replaceChildren();
        }}
      }};

      const renderCountersUnavailable = (message) => {{
        selectedRunCounters = {{}};
        text("kora-selected-counters-status", `${{message}} Generated local harness output only. No model execution. No provider calls.`);
        clearSelectedCards("kora-selected-run-counters");
        setShellSelectedRunSurfaceState({{counters: "unavailable"}});
      }};

      const renderComparisonUnavailable = (message) => {{
        selectedRunComparison = {{}};
        text("kora-selected-comparison-status", `${{message}} This is not production cost evidence. No model execution. No provider calls.`);
        clearSelectedCards("kora-selected-run-comparison");
        setShellSelectedRunSurfaceState({{comparison: "unavailable"}});
      }};

      const renderReportMetadataUnavailable = (message) => {{
        selectedRunReportMetadata = {{}};
        text("kora-selected-report-status", `${{message}} Report metadata preview only. No file export. No file writing.`);
        clearSelectedCards("kora-selected-run-report-metadata");
        setShellSelectedRunSurfaceState({{report: "unavailable"}});
      }};

      const renderSelectedCounters = (counters, eventCount) => {{
        selectedRunCounters = counters && typeof counters === "object" ? counters : {{}};
        const container = document.getElementById("kora-selected-run-counters");
        if (!container) {{
          return;
        }}
        container.replaceChildren();
        const counterKeys = [
          "total_requests",
          "baseline_model_calls",
          "kora_model_calls",
          "avoided_model_calls",
          "deterministic_routes",
          "model_escalations",
          "validation_pass_count",
          "validation_fail_count"
        ];
        if (!Object.keys(selectedRunCounters).length) {{
          renderCountersUnavailable("Selected-run counters unavailable.");
          return;
        }}
        text("kora-selected-counters-status", "Selected-run counters loaded from generated local harness output. Not production telemetry.");
        setShellSelectedRunSurfaceState({{counters: "loaded from selected run"}});
        counterKeys.concat(["event_count"]).forEach((key) => {{
          const value = key === "event_count" ? eventCount : selectedRunCounters[key];
          const card = document.createElement("div");
          card.className = "card";
          const title = document.createElement("h3");
          title.textContent = key;
          const number = document.createElement("p");
          number.className = "status-value";
          number.textContent = String(value === undefined ? 0 : value);
          const note = document.createElement("p");
          note.textContent = "Generated local harness counters only. No cost or energy claim.";
          card.appendChild(title);
          card.appendChild(number);
          card.appendChild(note);
          container.appendChild(card);
        }});
      }};

      const renderSelectedComparison = (comparison, modelExecutionStatus) => {{
        selectedRunComparison = comparison && typeof comparison === "object" ? comparison : {{}};
        const container = document.getElementById("kora-selected-run-comparison");
        if (!container) {{
          return;
        }}
        container.replaceChildren();
        const metrics = selectedRunComparison.metrics || selectedRunComparison.comparison_counters || {{}};
        const comparisonFields = [
          ["comparison_status", selectedRunComparison.comparison_status || "unknown"],
          ["baseline_model_calls", metrics.baseline_model_calls],
          ["kora_model_calls", metrics.kora_model_calls],
          ["avoided_model_calls", metrics.avoided_model_calls],
          ["model_escalations", metrics.model_escalations],
          ["deterministic_routes", metrics.deterministic_routes],
          ["model_execution_status", modelExecutionStatus || "execution_not_connected"]
        ];
        if (!Object.keys(selectedRunComparison).length) {{
          renderComparisonUnavailable("Selected-run comparison unavailable.");
          return;
        }}
        text("kora-selected-comparison-status", "Selected-run comparison loaded from approved local harness output. Not production cost evidence.");
        setShellSelectedRunSurfaceState({{comparison: "loaded from selected run"}});
        comparisonFields.forEach(([label, value]) => {{
          const card = document.createElement("div");
          card.className = "card";
          const title = document.createElement("h3");
          title.textContent = label;
          const display = document.createElement("p");
          display.className = "status-value";
          display.textContent = String(value === undefined ? 0 : value);
          const note = document.createElement("p");
          note.textContent = "Comparison is generated from approved local harness output. This does not execute a model.";
          card.appendChild(title);
          card.appendChild(display);
          card.appendChild(note);
          container.appendChild(card);
        }});
      }};

      const renderSelectedReportMetadata = (report) => {{
        selectedRunReportMetadata = report && typeof report === "object" ? report : {{}};
        const container = document.getElementById("kora-selected-run-report-metadata");
        if (!container) {{
          return;
        }}
        container.replaceChildren();
        if (!Object.keys(selectedRunReportMetadata).length) {{
          renderReportMetadataUnavailable("Selected-run report metadata unavailable.");
          return;
        }}
        text("kora-selected-report-status", "Selected-run report metadata loaded. Report metadata preview only. Not production evidence.");
        setShellSelectedRunSurfaceState({{report: "preview loaded from selected run"}});
        const fields = [
          ["report_status", selectedRunReportMetadata.report_status || selectedRunReportMetadata.report_viewer_status || "unknown"],
          ["report_source", selectedRunReportMetadata.report_source || "local_harness_summary"],
          ["run_id", selectedRunReportMetadata.run_id || selectedRunId || "unknown"],
          ["request_id", selectedRunReportMetadata.request_id || selectedRequestId || "unknown"],
          ["generated_at", selectedRunReportMetadata.generated_at || selectedRunReportMetadata.created_at || "unknown"],
          ["event_count", selectedRunReportMetadata.event_count === undefined ? 0 : selectedRunReportMetadata.event_count],
          ["counter_summary_status", selectedRunReportMetadata.counter_summary ? "available" : "not_available"],
          ["comparison_summary_status", selectedRunReportMetadata.comparison_summary_status || "unknown"],
          ["model_execution_status", selectedRunReportMetadata.model_execution_status || "execution_not_connected"],
          ["provider_calls_enabled", selectedRunReportMetadata.provider_calls_enabled === true ? "true" : "false"],
          ["cloud_sync_enabled", selectedRunReportMetadata.cloud_sync_enabled === true ? "true" : "false"],
          ["file_export_enabled", selectedRunReportMetadata.file_export_enabled === true ? "true" : "false"],
          ["file_written", selectedRunReportMetadata.file_written === true ? "true" : "false"]
        ];
        fields.forEach(([label, value]) => {{
          const card = document.createElement("div");
          card.className = "card";
          const title = document.createElement("h3");
          title.textContent = label;
          const display = document.createElement("p");
          display.className = "status-value";
          display.textContent = String(value);
          const note = document.createElement("p");
          note.textContent = "Report metadata preview only. No file export. No file writing.";
          card.appendChild(title);
          card.appendChild(display);
          card.appendChild(note);
          container.appendChild(card);
        }});
        const boundaryCard = document.createElement("div");
        boundaryCard.className = "card";
        const title = document.createElement("h3");
        title.textContent = "Report claim boundary";
        const boundary = document.createElement("p");
        boundary.textContent = selectedRunReportMetadata.claim_boundary || "Local deterministic harness output only. No model execution. No provider calls. No cloud sync. Not production evidence.";
        const noExport = document.createElement("p");
        noExport.textContent = "No file export. No file writing. No downloads.";
        boundaryCard.appendChild(title);
        boundaryCard.appendChild(boundary);
        boundaryCard.appendChild(noExport);
        container.appendChild(boundaryCard);
      }};

      const renderSelectedEvents = (events) => {{
        selectedRunEvents = Array.isArray(events) ? events : [];
        const container = document.getElementById("kora-selected-run-events");
        if (!container) {{
          return;
        }}
        container.replaceChildren();
        if (!selectedRunEvents.length) {{
          text("kora-selected-events-status", "Generated events unavailable for this local run. No model execution was attempted. Provider calls remain disabled.");
          setShellSelectedRunSurfaceState({{timeline: "unavailable"}});
          return;
        }}
        text("kora-selected-events-status", `Loaded ${{selectedRunEvents.length}} generated local harness events for the selected run.`);
        setShellSelectedRunSurfaceState({{timeline: `loaded from selected run (${{selectedRunEvents.length}} events)`}});
        selectedRunEvents.forEach((event) => {{
          const card = document.createElement("div");
          card.className = "card";
          const fields = [
            ["Stage", event.stage_id || "unknown"],
            ["Name", event.stage_name || "Unknown stage"],
            ["Route class", event.route_class || "unknown"],
            ["Status", event.status || "unknown"],
            ["Model called", event.model_called === true ? "true" : "false"],
            ["Deterministic route used", event.deterministic_route_used === true ? "true" : "false"],
            ["Validation result", event.validation_result || "not_applicable"],
            ["Latency", `${{event.latency_ms || 0}} ms`],
            ["Model execution status", event.model_execution_status || "execution_not_connected"]
          ];
          const title = document.createElement("h3");
          title.textContent = event.stage_name || event.stage_id || "Selected run event";
          card.appendChild(title);
          fields.forEach(([label, value]) => {{
            const row = document.createElement("p");
            row.textContent = `${{label}}: ${{value}}`;
            card.appendChild(row);
          }});
          const boundary = document.createElement("p");
          boundary.textContent = "Generated local harness events only. No model execution. No provider output. No downloads.";
          card.appendChild(boundary);
          container.appendChild(card);
        }});
      }};

      const eventFromSsePayload = (payload) => {{
        if (payload && payload.event && typeof payload.event === "object") {{
          return payload.event;
        }}
        if (!payload || !payload.stage_id) {{
          return null;
        }}
        return {{
          run_id: payload.run_id || selectedRunId,
          request_id: payload.request_id || selectedRequestId,
          stage_id: payload.stage_id,
          stage_name: payload.stage_name || payload.stage_id,
          route_class: payload.route_class || "unknown",
          status: payload.status || "unknown",
          model_called: false,
          deterministic_route_used: false,
          validation_result: "not_applicable",
          latency_ms: 0,
          model_execution_status: "execution_not_connected"
        }};
      }};

      const renderSseEvents = () => {{
        renderSelectedEvents(sseEvents);
        text("kora-selected-events-status", `Loaded ${{sseEvents.length}} generated harness events from the generated event stream. Not model token streaming. No provider streaming.`);
        setShellSelectedRunSurfaceState({{timeline: `streamed from selected run (${{sseEvents.length}} events)`}});
      }};

      const renderRunHistory = () => {{
        const container = document.getElementById("kora-local-run-history");
        text("kora-run-history-count", runHistory.length);
        text("kora-active-history-run-id", selectedRunId || "none");
        if (!container) {{
          return;
        }}
        container.replaceChildren();
        if (!runHistory.length) {{
          text("kora-run-history-status", "No browser-local run history yet. Page-memory only. Clears on refresh. No backend records or files are deleted.");
          return;
        }}
        text("kora-run-history-status", "Browser-local run history loaded. Active selected run is marked in page memory only. Not production evidence.");
        runHistory.forEach((record) => {{
          const isActive = record.run_id === selectedRunId;
          const counters = record.generated_counters || {{}};
          const card = document.createElement("div");
          card.className = "card";
          if (isActive) {{
            card.setAttribute("aria-current", "true");
          }}
          const title = document.createElement("h3");
          title.textContent = isActive ? "Active selected local run" : "Recent local run";
          const activeState = document.createElement("p");
          activeState.textContent = `Active selected run: ${{isActive ? "true" : "false"}}`;
          const runId = document.createElement("p");
          runId.textContent = `Run id: ${{record.run_id || "unknown"}}`;
          const requestId = document.createElement("p");
          requestId.textContent = `Request id: ${{record.request_id || "unknown"}}`;
          const status = document.createElement("p");
          status.textContent = `Status: ${{record.run_status || "unknown"}}`;
          const eventCount = document.createElement("p");
          eventCount.textContent = `Event count: ${{record.event_count || 0}}`;
          const compactCounters = document.createElement("p");
          compactCounters.textContent = `Compact counters: avoided_model_calls=${{counters.avoided_model_calls || 0}}, kora_model_calls=${{counters.kora_model_calls || 0}}, deterministic_routes=${{counters.deterministic_routes || 0}}, model_escalations=${{counters.model_escalations || 0}}, validation_pass_count=${{counters.validation_pass_count || 0}}`;
          const modelStatus = document.createElement("p");
          modelStatus.textContent = `Model execution status: ${{record.model_execution_status || "execution_not_connected"}}`;
          const createdAt = document.createElement("p");
          createdAt.textContent = `Created at: ${{record.created_at || "unknown"}}`;
          const completedAt = document.createElement("p");
          completedAt.textContent = `Completed at: ${{record.completed_at || "unknown"}}`;
          const boundary = document.createElement("p");
          boundary.textContent = "Browser-local history item. Local deterministic harness output only. No model execution, provider calls, downloads, persistence, or cloud sync.";
          const selectButton = document.createElement("button");
          selectButton.className = "action-button";
          selectButton.type = "button";
          selectButton.textContent = "Select run";
          selectButton.setAttribute("data-kora-history-run-id", record.run_id || "");
          if (isActive) {{
            selectButton.textContent = "Selected in page";
          }}
          selectButton.addEventListener("click", () => {{
            selectRunFromHistory(record.run_id || "");
          }});
          card.appendChild(title);
          card.appendChild(activeState);
          card.appendChild(runId);
          card.appendChild(requestId);
          card.appendChild(status);
          card.appendChild(eventCount);
          card.appendChild(compactCounters);
          card.appendChild(modelStatus);
          card.appendChild(createdAt);
          card.appendChild(completedAt);
          card.appendChild(boundary);
          card.appendChild(selectButton);
          container.appendChild(card);
        }});
      }};

      const selectRunFromHistory = (runId) => {{
        closeActiveEventSource();
        const record = runHistory.find((item) => item.run_id === runId);
        if (!record) {{
          renderRunError("Selected browser-local run was not found.");
          return;
        }}
        renderRunResponse(record, {{updateHistory: false}});
        renderSelectedEvents(record.generated_events || []);
        setSseState("idle", "Selected run restored from browser-local history. Generated stream not connected for restored history item.", false);
        setRetryState(false, "Selected run restored from browser-local page memory.");
        text("kora-run-history-status", "Selected run restored from browser-local page memory. Not production evidence.");
      }};

      const addRunToHistory = (run) => {{
        if (!run || !run.run_id || run.run_status !== "completed") {{
          return;
        }}
        runHistory = [run].concat(runHistory.filter((record) => record.run_id !== run.run_id)).slice(0, runHistoryLimit);
        renderRunHistory();
      }};

      const clearLocalRunHistory = () => {{
        closeActiveEventSource();
        runHistory = [];
        selectedRunId = "";
        selectedRunEvents = [];
        selectedRunCounters = {{}};
        selectedRunComparison = {{}};
        selectedRunReportMetadata = {{}};
        runError = "";
        text("kora-selected-run-id", "not run yet");
        text("kora-run-request-id", "not run yet");
        text("kora-run-status", "not_started");
        text("kora-composer-run-status", "not_started");
        text("kora-run-event-count", "0");
        text("kora-composer-run-id", "not run yet");
        text("kora-composer-request-id", selectedRequestId || "none");
        text("kora-run-model-execution-status", "not_connected");
        text("kora-run-provider-calls-enabled", "false");
        text("kora-run-cloud-sync-enabled", "false");
        text("kora-run-file-export-enabled", "false");
        text("kora-run-claim-boundary", "Cleared browser-local preview state only.");
        text("kora-active-history-run-id", "none");
        text("kora-selected-events-status", "No selected run events loaded yet.");
        renderCountersUnavailable("Run an approved local harness request to view selected-run counters.");
        renderComparisonUnavailable("Run an approved local harness request to view selected-run comparison.");
        renderReportMetadataUnavailable("Run an approved local harness request to view selected-run report metadata.");
        clearSelectedCards("kora-selected-run-events");
        setShellSelectedRunSurfaceState({{
          run_id: "not run yet",
          timeline: "not loaded",
          counters: "not loaded",
          comparison: "not loaded",
          report: "not loaded"
        }});
        setRetryState(false, "Cleared browser-local preview state only.");
        sseEvents = [];
        setSseState("idle", "Cleared browser-local preview state only. No backend records, files, report exports, or server endpoints were deleted.", false);
        renderRunHistory();
      }};

      const fetchSelectedEvents = async () => {{
        if (!selectedRunId) {{
          renderEventError("Generated events unavailable for this local run.");
          return;
        }}
        text("kora-selected-events-status", "Loading generated local harness events.");
        try {{
          const response = await fetch(`/api/harness/events?run_id=${{encodeURIComponent(selectedRunId)}}`);
          let payload;
          try {{
            payload = await response.json();
          }} catch (parseError) {{
            throw new Error("The local response could not be parsed.");
          }}
          if (!response.ok || payload.ok === false || !Array.isArray(payload.events)) {{
            throw new Error(payload.message || "Generated events unavailable for this local run.");
          }}
          renderSelectedEvents(payload.events);
        }} catch (error) {{
          const message = error instanceof TypeError ? "The local harness endpoint was unavailable." : (error && error.message ? error.message : "Generated events unavailable for this local run.");
          renderEventError(message);
        }}
      }};

      const fetchSelectedEventsFallback = async (message) => {{
        sseFallbackUsed = true;
        setSseState("fallback", message || "Generated event stream unavailable; using local events endpoint fallback.", true);
        await fetchSelectedEvents();
      }};

      const connectGeneratedEventStream = async () => {{
        closeActiveEventSource();
        sseEvents = [];
        sseFallbackUsed = false;
        if (!selectedRunId) {{
          await fetchSelectedEventsFallback("Generated event stream unavailable; using local events endpoint fallback.");
          return;
        }}
        if (!sseAvailable) {{
          await fetchSelectedEventsFallback("Generated EventSource is unavailable; using local events endpoint fallback.");
          return;
        }}
        setSseState("connecting", "Generated harness events only. No model execution was attempted. Provider calls remain disabled.", false);
        try {{
          const eventSource = new EventSource(`/api/harness/sse?run_id=${{encodeURIComponent(selectedRunId)}}`);
          activeEventSource = eventSource;
          eventSource.addEventListener("stream_started", () => {{
            if (eventSource !== activeEventSource) {{
              return;
            }}
            sseEvents = [];
            setSseState("streaming", "Generated harness events only. Not model token streaming. No provider streaming.", false);
          }});
          eventSource.addEventListener("harness_stage", (event) => {{
            if (eventSource !== activeEventSource) {{
              return;
            }}
            try {{
              const payload = JSON.parse(event.data || "{{}}");
              const stageEvent = eventFromSsePayload(payload);
              if (!stageEvent) {{
                throw new Error("Malformed generated stream event.");
              }}
              sseEvents.push(stageEvent);
              renderSseEvents();
            }} catch (parseError) {{
              closeActiveEventSource();
              fetchSelectedEventsFallback("Generated event stream returned malformed data; using local events endpoint fallback.");
            }}
          }});
          eventSource.addEventListener("stream_completed", () => {{
            if (eventSource !== activeEventSource) {{
              return;
            }}
            closeActiveEventSource();
            setSseState("completed", "Generated event stream completed. No model execution was attempted. Provider calls remain disabled.", false);
            if (sseEvents.length) {{
              renderSseEvents();
            }}
          }});
          eventSource.onerror = () => {{
            if (eventSource !== activeEventSource) {{
              return;
            }}
            closeActiveEventSource();
            fetchSelectedEventsFallback("Generated event stream unavailable; using local events endpoint fallback.");
          }};
        }} catch (error) {{
          closeActiveEventSource();
          await fetchSelectedEventsFallback("Generated event stream unavailable; using local events endpoint fallback.");
        }}
      }};

      const renderRunResponse = (run, options) => {{
        const shouldUpdateHistory = !options || options.updateHistory !== false;
        selectedRunId = run.run_id || "";
        const report = run.report_metadata_summary || {{}};
        setShellSelectedRunSurfaceState({{run_id: selectedRunId || "not returned"}});
        text("kora-selected-run-id", selectedRunId || "not returned");
        text("kora-composer-run-id", selectedRunId || "not returned");
        text("kora-run-request-id", run.request_id || selectedRequestId);
        text("kora-composer-request-id", run.request_id || selectedRequestId);
        text("kora-run-status", run.run_status || "unknown");
        text("kora-composer-run-status", run.run_status || "unknown");
        text("kora-run-event-count", run.event_count || (Array.isArray(run.generated_events) ? run.generated_events.length : 0));
        text("kora-run-model-execution-status", run.model_execution_status || "execution_not_connected");
        text("kora-run-provider-calls-enabled", run.provider_calls_enabled === true ? "true" : "false");
        text("kora-run-cloud-sync-enabled", run.cloud_sync_enabled === true ? "true" : "false");
        text("kora-run-file-export-enabled", report.file_export_enabled === true ? "true" : "false");
        text("kora-run-claim-boundary", run.claim_boundary || "Generated local harness output only. No model execution.");
        runError = "";
        setRetryState(false, "No selected-run error.");
        renderSelectedCounters(run.generated_counters, run.event_count || 0);
        renderSelectedComparison(run.comparison_summary, run.model_execution_status || "execution_not_connected");
        renderSelectedReportMetadata(run.report_metadata_summary);
        if (shouldUpdateHistory) {{
          addRunToHistory(run);
        }} else {{
          renderRunHistory();
        }}
      }};

      const runLocalHarness = async (requestId) => {{
        if (!requestById.has(requestId)) {{
          renderRunError("No approved request is selected.");
          return;
        }}
        selectedRequestId = requestId;
        lastApprovedRequestId = requestId;
        renderSelectedRequest();
        setRunLoading(true);
        setRetryState(false, "No selected-run error.");
        text("kora-run-status", "running");
        text("kora-composer-run-status", "running");
        text("kora-composer-request-id", requestId);
        text("kora-composer-run-id", "pending local harness response");
        text("kora-run-claim-boundary", "Local harness run requested for an approved request id only.");
        setShellSelectedRunSurfaceState({{
          run_id: "pending local harness response",
          timeline: "pending",
          counters: "pending",
          comparison: "pending",
          report: "pending"
        }});
        try {{
          const response = await fetch("/api/harness/run", {{
            method: "POST",
            headers: {{"Content-Type": "application/json"}},
            body: JSON.stringify({{request_id: requestId}})
          }});
          let payload;
          try {{
            payload = await response.json();
          }} catch (parseError) {{
            throw new Error("The local response could not be parsed.");
          }}
          if (!response.ok || payload.ok === false) {{
            throw new Error(payload.message || "Local harness run failed.");
          }}
          if (!payload.run_id || !payload.run_status) {{
            throw new Error("The local response was missing selected-run fields.");
          }}
          renderRunResponse(payload);
          await connectGeneratedEventStream();
        }} catch (error) {{
          const message = error instanceof TypeError ? "The local harness endpoint was unavailable." : (error && error.message ? error.message : "Local harness run failed.");
          renderRunError(message);
        }} finally {{
          setRunLoading(false);
        }}
      }};

      document.querySelectorAll("[data-kora-request-id]").forEach((button) => {{
        button.addEventListener("click", () => {{
          const requestId = button.getAttribute("data-kora-request-id") || "";
          if (requestById.has(requestId)) {{
            selectedRequestId = requestId;
            renderSelectedRequest();
          }}
        }});
      }});

      const runButton = document.getElementById("kora-run-local-harness-button");
      if (runButton) {{
        runButton.addEventListener("click", async () => {{
          await runLocalHarness(selectedRequestId);
        }});
      }}

      const composerRunButton = document.getElementById("kora-composer-run-local-harness-button");
      if (composerRunButton) {{
        composerRunButton.addEventListener("click", async () => {{
          await runLocalHarness(selectedRequestId);
        }});
      }}

      const retryButton = document.getElementById("kora-retry-last-approved-request-button");
      if (retryButton) {{
        retryButton.addEventListener("click", async () => {{
          if (!requestById.has(lastApprovedRequestId)) {{
            renderRunError("Retry is unavailable because no approved request has been selected.");
            return;
          }}
          await runLocalHarness(lastApprovedRequestId);
        }});
      }}

      const clearHistoryButton = document.getElementById("kora-clear-run-history-button");
      if (clearHistoryButton) {{
        clearHistoryButton.addEventListener("click", () => {{
          clearLocalRunHistory();
        }});
      }}

      renderSelectedRequest();
      setRetryState(false, "No selected-run error.");
      setShellSelectedRunSurfaceState({{
        run_id: "not run yet",
        timeline: "not loaded",
        counters: "not loaded",
        comparison: "not loaded",
        report: "not loaded"
      }});
      renderRunHistory();
      window.koraStudioAccessibilityState = {{
        get shell_state() {{ return getShellAccessibilityState(); }}
      }};
      window.koraStudioSelectedRunState = {{
        get selected_request_id() {{ return selectedRequestId; }},
        get selected_run_id() {{ return selectedRunId; }},
        get selected_run_record() {{ return runHistory.find((record) => record.run_id === selectedRunId) || null; }},
        get run_loading() {{ return runLoading; }},
        get run_error() {{ return runError; }},
        get last_approved_request_id() {{ return lastApprovedRequestId; }},
        get retry_available() {{ return retryAvailable; }},
        get run_history() {{ return runHistory.slice(); }},
        get run_history_limit() {{ return runHistoryLimit; }},
        get sse_available() {{ return sseAvailable; }},
        get sse_status() {{ return sseStatus; }},
        get sse_error() {{ return sseError; }},
        get sse_events() {{ return sseEvents.slice(); }},
        get sse_fallback_used() {{ return sseFallbackUsed; }},
        get selected_run_events() {{ return selectedRunEvents.slice(); }},
        get selected_run_counters() {{ return Object.assign({{}}, selectedRunCounters); }},
        get selected_run_comparison() {{ return Object.assign({{}}, selectedRunComparison); }},
        get selected_run_report_metadata() {{ return Object.assign({{}}, selectedRunReportMetadata); }}
      }};
      window.koraStudioScriptStatus = {{status: "ready", error: ""}};
    }})();
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
