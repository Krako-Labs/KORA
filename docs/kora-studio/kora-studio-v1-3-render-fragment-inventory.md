# KORA Studio v1.3 Render Fragment Inventory

## Status

Task 490 inventory for KORA Studio v1.3 local frontend extraction hardening.

This document records the current local preview render fragments, their owners, data assembly boundaries, extraction risk, and claim boundaries. It is a maintainability reference only. It does not add runtime behavior, static asset serving, frontend framework tooling, model execution, provider calls, downloads, cloud sync, report export, file writing, private directory scanning, runtime model listing, or production claims.

## Current Render Ownership

| Owner | Responsibility | Boundary |
|---|---|---|
| `kora/studio_server.py` | endpoint routing, status payload assembly, preview display value assembly, local harness display lists, legacy/reference preview body, final page assembly | may collect local status data and call render helpers; must not delegate provider/model/download/cloud/report export behavior |
| `kora/studio_shell_render.py` | shell layout, left rail, top model selector, model selector menu slot, composer slot, details drawer slot, legacy preview slot | pure string render helper; accepts server-prepared display values and HTML slots |
| `kora/studio_drawer_render.py` | right details drawer diagnostic panels | pure string render helper; accepts server-prepared display strings |
| `kora/studio_selected_run_render.py` | selected-run summary, state, event stream status, selected timeline, counters, comparison, and report metadata containers | pure string render helper; owns stable selected-run marker containers |
| `kora/studio_style_render.py` | inline CSS template | pure string render helper; no external CSS path or CDN |
| `kora/studio_script_render.py` | inline vanilla JavaScript template | pure string render helper; local harness endpoints only |

## Remaining Embedded Fragment Inventory

| Fragment | Current owner | Current evidence | Data source | Extraction direction | Claim boundary |
|---|---|---|---|---|---|
| Composer container | `kora/studio_server.py` | `composer_html` string with `data-kora-component="composer"` | selected request preview id and selected-run summary helper output | Candidate for `studio_composer_render.py` after slot and escaping contracts are explicit | approved request only; no arbitrary prompt execution |
| Shell boundary strip | `kora/studio_server.py` inside `composer_html` | `data-kora-component="boundary-strip"` | static local-only boundary copy | Candidate for composer helper or dedicated boundary helper | no provider calls, cloud sync, downloads, model execution, or report export |
| Selected-run shell strip | `kora/studio_server.py` inside `composer_html` | `data-kora-shell-selected-run-surface="v1.0"` | selected-run status element ids updated by local JS | Candidate for composer helper with fixed ids | generated local harness output only |
| Model selector item rows | `kora/studio_server.py` assembles `model_selector_items`; rendered by shell helper slot | recommended model catalog/status data | inventory escaping rules before extraction | catalog examples only; selection does not install, download, or execute |
| Approved request selector cards | `kora/studio_server.py` assembles `local_harness_selector_items` | approved local harness request set | Candidate for request selector helper after data shape contract is documented | approved request ids only; no arbitrary prompt text |
| Static local harness sample cards | `kora/studio_server.py` in Local Harness Preview section | `local_harness_status`, sample run, request data | Candidate for local harness preview helper only if behavior-preserving | generated deterministic harness data only |
| Static generated timeline cards | `kora/studio_server.py` assembles `local_harness_timeline_items` | `local_harness_sample_run.events` | Candidate for legacy/local harness timeline helper | not model token streaming; no model execution |
| Static generated counter cards | `kora/studio_server.py` assembles `local_harness_counter_items` | `local_harness_counters` | Candidate for counter card helper | not production telemetry; no cost or energy claim |
| Retry and run history panels | `kora/studio_server.py` | `data-kora-component="retry-error-state"` and `data-kora-component="run-history"` | browser-local page state ids only | Candidate for selected-run/history helper if ids remain stable | page-memory only; no persistence, cloud sync, or backend delete |
| Execution Viewer legacy section | `kora/studio_server.py` | `h2>Execution Viewer` | fixture/mock execution data | keep collapsed secondary or extract into legacy reference helper | fixture/mock events only; no runtime execution |
| Standard Mode vs KORA Boost legacy section | `kora/studio_server.py` | `h2>Standard Mode vs KORA Boost` | local deterministic comparison fixture/harness summary | keep claim-safe or extract into comparison reference helper | not production cost evidence; no model execution |
| Report Viewer legacy section | `kora/studio_server.py` | `h2>Report Viewer Placeholder` | report viewer placeholder/local harness summary metadata | Candidate for report reference helper | metadata preview only; no file export or writing |
| Endpoint panel | `kora/studio_server.py` | `h2>Endpoint Panel` | static local endpoint copy | Candidate for endpoint reference helper | local endpoints only; no provider/model/download endpoint |
| Limitations and local references sections | `kora/studio_server.py` | `h2>Limitations Panel`, `h2>Local References` | static claim boundary copy and docs/fixtures paths | Candidate for legacy reference helper | limitations remain explicit; no production claims |
| Legacy compatibility wrapper | `kora/studio_server.py` | `legacy_preview_html` opening details wrapper and closing body later in page template | wrapper string plus all detailed reference sections | inventory before extraction; high coupling to final page assembly | secondary developer/reference scaffold only |

