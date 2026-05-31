"""Render helpers for KORA Studio local run state and history panels."""

from __future__ import annotations


def render_retry_error_state_panels(*, selector_preview_id: str) -> str:
    """Render retry and error panels from an escaped approved request id."""

    return f"""        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\" data-kora-component=\"retry-error-state\"><h3>Selected Run Error State</h3><p id=\"kora-run-error-state\">No selected-run error.</p><p>Retry uses the last approved request only.</p><p>No model execution was attempted.</p><p>Provider calls remain disabled.</p><p>No downloads are connected.</p></div>
          <div class=\"card\"><h3>Retry Last Approved Request</h3><p>Last approved request: <code id=\"kora-last-approved-request-id\">{selector_preview_id}</code></p><p>Retry available: <span id=\"kora-retry-available\">false</span></p><button class=\"action-button\" type=\"button\" id=\"kora-retry-last-approved-request-button\" disabled>Retry Last Approved Request</button><p>Retry calls only <code>POST /api/harness/run</code> with the last approved <code>request_id</code>.</p><p>No arbitrary prompt execution.</p></div>
        </div>"""


def render_local_run_history_panels() -> str:
    """Render browser-local run history panels and the dynamic history container."""

    return """        <div class=\"grid\" style=\"margin-top: 16px;\">
          <div class=\"card\" data-kora-component=\"run-history\"><h3>Local Run History</h3><p>Browser-local run history.</p><p>Page-memory only.</p><p>Clears on refresh.</p><p>Active selected run: <code id=\"kora-active-history-run-id\">none</code></p><p>History cards show compact counters from generated harness output only.</p><p>Local deterministic harness output only.</p><p>No model execution. No provider calls. No downloads.</p><p>History count: <span id=\"kora-run-history-count\">0</span></p><p id=\"kora-run-history-status\">Run an approved local harness request to add browser-local history.</p></div>
          <div class=\"card\"><h3>Clear Local Run History</h3><button class=\"action-button\" type=\"button\" id=\"kora-clear-run-history-button\">Clear Local Run History</button><p>Clears browser-local preview state only.</p><p>Resets selected-run UI, selected events, selected counters, selected comparison, selected report metadata, and page-memory history.</p><p>Does not remove server run records, reports, files, backend records, or generated harness endpoints.</p><p>No persistence, no cloud sync, no file export, no file writing, and no backend delete call.</p></div>
        </div>
        <div class=\"grid\" id=\"kora-local-run-history\" aria-live=\"polite\"></div>"""


def render_run_state_history_panels(*, selector_preview_id: str) -> str:
    """Render retry, error, and browser-local history panels."""

    return "\n".join(
        [
            render_retry_error_state_panels(selector_preview_id=selector_preview_id),
            render_local_run_history_panels(),
        ]
    )
