# KORA Studio v0.6 Readiness Report

## Status

KORA Studio v0.6 is ready as a local frontend interaction hardening milestone. It keeps KORA Studio as a local deterministic harness preview while improving selected-run error handling, retry behavior, browser-local run history, generated-event stream display, and readiness validation.

v0.6 remains a local preview/demo readiness milestone, not a production release.

## Current HEAD

Validated before this report commit:

```text
eecdd172e504f8a26e7d2cffa79061b551e076a2
```

## Validation Commands and Results

```bash
git diff --check
```

Result: passed.

```bash
python3 -m pytest
```

Result: 231 passed.

```bash
python3 -m pytest tests -k "studio or sse or execution or harness"
```

Result: 93 passed, 138 deselected.

## Live Smoke Check Results

The local preview server was started with:

```bash
python3 -m kora studio --no-browser
```

Then the smoke check was run:

```bash
python3 scripts/check_kora_studio_preview.py
```

Result: passed.

Covered:

- `/health`
- `/status`
- `/api/harness/run`
- `/api/harness/run/<run_id>`
- `/api/harness/events`
- `/api/harness/sse`
- `/`

## v0.6 Implemented Surface

- Claim-safe selected-run error state.
- Retry Last Approved Request behavior limited to approved request IDs.
- Browser-local run history in page memory only.
- Active selected-run history card.
- Compact generated-counter summary on history cards.
- Clear Local Run History action that resets browser-local UI state only.
- Generated Event Stream panel using generated harness SSE events.
- Fallback from generated-event SSE to `GET /api/harness/events?run_id=<id>`.
- Selected-run event timeline from generated local harness events.
- Selected-run counters from generated local harness counters.
- Selected-run Standard Mode vs KORA Boost comparison from local harness output.
- Selected-run report metadata preview with file export and file writing disabled.

## UI Coverage

- Approved request selector remains limited to local deterministic sample request IDs.
- Run Local Harness sends only an approved `request_id`.
- Selected-run state remains browser-local page state only.
- Run history clears on refresh and is not persisted.
- Clear history does not delete server run records, backend records, report files, generated endpoints, or persisted data.
- Generated Event Stream is generated harness events only.
- Selected-run timeline is not model token streaming.
- Selected-run counters are not production telemetry.
- Selected-run comparison is not production cost evidence.
- Selected-run report metadata is preview-only and not production evidence.

## Claim Boundaries

- Local deterministic harness only.
- Approved sample requests only.
- Generated events only.
- Browser-local selected-run state only.
- Browser-local run history is page-memory only.
- No arbitrary prompt execution.
- No model execution.
- No provider calls.
- No model downloads.
- No cloud sync.
- No private model directory scanning.
- No runtime model list commands.
- No external network behavior.
- No report file export.
- No report file writing.
- No production cost reduction claim.
- No energy outcome claim.
- No unsupported larger-model execution claim.
- Not an LM Studio replacement.

## Known Limitations

- The local preview uses minimal vanilla JavaScript and is not a production frontend.
- Run records remain in-memory server state while the server process is alive.
- Browser-local history is intentionally not persisted across refreshes.
- SSE streams generated harness events only, not model tokens or provider output.
- Retry is limited to the last approved request ID and does not accept arbitrary input.
- Report metadata remains preview-only; export remains disabled.
- Model-needed boundaries return `execution_not_connected` and do not execute models.

## Next Recommended v0.7 Direction

KORA Studio v0.7 should focus on local preview reliability and UX polish:

- manual visual QA pass for the interactive local preview
- clearer responsive layout review
- selected-run state accessibility labels
- optional UI-side read-only run retrieval refresh
- no arbitrary prompt execution
- no model execution
- no provider calls
- no downloads
