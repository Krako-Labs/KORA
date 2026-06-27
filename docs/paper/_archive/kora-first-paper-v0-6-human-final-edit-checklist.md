# KORA First Paper v0.6 Human Final-Edit Checklist

Checklist date: 2026-05-18

## Purpose

This checklist prepares human final-edit review of manuscript v0.6 before any v0.7 manuscript pass. It focuses on text readiness, claim boundaries, citation readiness, and blockers that should be resolved before figure rebuild, Word export, PDF export, or arXiv package work resumes.

This checklist does not mark the paper as submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-6.md`
- `docs/paper/kora-first-paper-word-first-text-review-v0-1.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-final-human-review-packet-v0-1.md`
- `docs/paper/kora-first-paper-submission-readiness-gate-v0-1.md`

## Scope

In scope:

- manuscript-body final-edit review
- title and abstract review
- terminology and category framing
- claim-boundary review
- citation and bibliography-readiness review
- blocker review before a possible v0.7 pass

Out of scope:

- figure rebuild
- Word export
- PDF export
- arXiv source-package assembly
- final venue/category/license selection
- generated artifact creation

Current Figure 1 and Figure 2 remain text placeholders only. Word/PDF/arXiv/export work remains paused.

## Title and Abstract Readiness

Human reviewer checks:

- Confirm the title accurately frames KORA as deterministic-first execution control.
- Confirm the abstract no longer reads like a change log or draft-status note.
- Confirm the abstract states the evidence basis without implying production, cost, energy, or broad-superiority results.
- Confirm the abstract uses the approved deterministic-heavy benchmark boundary:

```text
In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.
```

Ready for v0.7 only if:

- The title and abstract can be approved without changing the claim boundary.

## Introduction and Problem Framing

Human reviewer checks:

- Confirm the introduction clearly explains why model-first execution can be wasteful for deterministic, structured, policy, routing, and validation tasks.
- Confirm "Structure first. Inference second." remains useful and not too informal for the target draft style.
- Confirm the contribution bullets are concise and do not overstate evidence.
- Confirm the introduction preserves model escalation as available when deterministic handling is insufficient.

Ready for v0.7 only if:

- The introduction can be tightened without adding new claims or new evidence.

## Category Framing: Execution-Control Layer

Human reviewer checks:

- Confirm KORA is framed as an execution-control layer before inference.
- Confirm KORA is not framed as a model-serving optimizer, workflow scheduler, RAG replacement, local runtime, or agent-framework replacement.
- Confirm related-work positioning stays complementary rather than superiority-based.
- Confirm the phrase "execution-control layer" is used consistently enough for a reader to understand the category.

Ready for v0.7 only if:

- Category language is clear and consistent across the abstract, introduction, related work, and execution-model sections.

## Terminology Consistency

Human reviewer checks:

- Confirm consistent use of:
  - deterministic-first execution control
  - execution-control layer
  - deterministic route
  - structured route or structured lookup
  - policy/validation
  - model escalation
  - model-candidate path
  - simulated model invocation
  - local/no-network validation
- Confirm `model_candidate`, `model_required`, and model escalation language are understandable and not conflated.
- Confirm benchmark terms distinguish simulated model invocations from real provider calls.

Ready for v0.7 only if:

- Terminology can be read consistently without relying on private context or prior task notes.

## Method and System Explanation Clarity

Human reviewer checks:

- Confirm Section 3 explains the execution-control model before Algorithm 1.
- Confirm the `model_candidate` explanation is understandable and does not imply a real provider call in the current benchmark evidence.
- Confirm Algorithm 1 is clearly paper-level pseudocode, not an implementation guarantee for every route class.
- Confirm the metric definitions separate model-call reduction from validation correctness.

Ready for v0.7 only if:

- A reader can understand the routing model and metric definitions from the manuscript alone.

## Benchmark Wording and Claim Boundary

Human reviewer checks:

- Confirm every benchmark-result statement remains tied to the deterministic-heavy benchmark or synthetic local/no-network workload.
- Confirm every quantitative deterministic-heavy result uses simulated model-invocation wording where applicable.
- Confirm the manuscript does not imply:
  - production cost reduction proof
  - real API-cost reduction proof
  - production benchmark proof
  - broad workload superiority proof
  - energy reduction evidence
  - formal government validation
  - signed partner validation
  - guaranteed adoption or funding
- Confirm the customer-support workload remains framed as synthetic local/no-network validation, not production support evidence.

Ready for v0.7 only if:

- Claim wording remains bounded to the current public evidence.

## Limitations and Non-Claim Completeness

Human reviewer checks:

- Confirm the limitations section explicitly keeps current blockers visible:
  - synthetic workloads
  - limited workload diversity
  - no production traffic
  - no real provider validation
  - no real API-cost proof
  - no production benchmark proof
  - no full runtime-integrated real-provider benchmark evidence
  - no energy measurement
  - no user study
  - no broad workload superiority claim
  - full BibTeX remains incomplete
  - final citation style remains pending
  - Figure 1 and Figure 2 remain placeholders
- Confirm Table 2 remains conservative and does not read like formal artifact approval.

Ready for v0.7 only if:

- Limitations remain complete after any copyediting.

## Citation Readiness and Bibliography Markers

Human reviewer checks:

- Confirm manuscript v0.6 cites only records currently allowed in the manuscript scope.
- Confirm the references section still warns that citation style and BibTeX are not final.
- Confirm deferred or still-not-eligible records are not added during text cleanup.
- Confirm full BibTeX remains incomplete unless a later bibliography task resolves it.
- Confirm final manuscript-to-final-BibTeX synchronization remains a blocker.

Ready for v0.7 only if:

- Human edits do not create new citation or bibliography obligations without source-backed metadata.

## Figure Placeholder Handling

Human reviewer checks:

- Confirm Figure 1 and Figure 2 are text placeholders only.
- Confirm placeholders do not distract from manuscript-body review.
- Confirm captions remain claim-safe while final figures are absent.
- Confirm no figure rebuild is attempted before manuscript body review is stable.

Ready for v0.7 only if:

- The manuscript body can be reviewed without final figures.

## Submission Blockers Before v0.7

Resolve or explicitly carry forward:

- human approval of title and abstract direction
- final copyedit notes for introduction and contributions
- terminology consistency review
- method/system explanation edits
- final claim-boundary review
- citation and bibliography blocker review
- decision on whether the final claim-boundary note stays in the manuscript or moves to package notes
- decision on whether Table 2 stays in limitations or moves to an appendix
- decision on whether Algorithm 1 stays in Section 3 or moves to an appendix

Do not proceed to figure rebuild or export solely from this checklist.

## Must Resolve Before Word/PDF/arXiv Export

Before export work resumes:

- manuscript text must be stable after human final edits
- final Figure 1 and Figure 2 direction must be approved
- final figure assets must be rebuilt or intentionally replaced
- tables and Algorithm 1 must be reviewed for layout
- final citation style and bibliography handling must be decided
- clean reproduction transcript must be captured or explicitly deferred from the package
- arXiv category, license, and final human approval must be resolved
- package source hygiene must be repeated before any upload

## Status

Manuscript v0.6 is ready for human final-edit review, not submission. Figure rebuild is out of scope, current figures remain placeholders, and Word/PDF/arXiv/export work remains paused.
