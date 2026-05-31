# KORA Studio v0.9 Mobile Visual QA Checklist

## Status

KORA Studio v0.9 mobile QA covers the local preview shell only. It is a visual and interaction checklist for the localhost preview, not a production release checklist.

## Scope

Covered surfaces:

- compact top bar at `max-width: 760px`
- left rail mobile overlay
- top model selector compact overlay menu
- centered composer and boundary pills
- right details drawer mobile overlay
- keyboard/focus markers used by shell controls
- legacy detailed preview remaining below the shell for compatibility

Out of scope:

- arbitrary prompt execution
- real model execution
- provider calls
- model downloads
- cloud sync
- private model directory scanning
- runtime model list commands
- report file export
- report file writing
- production benchmark, cost, or energy claims

## Mobile Viewports

Use at least these manual visual widths when reviewing the local preview:

- 390 px wide phone viewport
- 430 px wide large phone viewport
- 760 px breakpoint edge
- desktop width after returning from mobile width

## Required Visual Checks

- Top bar fits on one row without overlapping the left rail control, model selector, or Details control.
- Left rail is off-canvas by default on narrow viewports.
- Left rail opens as a local overlay and does not cover the whole page unnecessarily.
- Left rail close control is visible when the rail is open.
- Right details drawer is off-canvas by default.
- Right details drawer opens as a right overlay and remains scrollable.
- Details drawer close control is visible when the drawer is open.
- Model selector remains compact and readable.
- Model selector menu fits within the viewport and scrolls when content is taller than the available space.
- Composer headline, composer box, submit button, and selected-run summary remain readable.
- Boundary pills wrap without text overlap.
- Local preview, provider-disabled, and model-execution-disabled boundaries remain visible.
- Focus outlines are visible on shell and harness controls when tabbing.
- No UI text claims production readiness, provider calls, model execution, downloads, cost reduction, energy reduction, unsupported larger-model execution, or LM Studio replacement behavior.

## Smoke Check Markers

The local preview must expose these markers so automated smoke checks can catch accidental regressions:

- `data-kora-mobile-visual-qa="v0.9"`
- `data-kora-mobile-breakpoint="max-width-760"`
- `data-kora-mobile-qa-surfaces="left-rail,model-selector,composer,right-drawer,boundary-pills"`
- `data-kora-mobile-no-overlap-contract="true"`
- `data-kora-mobile-rail="collapsed-overlay"`
- `data-kora-mobile-selector="compact-overlay-menu"`
- `data-kora-mobile-drawer="right-overlay"`

## Validation

Run:

```bash
git diff --check
python3 -m pytest tests/test_kora_studio_server.py
python3 -m pytest tests/test_kora_studio_preview_smoke.py
python3 -m pytest tests -k "studio or sse or execution or harness"
```

For local smoke check:

```bash
python3 -m kora studio --no-browser
python3 scripts/check_kora_studio_preview.py
```

The smoke check remains localhost-only and must not execute models, call providers, download models, scan private model directories, call runtime model list commands, or export reports.

## Claim Boundary

v0.9 remains a local preview/demo readiness milestone. Mobile visual QA verifies layout markers and claim-safe copy only. It does not prove production readiness, real model execution, provider behavior, cost reduction, energy reduction, or unsupported larger-model execution.
