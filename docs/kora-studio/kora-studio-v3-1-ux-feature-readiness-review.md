# KORA Studio v3.1 UX/Feature Readiness Review

## Status

KORA Studio v3.1 is a review-only local demo/preview readiness assessment.

No runtime behavior, endpoint behavior, CSP behavior, static asset allowlist, dependency, frontend tooling, package manifest, lockfile, bundler, npm workflow, external asset, or CDN change is included in this review.

## Review Scope

This review covers the current KORA Studio operator workflow and demo surface:

- Run Local Harness workflow
- approved request selector
- browser-local run history
- selected-run summary
- timeline and generated event visibility
- generated event stream status and fallback behavior
- selected-run comparison panel
- report metadata display
- error and empty states
- Retry Last Approved Request
- details drawer
- compact model selector boundary
- local-only boundary/status strip
- narrow/mobile layout signals
- accessibility basics visible in the current implementation
- claim boundaries for what Studio does not do

## Current Capabilities

KORA Studio currently provides a local-only preview shell with a compact top model selector, centered composer, boundary strip, right details drawer, collapsed legacy compatibility preview, package-controlled CSS/JavaScript assets, and root-only local-preview CSP.

The primary operator workflow is:

1. Choose an approved local harness request from the approved request selector.
2. Run the selected approved request through the Run Local Harness action.
3. Inspect selected-run status, generated events, counters, comparison, report metadata, and claim boundaries.
4. Use the details drawer for mirrored selected-run diagnostics and local runtime/catalog boundary context.
5. Use browser-local run history to switch between recent completed local runs during the current page session.

The Studio preview can currently demonstrate:

- approved request selection without arbitrary prompt execution
- local deterministic harness run triggering through `POST /api/harness/run`
- generated event retrieval through `GET /api/harness/events?run_id=<id>`
- generated event stream display through `GET /api/harness/sse?run_id=<id>` with local endpoint fallback
- selected-run counters from generated local harness output
- selected-run Standard Mode vs KORA Boost comparison from generated local harness output
- selected-run report metadata preview without file export or file writing
- retry using only the last approved request ID
- page-memory run history with active-run selection and clear-state behavior
- shell and drawer state mirroring for selected-run timeline, counters, comparison, and report metadata
- local-only boundary display for provider calls, cloud sync, downloads, model execution, and report export

## What Studio Cannot Do

KORA Studio remains a local preview/demo surface only. It does not:

- execute arbitrary prompts
- execute real models
- call providers
- download models
- sync to cloud
- scan private model directories
- run runtime model-list commands
- export reports
- write report files
- provide production telemetry
- provide production cost evidence
- prove cost reduction or energy outcomes
- replace LM Studio
- remove RAM, VRAM, unified-memory, or model-loading requirements
- prove unsupported larger-model execution

## Findings

### Blocker

No blocker was found for the current local demo/preview scope.

The current Studio surface can support a bounded operator demo because the primary flow is visible, claim boundaries are explicit, and successful runs update the selected-run summary, timeline, counters, comparison, report metadata, history, and drawer diagnostics.

### Important But Not Blocker

1. The operator path is functionally complete but still visually dense.

   The local preview exposes many claim-boundary and diagnostic panels at once. This is useful for safety and testability, but the first-run operator path could be clearer if the primary run workflow, selected-run results, and diagnostic/reference material were more strongly separated.

2. Run history is intentionally page-memory only, but that limitation should remain prominent.

   Current copy says history clears on refresh and does not delete backend records or files. That is correct for preview scope. Future workflow work should preserve this wording unless persistent storage is intentionally added.

3. The details drawer mirrors selected-run state, but it is still primarily diagnostic.

   The drawer is useful for inspection, runtime/catalog boundaries, route trace, counters, report metadata, and claim boundaries. It is not yet a task-focused operator command center.

4. SSE status is claim-safe, but the operator meaning of fallback states could be clearer.

   The UI distinguishes generated harness events from model token streaming and has fallback to the local events endpoint. Future UX polish should make `streaming`, `completed`, and `fallback` states easier to scan without reducing the claim-safe wording.

5. The compact model selector boundary is strong, but it remains static-catalog only.

   The selector makes clear that catalog options are estimates and do not install, download, or execute a model. Future model-related work must keep catalog suggestions distinct from installed/runnable model detection.

6. Accessibility basics are present, but not a full accessibility audit.

   Current implementation includes ARIA expanded state, labelled drawer/rail controls, focus-visible styling, Escape close behavior, `aria-live` regions, and smoke-checkable accessibility state. A deeper keyboard traversal and screen-reader pass should be a future review goal before broader demos.

