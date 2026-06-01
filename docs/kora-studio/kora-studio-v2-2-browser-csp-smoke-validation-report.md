# KORA Studio v2.2 Browser-Level CSP Smoke Validation Report

## Decision

KORA Studio v2.2 adds an optional browser-level CSP smoke script without adding a committed browser automation dependency.

The repository still has no Playwright package manifest, lockfile, npm workflow, frontend build tooling, bundler, minifier, external asset, or CDN dependency. The optional script uses `npx` to run Playwright when available.

## Browser Smoke Script

Script:

```text
scripts/check_kora_studio_browser_csp.py
```

Expected use against an already-running local preview:

```text
python3 scripts/check_kora_studio_browser_csp.py
```

The script accepts only:

- `http://127.0.0.1`
- `http://localhost`

## Validation Coverage

The browser smoke validates:

- root Studio HTML loads in Chromium
- root response includes the expected CSP header
- `/studio-assets/studio.css` loads as CSS
- `/studio-assets/studio.js` loads as JavaScript
- the Studio shell is visible
- approved request selector elements are present
- the visible Run Local Harness control can be clicked
- selected-run state updates after the local harness run
- same-origin local fetch and SSE behavior remains compatible with `connect-src 'self'`
- browser console contains no obvious CSP violations
- same-origin requests do not fail unexpectedly

## CSP Findings

The first browser-level pass found CSP violations caused by remaining inline style attributes and a `data:` favicon placeholder. v2.2 fixes those without broadening the CSP:

- repeated `style="margin-top: ..."` attributes were replaced with first-party CSS classes
- the `data:` favicon placeholder was removed
- the CSP did not add `unsafe-inline`
- the CSP did not add `unsafe-eval`
- the CSP did not add wildcards
- the CSP did not add external host allowances

## Automated Test Coverage

Unit tests cover the optional script without requiring a browser:

- rejects non-local URLs
- verifies the generated Playwright smoke spec keeps local preview boundaries
- verifies the script invokes Playwright through `npx` without adding repo dependencies
- verifies missing `npx` is reported clearly

## Validation Results

Final validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed

Browser smoke check:

- `python3 -m kora studio --no-browser`: started local preview server
- `python3 scripts/check_kora_studio_browser_csp.py --timeout 20000`: passed
- server stopped cleanly

HTTP smoke check:

- `python3 scripts/check_kora_studio_preview.py`: passed

## Claim Boundaries Preserved

- KORA Studio remains local preview/demo readiness only.
- This is browser-level CSP smoke validation only.
- KORA Studio is not production-ready.
- KORA Studio does not claim production security readiness.
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
- No external network behavior was added beyond optional localhost browser automation.
- No external assets or CDN dependencies were added.
- No production telemetry claim was added.
- No production cost evidence claim was added.
- No production cost reduction claim was added.
- No energy outcome claim was added.
- No unsupported larger-model execution claim was added.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Follow-Up Criteria

Future browser validation changes should remain separate goals and should require:

- no committed browser dependency unless explicitly approved
- no CSP broadening without a documented reason
- browser-level checks for any new resource type
- continued local-only URL restrictions
- continued claim-safe wording

## Next Recommended Goal

Goal 522G — KORA Studio v2.3 CSP Resource-Type Regression Guard.

Recommended scope:

- add lightweight regression tests for future resource types such as images, fonts, workers, frames, and media
- keep CSP narrow
- preserve local-only route boundaries
- avoid production security readiness claims
