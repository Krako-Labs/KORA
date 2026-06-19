# Project Operating System

Status: reusable public-safe documentation package.

This directory extracts KORA's Goal 071 breadcrumb and review-hub pattern into a reusable Project Operating System package.

## Purpose

The Project Operating System helps a project answer quickly:

- What is the current state?
- What was the latest completed task?
- What reports matter most?
- What evidence matters most?
- What claims are supported?
- What risks remain?
- What should happen next?
- How should a planning agent, execution agent, reviewer, or project owner resume work?

`OPEN_THIS_FIRST.md` is the single source of human continuation. It should be the shortest reliable answer to "what should I read first and what should happen next?"

`REVIEW_HUB.md` is the detailed second stop. It should contain the evidence, reports, risks, claim boundaries, and continuation workflow behind the breadcrumb.

It is designed for projects that may have:

- a public GitHub repo.
- a private GitHub repo.
- local-only project context.
- generated evidence.
- reports.
- claim boundaries.
- recurring task-based work.

## Required Files

Every adopting project should create:

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- an ADR for the breadcrumb/review-hub decision.
- a project operating standard or runbook.

Templates:

- [OPEN_THIS_FIRST template](templates/OPEN_THIS_FIRST.template.md)
- [REVIEW_HUB template](templates/REVIEW_HUB.template.md)
- [ADR-001 template](templates/ADR-001-project-breadcrumb-standard.template.md)

## Optional Files

Optional but recommended:

- [Report template](templates/REPORT.template.md)
- [Evidence template](templates/EVIDENCE.template.md)
- [Claim registry template](templates/CLAIM_REGISTRY.template.md)
- [Project bootstrap checklist template](templates/PROJECT_BOOTSTRAP_CHECKLIST.template.md)

## Prompts

- [Project initialization prompt](prompts/project-initialization-prompt.md)
- [Project gap analysis prompt](prompts/project-gap-analysis-prompt.md)
- [Project documentation refresh prompt](prompts/project-doc-refresh-prompt.md)

## Operating Standard

Use [Project Operating Standard v0](project-operating-standard-v0.md) as the adoption runbook.

## Public/Private Boundary

The templates distinguish:

- public GitHub repo: public-safe source, docs, issues, releases, and evidence.
- private GitHub repo: strategy, credentials-free operational plans, and non-public context.
- local-only project context: uncommitted notes, raw logs, environment details, and temporary diagnostics.

Never copy private repo content or local-only context into a public repo unless it has been reviewed and rewritten as public-safe.

## KORA Source Pattern

This package generalizes:

- [KORA OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [KORA REVIEW_HUB.md](../../REVIEW_HUB.md)
- [KORA Project Documentation Operating Standard](../runbooks/project-documentation-operating-standard.md)
- [KORA ADR-001](../adr/ADR-001-project-breadcrumb-and-review-hub-standard.md)

## Adoption Rule

After adoption, every completed task should update:

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

unless the task explicitly exempts breadcrumb maintenance.
