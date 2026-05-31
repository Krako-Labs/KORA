# KORA Studio v1.3 Render Helper API Contracts

## Status

Task 492 API contract reference for KORA Studio v1.3 local frontend extraction hardening.

This document defines the render-helper contracts that protect the local preview while helper extraction continues. It is a maintainability reference only. It does not add product behavior, static asset serving, frontend framework tooling, model execution, provider calls, downloads, cloud sync, report export, file writing, private directory scanning, runtime model listing, external network behavior, or production claims.

## Contract Summary

KORA Studio render helpers are string renderers.

They may:

- accept server-prepared display values
- accept named HTML slot strings where a helper explicitly owns a slot boundary
- return deterministic HTML, CSS, or JavaScript strings
- preserve stable ids and `data-kora-component` markers
- preserve local-only claim copy for the component they render

They must not:

- call providers or remote APIs
- open network connections
- start or stop servers
- read or write files
- write reports or exports
- download or execute models
- scan private model directories
- run runtime model list commands
- mutate backend/global state
- introduce external CSS, JavaScript, images, CDNs, or frontend framework tooling

`kora/studio_server.py` remains the data assembly and endpoint routing boundary.

## Helper Contract Table

| Helper | Input contract | Output contract | Slot contract | Boundary |
|---|---|---|---|---|
| `render_shell_layout()` | server-prepared display strings and slot HTML | shell HTML string | model selector item slot, composer slot, details drawer slot, legacy preview slot | shell only; no runtime/model/provider behavior |
| `render_right_details_drawer()` | server-prepared display strings | drawer HTML string | none | diagnostics only; no runtime probing |
| `render_selected_run_summary_panel()` | server-prepared selected request id | selected-run summary HTML string | none | approved local harness request only |
| `render_selected_run_state_panel()` | none | selected-run state container HTML string | none | generated local harness state only |
| `render_selected_run_detail_panels()` | none | selected timeline/counter/comparison/report container HTML string | none | generated local harness output only |
| `render_selected_run_panels()` | none | combined selected-run helper HTML string | none | helper test surface only |
| `render_endpoint_panel()` | none | endpoint reference HTML string | none | local endpoints only |
| `render_limitations_panel()` | none | limitation reference HTML string | none | claim-safe limitation copy only |
| `render_local_references_panel()` | escaped docs and fixtures display paths | local reference HTML string | none | display-only local paths |
| `render_reference_panels()` | escaped docs and fixtures display paths | combined reference HTML string | none | static reference panels only |
| `render_studio_css()` | none | inline CSS string | none | no external CSS path or CDN |
| `render_studio_javascript()` | none | inline vanilla JavaScript string | none | local harness endpoints only |

Task 493 keeps this inline CSS/JavaScript helper path as the v1.3 decision. See [KORA Studio v1.3 static asset serving tradeoff](kora-studio-v1-3-static-asset-serving-tradeoff.md).

## Signature Rules

Render helper signatures should remain simple and explicit:

- return annotation is `str`
- parameters are keyword-only where arguments are required
- parameter annotations are primitive display types such as `str` or `int`
- helpers with no required data accept no parameters
- no helper accepts raw status payload dictionaries by default
- no helper accepts arbitrary user prompt text

Future helpers may use structured types only after a task documents the data boundary and adds tests for escaping, markers, and local-only claims.

## Escaping Rules

The current v1.3 default is:

- `kora/studio_server.py` prepares and escapes display values before passing them into render helpers.
- Helpers may render those values directly only when the helper contract says the values are display-ready.
- Slot HTML arguments are trusted only when produced by existing local render helpers or server-owned escaped assembly.
- Render helpers should not parse or transform raw status payloads.

## Test Coverage

Task 492 adds helper contract tests that verify:

- helper return annotations remain string-based
- helper parameters remain explicit and keyword-only
- render helper modules do not import or call filesystem, network, subprocess, server, or browser launch dependencies
- existing marker and claim-boundary tests still pass
- full preview and smoke marker coverage remain intact

These tests are guardrails for maintainability. They are not product behavior claims.

## Claim Boundaries

The render-helper contract preserves:

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
- not production-ready
- not production telemetry
- not production cost evidence
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement
