"""Render helpers for KORA Studio legacy compatibility scaffolds."""

from __future__ import annotations


def render_legacy_preview_opening() -> str:
    """Render the collapsed legacy preview opening wrapper."""

    return """  <details class=\"legacy-preview\" aria-label=\"Detailed local preview compatibility scaffolds\" data-kora-component=\"legacy-compatibility-reference\" data-kora-legacy-preview-mode=\"compatibility-collapsed\" data-kora-legacy-preview-default=\"collapsed\" data-kora-legacy-preview-role=\"developer-compatibility-scaffold\" data-kora-v1-1-legacy-secondary=\"developer-reference-only\" data-kora-v1-1-legacy-first-run-required=\"false\">
    <summary aria-label=\"Open legacy detailed preview compatibility scaffold\">
      <div class=\"legacy-preview-summary\">
        <div><strong>Legacy detailed preview compatibility scaffold</strong><span>Collapsed by default. The final shell and Details drawer above are the primary local preview; this developer reference is not required for first-run understanding.</span></div>
        <span class=\"legacy-preview-summary-badge\">Developer reference only</span>
      </div>
    </summary>
    <p class=\"legacy-preview-summary\" data-kora-v1-1-legacy-boundary=\"secondary-reference-only\">This compatibility scaffold remains local-only and secondary. It does not enable model execution, provider calls, downloads, cloud sync, report export, or report writing.</p>
    <div class=\"legacy-preview-content\">"""
