# KORA Studio v2.5 CSP Violation Fixture Matrix

## Decision

KORA Studio v2.5 adds a dependency-light CSP violation fixture matrix to make rejected resource patterns explicit in pytest. The matrix documents and tests representative blocked patterns without broadening KORA Studio behavior.

The fixture matrix is local-only and browser-free. It does not add frontend dependencies, browser dependencies, package manifests, lockfiles, bundlers, npm workflows, external assets, or CDN usage.

Current documentation note: v2.7 extends this matrix with targeted HTML resource cases while preserving the same root CSP, asset allowlist, optional browser smoke policy, and local-preview-only claim boundary.

## Fixture Matrix Coverage

HTML resource fixtures prove these patterns are rejected:

- inline `style` attributes
- inline executable script blocks
- external script URLs
- external stylesheet URLs
- `data:` image/resource URLs
- `blob:` resource URLs
- protocol-relative resource URLs
- unapproved `/studio-assets/...` paths

Later v2.7 HTML fixtures also reject mixed-case and whitespace-padded external URLs, `javascript:` pseudo URLs, `srcset` external candidates, `meta refresh` URL targets, external form actions, inline event handlers, and inline `<style>` blocks.

CSP fixtures prove these sources/directives are rejected:

- wildcard source `*`
- `unsafe-inline`
- `unsafe-eval`
- `data:`
- `blob:`
- external host sources
- new image directives such as `img-src`
- new font directives such as `font-src`

CSS fixtures prove these patterns are rejected:

- `@import`
- `url(...)`
- `data:` CSS URLs
- `blob:` CSS URLs
- external CSS URLs

## Approved Exception

The approved request JSON block remains the only allowed inline script-shaped element:

```html
<script type="application/json" id="kora-approved-requests-data">...</script>
```

It remains non-executable data for the local preview. Any future inline executable script should require a separate reviewed goal.

## Preserved Boundaries

The fixture matrix does not change:

- root CSP
- `/studio-assets/studio.css`
- `/studio-assets/studio.js`
- asset allowlist behavior
- optional browser CSP smoke behavior
- CI-optional wrapper behavior
- local preview endpoint behavior

There is still no wildcard static route, directory listing, arbitrary filesystem serving, external asset loading, CDN usage, or production security readiness claim.

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
- This is a CSP fixture matrix and regression guard only.
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

Goal 525G - KORA Studio CSP Guard Helper Cleanup.

Recommended scope:

- decide whether CSP guard helpers should stay in `tests/test_kora_studio_server.py` or move to a small test utility
- keep the guard dependency-light
- preserve the current CSP and asset allowlist
- avoid production security readiness claims
