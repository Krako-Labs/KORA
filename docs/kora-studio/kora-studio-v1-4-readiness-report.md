# KORA Studio v1.4 Readiness Report

## Status

KORA Studio v1.4 local preview fragment extraction is ready for the v1.4 readiness milestone based on validation run at:

`2a0d57673f80518ccd33fa768b78d58fbee61817`

This report commit is docs-only. v1.4 is a maintainability/refactor milestone. It does not add product behavior, endpoint behavior, dependencies, frontend framework tooling, external static asset serving, model execution, provider calls, model downloads, cloud sync, report export/file writing, private model directory scanning, runtime model listing, external network behavior, or production claims.

## Implemented Surface

v1.4 completed these maintainability surfaces:

- v1.4 local preview fragment extraction plan
- next-fragment inventory for remaining server-owned preview fragments
- approved request selector and local harness trigger extraction into `kora/studio_harness_request_render.py`
- retry/error and browser-local run history extraction into `kora/studio_run_state_render.py`
- collapsed legacy compatibility opening wrapper extraction into `kora/studio_legacy_render.py`
- render helper contract and marker coverage hardening
- v1.4 render helper contract documentation
- README, implementation breakdown, plan, and inventory cross-links

The local preview still renders CSS and JavaScript inline through:

- `render_studio_css()`
- `render_studio_javascript()`

No static asset routes were added.

## Validation Results

Validation run from:

`repository checkout root`

Results:

- `git diff --check`: passed
- `python3 -m pytest`: 243 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 105 passed, 138 deselected
- `python3 -m pytest tests/test_kora_studio_server.py`: 28 passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: 4 passed

## Live Smoke Check

Live local preview validation was run with:

```bash
python3 -m kora studio --no-browser
python3 scripts/check_kora_studio_preview.py
```

An existing local process was first found on `127.0.0.1:8765`, stopped, and the smoke check was rerun against a fresh local preview server.

Result: passed.

Covered surfaces:

- `/health`
- `/status`
- `POST /api/harness/run`
- `GET /api/harness/run/<run_id>`
- `GET /api/harness/events?run_id=<id>`
- `GET /api/harness/sse?run_id=<id>`
- `/`
- v1.0 shell-first markers
- v1.1 shell-only markers
- v1.2 component markers

## Files Added

- `docs/kora-studio/kora-studio-v1-4-local-preview-fragment-extraction-plan.md`
- `docs/kora-studio/kora-studio-v1-4-fragment-inventory.md`
- `docs/kora-studio/kora-studio-v1-4-render-helper-contracts.md`
- `kora/studio_harness_request_render.py`
- `kora/studio_run_state_render.py`
- `kora/studio_legacy_render.py`

## Files Updated

- `docs/kora-studio/README.md`
- `docs/kora-studio/kora-studio-implementation-breakdown.md`
- `kora/studio_server.py`
- `tests/test_kora_studio_server.py`

## Extraction Boundary

v1.4 extracted only the next safe group of server-owned preview fragments:

- approved request selector intro card
- selected request preview card
- Run Local Harness action card
- local harness selector option cards
- local harness trigger reference cards
- selected-run retry/error card
- Retry Last Approved Request card
- Local Run History card
- Clear Local Run History card
- local run history dynamic container
- collapsed legacy compatibility opening wrapper

`kora/studio_server.py` remains responsible for:

- endpoint routing
- local status payload assembly
- local harness request/run/event/comparison/report data assembly
- model catalog/status assembly
- escaping dynamic display values
- local harness requests JSON embedding
- detailed legacy preview body assembly
- closing legacy wrapper/final document assembly

## Helper Contract Boundary

Task 501 hardened helper contracts so:

- every public `render_*` function in known render-helper modules is covered by the contract test set
- expected helper membership cannot silently drift
- helper signatures remain string-returning and keyword-only for required inputs
- helper modules remain free of filesystem, network, subprocess, server, and browser-launch dependencies
- helper-owned component markers remain visible in the full rendered preview

Current extracted helper modules include:

- `kora/studio_shell_render.py`
- `kora/studio_drawer_render.py`
- `kora/studio_selected_run_render.py`
- `kora/studio_reference_render.py`
- `kora/studio_harness_request_render.py`
- `kora/studio_run_state_render.py`
- `kora/studio_legacy_render.py`
- `kora/studio_style_render.py`
- `kora/studio_script_render.py`

## Preserved Behavior

v1.4 preserves:

- endpoint routes
- endpoint response shapes
- selected-run JavaScript behavior
- local run history behavior
- retry behavior
- generated harness event/counter/comparison/report metadata shapes
- model selector behavior
- static asset serving decision
- inline CSS and inline JavaScript
- public UI copy except extraction-only placement changes

## Claim Boundaries

v1.4 preserves:

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

## Known Limitations

- `kora/studio_server.py` still owns endpoint routing, data assembly, escaping, and final page assembly.
- The composer container and shell boundary strip remain embedded in `kora/studio_server.py`.
- Model selector item rows remain server-assembled and passed into the shell helper as slot HTML.
- Local harness sample status/request/boundary cards remain server-owned.
- Static generated timeline and counter cards remain server-owned.
- Detailed legacy preview body sections remain server-owned.
- Static asset serving remains intentionally unimplemented.
- The preview remains local deterministic harness/demo output only.

## Readiness Decision

KORA Studio v1.4 is ready as a local preview fragment extraction milestone.

The milestone improves maintainability and helper contract coverage without changing product behavior, endpoint behavior, local-only boundaries, inline CSS/JavaScript, or public claim boundaries.

## Next Recommended Task

Task 503: create the consolidated KORA Studio v1.4 goal report.
