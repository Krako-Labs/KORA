# July 31 Evidence Package Index v0

Status: public-safe index. This is a navigation package, not a new benchmark result.

## Purpose

This index lists the evidence, methodology, paper, KORA Core, and example artifacts that can support a July 31 report, plan, and video package.

Evidence should be described only at its documented strength. Missing metrics should remain marked as pending rather than inferred.

## Deterministic-Heavy Benchmark

Primary references:

- [KORA benchmark result v1 100](../benchmarks/kora_benchmark_result_v1_100.md)
- [v0.3.0 runtime evidence reviewer guide](v0.3.0-alpha-runtime-evidence-reviewer-guide.md)
- [KRK July 1 evidence summary v0](krk-july1-evidence-summary-v0.md)

Current supported values:

- total tasks: 100.
- deterministic/no-model tasks: 80.
- fallback/model-candidate tasks: 20.
- direct-baseline simulated model invocations: 100.
- KORA-controlled simulated model invocations: 20.
- avoided simulated model invocations: 80.
- deterministic mismatches: 0.

Approved bounded wording:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

## KRK Performance Table

Reference:

- [KRK performance table v0](../evidence/krk-performance-table-v0.md)

Use for:

- deterministic-heavy benchmark table.
- current not-measured-yet routing metric table.
- GPU-routed subset methodology status.
- H100 bounded measurement public-package status.
- claim boundary summary.

## KRK Evidence Package

Reference:

- [KRK evidence package v0](../evidence/krk-evidence-package-v0.md)

Use for:

- what counts as evidence.
- what does not count as evidence.
- reproducibility path.
- deterministic benchmark evidence.
- methodology vs measured result separation.

## KRK Reproducibility Matrix

Reference:

- [KRK reproducibility matrix v0](../evidence/krk-reproducibility-matrix-v0.md)

Use for:

- reviewer path.
- reproducible vs methodology-only distinction.
- current gap around executable matrix evaluation.

## KRK Claim Boundary Table

Reference:

- [KRK claim boundary table v0](../evidence/krk-claim-boundary-table-v0.md)

Use for:

- allowed statements.
- unsupported statements.
- benchmark wording.
- prohibited interpretations.

## KRK Technical Paper Draft

References:

- [KRK technical paper draft v0](../paper/krk-technical-paper-draft-v0.md)
- [KRK technical paper outline v0](../paper/krk-technical-paper-outline-v0.md)
- [KRK figures and tables plan v0](../paper/krk-figures-and-tables-plan-v0.md)
- [KRK paper claim boundary v0](../paper/krk-paper-claim-boundary-v0.md)
- [KRK paper next experiments v0](../paper/krk-paper-next-experiments-v0.md)

Use for:

- technical explanation.
- paper/technical note status.
- limitations.
- next experiments.

Do not describe the paper as submitted or accepted.

## KORA Core Alpha Docs

References:

- [KORA Core alpha surface v0](../product/kora-core-alpha-surface-v0.md)
- [KORA Core user workflow v0](../product/kora-core-user-workflow-v0.md)
- [KORA Core inspect definition v0](../product/kora-core-inspect-definition-v0.md)
- [KORA Core compare definition v0](../product/kora-core-compare-definition-v0.md)
- [KORA Core run definition v0](../product/kora-core-run-definition-v0.md)
- [KORA Core report definition v0](../product/kora-core-report-definition-v0.md)
- [KORA Core expansion plan v0](../product/kora-core-expansion-plan-v0.md)

Use for:

- explaining KRK -> KORA Core expansion.
- separating current alpha from roadmap.
- defining inspect, compare, run, and report.

## KORA Naming And Roadmap Docs

References:

- [KORA routable AI workloads master plan v0.1](../strategy/kora-routable-ai-workloads-master-plan-v0-1.md)
- [KORA naming strategy v0](../strategy/kora-naming-strategy-v0.md)
- [KORA repo restructuring plan v0](../strategy/kora-repo-restructuring-plan-v0.md)
- [KORA post-July roadmap v0](../strategy/kora-post-july-roadmap-v0.md)
- [KORA community growth plan v0](../strategy/kora-community-growth-plan-v0.md)

Use for:

- naming hierarchy.
- repo strategy.
- community path.
- post-July roadmap.

## KRK Matrix Workload Examples

References:

- `examples/workloads/krk-mixed-routing-matrix-alpha.json`
- `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json`
- `examples/workloads/krk-adversarial-routing-matrix-alpha.json`

Use for:

- example matrix coverage.
- future dry-run evaluator input.
- public-safe workload shape review.

Limitations:

- these fixtures are not yet connected to a complete evaluator.
- oracle labels must remain separate from router inputs if code is added.

## Pending Evidence

Pending items:

- route accuracy against the extended matrix.
- acceptable route rate.
- unsafe misroute rate.
- cache correctness.
- fallback rates.
- compute-weighted GPU demand.
- public-safe bounded GPU-routed subset measurement.
- provider-routed sample validation.
- adversarial fallback evaluation.
- service-replay profile evaluation.

## Public-Safe Use

Use this index to build the July 31 report, development plan, and video without inventing results.

Every metric should be labeled as:

- measured.
- simulated.
- methodology-only.
- not measured yet.
- not included in current public package.
