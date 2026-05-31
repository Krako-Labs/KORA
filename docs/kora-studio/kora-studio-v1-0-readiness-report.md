# KORA Studio v1.0 Readiness Report

## Status

KORA Studio v1.0 preview readiness is complete as a local preview/demo milestone.

This report validates the shell-first local preview state. It does not mark KORA Studio as production-ready.

## Current Head

Validation was run from:

- `9e8b5f814cda8fbcd9855ed0ef1b4dea67a6622c`
- `9e8b5f8 test: add kora studio v1.0 shell smoke check`

This readiness report is added by the v1.0 closure documentation commit.

## v1.0 Objective

KORA Studio v1.0 reduces dependence on the legacy detailed preview and makes the final minimal shell the primary local preview experience.

The validated direction is:

- shell-first local preview surface
- compact catalog-estimate-only model selector
- approved local harness composer path
- selected-run state visible through shell and drawer surfaces
- right drawer as the primary diagnostics surface
- collapsed legacy preview retained as compatibility/developer scaffolding
- local-only claim boundaries preserved

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

The smoke check also covers:

- v1.0 shell-first readiness marker
- shell boundary coverage
- selected-run shell/drawer coverage
- collapsed legacy compatibility mode
- absence of legacy preview as the primary `<main>` surface

## Implemented v1.0 Surface

KORA Studio v1.0 preview readiness includes:

- final minimal shell as the primary local preview surface
- shell-first readiness marker
- local-only boundary strip in the shell
- provider calls disabled boundary
- cloud sync disabled boundary
- downloads disabled boundary
- model execution not connected boundary
- report export/write disabled boundary
- compact model selector with catalog-estimate-only copy
- composer path limited to approved local harness request IDs
- selected-run summary in the shell
- selected-run detail strip for timeline, counters, comparison, and report metadata state
- right details drawer as the primary diagnostics surface
- drawer runtime status
- drawer selected model boundary
- drawer catalog vs installed distinction
- drawer route trace status
- drawer generated counters status
- drawer selected-run surface status
- drawer report metadata status
- drawer claim boundary coverage
- collapsed legacy detailed preview compatibility scaffold
- generated harness run endpoint
- generated run retrieval endpoint
- generated events endpoint
- generated SSE endpoint for generated harness events only
- dedicated v1.0 shell-first smoke coverage

## Legacy Preview Compatibility Status

The legacy detailed preview is no longer the primary local preview surface.

It is:

- collapsed by default
- labelled as a compatibility/developer scaffold
- retained for reference and smoke coverage
- secondary to the final minimal shell and right drawer

## Claim Boundaries

The validated v1.0 preview keeps these boundaries:

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

KORA Studio v1.0 remains limited to local preview/demo readiness.

Known limitations:

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
- no production telemetry evidence
- no production cost evidence
- no energy evidence

## Next Recommended Direction

Recommended v1.1 direction:

KORA Studio v1.1 shell-only preview hardening or local frontend extraction/componentization.

The next milestone should continue reducing dependence on the compatibility scaffold while preserving the same local-only boundaries.
