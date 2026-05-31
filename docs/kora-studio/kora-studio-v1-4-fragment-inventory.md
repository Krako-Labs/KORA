# KORA Studio v1.4 Fragment Inventory

## Status

Task 497 inventory for KORA Studio v1.4 local preview fragment extraction.

This document classifies the next server-owned generated local harness preview fragments in `kora/studio_server.py`. It is a maintainability reference only. It does not add product behavior, endpoint behavior, static asset serving, frontend framework tooling, model execution, provider calls, downloads, cloud sync, report export, file writing, private directory scanning, runtime model listing, external network behavior, or production claims.

## Current Render Ownership

| Owner | Responsibility | Boundary |
|---|---|---|
| `kora/studio_server.py` | endpoint routing, status payload assembly, escaped display value preparation, local harness request/event/counter list assembly, model selector row assembly, final page assembly | may collect and escape local preview data; must not add provider/model/download/cloud/report export behavior |
| `kora/studio_shell_render.py` | shell layout, left rail, top model selector shell, model selector slot, composer slot, details drawer slot, legacy preview slot | pure string render helper; accepts server-prepared display values and slot HTML |
| `kora/studio_drawer_render.py` | right details drawer diagnostic panels | pure string render helper; accepts server-prepared display strings |
| `kora/studio_selected_run_render.py` | selected-run summary/state/detail containers for event stream status, selected timeline, counters, comparison, and report metadata | pure string render helper; owns stable selected-run ids and markers |
| `kora/studio_reference_render.py` | endpoint panel, limitations panel, and local references panel | pure string render helper; accepts escaped local path strings |
| `kora/studio_harness_request_render.py` | approved request selector cards, selected request preview card, Run Local Harness action card, selector option cards, and local harness trigger reference cards | pure string render helper; accepts escaped display strings and slot HTML |
| `kora/studio_legacy_render.py` | collapsed legacy compatibility preview opening wrapper | pure string render helper; keeps detailed body and closing assembly server-owned |
| `kora/studio_run_state_render.py` | selected-run retry/error panels, Retry Last Approved Request panel, browser-local run history panel, clear history panel, and dynamic history container | pure string render helper; accepts escaped approved request id |
| `kora/studio_style_render.py` | inline CSS template | pure string render helper; no external CSS path or CDN |
| `kora/studio_script_render.py` | inline vanilla JavaScript template | pure string render helper; local harness endpoints only |

`kora/studio_server.py` remains the data assembly boundary for v1.4. New helpers should receive pre-escaped display values or named slot HTML unless a later task explicitly documents a narrower local data contract.

## Fragment Classification

