# KORA Studio v1.1 Shell Diagnostics Coverage Map

## Status

This map documents the current v1.1 shell-only hardening coverage before additional UI changes.

It identifies which diagnostics are already available through the final shell or right drawer, which content remains available only in the collapsed legacy compatibility scaffold, and what must be hardened before the legacy scaffold can be reduced further.

v1.1 remains local preview/demo readiness only, not production readiness.

## Coverage Goal

The v1.1 goal is for normal local preview inspection to rely on:

- final minimal shell
- compact model selector
- approved local harness composer path
- right details drawer
- shell-visible selected-run state
- shell-visible local-only boundaries

The collapsed legacy detailed preview should remain a compatibility/developer scaffold only.

## Current Shell And Drawer Evidence

Current smoke-checkable shell/drawer markers include:

- `data-kora-v1-preview-readiness="shell-first-boundary-consolidation"`
- `data-kora-v1-shell-local-only-status="visible"`
- `data-kora-shell-local-only-boundary="v1.0"`
- `data-kora-shell-boundary-coverage="provider,cloud,download,model-execution,report-export"`
- `data-kora-shell-selected-run-surface="v1.0"`
- `data-kora-shell-selected-run-coverage="timeline,counters,comparison,report-metadata"`
- `data-kora-drawer-selected-run-coverage="timeline,counters,comparison,report-metadata"`
- `data-kora-drawer-boundary-coverage="provider,cloud,download,model-execution,report-export,private-scan,runtime-list"`
- `data-kora-legacy-preview-mode="compatibility-collapsed"`
- `data-kora-legacy-preview-default="collapsed"`
- `data-kora-legacy-preview-role="developer-compatibility-scaffold"`

These markers are covered by the local preview smoke check and server tests.

## Diagnostics Coverage Matrix

| Diagnostic area | Shell coverage | Drawer coverage | Legacy scaffold role | v1.1 hardening need |
|---|---|---|---|---|
| Local preview status | Boundary pills and shell boundary strip | Claim boundaries section | Reference only | Add v1.1-specific shell-only marker in Task 484. |
| Provider disabled state | Shell boundary strip | Claim boundaries section | Reference only | Covered; keep visible in shell/drawer. |
| Cloud sync disabled state | Shell boundary strip | Claim boundaries section | Reference only | Covered; keep visible in shell/drawer. |
| Download disabled state | Shell boundary strip | Claim boundaries section | Reference only | Covered; keep visible in shell/drawer. |
| Model execution not connected | Shell boundary strip and composer copy | Runtime status and claim boundaries | Reference only | Covered; keep wording concise and visible. |
| Report export/write disabled | Shell boundary strip | Report metadata and claim boundaries | Reference only | Covered; polish selected-run report status in Task 483 if needed. |
| Catalog-estimate model selector | Compact top selector | Selected model and catalog vs installed sections | Reference only | Covered; keep catalog examples distinct from installed models. |
| Runtime status | Not primary shell content | Runtime status section | Reference only | Covered in drawer; do not move dense runtime details into shell. |
| Catalog vs installed distinction | Top selector boundary | Catalog vs installed section | Reference only | Covered; keep installed detection claim-safe. |
| Approved harness request path | Composer action and selected request summary | Route trace section | Reference only | Covered; no arbitrary prompt input. |
| Selected run summary | Composer selected-run summary | Selected-run surfaces section | Reference only | Covered; Task 483 should polish state copy. |
| Event timeline availability | Selected-run detail strip | Selected-run surfaces section | Detailed fallback remains in legacy scaffold | Partially covered; Task 483 should make selected timeline state clearer in drawer. |
| Generated counters availability | Selected-run detail strip | Generated counters and selected-run surfaces sections | Detailed fallback remains in legacy scaffold | Covered, with polish opportunity. |
| Standard Mode vs KORA Boost comparison | Selected-run detail strip | Selected-run surfaces section | Detailed fallback remains in legacy scaffold | Partially covered; Task 483 should make comparison availability clearer. |
| Report metadata preview | Selected-run detail strip | Report metadata and selected-run surfaces sections | Detailed fallback remains in legacy scaffold | Covered, with polish opportunity for file export/write state. |
| Claim boundaries | Shell boundary strip | Claim boundaries section | Reference only | Covered; Task 484 should assert v1.1 shell-only marker. |
| Endpoint reference | Not a normal shell need | Not primary drawer need | Developer reference | Keep in legacy scaffold until separate developer docs cover it. |
| Long limitations/reference content | Not a normal shell need | Claim boundaries summarize critical parts | Developer reference | Keep secondary and collapsed. |

## Legacy-only Or Legacy-heavy Content

The following areas still rely on the collapsed legacy scaffold for dense details or contributor reference:

- endpoint reference panel
- long-form limitation/reference copy
- detailed static harness cards
- detailed generated event cards
- detailed report metadata cards

These are not required for normal first-run local preview inspection, but they remain useful as compatibility and contributor reference surfaces.

Before removal, v1.1 should ensure equivalent shell/drawer summaries or docs links cover any information that users need in the primary preview flow.

## Required Shell/Drawer Destinations Before Further Legacy Reduction

Before the legacy scaffold is reduced further or removed, the shell/drawer must continue to provide:

- local preview/demo status
- selected catalog estimate boundary
- catalog examples are not installed models
- approved request-only composer behavior
- selected run id and run status
- timeline/counters/comparison/report metadata availability
- provider calls disabled
- cloud sync disabled
- downloads disabled
- model execution not connected
- report export/write disabled
- no private model directory scanning
- no runtime model list commands
- not production telemetry
- not production cost evidence

## Task 482 Inputs

Task 482 should use this map to tighten the legacy scaffold while preserving safe reference coverage.

Recommended Task 482 checks:

- legacy scaffold remains collapsed by default
- legacy scaffold label says compatibility/developer scaffold
- shell/drawer coverage is not weakened
- no legacy content becomes the primary first-run experience
- no provider/model/download/cloud/report export behavior is introduced

## Task 483 Inputs

Task 483 should polish selected-run shell/drawer state where this map marks partial coverage:

- timeline availability
- comparison availability
- report metadata preview and file export/write boundary
- generated local harness output boundary
- not production telemetry/cost evidence wording

## Task 484 Inputs

Task 484 should expand smoke checks for:

- v1.1 shell-only hardening marker
- drawer diagnostics coverage marker
- selected-run shell/drawer state coverage
- legacy secondary/collapsed marker
- legacy preview absence as primary `<main>` surface
- no arbitrary prompt input
- no enabled model run/download action
- no provider/cloud/report export behavior

## Claim Boundaries

This map preserves:

- local preview/demo readiness only
- approved local harness requests only
- generated local harness events only
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
- no production cost reduction claim
- no energy outcome claim
- no unsupported larger-model execution claim
- not an LM Studio replacement
