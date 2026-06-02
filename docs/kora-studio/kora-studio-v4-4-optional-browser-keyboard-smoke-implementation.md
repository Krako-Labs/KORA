# KORA Studio v4.4 Optional Browser Keyboard Smoke Implementation

## Status

KORA Studio v4.4 implements the optional browser keyboard smoke designed in v4.3.

The smoke is explicitly opt-in and remains outside default pytest and default CI:

```bash
KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 scripts/check_kora_studio_browser_keyboard_ci_optional.sh
```

The implementation uses transient `npx --yes --package @playwright/test`, matching the existing browser CSP smoke pattern. It adds no package manifest, lockfile, Playwright config, axe tooling, frontend build tooling, external asset, or CDN.

## Implemented Files

- `scripts/check_kora_studio_browser_keyboard.py`
- `scripts/check_kora_studio_browser_keyboard_ci_optional.sh`
- `tests/test_kora_studio_browser_keyboard_smoke.py`

## Browser Keyboard Smoke Coverage

The optional smoke validates only the stable v4.3 assertions:

- root page load
- `data-kora-keyboard-selector-contract="v4.2"` marker
- script-ready state through `window.koraStudioScriptStatus`
- approved request selector contract and selected approved request state
- selected approved request `aria-pressed` and `aria-current` state
- Run Local Harness keyboard focus and Enter activation
- generated completed state in the primary result summary while run progress remains visible
- Retry Last Approved Request stays present and bounded while run/event-stream state changes
- details drawer keyboard open
- focus transfer to the details drawer close button
- Escape close
- focus return to the details drawer toggle
- no browser CSP console violations, page errors, or same-origin request failures

## Explicitly Not Covered

The optional smoke does not validate:

- exact full-page Tab order
- keyboard traversal into the collapsed compatibility request selector
- every secondary diagnostic surface by keyboard
- screen-reader announcement quality
- production accessibility conformance
- mobile rail traversal in this first implementation

Those remain manual-only or future optional-smoke expansion candidates.

## Dependency-Light Guard Coverage

Default pytest verifies the script and wrapper without launching a browser:

- non-local URLs are rejected
- the generated Playwright spec uses the v4.2 selector contract
- the generated Playwright spec avoids exact full-page Tab-order assertions
- transient `npx --package @playwright/test` invocation is used
- missing `npx` reports a clear optional-smoke error
- the shell wrapper is explicitly gated by `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1`
- the wrapper does not install dependencies or add package manifests

## Preserved Boundaries

- no backend route or API change
- no local harness behavior change
- no CSP broadening
- no static asset allowlist broadening
- no arbitrary prompt execution
- no model execution
- no provider calls
- no downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report export or file writing
- no production accessibility certification claim

## Validation Results

Required validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: 72 passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: 4 passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: 5 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 159 passed, 143 deselected
- `python3 -m pytest`: 302 passed

Optional validation:

- `python3 scripts/check_kora_studio_preview.py --base-url http://127.0.0.1:8768`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 KORA_STUDIO_BROWSER_CSP_PORT=8766 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 KORA_STUDIO_BROWSER_KEYBOARD_PORT=8767 scripts/check_kora_studio_browser_keyboard_ci_optional.sh`: passed against the local Studio server

## Next Recommended Goal

Goal 544G - KORA Studio Optional Browser Keyboard Smoke Mobile Rail Extension Review.

The next goal should decide whether to extend the optional keyboard smoke to the narrow/mobile rail flow or keep mobile rail validation manual-only.
