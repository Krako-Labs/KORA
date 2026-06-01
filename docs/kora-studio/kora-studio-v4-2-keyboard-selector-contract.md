# KORA Studio v4.2 Keyboard Selector Contract

## Status

KORA Studio v4.2 defines the stable selector and focus-state contract needed before adding a future optional browser keyboard smoke.

This milestone adds explicit `data-kora-keyboard-contract` markers to existing Studio shell controls and diagnostic surfaces. It does not add a browser keyboard smoke script.

## Selector Contract

The root shell exposes:

- `data-kora-keyboard-selector-contract="v4.2"`

Stable keyboard smoke selector names:

- `mobile-left-rail`
- `mobile-rail-toggle`
- `mobile-rail-close`
- `model-selector`
- `details-drawer-toggle`
- `details-drawer`
- `details-drawer-close`
- `primary-run-local-harness`
- `approved-request-selector`
- `approved-request-option`
- `lower-run-local-harness`
- `run-progress-summary`
- `shell-retry-last-approved-request`
- `primary-result-summary`
- `secondary-diagnostics-status`
- `secondary-generated-event-stream`
- `secondary-event-timeline`
- `secondary-run-counters`
- `secondary-run-comparison`
- `secondary-report-metadata`
- `secondary-retry-last-approved-request`

These selectors are intended for future optional browser keyboard smoke coverage. They are not presentation hooks and should not replace existing component markers.

## Desktop Focus Expectations

Expected desktop keyboard states:

- the model selector remains keyboard reachable through its native `details`/`summary` behavior
- the details drawer toggle exposes `aria-controls="kora-details-drawer"` and starts with `aria-expanded="false"`
- opening the details drawer should make the drawer available, focus the close button, and allow Escape to close it
- closing the details drawer should restore focus to the details drawer toggle
- approved request options expose `aria-pressed="false"` and `aria-current="false"` until selected
- keyboard activation of an approved request should update the selected request state
- Run Local Harness controls remain bounded to approved local harness request IDs
- Retry Last Approved Request starts disabled and becomes available only after an approved request run target exists
- run progress and result summary remain polite atomic live-region surfaces

## Narrow and Mobile Focus Expectations

Expected narrow/mobile keyboard states:

- the mobile rail toggle exposes `aria-controls="kora-left-rail"` and starts with `aria-expanded="false"`
- the mobile left rail starts in the closed state and can be opened from the Menu control
- opening the rail should focus the rail close button
- Escape should close the open rail and restore focus to the rail toggle
- closed mobile rail and closed details drawer controls should not create hidden overlay focus traps
- approved request selection, Run Local Harness, retry, progress, result, and diagnostics selectors remain the same as desktop

## Dependency-Light Guard Coverage

The selector contract is guarded by static server and preview smoke tests:

- root contract version marker
- stable selector names for primary controls
- stable selector names for overlays
- stable selector names for primary progress/result surfaces
- stable selector names for secondary diagnostic surfaces
- initial `aria-expanded`, `aria-pressed`, `aria-current`, `aria-hidden`, and `inert` assumptions where relevant
- live-region markers for progress and result summaries

No browser keyboard smoke script was added in this milestone.

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
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 154 passed, 143 deselected
- `python3 -m pytest`: 297 passed

Optional validation:

- `python3 scripts/check_kora_studio_preview.py`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed against the local Studio server

## Next Recommended Goal

Goal 542G - KORA Studio Optional Browser Keyboard Smoke Design.

The next goal should use this selector contract to design, but not necessarily implement, the explicitly gated optional browser keyboard smoke.
