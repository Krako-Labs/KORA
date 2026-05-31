# KORA Studio v1.7 Static Asset Serving Plan

## Status and Goal

KORA Studio v1.7 is a planning and decision milestone for local static asset serving. It is not an implementation milestone.

The goal is to define how KORA Studio could later serve first-party CSS, JavaScript, or other local preview assets from a narrow localhost-only asset boundary while preserving the current local-only security posture, endpoint behavior, smoke markers, and claim boundaries.

This plan does not implement static asset serving, add routes, move CSS or JavaScript out of inline render helpers, add dependencies, add frontend framework tooling, add external assets/CDNs, alter UI behavior, alter endpoint behavior, or change model/provider/download/cloud/report boundaries.

## Current State

KORA Studio currently serves the local preview as server-rendered HTML from `kora/studio_server.py`.

Current asset behavior:

- CSS is rendered inline through `render_studio_css()` in `kora/studio_style_render.py`.
- JavaScript is rendered inline through `render_studio_javascript()` in `kora/studio_script_render.py`.
- `kora/studio_server.py` inserts the inline `<style>` and `<script>` blocks into the root preview document.
- There is no `/studio-assets/...` route or equivalent local static asset namespace.
- There is no external CSS, JavaScript, image, font, or CDN dependency.
- Current smoke markers and tests inspect the rendered preview and inline JavaScript behavior directly.
- Existing endpoint tests cover `/health`, `/status`, `/`, `/api/harness/run`, `/api/harness/run/<run_id>`, `/api/harness/events`, and `/api/harness/sse`.

This keeps the preview simple, dependency-free, and narrow. It also means CSS and JavaScript are stored as large Python string templates, which is acceptable for the current preview but harder to maintain as UI work grows.

## Problem

Inline CSS and JavaScript helpers are behavior-preserving and testable, but they are not ideal long-term editing surfaces. Normal asset files would be easier to review, format, and eventually migrate.

Static asset serving could improve source organization, but it introduces a new local server responsibility:

- request routing for static assets
- path validation
- MIME handling
- cache behavior
- allowlist decisions
- no-external-reference enforcement
- additional smoke coverage

The architecture should not add static asset serving casually. A narrow, tested plan is required before any implementation.

## Non-goals

v1.7 does not:

- implement static asset serving
- add `/studio-assets/...` or any other static route
- move CSS out of inline helper output
- move JavaScript out of inline helper output
- add external assets
- add CDN references
- add dependencies
- add frontend framework tooling
- change product behavior
- change UI behavior
- change endpoint behavior
- add arbitrary prompt execution
- add model execution
- add provider calls
- add model downloads
- add cloud sync
- add report export or file writing
- scan private model directories
- run runtime model list commands
- add external network behavior
- add production claims

## Static Asset Serving Requirements

A future implementation should meet these requirements before it serves any local asset.

### Route Namespace

Use a dedicated local route namespace such as:

```text
/studio-assets/...
```

The namespace should be reserved for first-party Studio preview assets only. It should not overlap with `/api/...`, `/health`, `/status`, `/`, or harness routes.

### Explicit Allowlist

Serve only known asset names from an explicit allowlist.

Initial candidate allowlist for a CSS-only implementation:

```text
studio.css
```

Later candidates, if separately approved:

```text
studio.js
```

The server should map request paths to allowlisted asset keys, not arbitrary filesystem paths.

### Filesystem Boundary

Future static assets should live under a narrow controlled directory such as:

```text
kora/studio_assets/
```

The route must not serve from the project root, user home directory, current working directory, temporary directories, model directories, report directories, or uploaded/user-controlled locations.

### Path Rejection

Reject:

- `..`
- encoded traversal such as `%2e%2e`
- absolute paths
- path separators inside asset names unless explicitly required later
- empty asset names
- directory paths
- query-driven file lookup
- user-provided filesystem paths

### Directory Listing

Directory listing must not exist. Requests for `/studio-assets/`, `/studio-assets`, or any directory-like path should return a claim-safe `404` or `403`.

### MIME Types

Use fixed MIME types based on the allowlisted asset key.

Expected first set:

- `studio.css`: `text/css; charset=utf-8`
- `studio.js`, if later approved: `application/javascript; charset=utf-8`

Do not infer MIME type from arbitrary extensions.

### Cache Behavior

For the first local implementation, prefer development-friendly cache behavior:

```text
Cache-Control: no-store
```

This avoids hiding changed local assets during preview development. A later production-oriented cache policy can be designed separately if KORA Studio moves beyond local preview readiness.

### Localhost Boundary

Static assets must be served only by the existing localhost-only KORA Studio server boundary. Asset serving must not create a remote server, public file server, tunnel, cloud sync, upload surface, or external network dependency.

### No External Network Fetch

The server must not fetch remote assets. The preview must not depend on remote CSS, JavaScript, fonts, icons, images, analytics, package CDNs, or provider endpoints.

### No User Asset Paths

Users must not be able to provide asset paths through request bodies, query strings, local storage, prompt text, headers, or UI controls.

### Smoke Markers

Existing smoke markers for shell, drawer, selected run, harness controls, generated events, counters, comparison, report metadata, and claim boundaries must remain visible after any future CSS-only migration.

If CSS becomes external, tests should still verify:

- the HTML references only the local asset path
- the local CSS endpoint responds
- no external asset reference appears in the HTML
- the local preview remains readable if CSS fails to load

### Fallback Behavior

