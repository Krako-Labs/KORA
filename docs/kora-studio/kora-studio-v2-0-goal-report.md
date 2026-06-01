# KORA Studio v2.0 Goal Report

## Goal Status

Goal 519G is complete.

KORA Studio v2.0 migrates the Studio interaction JavaScript from inline HTML into a package-controlled first-party JavaScript file while preserving local-only behavior, the existing CSS asset route, endpoint behavior, smoke markers, and claim boundaries.

## Starting State

- Starting public HEAD: `81abd8aa49dff6894ddab2ae804456c0386eb449`
- Public truth: `origin/main`

## Migration Decision

JavaScript migration is approved and implemented for v2.0.

The migration is bounded because:

- the asset namespace remains `/studio-assets`
- the allowlist contains only `studio.css` and `studio.js`
- no wildcard static route is added
- no arbitrary filesystem serving is added
- no directory listing is added
- no frontend build tooling or dependency is added

## Completed Work

- Added package-controlled JavaScript source file: `kora/studio_assets/studio.js`
- Updated `render_studio_javascript()` to load that package resource
- Added `/studio-assets/studio.js` route with `application/javascript; charset=utf-8`
- Preserved `/studio-assets/studio.css` behavior
- Preserved `Cache-Control: no-store` for local preview assets
- Updated the root preview to reference `/studio-assets/studio.js`
- Kept approved request JSON inline as `type="application/json"`
- Preserved exact asset allowlist and rejection behavior
- Added tests proving the JavaScript helper returns the controlled source file contents
- Updated live smoke coverage for `/studio-assets/studio.js`
- Updated docs and reports

## Files Changed

- `pyproject.toml`
- `kora/studio_server.py`
- `kora/studio_script_render.py`
- `kora/studio_assets/studio.js`
- `tests/test_kora_studio_server.py`
- `tests/test_kora_studio_preview_smoke.py`
- `scripts/check_kora_studio_preview.py`
- `docs/kora-studio/README.md`
- `docs/kora-studio/kora-studio-implementation-breakdown.md`
- `docs/kora-studio/kora-studio-v2-0-javascript-asset-migration-decision-report.md`
- `docs/kora-studio/kora-studio-v2-0-goal-report.md`

## Route Behavior

Allowed:

- `GET /studio-assets/studio.css`
- `GET /studio-assets/studio.js`

Responses:

- CSS: `Content-Type: text/css; charset=utf-8`
- JavaScript: `Content-Type: application/javascript; charset=utf-8`
- both: `Cache-Control: no-store`

Rejected:

- unknown assets
- directory paths
- traversal paths
- encoded traversal
- double-encoded traversal
- backslash traversal
- absolute-path shaped requests under `/studio-assets`

Rejected responses do not expose local filesystem paths.

## Validation Results

Final validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed

Live smoke check:

- `python3 -m kora studio --no-browser`: passed server startup
- `python3 scripts/check_kora_studio_preview.py`: passed
- server stopped cleanly

## Claim Boundaries Preserved

- KORA Studio remains local preview/demo readiness only.
- KORA Studio is not production-ready.
- KORA Studio is not an LM Studio replacement.
- No arbitrary prompt execution was added.
- No model execution was added.
- No provider calls were added.
- No downloads were added.
- No cloud sync was added.
- No private model directory scanning was added.
- No runtime model list commands were added.
- No report export or file writing was added.
- No external assets or CDN dependencies were added.
- No production telemetry or production cost evidence claim was added.
- No production cost reduction claim was added.
- No energy outcome claim was added.
- No unsupported larger-model execution claim was added.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Known Limitations

- Approved request JSON remains inline in the root HTML document.
- No Content Security Policy header is added yet.
- There is no general static file server.
- There is no frontend framework or dependency-based asset pipeline.
- The asset route remains intentionally limited to two allowlisted package-controlled files.

## Next Recommended Goal

Goal 520G — KORA Studio v2.1 Local Asset CSP Readiness Review.

The next goal should remain planning-first and review whether a local-only Content Security Policy can be introduced while preserving the approved request JSON payload, local asset routes, endpoint behavior, smoke markers, and claim safety.
