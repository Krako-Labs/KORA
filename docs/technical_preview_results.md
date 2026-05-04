# KORA Technical Preview Results

Date: 2026-05-04

## Status

This document is an early technical preview results skeleton.

The current evidence is based on KORA v0.1.1-alpha and the controlled benchmark skeleton merged into `origin/main`. The benchmark is simulated, deterministic-heavy, and intentionally small. It is not yet a production benchmark.

This document separates current v0.1.1-alpha evidence from planned v0.2.0-alpha and v0.3.0-alpha evidence so future results can be added without overstating the current benchmark.

## Release Context

| Item | Value |
|---|---|
| Current release | `v0.1.1-alpha` |
| Public HEAD | `origin/main 14d5c40fa89d9872f748cb3a33aabfaccbdd70ea` |
| GitHub Release | `https://github.com/hkalbertkim/KORA/releases/tag/v0.1.1-alpha` |
| Benchmark summary | `docs/benchmarks/kora_benchmark_result_v0_1_1_alpha.md` |
| Workload | `experiments/workloads/deterministic_heavy_v0.json` |
| Runner | `experiments/run_benchmark.py` |

## Current Evidence Summary

KORA v0.1.1-alpha provides CI-backed validation and the first reproducible controlled benchmark skeleton. The current benchmark uses a 20-task deterministic-heavy workload and compares simulated direct-baseline execution with simulated KORA-controlled execution.

The benchmark runner does not call a real model, does not use external APIs, and does not execute full KORA runtime integration. It uses workload metadata to count model-invocation candidates and deterministic resolutions.

## Benchmark Modes

| Mode | Current behavior | Real model calls |
|---|---|---|
| `dry-run` | Loads the workload, validates task shape, counts categories, and counts `requires_model` values. | No |
| `direct-baseline` | Simulates a naive baseline where every task causes one model invocation. | No |
| `kora-controlled` | Simulates deterministic-first execution by treating `requires_model: false` tasks as deterministic resolutions and `requires_model: true` tasks as fallback candidates. | No |

## Current Result Table

| Metric | Value |
|---|---:|
| Total tasks | 20 |
| Direct-baseline simulated model invocations | 20 |
| KORA-controlled simulated model invocations | 4 |
| Deterministic resolutions | 16 |
| Fallback candidates | 4 |
| Avoided model invocations | 16 |
| Avoided invocation rate | 80% |

## What The Result Means

In a deterministic-heavy controlled benchmark skeleton, KORA-controlled execution avoided 16 of 20 simulated model invocations versus a naive direct baseline.

This means the current workload and runner can reproduce a metadata-based simulated comparison where deterministic-first handling avoids unnecessary simulated model invocations. It is useful as a benchmark scaffold and as a baseline for future hardening.

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
./scripts/release_smoke.sh
python3 -m pytest -q
python3 experiments/run_benchmark.py --mode dry-run --workload experiments/workloads/deterministic_heavy_v0.json --output /tmp/kora_deterministic_heavy_v0.dry_run.json
python3 experiments/run_benchmark.py --mode direct-baseline --workload experiments/workloads/deterministic_heavy_v0.json --output /tmp/kora_deterministic_heavy_v0.direct_baseline.json
python3 experiments/run_benchmark.py --mode kora-controlled --workload experiments/workloads/deterministic_heavy_v0.json --output /tmp/kora_deterministic_heavy_v0.kora_controlled.json
```

Optional JSON validation:

```bash
python3 -m json.tool /tmp/kora_deterministic_heavy_v0.dry_run.json > /tmp/kora_dry_run_check.json
python3 -m json.tool /tmp/kora_deterministic_heavy_v0.direct_baseline.json > /tmp/kora_direct_baseline_check.json
python3 -m json.tool /tmp/kora_deterministic_heavy_v0.kora_controlled.json > /tmp/kora_kora_controlled_check.json
```

## Planned Evidence Path To v0.2.0-alpha

The v0.2.0-alpha evidence path should strengthen the controlled benchmark without making production claims.

Planned work:

1. Expand the deterministic-heavy workload from 20 tasks to 100-500 tasks.
2. Add correctness checks against `expected_output` and `expected_path`.
3. Decide whether generated result JSON artifacts remain generated-only or become committed artifacts.
4. Add a stable benchmark result artifact policy.
5. Add benchmark summary generation from structured JSON outputs.
6. Add failure-case coverage for malformed workload tasks and invalid benchmark modes.
7. Keep benchmark wording limited to simulated controlled benchmark evidence.

## Planned Evidence Path To v0.3.0-alpha

The v0.3.0-alpha evidence path should move from metadata-only simulation toward runtime-integrated benchmark evidence.

Planned work:

1. Design a KORA runtime-integrated benchmark path.
2. Compare direct-baseline execution with actual KORA-controlled execution semantics.
3. Add structured telemetry for deterministic resolution, fallback, validation, retry, and cache paths.
4. Add ablation modes such as deterministic-only, fallback-only, cache-disabled, and verifier-disabled.
5. Add broader workload families beyond deterministic-heavy tasks.
6. Report correctness and invocation-count metrics together.
7. Preserve explicit non-claims until real model/API measurements exist.

## Open Benchmark Gaps

- The workload is small and manually written.
- The current benchmark is deterministic-heavy by design.
- Correctness scoring is not yet implemented as a benchmark metric.
- Generated JSON outputs are not committed as stable artifacts.
- No real model calls are measured.
- No external API cost is measured.
- No latency or energy metrics are measured.
- No full KORA runtime integration is benchmarked yet.
- No broad workload suite exists yet.

## Claim Ladder

| Evidence level | Status | Claim boundary |
|---|---|---|
| Benchmark skeleton exists | Current, v0.1.1-alpha | KORA has a reproducible simulated benchmark scaffold. |
| Simulated deterministic-heavy result | Current, v0.1.1-alpha | KORA-controlled simulation avoided 16 of 20 simulated model invocations on the current deterministic-heavy workload. |
| Larger controlled workload | Planned, v0.2.0-alpha | KORA can report simulated controlled benchmark results over a broader deterministic-heavy workload. |
| Runtime-integrated benchmark | Planned, v0.3.0-alpha | KORA can compare direct baseline and KORA-controlled runtime behavior under documented benchmark conditions. |
| Real API-cost evidence | Future, not current | Requires real model/API calls, measured cost, and reproducible methodology. |
| Production cost reduction | Future, not current | Requires production-like workloads, measured costs, correctness controls, and external validation. |
