# KORA Core PR Packet v0

Status: draft PR packet. This document does not open a PR and does not authorize push, merge, release, or tag actions.

## Recommended PR Title

docs: realign KORA Core around KRK and routable workloads

## Recommended PR Summary

This PR realigns the public KORA documentation around the updated hierarchy:

- KORA is the umbrella for making AI workloads routable.
- KORA Core is the planned open-source AI workload execution layer.
- KRK is the deterministic-first routing kernel inside KORA Core.
- The current public implementation is a KRK-oriented alpha with bounded deterministic-heavy benchmark evidence.

The PR adds public-safe documentation packages for:

- KRK definition, quickstart, architecture, and capability matrix.
- KORA Core inspect, compare, run, and report alpha surface definitions.
- Workload Spec, Target Registry, and Evidence Report architecture.
- KRK benchmark methodology, performance table package, reproducibility matrix, and claim boundaries.
- KRK technical paper draft package.
- KORA naming, repo restructuring, post-July roadmap, and community strategy.
- July 31 report, video, plan, evidence, readiness, and risk/gap package.
- public-safe KRK matrix workload fixtures.

## Recommended PR Body

```markdown
## Summary

This PR realigns the public KORA docs around KORA Core, KRK, and routable AI workloads.

KORA is now presented as the umbrella for making AI workloads routable. KORA Core is the planned open-source AI workload execution layer. KRK, the KORA Routing Kernel, is the deterministic-first routing kernel inside KORA Core and the current public alpha focus.

The change adds documentation packages for strategy, product surface, architecture, evidence, paper drafting, July 31 deliverables, and public merge readiness. It also adds small public-safe KRK matrix workload fixtures for future route-selectivity evaluation.

## Current Implementation Boundary

- Current public implementation is KRK-oriented.
- KORA Core `inspect`, `compare`, `run`, and `report` are defined as alpha surface and roadmap unless explicitly implemented.
- Current top-level CLI remains example-oriented.
- KRK `route`, `explain`, `benchmark`, and `report` are documented primitives, not all verified as top-level commands on this base.

## Evidence Boundary

The current bounded evidence remains:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

The PR does not claim production readiness, broad workload superiority, provider replacement, model serving replacement, infrastructure reduction, final competition results, formal external validation, 10x savings, or customer-level savings.

## Validation

- `python3 -m pytest`
- `git diff --check`
- `find docs -maxdepth 4 -type f | sort`
- public/private boundary scans
- claim boundary scans
- original dirty repo status check
- private status check
- external project status checks

## Notes

This is documentation and planning work. It does not rename repos, split repos, create repos, push, open a PR, merge, release, or tag.
```

## Reviewer Checklist

Reviewers should verify:

- README hero accurately reflects KORA Core and KRK.
- README does not present future commands as implemented.
- docs index links resolve.
- KORA, KORA Core, KRK, and Krako are used consistently.
- claim boundary docs preserve bounded benchmark wording.
- evidence docs clearly mark missing measurements as not measured yet.
- paper docs do not imply submission readiness.
- July 31 docs read as planning/readiness material, not final results.
- repo restructuring docs do not imply repo actions have happened.
- example workload fixtures are public-safe and do not leak oracle labels into router inputs in future code.
- broad scan matches are either pre-existing or documented.

## Files To Review First

1. `README.md`
2. `docs/README.md`
3. `docs/strategy/kora-routable-ai-workloads-master-plan-v0-1.md`
4. `docs/product/kora-routing-kernel-definition-v0.md`
5. `docs/product/kora-core-alpha-surface-v0.md`
6. `docs/evidence/krk-performance-table-v0.md`
7. `docs/evidence/krk-claim-boundary-table-v0.md`
8. `docs/reports/july31-report-outline-v0.md`
9. `docs/reports/kora-core-public-merge-readiness-v0.md`
10. `docs/reports/kora-core-public-boundary-audit-v0.md`

## Known Limitations To Call Out In PR

- KORA Core workflow verbs are not fully implemented.
- Current CLI is still example-oriented.
- Extended KRK matrix evaluator is not implemented.
- Route accuracy metrics are not measured yet.
- Bounded GPU-routed subset measurement is methodology-only.
- Provider-backed sample validation remains future work.
- Historical repo files still contain older claim-boundary and local-path scan hits.

## Merge Recommendation

Recommended status:

- mergeable after maintainer review if validation remains green on the final branch head.

This packet recommends a normal documentation PR review rather than immediate merge.
