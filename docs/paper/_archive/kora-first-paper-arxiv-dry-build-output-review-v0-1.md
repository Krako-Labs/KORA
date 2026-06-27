# KORA First Paper arXiv Dry Build Output Review v0.1

Status date: 2026-05-14

## Purpose

This report reviews the `/tmp` dry-build outputs from the installed-tools arXiv dry build. It records output inventory, build warnings, and source-package hygiene findings. It does not commit generated PDFs, rendered figures, source packages, binary outputs, or raw benchmark artifacts. It does not submit to arXiv and does not mark the paper as submission-ready.

## Source Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-5.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-dry-build-result-v0-1.md`
- `/tmp/kora-paper-arxiv-dry-build/build`
- `/tmp/kora-paper-arxiv-dry-build/source-package`

## Output Inventory

| Output | Exists | Approximate size | Purpose | Final package candidate | Committed |
|---|---:|---:|---|---:|---:|
| `/tmp/kora-paper-arxiv-dry-build/build/figure-1.pdf` | yes | 20,448 bytes | Rendered Figure 1 dry-run output | yes, after review | no |
| `/tmp/kora-paper-arxiv-dry-build/build/figure-2.pdf` | yes | 19,644 bytes | Rendered Figure 2 dry-run output | yes, after review | no |
| `/tmp/kora-paper-arxiv-dry-build/build/kora-first-paper-manuscript-v0-5.tex` | yes | 38,224 bytes | Generated LaTeX dry-run source | yes, after cleanup | no |
| `/tmp/kora-paper-arxiv-dry-build/build/kora-first-paper-manuscript-v0-5.pdf` | yes | 92,996 bytes | Generated PDF dry-run output | no, final PDF must be regenerated after cleanup | no |
| `/tmp/kora-paper-arxiv-dry-build/source-package/` | yes | 4 files, about 90,965 bytes total | Cleaned source-package dry-run folder | candidate structure only | no |

The generated figure PDFs are PDF 1.4 one-page documents according to local `file` inspection. The generated paper PDF is a PDF 1.5 document. Page-count tooling was not available locally beyond this basic file inspection.

## Source-Package Folder Contents

Reviewed folder:

```text
/tmp/kora-paper-arxiv-dry-build/source-package
```

Contents:

- `figure-1.pdf`
- `figure-2.pdf`
- `kora-first-paper-manuscript-v0-5.tex`
- `kora-first-paper-preliminary-bibtex-v0-1.md`

The cleaned source-package folder does not include the generated final PDF. A separate older scratch folder under `/tmp/kora-paper-arxiv-dry-build/package` contains a generated PDF and should not be used as the final source package candidate.

## Build Warning Summary

Fatal errors:

- The first Tectonic run failed because `figure-1.pdf` did not exist after the default Mermaid rendering attempt failed.
- The rerun passed after Mermaid CLI was pointed at the locally installed browser and figure PDFs were generated.

Warnings in the successful Tectonic run:

- Overfull boxes in route-metric text and long table/reference-heavy sections.
- Underfull boxes in several paragraph/table areas.
- Repeated overfull warnings around the appendix artifact inventory table.
- Warnings that tagged figure PDFs were read while tags were ignored.

No missing figure warnings remained in the successful build. Pandoc emitted no stderr output for the LaTeX generation step.

## Source-Package Hygiene Findings

Passed:

- No hidden files found in the cleaned source-package folder.
- No raw benchmark artifacts found.
- No generated logs, `.aux`, `.out`, stdout, stderr, JSON, archive, or temporary files found.
- No embedded `/tmp` paths found in the generated `.tex`.
- Figure includes use relative paths: `figure-1.pdf` and `figure-2.pdf`.
- No source-package files were committed.

Needs review:

- The bibliography source is still the preliminary Markdown BibTeX document, not final `.bib` integration.
- The generated `.tex` still contains repository-document links from the Markdown draft; decide whether these should remain, be converted, or be removed for the final source package.
- A broad secret-pattern scan produced a false positive on ordinary prose containing the substring `sk-`; no credential-like token was identified.
- The cleaned source package includes binary figure PDFs, which are appropriate as final package candidates only after human visual review.

## Blockers

- Review the generated PDF visually.
- Clean up overfull/underfull table and paragraph layout warnings.
- Decide final treatment for tagged figure PDF warnings.
- Convert preliminary bibliography handling into final package-ready form.
- Complete source-package hygiene review on the exact final package folder.
- Confirm arXiv category and license.
- Complete final human approval.

## Next Recommended Fixes

1. Review the `/tmp` PDF visually.
2. Simplify or reformat Table 1, Table 2, and Appendix Table A1 for LaTeX/PDF layout.
3. Decide whether repository-document links should remain in the final paper source.
4. Convert the preliminary BibTeX subset into a final package bibliography format.
5. Rebuild under `/tmp` and repeat source-package hygiene checks.

## Status

Dry-build output review and source-package hygiene review are complete for the current `/tmp` outputs. No generated binary output was committed. The paper remains not submission-ready.
