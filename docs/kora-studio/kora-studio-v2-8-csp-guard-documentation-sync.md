# KORA Studio v2.8 CSP Guard Documentation Sync

## Decision

KORA Studio v2.8 synchronizes CSP guard documentation across the README, implementation breakdown, and v2.4-v2.7 reports. This is a documentation-only step.

No runtime behavior, CSP directive, asset route, test policy, dependency policy, or browser smoke behavior changed.

## Documentation Sync Summary

The docs now consistently state:

- package-controlled Studio assets are `/studio-assets/studio.css` and `/studio-assets/studio.js`
- the local-preview CSP header applies to root Studio HTML only
- API, SSE, health, status, and asset routes do not receive CSP headers by default
- default CSP/resource guard coverage remains dependency-light and browser-free
- browser-level CSP smoke remains optional and explicitly gated with `KORA_STUDIO_BROWSER_CSP_SMOKE=1`
- positive regression guards cover root HTML, CSP directives, package CSS, and package JavaScript
- negative fixture guards cover rejected HTML, CSP, and CSS resource patterns
- v2.7 added targeted HTML negative cases for mixed-case/whitespace URLs, `javascript:`, `srcset`, `meta refresh`, form actions, inline event handlers, and inline `<style>` blocks
- none of these checks claim production security readiness

## Inconsistencies Fixed

- Added a README summary for the current local asset CSP guard model.
- Added a current CSP guard summary to the implementation breakdown.
- Added short synchronization notes to v2.4, v2.5, and v2.6 reports so they point forward to the expanded v2.7 negative coverage instead of reading as the final current matrix.
- Kept v2.7 as the current negative coverage reference.

## Preserved Boundaries

This documentation sync does not add or change:

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
- This is CSP guard documentation sync only.
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

Goal 528G - KORA Studio CSP Guard Maintenance Checklist.

Recommended scope:

- add a short contributor checklist for future Studio resource/CSP changes
- keep it documentation-only unless a clear test gap is found
- preserve the current CSP and asset allowlist
- avoid production security readiness claims
