"""Render helpers for KORA Studio selected-run preview panels."""

from __future__ import annotations


def render_selected_run_summary_panel(*, selector_preview_id: str) -> str:
    """Render the composer selected-run summary panel."""

    return f"""          <div class=\"composer-run-summary\" id=\"kora-composer-selected-run-summary\" data-kora-component=\"selected-run-summary\" aria-live=\"polite\">
            <strong>Composer selected-run summary</strong>
            <span>Request: <code id=\"kora-composer-request-id\">{selector_preview_id}</code></span>
            <span>Status: <code id=\"kora-composer-run-status\">not_started</code></span>
            <span>Run id: <code id=\"kora-composer-run-id\">not run yet</code></span>
            <span>Boundary: approved local harness request only</span>
          </div>"""


def render_selected_run_state_panel() -> str:
    """Render the selected-run state panel."""

    return """        <div class=\"grid grid-spaced\" data-kora-diagnostic-hierarchy=\"secondary\">
          <div class=\"card secondary-diagnostic-card\"><h3>Selected run state</h3><p>Secondary diagnostic mirror. Generated local harness output only.</p><div class=\"run-state\" id=\"kora-selected-run-state\" aria-live=\"polite\"><p>Status: <span id=\"kora-run-status\">not_started</span></p><p>Run id: <code id=\"kora-selected-run-id\">not run yet</code></p><p>Request id: <code id=\"kora-run-request-id\">not run yet</code></p><p>Event count: <span id=\"kora-run-event-count\">0</span></p><p>Model execution status: <span id=\"kora-run-model-execution-status\">not_connected</span></p><p>Provider calls: <span id=\"kora-run-provider-calls-enabled\">false</span></p><p>Cloud sync: <span id=\"kora-run-cloud-sync-enabled\">false</span></p><p>File export: <span id=\"kora-run-file-export-enabled\">false</span></p><p>Claim boundary: <span id=\"kora-run-claim-boundary\">No run has been generated yet.</span></p></div></div>
          <div class=\"card secondary-diagnostic-card\"><h3>Interactive run boundary</h3><p>Secondary diagnostic boundary.</p><p>Model-needed boundary returns <code>execution_not_connected</code>.</p><p>No model execution was attempted.</p><p>Provider calls remain disabled.</p><p>No downloads.</p><p>Selected run state is local browser memory only.</p></div>
        </div>"""


def render_selected_run_detail_panels() -> str:
    """Render selected-run event stream, timeline, counters, comparison, and report panels."""

    return """        <div class=\"grid grid-spaced\" data-kora-diagnostic-hierarchy=\"secondary\">
          <div class=\"card secondary-diagnostic-card\" data-kora-component=\"generated-event-stream-status\" data-kora-keyboard-contract=\"secondary-generated-event-stream\"><h3>Generated Event Stream</h3><p>Secondary diagnostic stream detail. Generated harness events only.</p><p>Not model token streaming.</p><p>No provider streaming.</p><p>No model execution.</p><p>Fallback to local events endpoint available.</p><p>Status: <span id=\"kora-sse-status\">idle</span></p><p>Fallback used: <span id=\"kora-sse-fallback-used\">false</span></p><p id=\"kora-sse-error\">No generated event stream error.</p></div>
        </div>
        <div class=\"card card-spaced secondary-diagnostic-card\" data-kora-component=\"selected-run-event-timeline\" data-kora-keyboard-contract=\"secondary-event-timeline\" data-kora-diagnostic-hierarchy=\"secondary\"><h3>Selected Run Event Timeline</h3><p>Secondary diagnostic timeline. Generated local harness events only. Not model token streaming. No model execution. No provider calls. No downloads.</p><p>Events are fetched from <code>GET /api/harness/events?run_id=&lt;id&gt;</code> after a successful approved local harness run.</p><p id=\"kora-selected-events-status\">No selected run events loaded yet.</p></div>
        <div class=\"grid\" id=\"kora-selected-run-events\" aria-live=\"polite\"></div>
        <div class=\"grid grid-spaced\" data-kora-diagnostic-hierarchy=\"secondary\">
          <div class=\"card secondary-diagnostic-card\" data-kora-component=\"selected-run-counters\" data-kora-keyboard-contract=\"secondary-run-counters\"><h3>Selected Run Counters</h3><p>Secondary diagnostic counters. Generated local harness counters only. Not production telemetry. No model execution. No provider calls. No cost or energy claim.</p><p id=\"kora-selected-counters-status\">Run an approved local harness request to view selected-run counters.</p></div>
          <div class=\"card secondary-diagnostic-card\" data-kora-component=\"selected-run-comparison\" data-kora-keyboard-contract=\"secondary-run-comparison\"><h3>Selected Run: Standard Mode vs KORA Boost</h3><p>Secondary diagnostic comparison. Comparison is generated from approved local harness output. This is not production cost evidence. This does not execute a model.</p><p>Model-needed boundaries remain <code>execution_not_connected</code>.</p><p id=\"kora-selected-comparison-status\">Run an approved local harness request to view selected-run comparison.</p></div>
        </div>
        <div class=\"grid\" id=\"kora-selected-run-counters\" aria-live=\"polite\"></div>
        <div class=\"grid\" id=\"kora-selected-run-comparison\" aria-live=\"polite\"></div>
        <div class=\"card card-spaced secondary-diagnostic-card\" data-kora-component=\"selected-run-report-metadata\" data-kora-keyboard-contract=\"secondary-report-metadata\" data-kora-diagnostic-hierarchy=\"secondary\"><h3>Selected Run Report Metadata</h3><p>Secondary diagnostic report metadata. Report metadata preview only. No file export. No file writing. Generated local harness output only.</p><p>No model execution. No provider calls. No cloud sync. Not production evidence.</p><p id=\"kora-selected-report-status\">Run an approved local harness request to view selected-run report metadata.</p></div>
        <div class=\"grid\" id=\"kora-selected-run-report-metadata\" aria-live=\"polite\"></div>"""


def render_selected_run_panels() -> str:
    """Render all selected-run helper-owned panels for direct marker tests."""

    return f"{render_selected_run_state_panel()}\n{render_selected_run_detail_panels()}"
