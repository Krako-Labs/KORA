# KORA Studio v1.2 Frontend Extraction Plan

## Status and Goal

KORA Studio v1.2 is a maintainability milestone, not a product capability milestone.

The goal is to plan how the current embedded local preview shell can be extracted into maintainable render sections, template fragments, or local static assets without changing behavior, weakening local-only boundaries, adding dependencies, or claiming production readiness.

v1.2 should preserve the v1.1 state:

- final shell as the primary local preview surface
- right details drawer as the normal diagnostics surface
- legacy detailed preview collapsed as developer/reference scaffolding
- approved local harness requests only
- generated local harness data only
- no provider, model execution, download, cloud sync, report export, or report writing behavior connected

## Current Problem

The shell-first local preview has grown into a dense embedded HTML, CSS, and vanilla JavaScript surface inside the local preview server.

This was acceptable while the preview was small, but the v1.1 shell now includes:

- shell layout
- left rail
- compact model selector
- composer and approved harness trigger
- selected-run summary
- selected-run event timeline
- selected-run counters
- selected-run Standard Mode vs KORA Boost comparison
- selected-run report metadata
- browser-local run history
- retry and error states
- generated event stream status
- right details drawer diagnostics
- collapsed legacy compatibility reference
- smoke-check markers and claim-boundary copy

Keeping all of this in one large server-rendered string makes future changes brittle. Small UI changes can unintentionally affect smoke markers, claim boundaries, local-only endpoint restrictions, accessibility state, or the legacy compatibility scaffold. v1.2 should reduce that maintenance risk before additional UI work lands.

## Non-goals

v1.2 planning does not authorize:

- new product behavior
- framework migration yet
- dependency addition
- production readiness claim
- model execution
- provider calls
- model downloads
- cloud sync
- report export
- report file writing
- arbitrary prompt input
- private model directory scanning
- runtime model list commands
- external network behavior

## Component Map

Current embedded UI should be mapped into the following maintainable components or render sections.

The current marker inventory is tracked in [KORA Studio v1.2 component inventory](kora-studio-v1-2-component-inventory.md).

| Proposed component | Current responsibility | Boundary to preserve |
|---|---|---|
| Shell layout | Main app frame, responsive shell markers, primary preview surface | Local preview/demo only |
| Left rail / workspace navigation | KORA Studio label, task/project labels, local workspace status | No cloud sync |
| Top model selector / runtime boundary | Static catalog estimate selector and selected estimate label | Catalog examples are not installed models; selection does not install, download, or execute |
| Composer / approved harness request input | Centered composer and Run Local Harness action | Approved request IDs only; no arbitrary prompt execution |
| Selected-run summary | Run id, request id, status, model/provider/cloud/export boundary states | Generated local harness output only |
| Selected-run event timeline | Generated event cards loaded from selected local run | Not model token streaming; no provider output |
| Selected-run counters | Generated counters from local run output | Not production telemetry; no cost or energy claim |
| Standard Mode vs KORA Boost comparison | Local harness comparison summary | Not production cost evidence; no real model execution |
| Selected-run report metadata | Report metadata preview from selected run response | Preview only; no file export or writing |
| Right details drawer | Runtime status, selected model boundary, route trace, counters, report metadata, claim boundaries | Diagnostics only; not a provider/runtime/model control panel |
| Run history | Browser-local selected-run history and clear-history behavior | Page memory only; no persistence or backend deletion |
| Retry/error state | Retry last approved request and claim-safe failure messages | Retry only approved request IDs; no fallback provider/model path |
| Generated event stream status | SSE status and fallback to events endpoint | Generated harness events only; no token/provider stream |
| Boundary/status strip | Compact local-only disabled state pills | Provider/cloud/download/model/report export remain disabled |
| Legacy compatibility reference | Collapsed detailed preview for developer/reference coverage | Secondary, collapsed, not required for normal first-run inspection |

## Extraction Options

### Option 1: Server-side render helper functions in Python

Move major shell sections into small Python helper functions in `kora/studio_server.py` or a sibling local module.

- Implementation risk: low to medium. The code remains standard-library Python and can be extracted incrementally.
- Test impact: low. Existing HTML marker tests and smoke checks can remain stable if helper output is unchanged.
- Dependency impact: none.
- Smoke check impact: low. Current markers can stay byte-for-byte stable while helper ownership changes.
- Local-only boundary: strong if helpers remain pure render helpers and do not add I/O or endpoint behavior.
- Suitability for v1.2: best first step.

### Option 2: Split embedded CSS/JS strings into local Python modules/templates

Move CSS and JavaScript into named Python constants or local template fragments while keeping the server as the renderer.

- Implementation risk: medium. It reduces file density but can create string/template coordination issues.
- Test impact: low to medium. Tests should verify no external scripts, no forbidden endpoint calls, and marker stability.
- Dependency impact: none if implemented with plain Python modules or local text fragments.
- Smoke check impact: low if generated HTML remains equivalent.
- Local-only boundary: strong if templates are shipped in repo and served only by localhost server.
- Suitability for v1.2: good after section-level render helpers are identified.

