# KORA Studio v0.6 Frontend Interaction Hardening Plan

## Status and Goal

KORA Studio v0.5 is complete as a local preview/demo milestone. It adds an approved request selector, Run Local Harness button, browser-local selected-run state, selected-run event timeline, selected-run counters, selected-run Standard Mode vs KORA Boost comparison, and selected-run report metadata preview.

KORA Studio v0.6 should harden the local frontend interaction layer around selected-run error handling, retry behavior, browser-local run history, optional generated-event SSE display, and local preview reliability.

v0.6 remains a local deterministic harness preview. It is not a production release, hosted service, LM Studio replacement, generic local chatbot, provider billing dashboard, cost-reduction dashboard, or energy dashboard.

## Scope

Allowed:

- selected-run error state display
- retry last approved request
- local endpoint unavailable messages
- malformed local response messages
- browser-local multi-run history state
- selected-run history list
- selected `run_id` switching within browser memory
- clear local state action
- optional generated-event SSE UI for existing generated harness events
- fallback from SSE display to `GET /api/harness/events?run_id=<id>`
- local preview smoke check updates
- public-safe readiness and goal reports

Forbidden:

- arbitrary prompt input
- model execution
- provider calls
- model downloads
- cloud sync
- private model directory scanning
- runtime model list commands
- report file export
- report file writing
- external network behavior
- production cost reduction claim
- energy outcome claim
- unsupported larger-model execution claim
- LM Studio replacement claim

## Selected-run Error and Retry UX

The local preview should make local interaction failures explicit without implying provider fallback, model execution, or cloud recovery.

Planned states:

- `idle`
- `running`
- `completed`
- `failed`
- `events_unavailable`
- `malformed_response`
- `local_endpoint_unavailable`
- `retry_available`

The retry action should:

- retry only the last approved `request_id`
- call only `POST /api/harness/run`
- never send arbitrary text
- never call provider, model, download, cloud, report export, or runtime model list endpoints
- preserve claim-safe failure copy

Safe error copy:

- "Local harness run failed."
- "Retry uses the last approved sample request only."
- "No model execution was attempted."
- "Provider calls remain disabled."
- "No downloads are connected."

## Generated-event SSE UI Option

v0.6 may connect the UI to:

```text
GET /api/harness/sse?run_id=<id>
```

This is optional and should be implemented only if it remains small and safe.

If included, the UI must:

- stream generated local harness events only
- display stream start/completion state
- show disconnect/error state
- fall back to `GET /api/harness/events?run_id=<id>`
- clearly state that it is not model token streaming
- clearly state that it is not provider streaming
- clearly state that it does not execute a model

The SSE UI must not:

- stream model tokens
- stream provider output
- stream model output
- execute a model
- call external services
- accept arbitrary prompts

## Multi-run Browser-local State

v0.6 should introduce browser-local run history in page memory only.

Planned state fields:

- `selected_request_id`
- `selected_run_id`
- `last_request_id`
- `last_error`
- `run_history`
- `run_history_limit`
- `selected_run`
- `selected_events`
- `selected_counters`
- `selected_comparison_summary`
- `selected_report_metadata_summary`
- `selected_claim_boundary`

Each run history item should include safe summary fields:

- `run_id`
- `request_id`
- `run_status`
- `created_at`
- `completed_at`
- `event_count`
- `model_execution_status`
- `provider_calls_enabled`
- `cloud_sync_enabled`
- `file_export_enabled`
- `claim_boundary`

State must remain browser-local memory only. Do not use `localStorage`, `sessionStorage`, IndexedDB, cookies, file writes, uploads, or cloud sync unless a future task explicitly scopes that behavior.

## Selected-run History List

The preview should show a selected-run history list after local harness runs are generated.

The history list should:

- show recent browser-local runs
- allow switching the selected run by `run_id`
- render selected-run summary, events, counters, comparison, and report metadata for the selected history item
- include a clear local state action
- explain that refresh clears browser-local state

The history list must not:

- persist run history to disk
- upload run history
- load arbitrary local files
- scan private directories
- imply production telemetry

## Local Preview Reliability Expectations

