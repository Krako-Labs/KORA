# Project Initialization Prompt

Use this prompt to initialize the Project Operating System in a new or existing project.

```text
You are acting as the execution agent for a project documentation initialization task.

Goal:
Create a public-safe Project Operating System layer for this project.

Use neutral roles:
- planning agent
- execution agent
- reviewer
- project owner

Required context to inspect:
- public GitHub repo, if available
- private GitHub repo, if available and authorized
- local-only project context, if available and authorized
- existing README, docs, reports, evidence, and claim-boundary files

Public/private rules:
- Do not expose private paths, credentials, hostnames, raw access details, raw provider responses, raw infrastructure logs, account IDs, billing details, or local-only notes.
- Do not turn private context into public claims.
- Summarize only public-safe facts in public files.

Create or update:
- OPEN_THIS_FIRST.md
- REVIEW_HUB.md
- docs/adr/ADR-001-project-breadcrumb-standard.md
- docs/runbooks/project-operating-standard.md
- docs/reports/<initialization-report>.md

OPEN_THIS_FIRST.md must include:
- current status
- latest task
- current branch/worktree/commit
- primary report
- primary evidence
- risks
- recommended next task
- how to resume

REVIEW_HUB.md must include:
- project identity
- public/private/local source-of-truth table
- current state summary
- recent task history
- evidence index
- report index
- claim boundary summary
- current workflow surface
- current risks
- remaining evidence gaps
- recommended next tasks
- resume instructions for planning agent, execution agent, reviewer, and project owner

Validation:
- run available tests or documentation checks
- run link/path sanity checks
- scan public files for private material and unsupported claims

Commit only public-safe files.
Do not push, open PR, tag, or release unless explicitly requested.
```
