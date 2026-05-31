# KORA Studio v0 (Mac Demo Scaffold)

KORA Studio v0 is a minimal local AI Task Execution Router / Execution Viewer demo for macOS development.
It includes a small FastAPI backend and a single-screen React UI.

The demo should be read as a local workflow-routing scaffold, not an LM Studio replacement or a generic local chatbot. LM Studio helps users run local models. KORA Studio routes local AI workflows by making the model one execution path, not the default path.

## What This Demo Shows

- A simple execution-viewer style metro map with stage replay animation
- Real-time station replay via Server-Sent Events (SSE) from `/api/sse_run`
- Stage-level metric badges (status/time and adapter token usage) overlaid on each station during replay
- Skip routing visualization (Decision -> Output bypass) when deterministic-first logic skips LLM execution
- Fixture Direct vs KORA comparison view using recent run history (demo cost/tokens/latency deltas for same prompt)
- A metrics panel fed by backend demo telemetry (`LLM calls`, `tokens`, `estimated cost`, `stage counts`)
- A local-only scaffold to iterate before wiring real runtime streaming

## Capability Boundary

- Your machine may be comfortable with a specific local model tier.
- KORA does not make large models smaller.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.
- KORA makes larger-model workflows lighter by sending less work to the model.
- KORA routes deterministic and structured work to CPU/local fast paths first.
- The model becomes one execution path, not the default path.
- Provider, cloud, and distributed routes are not enabled by default in this demo.

## Current API Wiring

- `POST /api/run`
  - body: `{"prompt": "...", "mode": "kora|direct", "adapter": "openai|mock"}`
  - currently frontend uses `mode="kora"` and `adapter="mock"` by default
  - executes a minimal TaskGraph via `run_graph()` and stores events in memory
- `GET /api/sse_run?run_id=<id>`
  - streams run events in sequence for metro-map animation

## Run Backend

The repository-level local preview skeleton launches with:

```bash
python3 -m kora studio
```

It starts the localhost-only server on `127.0.0.1:8765`, opens the default browser unless `--no-browser` is set, keeps provider calls and cloud sync disabled by default, and requires no API key for default local mode. If browser launch fails, it prints the manual local URL and keeps serving locally.

The preview `/status` response includes a local system profile scaffold and model capability estimate. The estimate is heuristic and local-only; recommendations are estimates until validated on the machine and do not claim unsupported larger-model execution.

The preview also includes a static local model catalog scaffold. Catalog recommendations are curated examples, do not fetch remote registries, do not download or execute models, and do not imply all open-source LLMs are supported.

Runtime status is also exposed as a local scaffold. Executable detection is local-only, catalog examples are not installed models, service reachability is a localhost-only scaffold rather than model execution readiness, installed-model detection is disabled/not connected by default, and download/execution actions are not connected. The default path does not scan private model directories or run runtime model list commands.

Catalog action labels are disabled planning scaffolds only. The preview may show "Download not connected yet" and "Run not connected yet"; these labels do not download, execute, call a registry, or call a provider.

Setup guidance is informational in this scaffold. Disabled actions can point to guidance copy, but they do not install runtimes, download models, execute models, call runtime model list commands, scan private model directories, or enable provider/cloud routes.

The first-run demo surface is ordered around Launch / Local-only Status, Your Computer, Model Capability Estimate, Runtime Status, Catalog vs Installed, Setup Guidance, Disabled Download/Run Actions, KORA Boost Boundary, Execution Viewer, Standard Mode vs KORA Boost, and Report Viewer Placeholder. The comparison shows fixture-only counters for baseline model calls, KORA model calls, avoided model calls, deterministic routes, model escalations, and validation passes. Execution viewer events show request received, deterministic route check, structured lookup, validation pass, model fallback skipped, and final counters. The report viewer uses fixture metadata only and does not scan arbitrary local files, upload reports, or commit generated reports. These fixtures do not execute models, call providers, download models, or prove production behavior.

