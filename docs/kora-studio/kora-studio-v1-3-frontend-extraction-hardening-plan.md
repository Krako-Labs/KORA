# KORA Studio v1.3 Frontend Extraction Hardening Plan

## Status and Goal

KORA Studio v1.3 is a maintainability/refactor milestone.

The goal is to continue local frontend extraction hardening after v1.2 by documenting remaining render fragments, clarifying render/data assembly boundaries, and stabilizing helper APIs with tests while preserving the existing local-only preview behavior.

v1.3 is not a product capability milestone. It must not add new runtime behavior, dependencies, frontend framework tooling, external assets, static asset serving, model execution, provider calls, downloads, cloud sync, report export/file writing, external network behavior, or production claims.

## v1.2 Starting Point

v1.2 completed:

- shell layout helper extraction in `kora/studio_shell_render.py`
- right details drawer helper extraction in `kora/studio_drawer_render.py`
- selected-run panel helper extraction in `kora/studio_selected_run_render.py`
- embedded CSS helper extraction in `kora/studio_style_render.py`
- embedded vanilla JavaScript helper extraction in `kora/studio_script_render.py`
- component inventory and marker coverage
- extraction smoke check
- readiness and consolidated goal reports

The rendered local preview remains behaviorally unchanged. CSS and JavaScript remain inline through helper output. `kora/studio_server.py` still owns endpoint routing, status assembly, harness data, preview data preparation, and final page assembly.

## Remaining Render Fragment Inventory

The following render fragments remain candidates for v1.3 inventory, documentation, or conservative extraction:

| Fragment | Current owner | v1.3 direction | Boundary to preserve |
|---|---|---|---|
| Composer container | `kora/studio_server.py` | Consider a composer render helper after confirming selected-run summary slot boundaries | Approved local harness request only; no arbitrary prompt execution |
| Shell boundary strip | `kora/studio_server.py` | Consider a boundary strip helper or keep with composer if tightly coupled | Provider, cloud, download, model execution, and report export remain disabled |
| Model selector item rows | `kora/studio_server.py` | Inventory item generation and escaping contract before extraction | Catalog examples only; selection does not install, download, or execute |
| Approved request selector cards | `kora/studio_server.py` | Inventory item generation and approved request data boundary | Approved request IDs only; no arbitrary prompt text |
| Local harness static preview sections | `kora/studio_server.py` | Consider grouping legacy preview sections into named render helpers | Generated harness data only |
| Execution Viewer legacy section | `kora/studio_server.py` | Keep as secondary reference or extract into legacy preview helper | Fixture/mock events only; no runtime execution |
| Standard Mode vs KORA Boost legacy section | `kora/studio_server.py` | Keep claim-safe and local deterministic only | Not production cost evidence |
| Report Viewer legacy section | `kora/studio_server.py` | Keep preview-only or extract into report preview helper | No file export or writing |
| Endpoint panel | `kora/studio_server.py` | Consider endpoint panel helper | Local endpoints only; behavior unchanged |
| Legacy compatibility wrapper and content | `kora/studio_server.py` | Inventory before extraction because it contains many reference sections | Secondary developer/reference scaffold only |

v1.3 should not extract all remaining fragments by default. Extraction should happen only when the helper boundary is clear, tests can preserve markers, and generated HTML behavior remains unchanged.

## Helper API Stabilization

v1.3 should make helper boundaries easier to maintain by documenting and testing:

- which helpers accept pre-escaped display values
- which helpers own raw markup strings
- which helpers own component marker contracts
- which helpers are allowed to accept HTML slot strings
- which helpers must remain pure render helpers with no I/O
- which helpers must not call endpoints, read files, start services, or inspect local runtime state

Preferred helper API rules:

- render helpers return strings only
- render helpers do not mutate global state
- render helpers do not perform network, filesystem, subprocess, runtime-model, or provider operations
- `kora/studio_server.py` assembles data and passes display-ready values into render helpers
- endpoint routing remains in `kora/studio_server.py`
- harness/run/event/report data shape remains unchanged

## Render/Data Assembly Boundary

`kora/studio_server.py` should remain the data assembly boundary for v1.3.

The server may:

- collect Studio status payload data
- assemble local harness summaries
- escape display strings before passing them to helpers where that pattern already exists
- call render helpers
- route local endpoints

Render helpers may:

- render markup from provided values
- expose stable `data-kora-component` marker contracts
- preserve local-only claim copy
- return inline CSS or JavaScript template strings

Render helpers must not:

- start servers
- call providers
- call remote APIs
- download models
- execute models
- scan private model directories
- run runtime model list commands
- write reports or exports
- add external static assets
- add frontend framework tooling

## Static Asset Serving Boundary

Static asset serving is a future option only.

v1.3 should not implement external CSS/JS files or static route serving unless a later task explicitly approves it. If evaluated in documentation, the tradeoff must include:

- local-only asset path constraints
- no CDN or external URL use
- no dependency addition
- cache and smoke-check implications
- marker preservation expectations
- why inline helper output may remain preferable for the local preview

Task 493 documents this tradeoff in [KORA Studio v1.3 static asset serving tradeoff](kora-studio-v1-3-static-asset-serving-tradeoff.md). The v1.3 decision is to keep CSS and JavaScript inline through render helpers and not implement static asset serving.

## Task Breakdown

Suggested v1.3 sequence:

- Task 489: v1.3 hardening plan and cross-links
- Task 490: inventory remaining embedded render fragments and data assembly boundaries
- Task 491: extract remaining non-JS/non-CSS preview fragments if safe
- Task 492: stabilize render helper API contracts with tests
- Task 493: document static asset serving tradeoff without implementing
- Task 494: v1.3 smoke check and readiness report
- Task 495: consolidated v1.3 goal report

## Test Strategy

Validation should continue to include:

- `git diff --check`
- `python3 -m pytest`
- `python3 -m pytest tests -k "studio or sse or execution or harness"`
- live local smoke check with `python3 -m kora studio --no-browser`
- `python3 scripts/check_kora_studio_preview.py`

Tests should preserve:

- helper output marker coverage
- full preview component marker coverage
- no external script or CDN checks
- no external CSS/static asset checks
- no arbitrary prompt input checks
- no model/provider/download endpoint call checks
- no persistence, report export, file writing, private scan, or runtime-list checks
- endpoint stability for `/health`, `/status`, `/`, `POST /api/harness/run`, `GET /api/harness/run/<run_id>`, `GET /api/harness/events?run_id=<id>`, and `GET /api/harness/sse?run_id=<id>`

Required component markers to preserve:

- `shell-layout`
- `left-rail`
- `boundary-strip`
- `top-model-selector`
- `composer`
- `approved-request-selector`
- `selected-run-summary`
- `selected-run-event-timeline`
- `selected-run-counters`
- `selected-run-comparison`
- `selected-run-report-metadata`
- `right-details-drawer`
- `run-history`
- `retry-error-state`
- `generated-event-stream-status`
- `legacy-compatibility-reference`

## Acceptance Criteria

v1.3 is ready when:

- remaining render fragments and data boundaries are documented
- any implemented extraction is behavior-preserving and test-covered
- helper API contracts are clearer and tested
- static asset serving tradeoffs are documented without implementation unless explicitly approved
- full validation passes
- live smoke check passes
- readiness and consolidated goal reports are created
- claim boundaries remain unchanged

## Claim Boundaries

v1.3 must preserve:

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
