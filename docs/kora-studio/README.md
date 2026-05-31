# KORA Studio

## Status

KORA Studio is an early local implementation and planning area. It is not a complete product, hosted service, or production-ready workflow yet.

## Planning Scope

The Studio documents describe candidate UI, workflow, fixture, and report-viewer ideas until implementation work lands in code. Current KORA validation remains CLI-based through local examples and generated validation reports. Do not describe Studio behavior as shipped unless the corresponding runtime, CLI, or server code exists in this repository.

## Purpose

KORA Studio is intended to become a local-first AI Task Execution Router workspace for Mac and Linux. It should help users run local AI workflows, not just local models, by routing each task to the right execution path: CPU deterministic fast path, structured lookup, local model, or larger execution path only when needed.

KORA Studio is not an LM Studio replacement and should not be framed as merely a local chatbot. LM Studio helps users run local models. KORA Studio should help users route local AI workflows while keeping the model as one execution path, not the default path.

## Core User Benefit

KORA Boost

Less waiting. Better answers. No hardware upgrade.

KORA Boost handles simple work through fast paths and saves model power for the tasks that need it.

Standard Mode sends every step to the model. KORA Boost routes deterministic and structured tasks to CPU/local fast paths first. The model becomes one execution path, not the default path.

KORA does not make large models smaller and does not remove RAM, VRAM, unified-memory, or model-loading requirements. Larger-model workflow feasibility depends on the user's actual system memory, runtime support, quantization, and validation. KORA can make larger-model workflows lighter by sending less work to the model.

## Initial Scope

The first MVP should focus on:

- Mac and Linux first
- CLI launch
- local browser UI
- system profile
- model capability view
- local runtime detection
- Ollama-first model selection
- Standard Mode vs KORA Boost
- project-based chat
- execution path visibility
- model-call counters
- local validation report viewer
- local-only storage

## Non-Scope

KORA Studio v0.1 planning is:

- not a hosted SaaS product yet
- not a production monitoring platform yet
- not an API-cost dashboard yet
- not an energy dashboard yet
- not a real provider billing dashboard yet
- not a claim that KORA Studio is implemented today
- not an LM Studio replacement
- not a claim that KORA removes model memory requirements
- not a claim that unsupported larger models physically run on local hardware

## Source Artifacts

Likely source artifacts include:

- local validation Markdown reports
- JSON summaries from local validation examples
- synthetic workload files
- reviewer packet outputs
- future local model validation reports

## Public/Private Boundary

KORA Studio docs in public KORA should describe technical design, local validation artifacts, and contributor-friendly planning only. Internal product strategy, launch planning, campaign materials, and private operating notes belong in the private internals repo.

## Claim Boundary

KORA Studio planning does not create new benchmark claims. It should only visualize already generated validation counters and claim-safe reports.

## CLI Launch

The local KORA Studio preview can be launched with:

```bash
python3 -m kora studio
```

The command starts the localhost-only Studio server and attempts to open the default browser at `http://127.0.0.1:8765/`. It does not call a model runtime, call a provider, enable cloud sync, or require API keys. If browser launch fails, it prints the local URL and keeps serving locally.

Default launch behavior:

- `kora studio` starts the localhost-only Studio server
- opens the default browser automatically
- keeps provider calls disabled by default
- keeps cloud sync disabled by default
- requires no API key for default local mode
- if browser launch fails, prints the local URL and keeps serving locally

Developer/status options:

- `kora studio --no-browser`
- `kora studio --port 8765`
- `kora studio --status`
- optional future browser selector, such as `--browser chrome`

Local smoke check for an already-running preview:

```bash
python3 scripts/check_kora_studio_preview.py
```

The smoke check only accepts `http://127.0.0.1` or `http://localhost` URLs. It checks `/health`, `/status`, and `/` without starting external services, calling providers, downloading models, executing models, scanning private model directories, or running runtime model list commands.

## Local Server Troubleshooting

If you encounter issues launching the local KORA Studio server, try the following steps:

- Confirm the CLI is available by running `python3 -m kora studio --help`.
- Start the server without opening a browser automatically by running `python3 -m kora studio --no-browser`.
- The default local URL is `http://127.0.0.1:8765/`.
- If port `8765` is busy, you can use another local port. For example: `python3 -m kora studio --no-browser --port 8766`.
- Note: This preview is localhost-only and does not call providers, download models, run models, enable cloud sync, or require API keys.

## Local Server Skeleton

A preview local-only server skeleton remains available through the compatibility flag:

```bash
python3 -m kora studio --serve
```

Status:

- preview/local-only skeleton
- default host: `127.0.0.1`
- default port: `8765`
- endpoints: `/health`, `/status`, `/`
- `/status` includes grouped v0.2 status, launch boundary, disabled action state, and claim boundary fields
- `/status` includes a local system profile scaffold and model capability estimate
- `/status` includes a static local model catalog scaffold and claim-safe recommendations
- `/status` includes a local runtime status scaffold and installed-model summary
- runtime service reachability is a localhost-only scaffold, not model execution readiness
- installed model detection is disabled/not connected by default
- `/status` includes informational runtime setup guidance metadata
- disabled model actions route to setup guidance, not an active installer
- `/status` includes local deterministic harness requests, a sample run, counters, and claim boundaries
- `/status` includes local fixture/mock execution viewer events for the preview surface
- `/status` includes a local harness-generated Standard Mode vs KORA Boost comparison
- `/status` includes a local report viewer/export placeholder based on local harness summary metadata
- browser launch enabled by default unless `--no-browser` is set
- no Ollama calls
- no runtime model list commands
- no private model directory scans
- no arbitrary local report file scans
- no report uploads
- no provider calls
- no cloud sync
- no API keys required

The server skeleton is not the full KORA Studio runtime or frontend. It exists to define the local server boundary for future Studio implementation work.

## Static Preview Page

The local server root serves a static UI prototype v0.1:

```bash
python3 -m kora studio
```

Open locally:

```text
http://127.0.0.1:8765/
```

The page shows a first-run flow ordered around launch/local-only status, Your Computer, Model Capability Estimate, Runtime Status, Catalog vs Installed, Setup Guidance, Disabled Download/Run Actions, KORA Boost Boundary, Local Harness Preview, Execution Viewer, Standard Mode vs KORA Boost, and Report Viewer Placeholder. It uses embedded HTML/CSS with minimal vanilla JavaScript for the approved local harness selector, can be opened automatically by the CLI, does not call Ollama or providers, does not enable cloud sync, does not connect a model/runtime, does not download models, does not require API keys, and does not use a frontend framework yet. Use `python3 -m kora studio --no-browser` to keep serving locally without opening a browser. The model capability estimate and model catalog recommendations are local and heuristic; recommendations are estimates until validated and do not claim unsupported larger models can run. Catalog examples are not installed models. Runtime executable detection is local-only; service reachability is a localhost-only scaffold and is not model execution readiness. Installed model detection remains not connected unless future work implements a safe local method. The default path does not scan private model directories and does not run runtime model list commands. Download and run actions are visible only as disabled/planned UI scaffolding and route to informational setup guidance, not an active installer. The Local Harness Preview includes an approved request selector and Run Local Harness button that send only an approved `request_id` to `POST /api/harness/run`; selected-run state remains browser-local in-memory state. The selected-run UI now includes claim-safe error state and Retry Last Approved Request behavior. Retry reuses only the last approved request ID, never accepts arbitrary prompt text, and calls only `POST /api/harness/run`. Endpoint unavailable and malformed response messages state that no model execution was attempted and provider calls remain disabled. Successful local harness run responses are kept in bounded browser-local page memory as Local Run History. The history clears on refresh, can switch the selected run, and Clear Local Run History clears browser UI state only without persistence, cloud sync, backend deletion, report export, or file writing. After a successful approved run, the UI can open a generated event stream from `GET /api/harness/sse?run_id=<id>` and falls back to `GET /api/harness/events?run_id=<id>` if EventSource is unavailable or the generated stream fails. The generated event stream is generated harness events only; it is not model token streaming, provider streaming, model output streaming, or arbitrary prompt execution. It also renders selected-run counters from the local run output, selected-run Standard Mode vs KORA Boost comparison from the local harness comparison summary, and selected-run report metadata from `report_metadata_summary`. The selected report metadata is preview-only; no file export, file writing, model execution, provider calls, cloud sync, or download action is connected. The selected timeline is not model token streaming and not provider output. The selected-run counters are not production telemetry, the selected-run comparison is not production cost evidence, and the selected-run report metadata is not production evidence. No arbitrary prompt input is added. It also shows a generated local harness event timeline, generated counters, and a local harness Standard Mode vs KORA Boost comparison. These outputs are local deterministic harness output only, not production evidence. The report panel now shows a local harness report metadata preview tied to generated harness summary metadata, including run/request relationship, event count, counter summary, comparison summary status, disabled file export state, and claim boundary text. No report file export is connected in this preview. The panel points to the local trigger endpoints but does not add arbitrary prompt input, model execution, provider calls, or downloads. `POST /api/harness/run` can trigger a generated local harness run for approved sample request IDs only, `GET /api/harness/run/<run_id>` can retrieve the in-memory run record while the server process is alive, `GET /api/harness/events?run_id=<id>` can retrieve generated events for that run, and `GET /api/harness/sse?run_id=<id>` can stream the same generated events as Server-Sent Events. The SSE endpoint streams generated local harness events only. It is not model token streaming, provider streaming, model output, or arbitrary prompt execution. Model-needed boundaries return `execution_not_connected` and do not execute a model. These surfaces do not execute models, call providers, download models, scan arbitrary local report files, upload reports, write report exports, or prove production behavior. KORA does not support all open-source LLMs by default.

The v0.6 history UI marks the active selected run, shows compact generated-counter summaries on history cards, and keeps Clear Local Run History limited to page-memory UI reset. Clearing history does not delete server run records, backend records, report files, generated endpoints, or persisted data.

The v0.8 preview shell now scaffolds the final UI/UX board structure above the detailed local preview: a small ChatGPT-style left mini rail, compact top model selector, centered composer, boundary pills, and hidden right details drawer. The top model selector now renders local static catalog recommendations as estimates only; opening it does not install, download, execute, or claim a model is installed. The centered composer action reuses the approved local harness request path and updates a compact selected-run summary without accepting arbitrary prompt text. The shell includes mobile-ready layout behavior for a collapsed left rail overlay, compact selector overlay menu, wrapped boundary pills, centered composer, and right details drawer overlay. The drawer carries runtime status, selected model boundary, catalog vs installed summary, route trace, generated counters, report metadata, and claim boundary sections while the detailed local preview remains below for compatibility. The shell does not add arbitrary prompt execution, model execution, provider calls, downloads, cloud sync, report export, or new frontend dependencies.

The v1.0 preview readiness work is moving the final shell toward the primary local preview experience. The shell now includes v1.0 local-only boundary markers and a compact boundary strip for provider calls disabled, cloud sync disabled, downloads disabled, model execution not connected, and report export disabled. The detailed legacy preview remains below for compatibility while shell and drawer coverage is completed.

The shell also includes a v1.0 selected-run detail strip for generated timeline, counters, comparison, and report metadata status, with matching status mirrored in the right drawer. These surfaces remain generated local harness output only and do not add model execution, provider calls, downloads, cloud sync, report export, or report writing.

The legacy detailed preview is now collapsed by default and labelled as compatibility/developer scaffolding. It remains available for reference and smoke coverage while the final shell becomes the primary local preview surface.

## Implementation Planning

