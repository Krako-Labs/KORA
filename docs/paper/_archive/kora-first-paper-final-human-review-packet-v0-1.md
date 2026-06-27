# KORA First Paper Final Human Review Packet v0.1

Status date: 2026-05-13

## Purpose

This packet lists the human decisions still required before any submission-ready decision. It does not answer those decisions and does not mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-4.md`
- `docs/paper/kora-first-paper-submission-package-readiness-v0-1.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-final-bibliography-claim-audit-v0-1.md`
- `docs/paper/kora-first-paper-submission-readiness-gate-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-claim-to-evidence-audit-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-bibliography-sync-v0-1.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`

## Review Checklist

| Review item | Human decision needed | Current status |
|---|---|---|
| Title and abstract | Approve final wording or request edits | Pending |
| Claim boundary | Approve the bounded deterministic-heavy benchmark claim | Pending |
| Bibliography scope | Confirm the conservative first arXiv-style package scope | Draft scope supplied; final approval pending |
| Limitations | Approve limitations and non-claim language | Pending |
| Artifact and reproducibility | Approve artifact package scope and reproduction transcript expectations | Pending |
| Figures, tables, and algorithm | Approve final diagrams, tables, pseudocode, captions, numbering, and placement | Inserted in manuscript v0.5; final approval pending |
| Author and affiliation metadata | Approve final author block, affiliation, and email display | Draft metadata supplied; final approval pending |
| Acknowledgement, funding, conflict, and ethics metadata | Approve minimal required disclosure text if any | Pending |
| Target venue and export format | Confirm arXiv category, license, and export route | arXiv-style direction supplied; details pending |
| Final submission-ready decision | Decide whether the exact final package is ready to submit | Pending |

## Bibliography Scope Decisions

- Current arXiv-style draft decision: `[R17]` and `[R18]` remain excluded from the first arXiv-style package.
- Current arXiv-style draft decision: `[R19]` through `[R24]` remain tracker/audit-only for now.
- Current arXiv-style draft decision: optional workload, latency, API-cost, production, energy, KORA Studio, and real customer-data evidence stay outside first package scope.
- Deferred and still-not-eligible records should remain excluded from manuscript body citations unless later resolved.
- Confirm that no missing metadata should be filled without source-backed verification.

## Evidence Scope Decisions

- Decide whether optional expanded workload evidence stays outside the first submission scope.
- Decide whether latency p50/p95 evidence stays outside the first submission scope.
- Decide whether API-cost, production-traffic, energy, and real customer-data studies stay outside the first submission scope.
- Decide whether KORA Studio discussion remains outside the first submission scope.

## Figure, Table, and Algorithm Decisions

- Decide whether Figure 1 and Figure 2 should remain as Mermaid-rendered diagrams, be converted to exported graphics, or be converted to text/ASCII form.
- Review whether Table 1 should stay as the expanded deterministic-heavy benchmark table in manuscript v0.5.
- Review whether Table 2 should stay in the limitations section or move to an appendix.
- Review whether Algorithm 1 should stay in Section 3 or move to an appendix.
- Review whether Appendix Table A1 should be included in the arXiv-style package or kept as reviewer-support material.
- Confirm final numbering and captions after export format is selected.
- Review the v0.5 render/export readiness report before approving final PDF/source-package treatment.
- Decide whether Mermaid diagrams should be rendered to image files, converted to another source format, or replaced with text/ASCII diagrams for final export.
- Review the arXiv export route dry-run report and approve or reject the recommended Pandoc-to-LaTeX plus manual cleanup route.
- Confirm whether the local export environment should use `pdflatex`, `xelatex`, `tectonic`, or another approved PDF generation route.
- Approve or reject the local tooling setup commands before any tool installation.
- Review the arXiv source package hygiene checklist before any source package is assembled or uploaded.
- Review the installed-tools dry-build PDF and source-package folder under `/tmp` before approving any final export route.
- Decide whether the Tectonic layout warnings require manuscript/table cleanup before final package assembly.
- Review the dry-build output review report and decide whether the generated figure PDFs, repository-document links, and preliminary bibliography handling are acceptable for the final package path.
- Review the image-inserted Word draft before resuming PDF/arXiv source-package work.
- Review redesigned Figure 1 and Figure 2 for readability, style, and claim boundaries.
- Decide whether the redesigned figures should become the basis for publication figures.
- Use the placeholder Word draft for manuscript-body review because the image-inserted figures had unreliable arrows and diagram elements.
- Treat current Figure 1 and Figure 2 content as placeholders only, not publication-ready figures.
- Defer final Figure 1 and Figure 2 rebuilding until after manuscript-body review is complete and the body text is stable.
- Keep PDF/arXiv export paused until both manuscript text and final figures are ready.

## Venue and Export Decisions

- Current direction: arXiv-style technical report / preprint first.
- Endorsement status: already obtained / not blocking.
- arXiv category compatibility remains pending because the endorsed category is not recorded here.
- Later conference, workshop, or journal scanning is deferred and should not select a target in the current package draft.
- Approve whether export preparation should proceed after category, license, bibliography formatting, and figures/tables are stable.

## Claim Boundary Reminder

The current safe claim is:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

This packet does not approve stronger claims about production cost reduction, real API-cost reduction, production benchmark proof, broad workload superiority, energy reduction evidence, formal government validation, signed partner validation, guaranteed adoption or funding, or formal artifact approval.

## Signoff Status

No final human signoff is recorded in this document. The paper remains not submission-ready until the pending decisions above are explicitly resolved and the exact final package is reviewed.