| Fragment | Current owner/evidence | Data source | Classification | v1.4 action | Boundary to preserve |
|---|---|---|---|---|---|
| Approved request selector intro card | `kora/studio_server.py`, `data-kora-component="approved-request-selector"` | static copy plus approved selector context | Safe to extract now | Include in Task 498 request/trigger helper candidate | approved request ids only; no arbitrary prompt execution |
| Selected request preview card | `kora/studio_server.py`, ids `kora-selected-request-id`, `kora-selected-request-text`, `kora-selected-request-route`, `kora-selected-request-model-needed` | first approved request, server-escaped display values | Safe to extract now | Include in Task 498 if helper accepts explicit escaped preview strings | selector state is browser-local page state only |
| Run Local Harness action card | `kora/studio_server.py`, id `kora-run-local-harness-button` | static endpoint copy and selected approved request state | Safe to extract now | Include in Task 498 | button sends approved `request_id` only; no arbitrary prompt text |
| Local harness selector option cards | `kora/studio_server.py`, `local_harness_selector_items` | `local_harness_requests` after server escaping | Safe to extract now with explicit contract | Include in Task 498 after preserving `request-option`, `data-kora-request-id`, and keyboard markers | local deterministic sample request data only |
| Run Local Harness action state reference cards | `kora/studio_server.py`, cards under local harness preview after selected-run panels | static endpoint and boundary copy | Safe to extract now | Include in Task 498 or keep as same helper footer | generated harness events only; no provider/model/download behavior |
| Retry/error state card | `kora/studio_server.py`, `data-kora-component="retry-error-state"` and id `kora-run-error-state` | static copy and browser-local JS ids | Safe to extract now | Include in Task 499 run state/history helper | retry uses last approved request only |
| Retry Last Approved Request card | `kora/studio_server.py`, ids `kora-last-approved-request-id`, `kora-retry-available`, `kora-retry-last-approved-request-button` | server-escaped selector preview id and browser-local JS state | Safe to extract now | Include in Task 499 with escaped preview id argument | no arbitrary prompt execution; POST uses approved request id only |
| Local Run History card | `kora/studio_server.py`, `data-kora-component="run-history"` and ids `kora-active-history-run-id`, `kora-run-history-count`, `kora-run-history-status` | static copy and browser-local JS state | Safe to extract now | Include in Task 499 | page-memory only; no persistence, cloud sync, file writing, or backend delete |
| Clear Local Run History card | `kora/studio_server.py`, id `kora-clear-run-history-button` | static copy and browser-local JS action | Safe to extract now | Include in Task 499 | clears browser-local preview state only |
| Local run history dynamic container | `kora/studio_server.py`, id `kora-local-run-history` | browser-local JS-rendered cards | Safe to extract now | Include in Task 499 as fixed empty container | no backend records, files, persistence, or report deletion |
| Local harness sample status/request/boundary cards | `kora/studio_server.py`, Local Harness Preview top grid | `local_harness_status`, sample request, claim boundary | Keep server-owned for data assembly | Defer extraction until request/trigger helper is stable | generated deterministic harness data only |
| Approved request list and harness event stage lists | `kora/studio_server.py`, `local_harness_request_items`, `local_harness_event_items` | request set and sample run events | Keep server-owned for data assembly | Defer until list helper contract is documented | local harness output only |
| Static generated timeline cards | `kora/studio_server.py`, `local_harness_timeline_items` | `local_harness_sample_run.events` | Keep server-owned for data assembly | Defer; possible later timeline helper after marker tests expand | not model token streaming; no model execution |
| Static generated counter cards | `kora/studio_server.py`, `local_harness_counter_items` | `local_harness_counters` | Keep server-owned for data assembly | Defer; possible later counter helper | not production telemetry; no cost or energy claim |
| Composer container | `kora/studio_server.py`, `composer_html` and `data-kora-component="composer"` | selected-run summary helper output and fixed composer ids | Defer to future frontend/static asset decision | Keep server-owned in v1.4 unless a later task narrows slot contract | approved local harness request only; no arbitrary prompt execution |
| Shell boundary strip | `kora/studio_server.py`, `data-kora-component="boundary-strip"` | static local-only boundary copy | Defer to future frontend/static asset decision | Keep inside composer slot for now | no provider calls, cloud sync, downloads, model execution, or report export |
| Selected-run shell strip | `kora/studio_server.py`, `data-kora-shell-selected-run-surface="v1.0"` | fixed ids updated by local JS | Defer to future frontend/static asset decision | Keep inside composer slot for now | generated local harness output only |
| Model selector item rows | `kora/studio_server.py`, `model_selector_items` slot into shell helper | recommended model catalog/status data | Defer to future frontend/static asset decision | Keep server-owned until catalog row escaping and selection behavior tests are expanded | catalog examples only; selection does not install, download, or execute |
| Legacy compatibility wrapper/body | `kora/studio_legacy_render.py` opening wrapper; `kora/studio_server.py` detailed body and closing assembly | wrapper around detailed reference sections | Partially extracted | Task 500 extracted the static opening wrapper only; keep body/closing server-owned | secondary developer/reference scaffold only |
| Launch/local status through setup/model boundary sections | `kora/studio_server.py`, detailed legacy section body | mixed status payload fields | Defer to future frontend/static asset decision | Keep server-owned; not a Task 498/499 target | local-only preview boundaries remain explicit |
| Execution Viewer legacy section | `kora/studio_server.py`, `h2>Execution Viewer` and `execution_event_items` | fixture/mock execution events | Keep server-owned for data assembly | Defer; possible later legacy helper only | fixture/mock events only; no runtime execution |
| Standard Mode vs KORA Boost legacy section | `kora/studio_server.py`, `standard_vs_kora_metric_items` | local comparison payload/metric cards | Keep server-owned for data assembly | Defer; possible later comparison reference helper | not production cost evidence; no model execution |
| Report Viewer Placeholder legacy section | `kora/studio_server.py`, `report_sections`, `report_warnings`, `report_counter_items` | report viewer placeholder and local harness metadata | Keep server-owned for data assembly | Defer; possible later report reference helper | metadata preview only; no file export or writing |
| Endpoint panel, limitations panel, local references panel | `kora/studio_reference_render.py` through `render_reference_panels()` | escaped docs/fixtures path display and static copy | Already extracted | No v1.4 extraction needed | local endpoints only; no provider/model/download endpoint |
| Selected-run summary/state/detail panels | `kora/studio_selected_run_render.py` | escaped selector preview id and static containers | Already extracted | No v1.4 extraction needed | selected-run output is generated local harness output only |
| Shell layout and details drawer | `kora/studio_shell_render.py`, `kora/studio_drawer_render.py` | server-provided display strings and slots | Already extracted | No v1.4 extraction needed | shell and drawer remain local preview only |
| Inline CSS and JavaScript templates | `kora/studio_style_render.py`, `kora/studio_script_render.py` | static inline templates | Already extracted | No v1.4 extraction needed | no external static assets, CDN, dependencies, or framework migration |

Task 498 update: the approved request selector intro card, selected request preview card, Run Local Harness action card, local harness selector option cards, and local harness trigger reference cards are now extracted into `kora/studio_harness_request_render.py`. `kora/studio_server.py` still owns status payload assembly, local harness request data selection, HTML escaping, `local_harness_requests_json`, and final helper placement.

Task 499 update: the selected-run retry/error state card, Retry Last Approved Request card, Local Run History card, Clear Local Run History card, and empty local run history dynamic container are now extracted into `kora/studio_run_state_render.py`. `kora/studio_server.py` still owns the escaped selector preview id and final helper placement. Browser-local run history behavior remains in inline JavaScript through `kora/studio_script_render.py`.

Task 500 update: the collapsed legacy compatibility preview opening wrapper is now extracted into `kora/studio_legacy_render.py`. The detailed legacy body, reference panels, closing `</details>` placement, approved requests JSON script, inline JavaScript, and final document assembly remain server-owned because they are still coupled to the large generated preview body.

## Task 500 Legacy Wrapper Decision

Task 500 reassessed the legacy compatibility wrapper and extracted only the safe static opening wrapper.

Helper module:

- `kora/studio_legacy_render.py`

Helper responsibility:

- render the collapsed `<details class="legacy-preview">` opening wrapper
- preserve `data-kora-component="legacy-compatibility-reference"`
- preserve collapsed-by-default marker attributes
- preserve secondary developer/reference scaffold copy and local-only boundary text

Still server-owned:

- detailed legacy preview body sections from Launch / Local-only Status through Report Viewer Placeholder
- `render_reference_panels(...)` placement
- closing `</details>` placement
- approved request JSON script placement
- inline JavaScript placement
- final page assembly

The helper does not add product behavior, endpoint behavior, frontend framework tooling, external static assets, provider calls, model execution, downloads, cloud sync, report export, file writing, or arbitrary prompt handling.

## Recommended Task 498 Target

Task 498 extracted only the request selector and local harness trigger markup that was low-risk and marker-bound.

Helper module:

- `kora/studio_harness_request_render.py`

Helper responsibilities:

- render the approved request selector intro card
- render the selected request preview card from escaped preview strings
- render the Run Local Harness action card
- render local harness selector option cards from pre-escaped item fields
- render the static trigger boundary/result surface cards from slot HTML

Required markers and ids to preserve:

- `data-kora-component="approved-request-selector"`
- `kora-selected-request-id`
- `kora-selected-request-text`
- `kora-selected-request-route`
- `kora-selected-request-model-needed`
- `kora-run-local-harness-button`
- `request-option`
- `data-kora-keyboard-selectable-request="true"`
- `data-kora-request-id`

The helper does not accept arbitrary prompt text, call endpoints, read files, execute models, call providers, add downloads, or add new dependencies.

## Recommended Task 499 Target

Task 499 extracted browser-local retry, error, and run history markup after Task 498 stabilized the request/trigger helper.

Helper module:

- `kora/studio_run_state_render.py`

Helper responsibilities:

- render selected-run error state panel
- render retry last approved request panel from an escaped preview request id
- render local run history panel
- render clear local run history panel
- render the empty local run history dynamic container

Required markers and ids to preserve:

- `data-kora-component="retry-error-state"`
- `kora-run-error-state`
- `kora-last-approved-request-id`
- `kora-retry-available`
- `kora-retry-last-approved-request-button`
- `data-kora-component="run-history"`
- `kora-active-history-run-id`
- `kora-run-history-count`
- `kora-run-history-status`
- `kora-clear-run-history-button`
- `kora-local-run-history`

The helper preserves browser-local page-memory semantics. It does not add persistence, backend delete calls, file writing, report export, cloud sync, provider calls, model execution, downloads, or arbitrary prompt handling.

## Data Assembly Boundary

For v1.4, `kora/studio_server.py` should continue to own:

- endpoint routing and response writing
- status payload assembly
- local harness request, run, event, comparison, and report metadata assembly
- model catalog/status assembly
- HTML escaping of dynamic display values
- final page assembly and helper slot placement

Render helpers should own only deterministic HTML strings from supplied arguments. They should preserve stable markers, ids, accessibility labels, and local-only boundary text.

Task 501 helper contract and marker coverage hardening is documented in [KORA Studio v1.4 render helper contracts](kora-studio-v1-4-render-helper-contracts.md).

## Validation Expectations

Task 497 is docs-only, but subsequent extraction tasks should preserve:

- preview marker coverage for request selector, selected-run, retry/error, run history, and reference panels
- JavaScript endpoint constraints: local harness run/events/generated SSE only
- absence of arbitrary prompt input
- absence of external scripts, CDN, external CSS, static asset routes, or new dependencies
- absence of provider/model/download/report export endpoint calls
- endpoint behavior for `/health`, `/status`, `/`, `POST /api/harness/run`, `GET /api/harness/run/<run_id>`, `GET /api/harness/events?run_id=<id>`, and `GET /api/harness/sse?run_id=<id>`

## Claim Boundaries

All v1.4 inventory and extraction work must preserve:

- KORA Studio is local preview/demo readiness only.
- KORA Studio is not production-ready.
- KORA Studio is not an LM Studio replacement.
- Generated harness data only.
- No arbitrary prompt execution.
- No model execution.
- No provider calls.
- No model downloads.
- No cloud sync.
- No private model directory scanning.
- No runtime model list commands.
- No report export.
- No file writing.
- No external static assets or CDN.
- No frontend framework migration.
- No dependency addition.
- Not production telemetry.
- Not production cost evidence.
- No production cost reduction claim.
- No energy outcome claim.
- No unsupported larger-model execution claim.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.
