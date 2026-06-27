# KORA First Paper arXiv Dry Build Command Plan v0.1

Status date: 2026-05-13

## Purpose

This command plan defines a repeatable local dry build path for manuscript v0.5 once the required local export tools are installed. It does not run an arXiv submission, does not create committed binaries, and does not mark the paper as submission-ready.

## Working Directory

Use a temporary working directory:

```bash
rm -rf /tmp/kora-paper-arxiv-dry-build
mkdir -p /tmp/kora-paper-arxiv-dry-build
```

Generated outputs must stay under `/tmp/kora-paper-arxiv-dry-build` unless a later task explicitly approves a tracked source package.

## Source Inputs

Copy the current manuscript and bibliography draft:

```bash
cp docs/paper/kora-first-paper-manuscript-v0-5.md /tmp/kora-paper-arxiv-dry-build/
cp docs/paper/kora-first-paper-preliminary-bibtex-v0-1.md /tmp/kora-paper-arxiv-dry-build/
cd /tmp/kora-paper-arxiv-dry-build
```

## Pandoc-to-LaTeX Command

```bash
pandoc kora-first-paper-manuscript-v0-5.md \
  -s \
  -t latex \
  -o kora-first-paper-manuscript-v0-5.tex
```

Expected result: LaTeX source is generated as a starting point. Manual cleanup is still required for diagrams, wide tables, bibliography formatting, and final package structure.

## Mermaid Rendering Command Template

If Mermaid CLI is installed and the final figure decision approves rendered figures:

```bash
mmdc -i figure-1-kora-execution-control.mmd -o figure-1-kora-execution-control.svg
mmdc -i figure-2-benchmark-flow.mmd -o figure-2-benchmark-flow.svg
```

These commands require extracting the Figure 1 and Figure 2 Mermaid blocks from manuscript v0.5 into `.mmd` files under `/tmp/kora-paper-arxiv-dry-build`.

Do not commit rendered figure files until final package policy is approved.

## LaTeX / PDF Command Templates

If `tectonic` is installed:

```bash
tectonic kora-first-paper-manuscript-v0-5.tex
```

If a TeX Live/MacTeX/BasicTeX route is selected:

```bash
pdflatex kora-first-paper-manuscript-v0-5.tex
pdflatex kora-first-paper-manuscript-v0-5.tex
```

If BibTeX is converted to a `.bib` file and cited from LaTeX:

```bash
pdflatex kora-first-paper-manuscript-v0-5.tex
bibtex kora-first-paper-manuscript-v0-5
pdflatex kora-first-paper-manuscript-v0-5.tex
pdflatex kora-first-paper-manuscript-v0-5.tex
```

The exact bibliography command sequence depends on the final bibliography format.

## Source Package Assembly Checklist

- Include the final `.tex` source.
- Include only approved figure files or approved text/ASCII figure replacements.
- Include only the finalized bibliography subset.
- Include any required style files that are not standard in the selected route.
- Include artifact appendix content only in approved source form.
- Exclude raw benchmark artifacts.
- Exclude generated temporary logs unless needed for debugging and explicitly approved.

## Package Hygiene Checks

Run these checks from the dry-build directory before any package is considered for upload:

```bash
find . -maxdepth 2 -type f -print | sort
grep -RInE 'sk-|ghp_|password=|secret=|api_key=|OPENAI_API_KEY=|ANTHROPIC_API_KEY=' .
grep -RInE 'production cost reduction|real API-cost reduction|production benchmark proof|formally approved|guaranteed' .
```

Also inspect manually for absolute local home paths, private local context paths, and internal workflow markers. Matches must be reviewed before any upload. Non-claim boundary text may be acceptable in repository docs, but the final arXiv source package should avoid unrelated audit/status material unless intentionally included.

## Commands Not to Run Without User Approval

Do not run any actual arXiv upload command or use the arXiv submission UI as part of this dry build.

Do not commit:

- generated PDFs,
- rendered figure binaries,
- source packages,
- raw benchmark artifacts,
- provider responses,
- private data,
- temporary build outputs.

## Current Dry-Build Status

A full `/tmp` dry build was not attempted in this task because no LaTeX engine and no Mermaid CLI are currently installed locally. The next dry build should start after the user approves and installs the selected tooling.
