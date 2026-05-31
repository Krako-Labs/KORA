# KORA Studio v1.1 Shell-only Preview Hardening Plan

## Status And Goal

KORA Studio v1.1 should harden the shell-only local preview experience so the final minimal shell and right drawer carry the normal first-run preview flow without requiring the collapsed legacy detailed preview.

v1.1 remains a local preview/demo readiness milestone, not production readiness.

The goal is to reduce the legacy detailed preview from compatibility scaffolding toward a developer-only reference surface while preserving all local-only and claim-safe boundaries.

## Current v1.0 State

v1.0 completed shell-first preview readiness:

- final minimal shell is the primary local preview surface
- compact model selector remains catalog-estimate-only
- composer remains approved-harness-only
- shell boundary strip exposes local-only disabled states
- selected-run timeline, counters, comparison, and report metadata state are visible in shell/drawer surfaces
- right drawer acts as the main diagnostics surface
- legacy detailed preview is collapsed by default and labelled as compatibility/developer scaffolding
- v1.0 shell-first smoke checks cover the readiness markers

## Shell-only Preview Target

The v1.1 target is:

- the shell and drawer are sufficient for normal local preview inspection
- the user can understand local-only status, selected model boundary, approved harness run state, route/counter/comparison/report metadata, and claim boundaries without opening the legacy compatibility scaffold
- legacy detailed preview content is only retained for compatibility or developer reference until it can be removed safely
- smoke checks prove that shell/drawer surfaces carry the critical preview information

## Scope

Allowed:

- local preview HTML, CSS, and minimal vanilla JavaScript only
- shell/drawer information architecture hardening
- additional smoke-checkable shell/drawer markers
- reducing repeated dense legacy content prominence
- keeping legacy preview collapsed and secondary
- public-safe docs and reports

Forbidden:

- arbitrary prompt input
- real model execution
- provider calls
- model downloads
- cloud sync
- private model directory scanning
- runtime model list commands
- report file export
- report file writing
- external network behavior
- new frontend dependency installation without explicit approval
- production readiness claim
- production cost reduction claim
- energy outcome claim
- unsupported larger-model execution claim
- LM Studio replacement claim

## Legacy Preview Reduction Strategy

v1.1 should treat the legacy detailed preview as a compatibility/developer scaffold only.

Required legacy behavior:

- collapsed by default
- clearly secondary to the shell and drawer
- not rendered as the primary `<main>` surface
- not required for first-run understanding
- does not introduce enabled model, provider, download, cloud, or report export behavior

Candidate hardening actions:

- strengthen compatibility labels and smoke markers
- move any remaining essential first-run wording into shell/drawer surfaces
- reduce duplicated dense legacy explanations where shell/drawer coverage is complete
- keep a safe reference path for tests and contributors while removal is planned

## Drawer-first Diagnostics Behavior

The right drawer should be the primary diagnostics surface for:

- runtime status
- selected catalog estimate boundary
- catalog vs installed distinction
- selected-run route trace
- selected-run event timeline status
- selected-run generated counters status
- Standard Mode vs KORA Boost local harness comparison status
- report metadata preview status
- claim boundaries

The drawer should remain local-only and should not become a provider, runtime, model execution, model download, or report export control panel.

## Shell-visible Local-only Boundaries

The shell should keep visible compact boundaries for:

- local preview/demo status
- approved local harness requests only
- generated local harness output only
- provider calls disabled
- cloud sync disabled
- downloads disabled
- model execution not connected
- report export/write disabled
- not production telemetry
- not production cost evidence

## Shell-visible Selected-run State

The shell should continue to show selected-run state without depending on the legacy preview:

- selected request/run summary
- run status
- event timeline availability
- generated counters availability
- local harness comparison availability
- report metadata preview availability
- model-needed boundary as `execution_not_connected`
- claim boundary

The selected-run state remains browser-local page memory only unless a later milestone explicitly adds persistence.

## Shell Smoke Markers

v1.1 smoke checks should cover:

- shell-only hardening marker
- shell-first readiness marker remains present
- shell local-only boundary coverage
- drawer diagnostics coverage
- selected-run shell/drawer coverage
- legacy preview compatibility mode remains collapsed
- legacy preview is not the primary `<main>` surface
- no arbitrary prompt input
- no enabled model run/download action
- no provider/cloud/report export behavior

## Test Plan

Validation should include:

- `git diff --check`
- `python3 -m pytest`
- `python3 -m pytest tests -k "studio or sse or execution or harness"`
- live local smoke check with `python3 -m kora studio --no-browser`
- `python3 scripts/check_kora_studio_preview.py`

Tests and smoke checks must not:

- open a real browser from unit tests
- call providers
- call external model APIs
- download models
- execute models
- scan private directories
- run runtime model list commands
- write report files
- require external network behavior

## Acceptance Criteria

v1.1 is ready when:

- shell/drawer surfaces cover the core local preview information without requiring the legacy preview
- legacy preview remains collapsed and clearly secondary
- shell-only smoke markers are present and tested
- selected-run details remain visible through shell/drawer surfaces
- model selector remains catalog-estimate-only
- composer remains approved-harness-only
- provider/model/download/cloud/report export boundaries remain disabled
- validation and live smoke checks pass

## v1.1 Task Breakdown

### Task 480: v1.1 shell-only hardening plan

Create this plan and link it from Studio docs.

### Task 481: shell-only diagnostics coverage map

Document which current legacy diagnostics are already covered by the shell/drawer and which remaining pieces need shell/drawer destinations before legacy removal.

Status: implemented. See [KORA Studio v1.1 shell diagnostics coverage map](kora-studio-v1-1-shell-diagnostics-coverage-map.md).

### Task 482: legacy preview secondary/collapsed tightening

Tighten the compatibility/developer scaffold state and smoke markers without removing safe reference coverage.

### Task 483: shell selected-run drawer polish

Polish selected-run shell/drawer status so timeline, counters, comparison, and report metadata are clear without opening the legacy preview.

### Task 484: shell-only smoke check expansion

Expand smoke checks for v1.1 shell-only hardening markers and legacy-secondary guarantees.

### Task 485: v1.1 readiness report

Run validation and live local smoke check, then add a public-safe readiness report.

### Task 486: consolidated v1.1 goal report

Add a consolidated goal report covering Tasks 480-486, commits, files changed, validations, smoke check results, boundaries, known limitations, and next recommended goal.

## Next Recommended Direction After v1.1

If v1.1 validates the shell/drawer as sufficient, the next goal can focus on local frontend extraction/componentization or safely removing the remaining legacy compatibility scaffold.