v0.6 should improve the reliability of the local preview interaction without broadening the product surface.

Expected behavior:

- selector starts with an approved request selected
- run button shows running/disabled state while a request is in flight
- repeated clicks do not create ambiguous UI state
- local endpoint errors show claim-safe messages
- malformed local JSON shows claim-safe messages
- event retrieval errors do not erase the run summary
- retry action is available only when there is a last approved request
- clear local state resets browser-local selected run and history only

## Claim Boundaries

Every v0.6 UI surface must keep these boundaries visible:

- local deterministic harness output only
- approved deterministic sample requests only
- browser-local state only
- generated events only
- no arbitrary prompt execution
- no model execution
- no provider calls
- no downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export
- no report file writing
- no production telemetry claim
- no production cost evidence claim
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement

## Test Plan

Required tests:

- preview HTML includes selected-run error state container
- preview HTML includes retry last approved request control
- retry calls only `POST /api/harness/run` with the last approved `request_id`
- endpoint unavailable errors render claim-safe copy
- malformed response errors render claim-safe copy
- preview HTML includes browser-local run history container
- history entries are page-memory only
- selected `run_id` switching updates selected-run rendering
- clear local state resets browser-local state
- optional SSE UI calls only `/api/harness/sse?run_id=<id>` for existing runs
- optional SSE UI includes no model token/provider streaming claims
- fallback event retrieval uses only `/api/harness/events?run_id=<id>`
- no arbitrary prompt input is present
- no provider/model/download/cloud/report export endpoints are called
- smoke check covers v0.6 UI markers

Tests must not:

- open a browser unless explicitly scoped to local preview smoke checking
- call external network
- call providers
- call external model APIs
- download models
- execute models
- scan private model directories
- run runtime model list commands
- write report files

## v0.6 Task Breakdown

### Task 449 - v0.6 Plan and Cross-links

Create this v0.6 frontend interaction hardening plan and add public-safe links from the Studio docs.

### Task 450 - Selected-run Error and Retry UX

Add selected-run error state display, retry last approved request behavior, endpoint unavailable copy, malformed response copy, and tests. Keep retry limited to approved request IDs.

Status: Connected in the local preview. The UI tracks browser-local loading/error state, shows claim-safe endpoint unavailable and malformed response messages, and exposes Retry Last Approved Request. Retry reuses only the last approved request ID and calls only `POST /api/harness/run`.

### Task 451 - Multi-run Browser-local History State

Add page-memory run history, selected `run_id` switching, and clear local state behavior. Do not persist state beyond browser memory.

Status: Connected in the local preview. Successful local harness run responses are stored in bounded browser page memory only, the UI can switch selected runs from recent browser-local history, and Clear Local Run History clears browser preview state only without persistence, file writes, cloud sync, backend deletion, model execution, provider calls, or downloads.

### Task 452 - Optional Generated-event SSE UI Connection

If still small and safe, add UI connection to `/api/harness/sse?run_id=<id>` for generated harness events only. Include disconnect/error handling and fallback to `/api/harness/events`.

### Task 453 - Selected-run History UI Hardening

Polish the browser-local history list, selected-run switching copy, empty states, and boundary text. Keep all outputs local deterministic harness output only.

### Task 454 - v0.6 Smoke Check and Readiness Report

Extend the smoke check for v0.6 markers and create `docs/kora-studio/kora-studio-v0-6-readiness-report.md` after validation.

### Task 455 - Consolidated v0.6 Goal Report

Create `docs/kora-studio/kora-studio-v0-6-goal-report.md` with task summaries, commits, validation results, live smoke check results, known limitations, and next recommended milestone.

## Acceptance Criteria

- v0.6 plan is linked from Studio docs.
- Error states are claim-safe.
- Retry uses only the last approved request ID.
- Browser-local run history is page-memory only.
- Selected-run switching does not require persistence or external calls beyond existing local harness endpoints.
- Optional SSE UI, if implemented, streams generated harness events only.
- Smoke check covers v0.6 local interaction markers.
- No model/provider/download/cloud/report export behavior is introduced.
- No unsupported product claims are introduced.
