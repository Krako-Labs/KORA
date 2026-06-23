# Codex Risk Classification

Status: repo-local risk model for KORA Codex work blocks.

## Risk Levels

### Low Risk

Low-risk work may be completed autonomously through PR open when the prompt permits it.

Examples:

- validators.
- tests.
- local runners and verifiers.
- report templates.
- breadcrumbs.
- internal runbooks.
- approval packet checkers.
- deterministic consistency checkers.

Low-risk work still needs validation, self-review, claim-boundary audit, and final classification.

### Medium Risk

Medium-risk work may proceed to PR, but it must not be marked `merge-ready` unless scope and claim boundaries are clearly unchanged.

Examples:

- README minor updates.
- examples guide updates.
- install guide improvements.
- user-facing CLI message changes.
- validation profile registry changes.
- source-install readiness wording.

Medium-risk work commonly ends as `needs-cto-review` when public positioning, user-facing language, or future automation authority is involved.

### High Risk

High-risk work must stop before execution unless the prompt explicitly authorizes it. If encountered during work, classify as `needs-cto-review` or `blocked`.

Examples:

- public positioning changes.
- claim expansion.
- benchmark interpretation.
- H100/provider/server execution.
- release, PyPI, package publication, or GitHub Release work.
- major public docs rewrite.
- file movement, archive, delete, or rename.
- repository settings.
- costs or external side effects.
- actual multi-agent execution.
- auto-merge or self-merging behavior.

## Classification Rule

Codex pass is not merge-ready pass. Passing validation commands can support `merge-ready`, but validation alone is insufficient when claim, evidence, public-positioning, or approval-gate risk remains.

## Claim Boundary Reminder

Risk classification must preserve that KORA work does not claim output-quality proof, broader workload representativeness proof, production proof, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, or published `getkora` unless separately approved and evidenced.
