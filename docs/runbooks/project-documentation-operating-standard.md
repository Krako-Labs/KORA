# Project Documentation Operating Standard

Status: KORA adaptation of Project Documentation Operating Standard v0.1.

## Purpose

KORA accumulates evidence, reports, generated summaries, implementation history, and claim-boundary decisions. Reports are necessary, but reports alone do not provide a durable project memory layer.

This standard defines the lightweight breadcrumb layer that every future KORA Goal should maintain.

## Standard

Every project using this standard should keep two root-level files:

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

KORA also records the standard decision in:

- [ADR-001 project breadcrumb and review hub standard](../adr/ADR-001-project-breadcrumb-and-review-hub-standard.md)

## OPEN_THIS_FIRST.md

`OPEN_THIS_FIRST.md` is the fast-start breadcrumb.

It should answer:

- What is the current status?
- What branch and commit should be considered current for the active work?
- What was the last completed Goal?
- What reports matter most?
- What evidence matters most?
- What is the current value proposition?
- What should happen next?
- How should a reviewer or future session continue?

It should be short enough to read first.

## REVIEW_HUB.md

`REVIEW_HUB.md` is the durable review and continuation hub.

It should include:

- project identity.
- public truth.
- active branch and worktree label.
- current state summary.
- recent Goal history table.
- evidence index.
- report index.
- claim boundary summary.
- current CLI surface.
- current first-value path.
- current risks.
- remaining evidence gaps.
- recommended next Goals.
- instructions for resuming with ChatGPT.
- instructions for resuming with Codex.

It should be comprehensive enough that a new reviewer can orient without reading every historical report.

## Required Goal Maintenance

Every completed Goal must update:

- [../../OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [../../REVIEW_HUB.md](../../REVIEW_HUB.md)

unless the Goal explicitly exempts breadcrumb maintenance.

At minimum, update:

- last completed Goal.
- current commit if known after commit, or note the pre-commit state if writing before commit.
- new primary reports or evidence.
- changed risks or evidence gaps.
- recommended next Goal.

## Review Workflow

For a reviewer:

1. Read [../../OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md).
2. Read [../../REVIEW_HUB.md](../../REVIEW_HUB.md).
3. Open only the linked report or evidence package relevant to the review.
4. Verify claim boundaries before approving public language.

## Continuation Workflow

For an implementation or documentation Goal:

1. Verify repository identity, branch, and status.
2. Read [../../OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md).
3. Read [../../REVIEW_HUB.md](../../REVIEW_HUB.md).
4. Read the linked docs relevant to the new Goal.
5. Complete the scoped work.
6. Run validation and scans.
7. Update the breadcrumb files.
8. Commit only public-safe files.

## Public-Safety Boundary

Breadcrumb and hub files must not include:

- private paths.
- credentials.
- hostnames.
- raw access details.
- raw provider responses.
- raw GPU logs.
- local-only runtime notes.
- unsupported production, savings, superiority, or readiness claims.

## KORA-Specific Claim Boundary

KORA may state:

- KORA makes AI workloads routable.
- KRK is the deterministic-first routing kernel inside KORA Core.
- KORA has public-safe first-value CLI workflows.
- KORA has bounded public evidence for routing, runtime dry-run evaluation, provider-path validation, H100 harness execution, expanded H100 representativeness, and output fidelity.

KORA must not state without future evidence:

- production readiness.
- production cost reduction.
- customer savings.
- energy reduction.
- broad workload superiority.
- real API/GPU cost reduction.
- provider superiority.
- H100 superiority.
- replacement of model serving, provider routing, or GPU serving systems.

## Anti-Pattern

Do not make every report a new starting point. Reports are historical artifacts. The breadcrumb layer is the current-state entrypoint.

Do not replace detailed evidence packages with the breadcrumb layer. The breadcrumb layer points to evidence; it does not substitute for it.
