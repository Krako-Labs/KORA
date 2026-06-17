# Review Hub

Status: current project review and continuation hub.

Last updated by: `[latest task id or name]`.

Detailed second stop: read `OPEN_THIS_FIRST.md` first. This file is the durable review hub for evidence, reports, risks, claim boundaries, and continuation instructions.

## Project Identity

`[Project name]` is `[short public-safe project definition]`.

## Source Of Truth

| Context | Location | Boundary |
| --- | --- | --- |
| Public GitHub repo | `[owner/repo or n/a]` | Public-safe code, docs, issues, releases, and evidence only. |
| Private GitHub repo | `[owner/repo or n/a]` | Private doctrine, strategy, or coordination; do not quote into public files. |
| Local-only project context | `[exists / none]` | Raw logs, diagnostics, environment details, and notes; do not commit. |

## Current Branch / Worktree / Commit

- public truth branch: `[branch]`
- active branch: `[branch]`
- worktree label: `[label or n/a]`
- current commit: `[commit hash]`

## Current State Summary

`[Short current-state summary.]`

Current project has:

- `[capability / evidence / report]`
- `[capability / evidence / report]`
- `[capability / evidence / report]`

Current project does not yet have:

- `[gap]`
- `[gap]`

## Recent Task History

This is a sufficient recent history backfill, not a complete reconstruction.

| Task | Public result | Primary artifact |
| --- | --- | --- |
| `[Task]` | `[result]` | `[Artifact] - relative/path.md` |
| `[Task]` | `[result]` | `[Artifact] - relative/path.md` |

## Evidence Index

Primary evidence:

- `[Evidence package] - relative/path.md`
- `[Generated summary] - relative/path.md`

Evidence status:

| Evidence area | Status | Boundary |
| --- | --- | --- |
| `[area]` | `[measured / prepared / not run / planned]` | `[claim boundary]` |
| `[area]` | `[measured / prepared / not run / planned]` | `[claim boundary]` |

## Report Index

Current reviewer path:

- `[Report] - relative/path.md`
- `[Report] - relative/path.md`

Current implementation path:

- `[Report] - relative/path.md`
- `[Runbook] - relative/path.md`

## Claim Boundary Summary

Supported:

- `[supported claim]`
- `[supported claim]`

Allowed with caveats:

- `[bounded claim and caveat]`

Not supported:

- `[unsupported claim]`
- `[unsupported claim]`

Future evidence required:

- `[future claim requiring evidence]`

## Current CLI / Product / Workflow Surface

Current public workflow:

```bash
[command]
[command]
```

Current limitations:

- `[limitation]`
- `[limitation]`

## Current First-Value Path

`[Describe the shortest public-safe path to project value.]`

Expected result:

- `[metric or artifact]`
- `[metric or artifact]`

## Current Risks

| Risk | Severity | Mitigation | Blocks next step? |
| --- | --- | --- | --- |
| `[risk]` | `[low / medium / high]` | `[mitigation]` | `[yes / no / if undisclosed]` |

## Remaining Evidence Gaps

- `[gap]`
- `[gap]`

## Recommended Next Tasks

1. `[Task id]` - `[objective]`
2. `[Task id]` - `[objective]`
3. `[Task id]` - `[objective]`

## How To Resume With A Planning Agent

```text
Start by reading OPEN_THIS_FIRST.md and REVIEW_HUB.md.
Use the active branch listed in REVIEW_HUB.md.
Keep public/private and claim boundaries from REVIEW_HUB.md.
Propose the next task only after checking current risks and evidence gaps.
```

## How To Resume With An Execution Agent

1. Verify repository identity and branch.
2. Read `OPEN_THIS_FIRST.md`.
3. Read this file.
4. Read only the linked reports/evidence relevant to the task.
5. Implement the scoped change.
6. Run validation.
7. Update `OPEN_THIS_FIRST.md` and this file.
8. Commit only public-safe files.

## How A Reviewer Should Use This Hub

1. Check current state and latest task.
2. Read the relevant report and evidence links.
3. Verify public/private boundaries.
4. Verify supported and unsupported claims.
5. Record approval, caveats, or blockers.

## Maintenance Rule

Every completed task must update:

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`

unless the task explicitly exempts breadcrumb maintenance.
