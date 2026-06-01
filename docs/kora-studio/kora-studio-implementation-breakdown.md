# KORA Studio Implementation Breakdown

## Status

This document breaks KORA Studio v0.1 planning into implementation phases. KORA Studio is not implemented yet.

## Implementation Principle

KORA Studio should start as a local-first, single-user, no-cloud AI Task Execution Router workspace for KORA validation artifacts, local model workflows, and task-path visibility.

KORA Studio should not be framed as an LM Studio replacement or a generic local chatbot. It should help users run local AI workflows by routing each task to the right execution path: deterministic CPU fast path, structured lookup, local model, or larger execution path only when needed.

- Mac/Linux first
- CLI launch first
- browser UI first
- local-only storage first
- Ollama-first runtime direction
- system profile and model capability narrative
- provider/cloud/distributed routes disabled by default
- no provider billing dashboard in v0.1
- no API-cost or energy claims

## Phase 0 — Planning and Fixtures

Goal: Prepare static fixtures and UI requirements before runtime code.

Tasks:

- define sample local validation JSON summary fixture
- define sample Markdown report fixture
- define dashboard counter schema
- define project/chat mock data
- define KORA Boost copy placement
- define no-cloud/no-API-key onboarding copy
- define AI Task Execution Router onboarding copy
- define system profile, model capability, and execution path UI copy

Deliverables:

- `docs/kora-studio/fixtures-plan.md`
- `docs/kora-studio/kora-studio-harness-engineering-spec.md`
- `docs/kora-studio/report-viewer-requirements.md`
- `docs/kora-studio/dashboard-counter-schema.md`
- `docs/kora-studio/fixture-schema-reference.md`
- `docs/kora-studio/fixtures/`

No code required.

## Phase 0.5 — Harness Engineering Specification

Status: Specification only. This phase does not implement new runtime behavior, provider calls, model downloads, or external network behavior.

Goal: Define the measurement and validation contract before expanding product UI claims.

Before expanding product UI claims, Studio harness engineering must define how system profiling, route events, metrics, adapters, and local reports are captured and validated.

Scope:

- system profile detection boundary
- model capability estimate boundary
- deterministic route event capture
- local model and adapter state event capture
- SSE/event replay schema
- Standard Mode vs KORA Boost comparison metrics
- local report export boundary
- provider/cloud disabled-by-default checks

Acceptance criteria:

- harness requirements are public-safe and claim-safe
- event schema and metrics are documented before UI expansion depends on them
- unsupported larger-model, production cost, real API-cost, and energy claims remain out of scope
- no provider/cloud route is enabled by default

## Phase 1 — CLI Launch Skeleton

Status: Initial CLI skeleton is available through `python3 -m kora studio`. It prints planning/preview status only; it does not start a server, open a browser, call a model runtime, or call a provider.

Goal: Evolve `kora studio` into the default local launch command for the Studio workspace.

Scope:

- command registration
- local-only status output
- default behavior eventually starts the localhost-only Studio server
- default behavior eventually opens the user's default browser automatically
- fallback behavior prints the local URL and keeps serving locally if browser launch fails
- developer mode supports `--no-browser` and `--port 8765`
- optional future browser selector such as `--browser chrome`
- no real model runtime calls
- no provider calls
- no cloud sync by default
- no API key required for default local mode

Acceptance criteria:

- `python3 -m kora studio --help` or equivalent works
- command clearly says Studio is experimental/planning if not fully implemented
- tests cover command availability

## Phase 2 — Local Studio Server Skeleton

Status: Initial local server skeleton is available through `python3 -m kora studio --serve`. It exposes preview `/health`, `/status`, and `/` endpoints on localhost only. It does not include the full frontend, runtime integration, model calls, browser launch, Ollama calls, or provider calls.

Goal: Create a local-only server boundary.

Scope:

- minimal local HTTP server or FastAPI-style skeleton if dependency already exists
- health endpoint
- static placeholder page endpoint
- no cloud upload
- no model calls
- no external network dependency

Acceptance criteria:

- local server starts and stops cleanly
- health endpoint returns local status
- tests do not require network beyond localhost

## Phase 3 — Static Web UI Prototype

Status: The local server root now serves a static preview page. The next step is to expand that placeholder into a static UI prototype while keeping it local-only and framework-free until a full frontend decision is made.

Goal: Create a static UI prototype for KORA Studio.

Screens:

- Welcome / Setup
- System Profile
- Model Capability
- Model Selection
- Project Chat Workspace
- Execution Trace Panel
- Report Viewer

Scope:

- static assets or minimal frontend structure
- system profile copy that explains what the computer can physically run
- model capability copy that separates physically runnable local models, larger-model workflow feasibility, and optional external/provider/distributed routes
- KORA Boost copy explaining that deterministic and structured tasks route to CPU/local fast paths first
- execution path UI copy for deterministic code, structured lookup, local model, larger model, and disabled-by-default external/provider/distributed route
- no runtime calls
- no model downloads
- no account system

Acceptance criteria:

- UI can be served locally
- KORA Boost copy appears correctly
- planning-only status is clear

## Phase 3.5 — System Profile and Model Capability Scaffold

Status: Initial local scaffold exists in the preview server. `/status` includes `system_profile` and `model_capability_estimate`, and the static preview page shows read-only system/model capability panels.

Scope:

- standard-library-only local system profile fields
- safe executable detection for runtime candidates
- local heuristic model capability estimate
- unknown/fail-closed memory fallback
- provider calls disabled by default
- cloud sync disabled by default
- no runtime API calls
- no model downloads
- no model execution

Acceptance criteria:

- recommendations are labelled as estimates until validated
- no unsupported larger-model claim is shown
- no provider/cloud route is enabled by default

## Phase 3.6 — Model Catalog Planning Scaffold

Status: Initial static local scaffold exists in the preview server. `/status` includes `model_catalog_status`, `recommended_models`, and `model_catalog_claim_boundary`, and the static preview page shows a read-only model catalog preview.

Scope:

- curated static model tier metadata
- local-only recommendation helper
- physically runnable local candidate labels
- larger-model workflow candidate labels
- estimate-until-validated claim boundary
- download and execution disabled
- no remote catalog fetching
- no Hugging Face search
- no Ollama registry calls
- no provider/cloud route

Acceptance criteria:

- model recommendations are estimates until validated
- no catalog entry claims all open-source LLM support
- no unsupported larger-model local execution claim is shown
- no download or execution action is connected

## Phase 3.7 — Runtime Status and Installed Model Scaffold

Status: Initial local scaffold exists in the preview server. `/status` includes `runtime_status`, localhost-only service reachability fields, `installed_models_summary`, and catalog/runtime distinction copy, and the static preview page shows read-only runtime and installed-model panels.

Scope:

- local runtime executable detection
- runtime service reachability scaffolded as a localhost-only check
- service reachability is not model execution readiness
- installed model detection marked `not_connected` by default
- installed model detection fields for enabled state, method, count, error, and claim boundary
- catalog examples distinguished from installed models
- download disabled
- execution disabled
- no private model directory scans
- no model listing calls
- no model execution
- no model downloads
- no remote registry calls
- no provider/cloud route

Acceptance criteria:

- runtime executable detection is local-only
- service reachability does not execute, list, pull, or download models
- catalog examples are not presented as installed models
- no model is shown as installed unless safely confirmed
- default installed-model detection does not scan private model directories or run model list commands
- no download or execution action is connected

## Phase 3.8 — Disabled Model Action Scaffold

Status: Initial disabled action metadata exists in catalog recommendations. The static preview page shows disabled download/run labels only.

Scope:

- disabled download action metadata
- disabled run action metadata
- install/runtime guidance copy
- action claim boundary
- no model downloads
- no model execution
- no registry calls
- no provider/cloud route

Acceptance criteria:

- download actions are disabled by default
- run actions are disabled by default
- UI copy does not imply models can be downloaded or run
- catalog examples remain distinct from installed models

## Phase 3.9 — Runtime Setup Guidance Scaffold

Status: Initial informational setup guidance exists in `kora-studio-runtime-setup-guidance.md`. `/status` includes setup guidance metadata, and disabled actions route to guidance copy rather than active install, download, or run behavior.

Scope:

- setup guidance docs path
- disabled actions route to guidance
- catalog vs installed vs downloadable boundary
- runtime readiness distinction
- no install commands
- no model downloads
- no model execution
- no runtime model list commands
- no private model directory scans
- no provider/cloud route

Acceptance criteria:

- setup guidance is informational only
- disabled actions remain disabled
- UI copy does not imply install/download/run behavior is connected
- provider/cloud routes remain disabled by default

## Phase 3.10 — First-run UI Order Scaffold

Status: Initial static preview ordering exists. The local preview page and React demo copy now orient first-run users around Launch/local-only status, Your Computer, Model Capability Estimate, Runtime Status, Catalog vs Installed, Setup Guidance, Disabled Download/Run Actions, KORA Boost Boundary, Execution Viewer, Standard Mode vs KORA Boost, and Report Viewer Placeholder.

