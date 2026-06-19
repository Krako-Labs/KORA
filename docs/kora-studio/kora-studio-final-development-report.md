# KORA Studio Final Development Report

## Status

KORA Studio is complete through the current local preview/demo implementation and final UI/UX source-of-truth work.

Current public truth before this report commit:

```text
Branch: main
HEAD: 773e4d84ec35dba6628cb4b4bbb8b2c18eed5f01
origin/main: 773e4d84ec35dba6628cb4b4bbb8b2c18eed5f01
Status: clean
```

KORA Studio remains a local preview/demo readiness milestone, not a production product.

## Product Positioning

KORA Studio is a local-first AI Task Execution Router workspace.

It is designed to show how local AI work can be routed through deterministic checks, structured lookup, validation, local harness events, and model-needed boundaries. The model is one possible execution path, not the default path.

KORA Studio is not an LM Studio replacement, a generic local chatbot, a production hosted service, a provider billing dashboard, a cost-reduction dashboard, or an energy dashboard.

## Implemented Local Preview Surface

The local preview can be launched with:

```bash
python3 -m kora studio
```

or without browser launch:

```bash
python3 -m kora studio --no-browser
```

The localhost-only preview exposes:

- `/health`
- `/status`
- `/`
- `POST /api/harness/run`
- `GET /api/harness/run/<run_id>`
- `GET /api/harness/events?run_id=<id>`
- `GET /api/harness/sse?run_id=<id>`

The server defaults to `127.0.0.1:8765` and keeps provider calls, cloud sync, downloads, and model execution disabled.

## Development Milestones Completed

### v0.1 Local Demo Readiness

KORA Studio established the local browser preview and first-run demo surfaces:

- CLI launch through `python3 -m kora studio`
- localhost-only server boundary
- `/health`, `/status`, and `/`
- system profile scaffold
- model capability estimate scaffold
- static local model catalog scaffold
- runtime status scaffold
- installed model detection scaffold
- disabled download/run action scaffold
- runtime setup guidance scaffold
- Execution Viewer fixture/mock events
- Standard Mode vs KORA Boost fixture comparison
- report viewer/export placeholder

### v0.2 First-Run Local Setup Experience

The preview was organized into a coherent first-run flow:

- launch/local-only status
- Your Computer
- Model Capability Estimate
- Runtime Status
- Catalog vs Installed
- Setup Guidance
- Disabled Download/Run Actions
- KORA Boost Boundary
- Execution Viewer fixture
- Standard Mode vs KORA Boost comparison fixture
- Report Viewer placeholder
- v0.2 planning, visual QA checklist, smoke helper, readiness report, and consolidated goal report

### v0.3 Live Local Harness Milestone

KORA Studio moved beyond static fixture-only display by adding a local deterministic harness:

- approved deterministic sample request set
- local harness event builder
- local harness status in `/status`
- generated event stages
- generated counters
- model-needed boundary with `execution_not_connected`
- Local Harness Preview panel
- local harness-generated Standard Mode vs KORA Boost comparison
- report placeholder connected to local harness summary metadata
- v0.3 smoke check, readiness report, and consolidated goal report

### v0.4 Local Run Trigger and Event Retrieval

KORA Studio added local run trigger scaffolding for approved sample requests only:

- `POST /api/harness/run`
- in-memory generated run records
- `GET /api/harness/run/<run_id>`
- `GET /api/harness/events?run_id=<id>`
- `GET /api/harness/sse?run_id=<id>`
- generated harness SSE stream
- static Run Local Harness panel
- generated event timeline panel
- generated counters section
- local harness Standard Mode vs KORA Boost comparison panel
- Local Harness Report / Report Metadata Preview panel
- v0.4 readiness report and consolidated goal report

### v0.5 Local Interactive UI and Selected-Run State

The static preview gained minimal vanilla JavaScript interaction:

- approved request selector
- Run Local Harness button connected to approved request IDs only
- browser-local selected-run state
- selected-run summary
- selected-run generated event timeline
- selected-run generated counters
- selected-run Standard Mode vs KORA Boost comparison
- selected-run report metadata preview
- no arbitrary prompt input
- no frontend framework dependency
- v0.5 readiness report and consolidated goal report

### v0.6 Frontend Interaction Hardening

The local interaction layer was hardened:

- claim-safe selected-run error state
- Retry Last Approved Request limited to approved request IDs
- browser-local run history in page memory only
- active selected-run history card
- compact generated-counter summaries on history cards
- Clear Local Run History limited to page-memory UI reset
- Generated Event Stream panel connected to generated harness SSE
- fallback from generated-event SSE to generated events endpoint
- v0.6 readiness report and consolidated goal report

### v0.7 Final UI/UX Source of Truth

The UI/UX direction was consolidated around a minimal chat-like workspace:

- final UI/UX board: `docs/kora-studio/design/claude-v0-7/kora-studio-final-uiux-board.png`
- Claude Design source-of-truth document
- supporting screenshots for empty states, mobile main composer, mobile left rail, and mobile details drawer
- reference prototype files preserved as design artifacts
- explicit warning not to copy external CDN, Babel, Google Fonts, or prototype dependencies into product code

The approved visual target is:

- sparse dark surface
- small chat-style left mini rail
- top model selector
- centered work composer
- compact status boundary pills
- hidden right details drawer
- mobile overlay behavior for left rail and right drawer

## Current UI/UX Source of Truth

Primary visual target:

- [KORA Studio final UI/UX board](design/claude-v0-7/kora-studio-final-uiux-board.png)

Primary specification:

