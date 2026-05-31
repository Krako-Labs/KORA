# KORA Studio v1.4 Local Preview Fragment Extraction Plan

## Status and Goal

KORA Studio v1.4 is a maintainability/refactor milestone.

The goal is to continue local preview fragment extraction by moving the next safe group of server-owned generated local harness preview fragments into render helpers while preserving behavior, helper contracts, marker coverage, local-only boundaries, and inline CSS/JavaScript.

v1.4 must not add product behavior, endpoint behavior, dependencies, frontend framework tooling, external static asset serving, model execution, provider calls, model downloads, cloud sync, report export/file writing, private model directory scanning, runtime model listing, external network behavior, or production claims.

## v1.3 Starting Point

v1.3 completed:

- frontend extraction hardening plan
- remaining render fragment inventory
- reference panel extraction into `kora/studio_reference_render.py`
- render helper API contract documentation
- render helper API contract tests
- static asset serving tradeoff documentation
- readiness and consolidated goal reports

Current extracted render helpers:

- `kora/studio_shell_render.py`
- `kora/studio_drawer_render.py`
- `kora/studio_selected_run_render.py`
- `kora/studio_reference_render.py`
- `kora/studio_style_render.py`
- `kora/studio_script_render.py`

`kora/studio_server.py` still owns endpoint routing, status payload assembly, local harness data assembly, escaped display value preparation, and final page assembly.

## Next Candidate Server-Owned Fragments

Task 497 inventory is documented in [KORA Studio v1.4 fragment inventory](kora-studio-v1-4-fragment-inventory.md).

The next candidate fragments in `kora/studio_server.py` are:

| Fragment | Current owner | v1.4 direction | Boundary to preserve |
|---|---|---|---|
| Approved request selector header and selected request preview | `kora/studio_server.py` | Candidate for a local harness request/trigger render helper | approved request ids only; no arbitrary prompt text |
| Local harness selector option cards | `kora/studio_server.py` via `local_harness_selector_items` | Candidate for helper-owned card list generation after escaping contract is documented | local deterministic request data only |
| Run Local Harness action state panel | `kora/studio_server.py` | Candidate for the same request/trigger helper | button remains approved-request-only; no model/provider/download behavior |
| Retry/error state panel | `kora/studio_server.py` | Candidate for a local run state/history helper | retry uses last approved request only |
| Local run history panel and clear history panel | `kora/studio_server.py` | Candidate for a local run state/history helper | browser-local page memory only; no persistence or backend delete |
| Local harness static sample cards | `kora/studio_server.py` | Defer until request/trigger and history helpers are stable | generated harness output only |
| Generated static timeline and counter cards | `kora/studio_server.py` | Defer unless marker tests are expanded first | not model token streaming; not production telemetry |
| Legacy compatibility wrapper/body | `kora/studio_server.py` | Inventory first; extract only if wrapper/body coupling is reduced | secondary developer/reference scaffold only |
| Composer container and boundary strip | `kora/studio_server.py` | Defer until selected-run slot contract is more explicit | approved local harness request only |
| Model selector item rows | `kora/studio_server.py` | Defer; catalog display and shell slot remain coupled | catalog examples only; no install/download/execute |

## Extraction Order

Preferred v1.4 extraction sequence:

1. Inventory the remaining generated local harness fragments and classify each as safe, server-owned, deferred, or already extracted.
2. Extract approved request selector and local harness trigger panels if tests can lock markers and boundary copy. Task 498 extracted these panels into `kora/studio_harness_request_render.py`.
3. Extract retry/error state and browser-local run history panels if ids and JavaScript expectations remain stable. Task 499 extracted these panels into `kora/studio_run_state_render.py`.
4. Reassess the legacy compatibility/reference wrapper; extract only if it can be done without altering final page assembly.
5. Harden helper contract and marker coverage after any extraction.
6. Run full validation and live smoke checks.
7. Create readiness and consolidated goal reports.

v1.4 should not try to extract every remaining fragment. Behavior preservation is more important than helper count.

## Helper API Contract Expectations

Any new v1.4 render helper should follow the v1.3 helper contract:

- return `str`
- use explicit keyword-only parameters
- accept pre-escaped display strings or named slot HTML only
- avoid raw status payload dictionaries by default
- avoid arbitrary prompt text
- avoid filesystem, network, subprocess, provider, runtime-model, server, browser-launch, persistence, and export dependencies
- preserve stable ids and `data-kora-component` markers
- keep claim boundaries visible where the helper owns the component

`kora/studio_server.py` should continue to own:

- endpoint routing
- local status payload assembly
- local harness data assembly
- escaping display values
- final page assembly

## Marker and Smoke Coverage Expectations

v1.4 must preserve current marker coverage, including:

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

Smoke checks must continue to cover:

- `/health`
- `/status`
- `/`
- `POST /api/harness/run`
- `GET /api/harness/run/<run_id>`
- `GET /api/harness/events?run_id=<id>`
- `GET /api/harness/sse?run_id=<id>`

## No Behavior Change Rule

v1.4 extraction must not change:

- endpoint routes
- endpoint response shapes
- selected-run JavaScript behavior
- local run history behavior
- retry behavior
- generated harness event/counter/comparison/report metadata shapes
- model selector behavior
- static asset serving decision
- public UI copy except tiny claim-safe corrections if required by tests

CSS and JavaScript must remain inline through render helpers unless a future explicitly approved task changes that decision.

## Test Plan

Required validation across v1.4:

- `git diff --check`
- `python3 -m pytest`
- `python3 -m pytest tests -k "studio or sse or execution or harness"`
- live local preview smoke check:
  - `python3 -m kora studio --no-browser`
  - `python3 scripts/check_kora_studio_preview.py`

Extraction-specific tests should verify:

- helper output includes expected component markers
- rendered preview includes all required markers
- no external script or CDN is introduced
- no external CSS/static asset route is introduced
- no provider/model/download/report export endpoint calls are introduced
- no arbitrary prompt input is introduced
- local-only and claim-safe boundary text remains present
- server still owns endpoint routing and data assembly

## Task Breakdown

Suggested v1.4 sequence:

- Task 496: v1.4 fragment extraction plan and cross-links
- Task 497: inventory next server-owned generated local harness preview fragments
- Task 498: extract local harness request/trigger panel render helper
- Task 499: extract local run history/retry/error render helper
- Task 500: extract legacy compatibility/reference render helper if still server-owned and safe
- Task 501: helper contract and marker coverage hardening
- Task 502: v1.4 smoke check and readiness report
- Task 503: consolidated v1.4 goal report

## Claim Boundaries

v1.4 must preserve:

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