7. Narrow/mobile layout has implementation markers and smoke coverage, but not current visual evidence in this goal.

   The shell includes mobile overlay markers for the rail, selector, composer, drawer, and boundary pills. This review did not generate fresh responsive screenshots, so mobile confidence remains based on prior checklist coverage and current markup/CSS inspection.

### Cosmetic

1. Some button labels remain text-heavy.

   `Menu`, `Details`, `Run Local Harness`, `Retry Last Approved Request`, and `Clear Local Run History` are explicit and test-friendly, but future visual polish could make the shell feel less heavy while preserving accessible names.

2. Repeated boundary copy is correct but verbose.

   The repeated "no model execution / no provider calls / no downloads" language is useful for claim safety. Future UX polish can reduce visual repetition only if the boundaries remain obvious at decision points.

3. Legacy compatibility preview remains visible below the primary shell.

   It is collapsed and labelled as secondary developer/reference scaffolding, so it is not a blocker. It still adds page length and cognitive load.

## Area-by-Area Readiness

| Area | Current state | Readiness | Notes |
|---|---|---|---|
| Run Local Harness workflow | Approved request ID only, posts to local run endpoint, updates selected-run surfaces | Demo-ready | No arbitrary prompt text is sent. |
| Approved request selector | Button-based approved request options and selected preview | Demo-ready | Current state is browser-local page memory. |
| Run history | Bounded browser-local history with active run cards and clear-state control | Demo-ready with caveat | Page-memory only; clears on refresh. |
| Selected run summary | Composer and shell state update with status/run/request IDs | Demo-ready | Good primary feedback path. |
| Timeline/events | Generated local harness events render as cards | Demo-ready | Not model token streaming or provider output. |
| SSE status | EventSource stream with local events fallback | Demo-ready with polish opportunity | Fallback state could be more scannable. |
| Comparison panel | Local harness comparison summary | Demo-ready | Not production cost evidence. |
| Report metadata | Preview-only metadata from run summary | Demo-ready | No export or file writing. |
| Error/empty states | Endpoint unavailable, parse error, missing fields, no events, unavailable counters/comparison/report | Demo-ready | Copy preserves disabled model/provider boundary. |
| Retry last approved request | Reuses last approved request ID only | Demo-ready | No prompt entry path added. |
| Details drawer | Mirrors selected-run status and boundary diagnostics | Useful diagnostic surface | Could become more operator-focused later. |
| Compact model selector | Catalog-only estimate state with explicit non-install/non-run boundary | Demo-ready | Not installed model detection. |
| Local-only boundary strip | Visible provider/cloud/download/model/report export boundary pills | Demo-ready | Maintains safe demo framing. |
| Narrow/mobile layout | Overlay-ready markers and CSS behavior present | Needs future visual re-check | This goal did not capture screenshots. |
| Accessibility basics | ARIA state, focus-visible styles, Escape close, live regions | Basic-ready | Not a complete accessibility audit. |

## Prioritized Next Goals

1. Goal 531G - KORA Studio Primary Operator Path Simplification Plan

   Review whether the first viewport should more clearly prioritize approved request selection, Run Local Harness, selected-run summary, and event/result inspection while keeping diagnostics available but secondary.

2. Goal 532G - KORA Studio SSE/Timeline State UX Polish

   Improve the scanability of generated event stream states, fallback state, and timeline loading/empty/error states without adding model streaming or provider claims.

3. Goal 533G - KORA Studio Details Drawer Operator Utility Review

   Decide which drawer sections should remain diagnostic, which should become operator-facing, and which should stay in legacy/reference surfaces.

4. Goal 534G - KORA Studio Responsive Visual QA Refresh

   Re-run narrow/mobile visual review for rail overlay, compact selector, composer, boundary pills, details drawer, and selected-run results.

5. Goal 535G - KORA Studio Accessibility Interaction Review

   Perform a focused keyboard and screen-reader-oriented review of the primary run workflow, drawer, rail, selector, history selection, and live selected-run updates.

## Claim Boundary Check

- KORA Studio remains local preview/demo readiness only.
- This is review-only documentation, not production readiness.
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

Required validation for this documentation-only review:

- `git diff --check`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed

Optional validation:

- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed
- `python3 scripts/check_kora_studio_preview.py`: passed

The local Studio server used for the standard preview smoke check was stopped cleanly after validation.
