# KORA README v2 visual assets

This directory contains PNG presentation assets used by the root README.

- `kora-original-horizontal-logo.png`: original KORA logo supplied by the project owner, preserved without redesign.
- `kora-readme-hero.png`: landscape composition using that original logo, with dark-navy background and descriptive typography.
- `kora-execution-control-diagram.png`: derived from the existing public `../kora-execution-control-overview.png`. The original diagram's top internal headline was cropped, while its model-first and KORA-controlled paths remain unchanged. Plain-text KORA marks the upper left, with a small original emblem at the lower right. The section heading and caption remain *outside* the bitmap in the README.

These are presentation graphics, not benchmark evidence. Documentation claims must continue to follow [the claim registry](../../claims/kora-claim-registry.md). The logo artwork was supplied by the project owner; its inclusion should not be read as an independent third-party license grant.

The PNG assets intentionally avoid SVG dependence in the root README. Keep Markdown captions separate and preserve whitespace around each image block.

The root README uses conventional CI, license, Python and arXiv badges linked to their sources. Badges are not PNG illustrations and are rendered using the official GitHub Actions badge endpoint and Shields.io.
