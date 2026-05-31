# KORA Studio v1.3 Static Asset Serving Tradeoff

## Status

Task 493 tradeoff note for KORA Studio v1.3 local frontend extraction hardening.

Static asset serving is not implemented in v1.3. The current local preview keeps CSS and JavaScript inline through render helpers:

- `kora/studio_style_render.py` provides `render_studio_css()`
- `kora/studio_script_render.py` provides `render_studio_javascript()`
- `kora/studio_server.py` embeds those strings into the single local preview HTML response

This document is a planning and boundary reference only. It does not add static routes, external assets, frontend build tooling, dependencies, provider calls, model execution, model downloads, cloud sync, report export, file writing, private directory scanning, runtime model listing, external network behavior, or production claims.

## Decision for v1.3

Keep CSS and JavaScript inline for v1.3.

Reason:

- the local preview is still a localhost-only demo/readiness surface
- current smoke checks can validate one HTML response without asset fetch failures
- inline helpers preserve the render-only contract established in Task 492
- no static route cache behavior needs to be tested yet
- no frontend build tool or dependency is required
- no external CDN or asset URL can accidentally enter the local preview runtime path

This is a maintainability decision, not a product capability claim.

## Current Inline Helper Path

Current flow:

1. `kora/studio_server.py` assembles local status and display values.
2. `render_studio_css()` returns the inline CSS string.
3. `render_studio_javascript()` returns the inline vanilla JavaScript string.
4. `render_studio_placeholder_html()` embeds both strings directly into the `/` response.
5. Smoke tests verify component markers and local-only boundaries from the rendered HTML.

Current constraints:

- no external `<script src>` is used by the runtime preview
- no external stylesheet is used by the runtime preview
- no CDN is used by the runtime preview
- no static asset route is required to render the preview
- no asset file is read by the render helpers
- local harness interactions remain limited to existing localhost endpoints

## Future Static Asset Serving Option

Static asset serving could be considered later if the local preview grows beyond the maintainability limits of inline helpers.

Potential future shape:

- local-only static route such as `/static/studio.css`
- local-only static route such as `/static/studio.js`
- files committed inside the repository
- no CDN or external URL
- no frontend build step unless explicitly approved later
- no generated or user-provided asset paths
- no arbitrary file serving
- content type and cache headers covered by tests

This option must remain local-only and must not be connected to provider calls, model execution, model downloads, cloud sync, report export, or external network behavior.

## Benefits of Staying Inline

| Benefit | Why it matters for v1.3 |
|---|---|
| Single response smoke check | `/` can prove the shell, markers, boundaries, CSS, and JavaScript are present without extra asset requests |
| No static route attack surface | there is no new path normalization, file lookup, MIME, or cache behavior to secure |
| No dependency or build step | local preview remains standard-library friendly |
| Stronger local-only boundary | no external asset URL, CDN, or remote font path is needed |
| Simpler render-helper contract | CSS and JavaScript helpers remain pure string renderers |
| Lower regression risk | current tests already cover inline helper output and forbidden endpoint strings |

## Costs of Staying Inline

| Cost | v1.3 mitigation |
|---|---|
| Large HTML response | acceptable for local preview/demo readiness |
| Harder CSS/JS editor ergonomics | helper files isolate CSS and JavaScript enough for current scope |
| No browser asset caching | not important for the local preview milestone |
| No separate static asset validation | keep testing inline helper output and rendered page markers |
| Potential future merge conflicts | continue extracting unrelated HTML fragments into small render helpers first |

## Future Static Asset Requirements

If a later task implements static asset serving, it must include:

- explicit user/task approval for implementation
- local-only route whitelist
- no arbitrary path loading
- no directory listing
- no private directory scanning
- no CDN or remote asset URL
- no dependency installation unless explicitly approved
- content type tests for CSS and JavaScript assets
- missing asset tests
- smoke check updates that fail on missing assets
- no provider/model/download/cloud/report export behavior
- no production readiness, cost, energy, or unsupported larger-model claims

## Test Expectations

While v1.3 keeps assets inline, tests should continue to verify:

- `render_studio_css()` returns CSS without `<script>` tags or external URLs
- `render_studio_javascript()` uses only approved local harness endpoints
- preview HTML includes the inline `<style>` and `<script>` sections
- preview HTML does not include external script sources
- preview HTML does not include external stylesheet sources
- preview HTML does not include CDN references
- smoke checks still cover `/health`, `/status`, `/`, local harness run, run retrieval, events, and generated SSE

## Claim Boundaries

The static asset decision preserves:

- local deterministic harness output only
- no arbitrary prompt execution
- no model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report export
- no file writing
- no external static assets or CDN
- no frontend framework migration
- no dependency addition
- not production-ready
- not production telemetry
- not production cost evidence
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement
