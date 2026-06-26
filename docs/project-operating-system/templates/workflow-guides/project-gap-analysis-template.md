# Project Gap Analysis Prompt

Use this prompt to identify gaps in a project that already has a breadcrumb and review hub.

```text
You are acting as the planning agent for a project gap analysis task.

Goal:
Review the current project state and produce a public-safe gap analysis.

Start by reading:
- OPEN_THIS_FIRST.md
- REVIEW_HUB.md
- primary evidence package
- primary claim registry, if present
- recent task reports linked from REVIEW_HUB.md

Analyze:
- current state
- latest completed task
- primary reports
- primary evidence
- supported claims
- unsupported claims
- risks
- remaining evidence gaps
- documentation gaps
- workflow or CLI gaps
- public/private boundary risks

Distinguish:
- public GitHub repo facts
- private GitHub repo facts
- local-only project context

Do not expose:
- private paths
- credentials
- hostnames
- raw access details
- raw provider responses
- raw infrastructure logs
- account IDs
- billing details
- local-only notes

Create:
- docs/reports/<project-gap-analysis-report>.md

Update:
- OPEN_THIS_FIRST.md
- REVIEW_HUB.md

Report must include:
- current state summary
- gap table
- risk table
- claim-boundary review
- recommended next tasks
- validation and scan results

Do not implement feature work unless explicitly requested.
Commit only public-safe files.
```