Task 491 update: the low-risk endpoint panel, limitations panel, and local references sections are now extracted into `kora/studio_reference_render.py`. `kora/studio_server.py` still owns escaped `docs_path` and `fixtures_path` display values and final page assembly.

## Data Assembly Boundary

`kora/studio_server.py` remains the authoritative data assembly boundary for v1.3.

Server-owned responsibilities:

- read fields from the local status payload
- assemble display strings from system profile, model catalog, runtime status, harness output, comparison output, and report placeholder metadata
- HTML-escape display values before interpolation where the existing pattern already does this
- assemble lists such as model selector rows, approved request cards, generated timeline cards, generated counters, report sections, and endpoint copy
- call render helpers and pass display-ready values or slot HTML
- serve `/health`, `/status`, `/`, `POST /api/harness/run`, `GET /api/harness/run/<run_id>`, `GET /api/harness/events?run_id=<id>`, and `GET /api/harness/sse?run_id=<id>`

Render-helper responsibilities:

- return deterministic strings
- preserve stable ids and `data-kora-component` marker contracts
- render only from arguments provided by the server
- avoid I/O, network, subprocess, provider, runtime model, filesystem scan, persistence, and export behavior
- keep local-only claim copy visible where the helper owns the component

## Escaping and Slot Contracts

Current helper contracts are mixed but bounded:

- `render_shell_layout()` receives pre-escaped display strings for model selector labels and receives slot HTML strings for model selector items, composer, details drawer, and legacy preview.
- `render_right_details_drawer()` receives pre-escaped display strings and renders only the drawer.
- `render_selected_run_summary_panel()` receives a server-prepared selector preview id.
- `render_selected_run_state_panel()` and `render_selected_run_detail_panels()` own static selected-run containers and ids.
- `render_studio_css()` and `render_studio_javascript()` own inline templates and should not receive runtime data.

Before extracting another fragment, the target helper should state whether it accepts:

- pre-escaped display values
- raw local data dictionaries
- slot HTML strings
- static marker-only markup

The preferred v1.3 rule is to pass pre-escaped display values or named slot HTML only. Avoid passing raw status payloads into render helpers.

## Extraction Risk Map

| Risk level | Fragments | Reason |
|---|---|---|
| Low | Endpoint panel, limitations panel, static local references | extracted in Task 491 into `kora/studio_reference_render.py`; mostly static copy and stable local-only boundaries |
| Medium | Approved request selector cards, generated timeline cards, generated counters, report metadata reference cards | generated lists need escaping and marker/id preservation |
| Medium | Composer container and boundary strip | central shell layout and selected-run ids make the slot boundary important |
| High | Legacy compatibility wrapper/body split | wrapper opens before the detailed preview body and closes near the final page footer/script assembly |
| High | Model selector item rows | model catalog display, selection copy, and shell helper slot are coupled |

## Recommended Task 491 Extraction Order

If Task 491 performs code extraction, prefer this order:

1. Extract a static endpoint/limitations/local references helper, because it is mostly static and marker-safe.
2. Extract generated local harness card-list helpers only after tests lock the rendered text and no-external-call boundaries.
3. Extract composer/boundary-strip only after a helper contract documents slot ids and selected-run summary placement.
4. Defer model selector row extraction unless test coverage is expanded for catalog boundaries and escaped display values.
5. Defer legacy wrapper extraction unless final page assembly is simplified first.

Task 491 may also choose no extraction if the inventory shows the helper boundary is still too coupled. Behavior preservation is more important than increasing helper count.

## Required Marker Contracts

These markers must remain visible in the preview HTML and smoke checks:

- `data-kora-component="shell-layout"`
- `data-kora-component="left-rail"`
- `data-kora-component="boundary-strip"`
- `data-kora-component="top-model-selector"`
- `data-kora-component="composer"`
- `data-kora-component="approved-request-selector"`
- `data-kora-component="selected-run-summary"`
- `data-kora-component="selected-run-event-timeline"`
- `data-kora-component="selected-run-counters"`
- `data-kora-component="selected-run-comparison"`
- `data-kora-component="selected-run-report-metadata"`
- `data-kora-component="right-details-drawer"`
- `data-kora-component="run-history"`
- `data-kora-component="retry-error-state"`
- `data-kora-component="generated-event-stream-status"`
- `data-kora-component="legacy-compatibility-reference"`

## Test Coverage Expectations

Task 490 is docs-only, but future extraction tasks should preserve:

- helper-level marker tests in `tests/test_kora_studio_server.py`
- full preview marker checks in `tests/test_kora_studio_preview_smoke.py`
- no external script, CDN, external CSS, provider endpoint, model endpoint, download endpoint, report export endpoint, or arbitrary prompt input checks
- selected-run JavaScript endpoint limits: local harness run, events, and generated SSE only
- endpoint behavior for health, status, run creation, run retrieval, events retrieval, and generated SSE

## Claim Boundaries

All inventory and extraction work must preserve:

- local deterministic harness output only
- no arbitrary prompt execution
- no model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report export
- no file writing
- no external static assets or CDN
- not production-ready
- not production telemetry
- not production cost evidence
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement
