# KORA Studio v1.4 Render Helper Contracts

## Status

Task 501 helper contract and marker coverage hardening for KORA Studio v1.4.

This document records the current render-helper ownership contract after the v1.4 fragment extraction tasks. It is a maintainability reference only. It does not add product behavior, endpoint behavior, static asset serving, frontend framework tooling, model execution, provider calls, downloads, cloud sync, report export, file writing, private directory scanning, runtime model listing, external network behavior, or production claims.

## Contract Rules

KORA Studio render helpers remain pure string renderers.

They may:

- accept server-prepared escaped display strings
- accept named slot HTML where a helper explicitly owns a slot boundary
- return deterministic HTML, CSS, or JavaScript strings
- preserve stable ids and `data-kora-component` markers
- preserve local-only claim boundary copy for owned components

They must not:

- accept raw status payload dictionaries by default
- accept arbitrary user prompt text
- call providers or remote APIs
- open network connections
- start or stop servers
- read or write files
- write reports or exports
- download or execute models
- scan private model directories
- run runtime model list commands
- mutate backend/global state
- introduce external CSS, JavaScript, images, CDNs, static asset routes, or frontend framework tooling

`kora/studio_server.py` remains responsible for endpoint routing, status payload assembly, escaping dynamic display values, local harness data assembly, and final page assembly.

## Current Helper Contract Table

| Helper | Input contract | Output contract | Owner boundary |
|---|---|---|---|
| `render_shell_layout()` | server-prepared display strings and slot HTML | shell HTML string | shell layout, left rail, top model selector shell, slot placement |
| `render_right_details_drawer()` | server-prepared display strings | drawer HTML string | diagnostics drawer only |
| `render_selected_run_summary_panel()` | escaped selected request id | composer selected-run summary HTML | approved local harness request summary only |
| `render_selected_run_state_panel()` | none | selected-run state containers | generated local harness state only |
| `render_selected_run_detail_panels()` | none | selected timeline/counter/comparison/report containers | generated local harness output only |
| `render_selected_run_panels()` | none | combined selected-run helper HTML | helper test surface only |
| `render_local_harness_selector_item()` | escaped request id/input/route/model-needed strings | selector option card HTML | approved local harness request option only |
| `render_local_harness_trigger_item()` | escaped request id/input/family/route/model-needed strings | trigger reference card HTML | approved local harness request reference only |
| `render_local_harness_request_selector_panels()` | escaped preview strings and selector item slot HTML | approved request selector panel HTML | request selector and Run Local Harness action card |
| `render_local_harness_trigger_reference_panels()` | trigger item slot HTML | trigger boundary/reference panel HTML | local harness trigger reference copy |
| `render_retry_error_state_panels()` | escaped selected request id | retry/error panel HTML | browser-local retry/error state only |
| `render_local_run_history_panels()` | none | run history panel HTML | browser-local page-memory history only |
| `render_run_state_history_panels()` | escaped selected request id | combined retry/history panel HTML | helper test surface and final placement |
| `render_legacy_preview_opening()` | none | collapsed legacy opening wrapper HTML | secondary developer/reference scaffold opening only |
| `render_endpoint_panel()` | none | endpoint reference HTML | local endpoint reference only |
| `render_limitations_panel()` | none | limitation reference HTML | claim-safe limitation copy only |
| `render_local_references_panel()` | escaped docs and fixtures display paths | local reference HTML | display-only local paths |
| `render_reference_panels()` | escaped docs and fixtures display paths | combined reference panel HTML | static reference panels |
| `render_studio_css()` | none | inline CSS string | no external CSS path or CDN |
| `render_studio_javascript()` | none | inline vanilla JavaScript string | local harness endpoints only |

## Marker Ownership Matrix

The rendered local preview must keep these helper-owned markers visible:

| Marker | Helper owner |
|---|---|
| `data-kora-component="shell-layout"` | `kora/studio_shell_render.py` |
| `data-kora-component="left-rail"` | `kora/studio_shell_render.py` |
| `data-kora-component="top-model-selector"` | `kora/studio_shell_render.py` |
| `data-kora-component="right-details-drawer"` | `kora/studio_drawer_render.py` |
| `data-kora-component="selected-run-summary"` | `kora/studio_selected_run_render.py` |
| `data-kora-component="generated-event-stream-status"` | `kora/studio_selected_run_render.py` |
| `data-kora-component="selected-run-event-timeline"` | `kora/studio_selected_run_render.py` |
| `data-kora-component="selected-run-counters"` | `kora/studio_selected_run_render.py` |
| `data-kora-component="selected-run-comparison"` | `kora/studio_selected_run_render.py` |
| `data-kora-component="selected-run-report-metadata"` | `kora/studio_selected_run_render.py` |
| `data-kora-component="approved-request-selector"` | `kora/studio_harness_request_render.py` |
| `data-kora-component="retry-error-state"` | `kora/studio_run_state_render.py` |
| `data-kora-component="run-history"` | `kora/studio_run_state_render.py` |
| `data-kora-component="legacy-compatibility-reference"` | `kora/studio_legacy_render.py` |

`data-kora-component="composer"` and `data-kora-component="boundary-strip"` are still server-owned inside the composer slot and should remain covered by rendered preview and smoke tests.

## Test Coverage Hardened In Task 501

Task 501 adds or preserves tests that verify:

- every public `render_*` function in the known render-helper modules is listed in the helper contract test set
- the expected helper set cannot silently drift when a helper is added or removed
- render helper signatures remain string-returning and keyword-only for required inputs
- render helper modules remain free of filesystem, network, subprocess, server, and browser-launch dependencies
- helper-owned component markers remain visible in the full rendered preview
- extracted helpers preserve local-only claim boundaries and marker ids
- no external script, CDN, external CSS/static asset route, provider endpoint, model endpoint, download endpoint, report export endpoint, or arbitrary prompt input is introduced

These tests are maintainability guardrails. They are not product readiness, production telemetry, benchmark, cost, energy, or model execution claims.

## Claim Boundaries

The v1.4 helper contract preserves:

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
