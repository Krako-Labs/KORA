# ADR-001: Project Breadcrumb and Review Hub Standard

Status: accepted.

Date: 2026-06-16.

## Context

KORA has accumulated substantial public documentation:

- evidence packages.
- generated summaries.
- benchmark reports.
- validation reports.
- implementation reports.
- risk registers.
- release-candidate decision packages.
- first-value CLI reports.

These documents are valuable, but they are historical and distributed. A reviewer, owner, future ChatGPT session, future Codex session, or new contributor should not need to reconstruct current state by reading every report in chronological order.

## Decision

KORA will maintain a root-level breadcrumb and review hub:

- [../../OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [../../REVIEW_HUB.md](../../REVIEW_HUB.md)

KORA will also maintain the operating runbook:

- [Project Documentation Operating Standard](../runbooks/project-documentation-operating-standard.md)

Every completed Goal must update `OPEN_THIS_FIRST.md` and `REVIEW_HUB.md` unless explicitly exempted.

## Why Reports Are Not Sufficient

Reports are append-only historical artifacts. They answer what a specific Goal did.

They do not reliably answer:

- What is the current state?
- What was the last completed Goal?
- Which evidence matters most now?
- Which reports should be read first?
- What claims are supported today?
- What risks remain?
- What should happen next?

KORA needs both historical reports and a current-state layer.

## Why The Review Hub Exists

`REVIEW_HUB.md` exists to make the project reviewable in minutes.

It gives:

- project identity.
- branch and public truth.
- current state summary.
- recent Goal history.
- evidence and report indexes.
- claim boundaries.
- first-value workflow.
- risks and gaps.
- continuation instructions.

This is especially important for long-lived branches, repeated supervised Goals, and handoffs between human reviewers and AI-assisted coding sessions.

## Consequences

Positive consequences:

- faster reviewer onboarding.
- lower risk of stale or unsupported public claims.
- clearer continuation path after long sessions.
- less dependence on private or local-only memory.
- better PR readiness because key evidence is indexed.

Costs:

- each future Goal has a small documentation maintenance burden.
- breadcrumbs can become stale if a Goal forgets to update them.
- current-state summaries must stay bounded and must not replace evidence files.

## Future Requirement

Every future completed Goal must update:

- [../../OPEN_THIS_FIRST.md](../../OPEN_THIS_FIRST.md)
- [../../REVIEW_HUB.md](../../REVIEW_HUB.md)

Minimum update:

- latest completed Goal.
- current commit or branch state.
- new primary report/evidence links.
- changed risks or evidence gaps.
- recommended next Goal.

If a Goal intentionally does not update the breadcrumb layer, the final report must state the exemption reason.

## Public-Safety Requirement

The breadcrumb layer must not include private paths, credentials, hostnames, raw access details, raw provider responses, raw GPU logs, local-only runtime notes, or unsupported claims.

The breadcrumb layer must preserve the current KORA claim boundary:

- no production readiness claim.
- no production cost reduction claim.
- no customer savings claim.
- no energy reduction claim.
- no broad workload superiority claim.
- no real API/GPU cost reduction claim.
- no provider superiority claim.
- no H100 superiority claim.
- no replacement claim for model serving, provider routing, or GPU serving systems.
