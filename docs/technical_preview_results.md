# KORA Technical Preview Results

Date: 2026-05-04

## Status

This document is an early technical preview results document.

The current primary evidence is the reproducible 100-task deterministic-heavy benchmark workload merged after KORA v0.1.1-alpha. The benchmark remains simulated, deterministic-heavy, and intentionally scoped. It is not yet a production benchmark.

The earlier v0.1.1-alpha 20-task result is preserved as historical skeleton evidence. The current 100-task workload is the primary evidence for the path toward v0.2.0-alpha.

## Release Context

| Item | Value |
|---|---|
| Current released tag | `v0.1.1-alpha` |
| Public HEAD | `origin/main de20e8c2a2f1b8e80d1260cccd638d18eff344fc` |
| GitHub Release | `https://github.com/hkalbertkim/KORA/releases/tag/v0.1.1-alpha` |
| Current benchmark summary | `docs/benchmarks/kora_benchmark_result_v1_100.md` |
| Historical benchmark summary | `docs/benchmarks/kora_benchmark_result_v0_1_1_alpha.md` |
| Current workload | `experiments/workloads/deterministic_heavy_v1_100.json` |
| Workload generator | `experiments/generate_workload.py` |
| Runner | `experiments/run_benchmark.py` |

## Current Evidence Summary

KORA now has a reproducible 100-task deterministic-heavy benchmark workload generated from seed `42`. The current benchmark compares simulated direct-baseline execution with simulated KORA-controlled execution.

The benchmark runner does not call a real model, does not use external APIs, and does not execute full KORA runtime integration. It uses workload metadata to count model-invocation candidates and deterministic/no-model tasks.

## Benchmark Modes

| Mode | Current behavior | Real model calls |
|---|---|---|
| `dry-run` | Loads the workload, validates task shape, counts categories, and counts `requires_model` values. | No |
| `direct-baseline` | Simulates a naive baseline where every task causes one model invocation. | No |
| `kora-controlled` | Simulates deterministic-first execution by treating `requires_model: false` tasks as deterministic/no-model resolutions and `requires_model: true` tasks as fallback/model-candidate tasks. | No |

## Current Primary Result

| Metric | Value |
|---|---:|
| Workload | `deterministic_heavy_v1_100` |
| Total tasks | 100 |
| Deterministic/no-model tasks | 80 |
| Fallback/model-candidate tasks | 20 |
| Direct-baseline simulated model invocations | 100 |
| KORA-controlled simulated model invocations | 20 |
| Avoided model invocations | 80 |
| Avoided invocation rate | 80% |

## Historical Skeleton Result

The earlier v0.1.1-alpha benchmark skeleton used a smaller 20-task deterministic-heavy workload. It remains useful as historical context, but it is no longer the primary technical preview evidence.

| Metric | Value |
|---|---:|
| Workload | `deterministic_heavy_v0` |
| Total tasks | 20 |
| Direct-baseline simulated model invocations | 20 |
| KORA-controlled simulated model invocations | 4 |
| Avoided model invocations | 16 |
| Avoided invocation rate | 80% |

## What The Current Result Means

In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

This means the current generator, workload, and runner can reproduce a metadata-based simulated comparison where deterministic-first handling avoids unnecessary simulated model invocations. It is useful as a benchmark scaffold and as a baseline for v0.2.0-alpha hardening.

## What It Does Not Mean

The current result is:

- not production cost reduction
- not real API-cost reduction
- not production benchmark proof
- not full runtime-integrated benchmark evidence
- not broad workload superiority
- not energy reduction evidence
- not latency improvement evidence
- not paper-grade evaluation evidence
- not proof of general performance superiority

## Reproducibility Commands

```bash
python3 experiments/generate_workload.py --count 100 --seed 42 --benchmark-name deterministic_heavy_v1 --output /tmp/kora_deterministic_heavy_v1_100.regenerated.json
cmp experiments/workloads/deterministic_heavy_v1_100.json /tmp/kora_deterministic_heavy_v1_100.regenerated.json

python3 experiments/run_benchmark.py --mode dry-run --workload experiments/workloads/deterministic_heavy_v1_100.json --output /tmp/kora_deterministic_heavy_v1_100.dry_run.json
python3 experiments/run_benchmark.py --mode direct-baseline --workload experiments/workloads/deterministic_heavy_v1_100.json --output /tmp/kora_deterministic_heavy_v1_100.direct_baseline.json
python3 experiments/run_benchmark.py --mode kora-controlled --workload experiments/workloads/deterministic_heavy_v1_100.json --output /tmp/kora_deterministic_heavy_v1_100.kora_controlled.json

./scripts/release_smoke.sh
python3 -m pytest -q
```

