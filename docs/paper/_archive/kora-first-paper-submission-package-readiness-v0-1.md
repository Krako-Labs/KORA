# KORA First Paper Submission Package Readiness v0.1

Status date: 2026-05-13

## Purpose

This venue-neutral checklist records what is present, missing, and blocked before the KORA first paper can become a submission package. It does not select a venue and does not mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-4.md`
- `docs/paper/kora-first-paper-manuscript-bibliography-sync-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-claim-to-evidence-audit-v0-1.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-final-bibliography-claim-audit-v0-1.md`
- `docs/paper/kora-first-paper-submission-readiness-gate-v0-1.md`
- `docs/paper/kora-first-paper-submission-readiness.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-figures-and-tables.md`
- `docs/paper/kora-first-paper-figure-specs.md`
- `docs/paper/kora-first-paper-table-specs.md`
- `docs/reports/benchmark_artifact_policy.md`
- `docs/reports/v0.3.0-alpha-runtime-evidence-reviewer-guide.md`
- `LICENSE`

## Current Package Status

- Manuscript version: v0.5 submission-candidate draft.
- Package status: not submission-ready.
- Venue status: arXiv-style technical report / preprint is the first target package direction; no conference, workshop, or journal target is selected.
- arXiv endorsement status: already obtained / not blocking.
- arXiv category compatibility: pending until endorsed category and selected category are confirmed.
- Bibliography status: preliminary BibTeX has 16 entries; full BibTeX remains incomplete.
- Claim status: bounded to the reproducible deterministic-heavy benchmark workload.
- Review status: final human review remains pending.

## Required Package Components

| Component | Current status | Missing or pending item | Blocker severity | Owner or decision type |
|---|---|---|---|---|
| Manuscript v0.5 | Candidate draft exists with inserted draft figure/table/algorithm assets | Final human approval and final sync after bibliography/export changes | High | User approval plus mechanical sync |
| Bibliography / BibTeX | Preliminary BibTeX has 16 entries | Full BibTeX completion and final formatting | High | Mechanical metadata work plus user scope approval |
| Citation sync audit | v0.1 exists | Repeat after final BibTeX and any manuscript edits | Medium | Mechanical |
| Claim-to-evidence audit | v0.1 exists | Repeat after any manuscript, figure, table, or package change | Medium | Mechanical |
| Figures and tables | Planning and specs exist | Final rendered figures/tables are not locked | High | Mechanical preparation plus user approval |
| Reproduction transcript | Checklist created in this packet | Clean transcript from a fresh checkout is not captured | High | Mechanical |
| Artifact availability statement | Policy and inventory inputs exist | Final preprint wording and artifact package selection are pending | Medium | User approval plus mechanical packaging |
| Repository / artifact inventory | Inventory created in this packet | Final submission bundle selection is pending | Medium | Mechanical plus user approval |
| License statement | Repository license exists | arXiv distribution-license decision is pending | Medium | User decision |
| Author and affiliation metadata | Author metadata supplied for preprint draft | Final display approval remains pending | Medium | User approval |
| Acknowledgement, funding, conflict, ethics metadata | Minimal/no-extra-statement approach selected | Required disclosure wording remains pending if applicable | Medium | User approval |
| Venue / export format | arXiv-style preprint direction selected | arXiv category, license, and export format are pending | High | User approval |
| Final human review signoff | Packet created in this pass | No final signoff recorded | High | User approval |

## Missing Components

- Final full BibTeX and final bibliography formatting.
- Final manuscript-to-final-bibliography synchronization.
- Final human-approved figures, tables, algorithm placement, numbering, and rendered/export form.
- Clean reproduction transcript from a fresh checkout.
- Final artifact availability statement and package selection.
- Final author/email display, acknowledgement, funding, conflict, and ethics wording if needed.
- arXiv category, license, and export format decision.
- Final human signoff.

## Conservative Status Notes

- Do not treat manuscript v0.5 as submission-ready.
- Do not treat the current preliminary BibTeX as a complete bibliography.
- Do not treat artifact docs or reproduction commands as formal artifact approval.
- Do not use this packet to claim production cost reduction, real API-cost reduction, production benchmark proof, broad workload superiority, or energy reduction evidence.

## Next Recommended Sequence

1. Confirm arXiv category compatibility and arXiv license.
2. Approve final title, abstract, author display, and email display.
3. Resolve first-package bibliography formatting using the conservative included subset.
4. Repeat manuscript-to-bibliography sync after final citation formatting.
5. Prepare final figures, tables, export package, and reproduction transcript.
6. Prepare artifact availability wording and selected artifact bundle.
7. Run final claim-to-evidence audit against the exact exported manuscript.
8. Complete final human review and only then decide whether the paper is submission-ready.

## Figure, Table, and Algorithm Asset Status

Figure/table/algorithm plan and draft docs now exist:

- `docs/paper/kora-first-paper-figure-table-algorithm-plan-v0-1.md`
- `docs/paper/kora-first-paper-figure-table-algorithm-drafts-v0-1.md`

They draft text-based architecture and benchmark-flow diagrams, benchmark and evidence-boundary tables, deterministic-first routing pseudocode, and an appendix artifact inventory table. Manuscript v0.5 now inserts these draft assets. Final rendered/export assets, numbering, layout, and captions remain pending human review.

## v0.5 Render and Export Readiness Status

Render/export readiness has been reviewed in `docs/paper/kora-first-paper-v0-5-render-export-readiness-v0-1.md`, and a text-only export package manifest exists at `docs/paper/kora-first-paper-arxiv-export-package-manifest-v0-1.md`.

No dedicated paper export pipeline was found in the repository. No PDF, rendered figure, binary export, or raw benchmark artifact was generated or committed. Final export route, Mermaid rendering/conversion, table layout, bibliography formatting, and human approval remain pending.

## arXiv Export Route Dry-Run Status

The export route dry run is recorded in `docs/paper/kora-first-paper-arxiv-export-route-dry-run-v0-1.md`, with the recommendation recorded in `docs/paper/kora-first-paper-arxiv-export-route-recommendation-v0-1.md`.

Pandoc can produce a LaTeX starting point from manuscript v0.5, but direct PDF generation is blocked locally by missing LaTeX tooling and Mermaid conversion is blocked locally by missing Mermaid CLI tooling. Generated dry-run outputs were kept under `/tmp/kora-paper-export-dry-run` and were not committed.

## Local Export Tooling and Hygiene Status

Local export tooling setup guidance, a dry-build command plan, and a source-package hygiene checklist now exist:

- `docs/paper/kora-first-paper-local-export-tooling-setup-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-dry-build-command-plan-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-source-package-hygiene-v0-1.md`

No tools were installed, no full dry build was attempted, and no generated PDF/source package/binary output was committed.

## Installed-Tools Dry Build Status

The installed-tools dry build is recorded in `docs/paper/kora-first-paper-arxiv-dry-build-result-v0-1.md`.

The `/tmp` dry build generated rendered figure PDFs, LaTeX source, and a PDF using Mermaid CLI with a local browser path and Tectonic. No generated PDF, rendered figure, source package, binary output, or raw benchmark artifact was committed. Layout warnings, bibliography integration, source-package hygiene, and final human review remain pending.

## Word-First Review Status

PDF and arXiv source-package work are paused while the Word review path is active. The Word draft review and figure redesign notes now exist:

- `docs/paper/kora-first-paper-word-draft-review-v0-1.md`
- `docs/paper/kora-first-paper-figure-redesign-note-v0-1.md`

Local-only Word drafts and redesigned figure assets were generated outside the repository for human review. No generated DOCX, PDF, image, source-package, or local working file was committed.

## Word Placeholder Review Status

The image-inserted Word draft is superseded for review because the inserted figure arrows and diagram elements did not render reliably. The active Word review draft uses placeholders for Figure 1 and Figure 2:

- `docs/paper/kora-first-paper-word-placeholder-review-v0-1.md`

Figure 1 and Figure 2 are placeholders only and should not be treated as publication-ready. Word-first manuscript text review remains the priority. Final publication-quality figures should be rebuilt separately after manuscript-body review is complete and the body text is stable. PDF/arXiv export remains paused until both text and final figures are ready.
