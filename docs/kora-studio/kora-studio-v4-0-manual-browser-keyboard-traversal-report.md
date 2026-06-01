# KORA Studio v4.0 Manual Browser Keyboard Traversal Report

## Status

KORA Studio v4.0 adds a bounded manual browser keyboard traversal report for the primary local demo path.

This is a documentation and validation milestone. It does not change runtime behavior, backend routes, local harness behavior, CSP behavior, static asset allowlist behavior, dependencies, or frontend tooling.

## Scope

The traversal checklist covers:

- initial page load
- approved request selection
- Run Local Harness controls
- run progress and result summary
- Retry Last Approved Request
- details drawer open and close
- mobile left rail open and close
- diagnostic surfaces and collapsed legacy/reference surfaces

The report uses the existing dependency-light tests and the optional browser CSP smoke path as supporting evidence. It does not add persistent browser tooling or claim production accessibility certification.

## Manual Traversal Checklist

### 1. Initial Page Load

Expected keyboard behavior:

- Tab starts on shell-level controls before lower diagnostic/reference content.
- Visible focus styling appears on focusable shell controls.
- Closed details drawer is not reachable until opened.
- On narrow/mobile layouts, the closed left rail is hidden from assistive technology and should not be reachable until opened.

Expected screen-reader signals:

- primary shell has a clear local preview boundary
- primary workflow is exposed as an ordered list
- run progress and result summary are polite atomic status regions
- details drawer is closed and marked hidden until opened

Finding: no blocker.

### 2. Approved Request Selection

Expected keyboard behavior:

- approved request buttons are reachable with Tab
- Enter or Space activates a selected approved request button
- visible focus styling remains present
- selected state updates without requiring pointer input

Expected screen-reader signals:

- request buttons have explicit names that include the approved request id
- selected request state is represented through `aria-pressed`
- current request state is represented through `aria-current`

Finding: no blocker.

### 3. Run Local Harness

Expected keyboard behavior:

- primary composer Run Local Harness button is reachable with Tab
- lower Run Local Harness button remains available in the detailed preview/reference area
- activation submits only the selected approved request id
- while loading, run buttons are disabled and do not create a second submit path

Expected screen-reader signals:

- Run Local Harness controls include descriptive boundary text
- status updates appear in the run progress live region
- result summary updates remain within generated local harness boundaries

Finding: no blocker.

### 4. Run Progress and Result Summary

Expected keyboard behavior:

- no keyboard-only action is required to read primary run progress after activation
- primary result summary appears before lower diagnostics in document order
- lower diagnostic surfaces remain reachable after primary result surfaces

Expected screen-reader signals:

- run progress announces idle/running/completed/error state as plain local preview status
- result summary announces generated local harness output only
- comparison/report metadata wording avoids production telemetry or production evidence claims

Finding: no blocker.

### 5. Retry Last Approved Request

Expected keyboard behavior:

- shell Retry Last Approved Request is reachable when enabled
- lower diagnostic retry remains available but secondary
- disabled retry controls are skipped or announced as disabled by the browser
- retry reuses only the last approved request id

Expected screen-reader signals:

- retry guidance text describes the safe next action
- retry button is described by the shell retry guidance and retry boundary note
- error states preserve no-model, no-provider, no-download boundaries

Finding: no blocker.

### 6. Details Drawer Open and Close

Expected keyboard behavior:

- Details button is reachable from the top bar
- Enter or Space opens the drawer
- opening the drawer moves focus to the close button
- Escape closes the drawer
- close button closes the drawer and returns focus to the Details button
- closed drawer is inert and not reachable in the tab sequence

Expected screen-reader signals:

- Details button exposes `aria-controls` and `aria-expanded`
- drawer exposes hidden/open state through `aria-hidden`
- closed drawer has an explicit inert keyboard boundary marker

Finding: no blocker.

### 7. Mobile Left Rail Open and Close

Expected keyboard behavior:

- Menu button is visible and reachable on narrow/mobile layout
- Enter or Space opens the left rail
- opening the rail moves focus to the close button
- Escape closes the rail
- close button closes the rail and returns focus to the Menu button
- closed mobile rail is hidden and inert

Expected screen-reader signals:

- Menu button exposes `aria-controls` and `aria-expanded`
- left rail state is kept in sync with `aria-hidden` and inert behavior on narrow layouts

Finding: important but not blocker.

Rationale: automated browser smoke does not currently drive a narrow viewport keyboard traversal. The implementation has state markers and inert handling, but a future visual/manual mobile pass should confirm actual browser behavior.

### 8. Diagnostic and Collapsed Reference Surfaces

Expected keyboard behavior:

- secondary diagnostics remain reachable after the primary path
- legacy/reference details surface remains collapsed by default
- opening the collapsed reference surface is optional and not required for the primary run path

Expected screen-reader signals:

- diagnostics are labeled secondary where appropriate
- legacy/reference surface copy says it is not required for first-run understanding

Finding: no blocker.

## Findings Summary

Blocker:

- none found for the current local preview/demo scope

Important but not blocker:

- narrow/mobile left rail should receive a future real-browser keyboard traversal pass
- optional browser smoke validates Run Local Harness interaction under CSP but does not yet automate full Tab order assertions

Cosmetic:

- simple text labels such as Menu, Details, and Retry remain acceptable for the local preview shell, but could be visually refined later

## Supporting Validation Approach

The existing optional browser CSP smoke is still the appropriate dependency-light browser-level check for now:

```bash
KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh
```

It validates local asset loading, CSP compatibility, visible shell controls, and Run Local Harness browser interaction without adding persistent dependencies.

## Claim Boundary Check

- KORA Studio remains local preview/demo readiness only.
- This is a bounded manual keyboard traversal report only.
- KORA Studio is not production-ready.
- KORA Studio is not production accessibility certification.
- KORA Studio is not an LM Studio replacement.
- No arbitrary prompt execution was added.
- No real model execution was added.
- No provider calls were added.
- No model downloads were added.
- No cloud sync was added.
- No private model directory scanning was added.
- No runtime model list commands were added.
- No report export or file writing was added.
- No production telemetry, production cost evidence, cost reduction claim, or energy outcome claim was added.

## Validation Results

Required validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: 71 passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: 4 passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: 5 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 153 passed, 143 deselected
- `python3 -m pytest`: 296 passed

Optional validation:

- `python3 scripts/check_kora_studio_preview.py`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed against the local Studio server

## Next Recommended Goal

Goal 540G - KORA Studio Optional Browser Keyboard Smoke Feasibility Plan.

The next goal should decide whether to extend the existing transient Playwright smoke with a small keyboard traversal check, while keeping it explicitly optional and outside the default dependency-light test path.
