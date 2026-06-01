# KORA Studio v4.1 Optional Browser Keyboard Smoke Feasibility

## Status

KORA Studio v4.1 evaluates whether to add an optional browser keyboard smoke script now.

Decision: keep keyboard traversal manual-only for this milestone. Do not add a new browser keyboard smoke script yet.

This is a documentation and feasibility milestone. It does not change runtime behavior, backend routes, local harness behavior, CSP behavior, static asset allowlist behavior, dependencies, scripts, tests, or frontend tooling.

## Inputs Reviewed

Reviewed implementation and validation surfaces:

- `scripts/check_kora_studio_browser_csp.py`
- `scripts/check_kora_studio_browser_csp_ci_optional.sh`
- `tests/test_kora_studio_browser_csp_smoke.py`
- `docs/kora-studio/kora-studio-v4-0-manual-browser-keyboard-traversal-report.md`

The existing optional browser CSP smoke already uses transient `npx --package @playwright/test`, is explicitly gated, and validates root load, CSP, local CSS/JS assets, and Run Local Harness browser interaction.

## Decision Rationale

Manual-only remains appropriate for v4.1 because:

- the current browser smoke validates the highest-risk browser runtime path under CSP without adding persistent dependencies
- full keyboard traversal has viewport-sensitive behavior, especially for the mobile left rail
- adding Tab-order assertions before a precise expected focus sequence is agreed could create brittle smoke coverage
- no blocker was found in the v4.0 manual traversal report
- current dependency-light tests already guard the static accessibility contracts: labels, `aria-current`, `aria-pressed`, `aria-expanded`, `aria-hidden`, `inert`, and live-region markers

This avoids broadening the maintenance surface while keeping the current optional browser smoke useful.

## Rejected for Now

Do not add yet:

- a new `scripts/check_kora_studio_browser_keyboard.py`
- a new CI-optional shell wrapper
- a Playwright config file
- axe tooling
- package manifests or lockfiles
- persistent frontend dependencies
- default pytest/browser coupling

## Future Acceptance Criteria

An optional browser keyboard smoke becomes appropriate when all of these are true:

- the expected desktop focus sequence is documented as a stable list of selectors
- the expected narrow/mobile focus sequence is documented separately
- the smoke remains explicitly opt-in through an environment variable
- the smoke reuses transient `npx --package @playwright/test`
- no package manifest, lockfile, Playwright config, axe tooling, or frontend build tooling is added
- assertions stay bounded to primary path signals:
  - initial shell focusable controls
  - approved request selection through keyboard activation
  - Run Local Harness activation through keyboard
  - details drawer open, focus transfer, Escape close, and focus return
  - mobile rail open, focus transfer, Escape close, and focus return
  - no hidden closed drawer or hidden mobile rail controls in the reachable focus path
- failure output stays concise enough for optional smoke triage

## Candidate Future Smoke Shape

If implemented later, the optional smoke should stay outside the default validation path:

```bash
KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 scripts/check_kora_studio_browser_keyboard_ci_optional.sh
```

Candidate checks:

- launch local Studio server in the wrapper
- open `http://127.0.0.1:<port>/`
- wait for `window.koraStudioScriptStatus.status === "ready"`
- press Tab through topbar controls and primary action controls
- press Enter/Space on one approved request
- press Enter/Space on Run Local Harness
- open Details, assert focus reaches close button, press Escape, assert focus returns
- set a narrow viewport, open Menu, assert focus reaches close button, press Escape, assert focus returns
- fail on page errors, CSP violations, or same-origin request failures

## Claim Boundary Check

- KORA Studio remains local preview/demo readiness only.
- This is optional browser keyboard smoke feasibility only.
- KORA Studio is not production-ready.
- KORA Studio is not production accessibility certification.
- KORA Studio is not an LM Studio replacement.
- No arbitrary prompt execution was added.
- No real model execution was added.
- No provider calls were added.
- No model downloads were added.
- No cloud sync was added.
- No private model directory scanning was added.
- No runtime model list commands were added.
- No report export or file writing was added.
- No production telemetry, production cost evidence, cost reduction claim, or energy outcome claim was added.

## Validation Results

Required validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: 71 passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: 4 passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: 5 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 153 passed, 143 deselected
- `python3 -m pytest`: 296 passed

Optional validation:

- `python3 scripts/check_kora_studio_preview.py`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed against the local Studio server

## Next Recommended Goal

Goal 541G - KORA Studio Optional Browser Keyboard Smoke Selector Contract.

The next goal should document the exact stable selector sequence for desktop and narrow/mobile keyboard traversal before any optional browser keyboard smoke script is added.
