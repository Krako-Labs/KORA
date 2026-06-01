# KORA Studio v3.6 Retry and Error State Polish Report

## Status

KORA Studio v3.6 implements the fourth bounded UX improvement from the v3.2 primary operator path simplification plan.

The change adds shell-level retry guidance and a shell-visible Retry Last Approved Request action near the run progress and error state context. It does not change backend behavior, endpoint behavior, CSP behavior, static asset allowlist behavior, local harness behavior, or report behavior.

## Implemented UX Change

The final Studio shell now includes a Safe next action area inside the run progress summary.

The shell-level retry area communicates:

- what happened through the existing run progress error/status copy
- whether retry is available
- that retry uses only the last approved request ID
- that the operator should select an approved request when no retry target exists
- that diagnostics/details remain available for failure explanation

The shell-level retry button reuses the existing browser-local retry behavior. It calls the same approved-request-only local harness path as the existing lower diagnostic retry panel.

## Preserved Diagnostics

The existing lower retry/error diagnostics remain available:

- selected run error state card
- Retry Last Approved Request diagnostic card
- run history
- selected-run event timeline
- generated event stream status
- selected-run counters
- selected-run comparison
- selected-run report metadata
- details drawer diagnostics
- collapsed legacy compatibility preview

## Runtime Boundary

No backend route, API, provider path, model execution path, download path, cloud sync path, file export path, or report-writing path was added.

Retry remains browser-local UI behavior over the existing `POST /api/harness/run` endpoint with the last approved request ID only.

## Test Coverage

Dependency-light coverage was updated to verify:

- the rendered shell includes `data-kora-component="shell-retry-action"`
- the rendered shell includes `data-kora-retry-boundary="last-approved-request-only"`
- shell retry guidance and button IDs are present
- package JavaScript wires both retry buttons through `data-kora-retry-last-approved-request-button`
- package CSS includes shell retry selectors
- preview smoke markers include shell retry guidance
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
- `python3 -m pytest tests/test_kora_studio_server.py`: passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed

Optional validation:

- `python3 scripts/check_kora_studio_preview.py`: passed
- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed

The local Studio server used for the standard preview smoke check was stopped cleanly after validation.

## Next Recommended Goal

Goal 536G - KORA Studio Diagnostic Surface Rebalancing.

The next implementation should decide which diagnostic surfaces remain primary, which stay in the details drawer, and which remain in the collapsed legacy compatibility preview.
