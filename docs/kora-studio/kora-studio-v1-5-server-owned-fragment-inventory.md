# KORA Studio v1.5 Server-Owned Fragment Inventory

## Purpose

This inventory captures the remaining `kora/studio_server.py` UI/data-display responsibilities after KORA Studio v1.4.

v1.5 is a maintainability/refactor milestone. This inventory does not implement behavior changes, endpoint changes, product capability changes, dependency changes, external static asset serving, frontend framework tooling, model execution, provider calls, downloads, cloud sync, report export/file writing, private model directory scanning, runtime model listing, external network behavior, or production claims.

## Current Source of Truth

Public truth:

- `origin/main`

Current v1.5 baseline:

- v1.4 completed at `4392696935beab6749b0867554160f1671780f3c`
- v1.5 plan added at `20144d1809c8c0500df7c5ef47ba328ddeede084`

Relevant implementation files:

- `kora/studio_server.py`
- `kora/studio_shell_render.py`
- `kora/studio_drawer_render.py`
- `kora/studio_selected_run_render.py`
- `kora/studio_reference_render.py`
- `kora/studio_harness_request_render.py`
- `kora/studio_run_state_render.py`
- `kora/studio_legacy_render.py`
- `kora/studio_status_boundary_render.py`
- `kora/studio_style_render.py`
- `kora/studio_script_render.py`

Relevant verification files:

- `tests/test_kora_studio_server.py`
- `tests/test_kora_studio_preview_smoke.py`
- `scripts/check_kora_studio_preview.py`

## Classification Legend

- `should remain server-owned`: endpoint routing, status/data assembly, dynamic escaping, JSON embedding, and final document assembly.
- `safe to extract now`: display-only HTML fragments with primitive/string inputs, stable markers/copy, and no endpoint or data assembly logic.
- `defer`: fragments tied to final document assembly, static asset strategy, broader frontend architecture, or mixed data/display responsibilities that need a later decision.
- `already extracted`: fragments currently owned by render helper modules.

## Server-Owned Responsibilities That Should Remain Server-Owned

| Responsibility | Current owner | Classification | Reason |
|---|---|---|---|
| `/health`, `/status`, `/`, `/api/harness/run`, `/api/harness/run/<run_id>`, `/api/harness/events`, `/api/harness/sse` routing | `kora/studio_server.py` | should remain server-owned | Endpoint routing belongs to the local standard-library server and must not move into render helpers. |
| JSON response writing | `kora/studio_server.py` | should remain server-owned | Response serialization and HTTP headers are server behavior. |
| HTML response writing | `kora/studio_server.py` | should remain server-owned | Response serialization and HTTP headers are server behavior. |
| SSE response writing | `kora/studio_server.py` | should remain server-owned | Generated SSE formatting endpoint behavior must remain server-owned. |
| Request body parsing | `kora/studio_server.py` | should remain server-owned | Input parsing is endpoint behavior, not display rendering. |
| Local status payload assembly | `get_studio_server_status()` | should remain server-owned | It joins system profile, runtime status, model catalog, local harness, comparison, and report metadata. |
| Local harness run creation/retrieval calls | `kora/studio_server.py` | should remain server-owned | Run trigger/retrieval is endpoint behavior. |
| Local harness run event/SSE retrieval calls | `kora/studio_server.py` | should remain server-owned | Event retrieval and SSE response logic are endpoint behavior. |
| Dynamic HTML escaping in `render_studio_placeholder_html()` | `kora/studio_server.py` | should remain server-owned for now | Existing helpers receive escaped display strings; moving escaping needs a separate contract decision. |
| Local approved request JSON embedding | `kora/studio_server.py` | should remain server-owned | The script data payload is coupled to selected-run JavaScript behavior. |
| Final document assembly | `kora/studio_server.py` | defer | The final `<!doctype html>` wrapper, inline style/script placement, shell insertion, legacy wrapper closing, and body close remain coupled. |

## Already Extracted Display Fragments