Optional JSON validation:

```bash
python3 -m json.tool experiments/workloads/deterministic_heavy_v1_100.json > /tmp/kora_generated_workload_check.json
python3 -m json.tool /tmp/kora_deterministic_heavy_v1_100.dry_run.json > /tmp/kora_v1_dry_run_check.json
python3 -m json.tool /tmp/kora_deterministic_heavy_v1_100.direct_baseline.json > /tmp/kora_v1_direct_baseline_check.json
python3 -m json.tool /tmp/kora_deterministic_heavy_v1_100.kora_controlled.json > /tmp/kora_v1_kora_controlled_check.json
```

## Planned Evidence Path To v0.2.0-alpha

The project has reached the near-term 100-task deterministic-heavy workload target. The v0.2.0-alpha evidence path should now strengthen that controlled benchmark without making production claims.

Planned work:

1. Add stronger expected-output correctness checks against deterministic `expected_output` and `expected_path`.
2. Add result summary generation automation from structured benchmark result JSON.
3. Decide whether raw generated result JSON artifacts remain generated-only or become committed artifacts.
4. Add expanded correctness, error, and fallback cases.
5. Add additional deterministic-heavy workload variants.
6. Add failure-case coverage for malformed workload tasks and invalid benchmark modes.
7. Prepare the v0.2.0-alpha release note and final readiness check.
8. Keep benchmark wording limited to simulated controlled benchmark evidence.

## Planned Evidence Path To v0.3.0-alpha

The v0.3.0-alpha evidence path should move from metadata-only simulation toward runtime-integrated benchmark evidence.

Planned work:

1. Design a KORA runtime-integrated benchmark path.
2. Compare direct-baseline execution with actual KORA-controlled execution semantics.
3. Add mixed workload coverage beyond deterministic-heavy cases.
4. Add retry and verifier workload coverage.
5. Add structured telemetry for deterministic resolution, fallback, validation, retry, and cache paths.
6. Add ablation modes such as deterministic-only, fallback-only, cache-disabled, and verifier-disabled.
7. Add a paper reproducibility document that records workload generation, benchmark commands, result interpretation, and claim boundaries.
8. Harden claim wording before any broader public technical preview claims.
9. Report correctness and invocation-count metrics together.
10. Preserve explicit non-claims until real model/API measurements exist.

## Open Benchmark Gaps

- Correctness scoring against deterministic `expected_output` is not yet reported as a benchmark metric.
- Generated JSON outputs are not committed as stable artifacts.
- No real model calls are measured.
- No external API cost is measured.
- No latency or energy metrics are measured.
- No full KORA runtime integration is benchmarked yet.
- The current workload is larger than the initial skeleton but remains deterministic-heavy by design.
- No broad workload suite exists yet.

## Claim Ladder

| Evidence level | Status | Claim boundary |
|---|---|---|
| Benchmark skeleton exists | Historical, v0.1.1-alpha | KORA has a reproducible simulated benchmark scaffold. |
| 20-task simulated deterministic-heavy result | Historical, v0.1.1-alpha | KORA-controlled simulation avoided 16 of 20 simulated model invocations on the initial deterministic-heavy workload. |
| 100-task reproducible deterministic-heavy result | Current | KORA-controlled simulation avoided 80 of 100 simulated model invocations on the reproducible generated workload. |
| Correctness-checked controlled workload | Planned, v0.2.0-alpha | KORA can report simulated invocation counts together with deterministic correctness checks. |
| Runtime-integrated benchmark | Planned, v0.3.0-alpha | KORA can compare direct baseline and KORA-controlled runtime behavior under documented benchmark conditions. |
| Real API-cost evidence | Future, not current | Requires real model/API calls, measured cost, and reproducible methodology. |
| Production cost reduction | Future, not current | Requires production-like workloads, measured costs, correctness controls, and external validation. |
