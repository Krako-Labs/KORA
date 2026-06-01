# KORA Studio v2.7 CSP Negative Coverage Review

## Decision

KORA Studio v2.7 adds a small set of relevant negative CSP/resource guard cases. The additions focus on HTML resource patterns that could realistically appear in the current server-rendered Studio preview and bypass the earlier simple prefix checks.

The review avoids speculative resource classes and keeps coverage dependency-light, local-only, and browser-free.

## Added Cases

The HTML fixture matrix now covers:

- mixed-case external resource schemes
- whitespace-padded external resource URLs
- `javascript:` pseudo URLs
- `srcset` external URL candidates
- `meta http-equiv="refresh"` URL targets
- external form `action` targets
- inline event handler attributes such as `onclick`
- inline `<style>` blocks

These cases materially reduce regression risk because they represent common ways resource loading or executable behavior can enter HTML without changing the current `/studio-assets/studio.css` and `/studio-assets/studio.js` model.

## Declined Cases

The review did not add fixtures for unrelated future resource classes such as workers, frames, media elements, icons beyond current resource URL handling, or font-specific cases. Those would be useful only if KORA Studio intentionally adds those resource types in a later goal.

The review also did not add browser-only assertions, because browser-level CSP validation remains optional and explicitly gated.

## Preserved Coverage

Existing v2.4/v2.5 coverage remains:

- inline style attributes
- inline executable script blocks
- external script URLs
- external stylesheet URLs
- `data:` resource URLs
- `blob:` resource URLs
- protocol-relative resource URLs
- unapproved `/studio-assets/...` paths
- wildcard CSP sources
- `unsafe-inline`
- `unsafe-eval`
- `data:` CSP sources
- `blob:` CSP sources
- external CSP hosts
- new image/font CSP directives
- CSS `@import`
- CSS `url(...)`
- CSS embedded or external URLs

The approved request JSON block remains the only allowed inline script-shaped element:

```html
<script type="application/json" id="kora-approved-requests-data">...</script>
```

## Boundaries

This review does not change:

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
- This is CSP guard negative coverage review only.
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

Goal 527G - KORA Studio CSP Guard Documentation Sync.

Recommended scope:

- review whether older KORA Studio CSP/static-asset docs need concise cross-links to the v2.4-v2.7 guard reports
- avoid changing runtime behavior
- preserve the current CSP and asset allowlist
- avoid production security readiness claims