- [KORA Studio final development report](kora-studio-final-development-report.md)
- [KORA Studio implementation breakdown](kora-studio-implementation-breakdown.md)
- [KORA Studio v0.1 readiness report](kora-studio-v0-1-readiness-report.md)
- [KORA Studio v0.2 plan](kora-studio-v0-2-plan.md)
- [KORA Studio v0.2 visual QA checklist](kora-studio-v0-2-visual-qa-checklist.md)
- [KORA Studio v0.2 readiness report](kora-studio-v0-2-readiness-report.md)
- [KORA Studio v0.2 goal report](kora-studio-v0-2-goal-report.md)
- [KORA Studio v0.3 live harness plan](kora-studio-v0-3-live-harness-plan.md)
- [KORA Studio v0.3 readiness report](kora-studio-v0-3-readiness-report.md)
- [KORA Studio v0.3 goal report](kora-studio-v0-3-goal-report.md)
- [KORA Studio v0.4 local run trigger plan](kora-studio-v0-4-local-run-trigger-plan.md)
- [KORA Studio v0.4 readiness report](kora-studio-v0-4-readiness-report.md)
- [KORA Studio v0.4 goal report](kora-studio-v0-4-goal-report.md)
- [KORA Studio v0.5 local interactive UI plan](kora-studio-v0-5-local-interactive-ui-plan.md)
- [KORA Studio v0.5 readiness report](kora-studio-v0-5-readiness-report.md)
- [KORA Studio v0.5 goal report](kora-studio-v0-5-goal-report.md)
- [KORA Studio v0.6 frontend interaction hardening plan](kora-studio-v0-6-frontend-interaction-hardening-plan.md)
- [KORA Studio v0.6 readiness report](kora-studio-v0-6-readiness-report.md)
- [KORA Studio v0.6 goal report](kora-studio-v0-6-goal-report.md)
- [KORA Studio v0.7 Claude Design source of truth](kora-studio-v0-7-claude-design-source-of-truth.md)
- [KORA Studio v0.7 chat-first minimal UI/UX boards](kora-studio-v0-7-chat-first-minimal-ui-ux-boards.md)
- [KORA Studio v0.7 minimal UI/UX boards](kora-studio-v0-7-minimal-ui-ux-boards.md)
- [KORA Studio v0.7 UI/UX board](kora-studio-v0-7-ui-ux-board.md)
- [KORA Studio v0.8 final UI implementation plan](kora-studio-v0-8-final-ui-implementation-plan.md)
- [KORA Studio v0.8 readiness report](kora-studio-v0-8-readiness-report.md)
- [KORA Studio v0.8 goal report](kora-studio-v0-8-goal-report.md)
- [KORA Studio v0.9 local usability polish plan](kora-studio-v0-9-local-usability-polish-plan.md)
- [KORA Studio v0.9 mobile visual QA checklist](kora-studio-v0-9-mobile-visual-qa-checklist.md)
- [KORA Studio v0.9 readiness report](kora-studio-v0-9-readiness-report.md)
- [KORA Studio v0.9 goal report](kora-studio-v0-9-goal-report.md)
- [KORA Studio v1.0 preview readiness plan](kora-studio-v1-0-preview-readiness-plan.md)
- [KORA Studio v1.0 shell-first information architecture](kora-studio-v1-0-shell-first-information-architecture.md)
- [KORA Studio v1.0 readiness report](kora-studio-v1-0-readiness-report.md)
- [KORA Studio v1.0 goal report](kora-studio-v1-0-goal-report.md)
- [KORA Studio v1.1 shell-only hardening plan](kora-studio-v1-1-shell-only-hardening-plan.md)
- [KORA Studio v1.1 shell diagnostics coverage map](kora-studio-v1-1-shell-diagnostics-coverage-map.md)
- [KORA Studio v1.1 readiness report](kora-studio-v1-1-readiness-report.md)
- [KORA Studio v1.1 goal report](kora-studio-v1-1-goal-report.md)
- [KORA Studio v1.2 frontend extraction plan](kora-studio-v1-2-frontend-extraction-plan.md)
- [KORA Studio v1.2 component inventory](kora-studio-v1-2-component-inventory.md)
- [KORA Studio v1.2 extraction smoke check](kora-studio-v1-2-extraction-smoke-check.md)
- [KORA Studio v1.2 readiness report](kora-studio-v1-2-readiness-report.md)
- [KORA Studio v1.2 goal report](kora-studio-v1-2-goal-report.md)
- [KORA Studio v1.3 frontend extraction hardening plan](kora-studio-v1-3-frontend-extraction-hardening-plan.md)
- [KORA Studio v1.3 render fragment inventory](kora-studio-v1-3-render-fragment-inventory.md)
- [KORA Studio v1.3 render helper API contracts](kora-studio-v1-3-render-helper-api-contracts.md)
- [KORA Studio v1.3 static asset serving tradeoff](kora-studio-v1-3-static-asset-serving-tradeoff.md)
- [KORA Studio v1.3 readiness report](kora-studio-v1-3-readiness-report.md)
- [Harness engineering specification](kora-studio-harness-engineering-spec.md)
- [Runtime setup guidance](kora-studio-runtime-setup-guidance.md)
- [Report viewer requirements](report-viewer-requirements.md)
- [Dashboard counter schema](dashboard-counter-schema.md)
- [Fixtures plan](fixtures-plan.md)
- [Fixture schema reference](fixture-schema-reference.md)
- [Phase 0 sample fixtures](fixtures/README.md)
- [Local server placeholder page](kora-studio-local-server-placeholder-page.md)
