# KORA First Paper arXiv Dry Build Result v0.1

Status date: 2026-05-14

## Purpose

This report records a local arXiv-style dry build for manuscript v0.5 after installing Tectonic and Mermaid CLI. Generated outputs were kept under `/tmp` only. No generated PDF, rendered figure, source package, binary output, or raw benchmark artifact was committed. No arXiv submission was made, and the paper remains not submission-ready.

## Source Files

- `docs/paper/kora-first-paper-manuscript-v0-5.md`
- `docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-dry-build-command-plan-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-source-package-hygiene-v0-1.md`
- `docs/paper/kora-first-paper-arxiv-export-route-recommendation-v0-1.md`

## Tool Versions

| Tool | Version / status |
|---|---|
| `pandoc` | 3.9.0.2 |
| `tectonic` | 0.16.9 |
| `mmdc` | 11.14.0 |
| `node` | v26.0.0 |
| `npm` | 11.12.1 |
| `python3` | 3.13.5 |

## Temporary Workspace

Dry-build workspace:

```text
/tmp/kora-paper-arxiv-dry-build
```

Generated outputs stayed in:

- `/tmp/kora-paper-arxiv-dry-build/build`
- `/tmp/kora-paper-arxiv-dry-build/source-package`

## Commands Run

The manuscript and preliminary BibTeX were copied to `/tmp`:

```bash
rm -rf /tmp/kora-paper-arxiv-dry-build
mkdir -p /tmp/kora-paper-arxiv-dry-build/source /tmp/kora-paper-arxiv-dry-build/build
cp docs/paper/kora-first-paper-manuscript-v0-5.md /tmp/kora-paper-arxiv-dry-build/source/
cp docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md /tmp/kora-paper-arxiv-dry-build/source/
```

The two Mermaid blocks were extracted into:

- `/tmp/kora-paper-arxiv-dry-build/build/figure-1.mmd`
- `/tmp/kora-paper-arxiv-dry-build/build/figure-2.mmd`

Initial Mermaid rendering commands:

```bash
mmdc -i figure-1.mmd -o figure-1.pdf
mmdc -i figure-2.mmd -o figure-2.pdf
```

Initial result: failed because Mermaid CLI could not find its Puppeteer-managed Chrome/headless-shell.

Successful Mermaid rendering commands using the locally installed browser:

```bash
PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" mmdc -i figure-1.mmd -o figure-1.pdf
PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" mmdc -i figure-2.mmd -o figure-2.pdf
```

Markdown-to-LaTeX command:

```bash
pandoc kora-first-paper-manuscript-v0-5-figures.md -s -t latex -o kora-first-paper-manuscript-v0-5.tex
```

PDF dry-build command:

```bash
tectonic kora-first-paper-manuscript-v0-5.tex
```

## Results

| Step | Result | Notes |
|---|---|---|
| Mermaid extraction | Passed | Two `.mmd` files created under `/tmp`. |
| Mermaid rendering, default `mmdc` | Failed | Puppeteer-managed Chrome/headless-shell was missing. |
| Mermaid rendering with local browser path | Passed | Figure 1 and Figure 2 PDFs were generated under `/tmp`. |
| Pandoc Markdown-to-LaTeX | Passed | Generated LaTeX source under `/tmp`. |
| Tectonic PDF build | Passed | Generated dry-run PDF under `/tmp`. |
| Source-package folder assembly | Passed as dry-run only | Created a source-only folder under `/tmp` with LaTeX, figure PDFs, and preliminary bibliography draft. |

## Generated `/tmp` Outputs

Key generated outputs:

- `/tmp/kora-paper-arxiv-dry-build/build/figure-1.pdf` - 20,448 bytes
- `/tmp/kora-paper-arxiv-dry-build/build/figure-2.pdf` - 19,644 bytes
- `/tmp/kora-paper-arxiv-dry-build/build/kora-first-paper-manuscript-v0-5.tex` - 38,224 bytes
- `/tmp/kora-paper-arxiv-dry-build/build/kora-first-paper-manuscript-v0-5.pdf` - 92,996 bytes

Dry-run source-package folder:

- `/tmp/kora-paper-arxiv-dry-build/source-package/kora-first-paper-manuscript-v0-5.tex`
- `/tmp/kora-paper-arxiv-dry-build/source-package/figure-1.pdf`
- `/tmp/kora-paper-arxiv-dry-build/source-package/figure-2.pdf`
- `/tmp/kora-paper-arxiv-dry-build/source-package/kora-first-paper-preliminary-bibtex-v0-1.md`

No `/tmp` output was committed.

## Build Warnings

Tectonic completed the PDF build, but emitted layout warnings:

- overfull boxes in long table and reference-heavy sections,
- underfull boxes in some paragraphs,
- repeated warnings around the appendix artifact table area,
- warnings about tagged PDF inputs from rendered figure PDFs.

These warnings do not block a dry build, but they do block treating the package as final without layout review.

## Remaining Blockers

- Final arXiv category and license confirmation.
- Final Mermaid rendering policy and browser configuration.
- Final wide-table and appendix-table layout cleanup.
- Final bibliography formatting; current dry-run package uses the preliminary bibliography draft as a source input, not a final `.bib` integration.
- Final source-package hygiene review.
- Final human review of the exact PDF and source package.

## Output Review Follow-Up

The dry-build output review now exists:

- `docs/paper/kora-first-paper-arxiv-dry-build-output-review-v0-1.md`

The review confirms that the `/tmp` PDF, rendered figure PDFs, generated LaTeX, and cleaned source-package folder exist. It also records layout warnings, source-package hygiene findings, and remaining blockers before final package approval.

## Claim and Submission Status

This dry build does not add evidence for production cost reduction, real API-cost reduction, production benchmark proof, broad workload superiority, energy reduction evidence, formal artifact approval, or paper submission readiness.

The dry build demonstrates that a local PDF can be generated from manuscript v0.5 using rendered Mermaid figures and Tectonic, but the paper remains not submission-ready.