The repository-level preview also includes an approved request selector and Run Local Harness button. They list approved deterministic sample request IDs, route classes, and model-needed boundaries, then send only the selected approved `request_id` to `POST /api/harness/run`; selected-run state is browser-local in-memory state only. The selected-run UI includes claim-safe error state and Retry Last Approved Request behavior. Retry reuses only the last approved request ID, does not accept arbitrary prompt text, and calls only `POST /api/harness/run`. Endpoint unavailable and malformed response messages do not suggest model execution, provider fallback, downloads, or cloud recovery. Successful local harness run responses are kept in bounded browser-local page memory as Local Run History. The history clears on refresh, can switch the selected run, and Clear Local Run History clears browser UI state only without persistence, cloud sync, backend deletion, report export, or file writing. After a successful approved run, the UI can open a generated event stream from `GET /api/harness/sse?run_id=<id>` and falls back to `GET /api/harness/events?run_id=<id>` if EventSource is unavailable or the generated stream fails. The generated event stream is generated harness events only; it is not model token streaming, provider streaming, model output streaming, or arbitrary prompt execution. It also renders selected-run counters from the local run output, selected-run Standard Mode vs KORA Boost comparison from the local harness comparison summary, and selected-run report metadata from `report_metadata_summary`. The selected report metadata is preview-only; no file export, file writing, model execution, provider calls, cloud sync, or download action is connected. The selected timeline is not model token streaming and not provider output. The selected-run counters are not production telemetry, the selected-run comparison is not production cost evidence, and the selected-run report metadata is not production evidence. No arbitrary prompt input is added. The preview renders a generated local harness event timeline, generated counters, a local harness Standard Mode vs KORA Boost comparison, and a report metadata preview tied to local harness summary metadata. These panels are local deterministic harness output only, not production evidence. The report metadata preview shows the run/request relationship, event count, counter summary, comparison status, and disabled file export state; it does not write report files or scan arbitrary local files. The preview exposes `POST /api/harness/run` for approved local deterministic sample request IDs only, `GET /api/harness/run/<run_id>` for in-memory run retrieval, `GET /api/harness/events?run_id=<id>` for generated event retrieval, and `GET /api/harness/sse?run_id=<id>` for generated event SSE streaming. The events and SSE endpoints stream no model tokens, provider output, or model output. Arbitrary prompt execution is not connected. Model-needed boundaries return `execution_not_connected` and do not execute a model. Provider calls, cloud sync, downloads, runtime model listing, private model directory scanning, and report file export remain disabled.

The v0.6 history UI marks the active selected run, shows compact generated-counter summaries on history cards, and keeps Clear Local Run History limited to browser page-memory UI reset. Clearing history does not delete server run records, backend records, report files, generated endpoints, or persisted data.

The repository-level preview now includes the v0.8 final UI shell scaffold: a small ChatGPT-style left mini rail, compact top model selector, centered composer, boundary pills, and hidden right details drawer. The top model selector renders local static catalog recommendations as estimates only; opening it does not install, download, execute, or claim a model is installed. The centered composer action reuses the approved local harness request path and updates a compact selected-run summary without accepting arbitrary prompt text. The drawer carries runtime status, selected model boundary, catalog vs installed summary, route trace, generated counters, report metadata, and claim boundary sections while the detailed local harness/runtime/report panels remain below for compatibility. This shell does not add arbitrary prompt execution, model execution, provider calls, downloads, cloud sync, report export, or new frontend dependencies.

The separate FastAPI/React demo scaffold can still be run manually:

From repo root:

```bash
cd studio/backend
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
uvicorn app.main:app --reload --port 8000
```

If importing `kora` fails, run from repo root context or set:
`PYTHONPATH=../..`

## Run Frontend

From repo root:

```bash
cd studio/frontend
npm install
npm run dev
```

Frontend: [http://localhost:5173](http://localhost:5173)
Backend: [http://localhost:8000](http://localhost:8000)

## Next Milestones

- Replace in-memory demo SSE with true live event streaming directly from active `run_graph()` execution
- Live runtime trigger from UI input
- Multi-run timeline and report comparison views
