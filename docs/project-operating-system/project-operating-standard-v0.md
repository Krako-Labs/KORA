# Project Operating Standard v0

Status: reusable project operating standard.

## Why This Exists

Projects with many tasks, reports, and generated artifacts need a current-state layer. Historical reports explain what happened, but they do not reliably tell a new reviewer or execution agent what matters now.

The Project Operating System creates a small durable layer that keeps current state, evidence, risks, claims, and next actions easy to find.

## Required Files

Every adopting project should maintain:

| File | Purpose |
| --- | --- |
| `OPEN_THIS_FIRST.md` | Single source of human continuation and fast-start breadcrumb for the current state. |
| `REVIEW_HUB.md` | Detailed second stop with evidence, reports, risks, claims, and continuation instructions. |
| `docs/adr/ADR-001-project-breadcrumb-standard.md` | Decision record explaining why the breadcrumb and review hub exist. |
| `docs/runbooks/project-operating-standard.md` | Project-specific operating standard. |

## Optional Files

Recommended optional files:

| File | Purpose |
| --- | --- |
| `docs/reports/<task-report>.md` | Task completion reports. |
| `docs/evidence/<evidence>.md` | Evidence summaries. |
| `docs/claims/claim-registry.md` | Supported, prohibited, and future claims. |
| `docs/runbooks/project-bootstrap-checklist.md` | New-project setup checklist. |

## Public/Private Rules

Classify context before writing:

| Context | Use | Public-safe handling |
| --- | --- | --- |
| Public GitHub repo | docs, public code, public evidence, public issues, releases | Include only public-safe summaries and reproducible artifacts. |
| Private GitHub repo | doctrine, strategy, private plans, private coordination | Do not quote or expose private content in public files. Rewrite into public-safe summaries only after review. |
| Local-only project context | raw logs, temporary diagnostics, environment notes, private runtime setup | Do not commit. Summarize only sanitized aggregate facts when allowed. |

Never commit:

- credentials.
- tokens.
- private keys.
- hostnames.
- private access details.
- raw provider responses.
- raw GPU or infrastructure logs.
- account IDs or billing details.
- unsupported public claims.

## ADR Rules

Create an ADR when the project adopts or changes:

- breadcrumb and review-hub structure.
- public/private boundary.
- evidence methodology.
- claim boundary policy.
- release or review process.

ADRs should include:

- status.
- context.
- decision.
- consequences.
- maintenance requirement.

## Evidence Rules

Evidence files should state:

- source inputs.
- method.
- run status.
- aggregate metrics.
- reproducibility command when safe.
- limitations.
- public/private boundary.
- claim boundary.

Evidence files should not contain raw private data.

## Claim Boundary Rules

Every project should maintain a claim boundary summary in `REVIEW_HUB.md` and, for larger projects, a claim registry.

Claims should be categorized as:

- supported now.
- allowed with caveats.
- not supported.
- future evidence required.

Claims must be tied to evidence. Do not turn plans, hopes, or private anecdotes into public claims.

## Runbook Rules

Runbooks should be action-oriented. They should include:

- when to use the runbook.
- prerequisites.
- exact commands or steps.
- validation gates.
- stop conditions.
- public/private boundaries.
- expected outputs.

## Task Completion Rules

Every completed task should update:

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

These are the required continuation files. `OPEN_THIS_FIRST.md` must remain the first stop for humans and agents. `REVIEW_HUB.md` must remain the detailed second stop.

Minimum update:

- latest task.
- current branch, worktree, and commit.
- primary report.
- primary evidence.
- changed risks.
- recommended next task.
- how to resume.

If a task is explicitly exempted, the final report should say why.

## Role Model

Use neutral roles:

- planning agent: scopes the work and identifies gaps.
- execution agent: performs implementation, validation, and artifact creation.
- reviewer: checks evidence, links, claims, and risk.
- project owner: decides priorities, approvals, releases, and public positioning.

Do not assume a specific vendor, tool, chat product, or local environment.

## Completion Checklist

Before committing a task:

- `OPEN_THIS_FIRST.md` updated or exemption recorded.
- `REVIEW_HUB.md` updated or exemption recorded.
- links checked.
- tests or validation run.
- whitespace/diff check run.
- public/private scan run.
- unsupported claims checked.
- only public-safe files staged.
