# KRK Goal 071 Project Breadcrumb Standard v0

Status: public-safe documentation operating standard established.

Final classification: `PROJECT_BREADCRUMB_STANDARD_ESTABLISHED`

## Motivation

KORA now contains enough evidence, reports, generated summaries, benchmarks, validation artifacts, and implementation history that a reviewer should not need to reconstruct current state from many historical files.

Goal 071 creates the project memory layer:

- a fast-start breadcrumb.
- a review hub.
- an operating standard.
- an ADR requiring future maintenance.

## Files Created

- [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [REVIEW_HUB.md](../../REVIEW_HUB.md)
- [Project Documentation Operating Standard](../runbooks/project-documentation-operating-standard.md)
- [ADR-001 project breadcrumb and review hub standard](../adr/ADR-001-project-breadcrumb-and-review-hub-standard.md)

## Files Updated

- [Documentation index](../README.md)

## History Backfill Scope

This Goal backfills recent history sufficient for project understanding. It does not attempt a full chronological reconstruction.

Backfilled Goals:

- Goal 044
- Goal 045
- Goal 046
- Goal 050
- Goal 053
- Goal 054
- Goal 058C
- Goal 059
- Goal 060
- Goal 070A
- Goal 070B
- Goal 070C
- Goal 071

## Review Workflow

Recommended reviewer path:

1. Read [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md).
2. Read [REVIEW_HUB.md](../../REVIEW_HUB.md).
3. Read [KRK evidence package v0](../evidence/krk-evidence-package-v0.md).
4. Read only the linked report relevant to the review question.
5. Verify claim boundaries before approving public language.

## Continuation Workflow

Recommended future Goal path:

1. Verify KORA identity and branch.
2. Read [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md).
3. Read [REVIEW_HUB.md](../../REVIEW_HUB.md).
4. Read only the relevant linked reports/evidence.
5. Complete scoped work.
6. Run validation and scans.
7. Update [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md) and [REVIEW_HUB.md](../../REVIEW_HUB.md).
8. Commit only public-safe files.

## Future Maintenance Rule

Every completed Goal must update:

- [OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [REVIEW_HUB.md](../../REVIEW_HUB.md)

unless explicitly exempted.

Minimum update:

- latest completed Goal.
- current branch and commit state.
- new primary report/evidence links.
- changed risks or evidence gaps.
- recommended next Goal.

## Limitations

- This is a documentation operating layer, not new technical evidence.
- The Goal history is intentionally partial.
- Current commit references reflect the branch state when the breadcrumb was created; future Goals must refresh them.
- The breadcrumb layer summarizes evidence and points to source reports. It does not replace detailed evidence packages.

## Claim Boundary

This Goal supports:

- KORA has a public project breadcrumb layer.
- KORA has a review hub for current-state navigation.
- KORA has a documented rule that future completed Goals update the breadcrumb layer.

This Goal does not support:

- production readiness.
- production cost reduction.
- customer savings.
- energy reduction.
- broad workload superiority.
- real API/GPU cost reduction.
- provider superiority.
- H100 superiority.
- release, tag, or PR readiness by itself.