| Fragment | Helper owner | Evidence |
|---|---|---|
| Shell layout, left rail, top model selector shell, shell workspace | `kora/studio_shell_render.py` | `render_shell_layout()` |
| Right details drawer | `kora/studio_drawer_render.py` | `render_right_details_drawer()` |
| Selected-run summary | `kora/studio_selected_run_render.py` | `render_selected_run_summary_panel()` |
| Selected-run state/detail panels | `kora/studio_selected_run_render.py` | `render_selected_run_state_panel()`, `render_selected_run_detail_panels()` |
| Endpoint/limitations/local references panels | `kora/studio_reference_render.py` | `render_reference_panels()` |
| Approved request selector and selected request preview | `kora/studio_harness_request_render.py` | `render_local_harness_request_selector_panels()` |
| Local harness trigger reference panels | `kora/studio_harness_request_render.py` | `render_local_harness_trigger_reference_panels()` |
| Retry/error state and browser-local run history panels | `kora/studio_run_state_render.py` | `render_run_state_history_panels()` |
| Collapsed legacy preview opening wrapper | `kora/studio_legacy_render.py` | `render_legacy_preview_opening()` |
| Shell boundary strip | `kora/studio_status_boundary_render.py` | `render_shell_boundary_strip()` |
| Launch/local-only status section | `kora/studio_status_boundary_render.py` | `render_launch_local_status_section()` |
| KORA Boost Boundary section | `kora/studio_status_boundary_render.py` | `render_kora_boost_boundary_section()` |
| Inline CSS template | `kora/studio_style_render.py` | `render_studio_css()` |
| Inline vanilla JavaScript template | `kora/studio_script_render.py` | `render_studio_javascript()` |

## Remaining Server-Owned UI/Data-Display Fragments

| Fragment | Current location | Classification | Extraction notes |
|---|---|---|---|
| Model selector item rows | `render_studio_placeholder_html()` | safe to extract now | Display-only repeated row markup. Keep filtering and escaping server-owned; helper should accept pre-escaped primitive display fields or pre-rendered rows. Candidate for model/catalog/runtime helper. |
| Composer container | `render_studio_placeholder_html()` | safe to extract now | Display-only shell slot markup with selected-run summary slot. Preserve `data-kora-component="composer"` and shell selected-run surface markers. Candidate for status/boundary helper or shell-adjacent helper. |
| Shell selected-run strip | `render_studio_placeholder_html()` | safe to extract now | Display-only status strip. Preserve v1.0/v1.1 markers and local-only copy. Could be extracted with composer container. |
| Shell boundary strip | `kora/studio_status_boundary_render.py` | already extracted | Extracted in Task 507. Preserve provider/cloud/download/model/report-export coverage marker and copy. |
| Header hero copy | `render_studio_placeholder_html()` | safe to extract now | Display-only local preview header. Keep dynamic `boost_message` and technical explanation escaped by server. Low priority because it has fewer markers. |
| Launch/local-only status cards | `kora/studio_status_boundary_render.py` | already extracted | Extracted in Task 507. Display-only status/boundary cards. |
| First-run order card | `kora/studio_status_boundary_render.py` | already extracted | Extracted in Task 507. Display-only list from server-prepared `section_order_items`. |
| Your Computer section | `render_studio_placeholder_html()` | safe to extract now | Display-only system profile cards. Candidate for Task 508 if server retains system-profile data preparation and escaping. |
| Model Capability Estimate section | `render_studio_placeholder_html()` | safe to extract now | Display-only model capability cards. Candidate for Task 508. Preserve memory requirement claim boundary. |
| Runtime Status section | `render_studio_placeholder_html()` | safe to extract now | Display-only runtime/service/installed-detection cards. Candidate for Task 508. Preserve localhost-only and no-model-execution copy. |
| Catalog vs Installed section | `render_studio_placeholder_html()` | safe to extract now | Display-only catalog/runtime distinction cards. Candidate for Task 508. Server should keep recommendation filtering and escaping. |
| Setup Guidance section | `render_studio_placeholder_html()` | safe to extract now | Display-only status/boundary cards. Can join Task 508 or Task 507 depending grouping. |
| Disabled Download/Run Actions section | `render_studio_placeholder_html()` | safe to extract now | Display-only disabled action copy. Preserve disabled download/run wording. Candidate for Task 507 or Task 508. |
| KORA Boost Boundary section | `kora/studio_status_boundary_render.py` | already extracted | Extracted in Task 507. Display-only claim boundary cards preserve no memory-removal and provider/cloud-disabled copy. |
| Local Harness Preview status/sample/boundary cards | `render_studio_placeholder_html()` | safe to extract now | Display-only local harness summary cards. Candidate for Task 509. Keep local harness data assembly server-owned. |
| Available sample requests and harness event stages lists | `render_studio_placeholder_html()` | safe to extract now | Display-only lists assembled from server-prepared escaped list items. Candidate for Task 509. |
| Generated Event Timeline static header and generated sample cards | `render_studio_placeholder_html()` | safe to extract now | Display-only generated harness sample timeline. Candidate for Task 509. Preserve not-token-streaming/no-model/no-provider wording. |
| Generated Counters static header and generated counter cards | `render_studio_placeholder_html()` | safe to extract now | Display-only local harness counters. Candidate for Task 509. Preserve no cost/energy conversion wording. |
| Execution Viewer fixture section | `render_studio_placeholder_html()` | safe to extract now | Display-only fixture/mock section. Candidate for Task 509 only if kept separate from live harness display. Preserve no real model execution/provider/download wording. |
| Execution Viewer workflow steps | `render_studio_placeholder_html()` | safe to extract now | Static display-only workflow cards. Can be extracted with Execution Viewer fixture section. |
| Standard Mode vs KORA Boost section | `render_studio_placeholder_html()` | safe to extract now | Display-only local harness comparison cards and metric card slot. Candidate for Task 509 or later comparison helper. Preserve not production cost evidence/no cost or energy claim wording. |
| Report Viewer Placeholder section | `render_studio_placeholder_html()` | safe to extract now | Display-only report metadata and boundary cards. Candidate for Task 509 or later report helper. Preserve no file export/no file writing/not production evidence wording. |
| Legacy detailed preview body | `render_studio_placeholder_html()` | defer | Large compatibility scaffold body remains coupled to the final document and old section ordering. Extract only after safer smaller sections are complete. |
| Closing legacy wrapper and page close | `render_studio_placeholder_html()` | defer | Closing `</details>`, approved request JSON, inline script, body/html close are final assembly concerns. |

