# KORA First Paper v0.10 Word-First Export Readiness Check

Status date: 2026-05-21

## Scope

This note checks whether manuscript v0.10 is ready for a later Word-first review-draft export. This task does not generate a Word file, PDF file, arXiv source package, archive, manuscript export package, or any other export artifact.

Reviewed sources:

- `docs/paper/kora-first-paper-manuscript-v0-10.md`
- `docs/paper/kora-first-paper-v0-10-figure-integration-delta.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/assets/paper/kora-first-paper-figure-1-v0-9-draft.svg`
- `docs/assets/paper/kora-first-paper-figure-1-v0-9-draft.png`
- `docs/assets/paper/kora-first-paper-figure-2-v0-9-draft.svg`
- `docs/assets/paper/kora-first-paper-figure-2-v0-9-draft.png`

## Readiness Summary

Manuscript v0.10 can proceed to a later Word-first review-draft export task, provided the export is explicitly labeled as a review draft and not as final publication layout. It is not ready for final Word, PDF, arXiv, archive, or submission-package export.

The main blockers are final bibliography/source-verification work, final figure layout approval, final Word layout inspection after export, and final claim-to-evidence review after any export or formatting changes.

## Manuscript Structure Readiness

The v0.10 manuscript has a complete working-draft structure for Word-first review:

- title and abstract
- introduction and positioning
- related work/background
- KORA execution model
- evaluation methodology
- results
- discussion/limitations
- reproducibility and artifact notes
- preliminary references
- claim-boundary note

The structure is sufficient for a review-draft Word export. It is not sufficient for final submission packaging because bibliography, final layout, final figure approval, and final export checks remain pending.

## Title And Abstract Readiness

The title and abstract are suitable for a Word-first review draft. The abstract keeps the central claim bounded to simulated model invocations in the reproducible deterministic-heavy benchmark and states that the evidence does not prove production cost reduction, real API-cost reduction, energy reduction, production behavior, or broad workload superiority.

Manual check after Word export: confirm the abstract remains readable as a standalone summary and that line wrapping does not make the non-claim language visually easy to miss.

## Figure Reference Readiness

Manuscript v0.10 now references reviewed draft assets for both figures:

- Figure 1 SVG source: `../assets/paper/kora-first-paper-figure-1-v0-9-draft.svg`
- Figure 1 PNG rendering: `../assets/paper/kora-first-paper-figure-1-v0-9-draft.png`
- Figure 2 SVG source: `../assets/paper/kora-first-paper-figure-2-v0-9-draft.svg`
- Figure 2 PNG rendering: `../assets/paper/kora-first-paper-figure-2-v0-9-draft.png`

The referenced files exist. The SVG files parse successfully, and the PNG files verify successfully at 2200x1200 RGB.

For Word-first review, the PNG renderings should be preferred for insertion because they are flattened and avoid fragile connector rendering. The SVG sources should remain available as editable sources for later figure revision.

## Caption Readiness

The Figure 1 caption is ready for review-draft export. It describes KORA as an execution-control layer before inference and states that the figure is architectural only and does not claim production readiness.

The Figure 2 caption is ready for review-draft export. It uses the approved benchmark boundary and explicitly avoids real API calls, production traffic, production cost savings, latency improvement, energy reduction, and broad workload superiority.

Manual check after Word export: verify that captions stay adjacent to their figures and that line wrapping does not detach the non-claim language from Figure 2.

## Citation And Reference Readiness

Citation and reference handling is sufficient for a review-draft Word export, but not final. Manuscript v0.10 preserves the v0.9 cited record set and keeps optional, deferred, or blocked records out of the manuscript body.

The bibliography is not final. Final citation style conversion, final bibliography formatting, source verification execution for records that still require it, and final manuscript-to-final-BibTeX synchronization remain pending.

Manual check before any final export: repeat citation-marker/reference matching and confirm that the preliminary references section and any future BibTeX output agree.

## Manual And External Verification Items

Manual/external verification items remain unresolved. The Word-first export may proceed only as a review draft while these items remain open. The export should not be described as final bibliography approval, final source-package approval, formal artifact approval, or submission readiness.

Open items include:

- final source verification for records still marked manual or external
- final bibliography style and field normalization
- final target-package citation requirements
- final claim-to-evidence audit after any manuscript or bibliography change
- final human approval of figure layout and manuscript formatting

## Claim Boundary Safety

The manuscript remains inside the approved claim boundary:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

The Word-first export must not visually or textually imply production cost reduction proof, real API-cost reduction proof, production benchmark proof, broad workload superiority proof, energy reduction evidence, formal external validation, signed partner validation, guaranteed adoption or funding, or benchmark results beyond the approved deterministic-heavy benchmark boundary.

## Figure Asset Readiness For Word Insertion

The draft figure assets are ready for a later Word insertion trial. The PNG renderings are the safest insertion target for a Word review draft because they are flattened images. The SVG sources remain useful for editing but should be checked carefully if inserted directly into Word.

Known risks:

- draft figures may need resizing for Word page width
- small labels may need manual readability inspection after insertion
- caption placement may shift during Word export or editing
- Word may treat SVGs differently across versions
- final publication layout is not yet approved

Figure 1 and Figure 2 are reviewed draft assets, not final publication layout.

## Manual Checks Required After Word Export

After a later Word export task, manually check:

- title, author metadata, and abstract layout
- heading hierarchy and section numbering
- Figure 1 and Figure 2 image resolution, scaling, and readability
- caption placement and non-claim wording near each figure
- table width, wrapping, and page breaks
- algorithm/pseudocode monospace formatting
- citation marker formatting and reference ordering
- preliminary bibliography formatting
- absence of broken local paths or private paths
- absence of accidental Word/PDF/arXiv final-submission language
- claim-boundary wording in abstract, Figure 2 caption, results, and claim-boundary note

## Decision

Word-first export can proceed in a later task as a review-draft export only. It should not be treated as final publication layout or a submission package.

PDF/arXiv/export packaging remains paused until a later task explicitly performs and verifies the export. Final bibliography, final figure approval, final layout review, source-package hygiene, and final human approval remain pending.
