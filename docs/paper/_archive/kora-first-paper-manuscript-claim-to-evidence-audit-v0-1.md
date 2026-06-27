# KORA First Paper Manuscript Claim-to-Evidence Audit v0.1

Audit date: 2026-05-13

## Purpose

This audit checks manuscript claim safety while preparing manuscript v0.4 as a submission-candidate draft. It does not create production evidence, does not complete artifact approval, and does not make the paper submission-ready.

## Source Files Reviewed

- `docs/paper/kora-first-paper-manuscript-v0-3.md`
- `docs/paper/kora-first-paper-manuscript-v0-4.md`
- `docs/paper/kora-first-paper-claim-boundary.md`
- `docs/paper/kora-first-paper-final-bibliography-claim-audit-v0-1.md`
- `docs/paper/kora-first-paper-submission-readiness-gate-v0-1.md`
- `docs/paper/kora-first-paper-evidence-summary.md`

## Claim Categories Checked

- production cost reduction proof
- real API-cost reduction proof
- production benchmark proof
- full runtime-integrated real-provider benchmark evidence
- broad workload superiority proof
- energy reduction evidence
- formal government validation
- signed partner validation
- guaranteed adoption or funding
- formal artifact approval
- paper submission readiness

## Bounded Claim

The bounded claim remains:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

## Evidence Path

The bounded claim remains tied to:

- the deterministic-heavy benchmark workload;
- 100 total tasks;
- 100 baseline model calls;
- 20 KORA-controlled model calls;
- 80 avoided simulated model invocations;
- zero mismatches;
- local public benchmark documentation and validation commands.

The synthetic customer-support local/no-network validation remains evidence that KORA can measure avoided model-call events in synthetic workloads. It is not production evidence.

## Unsafe Wording Found and Corrected

No unsupported production, API-cost, energy, broad superiority, formal approval, or submission-readiness claim was found in manuscript v0.3.

Mechanical tightening in manuscript v0.4:

- The manuscript now states that v0.4 synchronizes references with the current preliminary BibTeX state.
- `[R02]` background references were removed because `[R02]` remains still-not-eligible for preliminary BibTeX.
- Limitations now state that full BibTeX remains incomplete.

## Non-Claims That Must Remain

The manuscript must continue to state or preserve:

- no production cost proof;
- no real API-cost proof;
- no production benchmark proof;
- no full runtime-integrated real-provider benchmark evidence;
- no energy measurement;
- no broad workload superiority claim;
- no formal artifact evaluation or approval;
- no production validation;
- no superiority over cited systems.

## Limitations That Must Stay in Manuscript

- synthetic workloads;
- limited workload diversity;
- no production traffic;
- no real provider validation;
- no real API-cost proof;
- no production benchmark proof;
- no full runtime-integrated real-provider benchmark evidence;
- no energy measurement;
- no user study;
- no broad workload superiority claim;
- preliminary reference integration;
- full BibTeX remains incomplete;
- final citation style remains pending.

## Status

Manuscript v0.4 preserves the current claim boundary. The paper remains not submission-ready because bibliography, formatting/export, artifact/reproducibility, and final human-review blockers remain open.
