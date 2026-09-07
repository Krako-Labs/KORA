# Task027 — S5 first real KORA Solution integration and economics

Status: active.
Base: `53ab9bd6323f7c1109a06a26270e432e8908c00a`.

## Objective

Use an independently developed Specul.AI Content OS editorial workflow as the first bounded real-service dogfooding workload for KORA. Preserve Specul as an independent upstream. Measure only the incremental effect of KORA routing/reuse/local execution relative to Specul's existing deterministic control plane.

## Frozen upstream

- Product: Specul.AI Content OS / Publishing.
- Canonical upstream revision for S5: `de2f302326bb79ca541ccab099295c73fe2dce06`.
- Upstream remains read-only during this sprint.
- Existing Specul deterministic validation/state/versioning work is baseline capability and must not be counted as KORA savings.

## In scope

1. Define a provider-neutral editorial workload contract and telemetry schema.
2. Add a bounded Specul adapter that accepts immutable brief/research/evidence inputs without modifying the Specul repo.
3. Support explicit execution policies for baseline-frontier and KORA-routed execution using already configured adapters/resources.
4. Record per-node execution kind, provider/model identity label, calls, input/output tokens, elapsed time, reuse, and quality checks.
5. Calibration on the already-reviewed upstream article is evaluator/harness validation only; no savings claim.
6. Run at least one fresh unseen editorial workload through both paths when configured resources are available.
7. Run exact-repeat and changed-input cases to verify reuse/invalidation boundaries.
8. Preserve failures and unfavorable results.
9. Produce a bounded S5 report and approval packet.

## Quality floor

The two compared paths receive the same workload inputs and are judged by the same structural/evidence requirements. No KORA result passes merely because it is cheaper. Existing Specul deterministic controls are not disabled in the baseline.

## Hard boundaries

- No write to the Specul.AI canonical repository or its production SQLite database.
- No Substack/social publication or browser mutation.
- No H100 use in S5 unless separately required and re-authorized.
- No broad production, customer-savings, quality-superiority, representativeness, or hardware-superiority claim.
- Raw provider responses, credentials, private endpoints, and private content are local evidence only.
- No Pack is promoted from this one Solution; only Pack candidates may be recorded.

## Done condition

S5 closes only when the integration contract is tested, calibration succeeds, a fresh baseline/KORA comparison is either completed or explicitly blocked with the exact resource reason, repeat/changed-input semantics are tested, full regression passes, and the evidence/claim boundary is reviewed. A negative economics result is still a valid S5 result.