### Option 3: Static local assets served by the local server

Serve local CSS and JavaScript files from repository-owned static paths through the localhost server.

- Implementation risk: medium. It introduces asset routing and cache behavior that current tests do not need.
- Test impact: medium. Smoke checks must verify local-only asset paths, no CDN use, and no missing assets.
- Dependency impact: none if assets are plain CSS/JS and served by the existing server.
- Smoke check impact: medium. Tests should cover asset routes and preserve shell markers.
- Local-only boundary: acceptable if assets are served only from local repository files and no external URLs are added.
- Suitability for v1.2: possible later in v1.2, but should follow an inventory and helper extraction pass.

### Option 4: Future frontend framework extraction

Move the shell into a framework-based frontend later.

- Implementation risk: high for v1.2 because it would alter build, dependency, and validation expectations.
- Test impact: high. It would require frontend build/test decisions and stronger browser validation.
- Dependency impact: high unless an existing approved frontend stack is reused.
- Smoke check impact: high. Current static HTML marker checks would need redesign.
- Local-only boundary: manageable but easier to weaken accidentally if package scripts, dev servers, or external assets are introduced.
- Suitability for v1.2: not recommended. Keep as a later non-v1.2 option after local render ownership is cleaned up.

## Recommended v1.2 Path

Use a conservative extraction path:

1. Inventory the embedded shell sections and add component ownership markers where missing.
2. Extract shell layout rendering into Python helper functions or local template fragments.
3. Extract right drawer/detail rendering into helper functions.
4. Extract selected-run panels into helper functions.
5. Extract local CSS and JavaScript into named helper/template constants without dependencies.
6. Keep generated HTML behavior unchanged.
7. Keep all smoke markers stable.
8. Keep all endpoints stable.
9. Keep all claim boundaries unchanged.

This path avoids a framework migration and keeps the server local-only while making the current preview easier to maintain.

Task 483 started this path by adding a shell layout render helper for the outer shell frame, left rail, top model selector, workspace wrapper, and content slots. Runtime behavior, endpoint behavior, dependencies, and claim boundaries remain unchanged.

Task 484 continued this path by adding a right details drawer render helper for the drawer diagnostics markup. Runtime behavior, endpoint behavior, dependencies, smoke markers, and claim boundaries remain unchanged.

Task 485 continued this path by adding selected-run render helpers for the composer selected-run summary and selected-run state, generated event stream status, timeline, counters, comparison, and report metadata panels. Runtime behavior, endpoint behavior, dependencies, smoke markers, and claim boundaries remain unchanged.

Task 486 continued this path by adding embedded CSS and vanilla JavaScript template helpers. CSS and JavaScript remain inline in the rendered local preview, no external assets or static routes were added, and runtime behavior, endpoint behavior, dependencies, smoke markers, and claim boundaries remain unchanged.

Task 487 validated the extracted helper split with a dedicated [v1.2 extraction smoke check](kora-studio-v1-2-extraction-smoke-check.md). Validation and live smoke checks confirmed that endpoints, component markers, smoke markers, inline CSS/JavaScript behavior, and claim boundaries remain unchanged.

## Test Strategy

Validation should continue to include:

- existing pytest coverage
- `python3 -m pytest tests -k "studio or sse or execution or harness"`
- smoke check coverage for shell markers
- live local smoke check when implementation tasks touch rendering

Additional v1.2 extraction tests should include:

- HTML marker tests for each extracted component
- helper output tests where helper functions become public enough to test directly
- no external script or CDN checks
- no model/provider/download behavior checks
- no arbitrary prompt input checks
- no persistence checks
- no report export or file writing checks
- stable endpoint checks for `/health`, `/status`, `/`, `POST /api/harness/run`, `GET /api/harness/run/<run_id>`, `GET /api/harness/events?run_id=<id>`, and `GET /api/harness/sse?run_id=<id>`

## Task Breakdown

Suggested v1.2 task sequence:

- Task 481: v1.2 extraction plan and cross-links
- Task 482: inventory embedded shell sections and add component markers
- Task 483: extract shell layout render helper
- Task 484: extract right drawer/detail render helper
- Task 485: extract selected-run panels render helpers
- Task 486: extract local JS/CSS template helpers without dependencies
- Task 487: v1.2 extraction smoke check
- Task 488: v1.2 readiness and consolidated goal report

## Claim Boundaries

v1.2 must preserve:

- KORA Studio is local preview/demo readiness only.
- KORA Studio is not production-ready.
- KORA Studio is not an LM Studio replacement.
- No arbitrary prompt execution.
- No real model execution.
- No provider calls.
- No model downloads.
- No cloud sync.
- No private model directory scanning.
- No runtime model list commands.
- No report export or file writing.
- Generated harness data only.
- Not production telemetry.
- Not production cost evidence.
- No production cost reduction claim.
- No energy outcome claim.
- No unsupported larger-model execution claim.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.