- [KORA Studio v0.7 Claude Design source of truth](kora-studio-v0-7-claude-design-source-of-truth.md)

Implementation direction:

- The default screen should feel closer to a quiet chat workspace than to a dense model-management app.
- The left mini rail is for workspace/task navigation only.
- Runtime, route trace, counters, report metadata, and claim boundaries belong in the right details drawer.
- The top model selector may search/select open-source model candidates, but selection is not installation or execution.
- The composer remains the main surface.

## Status Endpoint Coverage

`/status` exposes local preview state including:

- `studio_status`
- `launch_boundary`
- `system_profile`
- `model_capability_estimate`
- `runtime_status`
- `installed_models_summary`
- `model_catalog_status`
- `recommended_models`
- `setup_guidance_status`
- `disabled_action_state`
- `execution_viewer_status`
- `local_harness_status`
- `local_harness_sample_run`
- `local_harness_comparison`
- `comparison_counters`
- `standard_vs_kora_comparison_status`
- `report_viewer_status`
- `report_viewer_placeholder`
- `provider_calls_enabled: false`
- `cloud_sync_enabled: false`
- `claim_boundaries`

## Harness API Behavior

The local harness API accepts approved sample request IDs only.

`POST /api/harness/run`:

- accepts `request_id`
- rejects unknown request IDs
- generates local harness events
- generates counters
- returns comparison summary
- returns report metadata summary
- stores an in-memory run record while the server process is alive
- does not execute a model
- does not call a provider
- does not download a model
- does not scan private model directories
- does not run runtime model list commands

`GET /api/harness/run/<run_id>` retrieves an in-memory generated run record.

`GET /api/harness/events?run_id=<id>` returns generated harness events for an existing run.

`GET /api/harness/sse?run_id=<id>` streams generated harness events only. It is not model token streaming, provider streaming, or model output streaming.

## Preview UI Behavior

The current preview UI includes:

- approved request selector
- Run Local Harness button
- selected-run summary
- selected-run event timeline
- selected-run counters
- selected-run Standard Mode vs KORA Boost comparison
- selected-run report metadata preview
- generated event stream display
- retry for last approved request
- browser-local run history
- clear browser-local run history

All UI state is local preview state. Browser-local run history is page-memory only and clears on refresh.

## Report Metadata Boundary

Report metadata is preview-only.

Current behavior:

- report source is local harness summary metadata
- report metadata includes run/request linkage
- file export is disabled
- file writing is disabled
- upload is disabled
- generated report commit is disabled
- arbitrary local file scanning is disabled

No report file is written by the preview.

## Validation Summary

Most recent validation before this report:

```bash
git diff --check
```

Result: passed.

```bash
python3 -m pytest tests -k "studio or sse or execution or harness"
```

Result: 90 passed, 3 skipped, 138 deselected.

Recent milestone validations also reported:

- v0.6 full test suite: 231 passed
- v0.6 Studio focused suite: 93 passed, 138 deselected
- live local smoke check passed for `/health`, `/status`, `/api/harness/run`, `/api/harness/run/<run_id>`, `/api/harness/events`, `/api/harness/sse`, and `/`

## Claim Boundaries

KORA Studio currently preserves these boundaries:

- local preview/demo only
- local deterministic harness only
- approved sample requests only
- generated harness events only
- browser-local selected-run state only
- browser-local run history is page-memory only
- in-memory server run records only
- no arbitrary prompt execution
- no real model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no external network behavior required by the preview
- no report file export
- no report file writing
- no production cost reduction claim
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement

## Explicit Non-Claims

KORA Studio does not currently claim:

- production readiness
- all open-source LLM support
- installed local model discovery by default
- connected model execution
- connected model downloads
- real provider execution
- real API-cost reduction
- real energy reduction
- benchmark proof from preview counters
- larger models physically run than the user's hardware supports
- KORA removes RAM, VRAM, unified-memory, or model-loading requirements

## Known Limitations

- The local preview uses minimal vanilla JavaScript and embedded server-rendered HTML.
- The final v0.7 UI/UX board is a source-of-truth design artifact, not fully implemented in the preview UI yet.
- Run records are process-local in-memory state.
- Browser run history is page-memory only and resets on refresh.
- SSE streams generated harness events only.
- The selected-run UI does not execute real model tokens or provider output.
- Report metadata is preview-only.
- File export remains disabled.
- Installed model detection remains not connected by default.
- Runtime service reachability is not model execution readiness.

## Files and Artifacts to Treat as Current References

- `kora/studio_server.py`
- `kora/studio_harness_requests.py`
- `kora/studio_harness_events.py`
- `kora/studio_harness_comparison.py`
- `kora/studio_harness_runs.py`
- `kora/studio_report_viewer.py`
- `scripts/check_kora_studio_preview.py`
- `docs/kora-studio/kora-studio-v0-6-readiness-report.md`
- `docs/kora-studio/kora-studio-v0-6-goal-report.md`
- `docs/kora-studio/kora-studio-v0-7-claude-design-source-of-truth.md`
- `docs/kora-studio/design/claude-v0-7/kora-studio-final-uiux-board.png`

## Next Recommended Goal

KORA Studio v0.8 should implement the final UI/UX board into the local preview while preserving the current local-only harness behavior.

Recommended first tasks:

- scaffold the chat-like layout in the existing local preview
- add the left mini rail as workspace/task navigation only
- keep the top model selector compact
- move dense runtime, route, counter, report, and claim information into a right details drawer
- keep the composer as the default main surface
- avoid new frontend dependencies unless explicitly approved
- keep all provider, model execution, download, cloud sync, private directory scan, runtime model list, and report export behavior disabled

