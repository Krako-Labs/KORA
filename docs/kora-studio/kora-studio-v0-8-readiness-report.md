# KORA Studio v0.8 Readiness Report

## Status

KORA Studio v0.8 is ready as a local preview/demo milestone for the final UI board implementation.

v0.8 implements the final v0.7 source-of-truth UI direction in the local preview while preserving the existing local deterministic harness and claim boundaries. It remains a local preview/demo milestone, not a production release.

## Current HEAD

- Public truth: `origin/main`
- Validated HEAD before this report commit: `30017c37cafc64f82596d6eb0efaef84b2a9ff81`
- Branch: `main`

## Implemented Surface

- Chat-first sparse default workspace shell.
- Small left mini rail for workspace/task navigation only.
- Compact top model selector scaffold sourced from local static catalog recommendations.
- Centered composer as the primary first-screen surface.
- Composer action connected to the approved local harness request path only.
- Compact composer selected-run summary.
- Boundary pills for local preview, provider-disabled state, and model-execution-not-connected state.
- Hidden right details drawer scaffold.
- Drawer sections for runtime status, selected model boundary, catalog vs installed, route trace, generated counters, report metadata, and claim boundaries.
- Mobile-ready shell markers and CSS for collapsed rail, compact selector, wrapped pills, centered composer, and right drawer overlay behavior.
- Detailed legacy local preview remains below the shell for compatibility while v0.8 migration continues.

## Endpoints Covered

- `GET /health`
- `GET /status`
- `GET /`
- `POST /api/harness/run`
- `GET /api/harness/run/<run_id>`
- `GET /api/harness/events?run_id=<id>`
- `GET /api/harness/sse?run_id=<id>`

## Validation Results

- `git diff --check`: passed
- `python3 -m pytest`: 231 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 93 passed, 138 deselected
- `python3 scripts/check_kora_studio_preview.py --base-url http://127.0.0.1:8766`: passed against a live local preview server
- Live UI marker check: passed for final shell, responsive shell, model selector, composer action, right drawer, drawer sections, and legacy preview marker
- Browser snapshot check: local page rendered with left rail, top selector, centered composer, and off-canvas right details drawer

The live preview was started with:

```bash
python3 -m kora studio --no-browser --port 8766
```

The server was stopped after validation.

## Claim Boundaries

- KORA Studio v0.8 is a local preview/demo milestone, not a production release.
- KORA Studio is a local-first AI Task Execution Router workspace.
- KORA Studio is not an LM Studio replacement.
- The compact model selector shows local static catalog recommendations as estimates only.
- Catalog examples are not installed models.
- Selecting a catalog item does not install, download, or execute a model.
- Model recommendations are estimates until validated.
- KORA does not remove model memory requirements.
- The composer action sends only the selected approved local harness request ID.
- Arbitrary prompt execution is not connected.
- Local harness events are generated deterministic harness events only.
- SSE streams generated harness events only, not model tokens, provider output, or model output.
- Model-needed boundaries return `execution_not_connected`.
- Provider calls are disabled by default.
- Cloud sync is disabled by default.
- Download/run/model execution actions remain disabled.
- Report metadata is preview-only.
- Report export and file writing remain disabled.
- No private model directories are scanned.
- No runtime model list commands are called.
- No production cost reduction claim is made.
- No energy outcome claim is made.
- No unsupported larger-model execution claim is made.

## Known Limitations

- The right details drawer remains visually off-canvas by default and is still a scaffolded destination.
- The left rail and drawer mobile behavior are CSS/marker scaffolds, not a full persisted navigation system.
- The top model selector is a local catalog scaffold, not a real installed-model picker.
- The composer does not accept or execute arbitrary prompts.
- Local harness runs remain generated deterministic harness output.
- Run records are in-memory only.
- Report metadata remains preview-only and does not export files.
- The detailed legacy preview remains below the new shell for compatibility.
- Node-side mobile rendering was not run because the Node REPL environment did not have Playwright installed; the live served HTML/CSS markers and desktop browser snapshot were verified.

## Next Recommended Task

Task 463 should create the consolidated v0.8 goal report covering Tasks 456-463, commits, changed files, validations, claim boundaries, known limitations, and the next recommended goal.

After v0.8 reporting is complete, the next product direction should be KORA Studio v0.9 local usability polish, including keyboard/focus accessibility, drawer open/close controls, and tighter removal of legacy preview dependence.
