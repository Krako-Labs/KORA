"""Render helpers for the KORA Studio local preview shell."""

from __future__ import annotations


def render_shell_layout(
    *,
    local_candidate_name: str,
    local_candidate_id: str,
    local_candidate_type: str,
    local_candidate_memory: str,
    local_candidate_installed: str,
    model_selector_count: int,
    model_selector_items: str,
    composer_html: str,
    details_drawer_html: str,
    legacy_preview_html: str,
) -> str:
    """Render the final local preview shell around extracted content slots."""

    return f"""
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
{composer_html}
{details_drawer_html}
    </div>
  </div>
{legacy_preview_html}"""
