"""JavaScript asset loader for the KORA Studio local preview."""

from __future__ import annotations

from importlib import resources

STUDIO_JAVASCRIPT_SOURCE_PACKAGE = "kora"
STUDIO_JAVASCRIPT_SOURCE_PATH = "studio_assets/studio.js"


def render_studio_javascript() -> str:
    """Load the package-controlled Studio JavaScript source asset."""

    return (
        resources.files(STUDIO_JAVASCRIPT_SOURCE_PACKAGE)
        .joinpath(STUDIO_JAVASCRIPT_SOURCE_PATH)
        .read_text(encoding="utf-8")
    )
