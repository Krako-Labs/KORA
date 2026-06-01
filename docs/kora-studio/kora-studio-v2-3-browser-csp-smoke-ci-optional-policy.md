# KORA Studio v2.3 Browser CSP Smoke CI-Optional Policy

## Decision

KORA Studio v2.3 keeps browser-level CSP smoke validation outside the default CI and pytest path, while adding an explicit CI-optional wrapper for environments that intentionally opt in.

The policy is CI-optional, not default CI:

- default GitHub CI continues to run release smoke and pytest only
- normal pytest does not require `npx`, Playwright, browser downloads, or network access
- the browser CSP smoke can be run in CI only when an environment explicitly sets `KORA_STUDIO_BROWSER_CSP_SMOKE=1`
- no persistent frontend dependency, package manifest, lockfile, bundler, npm workflow, or Playwright config is added

## CI-Optional Command

Script:

```text
scripts/check_kora_studio_browser_csp_ci_optional.sh
```

Explicit opt-in command:

```bash
KORA_STUDIO_BROWSER_CSP_SMOKE=1 scripts/check_kora_studio_browser_csp_ci_optional.sh
```

Without the opt-in variable, the script exits successfully after reporting that the optional browser smoke was skipped. This allows a CI job or local validation shell to include the script without making browser automation part of the default dependency-light path.

Optional environment variables:

- `KORA_STUDIO_BROWSER_CSP_PORT`: local preview port, default `8765`
- `KORA_STUDIO_BROWSER_CSP_BASE_URL`: local base URL, default `http://127.0.0.1:<port>`
- `KORA_STUDIO_BROWSER_CSP_TIMEOUT`: Playwright test timeout in milliseconds, default `20000`

## Runtime Behavior

When explicitly enabled, the wrapper:

- starts `python3 -m kora studio --no-browser` on a localhost port
- waits for `/health`
- runs `python3 scripts/check_kora_studio_browser_csp.py`
- stops the local server on exit

The underlying browser smoke still:

- accepts only `http://127.0.0.1` or `http://localhost`
- uses transient `npx --package @playwright/test`
- validates the root CSP header
- validates local CSS and JavaScript asset loading
- checks shell readiness and Run Local Harness interaction
- fails on browser CSP violations, page errors, or unexpected same-origin request failures

## Boundaries

This policy does not add:

- persistent Node dependencies
- a root `package.json`
- lockfiles
- Playwright config
- frontend build tooling
- bundlers or minifiers
- external assets or CDN usage
- default CI browser automation
- CSP broadening
- `unsafe-inline`
- `unsafe-eval`
- wildcard source allowances
- production security readiness claims

## Default Automated Coverage

The default automated path remains dependency-light:

- server/static-route/header tests stay in pytest
- preview HTTP smoke remains script-based and browser-free
- browser CSP script unit tests validate policy and invocation shape without launching a browser

## Claim Boundaries Preserved

- KORA Studio remains local preview/demo readiness only.
- This is browser-level CSP smoke validation only.
- KORA Studio is not production-ready.
- KORA Studio does not claim production security readiness.
- KORA Studio is not an LM Studio replacement.
- No arbitrary prompt execution was added.
- No model execution was added.
- No provider calls were added.
- No model downloads were added.
- No cloud sync was added.
- No private model directory scanning was added.
- No runtime model list commands were added.
- No report export or file writing was added.
- No production telemetry or production cost evidence claim was added.
- No production cost reduction claim was added.
- No energy outcome claim was added.
- No unsupported larger-model execution claim was added.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Next Recommended Goal

Goal 523G - KORA Studio CSP Resource-Type Regression Guard.

Recommended scope:

- add lightweight regression tests for future resource types such as images, fonts, workers, frames, and media
- keep CSP narrow
- preserve local-only route boundaries
- keep browser validation optional unless a future goal explicitly approves committed browser dependencies
