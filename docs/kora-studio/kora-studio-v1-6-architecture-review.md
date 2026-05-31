# KORA Studio v1.6 Architecture Review

## Status and Purpose

KORA Studio v1.6 is an architecture decision milestone for the local preview.

This review follows KORA Studio v1.5 Local Preview Server Slimming. v1.5 improved helper/server ownership boundaries and extracted safe display-only fragments, but it also made clear that KORA Studio should not continue extracting Python render fragments indefinitely without a broader architecture decision.

This document reviews the current local preview architecture and recommends the next technical direction. It does not implement product behavior, endpoint behavior, static asset serving, frontend framework tooling, model execution, provider calls, model downloads, cloud sync, report export/file writing, private model directory scanning, runtime model list commands, external network behavior, or production claims.

## Current Local Preview Server Responsibilities

`kora/studio_server.py` remains the local server boundary.

It currently owns:

- local host validation
- `/health`, `/status`, `/`, `/api/harness/run`, `/api/harness/run/<run_id>`, `/api/harness/events`, and `/api/harness/sse` routing
- JSON, HTML, and SSE response writing
- POST body parsing and claim-safe error handling
- local status payload assembly
- local harness request, run, event, comparison, and report metadata assembly
- model catalog/status assembly
- dynamic HTML escaping
- approved request JSON embedding for browser-local state
- composer container and shell selected-run strip assembly
- header hero copy
- detailed legacy preview body assembly
- final HTML document assembly, including inline CSS and inline JavaScript placement

These responsibilities remain intentionally server-owned because the current preview is a dependency-free, localhost-only standard-library server.

## Current Helper Modules

Current render helpers include:

- `kora/studio_shell_render.py`
- `kora/studio_drawer_render.py`
- `kora/studio_selected_run_render.py`
- `kora/studio_reference_render.py`
- `kora/studio_harness_request_render.py`
- `kora/studio_run_state_render.py`
- `kora/studio_legacy_render.py`
- `kora/studio_style_render.py`
- `kora/studio_script_render.py`
- `kora/studio_status_boundary_render.py`
- `kora/studio_model_runtime_render.py`
- `kora/studio_harness_display_render.py`

The helpers own display-only markup, inline CSS text, or inline JavaScript text. Helper contract tests require known public render functions to stay keyword-only where inputs are needed, return strings, avoid server/IO/network/subprocess dependencies, and avoid taking ownership of endpoint routing, response writing, payload assembly, local harness dispatch, JSON serialization/deserialization, HTML escaping, or final document assembly.

## Remaining Embedded Responsibilities

The main embedded responsibilities still in `kora/studio_server.py` are:

- composer container and shell selected-run strip
- header hero copy
- final document wrapper and closure
- approved request JSON script embedding
- inline CSS and inline JavaScript insertion points
- detailed legacy compatibility body boundaries
- endpoint and status payload assembly

The composer and header are partly display-oriented, but they sit at the shell/final-document composition boundary. Extracting them now would be possible, but it would continue the fragment-by-fragment pattern rather than resolving the larger question: whether KORA Studio should keep growing as server-assembled HTML strings or introduce a more explicit asset/component boundary.

## Current Inline CSS/JS Approach

CSS and JavaScript are still rendered inline through:

- `render_studio_css()`
- `render_studio_javascript()`

This keeps the preview simple and dependency-free. It also avoids static asset routing, cache behavior, path traversal risks, MIME type policy, and additional smoke-test surfaces.

The downside is that CSS and JavaScript remain large text templates. They are test-covered, but the source organization is not ideal for long-term UI iteration. A static local asset plan is the next likely architecture step, but implementation should wait until the path constraints, local-only serving rules, no-external-asset policy, cache behavior, and marker coverage are explicitly specified.

## Test and Smoke Marker Coverage

Current coverage includes:

- helper API contract tests
- helper module dependency boundary tests
- helper/server ownership tests
- helper-owned marker tests
- full rendered preview marker tests
- endpoint behavior tests
- local preview smoke tests
- live smoke coverage for `/health`, `/status`, `/api/harness/run`, `/api/harness/run/<run_id>`, `/api/harness/events`, `/api/harness/sse`, and `/`