Scope:

- first-run section order metadata
- static preview order cleanup
- React demo first-run surface copy
- disabled/planned action language preserved
- no model downloads
- no model execution
- no provider/cloud route

## Phase 3.11 — v0.2 Status Contract

Status: Initial v0.2 status contract fields exist. `/status` preserves the existing preview fields and also exposes grouped `studio_status`, `launch_boundary`, `disabled_action_state`, and `claim_boundaries` blocks so the first-run UI can read status, launch limits, disabled action state, fixture boundaries, and local-only constraints without inferring them from scattered fields.

Scope:

- grouped Studio status
- launch/local-only boundary
- disabled action state
- provider-disabled and cloud-disabled defaults
- system profile
- model capability estimate
- runtime status and installed model summary
- model catalog status and recommendations
- setup guidance status
- execution viewer fixture status
- Standard Mode vs KORA Boost fixture status
- report viewer placeholder status
- claim boundary grouping

Acceptance criteria:

- status response remains backward compatible with existing safe fields
- provider calls remain disabled
- cloud sync remains disabled
- download/run/model execution remain disconnected
- fixture and report placeholders remain clearly labelled

Acceptance criteria:

- first-run sections appear in the intended order
- catalog examples remain distinct from installed models
- setup guidance remains informational only
- execution viewer remains fixture/demo or placeholder until future harness work

## Phase 3.11 — Execution Viewer Fixture/Event Scaffold

Status: Initial local fixture/mock event scaffold exists. `/status` exposes execution viewer schema fields, fixture event data, fixture event count, and claim boundary text. The static preview page shows the fixture stage sequence without real model execution.

Scope:

- local fixture/mock event schema
- request received stage
- deterministic route check stage
- structured lookup stage
- validation pass stage
- model fallback skipped stage
- final counters stage
- provider/cloud disabled state in every event
- no model downloads
- no model execution
- no provider/cloud route

Acceptance criteria:

- execution viewer events include required UI/report schema fields
- preview UI labels events as fixture/mock data
- final counters are shown as fixture counters only
- no production behavior, cost reduction, energy reduction, or runtime execution claim is made

## Phase 3.12 — Standard Mode vs KORA Boost Comparison Fixture

Status: Initial local fixture/mock comparison exists. `/status` exposes Standard Mode vs KORA Boost comparison data, metrics, metric cards, and claim boundary text. The static preview page shows comparison cards and fixture-only metrics.

Scope:

- shared synthetic fixture input
- Standard Mode fixture baseline with model call counted
- KORA Boost fixture path with deterministic route, structured lookup, validation pass, and model call avoided
- metric cards for baseline model calls, KORA model calls, avoided model calls, deterministic routes, model escalations, and validation passes
- provider/cloud disabled state
- no model downloads
- no model execution
- no provider/cloud route
- no cost or energy claim

Acceptance criteria:

- same fixture input is represented for both modes
- comparison reports route and counter differences
- metrics are labelled as local fixture/mock data
- no production behavior, billing, cost, energy, or runtime execution claim is made

## Phase 3.13 — Report Viewer and Export Placeholder

Status: Initial local report viewer/export placeholder exists. `/status` exposes fixture report metadata, report counters, local-only boundary fields, disabled export state, and claim boundary text. The static preview page shows a report viewer placeholder and export placeholder without scanning arbitrary local files.

Scope:

- report viewer fixture metadata
- report section list
- fixture counter summary
- boundary warnings
- disabled export placeholder
- no arbitrary local file scans
- no report uploads
- no generated report commits
- no provider/cloud route
- no new benchmark evidence

Acceptance criteria:

- report viewer data is labelled as fixture metadata only
- export action remains disabled
- preview UI displays claim boundary text
- no local report file scan, upload, provider call, or generated report commit is connected

## Phase 3.14 — v0.3 Local Harness Preview

Status: Initial v0.3 local harness preview exists. `/status` exposes approved deterministic sample requests, a generated sample run, generated counters, a local harness-generated Standard Mode vs KORA Boost comparison, and report viewer metadata sourced from local harness summary data.

Scope:

- approved deterministic sample requests
- local harness event generation
- generated counters
- model-needed boundary without model execution
- Local Harness Preview UI panel
- local harness-generated comparison output
- report viewer placeholder sourced from local harness summary metadata
- no POST run endpoint
- no SSE stream
- no model downloads
- no model execution
- no provider/cloud route

Acceptance criteria:

- local harness data is visible in `/status`
- preview UI shows local harness status, sample request, event stages, and counters
- comparison metrics are labelled as local deterministic harness output
- report viewer remains placeholder behavior
- claim boundaries remain visible

## Phase 3.15 — v0.4 Local Run Trigger Scaffold

Status: v0.4 local preview/demo readiness is documented. See `docs/kora-studio/kora-studio-v0-4-local-run-trigger-plan.md`, `docs/kora-studio/kora-studio-v0-4-readiness-report.md`, and `docs/kora-studio/kora-studio-v0-4-goal-report.md`.

Goal: Add a local run trigger surface for approved deterministic sample requests and optional event-stream scaffolding for generated harness events.

Scope:

- approved request selection
- local-only run trigger through `POST /api/harness/run`
- static Run Local Harness trigger panel in the local preview UI
- in-memory run retrieval through `GET /api/harness/run/{run_id}`
- generated event retrieval through `GET /api/harness/events?run_id=<id>`
- generated counters
- generated local harness event timeline in the preview UI
- local harness Standard Mode vs KORA Boost comparison boundary in the preview UI
- generated event SSE stream through `GET /api/harness/sse?run_id=<id>`
- selected-run comparison update
- selected-run report metadata update with disabled file export state
- no arbitrary prompt execution unless explicitly bounded in a later task
- browser-side trigger calls only `POST /api/harness/run` with approved request IDs
- no provider calls
- no cloud sync
- no model downloads
- no real model execution
- no private model directory scans
- no runtime model list commands

Acceptance criteria:

- approved sample request can be triggered locally
- preview UI lists approved request IDs, route classes, and trigger boundaries
- invalid request ids are rejected
- model-needed boundaries return `execution_not_connected`
- run state and counters remain local deterministic harness output
- run records are in-memory only and are not persisted
- generated event retrieval is non-SSE and does not stream model tokens
- SSE streams generated harness events only and does not stream model tokens, provider output, or model output
- generated counters and comparison panels are local harness output only, not production evidence
- generated run report metadata includes report source, run/request relationship, event count, counter summary, comparison status, and disabled export state
- report metadata preview does not scan arbitrary local files, write report files, upload reports, or create production evidence
- smoke checks cover planned harness endpoints if implemented

## Phase 3.16 — v0.5 Local Interactive UI Plan

Status: v0.5 local interactive UI readiness is documented. See `docs/kora-studio/kora-studio-v0-5-local-interactive-ui-plan.md`, `docs/kora-studio/kora-studio-v0-5-readiness-report.md`, and `docs/kora-studio/kora-studio-v0-5-goal-report.md`.

Goal: Add a local interactive UI for approved deterministic sample requests and selected-run state.

Scope:

- approved request selector
- Run Local Harness button
- selected request preview
- browser-local selected-run state
- generated event timeline rendering for selected run through `GET /api/harness/events?run_id=<id>`
- selected-run counters and comparison rendering
- selected-run report metadata preview
- no arbitrary prompt input
- no model execution
- no provider calls
- no downloads
- no cloud sync
- no private model directory scans
- no runtime model list commands

Acceptance criteria:

- interactive UI only calls existing localhost harness endpoints
- selector lists approved request IDs without arbitrary prompt input
- Run Local Harness calls `POST /api/harness/run` with the selected approved request ID only
- selected-run event timeline fetches generated local harness events only and does not use SSE yet
- selected-run counters and comparison render from the selected local harness run response only
- selected-run report metadata renders from `report_metadata_summary` with file export and file writing disabled
- selected-run state stays browser-local
- model-needed boundaries remain `execution_not_connected`
- no production cost, energy, provider, model execution, or unsupported larger-model claim is introduced

## Phase 3.17 — v0.6 Frontend Interaction Hardening Plan

Status: v0.6 frontend interaction hardening readiness is documented. The local preview includes selected-run error state, Retry Last Approved Request behavior, browser-local run history with active-run cards and compact counters, and optional generated-event SSE UI with fallback to the local events endpoint. See `docs/kora-studio/kora-studio-v0-6-frontend-interaction-hardening-plan.md`, `docs/kora-studio/kora-studio-v0-6-readiness-report.md`, and `docs/kora-studio/kora-studio-v0-6-goal-report.md`.

Goal: Harden the local preview interaction layer around selected-run errors, retry behavior, browser-local history, optional generated-event SSE display, and local preview reliability.

Scope:

- selected-run error state display
- retry last approved request
- local endpoint unavailable messages
- malformed local response messages
- browser-local run history state
- selected-run history list
- active selected-run history card and compact counter summary
- selected `run_id` switching in browser memory
- clear local state action
- optional generated-event SSE UI for existing local harness runs
- fallback to generated event retrieval
- no arbitrary prompt input
- no model execution
- no provider calls
- no downloads
- no cloud sync
- no private model directory scans
- no runtime model list commands
- no report file export

Acceptance criteria:

- retry behavior is limited to approved request IDs
- browser-local history is not persisted to disk or cloud
- optional SSE UI streams generated harness events only
- selected-run error copy remains claim-safe
- local preview smoke checks cover v0.6 interaction markers
- no production cost, energy, provider, model execution, or unsupported larger-model claim is introduced

## Phase 3.18 — v0.7 UI/UX Board

Status: Claude Design source of truth captured. Implementation should wait for review before changing the local preview layout. Use `docs/kora-studio/kora-studio-v0-7-claude-design-source-of-truth.md` as the preferred source of truth, with `docs/kora-studio/kora-studio-v0-7-chat-first-minimal-ui-ux-boards.md` as supporting context. Keep older v0.7 boards as background only.

Goal: Align the next KORA Studio local preview layout with a minimal chat-first web app pattern while preserving KORA Studio's local-first AI Task Execution Router positioning.

Scope:

- approval board before implementation
- split minimal boards before implementation
- quiet top bar
- open-source LLM search and selection
- compact selected-model label
- centered main work surface
- right-side collapsible detail drawer
- model/runtime/catalog boundary placement inside the drawer or near risky actions
- no external CDN or font dependency copied from the reference prototype
- no arbitrary prompt input
- no model execution
- no provider calls
- no downloads
- no cloud sync
- no report export

Acceptance criteria:

- UI direction is reviewed before implementation
- LM Studio-like desktop workbench patterns are treated as layout inspiration, not product positioning
- KORA Studio remains framed as a local-first AI Task Execution Router workspace
- claim boundaries remain visible near affected surfaces
- implementation tasks do not start until the board is approved or revised

## Phase 4 — Report Viewer

Goal: Render existing local Markdown validation reports.

Scope:

- select local report path
- render Markdown
- show counter summary if structured data is available
- warn not to commit generated reports by default

Acceptance criteria:

- can load `/tmp/kora_customer_support_validation.md`
- displays boundary language
- does not upload report

## Phase 5 — Counter Dashboard

Goal: Show KORA validation counters as cards.

Counters:

- `total_requests`
- `baseline_model_calls`
- `kora_model_calls`
- `avoided_model_calls`
- `avoided_model_call_rate`
- `deterministic_routes`
- `model_escalations`
- `validation_pass_count`
- `validation_fail_count`
- `error_count`
- `fallback_count`

Acceptance criteria:

- cards render from fixture or summary JSON
- no cost or energy conversion
- local/no-network mode clearly labeled

## Phase 6 — Project Chat Mock

Goal: Create a project-based chat shell with mock/local placeholder messages.

Scope:

- project list
- conversation panel
- message list
- Standard Mode / KORA Boost toggle
- execution trace placeholder

Non-scope:

- no real model chat yet
- no provider calls
- no cloud sync

## Phase 7 — Ollama Runtime Detection

Goal: Detect whether Ollama is installed/available.

Scope:

- local detection only
- fail closed if unavailable
- no model pull yet
- no remote provider fallback

Acceptance criteria:

- detected / not detected state
- clear install/help copy
- tests can mock detection

## Phase 8 — Model List and Recommendation

Goal: Show supported local model options and recommended model/workflow.

Scope:

- static supported model list first
- system capability heuristic later
- Standard Mode recommendation
- KORA Boost workflow recommendation
- explain that the user's machine may be comfortable with a specific local model tier
- explain that KORA does not make large models smaller or remove model memory requirements
- explain that larger-model workflow feasibility depends on memory, runtime support, quantization, and validation

Acceptance criteria:

- does not claim impossible model support
- no bigger-model physical execution claim
- no all-open-source-LLM support claim
- uses benefit copy safely

## Phase 9 — Local Chat Integration

Goal: Integrate selected local runtime after explicit opt-in.

Scope:

- future task only
- likely Ollama first
- no provider API keys
- no cloud upload
- local runtime only

Acceptance criteria:

- model calls are measured
- execution path is visible
- local/no-network and local-runtime modes remain distinct

## Phase 10 — KORA Boost Execution Trace

Goal: Show route-level trace for each chat interaction.

Trace fields:

- `selected_route`
- `model_called`
- `deterministic_route_used`
- `model_escalation_used`
- `validation_result`
- `latency_ms`
- `counters`

Acceptance criteria:

- user can see what took the fast path
- user can see when model was used
- no unsupported cost/energy conversion

## Phase 11 — v0.8 Final UI Board Implementation

Status: complete as a local preview/demo milestone. See [KORA Studio v0.8 readiness report](kora-studio-v0-8-readiness-report.md) and [KORA Studio v0.8 goal report](kora-studio-v0-8-goal-report.md). The shell scaffold, right details drawer migration, compact local catalog model selector, composer-approved-harness action alignment, and responsive/mobile layout pass are implemented in the local preview.

Goal: Implement the final v0.7 UI/UX board into the local preview while preserving all local-only harness behavior and claim boundaries.

Target structure:

- ChatGPT-like sparse default workspace
- small left mini rail for workspace/task navigation only
- compact top model selector
- centered composer as the primary surface
- hidden right details drawer for runtime, catalog, route, counters, report metadata, and claim boundaries
- mobile overlay behavior for the left rail and right drawer

Scope:

- local preview HTML/CSS/vanilla JavaScript only
- no new frontend dependency unless explicitly approved
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- default preview screen is sparse and composer-centered
- left rail remains a workspace/task aid, not a diagnostics dashboard
- dense harness/runtime/report details move into the right drawer
- approved local harness run behavior still works
- selected-run state/history remain browser-local only
- validation and smoke checks pass

## Recommended First 10 Implementation Issues

These are future issue candidates. Do not create the issues from this document without maintainer approval.

## Phase 12 — v0.9 Local Usability Polish

Status: complete as a local preview/demo milestone. See [KORA Studio v0.9 readiness report](kora-studio-v0-9-readiness-report.md) and [KORA Studio v0.9 goal report](kora-studio-v0-9-goal-report.md). The right details drawer and mobile left rail now have local open/close controls, ARIA state, close buttons, and Escape close behavior. The compact model selector now marks the active estimate as catalog-only selected state without implying installation, download, or execution. The shell also includes broader keyboard/focus markers, focus-visible styling, smoke-checkable accessibility state, and a [v0.9 mobile visual QA checklist](kora-studio-v0-9-mobile-visual-qa-checklist.md).

Goal: Polish the v0.8 local preview shell with keyboard/focus accessibility, explicit drawer and rail interactions, clearer model selector selected state, stronger mobile QA, and less reliance on the legacy detailed preview.

Scope:

- local preview HTML/CSS/vanilla JavaScript only
- no new frontend dependency unless explicitly approved
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- right drawer can open and close locally
- left rail can open and close locally on small-screen scaffolds
- Escape closes shell overlays
- model selector selected state remains catalog-only and claim-safe
- composer remains approved-harness-only
- validation and smoke checks pass

## Phase 13 — v1.0 Preview Readiness

Status: complete as a local preview/demo milestone. See [KORA Studio v1.0 preview readiness plan](kora-studio-v1-0-preview-readiness-plan.md), [KORA Studio v1.0 shell-first information architecture](kora-studio-v1-0-shell-first-information-architecture.md), [KORA Studio v1.0 readiness report](kora-studio-v1-0-readiness-report.md), and [KORA Studio v1.0 goal report](kora-studio-v1-0-goal-report.md). The shell now has v1.0 local-only boundary markers and a compact boundary strip covering provider calls, cloud sync, downloads, model execution, and report export/write status. The shell and right drawer also expose selected-run surface status for timeline, counters, comparison, and report metadata so these details no longer depend only on the legacy preview. The legacy detailed preview is now collapsed by default and labelled as compatibility/developer scaffolding. The local preview smoke check includes a dedicated v1.0 shell-first result.

Goal: Reduce legacy detailed preview dependence and make the final minimal shell the primary local preview experience while preserving local-only claim boundaries.

Scope:

- local preview HTML/CSS/vanilla JavaScript only
- shell-first information architecture
- local-only status and boundary consolidation in shell surfaces
- selected-run timeline, counters, comparison, and report metadata available through shell/drawer surfaces
- right drawer as the primary place for detailed runtime, route, counter, report, and claim details
- legacy preview collapsed, relabelled, or clearly secondary once required shell coverage exists
- no new frontend dependency unless explicitly approved
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- final shell is the primary local preview surface
- first-run local-only status is understandable without relying on the legacy preview
- selected-run details remain available in shell/drawer surfaces
- legacy detailed preview is reduced or clearly marked as compatibility scaffolding
- composer remains approved-harness-only
- model selector remains catalog-estimate-only
- validation and live local smoke checks pass

## Phase 14 — v1.1 Shell-only Preview Hardening

Status: complete as a local preview/demo milestone. See [KORA Studio v1.1 shell-only hardening plan](kora-studio-v1-1-shell-only-hardening-plan.md), [KORA Studio v1.1 shell diagnostics coverage map](kora-studio-v1-1-shell-diagnostics-coverage-map.md), [KORA Studio v1.1 readiness report](kora-studio-v1-1-readiness-report.md), and [KORA Studio v1.1 goal report](kora-studio-v1-1-goal-report.md). v1.1 hardens the shell and right drawer so normal local preview inspection no longer depends on the collapsed legacy detailed preview.

Goal: Reduce remaining legacy detailed preview dependence and make shell/drawer surfaces sufficient for local preview inspection while preserving local-only claim boundaries.

Scope:

- local preview HTML/CSS/vanilla JavaScript only
- shell/drawer diagnostics coverage
- shell-visible selected-run state
- shell-visible local-only boundaries
- legacy preview retained only as collapsed compatibility/developer scaffold
- shell-only smoke markers
- no new frontend dependency unless explicitly approved
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- shell/drawer surfaces cover core local preview information without requiring the legacy preview
- legacy preview remains collapsed and clearly secondary
- selected-run details remain visible through shell/drawer surfaces
- composer remains approved-harness-only
- model selector remains catalog-estimate-only
- validation and live local smoke checks pass

## Phase 15 — v1.2 Frontend Extraction / Componentization Planning

Status: complete as a maintainability/refactor milestone. See [KORA Studio v1.2 frontend extraction plan](kora-studio-v1-2-frontend-extraction-plan.md), [KORA Studio v1.2 component inventory](kora-studio-v1-2-component-inventory.md), [KORA Studio v1.2 extraction smoke check](kora-studio-v1-2-extraction-smoke-check.md), [KORA Studio v1.2 readiness report](kora-studio-v1-2-readiness-report.md), and [KORA Studio v1.2 goal report](kora-studio-v1-2-goal-report.md). v1.2 extracted shell layout, right details drawer rendering, selected-run panel rendering, and embedded CSS/JavaScript templates into dedicated helpers while behavior, endpoints, dependencies, smoke markers, and claim boundaries remain unchanged.

Goal: Improve maintainability of the shell-first local preview by planning component boundaries for shell layout, left rail, model selector, composer, selected-run panels, right drawer, run history, event stream status, boundary strip, and legacy compatibility reference.

Scope:

- documentation/planning first
- local preview HTML/CSS/vanilla JavaScript structure
- no new product behavior
- no frontend framework migration yet
- no new dependency unless explicitly approved later
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- current embedded shell sections are mapped into component/render responsibilities
- recommended extraction path keeps behavior unchanged
- smoke markers and endpoint contracts remain stable
- local-only and claim-safe boundaries remain unchanged

## Phase 16 — v1.3 Local Frontend Extraction Hardening

Status: complete. See [KORA Studio v1.3 frontend extraction hardening plan](kora-studio-v1-3-frontend-extraction-hardening-plan.md), [KORA Studio v1.3 render fragment inventory](kora-studio-v1-3-render-fragment-inventory.md), [KORA Studio v1.3 render helper API contracts](kora-studio-v1-3-render-helper-api-contracts.md), [KORA Studio v1.3 static asset serving tradeoff](kora-studio-v1-3-static-asset-serving-tradeoff.md), [KORA Studio v1.3 readiness report](kora-studio-v1-3-readiness-report.md), and [KORA Studio v1.3 goal report](kora-studio-v1-3-goal-report.md). v1.3 continues local frontend extraction hardening by documenting remaining render fragments, clarifying render/data assembly boundaries, and stabilizing helper API contracts without changing behavior, adding dependencies, adding external assets, or weakening local-only claim boundaries.

Goal: Improve maintainability of remaining local preview render fragments after v1.2 helper extraction.

Scope:

- remaining render fragment inventory
- helper API stabilization
- render/data assembly boundary documentation
- static asset serving tradeoff documentation only
- behavior-preserving extraction only when low-risk and test-covered
- no product behavior change
- no frontend framework migration
- no dependency addition
- no external static asset serving unless explicitly approved later
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- remaining render fragments and data assembly boundaries are documented
- helper API contracts are clearer and test-covered
- any extraction preserves behavior and markers
- validation and live smoke checks pass
- readiness and consolidated goal reports are created

## Phase 17 — v1.4 Local Preview Fragment Extraction

Status: complete as a maintainability/refactor milestone. See [KORA Studio v1.4 local preview fragment extraction plan](kora-studio-v1-4-local-preview-fragment-extraction-plan.md), [KORA Studio v1.4 fragment inventory](kora-studio-v1-4-fragment-inventory.md), [KORA Studio v1.4 render helper contracts](kora-studio-v1-4-render-helper-contracts.md), [KORA Studio v1.4 readiness report](kora-studio-v1-4-readiness-report.md), and [KORA Studio v1.4 goal report](kora-studio-v1-4-goal-report.md). v1.4 continues conservative local preview fragment extraction by targeting the next safe server-owned generated local harness preview fragments while preserving helper contracts, marker coverage, local-only boundaries, inline CSS/JavaScript, and behavior. The approved request selector/local harness trigger panels are extracted into `kora/studio_harness_request_render.py`, retry/error/run-history panels are extracted into `kora/studio_run_state_render.py`, and the collapsed legacy opening wrapper is extracted into `kora/studio_legacy_render.py`.

Goal: Extract the next safe group of server-owned local preview fragments without product behavior change.

Scope:

- generated local harness request/trigger panel candidates
- retry/error state and browser-local run history panel candidates
- legacy compatibility/reference helper reassessment only if safe
- helper contract and marker coverage hardening
- no product behavior change
- no endpoint behavior change
- no frontend framework migration
- no dependency addition
- no external static asset serving
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- next server-owned fragments are inventoried and classified
- any extraction is behavior-preserving and test-covered
- all component markers and local-only boundaries remain visible
- inline CSS/JavaScript decision remains unchanged
- full validation and live smoke checks pass
- readiness and consolidated goal reports are created

## Phase 18 — v1.5 Local Preview Server Slimming

Status: complete as a maintainability/refactor milestone. See [KORA Studio v1.5 server slimming plan](kora-studio-v1-5-server-slimming-plan.md), [KORA Studio v1.5 server-owned fragment inventory](kora-studio-v1-5-server-owned-fragment-inventory.md), [KORA Studio v1.5 server responsibility audit](kora-studio-v1-5-server-responsibility-audit.md), [KORA Studio v1.5 readiness report](kora-studio-v1-5-readiness-report.md), and [KORA Studio v1.5 goal report](kora-studio-v1-5-goal-report.md). v1.5 continues conservative maintainability work by identifying remaining server-owned UI/data-display fragments in `kora/studio_server.py`, extracting only safe low-risk display fragments, and preserving endpoint behavior, helper contracts, smoke markers, inline CSS/JavaScript, and local-only claim boundaries. The shell boundary strip, launch/local-only status section, and KORA Boost Boundary section are extracted into `kora/studio_status_boundary_render.py`. Model selector option rows, system profile, model capability, runtime status, catalog versus installed, setup guidance, and disabled download/run action display fragments are extracted into `kora/studio_model_runtime_render.py`. Local Harness Preview, Execution Viewer, Standard Mode vs KORA Boost, and Report Viewer Placeholder display sections are extracted into `kora/studio_harness_display_render.py`; harness data assembly, comparison/report metadata assembly, escaping, and endpoint behavior remain server-owned. Task 510 hardens helper contract tests so helpers cannot take over server routing, request parsing, response writing, payload assembly, local harness dispatch, JSON serialization/deserialization, HTML escaping, or final document assembly.

Goal: Slim `kora/studio_server.py` without product behavior change.

Scope:

- remaining server-owned UI/data-display fragment inventory
- status/boundary display extraction candidates
- model/catalog/runtime display extraction candidates
- harness endpoint guidance/display extraction candidates
- server responsibility audit
- helper contract and marker coverage hardening
- no product behavior change
- no endpoint behavior change
- no frontend framework migration
- no dependency addition
- no external static asset serving
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- remaining server-owned UI/data-display fragments are inventoried and classified
- safe extractions preserve behavior and markers
- server-owned and helper-owned responsibilities are documented
- static asset serving remains a future decision
- full validation and live smoke checks pass
- readiness and consolidated goal reports are created

## Phase 19 — v1.6 Local Preview Architecture Review

