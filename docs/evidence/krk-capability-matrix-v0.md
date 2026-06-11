# KRK Capability Matrix v0

| Capability | Status | Evidence / Doc Link | Limitation | Next Action |
| --- | --- | --- | --- | --- |
| Route decision | Partially implemented through current execution-control examples; standalone top-level `route` command is roadmap. | [KRK definition](../product/kora-routing-kernel-definition-v0.md), [KRK quickstart](../product/krk-quickstart-v0.md) | Existing CLI uses `python3 -m kora run ...`; standalone KRK route command is not exposed. | Decide and implement top-level route alias or dedicated command. |
| Explanation | Partially represented through example outputs and telemetry; standalone top-level `explain` command is roadmap. | [KRK architecture](../architecture/krk-architecture-v0.md) | Explanation format is not yet a stable KRK CLI contract. | Define route explanation schema. |
| Benchmark comparison | Implemented for existing runtime benchmark example; extended matrix evaluator is roadmap. | [KRK routing benchmark methodology](krk-routing-benchmark-methodology-v0.md) | Current benchmark does not yet consume the new KRK matrix fixtures. | Build dry-run matrix evaluator. |
| Report generation | Partially implemented through existing benchmark/report examples, telemetry docs, and current performance package docs; standalone top-level `report` command is roadmap. | [KORA Evidence Report Schema](kora-evidence-report-schema-v0.md), [KRK performance table schema](krk-performance-table-schema-v0.md), [KRK performance table](krk-performance-table-v0.md) | Report schema is not yet enforced across KRK matrix runs. | Add generated table output from structured matrix results. |
| Deterministic-heavy benchmark evidence | Implemented as bounded alpha evidence. | [Benchmark result summary](../benchmarks/kora_benchmark_result_v1_100.md), [Runtime evidence reviewer guide](../reports/v0.3.0-alpha-runtime-evidence-reviewer-guide.md) | Evidence is deterministic-heavy and should not be generalized. | Keep claim wording bounded. |
| KRK extended matrix docs | Implemented as public-safe docs and fixtures. | [Extended H100 test matrix](krk-extended-h100-test-matrix-v0.md), `examples/workloads/krk-*.json` | Fixtures are not yet connected to a runner. | Add dry-run evaluator. |
| GPU-routed subset methodology | Documented. | [KRK public evidence boundary](krk-public-evidence-boundary-v0.md), [KRK performance table schema](krk-performance-table-schema-v0.md), [KRK evidence package](krk-evidence-package-v0.md) | Subset count is not measured yet. | Define bounded measurement runner and artifact policy. |
| H100 bounded measurement support | Planning / boundary only in this package. | [KRK extended H100 test matrix](krk-extended-h100-test-matrix-v0.md), [KRK performance table](krk-performance-table-v0.md) | Public-safe measured task count, runtime, throughput, and memory values are not included in the current public package. | Prepare public-safe measurement plan after dry-run matrix evaluator. |
| Inspect | KORA Core roadmap only. | [KORA Core expansion plan](../product/kora-core-expansion-plan-v0.md) | Not a KRK standalone command on current base. | Define future KORA Core command contract. |
| Compare | KORA Core roadmap only. | [KORA Core expansion plan](../product/kora-core-expansion-plan-v0.md) | Not a KRK standalone command on current base. | Define future KORA Core command contract. |
| Run | Current CLI has `run` for examples; KORA Core `run` workflow remains roadmap. | [KRK quickstart](../product/krk-quickstart-v0.md) | Existing `run` is example-oriented, not the full KORA Core workflow. | Separate example runner from future workload runner. |
| Report | KORA Core roadmap as a first-class workflow; current report behavior exists through examples and docs. | [KORA Evidence Report Schema](kora-evidence-report-schema-v0.md) | Not a top-level `report` command on current base. | Decide report CLI shape. |

## Boundary

This matrix is a capability map, not a production readiness claim.

It does not claim production cost reduction, customer savings, infrastructure savings, broad workload superiority, H100 superiority, or replacement of provider/router systems.

Related current evidence package docs:

- [KRK performance table v0](krk-performance-table-v0.md)
- [KRK evidence package v0](krk-evidence-package-v0.md)
- [KRK reproducibility matrix v0](krk-reproducibility-matrix-v0.md)
- [KRK claim boundary table v0](krk-claim-boundary-table-v0.md)