The v1.5 readiness run reported:

- `python3 -m pytest`: 248 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 110 passed, 138 deselected
- live smoke check passed for the local preview endpoints and shell/component markers

This coverage is strong enough for documentation and helper-boundary refactors. It is not yet enough to safely introduce static asset serving without additional asset-path, MIME, cache, and no-external-reference tests.

## Maintainability Risks

Current risks:

- `kora/studio_server.py` still owns final document assembly and several embedded shell fragments.
- Inline CSS and JavaScript helpers are easier to test than one large server string, but still harder to edit than normal asset files.
- Continuing Python helper extraction may produce diminishing returns.
- Static asset serving would improve source organization but adds new server behavior and security surface.
- A frontend framework migration would be premature without first stabilizing the asset boundary and deciding whether the preview should remain standard-library-only.
- Product capability scaffolding could resume, but doing so before an asset/static-serving decision may make later UI architecture changes harder.

## Local-Only and Security Implications

Current local-only posture is conservative:

- localhost-only server binding
- no external assets or CDN
- no provider calls
- no model execution
- no downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report export/file writing

Static asset serving would add new local file-serving behavior. That can still be local-only and dependency-free, but it needs explicit rules before implementation:

- serve only an allowlisted static directory
- reject path traversal
- use fixed MIME types
- avoid directory listing
- avoid arbitrary file reads
- avoid cache behavior that hides changed local assets during development
- reject remote asset references in CSS/JS/HTML
- preserve existing smoke markers

## Claim Boundary Implications

The architecture direction must not change KORA Studio's public claim boundary.

Any next step must preserve:

- KORA Studio is local preview/demo readiness only.
- KORA Studio is not production-ready.
- KORA Studio is not an LM Studio replacement.
- Generated harness data only.
- No arbitrary prompt execution.
- No real model execution.
- No provider calls.
- No model downloads.
- No cloud sync.
- No private model directory scanning.
- No runtime model list commands.
- No report export/file writing.
- Not production telemetry.
- Not production cost evidence.
- No production cost reduction claim.
- No energy outcome claim.
- No unsupported larger-model execution claim.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Decision Options

### Option 1: Continue Python Helper Extraction

Description:

Continue extracting remaining display fragments from `kora/studio_server.py` into Python render helpers.

Implementation risk:

- Low for small fragments.
- Risk grows as extraction approaches final document assembly and shell composition.

Dependency impact:

- None.

Test impact:

- Existing helper contract tests can cover this path.
- Additional helper marker tests would be straightforward.

Smoke check impact:

- Low if rendered markers and endpoints remain unchanged.

Local-only/security boundary:

- Strong. No new file serving or runtime surface.

Public claim risk:

- Low. This is organization-only work.

Developer maintainability:

- Improves small areas, but diminishing returns are likely after v1.5.
- Does not solve inline CSS/JS editing friction.

Suitability for next goal:

- Acceptable only for small cleanup if no architecture decision is desired.
- Not recommended as the main next goal because it may become busywork.

### Option 2: Move CSS/JS to Local Static Assets Served by the Local Server

Description:

Plan and later implement local static serving for first-party CSS and JavaScript assets while keeping the preview localhost-only, dependency-free, and claim-safe.

Implementation risk:

- Medium.
- Static serving is simple in concept but adds server behavior, path policy, MIME behavior, and cache decisions.

Dependency impact:

- None if implemented with the standard library.
- Must not add bundlers, package managers, or frontend framework tooling in the first implementation.

Test impact:

- Requires new tests for allowlisted paths, rejected traversal, content type, no external references, existing endpoint behavior, and marker preservation.

Smoke check impact:

- Requires smoke checks that `/` loads asset references and static endpoints respond locally.
- Must preserve existing `/health`, `/status`, harness endpoints, and shell/component marker checks.

Local-only/security boundary:

