# KORA First Paper Figure Redesign Note v0.1

Status date: 2026-05-14

## Purpose

This note records the figure redesign pass for the Word review draft. The redesigned figures are local-only review assets and were not committed as binary outputs.

## Design Direction

The Word review figures use a clean technical box-and-arrow style with:

- dark navy header and outlines,
- readable large labels,
- simple directional arrows,
- conservative captions and notes,
- no production, real API-cost, energy, broad-superiority, or formal-approval claims.

## Figure 1

Figure: KORA execution-control architecture.

Local review outputs:

- `figure-1-kora-execution-control-word.png`
- `figure-1-kora-execution-control-word.svg`

Status:

- Recreated for Word review.
- Inserted into the image-inserted Word draft.
- Ready for human visual review.
- Not yet publication-final.

Claim boundary:

- Shows architecture only.
- Does not claim production readiness.
- Does not claim every task can be handled deterministically.

## Figure 2

Figure: direct baseline vs KORA-controlled benchmark flow.

Local review outputs:

- `figure-2-benchmark-flow-word.png`
- `figure-2-benchmark-flow-word.svg`

Status:

- Recreated for Word review.
- Inserted into the image-inserted Word draft.
- Ready for human visual review.
- Not yet publication-final.

Claim boundary:

- Uses only the established deterministic-heavy benchmark counts: 100 tasks, 100 baseline simulated model invocations, 80 deterministic/no-model completions, 20 model-candidate paths, 80 avoided simulated model invocations, and 80% avoided invocation rate.
- Does not imply real API calls, production traffic, cost savings, latency improvement, or energy reduction.

## Remaining Work

- Review readability in Word.
- Decide whether to keep the dark navy technical style.
- Decide whether SVG or PNG should be the final editable/design source.
- Polish final publication figures only after human review.

## Status

The redesigned figures were reviewed in the Word draft and are not accepted for publication use because inserted arrows and diagram elements did not render reliably. They are superseded by placeholders for Word-first manuscript text review:

- `docs/paper/kora-first-paper-word-placeholder-review-v0-1.md`

The current figure outputs are placeholders only and should not be treated as publication-ready. Final publication-quality figures must be rebuilt separately after manuscript-body review is complete and the body text is stable. No generated image binaries were committed. PDF/arXiv export remains paused until the text and final figures are ready. The paper remains not submission-ready.
