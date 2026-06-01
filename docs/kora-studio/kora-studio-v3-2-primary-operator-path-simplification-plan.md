# KORA Studio v3.2 Primary Operator Path Simplification Plan

## Status

KORA Studio v3.2 is a planning-only review for simplifying the primary local demo operator journey.

No UI implementation, runtime behavior change, endpoint behavior change, CSP change, static asset allowlist change, dependency, frontend tooling, package manifest, lockfile, bundler, npm workflow, external asset, or CDN change is included in this plan.

## Goal

Make the first-time local demo path easier to follow while preserving the current local-only and claim-safe boundaries.

The target operator journey is:

1. Open Studio.
2. Understand local-only boundaries.
3. Select an approved request.
4. Run Local Harness.
5. Understand run progress.
6. Read result summary.
7. Inspect timeline/details if needed.
8. Retry last approved request if needed.

## Current Path Assessment

The current Studio surface can support the operator journey, but the path competes with diagnostic, boundary, compatibility, and reference surfaces. The main issue is not missing capability; it is the amount of equally weighted information around the primary action and result surfaces.

Current strengths:

- local-only boundary strip is visible in the shell
- approved request selector exists and prevents arbitrary prompt execution
- Run Local Harness is connected to the approved request ID path
- selected-run summary updates near the composer
- selected-run timeline, counters, comparison, and report metadata are available
- generated event stream has local events fallback
- Retry Last Approved Request is bounded to the last approved request ID
- details drawer mirrors selected-run diagnostics and claim boundaries
- legacy preview is collapsed and labelled secondary

Current simplification problem:

- the first operator action is split between the composer shell and lower approved request panels
- selected request, run action, run status, and result summary are not presented as one obvious primary workflow unit
- safety copy is correct but repeated at many levels
- diagnostic and reference panels still appear at similar visual weight to the primary run path
- timeline, counters, comparison, and report metadata are all valid but could use clearer progressive disclosure

## Friction Classification

### Blocker

No blocker was found for the current local demo/preview scope.

The operator can open Studio, see boundaries, select an approved request, run the local harness, see progress/status, inspect generated outputs, and retry the last approved request without adding arbitrary prompt execution or provider/model behavior.

### Important But Not Blocker

1. Primary action grouping is too diffuse.

   The approved request selector, selected request preview, Run Local Harness button, composer action, selected-run summary, and selected-run state all exist, but they are spread across several panels. The next implementation should create a clearer primary operator path section without changing the approved request ID boundary.

2. Boundary copy needs hierarchy, not removal.

   The local-only and "no model/provider/download/export" boundaries are necessary. They should remain visible at decision points, but repeated long explanations can move into secondary details once the primary boundary is clear.

3. Run progress needs a single scan target.

   The current UI updates composer status, selected run state, SSE status, selected-run strip, and drawer fields. Future UI should make one primary status surface authoritative while keeping mirrored diagnostics available.

4. Result summary should precede deep diagnostics.

   Counters, comparison, report metadata, and event timeline are all useful. The first result view should summarize the run outcome before showing full event cards and metadata grids.

5. Timeline and details should be progressive.

   Generated event timeline, SSE/fallback details, report metadata, and drawer diagnostics should be easy to inspect after the operator understands the run result. They should not compete with the initial action path.

6. Retry should be closer to the error/result context.

   Retry Last Approved Request is claim-safe and correctly bounded. It should appear where the operator sees the failure or last-run outcome, not only as a separate utility panel.

7. The compact model selector should remain secondary in this journey.

   The selector is useful context, but the primary local demo path is approved request routing, not model management. Its catalog-only boundary must remain explicit.

### Cosmetic

1. Button and panel labels are explicit but heavy.

   Current labels are safe and testable. Future polish can reduce visual weight while preserving accessible names and smoke markers.

2. Legacy compatibility preview adds page length.

   It is collapsed and not a blocker. Future implementation can keep it secondary while making the primary shell feel complete without scrolling into legacy content.

3. Boundary chips and repeated panel copy could be visually compressed.

   The content should remain claim-safe, but it can be organized into short labels plus expandable detail.

## Recommended Simplified Journey

### Step 1: Open Studio

Keep the first viewport focused on the shell, local-only boundary, selected approved request, Run Local Harness action, and selected-run status.

Implementation candidate:

- create a primary workflow band inside the shell that combines current selected request preview, Run Local Harness, and composer selected-run summary
- keep the top model selector visible but secondary
- keep details drawer access available from the top bar

### Step 2: Understand Local-Only Boundaries

Keep a compact boundary strip visible before the run action.

Implementation candidate:

- preserve visible pills for local preview, provider calls disabled, cloud sync disabled, downloads disabled, model execution not connected, and report export disabled
- move repeated explanatory boundary paragraphs into a secondary "Why this is safe" detail area or drawer section

### Step 3: Select Approved Request

Make approved request selection part of the primary workflow, not a lower diagnostic grid.

Implementation candidate:

- promote request options into a compact selectable list near the run action
- keep `data-kora-request-id` and approved request only behavior unchanged
- keep selected request preview concise: request ID, route class, model-needed boundary, short request text

### Step 4: Run Local Harness

Make one primary Run Local Harness button the obvious action.

Implementation candidate:

- keep both existing entry points only if they serve distinct layout needs
- if both remain, make the composer action and workflow button update the same primary status surface
- keep `POST /api/harness/run` with selected approved `request_id` only

### Step 5: Understand Run Progress

Make one run status block authoritative for the operator.

Implementation candidate:

- show states such as `not_started`, `running`, `completed`, `failed`, `streaming`, and `fallback`
- keep SSE status available, but do not require the operator to read the SSE diagnostic card to understand progress
- preserve generated event stream wording as generated harness events only

### Step 6: Read Result Summary

Show the result summary before deep event cards.

Implementation candidate:

- add a compact selected-run result summary card that includes status, run ID, request ID, event count, model execution status, provider calls, file export, and a short claim boundary
- show counters and comparison highlights as summary fields before full grids
- keep "not production telemetry" and "not production cost evidence" near these summary fields

### Step 7: Inspect Timeline/Details If Needed

Keep timeline and details available, but secondary to the summary.

Implementation candidate:

- place generated event timeline under an "Inspect generated timeline" section
- keep report metadata and detailed counters below the summary or in the drawer
- keep details drawer as the diagnostic mirror for runtime/catalog/route/report/boundary inspection

### Step 8: Retry Last Approved Request If Needed

Tie retry to error and last-run context.

Implementation candidate:

- surface Retry Last Approved Request near the failed status or last-run summary
- keep retry disabled unless a last approved request ID exists
- keep retry calling only `POST /api/harness/run` with the last approved request ID

## Prioritized Implementation Candidates

1. Goal 532G - Primary Workflow Band Implementation

   Create a shell-level primary workflow band that groups local-only boundary, selected approved request, Run Local Harness, and selected-run summary. Preserve existing endpoints, markers, approved request ID behavior, JavaScript asset route, CSS asset route, and claim boundaries.

2. Goal 533G - Result Summary Before Diagnostics

   Add a compact selected-run result summary above timeline/counter/comparison/report metadata detail grids. Keep generated harness data only and avoid production telemetry or cost evidence claims.

3. Goal 534G - Run Progress and SSE State Simplification

   Make run progress scannable through one primary status surface while preserving generated event stream status, fallback behavior, and no model-token-streaming boundary.

4. Goal 535G - Retry Placement and Error State Polish

   Move or mirror Retry Last Approved Request near the relevant error/result context while preserving the last approved request ID boundary.

5. Goal 536G - Diagnostic Surface Rebalancing

   Decide which current panels remain in the primary flow, which move behind the details drawer, and which stay in the collapsed legacy compatibility preview.

6. Goal 537G - Primary Path Responsive and Accessibility Check

   Validate the simplified path across narrow/mobile layout and basic keyboard/screen-reader interaction after implementation.

## Implementation Guardrails

Future implementation goals should preserve:

- approved request IDs only
- no arbitrary prompt text execution
- no real model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report export or file writing
- local deterministic harness data only
- generated event stream as generated harness events only
- selected-run counters as non-production telemetry
- selected-run comparison as non-production cost evidence
- report metadata as preview-only
- package-controlled `/studio-assets/studio.css` and `/studio-assets/studio.js`
- current narrow CSP and asset allowlist unless a separate reviewed goal changes them

Future implementation goals should not add:

- frontend frameworks
- frontend build tooling
- package manifests or lockfiles
- bundlers or npm workflows
- external assets or CDN sources
- broad CSP sources
- wildcard static asset routes
- report export or filesystem write behavior

## Acceptance Criteria For The Next Implementation Goal

The next implementation goal should be considered successful only if:

- the first-time operator can identify the selected approved request and primary Run Local Harness action without relying on the lower legacy/reference content
- local-only boundaries remain visible before running
- run progress has one obvious primary status surface
- result summary appears before deep diagnostics
- details/timeline/report metadata remain inspectable but secondary
- retry remains limited to the last approved request ID
- smoke markers and existing server/static/CSP tests remain stable
- no claim boundary is broadened

## Claim Boundary Check

- KORA Studio remains local preview/demo readiness only.
- This is planning/review only, not production readiness.
- KORA Studio is not production-ready.
- KORA Studio is not an LM Studio replacement.
- No arbitrary prompt execution was added or recommended.
- No real model execution was added or recommended.
- No provider calls were added or recommended.
- No model downloads were added or recommended.
- No cloud sync was added or recommended.
- No private model directory scanning was added or recommended.
- No runtime model list commands were added or recommended.
- No report export or file writing was added or recommended.
- No production telemetry, production cost evidence, cost reduction claim, or energy outcome claim was added.
- KORA still does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Validation Results

Required validation for this planning-only review:

- `git diff --check`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed
