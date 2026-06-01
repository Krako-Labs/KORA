# KORA Studio v2.0 JavaScript Asset Migration Decision Report

## Decision

KORA Studio v2.0 migrates the local preview interaction JavaScript to a package-controlled first-party source file and serves it through a single allowlisted JavaScript route:

```text
/studio-assets/studio.js
```

This is safe for v2.0 because the existing local asset namespace already has explicit path rejection, no directory listing, no wildcard serving, and no arbitrary filesystem lookup. v2.0 extends that boundary to exactly two approved assets:

- `/studio-assets/studio.css`
- `/studio-assets/studio.js`

## Source Location

JavaScript source:

```text
kora/studio_assets/studio.js
```

The server-facing helper remains:

```text
render_studio_javascript()
```

The helper loads the package-controlled source file. The HTTP route does not serve user-provided paths and does not serve from the project root.

## Risk Assessment

Route allowlist scope:

- approved: `studio.css`, `studio.js`
- rejected: unknown assets, directories, traversal, encoded traversal, double-encoded traversal, backslash traversal, and absolute-path shaped requests
- no wildcard route added

MIME behavior:

- CSS: `text/css; charset=utf-8`
- JavaScript: `application/javascript; charset=utf-8`

Cache behavior:

- both local preview assets keep `Cache-Control: no-store`
- this avoids stale local-preview behavior while the Studio shell is still changing frequently

CSP and future security:

- moving the interaction script out of inline HTML is a safer future CSP direction
- v2.0 does not add a CSP header yet because that needs a separate review of the remaining inline approved request JSON payload

Local preview simplicity:

- no frontend build tooling
- no bundler
- no minifier
- no npm workflow
- no external assets or CDN

Testability:

- the JavaScript source file can be checked directly
- the route can be checked independently for MIME, cache, and content markers
- the root preview can be checked for the script reference without embedding the interaction script body

Package data handling:

- `pyproject.toml` includes both CSS and JavaScript Studio assets as package data

## Implemented Surface

- `GET /studio-assets/studio.css`
- `GET /studio-assets/studio.js`
- root preview references both local package assets
- approved request JSON remains inline as `type="application/json"`
- no JavaScript static wildcard serving
- no arbitrary filesystem serving
- no directory listing

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

Future static asset changes should remain separate goals and should require:

- explicit asset allowlist updates
- MIME and cache tests
- traversal and unknown asset rejection tests
- smoke coverage for every new asset route
- no broad static directory serving
- no external asset, CDN, bundler, or dependency introduction without a separate design review

## Next Recommended Goal

Goal 520G — KORA Studio v2.1 Local Asset CSP Readiness Review.

Recommended scope:

- review the root preview for a future local-only Content Security Policy
- decide how to handle the remaining inline approved request JSON payload
- preserve local asset allowlists and route behavior
- avoid product behavior changes
