# KORA Studio v3.9 Keyboard and Screen-Reader Spot Check Report

## Status

KORA Studio v3.9 completes a bounded keyboard and screen-reader interaction spot check for the primary local demo path.

The change keeps backend behavior, endpoint behavior, local harness behavior, CSP behavior, and static asset allowlist behavior unchanged.

## Reviewed Interactions

The spot check reviewed:

- approved request selector buttons
- primary composer Run Local Harness button
- lower Run Local Harness button
- shell Retry Last Approved Request button
- lower retry button
- details drawer open and close controls
- left rail open and close controls
- legacy compatibility details surface
- primary run progress and result summary live regions

## Findings

No blocker was found for the current local preview/demo scope.

Important but not blocking:

- closed overlay surfaces should not leave hidden controls in the keyboard tab order
- selected approved request buttons should expose current selection state beyond `aria-pressed`
- future work should perform manual keyboard traversal and screen-reader spot checks in a real browser

Cosmetic:

- the local preview still uses simple text controls for shell toggles and local harness actions

## Implemented Frontend Improvements

Small frontend-shell fixes were added:

- the details drawer is initially closed with `inert`
- details drawer JavaScript removes `inert` when opened and restores it when closed
- mobile left rail JavaScript applies `inert` when the rail is closed and hidden from assistive technologies
- approved request selector buttons now start with `aria-current="false"`
- selected approved request JavaScript now updates both `aria-pressed` and `aria-current`
- accessibility state exposed for smoke/debug inspection now includes left rail and details drawer inert state

## Preserved Behavior

- no backend route or API changed
- no local harness request or run behavior changed
- no provider call path was added
- no model execution path was added
- no download, cloud sync, report export, or file writing path was added
- no CSP or static asset allowlist behavior changed
- no dependency, browser framework config, package manifest, lockfile, frontend build tooling, or axe tooling was added

## Test Coverage

Dependency-light coverage now verifies:

- approved request buttons include `aria-current`
- selected request JavaScript updates `aria-current`
- closed details drawer has the inert keyboard boundary marker
- shell JavaScript toggles `inert` on overlay surfaces
- exposed accessibility state includes left rail and details drawer inert fields
- standard preview smoke checks include the keyboard/screen-reader spot-check markers
- existing browser CSP smoke and static asset guard tests remain intact

## Claim Boundary Check

- KORA Studio remains local preview/demo readiness only.
- This is a bounded keyboard/screen-reader spot check only.
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

Goal 539G - KORA Studio Manual Browser Keyboard Traversal Report.

The next goal should use the existing optional browser smoke path or a manual checklist to verify actual Tab, Enter, Space, and Escape behavior across the primary path, details drawer, left rail, and approved request selector.
