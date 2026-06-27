# KORA First Paper arXiv Export Route Dry Run v0.1

Status date: 2026-05-13

## Purpose

This report records a local export-route dry run for manuscript v0.5. It does not create a committed PDF, does not create committed figure binaries, does not upload an arXiv package, and does not mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-5.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-v0-5-render-export-readiness-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-export-package-manifest-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-style-package-readiness-v0-1.md`
- `docs/paper/kora-first-paper-final-human-review-packet-v0-1.md`
- `docs/paper/kora-first-paper-reproduction-transcript-checklist-v0-1.md`
- `docs/paper/kora-first-paper-artifact-package-inventory-v0-1.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`

## Tool Availability

| Tool | Availability | Notes |
|---|---|---|
| `pandoc` | Available: 3.9.0.2 | Markdown-to-LaTeX and Markdown-to-HTML dry runs were feasible. |
| `pdflatex` | Not found | Direct Pandoc PDF generation is blocked locally. |
| `xelatex` | Not found | XeLaTeX export is blocked locally. |
| `tectonic` | Not found | Tectonic export is blocked locally. |
| `mmdc` | Not found | Mermaid-to-image conversion is blocked locally. |
| `mermaid-cli` | Not found | Mermaid-to-image conversion is blocked locally. |
| `node` | Available: v22.21.1 | Runtime exists, but no Mermaid CLI is installed. |
| `npm` | Available: 10.9.4 | No network dependency install was performed. |
| `python3` | Available: 3.13.5 | Useful for validation scripts only. |
| `pdftoppm` | Not found | PDF page rendering review is blocked until a PDF renderer is installed. |

## Temporary Dry-Run Area

Generated outputs were placed only under:

```text
/tmp/kora-paper-export-dry-run
```

The dry run copied only:

- `kora-first-paper-manuscript-v0-5.md`
- `kora-first-paper-preliminary-bibtex-v0-1.md`

No generated outputs from `/tmp` were committed.

## Routes Tested

### Route A: Pandoc Markdown to LaTeX / PDF

Commands attempted in `/tmp/kora-paper-export-dry-run`:

```bash
pandoc kora-first-paper-manuscript-v0-5.md -s -t latex -o kora-first-paper-manuscript-v0-5.tex
pandoc kora-first-paper-manuscript-v0-5.md -s -o kora-first-paper-manuscript-v0-5.pdf
```

Result:

- Markdown-to-LaTeX succeeded.
- Markdown-to-PDF failed because `pdflatex` is not installed locally.
- The generated LaTeX source is useful as an intermediate export artifact, not as a final source package.

Observed blockers:

- Mermaid diagrams are carried through as code blocks, not rendered figures.
- Markdown tables become LaTeX `longtable` structures and require final layout review.
- PDF generation requires a local LaTeX engine or another approved PDF route.

### Route B: Markdown to LaTeX with Mermaid Converted Separately

Mermaid conversion was not executed because neither `mmdc` nor `mermaid-cli` is installed locally.

Recommended blocker handling:

- Convert Figure 1 and Figure 2 to arXiv-compatible figure assets only after user approval of the figure format.
- Keep generated figure outputs outside the repository until the final package policy is approved.

### Route C: Manual LaTeX Source Package Route

This route was assessed but not created as a full package in this task.

Required steps:

- Use Pandoc-generated LaTeX as a starting point, then manually review and simplify the source.
- Replace Mermaid code blocks with approved figure assets or text/ASCII diagrams.
- Convert Table 1, Table 2, and Appendix Table A1 into layout-safe LaTeX tables or simplified text tables.
- Convert the preliminary BibTeX subset into the final citation style selected for the package.
- Include only approved source files and exclude raw benchmark artifacts.

This route is likely safer than direct Markdown-to-PDF because it exposes the figure, table, and bibliography decisions before final packaging.

### Route D: HTML / GitHub-Rendered Review Route

Command attempted in `/tmp/kora-paper-export-dry-run`:

```bash
pandoc kora-first-paper-manuscript-v0-5.md -s -t html -o kora-first-paper-manuscript-v0-5.html
```

Result:

- Markdown-to-HTML succeeded.
- This route is useful for human review only.
- It is not sufficient as an arXiv source package route.

## Recommendation

Use a Pandoc-to-LaTeX starting route followed by manual source-package cleanup:

1. Generate LaTeX from manuscript v0.5 with Pandoc.
2. Convert or replace Mermaid diagrams after user approval of figure format.
3. Review and simplify wide tables for PDF/LaTeX layout.
4. Finalize the bibliography subset and citation style.
5. Generate the final PDF/source package only after category, license, figure format, and human review decisions are complete.

Fallback route:

- Use the HTML/GitHub-rendered path for human review only while the arXiv-compatible LaTeX/PDF route is prepared.

## Outputs Generated

Temporary outputs generated under `/tmp/kora-paper-export-dry-run`:

- `kora-first-paper-manuscript-v0-5.tex`
- `kora-first-paper-manuscript-v0-5.html`
- `pandoc-latex.stdout`
- `pandoc-latex.stderr`
- `pandoc-pdf.stdout`
- `pandoc-pdf.stderr`
- `pandoc-html.stdout`
- `pandoc-html.stderr`

No PDF was generated. No binary figure files were generated. No `/tmp` outputs were committed.

## Remaining User Approvals

- Final arXiv category and compatibility confirmation.
- Final arXiv license confirmation.
- Mermaid figure format decision.
- Wide-table layout decision.
- Final bibliography formatting decision.
- Final human review of the exact export package.

## Status

The dry run identifies a practical export route, but the paper remains not submission-ready.
