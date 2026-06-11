# July 31 Risk And Gap Register v0

Status: public-safe risk register. This document identifies gaps and mitigations for the July 31 package.

## Purpose

The July 31 package should be credible because it is explicit about current limitations. This register separates current evidence from gaps that need follow-up work.

Severity:

- High: could mislead reviewers or block a credible package.
- Medium: important gap, but manageable with clear wording.
- Low: useful improvement, not package-blocking.

## Risk Register

| Risk / Gap | Severity | Current Status | Mitigation |
| --- | --- | --- | --- |
| KORA Core `inspect`, `compare`, `run`, and `report` are not fully implemented as first-class workflows. | High | Defined as alpha surface and roadmap. | Label them as planned KORA Core workflows; implement small tested paths in future goals. |
| Top-level CLI does not expose all KRK primitive names as commands. | High | Current CLI is example-oriented. | Document exact working command forms; avoid claiming future commands are implemented. |
| KRK extended matrix route metrics are not measured yet. | High | Matrix fixtures and methodology exist. | Build dry-run evaluator and generate route accuracy tables. |
| GPU-routed subset measurement is methodology-only. | High | Public docs define the method but not measured subset results. | Run bounded public-safe subset measurement only after evaluator and artifact policy are ready. |
| H100 measurement values are not included in the current public package. | Medium | Current performance table marks them not included. | Keep public summary sanitized; add values only if public-safe, reproducible, and approved. |
| Provider evidence is incomplete. | Medium | Provider validation remains future work. | Add small provider-routed sample validation with offline-safe tests and explicit boundaries. |
| Broad workload representativeness is not proven. | High | Current measured evidence is deterministic-heavy and simulated. | Add mixed-realistic, cache-heavy, GPU-heavy, adversarial, and service-replay profiles over time. |
| Workload Spec is not yet enforced by code. | Medium | Architecture doc exists. | Add schema validation and migrate fixtures gradually. |
| Target Registry is not yet executable. | Medium | Architecture doc exists. | Add public-safe registry examples and dry-run target selection. |
| Evidence Report is not yet generated as a first-class KORA Core artifact. | Medium | Schema doc exists. | Generate structured reports from inspect/compare/run outputs. |
| Repo naming is not yet restructured. | Low | Strategy recommends no immediate split. | Keep naming clear in docs; revisit after KORA Core alpha stabilizes. |
| Studio dirty work remains separate from this clean worktree. | Medium | Original repo has separate dirty Studio work. | Keep this goal scoped to the clean worktree; do not mix Studio changes into the July 31 package. |
| Old public docs include historical local paths and private-adjacent planning references. | Medium | Existing broad scans may find pre-existing matches. | Distinguish pre-existing matches from new package files; clean historical docs in a separate goal if needed. |
| Report/video could sound final or promotional. | High | Current package is planning/readiness only. | Use status language, limitations, and claim boundary tables in report and storyboard. |
| Evidence wording could be overgeneralized from one benchmark. | High | Approved wording is bounded. | Preserve the exact deterministic-heavy, simulated-invocation qualifiers. |

## Current Known Gaps

### Unimplemented KORA Core Workflow

The inspect, compare, run, and report workflow is the intended KORA Core surface. It should not be described as fully implemented.

Mitigation:

- describe as alpha surface and roadmap.
- implement small read-only or dry-run paths next.
- keep command docs synchronized with tests.

### Top-Level CLI Mismatch

KRK primitives are route, explain, benchmark, and report. The current top-level CLI is example-oriented and does not expose all of these primitive names directly.

Mitigation:

- document exact working command forms.
- avoid unverified CLI examples.
- add aliases only when tests prove they work.

### H100 Measurement Gaps

Current public docs define bounded GPU-routed subset methodology, but the current public package does not include public-safe task count, runtime, throughput, or memory values.

Mitigation:

- keep H100 measurement language at methodology or not-included status until public-safe values are ready.
- publish only sanitized summaries.
- never publish raw logs, local-only paths, server details, credentials, or private resource identifiers.

### Provider Evidence Gaps

Provider-routed validation is not yet enough to support broad claims.

Mitigation:

- add small public-safe provider sample validation.
- keep external calls optional or fixture-backed for tests.
- mark provider-backed results separately from simulated results.

### Broad Workload Representativeness

The deterministic-heavy benchmark is useful but narrow.

Mitigation:

- add multi-profile matrix evaluation.
- include mixed-realistic, cache-heavy, GPU-heavy, adversarial, and service-replay profiles.
- report profile-level limitations.

### Repo Naming And Structure

The current repo is still a single public repo. Naming docs now define KORA, KORA Core, KRK, and Krako, but no repo restructuring has happened.

Mitigation:

- keep one repo for the near term.
- revisit umbrella + core split only after KORA Core alpha stabilizes.
- do not announce repo splits before approval and concrete migration plans.

### Studio Dirty Work Separation

The original public repo contains separate dirty Studio work. This July 31 package is built in the clean goal worktree.

Mitigation:

- keep the July 31 package scoped to this clean worktree.
- do not import unreviewed dirty Studio changes.
- handle Studio work in a separate goal if needed.

## Package-Level Mitigation Plan

Before external use:

1. run the full test suite.
2. run public/private scans.
3. scan only the July 31 package files for private terms and unsupported claims.
4. verify demo commands.
5. verify all benchmark values against public evidence docs.
6. label every roadmap item as planned, future, pending, or not measured yet.
7. preserve the approved bounded benchmark wording.

## Non-Goals

This package does not:

- submit a report.
- create a video.
- create a PDF.
- create final competition-result claims.
- claim production readiness.
- claim production savings.
- claim provider replacement.
- publish raw GPU artifacts.