Status: complete as a docs-only architecture decision milestone. See [KORA Studio v1.6 architecture review](kora-studio-v1-6-architecture-review.md) and [KORA Studio v1.6 goal report](kora-studio-v1-6-goal-report.md). v1.6 reviews the post-v1.5 local preview architecture, compares continuing Python helper extraction, planning local static asset serving, preparing a future frontend framework extraction, and pausing refactor work for product capability scaffolding. It recommends a v1.7 local static asset serving plan before any CSS or JavaScript file serving is implemented.

Goal: Decide the next architecture direction after v1.5 without changing product behavior.

Scope:

- local preview server responsibility review
- render helper ownership review
- inline CSS/JavaScript tradeoff review
- static asset serving risk and benefit review
- frontend framework timing review
- product capability scaffolding sequencing review
- no product behavior change
- no endpoint behavior change
- no static asset serving implementation
- no frontend tooling or dependency addition
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- current server/helper responsibilities are documented
- architecture options are compared with risk and test implications
- static asset serving is recommended only as a future planning goal
- frontend framework extraction remains deferred
- claim boundaries remain unchanged
- validation passes

## Phase 20 — v1.7 Local Static Asset Serving Plan

Status: complete as a docs-only static asset serving plan. See [KORA Studio v1.7 static asset serving plan](kora-studio-v1-7-static-asset-serving-plan.md) and [KORA Studio v1.7 goal report](kora-studio-v1-7-goal-report.md). v1.7 defines the constraints for any future local CSS/JavaScript static asset serving work without implementing routes, moving inline assets, adding dependencies, changing endpoint behavior, or changing UI behavior.

Goal: Define the future local static asset serving boundary before implementation.

Scope:

- current inline CSS/JavaScript state review
- static asset route namespace planning
- asset allowlist planning
- path traversal rejection requirements
- MIME and cache behavior requirements
- no-external-assets/CDN policy
- smoke marker and test expectations
- migration option comparison
- no product behavior change
- no endpoint behavior change
- no static asset serving implementation
- no CSS/JavaScript migration out of inline helpers
- no frontend tooling or dependency addition
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- future static asset serving requirements are documented
- security constraints are explicit
- testing and smoke expectations are defined
- migration options are compared
- CSS-only first implementation is recommended only for a future approved goal
- claim boundaries remain unchanged
- validation passes

## Phase 21 — v1.8 Static Asset Allowlist Test Planning

Status: complete as a docs-only design/test plan. See [KORA Studio v1.8 static asset allowlist test plan](kora-studio-v1-8-static-asset-allowlist-test-plan.md). Task 516 prepares the next implementation goal by specifying the future CSS-only asset allowlist, rejection rules, MIME/header expectations, security boundary, test plan, and migration sequence. It does not implement static asset serving, add routes, move CSS or JavaScript out of inline helpers, add dependencies, or change endpoint/UI behavior.

Goal: Define tests and boundaries for a future CSS-only local static asset route.

Scope:

- first asset proposal for `/studio-assets/studio.css`
- explicit allowlist definition
- path traversal and private-file rejection rules
- MIME and cache behavior expectations
- local-only and no-CDN policy
- future unit/smoke test coverage
- conservative CSS-only migration sequence
- no static asset route implementation
- no CSS/JavaScript migration out of inline helpers
- no JavaScript static serving
- no frontend framework or dependency addition
- no product behavior change
- no endpoint behavior change
- no UI behavior change
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- future CSS asset route is defined as a single allowlisted candidate
- rejection rules cover traversal, unknown assets, directories, and private paths
- MIME/cache expectations are documented
- tests are specified before implementation
- migration keeps JavaScript inline
- claim boundaries remain unchanged
- validation passes

## Phase 22 — v1.8 CSS-only Static Asset Route

Status: complete as a narrow local static asset implementation. See [KORA Studio v1.8 readiness report](kora-studio-v1-8-readiness-report.md) and [KORA Studio v1.8 goal report](kora-studio-v1-8-goal-report.md). Goal 517G implements the approved CSS-only route `/studio-assets/studio.css` using the existing `render_studio_css()` output as the source, updates the root preview to reference that local stylesheet, and keeps JavaScript inline through `render_studio_javascript()`.

Goal: Implement the single allowlisted CSS asset route while preserving endpoint behavior, local-only boundaries, smoke markers, and claim safety.

Scope:

- `/studio-assets/studio.css` route implementation
- CSS source remains `render_studio_css()`
- `Content-Type: text/css; charset=utf-8`
- `Cache-Control: no-store`
- exact CSS allowlist only
- unknown asset rejection
- directory request rejection
- traversal and encoded traversal rejection
- root preview references only the local CSS asset
- JavaScript remains inline
- no JavaScript static serving
- no wildcard static route
- no directory listing
- no arbitrary filesystem serving
- no external assets or CDN
- no frontend framework or dependency addition
- no product behavior change
- no arbitrary prompt execution
- no provider calls
- no model execution
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing

Acceptance criteria:

- approved CSS asset route returns CSS with expected MIME/cache headers
- unsafe/unknown asset paths fail without exposing local filesystem details
- root preview references `/studio-assets/studio.css`
- root preview keeps inline JavaScript
- endpoint and smoke marker coverage remains stable
- full validation and live smoke checks pass

## Phase 23 — v1.9 CSS Asset Source File Migration

Status: complete as a narrow source migration. See [KORA Studio v1.9 CSS asset source file migration report](kora-studio-v1-9-css-asset-source-file-migration-report.md) and [KORA Studio v1.9 goal report](kora-studio-v1-9-goal-report.md). Goal 518G moves the Studio CSS source into a package-controlled first-party CSS file while preserving the existing `/studio-assets/studio.css` route, exact allowlist, `no-store` cache behavior, root preview stylesheet reference, and inline JavaScript boundary.

Goal: Make the CSS asset source file-based without introducing broad static serving, frontend tooling, or product behavior changes.

Scope:

- CSS source file: `kora/studio_assets/studio.css`
- package resource loader remains behind `render_studio_css()`
- `/studio-assets/studio.css` remains the only served CSS asset
- `Content-Type: text/css; charset=utf-8`
- `Cache-Control: no-store`
- exact CSS allowlist only
- unknown asset rejection
- directory request rejection
- traversal and encoded traversal rejection
- root preview references only the local CSS asset
- JavaScript remains inline through `render_studio_javascript()`
- no JavaScript static serving
- no wildcard static route
- no directory listing
- no arbitrary filesystem serving
- no external assets or CDN
- no frontend framework or dependency addition
- no product behavior change

Acceptance criteria:

- CSS helper returns the package-controlled source file contents
- approved CSS asset route still returns CSS with expected MIME/cache headers
- unsafe/unknown asset paths fail without exposing local filesystem details
- root preview references `/studio-assets/studio.css`
- root preview keeps inline JavaScript and no external JavaScript source
- endpoint and smoke marker coverage remains stable
- full validation and live smoke checks pass

## Phase 24 — v2.0 JavaScript Asset Migration

Status: complete as a narrow package-controlled JavaScript asset migration. See [KORA Studio v2.0 JavaScript asset migration decision report](kora-studio-v2-0-javascript-asset-migration-decision-report.md) and [KORA Studio v2.0 goal report](kora-studio-v2-0-goal-report.md). Goal 519G moves the Studio interaction script into `kora/studio_assets/studio.js` and serves it through the existing local asset namespace with an explicit allowlist for `studio.css` and `studio.js` only.

Goal: Move JavaScript from inline final document assembly to a package-controlled source file without adding broad static serving, frontend tooling, external assets, or product behavior changes.

Scope:

- JavaScript source file: `kora/studio_assets/studio.js`
- package resource loader remains behind `render_studio_javascript()`
- `/studio-assets/studio.css` remains the only served CSS asset
- `/studio-assets/studio.js` is the only served JavaScript asset
- explicit allowlist for `studio.css` and `studio.js`
- JavaScript response: `application/javascript; charset=utf-8`
- CSS response: `text/css; charset=utf-8`
- `Cache-Control: no-store` for both local preview assets
- unknown asset rejection
- directory request rejection
- traversal and encoded traversal rejection
- no wildcard static route
- no directory listing
- no arbitrary filesystem serving
- no external assets or CDN
- no frontend framework, bundler, minifier, npm workflow, or dependency addition
- no product behavior change

Acceptance criteria:

- JavaScript helper returns the package-controlled source file contents
- approved JavaScript asset route returns expected MIME/cache headers
- approved CSS asset route behavior remains stable
- unsafe/unknown asset paths fail without exposing local filesystem details
- root preview references `/studio-assets/studio.css` and `/studio-assets/studio.js`
- root preview keeps approved request JSON inline but does not embed the interaction script body
- endpoint and smoke marker coverage remains stable
- full validation and live smoke checks pass

## Phase 25 — v2.1 Local Asset CSP Readiness

