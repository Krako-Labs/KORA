# KORA Studio v1.1 Readiness Report

## Status

KORA Studio v1.1 shell-only preview hardening is complete as a local preview/demo milestone.

This report validates that the shell and right drawer now carry the normal local preview inspection path without requiring the collapsed legacy detailed preview.

KORA Studio v1.1 is not production readiness.

## Current Head

Validation was run from:

- `f9e7a40bf0bc4405bc3a0cd1946230df2dda2a50`
- `f9e7a40 test: expand kora studio v1.1 shell smoke check`

This readiness report is added by the v1.1 readiness documentation commit.

## v1.1 Objective

KORA Studio v1.1 hardens the shell-only preview experience while preserving local-only claim boundaries.

The validated target is:

- final minimal shell as the normal local preview surface
- right drawer as the normal diagnostics surface
- selected-run timeline, counters, comparison, and report metadata status mirrored through shell and drawer
- legacy detailed preview collapsed and marked as developer reference only
- v1.1 shell-only smoke result available
- no model, provider, download, cloud, report export, or report writing behavior connected

## Implemented Surface

v1.1 includes:

- shell-only hardening plan
- shell diagnostics coverage map
- v1.1 shell-only hardening marker
- v1.1 shell-only coverage marker for boundaries, drawer diagnostics, selected run, and legacy secondary state
- explicit legacy secondary/developer-reference markers
- legacy first-run-required marker set to false
- secondary local-only legacy boundary copy
- selected-run shell polish marker
- selected-run drawer primary diagnostics marker
- drawer copy that selected-run diagnostics mirror shell state for normal inspection
- shell copy that the legacy preview is not required for normal selected-run inspection
- expanded smoke check with `/ v1.1 shell-only ok`

## Validation Results

Commands run:

```bash
git diff --check
python3 -m pytest
python3 -m pytest tests -k "studio or sse or execution or harness"
```

Results:

- `git diff --check`: passed
- `python3 -m pytest`: 231 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 93 passed, 138 deselected

## Live Smoke Check

Live local preview command:

```bash
python3 -m kora studio --no-browser --port 8766
python3 scripts/check_kora_studio_preview.py --base-url http://127.0.0.1:8766
```

Result:

- live local preview smoke check passed
- local server stopped cleanly after validation

Covered smoke surfaces:

- `/health`
- `/status`
- `/api/harness/run`
- `/api/harness/run/<run_id>`
- `/api/harness/events?run_id=<id>`
- `/api/harness/sse?run_id=<id>`
- `/`

Covered shell readiness markers:

- `/ v1.0 shell-first ok`
- `/ v1.1 shell-only ok`
- final shell marker
- shell local-only boundary coverage
- drawer diagnostics coverage
- selected-run shell/drawer coverage
- legacy secondary/collapsed marker
- absence of legacy preview as the primary `<main>` surface
- legacy preview not open by default

## Claim Boundaries

The validated v1.1 preview preserves:

- local preview/demo readiness only
- approved local harness requests only
- generated local harness events only
- no arbitrary prompt execution
- no real model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export
- no report file writing
- not production telemetry
- not production cost evidence
- no production cost reduction claim
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement

## Known Limitations

Known limitations:

- v1.1 remains local preview/demo readiness only
- not production-ready
- no arbitrary prompt execution
- no real model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report export or file writing
- no persistent run history
- generated SSE streams generated harness events only
- selected run history is browser-local page memory only
- model selector is catalog-estimate-only
- catalog examples are not installed models
- legacy detailed preview still exists as collapsed developer reference
- no production telemetry evidence
- no production cost evidence
- no energy evidence

## Next Recommended Direction

Recommended next task:

- Task 486: consolidated v1.1 goal report

Recommended next goal after v1.1:

- local frontend extraction/componentization or safe removal of the remaining legacy compatibility scaffold after shell/drawer coverage is confirmed sufficient.
