# KORA Studio v2.1 Local Asset CSP Readiness Report

## Decision

KORA Studio v2.1 adds a minimal enforced Content Security Policy header to the root local preview HTML response only.

This is a local preview readiness step. It is not a production security readiness claim.

## Implemented CSP

The root Studio HTML response now includes:

```text
Content-Security-Policy: default-src 'none'; base-uri 'none'; object-src 'none'; frame-ancestors 'none'; form-action 'none'; style-src 'self'; script-src 'self'; connect-src 'self'
```

The policy is intentionally narrow:

- `style-src 'self'` allows the package-controlled `/studio-assets/studio.css`
- `script-src 'self'` allows the package-controlled `/studio-assets/studio.js`
- `connect-src 'self'` allows existing local fetch and generated-event SSE calls
- `default-src 'none'` denies unspecified resource types
- `base-uri 'none'`, `object-src 'none'`, `frame-ancestors 'none'`, and `form-action 'none'` keep the local preview surface narrow

The policy does not include:

- external hosts
- broad wildcards
- `unsafe-inline`
- `unsafe-eval`
- nonces
- hashes
- CDN allowances

## Route Scope

The CSP header is added only to:

- `GET /`

The CSP header is not added to:

- `/health`
- `/status`
- `/api/harness/run`
- `/api/harness/run/<run_id>`
- `/api/harness/events`
- `/api/harness/sse`
- `/studio-assets/studio.css`
- `/studio-assets/studio.js`

## Approved Request JSON

The approved request payload remains inline in the root HTML as:

```html
<script type="application/json" id="kora-approved-requests-data">...</script>
```

The executable interaction script remains external and package-controlled:

```html
<script src="/studio-assets/studio.js"></script>
```

v2.1 does not add nonce or hash handling because the current root preview can keep executable JavaScript outside the HTML document without adding that machinery.

## Validation Results

Final validation for this goal:

- `git diff --check`: passed
- `python3 -m pytest tests/test_kora_studio_server.py`: passed
- `python3 -m pytest tests/test_kora_studio_preview_smoke.py`: passed
- `python3 -m pytest tests -k "studio or sse or execution or harness"`: passed
- `python3 -m pytest`: passed

Live smoke check:

- `python3 -m kora studio --no-browser`: started local preview server
- `python3 scripts/check_kora_studio_preview.py`: passed
- server stopped cleanly

## Claim Boundaries Preserved

- KORA Studio remains local preview/demo readiness only.
- KORA Studio is not production-ready.
- KORA Studio does not claim production security readiness.
- KORA Studio is not an LM Studio replacement.
- Generated harness data remains local deterministic preview data.
- No arbitrary prompt execution was added.
- No model execution was added.
- No provider calls were added.
- No model downloads were added.
- No cloud sync was added.
- No private model directory scanning was added.
- No runtime model list commands were added.
- No report export or file writing was added.
- No external network behavior was added.
- No external assets or CDN dependencies were added.
- No production telemetry claim was added.
- No production cost evidence claim was added.
- No production cost reduction claim was added.
- No energy outcome claim was added.
- No unsupported larger-model execution claim was added.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.

## Follow-Up Criteria

Future CSP changes should remain separate goals and should require:

- browser-level validation of CSP behavior
- explicit review of any new inline data blocks
- explicit review of any new resource type such as images, fonts, workers, frames, or media
- no broad wildcard source allowances
- no external host allowances unless separately justified and documented

## Next Recommended Goal

Goal 521G — KORA Studio v2.2 Browser-Level CSP Smoke Validation.

Recommended scope:

- add a browser-level local preview check for CSP console violations
- preserve local asset allowlists and route behavior
- avoid production security readiness claims
- avoid product behavior changes