Status: complete as a local preview CSP readiness step. See [KORA Studio v2.1 local asset CSP readiness report](kora-studio-v2-1-local-asset-csp-readiness-report.md) and [KORA Studio v2.1 goal report](kora-studio-v2-1-goal-report.md). Goal 520G adds a minimal enforced `Content-Security-Policy` header to the root Studio HTML route only while preserving package-controlled local CSS/JavaScript assets, approved request JSON behavior, API/SSE/status responses, and local-only claim boundaries.

Goal: Add a bounded local-preview CSP header without claiming production security readiness.

Scope:

- root HTML response includes local preview CSP
- API, SSE, health, status, CSS asset, and JavaScript asset responses are not altered with CSP
- CSS and JavaScript remain package-controlled assets under `/studio-assets`
- approved request JSON remains inline as `type="application/json"`
- no external source allowances
- no broad wildcard source allowances
- no `unsafe-inline`
- no `unsafe-eval`
- no nonce framework
- no hash management
- no frontend framework, bundler, minifier, npm workflow, or dependency addition
- no product behavior change
- no production security readiness claim

Acceptance criteria:

- root HTML CSP includes only local preview allowances needed for self-hosted CSS, JavaScript, fetch, and SSE
- CSP does not include external hosts, broad wildcards, `unsafe-inline`, or `unsafe-eval`
- API/SSE/status and asset routes are not accidentally changed by the CSP step
- root preview still references `/studio-assets/studio.css` and `/studio-assets/studio.js`
- approved request JSON behavior remains unchanged
- endpoint and smoke marker coverage remains stable
- full validation and live smoke checks pass

## Phase 26 — v2.2 Browser-Level CSP Smoke Validation

Status: complete as an optional browser-level CSP smoke validation step. See [KORA Studio v2.2 browser-level CSP smoke validation report](kora-studio-v2-2-browser-csp-smoke-validation-report.md) and [KORA Studio v2.2 goal report](kora-studio-v2-2-goal-report.md). Goal 521G adds a dependency-light optional browser smoke script that uses Playwright through `npx` when available, validates the root CSP header in a real browser, confirms local CSS/JavaScript asset loading, checks initial shell readiness, clicks the visible Run Local Harness control, and fails on browser CSP violations.

Goal: Validate the local preview under the enforced CSP at browser/runtime level without adding repo dependencies or production security readiness claims.

Scope:

- optional browser smoke script: `scripts/check_kora_studio_browser_csp.py`
- script accepts only localhost preview URLs
- script uses `npx` and temporary Playwright files when available
- no committed Node package manifest, lockfile, or browser dependency
- no frontend framework, bundler, minifier, npm workflow, external asset, or CDN addition
- no CSP broadening
- no `unsafe-inline`
- no `unsafe-eval`
- no wildcard or external host allowances
- root preview inline styles removed in favor of package CSS classes
- data favicon removed to avoid CSP noise
- local CSS and JavaScript package assets preserved
- approved request JSON behavior preserved
- no production security readiness claim

Acceptance criteria:

- browser smoke passes against a running local preview when Playwright is available through `npx`
- browser smoke fails on CSP console violations
- browser smoke verifies root CSP header, local CSS/JS assets, initial shell readiness, approved request availability, and Run Local Harness interaction
- automated unit coverage remains dependency-light and does not require a browser
- existing server/header/static-route tests remain stable
- full validation and live smoke checks pass

## Phase 27 — v2.3 Browser CSP Smoke CI-Optional Policy

Status: complete as a CI-optional policy step. See [KORA Studio v2.3 browser CSP smoke CI-optional policy](kora-studio-v2-3-browser-csp-smoke-ci-optional-policy.md) and [KORA Studio v2.3 goal report](kora-studio-v2-3-goal-report.md). Goal 522G keeps the browser-level CSP smoke outside the default CI and pytest path while adding an explicit opt-in wrapper for CI or local validation environments.

Goal: Decide and document whether browser CSP smoke remains manual-only or becomes CI-optional without adding persistent frontend dependencies.

Decision:

- CI-optional, explicitly gated by `KORA_STUDIO_BROWSER_CSP_SMOKE=1`
- default GitHub CI remains release smoke plus pytest
- normal pytest remains browser-free and does not require `npx`
- no persistent Node dependency, root package manifest, lockfile, bundler, npm workflow, Playwright config, external asset, or CDN is added

Scope:

- add `scripts/check_kora_studio_browser_csp_ci_optional.sh`
- preserve `scripts/check_kora_studio_browser_csp.py`
- start a localhost-only Studio preview only when explicitly enabled
- run browser CSP smoke against that local preview
- stop the server cleanly on exit
- preserve root CSP and local asset route behavior
- preserve no wildcard static route, no directory listing, and no arbitrary filesystem serving
- preserve no production security readiness claim

Acceptance criteria:

- optional wrapper skips cleanly unless `KORA_STUDIO_BROWSER_CSP_SMOKE=1` is set
- optional wrapper can run the existing browser CSP smoke against a local preview when enabled
- dependency-light unit coverage proves the opt-in policy without launching a browser
- default CI/test path remains unchanged
- full validation, optional browser smoke, and standard preview smoke pass

## Phase 28 — v2.4 CSP Resource-Type Regression Guard

Status: complete as dependency-light pytest regression coverage. See [KORA Studio v2.4 CSP resource-type regression guard](kora-studio-v2-4-csp-resource-type-regression-guard.md) and [KORA Studio v2.4 goal report](kora-studio-v2-4-goal-report.md). Goal 523G adds static and server-rendered HTML guard coverage for CSP resource classes without adding frontend dependencies or changing browser smoke policy.

Goal: Prevent future local preview changes from silently adding blocked inline styles/scripts, remote resource URLs, embedded resource URL schemes, broad CSP sources, or new resource classes without explicit review.

Scope:

- add HTML parser-based guard coverage for root Studio HTML
- allow only `/studio-assets/studio.css` as the stylesheet
- allow only `/studio-assets/studio.js` as executable JavaScript
- keep approved request JSON as the only inline script block with `type="application/json"`
- reject resource-bearing attributes that point to `data:`, `blob:`, HTTP(S), protocol-relative, CDN, or remote URLs
- assert CSP directives remain narrow and exact for current local preview needs
- assert package CSS/JavaScript do not introduce remote or embedded resource URLs
- preserve optional browser CSP smoke and CI-optional wrapper behavior

Acceptance criteria:

- root HTML has no inline `style` attributes
- root HTML has no inline executable script blocks
- approved request JSON exception remains explicit
- root HTML references only current package-controlled Studio assets
- CSP has no `unsafe-inline`, `unsafe-eval`, wildcard, `data:`, `blob:`, HTTP(S), or external host sources
- package CSS has no `@import` or `url(...)` resource loading
- no persistent frontend dependency, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN is added
- full validation, optional browser smoke, and standard preview smoke pass

## Phase 29 — v2.5 CSP Violation Fixture Matrix

Status: complete as table-driven negative fixture coverage. See [KORA Studio v2.5 CSP violation fixture matrix](kora-studio-v2-5-csp-violation-fixture-matrix.md) and [KORA Studio v2.5 goal report](kora-studio-v2-5-goal-report.md). Goal 524G keeps the positive CSP/resource guards from v2.4 and adds representative rejected fixtures so future contributors can see which patterns require explicit review.

Goal: Make rejected CSP/resource patterns explicit without broadening Studio behavior.

Scope:

- add reusable test helpers for HTML resource, CSP source, and CSS resource policy violations
- add HTML negative fixtures for inline styles, inline executable scripts, external scripts, external stylesheets, `data:`, `blob:`, protocol-relative URLs, and unapproved Studio assets
- add CSP negative fixtures for wildcard sources, `unsafe-inline`, `unsafe-eval`, `data:`, `blob:`, external hosts, and new image/font directives
- add CSS negative fixtures for `@import`, `url(...)`, `data:`, `blob:`, and external URLs
- preserve the approved request JSON exception
- preserve optional browser CSP smoke and CI-optional wrapper behavior

Acceptance criteria:

- fixture matrix tests are dependency-light and browser-free
- fixture matrix tests fail for representative rejected patterns
- positive guard still passes for current Studio HTML, CSP, CSS, and JavaScript assets
- no CSP broadening or asset allowlist broadening is introduced
- no persistent frontend dependency, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN is added
- full validation, optional browser smoke, and standard preview smoke pass

## Phase 30 — v2.6 CSP Guard Helper Cleanup

Status: complete as test-module helper consolidation. See [KORA Studio v2.6 CSP guard helper cleanup](kora-studio-v2-6-csp-guard-helper-cleanup.md) and [KORA Studio v2.6 goal report](kora-studio-v2-6-goal-report.md). Goal 525G keeps the CSP/resource helpers inside `tests/test_kora_studio_server.py` and consolidates repeated constants and parser helpers without changing runtime behavior.

Goal: Keep the CSP guard and fixture matrix maintainable without weakening assertions.

Scope:

- centralize expected Studio CSS and JavaScript asset paths
- centralize approved request JSON script shape
- centralize allowed Studio asset URLs
- centralize forbidden HTML resource prefixes
- centralize expected CSP directives and forbidden CSP sources
- centralize forbidden CSS/package asset tokens
- reuse helper parsing for positive guards and fixture matrix tests
- preserve all v2.4/v2.5 coverage

Acceptance criteria:

- helper cleanup stays inside the test module only
- positive guard coverage remains equivalent
- negative fixture matrix coverage remains equivalent
- no Studio runtime behavior changes
- no CSP broadening or asset allowlist broadening is introduced
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN is added
- full validation, optional browser smoke, and standard preview smoke pass

## Phase 31 — v2.7 CSP Guard Negative Coverage Review

Status: complete as targeted negative coverage additions. See [KORA Studio v2.7 CSP negative coverage review](kora-studio-v2-7-csp-negative-coverage-review.md) and [KORA Studio v2.7 goal report](kora-studio-v2-7-goal-report.md). Goal 526G reviews the v2.4-v2.6 CSP/resource guards and adds only relevant fixture cases for the current server-rendered Studio HTML model.

Goal: Add obvious missing negative cases without speculative test bloat or runtime changes.

Added coverage:

- mixed-case external resource schemes
- whitespace-padded external resource URLs
- `javascript:` pseudo URLs
- `srcset` external URL candidates
- `meta refresh` URL targets
- external form `action` targets
- inline event handler attributes
- inline `<style>` blocks

Declined scope:

- workers, frames, media, and font-specific cases until those resource classes are intentionally introduced
- browser-only assertions, because browser CSP validation remains optional and explicitly gated
- broader static asset fixtures, because existing allowlist and traversal tests already cover route behavior

Acceptance criteria:

- added fixtures remain dependency-light and browser-free
- added fixtures are relevant to HTML resource behavior
- approved request JSON exception remains explicit
- no Studio runtime behavior changes
- no CSP broadening or asset allowlist broadening is introduced
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN is added
- full validation, optional browser smoke, and standard preview smoke pass

## Current CSP Guard Summary

Current Studio CSP/static-asset guard documentation spans v2.1-v2.7:

- v2.1 adds the root-only local-preview CSP header
- v2.2 adds optional browser-level CSP smoke validation
- v2.3 keeps browser CSP smoke explicitly CI-optional with `KORA_STUDIO_BROWSER_CSP_SMOKE=1`
- v2.4 adds dependency-light positive regression guards for root HTML, CSP directives, package CSS, and package JavaScript
- v2.5 adds table-driven negative fixtures for rejected HTML, CSP, and CSS patterns
- v2.6 consolidates guard helpers inside `tests/test_kora_studio_server.py`
- v2.7 expands targeted negative HTML coverage for mixed-case/whitespace URLs, `javascript:`, `srcset`, `meta refresh`, form actions, inline event handlers, and inline `<style>` blocks

Current boundaries:

- package assets remain `/studio-assets/studio.css` and `/studio-assets/studio.js`
- root Studio HTML is the only route with the local-preview CSP header
- API, SSE, health, status, and asset routes are not given CSP headers by default
- default automated CSP/resource guard tests remain dependency-light and browser-free
- browser-level CSP smoke remains optional and explicitly gated
- these are local preview regression guards, not production security readiness claims

## Current CSP/Asset Maintenance Checklist

For future Studio HTML, CSS, JavaScript, CSP, or asset-route changes:

- update `tests/test_kora_studio_server.py` for any new resource attribute, CSS resource pattern, JavaScript asset behavior, CSP directive, or `/studio-assets/...` route
- preserve `/studio-assets/studio.css` and `/studio-assets/studio.js` as the only current package-controlled Studio assets unless a separate reviewed goal expands the allowlist
- keep executable JavaScript external through `/studio-assets/studio.js`; keep approved request JSON non-executable with `type="application/json"`
- update allowlist, rejection, MIME/cache, smoke, and docs coverage for any new asset route
- avoid `unsafe-inline`, `unsafe-eval`, wildcard sources, external hosts, CDN sources, `data:`, and `blob:` without explicit review
- avoid package manifests, lockfiles, frontend tooling, bundlers, npm workflows, Playwright config, external assets, or CDN dependencies as routine maintenance
- run standard validation, and run the optional browser CSP smoke when resource loading or CSP behavior changes

## Phase 32 — v3.0 Static Asset Guard Stability Review

Status: complete as static asset guard stability review. See [KORA Studio v3.0 static asset guard stability report](kora-studio-v3-0-static-asset-guard-stability-report.md) and [KORA Studio v3.0 goal report](kora-studio-v3-0-goal-report.md). Goal 529G reviews allowlist, MIME/cache, package-data, package source loading, route rejection, and filesystem static-serving risks.

Goal: Close obvious maintenance risks around the current Studio static asset guard without changing runtime behavior.

Added coverage:

- package-data config must include only `studio_assets/*.css` and `studio_assets/*.js`
- asset handler must not introduce filesystem-backed static serving helpers or directory-serving behavior

No-gap rationale:

- exact `studio.css` and `studio.js` allowlist coverage already exists
- unknown asset rejection already exists
- traversal and encoded traversal rejection already exists
- directory-style asset rejection already exists
- CSS/JS MIME and `Cache-Control: no-store` coverage already exists
- package-controlled source loading coverage already exists
- optional browser CSP smoke already covers live asset loading

Acceptance criteria:

- no runtime behavior changes
- no CSP broadening or asset allowlist broadening is introduced
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN is added
- full validation, optional browser smoke, and standard preview smoke pass

## Phase 33 — v3.1 UX/Feature Readiness Review

Status: complete as a review-only UX and feature readiness assessment. See [KORA Studio v3.1 UX/feature readiness review](kora-studio-v3-1-ux-feature-readiness-review.md). Goal 530G reviews the current local preview operator workflow without changing runtime behavior.

Review coverage:

- Run Local Harness workflow
- approved request selector
- browser-local run history
- selected-run summary
- timeline/event visibility
- generated event stream status and fallback behavior
- selected-run comparison and report metadata
- error, empty, and retry states
- details drawer and compact model selector boundaries
- local-only boundary strip
- narrow/mobile and accessibility basics
- claim boundaries for what Studio cannot claim or do

Findings summary:

- no blocker was found for the current local demo/preview scope
- important follow-up work should simplify the primary operator path, make SSE/timeline states easier to scan, review drawer utility, refresh responsive visual QA, and run a focused accessibility interaction review
- cosmetic issues are mostly text density, repeated boundary copy, and legacy compatibility page length

Acceptance criteria:

- documentation-only review
- no Studio runtime behavior changes
- no CSP broadening or asset allowlist broadening is introduced
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN is added
- claim boundaries remain local preview/demo only

## Phase 34 — v3.2 Primary Operator Path Simplification Plan

Status: complete as a planning-only operator path simplification review. See [KORA Studio v3.2 primary operator path simplification plan](kora-studio-v3-2-primary-operator-path-simplification-plan.md). Goal 531G reviews the first-time local demo journey without implementing UI changes.

Review coverage:

- opening Studio
- understanding local-only boundaries
- selecting an approved request
- running Local Harness
- understanding run progress
- reading a result summary
- inspecting timeline/details if needed
- retrying the last approved request if needed

Findings summary:

- no blocker was found for the current local demo/preview scope
- important friction comes from a diffuse primary action path, repeated boundary copy, multiple status surfaces, and diagnostics competing with the result summary
- cosmetic friction comes from heavy labels, repeated panel copy, and legacy compatibility page length

Prioritized implementation candidates:

- primary workflow band implementation
- result summary before diagnostics
- run progress and SSE state simplification
- retry placement and error state polish
- diagnostic surface rebalancing
- responsive and accessibility check after simplification

Acceptance criteria:

- planning/review only
- no Studio runtime behavior changes
- no CSP broadening or asset allowlist broadening is introduced
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN is added
- claim boundaries remain local preview/demo only

## Phase 35 — v3.3 Primary Workflow Band

Status: complete as a bounded UX-only frontend shell improvement. See [KORA Studio v3.3 primary workflow band report](kora-studio-v3-3-primary-workflow-band-report.md) and [KORA Studio v3.3 goal report](kora-studio-v3-3-goal-report.md). Goal 532G implements the first v3.2 simplification candidate by adding a concise primary workflow band near the top of the final Studio shell.

Implemented behavior:

- shell-level primary workflow band
- sequence copy for selecting an approved request, running Local Harness, reviewing the result summary, and inspecting timeline/details
- compact local preview boundary copy
- package CSS styling for the band
- dependency-light server and smoke marker coverage

Preserved boundaries:

- no backend route or API change
- no model execution, provider calls, downloads, cloud sync, report export, or file writing
- no CSP broadening or asset allowlist broadening
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN

Next recommended implementation:

- add or promote selected-run result summary before deep diagnostics

