# KORA Studio v1.9 CSS Asset Source File Migration Report

## Status

KORA Studio v1.9 is complete as a narrow local preview asset-source migration.

v1.9 keeps the existing CSS-only route:

```text
/studio-assets/studio.css
```

The route remains allowlisted and still serves the CSS through `render_studio_css()`. The source behind that helper is now a package-controlled first-party CSS file at `kora/studio_assets/studio.css`, rather than an embedded Python triple-quoted CSS template.

## Source Location Decision

The safest migration step is a package-controlled source file inside the `kora` package:

```text
kora/studio_assets/studio.css
```

This keeps the asset source under version control and package ownership. It does not create a filesystem-backed static directory server, does not serve from the project root, and does not use user-provided paths.

## Implemented Surface

- `GET /studio-assets/studio.css`
- `Content-Type: text/css; charset=utf-8`
- `Cache-Control: no-store`
- CSS source file: `kora/studio_assets/studio.css`
- CSS loader: `render_studio_css()`
- root preview references `/studio-assets/studio.css`
- inline JavaScript remains in the root preview
- no JavaScript static asset route
- no wildcard static route
- no directory listing
- no arbitrary filesystem serving

## Route Boundary

Allowed:

- `/studio-assets/studio.css`

Rejected:

- unknown asset names
- `/studio-assets`
- `/studio-assets/`
- traversal paths containing `..`
- encoded traversal
- double-encoded traversal
- backslash traversal
- double-slash absolute-path shaped requests under the asset namespace

Rejected responses use claim-safe JSON and do not expose local filesystem paths.

## Packaging Boundary

`pyproject.toml` includes the Studio CSS source as package data:

```toml
[tool.setuptools.package-data]
kora = ["studio_assets/*.css"]
```

This preserves a package-owned asset source without adding frontend build tooling or runtime dependencies.

## Validation Results

Final validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed

Live smoke check:

- `python3 -m kora studio --no-browser`: started local preview server
- `python3 scripts/check_kora_studio_preview.py`: passed
- server stopped cleanly

Live smoke coverage includes:

- `/health`
- `/status`
- `/api/harness/run`
- `/api/harness/run/<run_id>`
- `/api/harness/events?run_id=<id>`
- `/api/harness/sse?run_id=<id>`
- `/studio-assets/studio.css`
- `/`

## Claim Boundaries Preserved

- KORA Studio remains local preview/demo readiness only.
- KORA Studio is not production-ready.
- KORA Studio is not an LM Studio replacement.
- Generated harness data remains local deterministic preview data.
- No arbitrary prompt execution was added.
- No model execution was added.
- No provider calls were added.
- No model downloads were added.
- No cloud sync was added.
- No private model directory scanning was added.
- No runtime model list commands were added.
- No report export or file writing was added.
- No external network behavior was added.
- No external assets or CDN dependencies were added.
- No production telemetry claim was added.
- No production cost evidence claim was added.
- No production cost reduction claim was added.
- No energy outcome claim was added.
- No unsupported larger-model execution claim was added.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Known Limitations

- JavaScript remains inline.
- No JavaScript static asset route exists.
- No frontend framework tooling exists.
- No product behavior changed.
- The CSS asset route remains intentionally limited to one allowlisted file.

## Next Recommended Goal

Goal 519G — KORA Studio v2.0 JavaScript Asset Migration Decision Plan.

Recommended scope:

- keep the next step planning-first
- decide whether JavaScript should remain inline or move to a first-party package-controlled source file
- preserve local-only route boundaries
- avoid frontend framework tooling and dependencies
- preserve all endpoint and smoke marker coverage
