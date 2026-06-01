"""Render helpers for the KORA Studio local preview details drawer."""

from __future__ import annotations


def render_right_details_drawer(
    *,
    runtime_name: str,
    runtime_detected: str,
    service_status: str,
    local_candidate_name: str,
    catalog_status: str,
    installed_status: str,
    installed_count: str,
    sample_request_id: str,
    sample_route: str,
    sample_validation: str,
    total_requests: str,
    baseline_model_calls: str,
    kora_model_calls: str,
    avoided_model_calls: str,
    report_viewer_status: str,
    report_source: str,
    report_file_export_enabled: str,
    report_file_written: str,
) -> str:
    """Render the right details drawer from server-prepared display values."""

    return f"""      <aside class=\"details-drawer-shell\" id=\"kora-details-drawer\" aria-label=\"KORA Studio right details drawer scaffold\" data-kora-component=\"right-details-drawer\" data-kora-keyboard-contract=\"details-drawer\" data-kora-mobile-drawer=\"right-overlay\" data-kora-drawer-state=\"closed\" data-kora-keyboard-trap-boundary=\"closed-inert-open-focus-managed\" aria-hidden=\"true\" tabindex=\"-1\" inert>
        <div class=\"drawer-header\">
          <div>
            <h2>Details</h2>
            <p class=\"subtitle\">Inspector · local preview</p>
          </div>
          <button class=\"drawer-close-button\" type=\"button\" id=\"kora-details-drawer-close\" aria-label=\"Close details drawer\" data-kora-keyboard-contract=\"details-drawer-close\" data-kora-drawer-close=\"true\">x</button>
        </div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"runtime-status\"><h3>Runtime status</h3><p>Local runtime: {runtime_name}</p><p>Runtime detected: {runtime_detected}</p><p>Service reachability: {service_status}</p><p>Model execution: not connected yet</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"selected-model\"><h3>Selected model</h3><p>Suggested estimate: {local_candidate_name}</p><p>Catalog candidate only; not installed unless detected.</p><p>Selection does not install or run a model.</p><p>Top selector: <code>Search or select open-source LLM</code></p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"catalog-vs-installed\"><h3>Catalog vs installed</h3><p>Catalog candidate: {local_candidate_name}</p><p>Catalog status: {catalog_status}</p><p>Installed detection: {installed_status}</p><p>Installed count: {installed_count}</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"route-trace\"><h3>Route trace</h3><p>Sample request: <code>{sample_request_id}</code></p><p>Expected route: {sample_route}</p><p>Validation: {sample_validation}</p><p>Generated harness events only.</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"generated-counters\"><h3>Generated counters</h3><p>Total requests: {total_requests}</p><p>Baseline model calls: {baseline_model_calls}</p><p>KORA model calls: {kora_model_calls}</p><p>Avoided model calls: {avoided_model_calls}</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"selected-run-surfaces\" data-kora-drawer-selected-run-coverage=\"timeline,counters,comparison,report-metadata\" data-kora-v1-1-drawer-selected-run-polish=\"primary-diagnostics\"><h3>Selected run surfaces</h3><p>Run id: <code id=\"kora-drawer-selected-run-id\">not run yet</code></p><p>Timeline: <span id=\"kora-drawer-selected-timeline-status\">not loaded</span></p><p>Counters: <span id=\"kora-drawer-selected-counters-status\">not loaded</span></p><p>Comparison: <span id=\"kora-drawer-selected-comparison-status\">not loaded</span></p><p>Report metadata: <span id=\"kora-drawer-selected-report-status\">not loaded</span></p><p>Drawer selected-run diagnostics mirror shell state for normal inspection: timeline availability, generated counters, local harness comparison, and report metadata preview.</p><p>Generated local harness output only. Not model token streaming. Not production telemetry. Not production cost evidence. Report metadata preview only. No file export or writing.</p></div>
        <div class=\"drawer-section-block\" data-kora-drawer-section=\"report-metadata\"><h3>Report metadata</h3><p>Report status: {report_viewer_status}</p><p>Report source: {report_source}</p><p>File export: {report_file_export_enabled}</p><p>File written: {report_file_written}</p></div>
        <div class=\"drawer-section-block drawer-boundary\" data-kora-drawer-section=\"claim-boundaries\" data-kora-drawer-boundary-coverage=\"provider,cloud,download,model-execution,report-export,private-scan,runtime-list\"><h3>Claim boundaries</h3><p>Local preview only.</p><p>No arbitrary prompt execution.</p><p>No model execution.</p><p>No provider calls.</p><p>No downloads.</p><p>No cloud sync.</p><p>No report file export or writing.</p><p>No private model directory scanning.</p><p>No runtime model list commands.</p></div>
      </aside>"""
