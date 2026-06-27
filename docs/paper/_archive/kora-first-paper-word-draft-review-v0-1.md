# KORA First Paper Word Draft Review v0.1

Status date: 2026-05-14

## Purpose

This report records the Word-first human review package created from manuscript v0.5. PDF and arXiv source-package generation are paused. Generated Word files, figure images, and local Markdown working copies were created outside the public repository and were not committed. The paper remains not submission-ready.

## Source Manuscript

- `docs/paper/kora-first-paper-manuscript-v0-5.md`

## Local Output Root

Generated outputs were written under the local-only generated paper output root:

```text
generated_paper_outputs/word_draft_v0_5/
```

This directory is outside the public KORA repository and is not tracked.

## Word Outputs

| Output | Status | Approximate size | Recommended use | Committed |
|---|---|---:|---|---:|
| `kora-first-paper-manuscript-v0-5-word-review-image-inserted.docx` | generated | 177,462 bytes | Primary human review draft | no |
| `kora-first-paper-manuscript-v0-5-word-review-text-only.docx` | generated | 22,085 bytes | Fallback text-only review draft | no |

The image-inserted Word draft contains two embedded PNG figure media files. The text-only Word draft preserves the manuscript content without embedded figure images.

## Figure Outputs

| Figure | Local outputs | Status | Committed |
|---|---|---|---:|
| Figure 1: KORA execution-control architecture | `figure-1-kora-execution-control-word.png`, `figure-1-kora-execution-control-word.svg` | recreated for Word review | no |
| Figure 2: direct baseline vs KORA-controlled benchmark flow | `figure-2-benchmark-flow-word.png`, `figure-2-benchmark-flow-word.svg` | recreated for Word review | no |

The figures were recreated as simple technical diagrams for Word review rather than using the prior Mermaid-rendered outputs directly.

## Generation Commands

The local Word package was generated with Pandoc and local image assets:

```bash
pandoc docs/paper/kora-first-paper-manuscript-v0-5.md -o <local-output>/kora-first-paper-manuscript-v0-5-word-review-text-only.docx
pandoc <local-output>/kora-first-paper-manuscript-v0-5-word-review-image-inserted.md --resource-path=<local-output> -o <local-output>/kora-first-paper-manuscript-v0-5-word-review-image-inserted.docx
```

The image-inserted Markdown working copy replaced the two Mermaid code blocks with local PNG figure references. The repository manuscript was not modified for local image paths.

## Verification

- Word generation passed.
- The image-inserted DOCX contains two embedded PNG media files.
- The text-only DOCX contains no embedded media files.
- No PDF was generated for this task.
- No generated DOCX, PNG, SVG, Markdown working copy, PDF, or source package was committed.

## Known Word Layout Risks

- Tables still need human visual review in Word, especially Table 1, Table 2, and Appendix Table A1.
- Captions are plain manuscript text and may need Word-native caption styling later.
- Cross-references are manual text references, not Word fields.
- Bibliography remains a preliminary manuscript section and is not final Word bibliography automation.
- Algorithm 1 remains a text block and may need styling for readability.

## Remaining Review Items

- Human review of the image-inserted Word draft.
- Human review of both redesigned figures for clarity, scale, and visual style.
- Decide whether the redesigned figures should become the basis for publication figures.
- Review table layout and captions in Word.
- Final bibliography formatting and citation review.
- Final arXiv PDF/source-package work remains paused until Word review is complete.

## Status

The image-inserted Word draft is superseded for review because the inserted figure arrows did not render correctly. The active Word review draft uses figure placeholders and is recorded in:

- `docs/paper/kora-first-paper-word-placeholder-review-v0-1.md`

The Word-first review route remains active. The paper remains not submission-ready.
