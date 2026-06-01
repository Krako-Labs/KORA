# KORA Studio v2.1 Goal Report

## Goal Status

Goal 520G is complete.

KORA Studio v2.1 adds a minimal local-preview Content Security Policy header to the root Studio HTML response while preserving package-controlled local assets, approved request JSON behavior, endpoint behavior, smoke markers, and claim boundaries.

## Starting State

- Starting public HEAD: `ed8b8c11ed09083ef3c1cbd5f9f229a76933d7a5`
- Public truth: `origin/main`

## CSP Decision

An enforced CSP header is safe for the root local preview HTML route now that CSS and executable JavaScript are package-controlled local assets.

The CSP is applied only to the root HTML response. API, SSE, health, status, and static asset responses are not changed by the CSP step.

## Completed Work

- Added root HTML `Content-Security-Policy` header
- Preserved `/studio-assets/studio.css`
- Preserved `/studio-assets/studio.js`
- Preserved approved request JSON as inline `type="application/json"`
- Kept executable JavaScript external through `/studio-assets/studio.js`
- Added tests for the CSP header value
- Added tests that health, status, CSS asset, and JavaScript asset routes do not receive the CSP header
- Updated docs and reports

## Files Changed

- `kora/studio_server.py`
- `tests/test_kora_studio_server.py`
- `docs/kora-studio/README.md`
- `docs/kora-studio/kora-studio-implementation-breakdown.md`
- `docs/kora-studio/kora-studio-v2-1-local-asset-csp-readiness-report.md`
- `docs/kora-studio/kora-studio-v2-1-goal-report.md`

## CSP Behavior

Root HTML response:

- includes `Content-Security-Policy`
- allows self-hosted CSS and JavaScript
- allows same-origin local fetch and SSE connections
- does not allow external hosts
- does not include broad wildcards
- does not include `unsafe-inline`
- does not include `unsafe-eval`

Routes intentionally not given the CSP header:

- `/health`
- `/status`
- `/api/harness/...`
- `/studio-assets/studio.css`
- `/studio-assets/studio.js`

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
- KORA Studio does not claim production security readiness.
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

- This is not a production security readiness claim.
- Browser-level CSP violation monitoring is not added yet.
- Approved request JSON remains inline as a non-executable data script.
- There is no general static file server.
- The asset route remains intentionally limited to two allowlisted package-controlled files.

## Next Recommended Goal

Goal 521G — KORA Studio v2.2 Browser-Level CSP Smoke Validation.

The next goal should validate CSP behavior in a browser-level local smoke pass while preserving route boundaries, local asset behavior, endpoint behavior, smoke markers, and claim safety.
