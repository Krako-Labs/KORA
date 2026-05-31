# KORA Studio v1.5 Server Slimming Plan

## Status and Goal

KORA Studio v1.5 is a maintainability/refactor milestone for the local preview server.

The goal is to slim `kora/studio_server.py` by identifying remaining server-owned UI/data-display fragments, extracting only safe low-risk fragments into render helpers, and preserving all endpoint behavior, smoke markers, helper contracts, inline CSS/JavaScript, and claim boundaries.

v1.5 must not add product behavior. It must not change local harness behavior, endpoint response shapes, selected-run JavaScript behavior, local run history behavior, retry behavior, generated harness event/counter/comparison/report metadata shapes, model selector behavior, static asset serving decisions, or public claim boundaries.

## Current Server Responsibilities

After v1.4, `kora/studio_server.py` still owns:

- endpoint routing
- local status payload assembly
- local harness request, run, event, comparison, and report data assembly
- model catalog/status assembly
- HTML escaping of dynamic display values
- local harness requests JSON embedding
- model selector item row assembly
- composer container and boundary strip assembly
- local harness sample status/request/boundary cards
- static generated timeline and counter cards
- detailed legacy preview body assembly
- closing legacy wrapper and final document assembly

These responsibilities are intentionally mixed today because the preview is dependency-free, local-only, and served by a standard-library Python server.

## Existing Helper State

Current render helper modules include:

- `kora/studio_shell_render.py`
- `kora/studio_drawer_render.py`
- `kora/studio_selected_run_render.py`
- `kora/studio_reference_render.py`
- `kora/studio_harness_request_render.py`
- `kora/studio_run_state_render.py`
- `kora/studio_legacy_render.py`
- `kora/studio_style_render.py`
- `kora/studio_script_render.py`

v1.5 should extend this pattern only where the extracted fragment is display-only, has a clear helper contract, and can be covered by marker/smoke tests without weakening local-only boundaries.

## Remaining Server-Owned UI/Data-Display Fragments

Initial v1.5 candidates for inventory:

- Launch/local-only status cards
- system profile summary cards
- model capability estimate cards
- runtime detected/service reachability cards
- model catalog versus installed-local cards
- setup guidance cards
- local harness status and boundary cards
- local harness static sample event cards
- generated counters static cards
- report metadata preview cards still embedded in server composition
- model selector item row display assembly
- composer container and shell boundary strip
- detailed legacy preview body sections
- closing legacy wrapper and final document assembly

## Classification Rules

Each remaining responsibility should be classified as one of:

- `should remain server-owned`: endpoint routing, status/data assembly, escaping, JSON embedding, and final document assembly.
- `safe to extract now`: display-only markup with primitive/string parameters, preserved markers, and no endpoint/data logic.
- `defer to future static asset/frontend decision`: CSS/JS asset routing, build tooling, framework migration, or any broader frontend architecture change.
- `already extracted`: fragments owned by existing render helper modules.

## Preferred Extraction Order

v1.5 should proceed conservatively:

1. Inventory remaining server-owned UI/data-display fragments before extraction.
2. Extract status/boundary display fragments if they are display-only and marker-covered.
3. Extract model/catalog/runtime display fragments if data preparation and escaping remain server-owned.
4. Extract harness endpoint guidance/display fragments if they do not change endpoint behavior.
5. Audit server responsibility and helper contracts after extraction.
6. Run full validation and live smoke checks before readiness closure.

If a fragment mixes display, escaping, and data assembly too tightly, it should remain server-owned and be documented as deferred.

## Helper API Contract Expectations

New or changed render helpers should:

- return HTML strings
- use keyword-only required parameters where parameters are needed
- accept primitive display values or pre-rendered slot HTML, not raw `/status` payload dictionaries by default
- avoid filesystem access
- avoid network access
- avoid subprocess calls
- avoid browser-launch logic
- avoid endpoint routing logic
- avoid provider/model/download/cloud/report-export behavior
- preserve existing component markers and smoke-checkable copy
- preserve local-only/no-provider/no-model/no-download/no-cloud/no-report-export boundaries

The server should continue to own dynamic escaping unless a helper receives only already-escaped display strings.

## Marker and Smoke Coverage Expectations

All v1.5 extractions must preserve:

- `/health`
- `/status`
- `/`
- `POST /api/harness/run`
- `GET /api/harness/run/<run_id>`
- `GET /api/harness/events?run_id=<id>`
- `GET /api/harness/sse?run_id=<id>`
- v1.0 shell-first markers
- v1.1 shell-only markers
- v1.2 component markers
- v1.3/v1.4 helper-owned markers where applicable
- local-only claim boundary text
- no-model/no-provider/no-download/no-cloud/no-report-export text

Smoke checks must not require a browser, provider, model runtime, model download, private directory scan, runtime model list command, or external network behavior.

## No Behavior Change Rule

v1.5 must preserve:

- endpoint routes
- endpoint response shapes
- selected-run JavaScript behavior
- optional generated-event SSE UI behavior
- local run history behavior
- retry behavior
- generated harness event/counter/comparison/report metadata shapes
- compact model selector behavior
- static asset serving decision
- inline CSS and inline JavaScript
- public UI behavior except extraction-only source organization

## Test Plan

Run after each safe extraction:

- `git diff --check`
- `python3 -m pytest tests/test_kora_studio_server.py`
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`
- `python3 -m pytest tests -k "studio or sse or execution or harness"`

Run for readiness closure:

- `git diff --check`
- `python3 -m pytest`
- `python3 -m pytest tests -k "studio or sse or execution or harness"`
- `python3 -m kora studio --no-browser`
- `python3 scripts/check_kora_studio_preview.py`

The local server must be stopped cleanly after live smoke validation.

## Claim Boundaries

v1.5 preserves:

- KORA Studio is local preview/demo readiness only.
- KORA Studio is not production-ready.
- KORA Studio is not an LM Studio replacement.
- Generated harness data only.
- No arbitrary prompt execution.
- No model execution.
- No provider calls.
- No model downloads.
- No cloud sync.
- No private model directory scanning.
- No runtime model list commands.
- No report export.
- No file writing.
- No external static assets or CDN.
- No frontend framework migration.
- No dependency addition.
- Not production telemetry.
- Not production cost evidence.
- No production cost reduction claim.
- No energy outcome claim.
- No unsupported larger-model execution claim.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Task Breakdown

Task 505: v1.5 server slimming plan and cross-links.

Task 506: inventory remaining server-owned UI/data-display fragments. See [KORA Studio v1.5 server-owned fragment inventory](kora-studio-v1-5-server-owned-fragment-inventory.md).

Task 507: extract status/boundary display fragment if safe. Extracted shell boundary, launch/local-only status, and KORA Boost boundary display fragments into `kora/studio_status_boundary_render.py`.

Task 508: extract model/catalog/runtime display fragment if safe.

Task 509: extract harness endpoint guidance/display fragment if safe.

Task 510: server responsibility audit and helper contract hardening.

Task 511: v1.5 smoke check and readiness report.

Task 512: consolidated v1.5 goal report.

## Readiness Criteria

KORA Studio v1.5 is ready when:

- remaining server-owned UI/data-display fragments are inventoried
- safe extractions are behavior-preserving and covered by tests
- server-owned responsibilities are documented
- helper-owned responsibilities are documented
- deferred fragments are explicitly classified
- static asset serving remains a future decision
- all endpoint behavior and smoke markers remain intact
- full validation passes
- live local preview smoke check passes
- readiness and consolidated goal reports are created
