# KORA Studio v2.9 CSP Guard Maintenance Checklist

## Decision

KORA Studio v2.9 adds a concise public maintenance checklist for future Studio HTML, CSS, JavaScript, CSP, and static asset route changes. This is a documentation-only step.

No runtime behavior, CSP directive, asset route, asset allowlist, dependency policy, frontend tooling, or browser smoke behavior changed.

## Checklist Summary

Future Studio resource/CSP changes should:

- update dependency-light tests in `tests/test_kora_studio_server.py`
- preserve the current package-controlled assets unless a reviewed goal expands the allowlist:
  - `/studio-assets/studio.css`
  - `/studio-assets/studio.js`
- keep executable JavaScript external through `/studio-assets/studio.js`
- keep approved request JSON non-executable with `type="application/json"`
- update allowlist, rejection, MIME/cache, smoke, and docs coverage for any new asset route
- add guard coverage before introducing new CSS resource patterns such as `@import`, `url(...)`, images, fonts, media, frames, or workers
- run standard validation
- run optional browser CSP smoke when resource loading or CSP behavior changes:

```bash
KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh
```

## Explicit Review Required

Do not add or broaden these without explicit review:

- `unsafe-inline`
- `unsafe-eval`
- wildcard CSP sources
- external hosts
- CDN sources
- `data:`
- `blob:`
- package manifests
- lockfiles
- frontend tooling
- bundlers
- npm workflows
- Playwright config
- external assets
- CDN dependencies

## Docs Updated

- `docs/kora-studio/README.md`
- `docs/kora-studio/kora-studio-implementation-breakdown.md`

## Preserved Boundaries

This checklist does not add or change:

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
- This is a CSP/static asset maintenance checklist only.
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

Goal 529G - KORA Studio Static Asset Guard Stability Review.

Recommended scope:

- review whether the current docs/tests are stable enough to pause CSP/static guard work
- avoid runtime behavior changes unless a concrete bug is found
- preserve the current CSP and asset allowlist
- avoid production security readiness claims
