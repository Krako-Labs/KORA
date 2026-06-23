# Codex Approval Packet

Status: standard KORA PR approval packet format.

## Required Packet Fields

Every Codex-owned work block should provide:

- decision needed.
- risk level.
- final status classification.
- changed files.
- validation summary.
- repair attempts.
- failures encountered.
- self-review summary.
- claim-boundary audit.
- forbidden-action audit.
- uncertainty notes.
- Codex recommendation.
- Albert action options: Merge / Request R1 / Stop / CTO Review.

## Packet Template

```text
Decision needed:
Risk level:
Final status classification:
Changed files:
Validation summary:
Repair attempts:
Failures encountered:
Self-review summary:
Claim-boundary audit:
Forbidden-action audit:
Uncertainty notes:
Codex recommendation:
Albert action options: Merge / Request R1 / Stop / CTO Review
```

## Recommendation Guidance

Codex may recommend `Merge` only when final classification is `merge-ready`. If final classification is `needs-r1`, recommend `Request R1`. If final classification is `needs-cto-review`, recommend `CTO Review`. If final classification is `blocked`, recommend `Stop` or `CTO Review`.

## Claim Boundary Reminder

Approval packets must explicitly preserve that the PR does not claim output-quality proof, broader workload representativeness proof, production proof, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, or published `getkora` unless separately approved and evidenced.
