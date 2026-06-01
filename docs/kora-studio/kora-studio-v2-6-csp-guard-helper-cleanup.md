# KORA Studio v2.6 CSP Guard Helper Cleanup

## Decision

KORA Studio v2.6 keeps CSP/resource guard helpers inside `tests/test_kora_studio_server.py`. The current helper set is still small, test-only, and directly tied to the Studio server render assertions, so moving it into a separate test utility would add indirection without improving runtime boundaries.

The cleanup consolidates repeated constants and parsing/checking logic while preserving all v2.4/v2.5 guard coverage.

## Helper Cleanup Summary

The test module now centralizes:

- expected Studio stylesheet path
- expected Studio JavaScript asset path
- approved inline request JSON script shape
- allowed `/studio-assets/...` URLs
- forbidden HTML resource URL prefixes
- expected CSP directives
- forbidden CSP sources
- CSP resource directives requiring review
- forbidden CSS resource patterns
- forbidden package asset tokens

The helper functions now share the same constants used by positive guards and table-driven negative fixtures.

## Preserved Fixture Coverage

HTML fixture coverage remains:

- inline style attributes
- inline executable scripts
- external script URLs
- external stylesheet URLs
- `data:` image/resource URLs
- `blob:` resource URLs
- protocol-relative URLs
- unapproved `/studio-assets/...` paths

CSP fixture coverage remains:

- wildcard CSP sources
- `unsafe-inline`
- `unsafe-eval`
- `data:`
- `blob:`
- external host sources
- new image directives
- new font directives

CSS fixture coverage remains:

- `@import`
- `url(...)`
- `data:` CSS URLs
- `blob:` CSS URLs
- external CSS URLs

## Boundaries

This cleanup does not change:

- Studio runtime behavior
- root CSP
- `/studio-assets/studio.css`
- `/studio-assets/studio.js`
- asset allowlist behavior
- optional browser CSP smoke behavior
- CI-optional wrapper behavior
- local preview endpoint behavior

No dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, CDN, CSP broadening, or asset allowlist broadening was added.

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
- This is CSP guard helper cleanup only.
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

Goal 526G - KORA Studio CSP Guard Negative Coverage Review.

Recommended scope:

- review whether additional representative negative fixtures are useful
- keep coverage dependency-light
- preserve the current CSP and asset allowlist
- avoid production security readiness claims
