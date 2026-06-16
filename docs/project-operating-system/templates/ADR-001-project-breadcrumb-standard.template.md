# ADR-001: Project Breadcrumb And Review Hub Standard

Status: `[proposed / accepted / superseded]`.

Date: `[YYYY-MM-DD]`.

## Context

`[Project name]` has accumulated or expects to accumulate reports, evidence, decisions, and task history across public, private, and local-only contexts.

Historical reports are useful, but they do not reliably answer current-state questions for a reviewer, planning agent, execution agent, or project owner.

## Decision

The project will maintain:

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

The project will update both files after every completed task unless explicitly exempted.

## Why Reports Are Not Sufficient

Reports explain what happened during a task. They do not consistently identify:

- the current state.
- the latest completed task.
- the primary report.
- the primary evidence.
- supported and unsupported claims.
- current risks.
- the recommended next task.
- how to resume.

## Why The Review Hub Exists

`REVIEW_HUB.md` is the durable current-state layer. It should help a reviewer, planning agent, execution agent, or project owner orient quickly without reconstructing the full task history.

## Public / Private / Local Boundary

| Context | Rule |
| --- | --- |
| Public GitHub repo | Public-safe docs, code, reports, and evidence only. |
| Private GitHub repo | Do not expose private contents in public files. |
| Local-only project context | Do not commit raw logs, local diagnostics, or environment details. |

## Consequences

Positive:

- faster review.
- clearer handoff.
- lower risk of stale public claims.
- lower dependence on private memory.

Costs:

- every task has a small maintenance burden.
- stale breadcrumbs can mislead reviewers.
- summaries must stay bounded and must not replace evidence files.

## Future Requirement

Every completed task must update:

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

Minimum update:

- latest task.
- branch/worktree/commit.
- primary report.
- primary evidence.
- changed risks.
- recommended next task.

## Claim Boundary

This ADR does not create product, performance, savings, readiness, or superiority claims. It creates a documentation operating requirement.
