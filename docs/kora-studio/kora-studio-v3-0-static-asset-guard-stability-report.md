# KORA Studio v3.0 Static Asset Guard Stability Report

## Decision

KORA Studio v3.0 reviews static asset guard stability around the local Studio asset route, package asset loading, package-data configuration, MIME/cache behavior, and route rejection coverage.

The review found the existing runtime behavior stable. Two dependency-light tests were added to close maintenance gaps:

- package-data configuration must include only the package-controlled Studio CSS and JavaScript asset globs
- the Studio asset handler must not introduce filesystem-backed static serving helpers or directory-serving behavior

No runtime behavior changed.

## Stability Review Summary

Current stable asset model:

- allowed asset routes:
  - `/studio-assets/studio.css`
  - `/studio-assets/studio.js`
- asset source:
  - `kora/studio_assets/studio.css`
  - `kora/studio_assets/studio.js`
- package-data configuration:
  - `studio_assets/*.css`
  - `studio_assets/*.js`
- MIME and cache:
  - CSS: `text/css; charset=utf-8`
  - JavaScript: `application/javascript; charset=utf-8`
  - both use `Cache-Control: no-store`
- CSP:
  - root HTML route only
  - no CSP header on API, SSE, health, status, or asset routes by default

## Gaps Found and Fixed

Added tests for:

- exact package-data asset globs in `pyproject.toml`
- absence of filesystem static serving patterns in the Studio asset request handler

No-gap rationale for existing coverage:

- exact allowlist is already tested for `studio.css` and `studio.js`
- unknown assets are already rejected
- traversal, encoded traversal, backslash traversal, and absolute-path-shaped asset requests are already rejected
- directory-style asset requests are already rejected
- CSS and JavaScript MIME/content-type and `no-store` cache behavior are already tested
- package source loading is already tested against the package-controlled source files
- browser-free default smoke and optional browser CSP smoke both cover the current asset routes

## Preserved Boundaries

This review does not add or change:

- Studio runtime behavior
- root CSP
- `/studio-assets/studio.css`
- `/studio-assets/studio.js`
- asset allowlist behavior
- optional browser CSP smoke behavior
- CI-optional wrapper behavior
- local preview endpoint behavior
- persistent dependencies
- frontend tooling
- package manifests or lockfiles
- Playwright config
- bundlers or npm workflows
- external assets or CDN usage
- production security readiness claims

## Validation Results

Final validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed

Optional smoke checks:

- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed
- `python3 scripts/check_kora_studio_preview.py`: passed

## Claim Boundaries Preserved

- KORA Studio remains local preview/demo readiness only.
- This is static asset guard stability review only.
- Browser CSP validation remains smoke validation only.
- KORA Studio is not production-ready.
- KORA Studio does not claim production security readiness.
- KORA Studio is not an LM Studio replacement.
- No arbitrary prompt execution was added.
- No model execution was added.
- No provider calls were added.
- No model downloads were added.
- No cloud sync was added.
- No private model directory scanning was added.
- No runtime model list commands were added.
- No report export or file writing was added.
- No production telemetry or production cost evidence claim was added.
- No production cost reduction claim was added.
- No energy outcome claim was added.
- No unsupported larger-model execution claim was added.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Next Recommended Goal

Goal 530G - KORA Studio Static Asset Guard Pause Decision.

Recommended scope:

- decide whether CSP/static asset guard work should pause after v3.0
- keep the decision documentation-only unless a concrete bug is found
- preserve the current CSP and asset allowlist
- avoid production security readiness claims
