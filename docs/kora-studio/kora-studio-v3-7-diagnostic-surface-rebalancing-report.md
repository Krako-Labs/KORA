# KORA Studio v3.7 Diagnostic Surface Rebalancing Report

## Status

KORA Studio v3.7 implements the fifth bounded UX improvement from the v3.2 primary operator path simplification plan.

The change makes lower diagnostic surfaces visually and semantically secondary while preserving the diagnostic information. It does not change backend behavior, endpoint behavior, CSP behavior, static asset allowlist behavior, local harness behavior, or report behavior.

## Implemented UX Change

The final Studio shell keeps these surfaces primary:

- primary workflow band
- run progress summary
- Safe next action retry guidance
- primary result summary

The following surfaces remain available but are marked as secondary diagnostics:

- selected run state mirror
- generated event stream detail
- selected-run event timeline
- selected-run counters
- selected-run comparison
- selected-run report metadata
- lower retry/error diagnostic panels
- browser-local run history and clear-state panels

## Rebalancing Approach

No diagnostic information was removed. Instead, secondary diagnostic surfaces now use:

- `data-kora-diagnostic-hierarchy="secondary"`
- `secondary-diagnostic-card`
- copy that labels the area as secondary diagnostic detail
- CSS that visually lowers the card weight relative to the primary shell surfaces

The collapsed legacy compatibility preview remains secondary/reference-only.

## Runtime Boundary

No backend route, API, provider path, model execution path, download path, cloud sync path, file export path, or report-writing path was added.

The rebalancing is server-rendered HTML and package CSS only.

## Test Coverage

Dependency-light coverage was updated to verify:

- secondary diagnostic hierarchy markers render
- secondary diagnostic card styling is present
- selected-run timeline/counter/comparison/report metadata remain available
- lower retry/error and run-history diagnostics remain available
- smoke markers include the secondary hierarchy labels
- CSP/resource guard coverage remains in the existing server tests

## Claim Boundary Check

- KORA Studio remains local preview/demo readiness only.
- This is a UX-only frontend shell improvement.
- KORA Studio is not production-ready.
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
- KORA still does not remove RAM, VRAM, unified-memory, or model-loading requirements.

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

Goal 537G - KORA Studio Primary Path Responsive and Accessibility Check.

The next goal should validate the simplified primary path across narrow/mobile layout and basic keyboard/screen-reader interaction.
