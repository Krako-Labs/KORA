# KORA Studio v1.8 Readiness Report

## Status

KORA Studio v1.8 is ready as a local preview architecture milestone.

v1.8 implements a single CSS-only local static asset route:

```text
/studio-assets/studio.css
```

The route is allowlisted, uses existing `render_studio_css()` output as its source, and does not serve arbitrary files. JavaScript remains inline through `render_studio_javascript()`.

## Implemented Surface

- `GET /studio-assets/studio.css`
- `Content-Type: text/css; charset=utf-8`
- `Cache-Control: no-store`
- CSS source remains `render_studio_css()`
- root preview references `/studio-assets/studio.css`
- inline JavaScript remains in the root preview
- no JavaScript static asset route
- no wildcard static route
- no directory listing
- no arbitrary filesystem serving

## Route Behavior

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

## Security Boundary

The static asset route:

- serves only the approved CSS asset
- does not build paths from user input
- does not serve from the project root
- does not serve user uploads
- does not serve model files
- does not serve reports or report exports
- does not expose directory listings
- does not fetch external assets
- does not add CDN references
- does not add dependencies

The existing localhost-only server boundary remains unchanged.

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

- CSS is served from `render_studio_css()` output, not a standalone CSS file yet.
- JavaScript remains inline.
- No JavaScript static asset route exists.
- No frontend framework tooling exists.
- No product behavior changed.

## Next Recommended Goal

Goal 518G — KORA Studio v1.9 CSS Asset Source File Migration Plan.

Recommended scope:

- plan whether `render_studio_css()` should remain the source or delegate to a reviewed first-party CSS file
- preserve the existing `/studio-assets/studio.css` route
- keep JavaScript inline
- avoid dependencies and frontend framework tooling
- preserve all endpoint and smoke marker coverage
