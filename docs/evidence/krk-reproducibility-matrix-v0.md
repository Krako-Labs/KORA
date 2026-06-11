# KRK Reproducibility Matrix v0

Status: current public reproducibility map.

This matrix identifies which KRK evidence items are reproducible from the public repository today and which are methodology-only.

| Evidence Item | Reproducible | How | Limitations |
| --- | --- | --- | --- |
| Deterministic-heavy benchmark | Yes | Use the tracked workload and runtime benchmark path documented in the [runtime evidence reviewer guide](../reports/v0.3.0-alpha-runtime-evidence-reviewer-guide.md). | Simulated deterministic-heavy benchmark; not a broad workload result. |
| Deterministic mismatch count | Yes | Run the runtime benchmark path and check `deterministic_outputs_checked` and `mismatch_count`. | Applies to the current deterministic-heavy workload only. |
| Benchmark methodology | Yes | Review [KRK routing benchmark methodology v0](krk-routing-benchmark-methodology-v0.md). | Methodology docs are reproducible as review artifacts, not measured results. |
| KRK extended test matrix | Partially | Review the matrix docs and JSON fixtures in `examples/workloads/krk-*-routing-matrix-alpha.json`. | Fixtures are not yet connected to a runner. |
| GPU subset methodology | Yes | Review [KRK public evidence boundary v0](krk-public-evidence-boundary-v0.md) and [KRK performance table schema v0](krk-performance-table-schema-v0.md). | Methodology only; subset count is not measured yet. |
| Bounded GPU measurement | No | Not included in the current public package. | No public-safe measured task count, runtime, throughput, or memory table is included. |
| Claim boundary table | Yes | Review [KRK claim boundary table v0](krk-claim-boundary-table-v0.md). | This defines allowed language; it is not a benchmark result. |

## Reviewer Path

1. Run the test suite.
2. Run the offline runtime benchmark.
3. Compare the counters with the runtime evidence reviewer guide.
4. Review the performance table and claim boundary table.
5. Treat unmeasured routing metrics as open work.

## Current Gap

The main missing reproducibility link is an executable dry-run evaluator for the KRK extended matrix fixtures.
