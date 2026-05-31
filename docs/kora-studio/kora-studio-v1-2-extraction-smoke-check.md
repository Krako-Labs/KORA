# KORA Studio v1.2 Extraction Smoke Check

## Status

Passed.

KORA Studio v1.2 extraction smoke validation confirms that the local preview still renders the same local-only shell surfaces after shell/layout, right drawer, selected-run panel, CSS, and JavaScript template extraction.

Current HEAD at validation time:

`705c39474f96c13ac6b10f26803eb07878ab4373`

## Extraction Scope Covered

The smoke check covers the v1.2 maintainability extraction path through:

- shell layout render helper
- right details drawer render helper
- selected-run panel render helpers
- embedded CSS template helper
- embedded vanilla JavaScript template helper
- existing server-owned endpoint routing and data assembly
- existing local preview smoke markers
- existing local-only claim boundaries

This task does not add product behavior, endpoint behavior, dependencies, external assets, static file serving, frontend framework tooling, model execution, provider calls, downloads, cloud sync, report export/file writing, private model directory scanning, runtime model listing, external network behavior, or production claims.

## Helper Modules Verified

- `kora/studio_shell_render.py`
  - Provides `render_shell_layout(...)`.
  - Owns the outer shell layout, left rail, top model selector, workspace frame, and slots for composer, details drawer, and legacy reference content.

- `kora/studio_drawer_render.py`
  - Provides `render_right_details_drawer(...)`.
  - Owns right details drawer diagnostic markup and drawer marker contracts.

- `kora/studio_selected_run_render.py`
  - Provides selected-run summary, state, event stream status, timeline, counters, comparison, and report metadata render helpers.
  - Owns selected-run panel marker contracts.

- `kora/studio_style_render.py`
  - Provides `render_studio_css()`.
  - Owns the embedded local preview CSS template.
  - CSS remains inline in the rendered preview; no external CSS asset or static route is introduced.

- `kora/studio_script_render.py`
  - Provides `render_studio_javascript()`.
  - Owns the embedded vanilla JavaScript template.
  - JavaScript remains inline in the rendered preview; no external script, CDN, or static route is introduced.

`kora/studio_server.py` remains responsible for endpoint routing, status assembly, harness data, preview data preparation, and final page assembly.

## Component Markers Verified

The rendered preview and smoke checks verify these `data-kora-component` markers:

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

Additional smoke coverage remains in place for v1.0 shell-first markers and v1.1 shell-only hardening markers.

## Validation Results

Validation commands run:

- `git diff --check`
  - Passed.

- `python3 -m pytest tests/test_kora_studio_server.py`
  - Passed: 20 passed.

- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`
  - Passed: 4 passed.

- `python3 -m pytest tests -k "studio or sse or execution or harness"`
  - Passed: 97 passed, 138 deselected.

- `python3 -m pytest`
  - Passed: 235 passed.

## Live Smoke Check Result

Live local preview smoke check passed after starting the local preview with:

`python3 -m kora studio --no-browser`

Smoke command:

`python3 scripts/check_kora_studio_preview.py`

Result:

- `/health` ok
- `/status` ok
- `/api/harness/run` ok
- `/api/harness/run/<run_id>` ok
- `/api/harness/events` ok
- `/api/harness/sse` ok
- `/` v1.0 shell-first ok
- `/` v1.1 shell-only ok
- `/` v1.2 component markers ok
- `/` ok

The local preview server was stopped after the smoke check.

## Endpoints Covered

The validation and smoke pass cover:

- `GET /health`
- `GET /status`
- `GET /`
- `POST /api/harness/run`
- `GET /api/harness/run/<run_id>`
- `GET /api/harness/events?run_id=<id>`
- `GET /api/harness/sse?run_id=<id>`

Endpoint behavior remains unchanged.

## Claim Boundaries

The extraction smoke check preserves these boundaries:

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

## Known Limitations

- v1.2 is maintainability/refactor only.
- No product behavior changed.
- No frontend framework migration was performed.
- CSS and JavaScript are still inline in the rendered local preview through helper output.
- No external static asset serving was added.
- The local preview remains a local preview/demo milestone, not production readiness.
- Existing local preview/demo boundaries remain unchanged.

## Next Recommended Task

Task 488 — v1.2 readiness and consolidated goal report.
