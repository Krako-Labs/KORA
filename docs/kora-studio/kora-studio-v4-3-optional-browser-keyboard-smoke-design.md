# KORA Studio v4.3 Optional Browser Keyboard Smoke Design

## Status

KORA Studio v4.3 designs the future optional browser keyboard smoke now that the v4.2 selector contract exists.

Decision: do not add the browser keyboard smoke script in this milestone. The design is stable enough to implement later as an explicitly gated transient Playwright smoke, but no new script, wrapper, dependency, package manifest, lockfile, Playwright config, axe tooling, frontend build tooling, external asset, or CDN is added here.

## Inputs Reviewed

Reviewed implementation and validation surfaces:

- `docs/kora-studio/kora-studio-v4-2-keyboard-selector-contract.md`
- `scripts/check_kora_studio_browser_csp.py`
- `scripts/check_kora_studio_browser_csp_ci_optional.sh`
- `tests/test_kora_studio_browser_csp_smoke.py`
- Studio shell keyboard selector markers in the render helpers

The existing browser CSP smoke already proves a real browser can load the Studio shell, local CSS, local JavaScript, and Run Local Harness interaction under the enforced root CSP. A future keyboard smoke should reuse that transient `npx --package @playwright/test` shape and remain outside default pytest.

## Future Optional Smoke Shape

Candidate future command:

```bash
KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 scripts/check_kora_studio_browser_keyboard_ci_optional.sh
```

The wrapper should:

- require explicit opt-in through `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1`
- start `python3 -m kora studio --no-browser` on a local port
- wait for `/health`
- run a transient Playwright spec through `npx --yes --package @playwright/test`
- remove temporary files after execution
- leave normal pytest and default CI dependency-light

The Python script should accept only `http://127.0.0.1` or `http://localhost` base URLs, matching the browser CSP smoke boundary.

## Stable Assertions for Future Automation

These assertions are stable enough for a future transient Playwright script:

- root loads with HTTP 200
- root exposes `data-kora-keyboard-selector-contract="v4.2"`
- `window.koraStudioScriptStatus.status === "ready"`
- no page errors, browser CSP violations, or failed same-origin requests occur
- `[data-kora-keyboard-contract="model-selector"]` is attached
- `[data-kora-keyboard-contract="details-drawer-toggle"]` is visible and starts with `aria-expanded="false"`
- `[data-kora-keyboard-contract="approved-request-option"]` is attached and starts with `aria-pressed="false"` and `aria-current="false"`
- keyboard activation of the first approved request updates it to `aria-pressed="true"` and `aria-current="true"`
- `[data-kora-keyboard-contract="primary-run-local-harness"]` is visible and can be activated by keyboard
- after Run Local Harness, selected run state reaches a generated completed state
- `[data-kora-keyboard-contract="run-progress-summary"]` remains visible
- `[data-kora-keyboard-contract="primary-result-summary"]` remains visible
- `[data-kora-keyboard-contract="shell-retry-last-approved-request"]` becomes enabled only after an approved request run target exists
- opening `[data-kora-keyboard-contract="details-drawer-toggle"]` sets the drawer open state, moves focus to `[data-kora-keyboard-contract="details-drawer-close"]`, and Escape closes the drawer
- after Escape closes the drawer, focus returns to `[data-kora-keyboard-contract="details-drawer-toggle"]`

These checks validate the primary local demo path without claiming accessibility certification.

## Mobile Rail Automation Scope

Mobile rail checks are feasible but should be a second phase inside the future optional smoke:

- set a narrow viewport, for example 390 by 844
- assert `[data-kora-keyboard-contract="mobile-rail-toggle"]` is visible
- activate the rail toggle by keyboard
- assert `[data-kora-keyboard-contract="mobile-left-rail"]` reports open state
- assert focus reaches `[data-kora-keyboard-contract="mobile-rail-close"]`
- press Escape
- assert focus returns to `[data-kora-keyboard-contract="mobile-rail-toggle"]`

This should remain optional because viewport handling and browser focus behavior are more brittle than the desktop primary path.

## Manual-Only Assertions for Now

Keep these checks manual-only for now:

- exact full-page Tab order across every secondary diagnostic and legacy/reference surface
- visual focus ring quality across all browsers
- screen reader announcement wording
- timing-sensitive live-region announcement behavior
- keyboard interaction inside every collapsed or secondary diagnostic surface
- any production accessibility conformance claim

These require human review or dedicated accessibility tooling, neither of which belongs in the current dependency-light local preview scope.

## Non-Goals

Do not add in the future implementation unless a separate goal explicitly approves it:

- package manifests or lockfiles
- persistent Playwright dependency
- Playwright config
- axe tooling
- frontend build tooling
- external assets or CDN
- default pytest dependency on browser installation
- production accessibility certification claims

## Preserved Boundaries

- no browser keyboard smoke script was added
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
- no production telemetry, production cost evidence, cost reduction claim, or energy outcome claim

## Validation Results

Required validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: 72 passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: 4 passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: 5 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 154 passed, 143 deselected
- `python3 -m pytest`: 297 passed

Optional validation:

- `python3 scripts/check_kora_studio_preview.py --base-url http://127.0.0.1:8766`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed against the local Studio server

## Next Recommended Goal

Goal 543G - KORA Studio Optional Browser Keyboard Smoke Implementation.

The next goal can implement the explicitly gated optional browser keyboard smoke using this design and the v4.2 selector contract, while keeping it outside default pytest and default CI.
