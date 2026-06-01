"""Render helpers for KORA Studio local harness request panels."""

from __future__ import annotations


def render_local_harness_selector_item(
    *,
    request_id: str,
    input_text: str,
    route_class: str,
    model_needed: str,
) -> str:
    """Render one approved local harness selector option from escaped display strings."""

    return (
        '<div class="card">'
        "<h3>Selector option</h3>"
        f'<button class="request-option" type="button" data-kora-keyboard-selectable-request="true" aria-pressed="false" aria-current="false" aria-label="Select approved local harness request {request_id}" data-kora-request-id="{request_id}">'
        f"{request_id}"
        "</button>"
        f"<p>{input_text}</p>"
        f"<p>Route class: {route_class}</p>"
        f"<p>Model-needed boundary: {model_needed}</p>"
        '<p><span class="badge">Approved local harness requests only</span></p>'
        "</div>"
    )


def render_local_harness_trigger_item(
    *,
    request_id: str,
    input_text: str,
    task_family: str,
    route_class: str,
    model_needed: str,
) -> str:
    """Render one local harness trigger reference card from escaped display strings."""

    return (
        '<div class="card">'
        "<h3>Run Local Harness</h3>"
        f"<p><code>{request_id}</code></p>"
        f"<p>{input_text}</p>"
        f"<p>Family: {task_family}</p>"
        f"<p>Route: {route_class}</p>"
        f"<p>Model-needed boundary: {model_needed}</p>"
        '<p><span class="badge">Approved deterministic sample requests only</span></p>'
        "</div>"
    )


def render_local_harness_request_selector_panels(
    *,
    selector_preview_id: str,
    selector_preview_text: str,
    selector_preview_route: str,
    selector_preview_model_needed: str,
    selector_items_html: str,
) -> str:
    """Render approved request selector panels from escaped strings and selector item slot HTML."""

    return f"""        <div class=\"grid grid-spaced\">
          <div class=\"card\" data-kora-component=\"approved-request-selector\"><h3>Approved Request Selector</h3><p>Interactive approved request selector.</p><p>Approved local harness requests only.</p><p>Approved request only.</p><p>No arbitrary prompt execution.</p><p>No model execution.</p><p>No provider calls.</p><p>No downloads.</p><p>Local deterministic harness data only.</p></div>
          <div class=\"card\"><h3>Selected request preview</h3><p><code id=\"kora-selected-request-id\">{selector_preview_id}</code></p><p id=\"kora-selected-request-text\">{selector_preview_text}</p><p>Route class: <span id=\"kora-selected-request-route\">{selector_preview_route}</span></p><p>Model-needed boundary: <span id=\"kora-selected-request-model-needed\">{selector_preview_model_needed}</span></p><p>Selector state is browser-local in-memory page state only.</p></div>
          <div class=\"card\"><h3>Run Local Harness</h3><p><span class=\"badge\">Approved request only</span></p><button class=\"action-button\" type=\"button\" id=\"kora-run-local-harness-button\" aria-describedby=\"kora-run-local-harness-boundary\">Run Local Harness</button><p id=\"kora-run-local-harness-boundary\">Calls <code>POST /api/harness/run</code> with the selected approved <code>request_id</code> only.</p><p>No arbitrary prompt text is sent.</p></div>
        </div>
        <div class=\"grid grid-spaced\">{selector_items_html}</div>"""


def render_local_harness_trigger_reference_panels(*, trigger_items_html: str) -> str:
    """Render local harness trigger reference panels from trigger item slot HTML."""

    return f"""        <div class=\"grid grid-spaced\">
          <div class=\"card\"><h3>Run Local Harness action state</h3><p><span class=\"badge\">Run Local Harness</span></p><p>The browser button calls only the local harness run endpoint for an approved request id.</p><p>Use <code>POST /api/harness/run</code> with an approved <code>request_id</code>.</p><p>Generated harness events only.</p></div>
          <div class=\"card\"><h3>Trigger boundary</h3><p>Approved deterministic sample requests only.</p><p>No arbitrary prompt execution.</p><p>No model execution.</p><p>No provider calls.</p><p>No downloads.</p><p>This is local preview/demo data, not production evidence.</p></div>
          <div class=\"card\"><h3>Result surfaces</h3><p><code>GET /api/harness/run/&lt;run_id&gt;</code></p><p><code>GET /api/harness/events?run_id=&lt;id&gt;</code></p><p><code>GET /api/harness/sse?run_id=&lt;id&gt;</code></p><p>Model-needed boundary returns <code>execution_not_connected</code>.</p></div>
        </div>
        <div class=\"grid grid-spaced\">{trigger_items_html}</div>"""