## Recommended Task 507 Candidate

Task 507 extracted the safest status/boundary display group:

- launch/local-only status cards
- first-run order card
- shell boundary strip
- KORA Boost Boundary section

Task 507 added `kora/studio_status_boundary_render.py`. Status payload assembly, first-run ordering, and dynamic escaping remain server-owned. Helper contract tests and rendered-preview marker/copy tests cover the new helper.

## Recommended Task 508 Candidate

Task 508 should extract model/catalog/runtime display fragments only if Task 507 passes cleanly:

- Your Computer section
- Model Capability Estimate section
- Runtime Status section
- Catalog vs Installed section
- Setup Guidance section
- Disabled Download/Run Actions section if not already extracted
- model selector item rows if a compact helper contract is clear

Keep model recommendation filtering, runtime status selection, installed-summary interpretation, and escaping in `kora/studio_server.py`.

## Recommended Task 509 Candidate

Task 509 should extract local harness display fragments after status/model extraction:

- Local Harness Preview status/sample/boundary cards
- available request and event-stage lists
- generated event timeline static/sample cards
- generated counters static cards
- Execution Viewer fixture section
- Standard Mode vs KORA Boost static/default comparison section
- Report Viewer Placeholder section

Keep local harness request/run/event/comparison/report metadata assembly in `kora/studio_server.py`.

## Deferred Decisions

Defer these areas until a later explicit goal:

- external static asset serving
- CSS or JavaScript file routing
- frontend framework migration
- moving dynamic escaping into helpers
- passing raw `/status` dictionaries into helpers
- extracting endpoint routing
- extracting status payload assembly
- extracting final document assembly
- extracting the full detailed legacy preview body

## Marker and Test Coverage Notes

Current marker coverage is anchored by:

- helper contract tests in `tests/test_kora_studio_server.py`
- full preview marker assertions in `tests/test_kora_studio_server.py`
- smoke marker checks in `scripts/check_kora_studio_preview.py`

Any v1.5 helper added in Task 507, Task 508, or Task 509 should be added to:

- `RENDER_HELPER_FUNCTIONS`
- `RENDER_HELPER_MODULES`
- `EXPECTED_RENDER_HELPER_NAMES`
- helper-owned marker/copy tests where a stable marker exists

## Claim Boundaries

All v1.5 extraction work must preserve:

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

## Validation Expectation

Task 506 is docs-only. Validation should include:

- `git diff --check`
- `python3 -m pytest tests -k "studio or sse or execution or harness"`

Later extraction tasks should also run focused server and preview smoke tests after each code change.