## Phase 36 — v3.4 Result Summary Before Diagnostics

Status: complete as a bounded UX-only frontend shell improvement. See [KORA Studio v3.4 result summary before diagnostics report](kora-studio-v3-4-result-summary-before-diagnostics-report.md) and [KORA Studio v3.4 goal report](kora-studio-v3-4-goal-report.md). Goal 533G implements the second v3.2 simplification candidate by adding a primary result summary before lower-level diagnostics.

Implemented behavior:

- shell-level primary result summary before diagnostics
- request/run identity, status, event count, key counters, comparison status, and report metadata status
- generated local harness output boundary copy
- package CSS styling for the summary
- browser-local JavaScript state updates using the existing local harness run response
- dependency-light server and smoke marker coverage

Preserved boundaries:

- no backend route or API change
- no diagnostic information removed
- no model execution, provider calls, downloads, cloud sync, report export, or file writing
- no CSP broadening or asset allowlist broadening
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN

Next recommended implementation:

- simplify run progress and generated event stream states while preserving generated-harness-only boundaries

## Phase 37 — v3.5 Run Progress and SSE State Simplification

Status: complete as a bounded UX-only frontend shell improvement. See [KORA Studio v3.5 run progress and SSE state simplification report](kora-studio-v3-5-run-progress-sse-state-simplification-report.md) and [KORA Studio v3.5 goal report](kora-studio-v3-5-goal-report.md). Goal 534G implements the third v3.2 simplification candidate by adding a concise run progress and generated event stream summary before result and diagnostic surfaces.

Implemented behavior:

- shell-level run progress summary before result summary
- idle/running/generated-events/completed/failed state copy
- generated event stream connection status in plain language
- package CSS styling for the summary
- browser-local JavaScript state updates using existing local harness and SSE state
- dependency-light server and smoke marker coverage

Preserved boundaries:

- no backend route or API change
- no diagnostic information removed
- no model execution, provider calls, downloads, cloud sync, report export, or file writing
- no CSP broadening or asset allowlist broadening
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN

Next recommended implementation:

- move or mirror Retry Last Approved Request closer to failed status and last-run context

## Phase 38 — v3.6 Retry and Error State Polish

Status: complete as a bounded UX-only frontend shell improvement. See [KORA Studio v3.6 retry and error state polish report](kora-studio-v3-6-retry-error-state-polish-report.md) and [KORA Studio v3.6 goal report](kora-studio-v3-6-goal-report.md). Goal 535G implements the fourth v3.2 simplification candidate by adding shell-level retry guidance and a safe retry action near run progress/error context.

Implemented behavior:

- shell-level Safe next action guidance
- shell-level Retry Last Approved Request button
- shared retry enable/disable handling for shell and diagnostic retry controls
- last-approved-request-only retry boundary copy
- package CSS styling for shell retry placement
- dependency-light server and smoke marker coverage

Preserved boundaries:

- no backend route or API change
- no diagnostic information removed
- no model execution, provider calls, downloads, cloud sync, report export, or file writing
- no CSP broadening or asset allowlist broadening
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN

Next recommended implementation:

- rebalance diagnostic surfaces across primary shell, details drawer, and collapsed legacy compatibility preview

## Phase 39 — v3.7 Diagnostic Surface Rebalancing

Status: complete as a bounded UX-only frontend shell improvement. See [KORA Studio v3.7 diagnostic surface rebalancing report](kora-studio-v3-7-diagnostic-surface-rebalancing-report.md) and [KORA Studio v3.7 goal report](kora-studio-v3-7-goal-report.md). Goal 536G rebalances diagnostic surfaces so primary workflow, run progress, safe next action, and result summary remain visually primary while lower diagnostics stay available.

Implemented behavior:

- secondary hierarchy markers for selected-run diagnostics
- secondary hierarchy markers for lower retry/error panels
- secondary hierarchy markers for browser-local run history
- package CSS styling for secondary diagnostic cards
- dependency-light server and smoke marker coverage

Preserved boundaries:

- no backend route or API change
- no diagnostic information removed
- no model execution, provider calls, downloads, cloud sync, report export, or file writing
- no CSP broadening or asset allowlist broadening
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN

Next recommended implementation:

- validate simplified primary path responsive behavior and accessibility basics

## Phase 40 — v3.8 Responsive and Accessibility Check

Status: complete as a bounded UX/accessibility review and small frontend-shell improvement. See [KORA Studio v3.8 responsive and accessibility check report](kora-studio-v3-8-responsive-accessibility-check-report.md) and [KORA Studio v3.8 goal report](kora-studio-v3-8-goal-report.md). Goal 537G reviews the primary operator path for narrow/mobile behavior and basic accessibility signals.

Implemented behavior:

- primary path responsive/accessibility markers
- list semantics for the primary workflow band
- explicit descriptive relationships for Run Local Harness and Retry Last Approved Request controls
- atomic polite live-region markers for run progress and primary result summary
- 520px single-column fallback for primary status grids
- dependency-light server and smoke marker coverage

Preserved boundaries:

- no backend route or API change
- no harness behavior change
- no model execution, provider calls, downloads, cloud sync, report export, or file writing
- no CSP broadening or asset allowlist broadening
- no dependency, frontend tooling, package manifest, lockfile, Playwright config, bundler, npm workflow, external asset, or CDN
- no production accessibility certification claim

Next recommended implementation:

- run a focused keyboard and screen-reader interaction spot check for the primary path, drawer, and approved request selector

## Phase 41 — v3.9 Keyboard and Screen-Reader Spot Check

Status: complete as a bounded keyboard/screen-reader spot check and small frontend-shell improvement. See [KORA Studio v3.9 keyboard and screen-reader spot check report](kora-studio-v3-9-keyboard-screen-reader-spot-check-report.md) and [KORA Studio v3.9 goal report](kora-studio-v3-9-goal-report.md). Goal 538G reviews primary keyboard controls, selected request state, and overlay drawer/rail semantics.

Implemented behavior:

- closed details drawer starts inert
- details drawer open/close JavaScript toggles inert with `aria-hidden`
- closed mobile left rail JavaScript toggles inert with `aria-hidden`
- approved request selector buttons expose `aria-current`
- selected request JavaScript keeps `aria-pressed` and `aria-current` in sync
- dependency-light server and smoke marker coverage

Preserved boundaries:

- no backend route or API change
- no harness behavior change
- no model execution, provider calls, downloads, cloud sync, report export, or file writing
- no CSP broadening or asset allowlist broadening
- no dependency, axe tooling, browser framework config, package manifest, lockfile, frontend build tooling, external asset, or CDN
- no production accessibility certification claim

Next recommended implementation:

- run a manual browser keyboard traversal report for Tab, Enter, Space, and Escape behavior across the primary path and overlays

| Title | Phase | Target files | Difficulty | Contributor suitability | Claim risk |
|---|---:|---|---|---|---|
| Add KORA Studio fixture plan | 0 | `docs/kora-studio/fixtures-plan.md` | small | good first docs issue | low |
| Add report viewer requirements | 0 | `docs/kora-studio/report-viewer-requirements.md` | small | good first docs issue | low |
| Add dashboard counter schema | 0 | `docs/kora-studio/dashboard-counter-schema.md` | small | good first docs issue | medium if counters are overinterpreted |
| Add `kora studio` CLI help stub | 1 | `kora/cli.py`, CLI tests | small | Python contributor | medium if wording implies shipped Studio |
| Add local Studio server design skeleton | 2 | future server module, tests | medium | Python contributor | low if no external calls |
| Add static welcome/setup page mock | 3 | future static UI files or docs mock | small | frontend/docs contributor | low |
| Add KORA Boost mode card mock | 3 | future static UI files or docs mock | small | frontend/docs contributor | medium if copy overclaims |
| Add report viewer static mock | 4 | future static UI files or docs mock | medium | frontend contributor | medium if reports expose raw data |
| Add counter dashboard fixture | 5 | future fixture path, tests | small | good first data/docs issue | medium if cost/energy fields are added |
| Add Ollama detection design note | 7 | future runtime design doc | small | local-runtime contributor | medium if support is implied before code |

## Claim-Safety Rules

- do not claim KORA Studio exists until code exists
- do not claim KORA Studio is an LM Studio replacement
- do not frame KORA Studio as merely a local chatbot
- do not claim production cost reduction
- do not claim real API-cost reduction
- do not claim energy reduction
- do not claim larger models physically run unless validated
- do not claim KORA removes RAM, VRAM, unified-memory, or model-loading requirements
- do not claim all open-source LLMs are supported
- keep provider/cloud/distributed execution disabled by default unless explicitly enabled
- use "Less waiting. Better answers. No hardware upgrade." as product benefit copy
- use technical explanation after benefit copy

## Implementation Order Recommendation

1. fixtures and schemas
2. CLI stub
3. local server skeleton
4. static UI
5. report viewer
6. counter dashboard
7. runtime detection
8. local chat
