# KORA First Paper Word-First Text Review v0.1

Review date: 2026-05-18

## Purpose

This note reviews the current KORA first-paper manuscript text for Word-first human review. It focuses on manuscript structure, claim boundaries, readability, citation readiness, and submission blockers.

Figure quality is out of scope for this review because Figure 1 and Figure 2 are current placeholders only. Figure arrows and diagram elements did not render reliably in the generated Word draft, and final publication-quality figures should be rebuilt separately after manuscript-body review is complete.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-5.md`
- `docs/paper/kora-first-paper-word-placeholder-review-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-claim-to-evidence-audit-v0-1.md`
- `docs/paper/kora-first-paper-manuscript-bibliography-sync-v0-1.md`
- `docs/paper/kora-first-paper-submission-candidate-status-v0-1.md`
- `docs/paper/kora-first-paper-submission-package-readiness-v0-1.md`
- `docs/paper/kora-first-paper-final-human-review-packet-v0-1.md`
- `docs/paper/kora-first-paper-missing-evidence-checklist.md`

## Manuscript Version Reviewed

- Current manuscript: `docs/paper/kora-first-paper-manuscript-v0-5.md`
- Review mode: Word-first manuscript text review
- Figure status: placeholders only
- Package status: not submission-ready

## Claim Boundary

The approved bounded claim for the manuscript text is:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

This review found that the manuscript text keeps the claim tied to the deterministic-heavy benchmark and repeatedly labels the evidence as simulated, local/no-network, or synthetic where applicable.

The manuscript does not claim:

- production cost reduction proof
- real API-cost reduction proof
- production benchmark proof
- broad workload superiority proof
- energy reduction evidence
- formal government validation
- signed partner validation
- guaranteed adoption or funding

## Abstract Clarity

The abstract explains the model-first problem, introduces KORA as deterministic-first execution control, and states the benchmark result within the current evidence boundary. It also states the main non-claims directly.

Recommended next edit:

- Shorten draft-process language before final publication. The sentence about the manuscript version synchronizing references and inserting assets is useful for review tracking, but it reads like package status rather than paper abstract content.

## Introduction and Problem Framing

The introduction clearly frames the problem: model-first systems can invoke models even when the task is deterministic, structured, policy-driven, or validation-oriented. The phrase "Structure first. Inference second." is readable and aligned with the paper's positioning.

Recommended next edits:

- Keep the four contribution bullets, but tighten them into final-paper language after human review.
- Preserve the distinction between deterministic-first routing and model replacement; the text should continue to say that model escalation remains available when deterministic handling is insufficient.

## KORA Positioning

The manuscript positions KORA as an execution-control layer before inference. This is clear and claim-safe. The related-work sections distinguish KORA from model serving, workflow orchestration, agent/tool frameworks, RAG, and local runtime systems without claiming superiority over those systems.

Recommended next edit:

- Keep the "complementary" framing in the related-work section. It prevents overclaiming and helps explain why KORA is not presented as a replacement for serving systems, workflow engines, agent frameworks, RAG, or local runtimes.

## Method and System Explanation

The execution model section is readable and gives the reviewer a concrete vocabulary: task graph, deterministic route, structured lookup, policy/validation, model escalation, and telemetry/reporting. Algorithm 1 is useful as paper-level pseudocode and remains appropriately non-implementation-specific.

Recommended next edits:

- Confirm during human review whether `model_candidate` should be explained once in prose before Algorithm 1.
- Keep Algorithm 1 as a conceptual routing description unless a later implementation appendix is added.

## Benchmark and Evidence Claim Safety

The evaluation and results sections keep the strongest result narrow. Table 1 uses the established deterministic-heavy benchmark values only: 100 tasks, 80 deterministic/no-model tasks, 20 model-candidate tasks, 100 direct-baseline simulated model invocations, 20 KORA-controlled simulated model invocations, 80 avoided simulated model invocations, 80% avoided invocation rate, 80 deterministic outputs checked, and 0 mismatches.

The customer-support workload is described as synthetic local/no-network validation and is not used as production evidence.

Recommended next edits:

- Keep "simulated model invocations" in every benchmark-result statement unless a later evidence pass adds real provider results.
- Keep the customer-support workload framed as validation/reporting evidence, not as a production support benchmark.

## Related Work and Citation Readiness

The manuscript cites the current v0.4/v0.5 citation scope and does not add deferred or still-not-eligible records. The references section notes that citation style and BibTeX are not final.

Citation readiness status:

- Manuscript-cited records remain aligned with the current preliminary BibTeX subset.
- Full BibTeX remains incomplete.
- Final bibliography formatting and final citation style conversion remain blockers.
- Final manuscript-to-final-BibTeX synchronization must be repeated after any future text or bibliography changes.

Recommended next edits:

- Do not add new citations during text cleanup unless the referenced record already has sufficient repository metadata and is approved for the current bibliography scope.
- Keep tracker-only and deferred records out of the manuscript body until the bibliography decision is updated.

## Limitations and Non-Claims

The limitations section is strong and should remain in the manuscript. It clearly lists synthetic workloads, limited workload diversity, no production traffic, no real provider validation, no real API-cost proof, no production benchmark proof, no full runtime-integrated real-provider benchmark evidence, no energy measurement, no user study, no broad workload superiority claim, preliminary reference integration, incomplete full BibTeX, and pending final citation style.

Recommended next edit:

- Preserve the limitations list through final copyediting. It is the main guardrail preventing the benchmark result from being read as a production, cost, energy, or broad-superiority claim.

## Readability and Structure

The manuscript structure is coherent for a technical report:

- Abstract
- Introduction
- Background and related work
- KORA execution model
- Evaluation methodology
- Results
- Limitations
- Reproducibility and artifact notes
- Conclusion
- Appendix artifact inventory
- References
- Claim boundary note

Recommended next edits before figure rebuild:

- Remove or revise manuscript-version status language from the abstract before final export.
- Tighten the transition between Section 3 and Section 4 so the evaluation follows naturally from the execution model.
- Review Table 1, Table 2, Algorithm 1, and Appendix Table A1 in Word for readability while keeping Figure 1 and Figure 2 as placeholders.
- Keep the claim boundary note at the end until final human review confirms whether it should remain in the submitted manuscript or move to package notes.

## Submission Blockers

The paper remains blocked on:

- Word-first manuscript text review.
- Final publication-quality Figure 1 and Figure 2 rebuild after the manuscript body is stable.
- Final table, algorithm, and appendix layout review.
- Full BibTeX completion or final accepted bibliography-scope decision.
- Final citation style conversion and manuscript-to-bibliography synchronization.
- Clean reproduction transcript.
- Final artifact/package review.
- Final arXiv category, license, export format, and human approval.
- Final claim-to-evidence audit after any future manuscript or bibliography edits.

PDF/arXiv export remains paused until the manuscript text and final figures are ready.

## Status

The current manuscript text is coherent and claim-safe for continued Word-first human review. Figure quality is intentionally out of scope because the current figures are placeholders only. The paper remains not submission-ready.
