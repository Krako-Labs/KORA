# KORA Studio v1.8 Static Asset Allowlist Test Plan

## Status and Goal

This started as a design and test plan for a future CSS-only local static asset route. Goal 517G implements the planned CSS-only route after this plan defined the allowlist and rejection boundary.

The goal is to define the allowlist, rejection rules, MIME/header behavior, security boundary, and test coverage required before KORA Studio can safely serve a first-party local CSS asset from the localhost-only Studio preview server.

This document remains the reference boundary for the CSS-only static route. It does not approve JavaScript static serving, dependencies, frontend framework tooling, external assets or CDNs, product behavior changes, or model/provider/download/cloud/report boundary changes.

## Proposed First Asset

Future first asset:

- route: `/studio-assets/studio.css`
- source: CSS currently emitted by `render_studio_css()`
- MIME: `text/css`
- scope: local preview style only
- serving boundary: existing localhost-only KORA Studio server
- JavaScript asset: not included in the first implementation

The first implementation should prove the static route boundary with CSS only. JavaScript should remain inline through `render_studio_javascript()` until the CSS route is implemented, tested, and smoke-checked.

## Allowlist

The future route must use an explicit allowlist:

```text
/studio-assets/studio.css
```

Allowed asset key:

```text
studio.css
```

Disallowed:

- wildcard matching
- directory listing
- arbitrary path lookup
- user-provided file lookup
- query-selected filenames
- serving by filesystem path
- serving by project-relative path
- serving unknown extensions
- serving JavaScript in the first implementation

The server should map the route to the allowlisted asset key directly. It should not construct a filesystem path from untrusted request text.

## Rejection Rules

A future implementation must reject:

- `..`
- encoded traversal such as `%2e%2e`
- double-encoded traversal
- absolute paths
- backslash traversal such as `..\\`
- mixed slash/backslash traversal
- query-driven file selection such as `?file=studio.css`
- unknown asset names
- unknown extensions
- directory paths
- project-root paths
- private file paths
- home directory paths
- temporary directory paths
- model directory paths
- report directory paths
- upload paths

Acceptable responses for rejected paths:

- `400` for malformed or traversal-shaped paths
- `404` for unknown but non-sensitive paths

Responses must not include stack traces, local filesystem paths, environment values, private path hints, or implementation details that would make filesystem probing easier.

## MIME and Headers

Expected future behavior for `/studio-assets/studio.css`:

- status: `200`
- `Content-Type`: `text/css; charset=utf-8`
- `Cache-Control`: `no-store`
- content sniffing: do not rely on browser sniffing
- serving boundary: localhost-only
- external network fetch: none
- CDN: none

Do not infer MIME types from arbitrary request extensions. The MIME type should come from the allowlisted asset key.

The first implementation should not add `studio.js`, fonts, images, source maps, or generated report files to the static asset map.

## Security Boundary

The future route must:

- serve only generated or packaged known assets
- serve only from a narrow first-party Studio asset boundary
- never serve from the project root broadly
- never serve user uploads
- never inspect private directories
- never expose local filesystem paths in responses
- never serve model files
- never serve reports or report exports
- never serve environment files
- never use external network fetches
- never proxy remote assets
- never introduce provider calls, model execution, downloads, cloud sync, or report writing

The implementation should be easier to audit than a general static file server. A single-asset allowlist is preferred for the first route.

## Test Plan

Future unit tests should cover:

- allowed CSS path returns `200`
- allowed CSS path returns `text/css; charset=utf-8`
- allowed CSS path returns `Cache-Control: no-store`
- allowed CSS response contains expected Studio CSS marker text
- unknown asset returns `404`
- `/studio-assets/` returns no directory listing
- `/studio-assets` returns no directory listing
- traversal paths return `400` or `404`
- encoded traversal is rejected
- absolute paths are rejected
- backslash traversal is rejected
- query-driven file selection is rejected or ignored
- directory paths are rejected
- project-root paths are rejected
- response body does not expose local filesystem paths
- no JavaScript asset is served in the first implementation
- no external script, stylesheet, font, image, or CDN reference is introduced

Future rendered-preview tests should cover:

- preview HTML references only `/studio-assets/studio.css` if external CSS is enabled later
- preview HTML does not reference external CSS
- preview HTML does not reference CDN assets
- preview HTML keeps JavaScript inline until a later approved task
- preview HTML preserves v1.0 shell-first markers
- preview HTML preserves v1.1 shell-only markers
- preview HTML preserves v1.2 component markers
- preview HTML preserves claim-boundary text
- preview HTML preserves local harness endpoints and selected-run UI markers

Future smoke checks should cover:

- `/health` unchanged
- `/status` unchanged
- `/` unchanged except for the approved local CSS reference if external CSS is enabled
- `/api/harness/run` unchanged
- `/api/harness/run/<run_id>` unchanged
- `/api/harness/events?run_id=<id>` unchanged
- `/api/harness/sse?run_id=<id>` unchanged
- `/studio-assets/studio.css` returns `200` and `text/css` only after the implementation exists
- traversal and unknown asset probes fail without exposing private details

Current inline behavior remains the baseline until implementation. Task 516 does not require new route tests because no route is added.

## Migration Plan

Conservative migration sequence:

1. Keep inline CSS as the source of truth.
2. Add static route behind tests in a future approved implementation task.
3. Optionally make the preview reference `/studio-assets/studio.css` only after the route passes allowlist, rejection, MIME, cache, endpoint preservation, and smoke marker tests.
4. Keep JavaScript inline.
5. Preserve a fallback plan if the CSS route fails.

Fallback expectations:

- root preview still returns HTML
- no provider calls
- no model execution
- no downloads
- no cloud sync
- no report export
- no external network fetches
- claim boundary text remains visible in HTML

## Non-goals

Task 516 does not include:

- JavaScript static serving
- frontend framework migration
- external static assets
- CDN usage
- dependency installation
- product behavior changes
- endpoint behavior changes
- UI behavior changes
- model execution
- provider calls
- model downloads
- cloud sync
- report export or file writing
- private model directory scanning
- runtime model listing
- external network behavior
- production claims

## Claim Boundaries

Any future static asset work must preserve:

- KORA Studio remains local preview/demo readiness only.
- KORA Studio is not production-ready.
- KORA Studio is not an LM Studio replacement.
- Generated harness data remains local deterministic preview data.
- No arbitrary prompt execution.
- No real model execution.
- No provider calls.
- No model downloads.
- No cloud sync.
- No private model directory scanning.
- No runtime model list commands.
- No report export or file writing.
- No external network behavior.
- No external assets or CDN dependencies.
- No production telemetry claim.
- No production cost evidence claim.
- No production cost reduction claim.
- No energy outcome claim.
- No unsupported larger-model execution claim.
- KORA does not remove RAM, VRAM, unified-memory, or model-loading requirements.