If a local CSS asset fails to load, the server should still return the root HTML document. The failure should not trigger provider calls, model execution, downloads, cloud sync, report export, or external fetches.

JavaScript should remain inline until the CSS route has been implemented and validated. If JavaScript is later moved, the preview should preserve claim-safe unavailable states and avoid silently enabling unsupported behavior.

## Security Boundary

A future static asset implementation must preserve these security constraints:

- reject `..`
- reject encoded traversal
- reject absolute paths
- reject backslash traversal
- reject directory requests
- reject unknown asset names
- reject query-driven file lookup unless explicitly required and tested
- do not serve private files
- do not serve from the project root broadly
- do not serve user uploads
- do not serve generated reports
- do not serve model files
- do not serve environment files
- do not serve arbitrary local files
- do not use external network fetches
- do not expose directory listings

The static asset root must be narrow, controlled, and first-party. It should contain only reviewed Studio preview assets.

## Testing Plan

Before implementation, tests should be planned for:

- allowed asset name returns expected content
- unknown asset returns `404`
- `/studio-assets/` returns no directory listing
- `../` traversal is rejected
- encoded traversal is rejected
- absolute path requests are rejected
- query-driven file lookup is ignored or rejected
- CSS response has `text/css; charset=utf-8`
- JavaScript response has `application/javascript; charset=utf-8` only if JS serving is later approved
- cache header is explicit
- no external assets/CDNs appear in root HTML
- existing `/health`, `/status`, `/`, and harness endpoints continue to work
- existing smoke markers remain visible
- current inline behavior remains unchanged until implementation

Future smoke check updates should verify the local asset endpoint only after static serving exists. v1.7 does not require smoke changes because it does not add a static route.

## Migration Options

### Option 1: Keep Inline Helpers Indefinitely

Maintainability:

- Simple for server behavior.
- Increasingly awkward for CSS and JavaScript editing.

Implementation risk:

- Lowest. No new route or file serving behavior.

Security risk:

- Lowest. No new file-serving surface.

Test burden:

- Current tests remain sufficient.

Local-only implications:

- Strongest local-only posture.

Suitability for v1.8:

- Acceptable if architecture risk outweighs maintainability needs.
- Not the preferred next step because CSS editing friction will keep growing.

### Option 2: Move Only CSS to a Local Static Asset

Maintainability:

- Improves styling iteration and review.
- Keeps JavaScript behavior close to current tested inline path.

Implementation risk:

- Moderate but narrow.
- Adds one static asset route and one MIME type.

Security risk:

- Manageable if allowlisted and traversal-tested.

Test burden:

- Requires asset route tests, no-external-reference tests, and smoke marker preservation tests.

Local-only implications:

- Good if served by the existing localhost-only server and narrow allowlist.

Suitability for v1.8:

- Recommended as the first implementation candidate if approved after this plan.

### Option 3: Move CSS and JavaScript to Local Static Assets

Maintainability:

- Best source organization for current server-rendered architecture.
- Makes CSS/JS easier to edit as normal files.

Implementation risk:

- Higher than CSS-only because JavaScript drives local harness interaction, selected-run state, event fetches, SSE fallback, retry, and run history behavior.

Security risk:

- Manageable with allowlist, but broader because script loading failures directly affect interaction behavior.

Test burden:

- Requires all CSS tests plus JavaScript route tests, HTML reference tests, interaction marker tests, and failure behavior checks.

Local-only implications:

- Still acceptable if first-party and localhost-only.

Suitability for v1.8:

- Not recommended as the first implementation step.
- Revisit only after CSS-only static serving is validated.

### Option 4: Defer Static Assets and Move Toward a Future Frontend App Later

Maintainability:

- Could eventually improve component boundaries more than static asset serving.

Implementation risk:

- High if attempted now.
- Introduces build tooling, dependency decisions, serving behavior, and broader validation requirements.

Security risk:

- Depends on tooling and asset pipeline.
- Higher than current dependency-free local preview.

Test burden:

- Requires frontend build validation, browser rendering checks, asset serving checks, and possibly CI changes.

Local-only implications:

- Can remain local-only, but the toolchain would need explicit no-external-runtime and no-CDN rules.

Suitability for v1.8:

- Not recommended.
- Frontend framework migration remains deferred until the static asset boundary is either implemented safely or explicitly rejected.

## Recommendation

Recommended path:

1. Keep v1.7 planning-only.
2. Use a future approved goal to implement a narrow CSS-only static asset route first.
3. Keep JavaScript inline until CSS static serving is implemented, tested, and smoke-checked.
4. Keep frontend framework migration deferred.
5. Resume product capability scaffolding only after the asset boundary is stable enough to avoid repeated local preview rewrites.

Expected next implementation candidate:

- Route namespace: `/studio-assets/studio.css`
- Asset source: narrow first-party local asset file
- Allowlist: `studio.css` only
- MIME: `text/css; charset=utf-8`
- Cache: `Cache-Control: no-store`
- No JavaScript migration yet
- No external assets or CDN references

## Task Breakdown

- Task 515: v1.7 static asset serving plan and cross-links.
- Task 516: [static asset allowlist/design tests planning](kora-studio-v1-8-static-asset-allowlist-test-plan.md).
- Task 517: optional CSS-only static asset route implementation if approved.
- Task 518: smoke check for CSS static route.
- Task 519: readiness/goal report.

## Claim Boundaries

Any static asset work must preserve:

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
