# KORA Studio v4.5 Mobile Rail Keyboard Smoke Extension Review

## Status

KORA Studio v4.5 reviews whether the optional browser keyboard smoke should cover the narrow/mobile left rail.

Decision: implement a bounded mobile rail check now inside the existing optional browser keyboard smoke. The mobile rail has stable v4.2 selector contracts, explicit open/close state attributes, `aria-expanded`, `aria-hidden`, and existing JavaScript focus return behavior. The extension remains explicitly gated by `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1`.

## Inputs Reviewed

Reviewed implementation and validation surfaces:

- `scripts/check_kora_studio_browser_keyboard.py`
- `scripts/check_kora_studio_browser_keyboard_ci_optional.sh`
- `tests/test_kora_studio_browser_keyboard_smoke.py`
- `docs/kora-studio/kora-studio-v4-2-keyboard-selector-contract.md`
- Studio left rail HTML, CSS, and JavaScript state handling

## Implemented Mobile Rail Assertions

The optional keyboard smoke now includes a separate narrow-viewport Playwright test that validates:

- viewport set to 390 by 844
- `mobile-rail-toggle` is visible
- toggle starts with `aria-expanded="false"`
- `mobile-left-rail` starts closed with `data-kora-rail-state="closed"`
- closed mobile rail has `aria-hidden="true"`
- keyboard Enter on the toggle opens the rail
- open rail reports `data-kora-rail-state="open"` and `aria-hidden="false"`
- focus moves to `mobile-rail-close`
- Escape closes the rail
- focus returns to `mobile-rail-toggle`
- no browser CSP console violations, page errors, or same-origin request failures occur

## Kept Out of Automation

The optional smoke still does not validate:

- exact full-page Tab order
- every mobile visual overlap scenario
- screen-reader announcement quality
- production accessibility conformance
- cross-browser accessibility certification

Those remain manual-only or future review candidates.

## Preserved Boundaries

- no backend route or API change
- no local harness behavior change
- no CSP broadening
- no static asset allowlist broadening
- no dependency, package manifest, lockfile, Playwright config, axe tooling, frontend build tooling, external asset, or CDN
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
- `python3 -m pytest tests/test_kora_studio_browser_keyboard_smoke.py`: 5 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 159 passed, 143 deselected
- `python3 -m pytest`: 302 passed

Optional validation:

- `python3 scripts/check_kora_studio_preview.py --base-url http://127.0.0.1:8768`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 KORA_STUDIO_BROWSER_CSP_PORT=8766 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 KORA_STUDIO_BROWSER_KEYBOARD_PORT=8767 scripts/check_kora_studio_browser_keyboard_ci_optional.sh`: passed against the local Studio server

## Next Recommended Goal

Goal 545G - KORA Studio Optional Browser Keyboard Smoke Stability Documentation.

The next goal should document the exact boundaries of the optional browser keyboard smoke so future contributors know which checks are automated and which remain manual-only.
