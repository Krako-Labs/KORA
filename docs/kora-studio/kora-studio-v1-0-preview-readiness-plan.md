# KORA Studio v1.0 Preview Readiness Plan

## Status And Goal

KORA Studio v1.0 should make the minimal final shell the primary local preview experience and reduce dependence on the legacy detailed preview below it.

The goal is preview readiness, not production readiness:

- keep the sparse ChatGPT-style workspace as the default surface
- keep model selection compact and catalog-estimate-only
- keep advanced routing, runtime, counter, report, and claim details in the right drawer
- migrate critical local-only information out of the legacy preview into the shell or drawer
- keep the legacy preview only as compatibility scaffolding until it can be safely removed
- preserve all local-only claim boundaries

v1.0 remains a local preview/demo readiness milestone.

## v0.9 Complete State

v0.9 completed local usability polish:

- right details drawer open/close controls
- mobile left rail open/close controls
- Escape close behavior for shell overlays
- focus-visible styling and keyboard/focus markers
- catalog-only model selector selected state
- approved local harness request controls
- browser-local selected-run state, history, retry, generated events, generated counters, comparison, and report metadata
- mobile visual QA checklist and smoke markers

The detailed legacy preview still remains below the final shell for compatibility.

## v1.0 Objective

v1.0 should move the local preview from "final shell above legacy preview" to "final shell as the main local preview."

The work should make the shell sufficient for first-run local inspection:

- local-only status
- selected catalog estimate boundary
- approved request trigger state
- selected-run timeline, counters, comparison, and report metadata
- runtime/catalog/installed-model distinction
- no-provider/no-cloud/no-download/no-model-execution boundaries
- right drawer as the primary place for detailed diagnostics

The legacy detailed preview should be reduced, hidden behind a compatibility/developer affordance, or made clearly secondary.

## Scope

Allowed:

- embedded HTML, CSS, and minimal vanilla JavaScript only
- shell-first information architecture changes
- moving local-only status and boundary copy into the shell or drawer
- moving selected-run timeline, counters, comparison, and report metadata into shell/drawer surfaces
- reducing legacy preview prominence
- compatibility markers while legacy preview still exists
- smoke-check markers for shell-first readiness
- public-safe readiness and goal reports

Forbidden:

- arbitrary prompt execution
- real model execution
- provider calls
- model downloads
- cloud sync
- private model directory scanning
- runtime model list commands
- report file export
- report file writing
- remote registry or catalog fetching
- new dependency installation without explicit approval
- production cost reduction claim
- energy outcome claim
- unsupported larger-model execution claim
- LM Studio replacement claim

## Required Preview Surfaces

### Shell-First Launch View

The default root page should prioritize:

- left mini rail for workspace/task navigation only
- compact top model selector
- centered composer
- local preview status pills
- selected-run summary
- right drawer for advanced details

The user should not need to scroll to the legacy preview to understand the local preview boundary.

### Top Selector Boundary

The compact model selector should keep showing:

- static local catalog estimates only
- catalog examples are not installed models
- selecting an estimate does not install, download, or execute a model
- model recommendations are estimates until validated

### Composer Boundary

The composer should remain an approved local harness surface:

- no arbitrary prompt execution
- approved deterministic sample requests only
- generated local harness output only
- model-needed boundaries return `execution_not_connected`

### Right Drawer Details

The right drawer should be the primary home for:

- runtime status
- selected catalog estimate boundary
- catalog vs installed summary
- route trace
- generated counters
- local harness comparison
- report metadata preview
- claim boundaries

### Legacy Preview Reduction

The legacy detailed preview should move toward one of these states:

- collapsed compatibility section
- developer-only preview section
- clear "legacy detail scaffold" label
- removed after all required information is represented in the shell and drawer

Any reduction must preserve tests, smoke markers, and public-safe claim boundaries.

## Claim Boundary UI

Every shell-first surface must preserve these boundaries:

- local preview/demo readiness only
- approved local harness requests only
- generated local harness events only
- no arbitrary prompt execution
- no real model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export
- no report file writing
- not production telemetry
- not production cost evidence
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement

## Acceptance Criteria

- the final shell is the primary local preview surface
- a first-run user can understand local-only status without relying on the legacy preview
- selected-run timeline, counters, comparison, and report metadata are accessible from the shell or drawer
- legacy preview dependence is reduced or clearly marked as compatibility scaffolding
- model selector remains catalog-estimate-only
- composer remains approved-harness-only
- all provider/model/download/cloud/report export boundaries remain disabled
- smoke check covers shell-first v1.0 markers
- tests pass without browser automation, provider calls, model execution, downloads, or external services

## Test Plan

Validation should cover:

- shell-first readiness marker
- legacy preview compatibility/reduction marker
- local-only status visible in shell
- compact model selector boundary
- composer approved-harness-only boundary
- right drawer carries route, counters, comparison, report, and claim detail markers
- selected-run timeline/counters/comparison/report metadata remain available
- no arbitrary prompt input
- no enabled model run or model download action
- no provider/cloud/report export behavior
- `/health`, `/status`, `/`, run, run retrieval, events, and SSE smoke checks still pass

Tests must not:

- open a real browser from unit tests
- call providers
- call external model APIs
- download models
- execute models
- scan private directories
- run runtime model list commands
- write report files

## v1.0 Task Breakdown

### Task 472: v1.0 preview readiness plan

Create this plan and link it from Studio docs.

### Task 473: shell-first information architecture map

Document and/or mark which legacy preview content must move into the shell, right drawer, or compatibility section before legacy dependence can be reduced.

Status: implemented. See [KORA Studio v1.0 shell-first information architecture](kora-studio-v1-0-shell-first-information-architecture.md).

### Task 474: shell local-only status and boundary consolidation

Move or duplicate critical launch, local-only, provider/cloud-disabled, model-download-disabled, and model-execution-disabled status into shell-first surfaces.

Status: implemented. The final shell now exposes v1.0 shell-first boundary markers and a compact local-only boundary strip covering provider calls, cloud sync, downloads, model execution, and report export/write status without relying on the legacy preview.

### Task 475: shell and drawer selected-run surface consolidation

Ensure selected-run timeline, counters, comparison, and report metadata are visible through shell/drawer surfaces without requiring the legacy preview.

Status: implemented. The shell now exposes a v1.0 selected-run detail strip for timeline, counters, comparison, and report metadata state, and the right drawer mirrors selected-run surface status while preserving local harness, no-model, no-provider, no-download, no-cloud, and no-report-export boundaries.

### Task 476: legacy preview compatibility reduction

Collapse, relabel, or otherwise reduce the legacy detailed preview while preserving safe fallback access and smoke-test coverage.

Status: implemented. The legacy detailed preview is now a collapsed compatibility/developer scaffold by default, while the final shell remains the primary local preview surface. Existing legacy detail markers remain available for compatibility and smoke coverage.

### Task 477: v1.0 shell-first smoke check

Update smoke checks and tests for v1.0 shell-first readiness markers, legacy compatibility markers, and claim boundaries.

Status: implemented. The local preview smoke check now has a dedicated v1.0 shell-first check result covering shell readiness markers, shell boundary coverage, selected-run shell/drawer coverage, collapsed legacy compatibility mode, and the absence of legacy preview as the primary main surface.

### Task 478: v1.0 readiness report

Run validation and live local smoke check, then add a public-safe readiness report.

### Task 479: consolidated v1.0 goal report

Add a consolidated goal report covering Tasks 472-479, commits, files changed, validations, smoke check results, boundaries, known limitations, and next recommended goal.

## Validation Expectations

After implementation tasks:

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

## v1.0 Readiness Criteria

v1.0 is ready when:

- the final minimal shell can stand as the primary preview experience
- the legacy preview is no longer required for first-run understanding
- compatibility scaffolding remains claim-safe if it still exists
- all local-only boundaries remain visible
- full tests and live local preview smoke checks pass

## Recommended Next Goal

After v1.0, the next likely goal is KORA Studio v1.1 shell-only preview hardening or local frontend extraction/componentization, depending on whether the embedded static server remains sufficient.
