# KORA First Paper Local Export Tooling Setup v0.1

Status date: 2026-05-13

## Purpose

This guide records the local tooling needed for the next arXiv-style dry build of manuscript v0.5. It does not install tools automatically, does not generate a committed PDF, does not submit to arXiv, and does not mark the paper as submission-ready.

## Current Tool Availability

| Tool | Current status | Use in export path |
|---|---|---|
| `pandoc` | Available: 3.9.0.2 | Markdown-to-LaTeX starting conversion |
| `pdflatex` | Not found | PDF build route if TeX Live/MacTeX/BasicTeX is selected |
| `xelatex` | Not found | Alternate PDF build route if Unicode/font handling needs it |
| `tectonic` | Not found | Minimal PDF build route candidate |
| `mmdc` | Not found | Mermaid figure rendering |
| `mermaid-cli` | Not found | Mermaid figure rendering |
| `node` | Available: v22.21.1 | Runtime for Mermaid CLI |
| `npm` | Available: 10.9.4 | Mermaid CLI install path |
| `brew` | Available: 5.1.10 | macOS package install path |
| `python3` | Available: 3.13.5 | Validation and package hygiene scripts |

## Recommended Minimal Tool Path

Recommended minimal local tool path:

1. Install one LaTeX/PDF engine.
2. Install Mermaid CLI only if the final diagram decision is to render Mermaid diagrams locally.
3. Keep Pandoc as the Markdown-to-LaTeX starting converter.
4. Keep generated PDFs, rendered figures, and source packages outside the repository until final package policy is approved.

## User-Run Install Commands

No installation was performed in this task. If the user approves local setup, the likely macOS commands are:

```bash
brew install tectonic
npm install -g @mermaid-js/mermaid-cli
```

If `tectonic` is insufficient for the final source package, fallback TeX options are:

```bash
brew install --cask mactex
```

or, for a smaller TeX distribution:

```bash
brew install --cask basictex
```

After installing BasicTeX, a new shell may be needed so TeX binaries are on `PATH`.

## Fallback Options

- Render Mermaid diagrams manually from GitHub preview or Mermaid Live Editor after final figure approval.
- Convert Mermaid diagrams to text/ASCII diagrams if source-package simplicity is more important than visual rendering.
- Keep Mermaid diagrams as appendix source during review, but do not treat that as final arXiv-ready figure handling.
- Use GitHub-rendered Markdown or Pandoc HTML for human review only, not as the final arXiv source package.

## Non-Goals

- No automatic tool installation.
- No generated PDF committed.
- No rendered figure binaries committed.
- No source package committed.
- No arXiv upload.
- No submission-ready claim.
