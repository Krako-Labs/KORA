# KORA First Paper v0.5 Render and Export Readiness v0.1

Status date: 2026-05-13

## Purpose

This report reviews manuscript v0.5 for Markdown, Mermaid, table, pseudocode, and export-package readiness. It does not generate a PDF, does not submit to arXiv, and does not mark the paper as submission-ready.

## Manuscript Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-5.md`

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-5.md`
- `docs/paper/kora-first-paper-figure-table-algorithm-plan-v0-1.md`
- `docs/paper/kora-first-paper-figure-table-algorithm-drafts-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-style-package-readiness-v0-1.md`
- `docs/paper/kora-first-paper-submission-package-readiness-v0-1.md`
- `docs/paper/kora-first-paper-final-human-review-packet-v0-1.md`
- `docs/paper/kora-first-paper-reproduction-transcript-checklist-v0-1.md`
- `docs/paper/kora-first-paper-artifact-package-inventory-v0-1.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `README.md`
- `docs/README.md`
- `.github/workflows/ci.yml`
- `pyproject.toml`

## Rendering Review

| Area | Review result | Risk | Action |
|---|---|---|---|
| Heading hierarchy | Ordered from title to section/subsection/appendix | Low | No manuscript fix needed |
| Mermaid Figure 1 | Uses a simple `flowchart LR`; node labels are quoted | Medium | GitHub Markdown should render; arXiv/PDF export needs rendered image or conversion path |
| Mermaid Figure 2 | Uses a simple `flowchart LR`; node labels are quoted | Medium | GitHub Markdown should render; arXiv/PDF export needs rendered image or conversion path |
| Markdown tables | Tables are syntactically valid | Medium | Wide rows may need narrowing for PDF/LaTeX export |
| Algorithm block | Uses fenced `text` pseudocode | Low | No manuscript fix needed |
| Figure/table numbering | Figure 1, Figure 2, Table 1, Table 2, Algorithm 1, Appendix Table A1 are internally consistent | Low | Final numbering still needs human review after export |
| Appendix numbering | Appendix A and Table A1 are consistent | Low | No manuscript fix needed |
| Internal references | No broken Markdown links found in the new v0.5 additions | Low | No manuscript fix needed |
| Local paths | Artifact paths in Appendix Table A1 exist in the repository | Low | No manuscript fix needed |
| Unicode/text hygiene | ASCII-only in changed files | Low | No manuscript fix needed |

## Fixes Applied

No manuscript content fixes were required in this pass. Status/readiness documents were updated to record that render/export readiness has been reviewed and that final export remains pending.

## Export Pipeline Status

No dedicated paper export pipeline was found in the repository.

Checked for:

- repository `Makefile`
- Pandoc or LaTeX paper build scripts
- Markdown-to-PDF export scripts
- paper-specific export instructions
- docs build/export GitHub Actions
- pyproject export tooling

Current repository automation is CI/test oriented. `.github/workflows/ci.yml` installs the package, runs release smoke checks, and runs pytest. It does not build a paper PDF or arXiv source package.

## PDF and Source Package Status

- PDF generated in this pass: no.
- Binary PDF committed: no.
- arXiv source package created: no.
- Raw benchmark artifacts uploaded or committed: no.
- Export package manifest created: yes, see `docs/paper/kora-first-paper-arxiv-export-package-manifest-v0-1.md`.

## Mermaid Rendering Status

Mermaid syntax is appropriate for GitHub Markdown review, but arXiv does not accept Mermaid as a rendered figure by itself. Before submission, Figure 1 and Figure 2 need one of these paths:

- render Mermaid diagrams to reviewed image files and include those in the source package, or
- convert diagrams to LaTeX/TikZ or another arXiv-compatible figure source, or
- replace Mermaid diagrams with plain text/ASCII diagrams if the package stays text-only.

No rendered diagram files were created in this pass.

## Table Rendering Status

The Markdown tables are valid for repository review. For PDF/LaTeX export, Table 1, Table 2, and Appendix Table A1 may need:

- shortened row text,
- smaller font or landscape/appendix treatment,
- conversion to LaTeX tables,
- final caption placement.

No benchmark values were changed.

## Remaining Blockers

- Select final arXiv category and confirm category compatibility.
- Confirm arXiv license.
- Decide final export route: Markdown-to-PDF, LaTeX, or another arXiv-compatible source package.
- Render or convert Mermaid diagrams for arXiv-compatible submission.
- Review and possibly narrow wide tables for final PDF layout.
- Finalize bibliography formatting and full citation treatment.
- Capture final clean reproduction transcript.
- Complete final human review.

## Claim Safety

The render/export review does not change the bounded claim:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

This report does not support production cost reduction proof, real API-cost reduction proof, production benchmark proof, full runtime-integrated real-provider benchmark evidence, broad workload superiority proof, energy reduction evidence, formal government validation, signed partner validation, guaranteed adoption or funding, formal artifact approval, or paper submission readiness.

## Status

Manuscript v0.5 is ready for repository Markdown review, but not ready for arXiv submission. Export tooling, figure rendering/conversion, final table layout, final bibliography formatting, and human approval remain pending. The paper remains not submission-ready.
