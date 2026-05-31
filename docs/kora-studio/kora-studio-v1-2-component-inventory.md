# KORA Studio v1.2 Component Inventory

## Purpose

This inventory records stable component markers for the current embedded KORA Studio local preview shell.

The markers prepare future extraction work by giving tests and contributors stable ownership points before large HTML, CSS, or JavaScript blocks are moved into render helpers or local template fragments.

This task does not extract components yet and does not change runtime behavior.

## Marker Contract

Current component markers use `data-kora-component`.

The marker contract is:

- marker names are stable enough for tests and smoke checks
- markers identify render-section ownership
- markers do not imply a framework component exists yet
- markers do not change endpoint behavior
- markers do not add user-visible product behavior
- markers do not add dependencies

## Component List

| Component marker | Current location | Intended future extraction target | Boundary notes |
|---|---|---|---|
| `shell-layout` | Root final shell container rendered by `kora/studio_shell_render.py` | Shell layout render helper | Local preview/demo only |
| `left-rail` | Left mini rail `<aside>` rendered by `kora/studio_shell_render.py` | Left rail render helper | Local workspace only; no cloud sync |
| `top-model-selector` | Top catalog estimate `<details>` selector rendered by `kora/studio_shell_render.py` | Model selector render helper | Catalog estimates only; no install, download, or execution |
| `composer` | Centered composer stage | Composer render helper | Approved harness request action only |
| `selected-run-summary` | Composer selected-run summary rendered by `kora/studio_selected_run_render.py` | Selected-run summary render helper | Browser-local selected-run state only |
| `boundary-strip` | Shell boundary strip | Boundary/status render helper | Provider, cloud, download, model execution, and report export remain disabled |
| `right-details-drawer` | Right details drawer `<aside>` rendered by `kora/studio_drawer_render.py` | Drawer render helper | Diagnostics only; not a provider/runtime/model control panel |
| `approved-request-selector` | Approved request selector panel | Harness selector render helper | Approved request IDs only; no arbitrary prompt input |
| `retry-error-state` | Selected-run error/retry panel | Retry/error render helper | Retry last approved request only |
| `run-history` | Browser-local history panel | Run history render helper | Page memory only; no persistence or backend deletion |
| `generated-event-stream-status` | Generated event stream status panel rendered by `kora/studio_selected_run_render.py` | Event stream status render helper | Generated harness events only; no token/provider stream |
| `selected-run-event-timeline` | Selected-run event timeline panel rendered by `kora/studio_selected_run_render.py` | Selected-run timeline render helper | Not model token streaming; no provider output |
| `selected-run-counters` | Selected-run counters panel rendered by `kora/studio_selected_run_render.py` | Selected-run counters render helper | Not production telemetry; no cost or energy claim |
| `selected-run-comparison` | Selected-run comparison panel rendered by `kora/studio_selected_run_render.py` | Selected-run comparison render helper | Not production cost evidence; no real model execution |
| `selected-run-report-metadata` | Selected-run report metadata panel rendered by `kora/studio_selected_run_render.py` | Selected-run report metadata render helper | Preview only; no file export or writing |
| `legacy-compatibility-reference` | Collapsed legacy detailed preview `<details>` | Legacy reference render helper or later safe removal plan | Secondary developer/reference scaffold only |

## Extraction Status

Task 483 started shell extraction by adding `kora/studio_shell_render.py` with `render_shell_layout(...)`.

Task 484 continued extraction by adding `kora/studio_drawer_render.py` with `render_right_details_drawer(...)`.

Task 485 continued extraction by adding `kora/studio_selected_run_render.py` with selected-run summary, state, event stream, timeline, counters, comparison, and report metadata render helpers.

Task 486 continued extraction by adding `kora/studio_style_render.py` and `kora/studio_script_render.py` for embedded CSS and vanilla JavaScript template helpers.

Task 487 validated the extracted helper split in the [KORA Studio v1.2 extraction smoke check](kora-studio-v1-2-extraction-smoke-check.md).

Current split:

- `kora/studio_server.py` still owns endpoint routing, status assembly, harness data, and preview data preparation.
- `kora/studio_shell_render.py` owns the outer shell layout, left rail, top model selector, workspace frame, and slot placement for composer, details drawer, and legacy reference content.
- `kora/studio_drawer_render.py` owns the right details drawer diagnostic markup and marker contract.
- `kora/studio_selected_run_render.py` owns selected-run summary/state/detail panel markup and selected-run marker contracts.
- `kora/studio_style_render.py` owns the embedded local preview CSS template.
- `kora/studio_script_render.py` owns the embedded local preview vanilla JavaScript template.
- Composer container and legacy content remain in `kora/studio_server.py` until later v1.2 tasks.
- Behavior, endpoints, smoke markers, and claim boundaries are intended to remain unchanged.

## No-behavior-change Rule

Adding markers must not change:

- `/health`
- `/status`
- `/`
- `POST /api/harness/run`
- `GET /api/harness/run/<run_id>`
- `GET /api/harness/events?run_id=<id>`
- `GET /api/harness/sse?run_id=<id>`
- selected-run browser state behavior
- generated event stream fallback behavior
- legacy preview collapsed-by-default behavior

## No-dependency Rule

v1.2 component inventory does not add:

- frontend framework
- build step
- package install
- external script
- CDN asset
- new runtime dependency

## Test and Smoke Marker Expectations

Tests and smoke checks should verify:

- every required `data-kora-component` marker is present
- v1.0 shell-first markers remain present
- v1.1 shell-only hardening markers remain present
- no external script or CDN is introduced
- no arbitrary prompt input is introduced
- no model, provider, download, cloud, report export, private scan, or runtime-list behavior is introduced

## Claim Boundaries

The component inventory preserves:

- KORA Studio is local preview/demo readiness only.
- KORA Studio is not production-ready.
- KORA Studio is not an LM Studio replacement.
- No arbitrary prompt execution.
- No real model execution.
- No provider calls.
- No model downloads.
- No cloud sync.
- No private model directory scanning.
- No runtime model list commands.
- No report export or file writing.
- Generated harness data only.
- Not production telemetry.
- Not production cost evidence.
- No production cost reduction claim.
- No energy outcome claim.
- No unsupported larger-model execution claim.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.
