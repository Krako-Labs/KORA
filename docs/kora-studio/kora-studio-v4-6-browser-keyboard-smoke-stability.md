# KORA Studio v4.6 Browser Keyboard Smoke Stability

## Status

KORA Studio v4.6 documents stability expectations and maintenance rules for the optional browser keyboard smoke.

This is documentation-only. It does not change the smoke script, wrapper, runtime behavior, backend routes, local harness behavior, CSP, static asset allowlist, dependencies, package manifests, lockfiles, Playwright config, axe tooling, frontend build tooling, external assets, or CDN.

## How the Smoke Runs

The browser keyboard smoke is explicitly opt-in:

```bash
KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 scripts/check_kora_studio_browser_keyboard_ci_optional.sh
```

Default behavior:

- the wrapper exits without running browser automation unless `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1`
- normal pytest does not launch Playwright
- default CI should not depend on browser installation, network access, or `npx`
- the wrapper starts a local `python3 -m kora studio --no-browser` server
- the Python script accepts only `http://127.0.0.1` or `http://localhost` base URLs

Dependency model:

- uses transient `npx --yes --package @playwright/test`
- does not add `package.json`
- does not add lockfiles
- does not add Playwright config
- does not add axe tooling
- does not add frontend build tooling

## Stable Desktop Assertions

The desktop-primary path is stable when these remain true:

- root page loads with HTTP 200
- `window.koraStudioScriptStatus.status` reaches `ready`
- root shell exposes `data-kora-keyboard-selector-contract="v4.2"`
- model selector contract is attached
- approved request option contract is attached
- selected approved request state is present
- selected approved request exposes `aria-pressed="true"` and `aria-current="true"`
- primary Run Local Harness control is visible, focusable, and activates through Enter
- primary result summary reaches `completed`
- run progress summary remains visible
- shell retry control remains present and bounded while run/event-stream state changes
- details drawer toggle is visible, starts closed, opens through Enter, moves focus to the close button, closes through Escape, and returns focus to the toggle
- browser CSP console violations, page errors, and same-origin request failures remain absent

These checks validate the local demo path. They do not certify accessibility.

## Stable Mobile Rail Assertions

The mobile rail path is stable when these remain true:

- viewport is set to 390 by 844
- `mobile-rail-toggle` is visible
- toggle starts with `aria-expanded="false"`
- `mobile-left-rail` starts with `data-kora-rail-state="closed"`
- closed rail has `aria-hidden="true"`
- Enter on the toggle opens the rail
- open rail reports `data-kora-rail-state="open"` and `aria-hidden="false"`
- focus moves to `mobile-rail-close`
- Escape closes the rail
- focus returns to `mobile-rail-toggle`
- browser CSP console violations, page errors, and same-origin request failures remain absent

Do not extend this into full mobile visual QA inside the smoke. Visual overlap, spacing, and polish remain manual or separate visual QA work.

## Manual-Only Assertions

Do not add these to the optional browser keyboard smoke without a separate review goal:

- exact full-page Tab order
- every secondary diagnostic surface by keyboard
- every collapsed compatibility/reference surface by keyboard
- keyboard traversal into the collapsed compatibility request selector
- screen-reader announcement quality
- live-region spoken announcement timing
- visual focus ring quality across all browsers
- every mobile overlap or responsive layout visual condition
- production accessibility conformance
- production security, production readiness, or certification claims

## When to Update the Smoke

Update the optional browser keyboard smoke when:

- a `data-kora-keyboard-contract` selector used by the smoke changes
- `data-kora-keyboard-selector-contract` version changes
- primary Run Local Harness control changes selector, focus behavior, or activation behavior
- details drawer open/close/focus return behavior changes
- mobile rail open/close/focus return behavior changes
- approved request selected-state semantics change
- result summary completion marker changes
- retry control state semantics change

When updating, keep the smoke bounded to stable selectors and state attributes. Prefer adding dependency-light tests for script/spec changes before changing the optional live browser path.

## When Not to Broaden the Smoke

Do not broaden the smoke merely because a visual detail changed, because a manual accessibility review found a cosmetic issue, or because a diagnostic surface gained new content.

Do not add:

- persistent npm dependencies
- package manifests or lockfiles
- Playwright config
- axe tooling
- frontend build tooling
- external assets or CDN
- wildcard network access
- production accessibility certification claims

## Preserved Boundaries

- local preview/demo readiness only
- optional browser keyboard smoke stability documentation only
- not production-ready
- not production accessibility certification
- not an LM Studio replacement
- no arbitrary prompt execution
- no real model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report export or file writing
- not production telemetry or production cost evidence
- no cost reduction or energy outcome claim

## Validation Results

Required validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: 72 passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: 4 passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: 5 passed
- `python3 -m pytest tests/test_kora_studio_browser_keyboard_smoke.py`: 5 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 159 passed, 143 deselected
- `python3 -m pytest`: 302 passed

Optional validation:

- `python3 scripts/check_kora_studio_preview.py --base-url http://127.0.0.1:8768`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 KORA_STUDIO_BROWSER_CSP_PORT=8766 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 KORA_STUDIO_BROWSER_KEYBOARD_PORT=8767 scripts/check_kora_studio_browser_keyboard_ci_optional.sh`: passed against the local Studio server

## Next Recommended Goal

Goal 546G - KORA Studio Optional Browser Smoke Documentation Consolidation.

The next goal should decide whether the CSP smoke and keyboard smoke stability notes should be consolidated into a single optional browser smoke maintenance guide.
