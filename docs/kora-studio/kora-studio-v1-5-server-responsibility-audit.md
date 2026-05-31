# KORA Studio v1.5 Server Responsibility Audit

## Status

Task 510 audit complete.

KORA Studio v1.5 remains a maintainability/refactor milestone. This audit does not add product behavior, endpoint behavior, provider calls, model execution, model downloads, cloud sync, report export, private model directory scanning, runtime model listing, external network behavior, frontend framework tooling, dependency changes, or production claims.

## Current HEAD

Task 510 starts from:

- `b1fd6aac03a2574336826e794b25448dbb9fd835`

## Server-Owned Responsibilities

These responsibilities remain in `kora/studio_server.py`:

- local HTTP endpoint routing for `/health`, `/status`, `/`, `/api/harness/run`, `/api/harness/run/<run_id>`, `/api/harness/events`, and `/api/harness/sse`
- JSON, HTML, and SSE response writing
- POST body parsing and claim-safe error handling
- local status payload assembly in `get_studio_server_status()`
- local harness run trigger, run retrieval, event retrieval, and generated SSE dispatch
- dynamic escaping in `render_studio_placeholder_html()`
- approved request JSON embedding for the existing inline browser state script
- final document assembly, including `<!doctype html>`, inline CSS placement, inline JavaScript placement, legacy compatibility wrapper closure, and body/html closure

These responsibilities should not move to render helpers in v1.5.

## Helper-Owned Responsibilities

Render helpers own display-only markup fragments with keyword-only primitive contracts:

- shell layout and model selector shell in `kora/studio_shell_render.py`
- right details drawer in `kora/studio_drawer_render.py`
- selected-run panels in `kora/studio_selected_run_render.py`
- approved request and trigger reference panels in `kora/studio_harness_request_render.py`
- local harness/report display sections in `kora/studio_harness_display_render.py`
- run-state/history panels in `kora/studio_run_state_render.py`
- collapsed legacy opening wrapper in `kora/studio_legacy_render.py`
- model/runtime/catalog/setup/disabled-action sections in `kora/studio_model_runtime_render.py`
- endpoint/reference/limitations panels in `kora/studio_reference_render.py`
- status/boundary sections in `kora/studio_status_boundary_render.py`
- inline CSS and inline JavaScript templates in their existing render modules

Helpers receive escaped primitive strings, integers, or pre-rendered slot HTML. They must not own endpoint routing, request parsing, response writing, raw status dictionaries, local harness execution, JSON serialization/deserialization, HTML escaping, or final document assembly.

## Remaining Fragment Decision

The remaining server-owned display fragments are intentionally not extracted in Task 510:

- composer container and shell selected-run strip
- header hero copy
- final document wrapper and closing assembly
- detailed legacy compatibility body boundaries

The composer and header fragments are display-oriented, but they sit inside the shell/final-page assembly boundary and are lower-risk to leave server-owned until a later explicit shell composition decision. The final wrapper, JSON data script, inline CSS/JS placement, and compatibility wrapper closure are final document assembly concerns and remain deferred.

## Helper Contract Hardening

Task 510 hardens tests so render helpers remain display-only:

- every public helper remains keyword-only
- helper parameters remain primitive `str` or `int`
- helper return annotations remain `str`
- helper modules do not import IO, network, subprocess, HTTP server, path, browser, or request libraries
- helper modules do not reference `studio_server`, endpoint handler classes, response writer APIs, local harness run dispatch, generated event/SSE retrieval, JSON serialization/deserialization, or HTML escaping
- `kora/studio_server.py` continues to prove ownership of status assembly, endpoint handling, escaping, approved request JSON embedding, and final document assembly

## Boundaries Preserved

Task 510 preserves:

- local deterministic harness output only
- no arbitrary prompt execution
- no model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export or writing
- no external static assets or CDN
- no frontend framework migration
- no dependency addition
- not production telemetry
- not production cost evidence
- no production cost reduction claim
- no energy outcome claim
- no unsupported larger-model execution claim
- KORA Studio is not an LM Studio replacement
- KORA does not remove model memory requirements

## Task 511 Readiness Input

Task 511 should create the v1.5 readiness report after running final validation and live smoke checks. The readiness report should cite this audit as the evidence that server-owned and helper-owned responsibilities are explicitly classified.
