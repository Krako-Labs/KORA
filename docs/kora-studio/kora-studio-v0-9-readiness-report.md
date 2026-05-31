# KORA Studio v0.9 Readiness Report

## Status

KORA Studio v0.9 local usability polish is readiness-validated as a local preview/demo milestone.

Current HEAD at validation:

```text
4cd81cdbf1c6ba4d3aa365e6fc869b9529ba532f
```

v0.9 is not a production release.

## Implemented Surface

v0.9 builds on the v0.8 final shell and adds:

- right details drawer open/close controls
- right drawer close button
- right drawer `aria-controls`, `aria-expanded`, `aria-hidden`, and state markers
- Escape close behavior for shell overlays
- mobile left rail open/close controls
- mobile left rail close button
- left rail `aria-controls`, `aria-expanded`, viewport-aware `aria-hidden`, and state markers
- compact model selector selected-state polish
- catalog-only selected estimate label
- `aria-selected` and selected-state markers for the active estimate
- focus-visible styling for shell and harness controls
- approved request button accessibility labels and keyboard-selection markers
- smoke-checkable local shell accessibility state
- v0.9 mobile visual QA checklist
- mobile visual QA markers for shell breakpoint, rail, selector, composer, drawer, and boundary pills

## Validation Results

Validation was run from:

```text
/Users/albertkim/02_PROJECTS/05_KORA_Project/repo/KORA
```

Commands and results:

```bash
git diff --check
# passed

python3 -m py_compile kora/studio_server.py
# passed

python3 -m pytest
# 231 passed

python3 -m pytest tests -k "studio or sse or execution or harness"
# 93 passed, 138 deselected
```

## Live Smoke Check

Local preview server:

```bash
python3 -m kora studio --no-browser --port 8766
```

Smoke check:

```bash
python3 scripts/check_kora_studio_preview.py --base-url http://127.0.0.1:8766
```

Result:

```text
KORA Studio preview smoke check passed.
- /health ok
- /status ok
- /api/harness/run ok
- /api/harness/run/<run_id> ok
- /api/harness/events ok
- /api/harness/sse ok
- / ok
```

Browser marker check confirmed:

- final shell marker present
- v0.9 mobile QA marker present
- keyboard/focus pass marker present
- left rail toggle present
- right details drawer toggle present
- model selector state is `catalog-estimate-only`
- no model/provider/download endpoint markers present

## Readiness Criteria

Readiness evidence:

- right drawer can open and close locally
- left rail can open and close locally on small-screen scaffolds
- Escape closes shell overlays
- controls expose claim-safe accessible labels and state markers
- model selector selected state is clearer without implying installation or execution
- composer remains approved-harness-only
- mobile visual QA checklist exists
- smoke check covers v0.9 shell, mobile QA, keyboard/focus, rail, drawer, selector, and harness markers
- full test suite passed

## Claim Boundaries

KORA Studio v0.9 remains local preview/demo readiness only.

Boundaries:

- local deterministic harness output only
- generated events only
- approved sample request IDs only
- no arbitrary prompt execution
- no real model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export
- no report file writing
- no external model/provider APIs
- no production cost reduction claim
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement

## Known Limitations

- v0.9 remains a local preview/demo milestone.
- The detailed legacy preview remains below the shell for compatibility.
- The model selector is still a local static catalog estimate surface, not an installed-model picker.
- The local preview uses embedded HTML/CSS and vanilla JavaScript, not a full frontend app.
- Run records remain in-memory while the server process is alive.
- SSE streams generated harness events only, not model tokens.
- Report metadata is preview-only; export remains disabled.
- Mobile QA is documented and marker-checked, but manual visual review remains required for final visual approval.

## Next Recommended Task

Task 471: create the consolidated v0.9 goal report covering Tasks 464-471, commits, changed files, validation results, live smoke check, claim boundaries, known limitations, and the next recommended v1.0 preview readiness goal.
