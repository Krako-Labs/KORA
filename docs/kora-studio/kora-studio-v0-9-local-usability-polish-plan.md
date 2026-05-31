# KORA Studio v0.9 Local Usability Polish Plan

## Status And Goal

KORA Studio v0.9 should polish the v0.8 final UI shell into a more usable local preview without changing the product boundary.

The goal is to make the local preview easier to inspect and operate:

- keyboard and focus accessibility
- explicit right drawer open/close interaction
- explicit left rail open/close interaction
- model selector focus and selection states
- stronger mobile visual QA
- reduced dependence on the legacy detailed preview

v0.9 remains a local preview/demo milestone, not a production release.

## Current v0.8 State

v0.8 implemented:

- sparse default workspace shell
- left mini rail
- compact top model selector from local static catalog estimates
- centered composer as primary surface
- approved local harness composer action
- compact selected-run summary
- right details drawer destination
- responsive/mobile shell markers
- v0.8 readiness report
- v0.8 consolidated goal report

The detailed legacy preview still remains below the shell for compatibility.

## Scope

Allowed:

- vanilla JavaScript only
- no new frontend dependency
- drawer open/close state in browser memory
- left rail open/close state in browser memory
- keyboard focus states and ARIA attributes
- Escape key close behavior
- tab order improvements
- model selector selected-state polish using existing local catalog data
- mobile visual QA notes and smoke check markers
- moving more user-facing local preview content from legacy area into shell/drawer surfaces

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
- remote registry/catalog fetching
- production cost reduction claim
- energy outcome claim
- unsupported larger-model execution claim
- LM Studio replacement claim

## Interaction Targets

### Right Details Drawer

The details button should:

- open the right drawer
- expose drawer content to keyboard users
- set `aria-expanded`
- support close button
- close on Escape
- keep focus behavior predictable

The drawer must show only local preview details and claim boundaries.

### Left Rail

The rail button should:

- open the left rail on small screens
- set `aria-expanded`
- support close behavior
- close on Escape
- remain workspace/task navigation only

The left rail must not become a diagnostics dashboard.

### Model Selector

The selector should:

- preserve local static catalog-only data
- show selected estimate state
- make installed-vs-catalog boundary visible
- not imply model installation or execution
- remain keyboard navigable

### Composer

The composer should:

- remain the primary surface
- keep the approved local harness action path
- not accept arbitrary prompt execution
- keep selected-run summary visible
- preserve no-model/no-provider/no-download boundaries

## Claim Boundary UI

Every interactive shell surface should preserve visible boundaries:

- local preview only
- approved local harness request only
- generated deterministic harness output only
- no arbitrary prompt execution
- no model execution
- no provider calls
- no downloads
- no cloud sync
- model-needed boundary returns `execution_not_connected`
- not production evidence

## Test Plan

- preview HTML includes drawer open/close controls
- drawer controls set accessible labels and state markers
- preview HTML includes left rail open/close controls
- rail controls set accessible labels and state markers
- JS handles Escape key for shell overlays
- model selector keeps static local catalog boundaries visible
- composer action still calls only `/api/harness/run`
- JS does not call provider/model/download endpoints
- arbitrary prompt input remains absent
- smoke check covers shell interaction markers
- live local preview smoke check still covers `/health`, `/status`, `/`, run, run retrieval, events, and SSE

Tests must not:

- open a real browser from unit tests
- call external network
- call providers
- call model runtimes
- download models
- execute models
- scan private directories
- write report files

## v0.9 Task Breakdown

### Task 464: v0.9 local usability polish plan

Create this plan and link it from Studio docs.

### Task 465: right drawer open/close interaction

Add explicit Details open/close behavior, Escape close, ARIA state, focus-safe controls, and tests.

Status: implemented. The Details control opens and closes the right drawer in local browser state, exposes `aria-controls` / `aria-expanded` / `aria-hidden` state, includes an explicit close button, and closes on Escape. The drawer remains local preview content only: no model execution, provider calls, downloads, cloud sync, or report export behavior is connected.

### Task 466: left rail open/close interaction

Add mobile left rail open/close behavior, Escape close, ARIA state, and tests.

Status: implemented. The mobile rail control opens and closes the left rail in local browser state, exposes `aria-controls` / `aria-expanded` and rail state markers, includes an explicit close button, closes on Escape, and keeps desktop rail content visible to assistive technology. The rail remains workspace/task navigation only and does not add diagnostics, provider calls, model execution, downloads, cloud sync, or file export behavior.

### Task 467: model selector selected-state polish

Improve selected estimate state, focus styling, static catalog boundary copy, and tests.

Status: implemented. The compact model selector now labels the active estimate as a catalog-only selected estimate, exposes selected-state markers and `aria-selected` state, adds focus styling for the selector and catalog options, and keeps installed-vs-catalog copy visible. The selector still uses local static catalog data only and does not install, download, or execute models.

### Task 468: keyboard/focus accessibility pass

Add predictable focus styles, keyboard state checks, and accessibility-oriented smoke markers.

Status: implemented. Shell and harness controls now expose a v0.9 keyboard/focus pass marker, visible focus styles cover request buttons, action buttons, composer action, rail controls, drawer controls, and model selector options, approved request buttons include keyboard/accessibility selection markers, and the page exposes local shell accessibility state for smoke checks. No new runtime, provider, model, download, cloud, or file-export behavior was added.

### Task 469: mobile visual QA checklist and smoke check update

Add or update mobile QA checklist and smoke check markers for v0.9 shell interactions.

Status: implemented. Added the v0.9 mobile visual QA checklist and smoke-check markers for the mobile shell breakpoint, left rail overlay, compact model selector, centered composer, right drawer overlay, boundary pills, and no-overlap contract. This remains local preview QA only and does not add model execution, provider calls, downloads, cloud sync, or report export behavior.

### Task 470: v0.9 readiness report

Run validation, live local smoke check, and add v0.9 readiness report.

Status: implemented. See [KORA Studio v0.9 readiness report](kora-studio-v0-9-readiness-report.md).

### Task 471: consolidated v0.9 goal report

Create a consolidated v0.9 goal report covering Tasks 464-471, commits, validations, claim boundaries, known limitations, and next recommended goal.

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

v0.9 is complete when:

- right drawer can open and close locally
- left rail can open and close locally on small-screen scaffolds
- Escape closes shell overlays
- controls expose claim-safe accessible labels and state
- model selector selected state is clearer without implying installation or execution
- composer remains approved-harness-only
- no provider/model/download/cloud/report export behavior is added
- tests and smoke checks pass
- v0.9 readiness and consolidated goal reports are added

## Next Recommended Goal After v0.9

KORA Studio v1.0 preview readiness should focus on reducing legacy-preview dependence, tightening the shell-only information architecture, and preparing a cleaner local preview path for user testing while preserving all local-only boundaries.
