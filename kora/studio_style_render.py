"""CSS asset loader for the KORA Studio local preview."""

from __future__ import annotations

from importlib import resources

STUDIO_CSS_SOURCE_PACKAGE = "kora"
STUDIO_CSS_SOURCE_PATH = "studio_assets/studio.css"


def render_studio_css() -> str:
    """Load the package-controlled Studio CSS source asset."""

    return (
        resources.files(STUDIO_CSS_SOURCE_PACKAGE)
        .joinpath(STUDIO_CSS_SOURCE_PATH)
        .read_text(encoding="utf-8")
    )
