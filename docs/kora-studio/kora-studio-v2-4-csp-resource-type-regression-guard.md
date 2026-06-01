# KORA Studio v2.4 CSP Resource-Type Regression Guard

## Decision

KORA Studio v2.4 adds dependency-light CSP resource-type regression guards in pytest. The guard is static and server-rendered HTML oriented, so default validation remains browser-free and does not require `npx`, Playwright, Node package manifests, browser downloads, or network access.

The browser CSP smoke from v2.2/v2.3 remains optional and explicitly gated. v2.4 does not broaden CSP or static asset serving.

## Guard Coverage

The regression guard validates:

- root Studio HTML has no inline `style` attributes
- executable JavaScript is loaded only from `/studio-assets/studio.js`
- the only inline script block is the approved request JSON block with `type="application/json"`
- root Studio HTML references `/studio-assets/studio.css` as the only stylesheet
- root Studio HTML does not use `data:`, `blob:`, remote HTTP(S), protocol-relative, CDN, or external resource URLs in resource-bearing attributes
- `/studio-assets/` references remain limited to `studio.css` and `studio.js`
- CSP directives remain intentionally narrow
- CSP does not include `unsafe-inline`, `unsafe-eval`, wildcard sources, `data:`, `blob:`, HTTP(S) sources, or broad external hosts
- package-controlled CSS and JavaScript do not introduce remote or embedded resource URLs
- package-controlled CSS does not introduce `@import` or `url(...)` resource loading

## Current CSP

```text
default-src 'none'; base-uri 'none'; object-src 'none'; frame-ancestors 'none'; form-action 'none'; style-src 'self'; script-src 'self'; connect-src 'self'
```

Current allowed local asset routes:

- `/studio-assets/studio.css`
- `/studio-assets/studio.js`

The allowed routes remain explicit and package-controlled. There is still no wildcard static route, directory listing, arbitrary filesystem serving, external asset loading, or CDN usage.

## Approved Inline JSON Exception

KORA Studio still includes approved request data as:

```html
<script type="application/json" id="kora-approved-requests-data">...</script>
```

This block is not executable JavaScript. The guard keeps this exception explicit so future executable inline script additions fail review unless deliberately changed in a later goal.

## Boundaries

This step does not add:

- persistent frontend dependencies
- root `package.json`
- lockfiles
- Playwright config
- frontend build tooling
- bundlers or minifiers
- external assets or CDN usage
- CSP broadening
- new static asset routes
- wildcard asset serving
- production security readiness claims

## Validation Results

Final validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed

Browser and preview smoke:

- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed
- `python3 scripts/check_kora_studio_preview.py`: passed

## Claim Boundaries Preserved

- KORA Studio remains local preview/demo readiness only.
- This is a CSP resource-type regression guard only.
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

Goal 524G - KORA Studio CSP Violation Fixture Matrix.

Recommended scope:

- add small negative fixtures for representative blocked HTML/CSP patterns
- keep tests dependency-light
- preserve the current CSP and asset allowlist
- avoid production security readiness claims
