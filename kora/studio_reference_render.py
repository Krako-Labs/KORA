"""Render helpers for KORA Studio local preview reference panels."""

from __future__ import annotations


def render_endpoint_panel() -> str:
    """Render static local endpoint reference panels."""

    return """      <section>
        <h2>Endpoint Panel</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3><a href=\"/health\">/health</a></h3><p>Returns local health status JSON for the preview server.</p></div>
          <div class=\"card\"><h3><a href=\"/status\">/status</a></h3><p>Returns local preview status, system profile, model capability estimate, KORA Boost copy, docs paths, and fixture paths.</p></div>
          <div class=\"card\"><h3>/api/harness/run</h3><p>POST accepts only approved local deterministic sample request IDs and returns generated local harness events. Arbitrary prompt execution is not connected.</p></div>
          <div class=\"card\"><h3>/api/harness/run/&lt;run_id&gt;</h3><p>GET returns an in-memory local harness run record if it exists. No persistence, provider call, download, or model execution is connected.</p></div>
          <div class=\"card\"><h3>/api/harness/events?run_id=&lt;id&gt;</h3><p>GET returns generated harness events for an existing local run. This is not SSE, not model token streaming, and not model output.</p></div>
          <div class=\"card\"><h3>/api/harness/sse?run_id=&lt;id&gt;</h3><p>GET streams generated harness events as Server-Sent Events. It streams no model tokens, provider output, or model output.</p></div>
        </div>
      </section>"""


def render_limitations_panel() -> str:
    """Render static local preview limitation panels."""

    return """      <section>
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
      </section>"""


def render_local_references_panel(*, docs_path: str, fixtures_path: str) -> str:
    """Render local documentation and fixture references from escaped display paths."""

    return f"""      <section>
        <h2>Local References</h2>
        <ul>
          <li><code>{docs_path}</code></li>
          <li><code>{fixtures_path}</code></li>
        </ul>
      </section>"""


def render_reference_panels(*, docs_path: str, fixtures_path: str) -> str:
    """Render low-risk static reference panels for the legacy preview."""

    return "\n\n".join(
        [
            render_endpoint_panel(),
            render_limitations_panel(),
            render_local_references_panel(docs_path=docs_path, fixtures_path=fixtures_path),
        ]
    )
