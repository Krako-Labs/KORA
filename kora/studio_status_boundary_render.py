"""Render KORA Studio status and boundary display fragments."""

from __future__ import annotations


def render_shell_boundary_strip() -> str:
    """Render the shell-first local-only boundary strip."""

    return """          <div class=\"shell-boundary-strip\" data-kora-component=\"boundary-strip\" data-kora-shell-local-only-boundary=\"v1.0\" data-kora-shell-boundary-coverage=\"provider,cloud,download,model-execution,report-export\">
            <div class=\"shell-boundary-pills\">
              <span class=\"shell-pill cyan\">Local preview only</span>
              <span class=\"shell-pill\">Provider calls disabled</span>
              <span class=\"shell-pill\">Cloud sync disabled</span>
              <span class=\"shell-pill\">Downloads disabled</span>
              <span class=\"shell-pill amber\">Model execution not connected yet</span>
              <span class=\"shell-pill\">Report export disabled</span>
            </div>
            <p>Shell-first boundary: approved local harness requests only. No arbitrary prompt execution, no provider calls, no cloud sync, no downloads, no model execution, and no report file export or writing.</p>
          </div>"""


def render_launch_local_status_section(*, section_order_items: str) -> str:
    """Render the launch/local-only status section."""

    return f"""    <section aria-label=\"Launch Local-only Status\" class=\"section-spaced\">
      <h2>Launch / Local-only Status</h2>
      <div class=\"grid\">
        <div class=\"status-card card\"><h3>Server</h3><p class=\"status-value\">Server: local</p><p>Bound to the local Studio skeleton.</p></div>
        <div class=\"status-card card\"><h3>Provider Calls</h3><p class=\"status-value disabled\">Provider calls: disabled</p><p>No remote provider requests are made.</p></div>
        <div class=\"status-card card\"><h3>Cloud Sync</h3><p class=\"status-value disabled\">Cloud sync: disabled</p><p>No cloud sync is performed.</p></div>
        <div class=\"status-card card\"><h3>Model Runtime</h3><p class=\"status-value disabled\">Model/runtime integration: not connected</p><p>Future runtime work must distinguish physically runnable local models from workflow-usable models.</p></div>
        <div class=\"status-card card\"><h3>Browser Launch</h3><p class=\"status-value\">Browser launch: available</p><p>The CLI opens the local page by default; use <code>--no-browser</code> to suppress it.</p></div>
        <div class=\"status-card card\"><h3>Ollama</h3><p class=\"status-value disabled\">Ollama integration: not connected</p><p>No Ollama model calls happen here.</p></div>
      </div>
      <div class=\"card card-spaced\"><h3>First-run order</h3><ol>{section_order_items}</ol></div>
    </section>"""


def render_kora_boost_boundary_section() -> str:
    """Render the KORA Boost claim-boundary section."""

    return """      <section>
        <h2>KORA Boost Boundary</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Standard Mode</h3><p>Standard Mode sends every step to the model.</p><p>In this preview, model execution is not connected.</p></div>
          <div class=\"card\"><h3>KORA Boost</h3><p>KORA Boost routes deterministic and structured tasks to CPU/local fast paths first.</p><p>Larger-model workflows may become more practical when deterministic work avoids the model path.</p></div>
          <div class=\"card\"><h3>Boundary</h3><p>KORA does not remove model memory requirements.</p><p>Provider/cloud routes are disabled by default.</p></div>
        </div>
      </section>"""