- Good if allowlisted and localhost-only.
- Riskier than inline assets until path constraints are tested.

Public claim risk:

- Low if documented as architecture-only and local preview only.

Developer maintainability:

- High potential benefit.
- CSS/JS become easier to edit, review, and eventually migrate.

Suitability for next goal:

- Recommended as the next planning goal, not immediate implementation.
- A v1.7 static asset serving plan should define exact path constraints, cache behavior, MIME policy, no-external-asset checks, tests, and smoke markers before code changes.

### Option 3: Prepare Future Frontend Framework Extraction

Description:

Start planning a later migration from server-rendered HTML strings to a frontend framework or component build.

Implementation risk:

- High if implemented now.
- It would change build assumptions, dependency policy, asset serving, test strategy, and contributor workflow.

Dependency impact:

- High if any framework/toolchain is introduced.
- Conflicts with current no-dependency local preview posture.

Test impact:

- Requires frontend build validation, browser rendering checks, asset serving tests, and likely a broader CI decision.

Smoke check impact:

- Significant. Current smoke checks assume server-rendered inline assets and stable marker strings.

Local-only/security boundary:

- Manageable later, but riskier now because new toolchains may introduce external asset or package assumptions.

Public claim risk:

- Low if kept as planning, but implementation churn could distract from claim-safe product work.

Developer maintainability:

- Could be high later.
- Premature now because the project has not yet made the static asset serving decision.

Suitability for next goal:

- Not recommended as the immediate next goal.
- Revisit after static asset policy and local frontend architecture are explicit.

### Option 4: Pause Refactor and Shift to Product Capability Scaffolding

Description:

Stop architecture refactoring and return to product capability scaffolding such as runtime/model availability validation, still without model execution or provider calls.

Implementation risk:

- Medium.
- Product capability scaffolds often touch status payloads, UI copy, and claim boundaries.

Dependency impact:

- Should remain none if scoped carefully.

Test impact:

- Requires new status contract tests and claim-boundary tests.
- May require additional smoke markers.

Smoke check impact:

- Moderate. New surfaces would need smoke coverage.

Local-only/security boundary:

- Must remain conservative.
- Runtime/model availability work is especially sensitive because it could imply installed-model scanning, runtime model listing, downloads, or execution if not tightly bounded.

Public claim risk:

- Medium.
- Capability scaffolding can easily imply production readiness, model support, or hardware capability if copy is not strict.

Developer maintainability:

- Product value is higher than continued fragment extraction.
- But capability work before asset/static architecture is settled may make UI maintenance harder.

Suitability for next goal:

- Good after local preview architecture is stable enough.
- Not recommended as the immediate next goal if static asset serving remains undecided.

## Recommendation

Recommended path:

1. Treat v1.6 as architecture decision only.
2. Use v1.7 to plan local static asset serving for CSS/JS, not implement it.
3. Delay actual static asset serving until the plan defines:
   - allowlisted local asset directory
   - rejected path traversal behavior
   - MIME types
   - cache behavior
   - no external assets or CDN references
   - no arbitrary local file reads
   - preservation of existing endpoint behavior
   - preservation of existing smoke markers
   - tests and live smoke expectations
4. Keep frontend framework extraction deferred until after static asset serving is either implemented safely or explicitly rejected.
5. Resume product capability scaffolding after local preview architecture is stable enough to avoid repeated large UI/server rewrites.

Rationale:

- Continuing helper extraction alone has diminishing returns after v1.5.
- Static asset serving is the next real architectural decision, but implementing it without a dedicated plan would add avoidable local file-serving risk.
- A frontend framework is premature while the repo still intentionally avoids frontend dependencies.
- Product capability scaffolding is important, but claim-sensitive capability work should follow a stable local preview architecture.

## Next Recommended Goal

Goal 515G — KORA Studio v1.7 Local Static Asset Serving Plan.

The v1.7 goal should be documentation/planning only. It should define the static asset serving design, constraints, tests, smoke markers, and no-external-asset policy before any implementation task serves CSS or JavaScript from files.
