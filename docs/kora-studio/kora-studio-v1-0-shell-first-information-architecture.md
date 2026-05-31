# KORA Studio v1.0 Shell-First Information Architecture

## Status

This document maps the current local preview surfaces into the v1.0 shell-first target.

The goal is to reduce dependence on the detailed legacy preview while preserving all local-only claim boundaries.

v1.0 remains local preview/demo readiness only, not production readiness.

## Current Preview Structure

The current root preview has two major layers:

- final minimal shell: left mini rail, compact top model selector, centered composer, boundary pills, and right details drawer
- legacy detailed preview: long section stack below the shell with local status, system profile, model capability, runtime status, catalog vs installed, setup guidance, disabled actions, local harness, execution viewer, comparison, report viewer, endpoint panel, limitations, and references

The shell already contains the intended product shape. The legacy preview still carries too much first-run explanatory weight.

## v1.0 Target Structure

The v1.0 target is:

- shell is the primary preview surface
- right drawer is the primary detail surface
- legacy preview is compatibility scaffolding only
- a first-run user can understand local status, model/catalog boundaries, harness behavior, selected-run output, and disabled actions without scrolling to the legacy preview

## Shell Surface Map

| Current surface | v1.0 destination | Status | Notes |
|---|---|---|---|
| Left mini rail | Keep in shell | Already shell-first | Navigation only. It must not become a diagnostics dashboard. |
| Top model selector | Keep in shell | Already shell-first | Catalog-estimate-only. It must not imply installation, download, or execution. |
| Centered composer | Keep in shell | Already shell-first | Approved local harness request only. No arbitrary prompt execution. |
| Shell boundary pills | Expand in shell | Needs consolidation | Should cover local preview, provider disabled, cloud disabled, download disabled, and model execution not connected without relying on legacy preview. |
| Composer selected-run summary | Keep in shell | Already shell-first | Should remain compact and not replace detailed drawer inspection. |
| Selected-run timeline | Move/keep shell-adjacent or drawer | Partially duplicated | Interactive selected-run event timeline exists in legacy local harness section; v1.0 should surface selected-run timeline access through the shell or drawer. |
| Selected-run counters | Move/keep shell-adjacent or drawer | Partially duplicated | Selected counters exist in legacy section; drawer already has generated counters summary. |
| Selected-run comparison | Move/keep shell-adjacent or drawer | Partially duplicated | Selected comparison exists in legacy section; drawer should show comparison availability or summary. |
| Selected-run report metadata | Move/keep shell-adjacent or drawer | Partially duplicated | Selected report metadata exists in legacy section; drawer already has report metadata summary. |

## Right Drawer Map

The right drawer should become the main destination for dense local preview details.

| Detail area | v1.0 drawer role | Current coverage | Required v1.0 action |
|---|---|---|---|
| Runtime status | Primary detail | Present | Add clearer local-only status and model execution boundary if needed. |
| Selected model | Primary detail | Present | Keep catalog-only selected estimate boundary visible. |
| Catalog vs installed | Primary detail | Present | Keep installed detection disabled/not-connected copy visible. |
| Route trace | Primary detail | Present | Tie route trace to selected run where possible in later implementation tasks. |
| Generated counters | Primary detail | Present | Ensure counters are sufficient without legacy preview scrolling. |
| Standard Mode vs KORA Boost comparison | Primary detail | Partial | Drawer should expose comparison summary or link/anchor within shell-first UI. |
| Report metadata | Primary detail | Present | Keep file export disabled and file written false. |
| Claim boundaries | Primary detail | Present | Expand to include cloud sync, downloads, report export/write, private scans, runtime model list commands, and production evidence boundaries. |

## Legacy Preview Section Migration Map

| Legacy section | v1.0 destination | Priority | Rationale |
|---|---|---:|---|
| Launch / Local-only Status | Shell boundary strip and drawer claim boundaries | High | First-run users must see local-only status before any scroll. |
| Your Computer | Drawer or compatibility section | Medium | Useful context, but not primary chat/workspace UI. |
| Model Capability Estimate | Top selector and drawer | High | Model fit estimates must remain near selection. |
| Runtime Status | Drawer | High | Runtime and execution boundaries belong in details. |
| Catalog vs Installed | Top selector and drawer | High | Prevents catalog examples from being mistaken for installed models. |
| Setup Guidance | Compatibility section or drawer link | Medium | Informational only; should not dominate default shell. |
| Disabled Download/Run Actions | Shell boundary strip and drawer claim boundaries | High | Disabled status must be visible near risky actions. |
| KORA Boost Boundary | Composer copy and drawer comparison | Medium | Product narrative should be concise in shell, detailed in drawer. |
| Local Harness Preview | Composer and selected-run shell/drawer surfaces | High | This is the main local interactive path. |
| Execution Viewer | Drawer route trace and selected-run timeline | High | Event details should not require legacy scroll. |
| Standard Mode vs KORA Boost | Drawer comparison and selected-run comparison panel | High | Comparison must remain local harness output only. |
| Report Viewer Placeholder | Drawer report metadata and selected-run report metadata | High | Report metadata must keep no-export/no-write boundaries. |
| Endpoint Panel | Compatibility/developer section | Low | Developer reference, not first-run UI. |
| Limitations Panel | Drawer claim boundaries and compatibility section | Medium | Critical limitations should move to shell/drawer; long list can remain secondary. |
| Local References | Compatibility/developer section | Low | Contributor reference only. |

## Shell-First Readiness Markers

v1.0 implementation should add smoke-checkable markers for:

- shell-first preview readiness
- legacy preview compatibility mode
- shell local-only boundary coverage
- drawer detail coverage
- selected-run shell/drawer coverage
- no arbitrary prompt execution
- no model execution
- no provider calls
- no downloads
- no cloud sync
- no report export or report writing

These markers should not imply production readiness.

## Legacy Compatibility Policy

Until removal is safe, the legacy preview should be treated as compatibility scaffolding:

- clearly labelled as secondary or compatibility detail
- not required for first-run understanding
- not the primary place to inspect local-only boundaries
- not the primary place to inspect selected-run output
- preserved only while shell/drawer coverage is being completed

The compatibility section must keep the same claim boundaries as the shell.

## Claim Boundaries

The information architecture must preserve:

- local deterministic harness output only
- approved sample request IDs only
- generated events only
- no arbitrary prompt execution
- no real model execution
- no provider calls
- no model downloads
- no cloud sync
- no private model directory scanning
- no runtime model list commands
- no report file export
- no report file writing
- not production telemetry
- not production cost evidence
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement

## Implementation Sequence

Recommended sequence:

1. Add shell-first status and boundary coverage.
2. Add drawer detail coverage for selected-run timeline, counters, comparison, and report metadata.
3. Add v1.0 smoke markers for shell-first readiness.
4. Collapse or relabel the legacy preview as compatibility scaffolding.
5. Run readiness validation and publish v1.0 reports.

## Acceptance Criteria

Task 473 is complete when:

- the legacy section migration map exists
- each current legacy section has a shell, drawer, or compatibility destination
- required shell-first smoke markers are identified
- claim boundaries remain explicit
- public docs link to this map without claiming implementation is complete
