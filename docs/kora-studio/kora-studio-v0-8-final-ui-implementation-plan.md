# KORA Studio v0.8 Final UI Implementation Plan

## Status and Goal

KORA Studio v0.8 should implement the final v0.7 UI/UX board into the local Studio preview while preserving all existing local deterministic harness behavior and claim boundaries.

The target is a minimal chat-like local workspace:

- small left mini rail for workspace/task navigation
- top model selector
- centered composer as the default surface
- compact boundary pills
- hidden right details drawer for advanced/runtime/harness/report information
- mobile overlay behavior for left rail and right drawer

The source of truth is:

- [KORA Studio final UI/UX board](design/v0-7-reference/kora-studio-final-uiux-board.png)
- [KORA Studio v0.7 external design source of truth](kora-studio-v0-7-design-source-of-truth.md)

v0.8 is an implementation milestone for the local preview UI. It remains a local preview/demo readiness milestone, not a production release.

## Current Baseline

The current local preview already includes:

- `python3 -m kora studio`
- localhost-only server
- `/health`
- `/status`
- `/`
- `POST /api/harness/run`
- `GET /api/harness/run/<run_id>`
- `GET /api/harness/events?run_id=<id>`
- `GET /api/harness/sse?run_id=<id>`
- approved request selector
- Run Local Harness button for approved request IDs only
- selected-run summary
- selected-run generated event timeline
- selected-run counters
- selected-run Standard Mode vs KORA Boost comparison
- selected-run report metadata preview
- generated event stream display
- browser-local run history
- retry last approved request
- clear browser-local run history

v0.8 must preserve this behavior while changing the default information architecture.

## Scope

Allowed:

- update the local preview HTML/CSS/vanilla JavaScript in `kora/studio_server.py`
- add helper functions if needed to keep rendering manageable
- add a left mini rail with static local workspace/task labels
- add a compact top model selector scaffold
- keep selected model state local and claim-safe
- move dense runtime, catalog, route, counter, report, and claim information into a hidden right details drawer
- keep Run Local Harness behavior limited to approved request IDs
- keep selected-run state and history in browser page memory only
- improve responsive layout with no new dependencies
- update tests and smoke check markers
- update docs and readiness/goal reports

Forbidden:

- arbitrary request text execution
- real model execution
- provider calls
- model downloads
- cloud sync
- private model directory scanning
- runtime model list commands
- external network behavior
- new frontend framework or package installation without explicit approval
- report file export
- report file writing
- production cost reduction claim
- energy outcome claim
- unsupported larger-model execution claim
- LM Studio replacement claim

## Required Default Layout

The first screen should show:

- left mini rail
- top model selector
- centered headline
- centered composer
- compact local boundary pills
- details button for the right drawer

The first screen should not show:

- dense system profile cards
- full model catalog table
- route trace
- generated counters
- report metadata tables
- setup guidance wall of text
- always-visible harness internals

## Left Mini Rail

The left mini rail should be a quiet workspace/task aid, not a diagnostics dashboard.

Allowed rail content:

- `KORA Studio`
- `New task`
- `Search tasks`
- lightweight project/task labels
- `Local workspace`
- `Cloud sync disabled`

Forbidden rail content:

- runtime diagnostics
- route trace
- generated counters
- report metadata
- model installation controls
- provider controls
- cloud controls

Behavior:

- visible on desktop
- collapsible or overlayed on constrained widths
- no persistence required in v0.8
- no cloud sync
- no file scanning

## Top Model Selector

The model selector should remain compact and centered in the top bar.

Required behavior:

- shows `Search or select open-source LLM`
- can display local catalog candidate rows
- selected model label is compact
- model selection does not install a model
- model selection does not execute a model
- catalog examples are not installed models
- estimated runnable is not execution readiness

Implementation may remain scaffolded if full interaction would broaden the task. The claim boundary must be visible.

## Center Composer

The composer remains the main product surface.

Required copy:

- headline: `What do you want to work on?`
- supporting copy: `Choose a local model once. KORA keeps routing details out of the way.`
- placeholder: `Ask KORA...`

The composer may continue to trigger only approved local harness behavior until arbitrary request text execution is explicitly scoped. It must not accept or execute arbitrary workflow guides as a real model/provider path.

## Right Details Drawer

The right drawer should be hidden by default and opened by a details control.

Drawer sections:

- Runtime status
- Selected model
- Catalog vs installed
- Route trace
- Generated counters
- Report metadata
- Claim boundaries

The drawer may use simple disclosure sections. It should contain the dense information currently shown directly in the page.

## Local Harness Interaction

Existing local harness behavior must remain connected:

- approved request selector
- Run Local Harness for approved request IDs only
- selected-run summary
- selected-run event timeline
- selected-run counters
- selected-run Standard Mode vs KORA Boost comparison
- selected-run report metadata preview
- generated event stream display
- retry last approved request
- browser-local run history

Placement target:

- primary action and selected-run summary near the composer
- detailed timeline/counters/comparison/report metadata in the right drawer
- history can remain in the left rail or a compact local history section, but must remain page-memory only

## Mobile and Responsive Behavior

Mobile behavior should follow the final board:

- composer is the default state
- left rail opens as an overlay or constrained side panel
- right details drawer opens as an overlay
- top model selector remains compact
- boundary pills wrap without overlapping
- no dense mobile dashboard

## Claim Boundary UI

The UI must continue to show:

- `Local preview`
- `Provider calls disabled`
- `Model execution not connected yet`
- `Cloud sync disabled`
- `No downloads`
- `Catalog examples are not installed models`
- `Generated harness events only`

Every interactive selected-run result must preserve:

- no model execution
- no provider calls
- no downloads
- no cloud sync
- model-needed boundary returns `execution_not_connected`
- report metadata preview only
- no production evidence claim

## Test Plan

Update or add tests for:

- preview HTML includes left mini rail
- preview HTML includes top model selector
- preview HTML includes centered composer copy
- preview HTML includes right details drawer container
- dense runtime/harness/report content is not the default first-screen structure
- drawer includes runtime, catalog, route, counters, report, and claim sections
- approved request selector still exists
- Run Local Harness still calls only `POST /api/harness/run`
- selected-run event fetch still uses `GET /api/harness/events?run_id=<id>`
- optional generated event stream still uses `GET /api/harness/sse?run_id=<id>`
- no arbitrary request text execution endpoint is introduced
- no external script source is introduced
- no provider/model/download/cloud endpoints are introduced
- no report export/download endpoint is introduced
- preview smoke check still passes

Tests must not:

- open a real browser
- call external network
- call providers
- call Ollama API
- require Ollama installed
- download models
- execute a model
- scan private directories
- list runtime models
- write report files

## v0.8 Task Breakdown

### Task 456: v0.8 final UI implementation plan

Create this implementation plan and link it from Studio docs.

### Task 457: chat-like shell layout scaffold

Rework the local preview shell around:

- left mini rail
- top model selector
- centered composer
- details drawer container

Keep existing harness functionality reachable and keep all existing endpoints intact.

Status: implemented as the first v0.8 code step. The preview now includes the shell scaffold above the existing detailed local preview. Dense information migration remains Task 458.

### Task 458: Right details drawer migration

Move dense runtime, catalog, setup guidance, route, counters, comparison, report, and claim sections into the right drawer.

Default page should remain sparse.

Status: implemented. The right details drawer now contains runtime status, selected model boundary, catalog vs installed summary, route trace, generated counters, report metadata, and claim boundary sections. Existing detailed local preview content remains below the shell for compatibility while the default workspace stays sparse.

### Task 459: Compact model selector scaffold

Render the model selector from existing local catalog recommendation data.

Preserve catalog vs installed vs estimated runnable vs execution-connected boundaries.

Status: implemented. The compact top selector is now a local catalog scaffold that shows the suggested estimate and available static catalog options without installing, downloading, executing, or claiming the examples are installed models.

### Task 460: Composer and approved harness action alignment

Align the existing approved local harness trigger with the new composer surface.

Do not add arbitrary request text execution.

Status: implemented. The centered composer action now reuses the approved local harness request path and updates a compact composer selected-run summary. It sends only the selected approved request ID to the existing local harness endpoint and does not add arbitrary request text execution, model execution, provider calls, downloads, or cloud sync.

### Task 461: Responsive/mobile layout pass

Implement mobile behavior for:

- left rail overlay/collapse
- right drawer overlay
- compact top model selector
- wrapped boundary pills
- centered composer

Status: implemented. The local preview now includes mobile-ready markers and CSS for a collapsed left rail overlay, compact top selector overlay menu, wrapped boundary pills, centered composer scaling, and right details drawer overlay behavior. This remains a local preview scaffold and does not add provider calls, model execution, downloads, cloud sync, or new frontend dependencies.

### Task 462: v0.8 smoke check and readiness report

Run validation and live local smoke check. Add a v0.8 readiness report.

Status: implemented in [KORA Studio v0.8 readiness report](kora-studio-v0-8-readiness-report.md). Full pytest, Studio-focused pytest, live local smoke check, live UI marker check, and browser snapshot review passed for the v0.8 local preview.

### Task 463: consolidated v0.8 goal report

Create a consolidated goal report covering Tasks 456-463, commits, changed files, validations, claim boundaries, known limitations, and next recommended goal.

Status: implemented in [KORA Studio v0.8 goal report](kora-studio-v0-8-goal-report.md).

## Validation Expectations

After each implementation task:

```bash
git diff --check
python3 -m pytest tests/test_kora_studio_server.py
python3 -m pytest tests/test_kora_studio_preview_smoke.py
python3 -m pytest tests -k "studio or sse or execution or harness"
```

For readiness:

```bash
python3 -m pytest
python3 -m kora studio --no-browser
python3 scripts/check_kora_studio_preview.py
```

The live smoke check requires an already-running local preview server and must remain localhost-only.

## Acceptance Criteria

v0.8 is complete when:

- the local preview visually follows the final UI/UX board structure
- default screen is sparse and composer-centered
- left mini rail exists and remains workspace/task-only
- top model selector exists with claim-safe model boundaries
- right details drawer contains advanced runtime/harness/report details
- existing local harness run behavior still works
- selected-run state/history remain browser-local only
- provider/model/download/cloud/report export behavior remains disabled
- tests and smoke checks pass
- v0.8 readiness and consolidated goal reports are added

## Next Recommended Goal After v0.8

KORA Studio v0.9 should focus on local usability polish after the final layout is implemented:

- keyboard/focus accessibility pass
- visual QA screenshots from local preview
- read-only selected-run refresh by run ID
- clearer model picker search behavior
- no arbitrary request text execution unless separately scoped
- no model execution/provider/download/cloud behavior
