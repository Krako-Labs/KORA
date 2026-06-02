# KORA Studio v4.7 Optional Browser Smoke Documentation Consolidation

## Status

KORA Studio v4.7 consolidates optional browser smoke guidance into the main Studio README so contributors can distinguish default browser-free tests, optional preview smoke, optional browser CSP smoke, and optional browser keyboard smoke.

This is documentation-only. It does not change runtime behavior, backend routes, local harness behavior, CSP, static asset allowlist, dependencies, package manifests, lockfiles, Playwright config, axe tooling, frontend build tooling, external assets, or CDN.

## Consolidated Smoke Policy

Default validation remains dependency-light and browser-free. Normal pytest covers server behavior, root HTML, CSP directives, package CSS/JavaScript assets, `/studio-assets/...` allowlist behavior, resource guards, selector contracts, and optional wrapper/script opt-in behavior. It does not install browsers, invoke `npx`, or require Playwright.

Optional local smoke paths are intentionally separate:

| Smoke path | Command | Browser automation | Gate |
|---|---|---:|---|
| Preview smoke | `python3 scripts/check_kora_studio_preview.py` | no | none |
| Browser CSP smoke | `KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh` | yes, transient Playwright through `npx` | `KORA_STUDIO_BROWSER_CSP_SMOKE=1` |
| Browser keyboard smoke | `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 scripts/check_kora_studio_browser_keyboard_ci_optional.sh` | yes, transient Playwright through `npx` | `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1` |

## What Each Smoke Validates

Preview smoke validates localhost-only HTTP behavior against an already-running local Studio preview:

- `/health`
- `/status`
- root shell markers
- approved local harness endpoints
- generated event and SSE behavior
- local `/studio-assets/studio.css` and `/studio-assets/studio.js` routes

Browser CSP smoke validates browser/runtime resource behavior under the root CSP:

- root CSP header
- local CSS/JavaScript asset loading
- absence of browser CSP console violations, page errors, and same-origin request failures
- visible shell controls
- Run Local Harness browser interaction under `connect-src 'self'`

Browser keyboard smoke validates stable selector and focus-state behavior:

- v4.2 keyboard selector contract marker
- approved request selected state
- Run Local Harness keyboard activation
- progress and result summary visibility
- bounded retry state
- details drawer focus return
- narrow/mobile rail open, close, `aria-expanded`, `aria-hidden`, and focus-return behavior at 390 by 844

## What Remains Out of Scope

The optional smoke paths intentionally do not validate:

- exact full-page Tab order
- screen-reader announcement quality
- live-region spoken timing
- full visual responsive QA
- production accessibility certification
- production security readiness
- production readiness

Do not broaden these smoke paths into persistent frontend dependencies, package manifests, lockfiles, Playwright config, axe tooling, npm workflows, external hosts, external assets, or CDN without a separate reviewed change.

## When to Run

Run default pytest for normal Studio changes.

Run preview smoke after changing Studio server behavior, root shell markers, approved local harness endpoints, generated event/SSE behavior, or static asset routes.

Run browser CSP smoke after changing CSP, local CSS/JavaScript asset loading, root shell resource behavior, or browser-visible local fetch behavior.

Run browser keyboard smoke after changing selector contracts, primary controls, approved request state, Run Local Harness activation, retry state, details drawer focus behavior, or mobile rail open/close/focus behavior.

## Preserved Boundaries

- local preview/demo readiness only
- optional browser smoke documentation consolidation only
- not production-ready
- not production accessibility certification
- not an LM Studio replacement
- no arbitrary prompt execution
- no real model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report export or file writing
- not production telemetry or production cost evidence
- no cost reduction or energy outcome claim

## Validation Results

Required validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: 72 passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: 4 passed
- `python3 -m pytest tests/test_kora_studio_browser_csp_smoke.py`: 5 passed
- `python3 -m pytest tests/test_kora_studio_browser_keyboard_smoke.py`: 5 passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: 159 passed, 143 deselected
- `python3 -m pytest`: 302 passed

Optional validation:

- `python3 scripts/check_kora_studio_preview.py --base-url http://127.0.0.1:8768`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_CSP_SMOKE=1 KORA_STUDIO_BROWSER_CSP_PORT=8766 scripts/check_kora_studio_browser_csp_ci_optional.sh`: passed against the local Studio server
- `KORA_STUDIO_BROWSER_KEYBOARD_SMOKE=1 KORA_STUDIO_BROWSER_KEYBOARD_PORT=8767 scripts/check_kora_studio_browser_keyboard_ci_optional.sh`: passed against the local Studio server

## Next Recommended Goal

Goal 547G - KORA Studio Optional Browser Smoke Drift Guard Review.

The next goal should review whether a small dependency-light docs/script drift guard is useful for keeping README smoke commands aligned with the wrapper script names and opt-in environment variables.
