"""Render KORA Studio local harness display fragments."""

from __future__ import annotations


def render_local_harness_preview_section(
    *,
    local_harness_status_text: str,
    local_harness_event_source: str,
    local_harness_run_trigger: str,
    local_harness_request_count: str,
    sample_request_id: str,
    sample_input: str,
    sample_family: str,
    sample_route: str,
    sample_validation: str,
    sample_model_needed: str,
    local_harness_boundary: str,
    request_selector_html: str,
    selected_run_state_html: str,
    run_state_history_html: str,
    selected_run_detail_panels_html: str,
    trigger_reference_html: str,
    local_harness_request_items: str,
    local_harness_event_items: str,
    local_harness_timeline_items: str,
    local_harness_counter_items: str,
) -> str:
    """Render local harness preview display cards and slots."""

    return f"""      <section>
        <h2>Local Harness Preview</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Harness status</h3><p>{local_harness_status_text}</p><p>Event source: {local_harness_event_source}</p><p>Run trigger: {local_harness_run_trigger}</p><p>Available sample requests: {local_harness_request_count}</p></div>
          <div class=\"card\"><h3>Sample request</h3><p><code>{sample_request_id}</code></p><p>{sample_input}</p><p>Family: {sample_family}</p><p>Expected route: {sample_route}</p><p>Validation: {sample_validation}</p><p>Model needed: {sample_model_needed}</p></div>
          <div class=\"card\"><h3>Boundary</h3><p>{local_harness_boundary}</p><p>Model-needed boundaries do not execute models in this milestone.</p><p>No provider call, download, or cloud sync is connected.</p></div>
        </div>
{request_selector_html}
{selected_run_state_html}
{run_state_history_html}
{selected_run_detail_panels_html}
{trigger_reference_html}
        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\"><h3>Available local deterministic sample requests</h3><ul>{local_harness_request_items}</ul></div>
          <div class=\"card\"><h3>Harness event stages</h3><ul>{local_harness_event_items}</ul></div>
        </div>
        <div class=\"card\" style=\"margin-top: 16px;\"><h3>Generated Event Timeline</h3><p>Generated local harness events only. Not model token streaming. No model execution. No provider output.</p></div>
        <div class=\"grid\">{local_harness_timeline_items}</div>
        <div class=\"card\" style=\"margin-top: 16px;\"><h3>Generated Counters</h3><p>Generated counters come from local deterministic harness output only. No cost or energy conversion is performed.</p></div>
        <div class=\"grid\">{local_harness_counter_items}</div>
      </section>"""


def render_execution_viewer_section(
    *,
    execution_status: str,
    execution_schema_count: str,
    execution_event_count: str,
    execution_boundary: str,
    execution_event_items: str,
) -> str:
    """Render the fixture/mock execution viewer section."""

    return f"""      <section>
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
      </section>"""


def render_standard_vs_kora_section(
    *,
    standard_vs_kora_status: str,
    standard_route_summary: str,
    kora_route_summary: str,
    standard_vs_kora_boundary: str,
    standard_vs_kora_metric_items: str,
) -> str:
    """Render the Standard Mode versus KORA Boost comparison section."""

    return f"""      <section>
        <h2>Standard Mode vs KORA Boost</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Comparison status</h3><p>{standard_vs_kora_status}</p><p>Local deterministic harness comparison.</p><p>No model execution occurs.</p></div>
          <div class=\"card\"><h3>Standard Mode</h3><p>{standard_route_summary}</p><p>Model call counted in fixture baseline: 1</p></div>
          <div class=\"card\"><h3>KORA Boost</h3><p>{kora_route_summary}</p><p>Model call counted in fixture KORA path: 0</p></div>
          <div class=\"card\"><h3>Local Harness Comparison boundary</h3><p>{standard_vs_kora_boundary}</p><p>Comparison is generated from local deterministic harness output.</p><p>This is not production cost evidence.</p><p>This does not execute a model.</p><p>No cost or energy claim is made.</p></div>
        </div>
        <div class=\"grid\">{standard_vs_kora_metric_items}</div>
      </section>"""


def render_report_viewer_placeholder_section(
    *,
    report_viewer_status: str,
    report_title: str,
    report_source: str,
    report_sample_run_id: str,
    report_sample_request_id: str,
    report_event_count: str,
    report_comparison_status: str,
    report_export_status: str,
    report_export_label: str,
    report_file_export_enabled: str,
    report_file_written: str,
    report_export_reason: str,
    report_export_boundary: str,
    report_boundary: str,
    report_path_display: str,
    report_fixture_path: str,
    report_sections: str,
    report_warnings: str,
    report_counter_items: str,
) -> str:
    """Render the report viewer placeholder section."""

    return f"""      <section>
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
      </section>"""
