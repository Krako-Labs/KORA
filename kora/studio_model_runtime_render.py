"""Render KORA Studio model, catalog, and runtime display fragments."""

from __future__ import annotations


def render_model_selector_option(
    *,
    display_name: str,
    model_id: str,
    candidate_type: str,
    estimated_memory_gb: str,
    installed_locally: str,
) -> str:
    """Render one compact catalog-only model selector option."""

    return (
        '<div class="model-selector-option" data-kora-model-option="true" '
        'data-kora-model-option-state="catalog-estimate-only" aria-selected="false" tabindex="0">'
        f"<strong>{display_name}</strong>"
        "<span>Catalog estimate option; not installed or executed by selection.</span>"
        f"<span>{model_id}</span>"
        f"<span>{candidate_type}</span>"
        f"<span>{estimated_memory_gb} GB estimate</span>"
        f"<span>Installed: {installed_locally}</span>"
        "</div>"
    )


def render_system_profile_section(
    *,
    os_name: str,
    machine: str,
    memory_text: str,
    memory_status: str,
    ollama_status: str,
    llama_cpp_status: str,
) -> str:
    """Render local system profile display cards."""

    return f"""      <section>
        <h2>Your Computer</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>System Profile</h3><p>OS: {os_name}</p><p>Machine: {machine}</p><p>Memory: {memory_text} ({memory_status})</p></div>
          <div class=\"card\"><h3>Local Runtime Detection</h3><p>Ollama: {ollama_status}</p><p>llama.cpp: {llama_cpp_status}</p><p>No runtime APIs are called by this preview.</p></div>
        </div>
      </section>"""


def render_model_capability_section(
    *,
    recommended_tier: str,
    physical_notes: str,
    workflow_notes: str,
    claim_boundary: str,
) -> str:
    """Render model capability estimate display cards."""

    return f"""      <section>
        <h2>Model Capability Estimate</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Estimated local model tier</h3><p>{recommended_tier}</p><p>{physical_notes}</p></div>
          <div class=\"card\"><h3>Workflow feasibility</h3><p>{workflow_notes}</p><p>{claim_boundary}</p></div>
        </div>
      </section>"""


def render_runtime_status_section(
    *,
    runtime_name: str,
    runtime_detected: str,
    service_status: str,
    service_url: str,
    service_boundary: str,
    installed_enabled: str,
    installed_method: str,
) -> str:
    """Render runtime status display cards."""

    return f"""      <section>
        <h2>Runtime Status</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Runtime detected</h3><p>{runtime_name}: {runtime_detected}</p><p>Runtime executable detection is local-only.</p></div>
          <div class=\"card\"><h3>Service reachability</h3><p>Runtime reachable: {service_status}</p><p>Service URL: {service_url}</p><p>Service reachability is a localhost-only check.</p><p>No model execution occurs during this check.</p><p>{service_boundary}</p></div>
          <div class=\"card\"><h3>Installed model detection</h3><p>Detection enabled: {installed_enabled}</p><p>Detection method: {installed_method}</p><p>Installed model detection is not connected yet.</p></div>
        </div>
      </section>"""


def render_catalog_installed_section(
    *,
    catalog_status: str,
    local_candidate_name: str,
    local_candidate_note: str,
    workflow_candidate_name: str,
    workflow_candidate_note: str,
    installed_status: str,
    installed_count: str,
    catalog_boundary: str,
    installed_boundary: str,
) -> str:
    """Render catalog versus installed-local display cards."""

    return f"""      <section>
        <h2>Catalog vs Installed</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Catalog examples</h3><p>{catalog_status}</p><p>Catalog examples are curated examples, not installed models.</p></div>
          <div class=\"card\"><h3>Physically runnable local candidates</h3><p>{local_candidate_name}</p><p>{local_candidate_note}</p></div>
          <div class=\"card\"><h3>Larger-model workflow candidates</h3><p>{workflow_candidate_name}</p><p>{workflow_candidate_note}</p></div>
          <div class=\"card\"><h3>Installed locally</h3><p>Installed model detection: {installed_status}</p><p>Installed count: {installed_count}</p><p>No private model directories are scanned.</p><p>No runtime model list command is called by default.</p></div>
          <div class=\"card\"><h3>Catalog boundary</h3><p>{catalog_boundary}</p><p>{installed_boundary}</p></div>
        </div>
      </section>"""


def render_setup_guidance_section(
    *,
    setup_guidance_status: str,
    setup_guidance_url: str,
    setup_guidance_boundary: str,
) -> str:
    """Render setup guidance display cards."""

    return f"""      <section>
        <h2>Setup Guidance</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Guidance status</h3><p>{setup_guidance_status}</p><p>Disabled actions point to guidance, not to an active installer.</p><p><code>{setup_guidance_url}</code></p></div>
          <div class=\"card\"><h3>Setup boundary</h3><p>No model is downloaded.</p><p>No model is executed.</p><p>No provider call is made.</p><p>Provider/cloud routes are disabled by default.</p></div>
          <div class=\"card\"><h3>Runtime readiness</h3><p>Runtime executable detection is not model execution readiness.</p><p>Catalog examples are not installed models.</p><p>{setup_guidance_boundary}</p></div>
        </div>
      </section>"""


def render_disabled_actions_section(
    *,
    local_download_label: str,
    local_download_reason: str,
    local_run_label: str,
    local_run_reason: str,
    local_action_boundary: str,
) -> str:
    """Render disabled download/run action display cards."""

    return f"""      <section>
        <h2>Disabled Download/Run Actions</h2>
        <div class=\"grid\">
          <div class=\"card\"><h3>Download action</h3><p><span class=\"badge\">{local_download_label}</span></p><p>{local_download_reason}</p><p>Download remains disabled until explicitly connected.</p></div>
          <div class=\"card\"><h3>Run action</h3><p><span class=\"badge\">{local_run_label}</span></p><p>{local_run_reason}</p><p>Run remains disabled until explicitly connected.</p></div>
          <div class=\"card\"><h3>Action boundary</h3><p>Download and run actions remain disabled.</p><p>{local_action_boundary}</p><p>No install, download, or model execution action is active in this preview.</p></div>
        </div>
      </section>"""
