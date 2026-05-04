# KORA Benchmark Result Summary - v0.1.1-alpha

Date: 2026-05-04

## Release Context

| Item | Value |
|---|---|
| Release tag | `v0.1.1-alpha` |
| Public HEAD | `origin/main 036776ce2286453743cf1f9cea4cad4128621364` |
| GitHub Release | `https://github.com/hkalbertkim/KORA/releases/tag/v0.1.1-alpha` |
| Workload | `experiments/workloads/deterministic_heavy_v0.json` |
| Runner | `experiments/run_benchmark.py` |

## Benchmark Purpose

This benchmark result summary records the current controlled benchmark skeleton result for KORA v0.1.1-alpha. The goal is to document the reproducible simulated comparison that now exists in the repository and to prepare the path toward v0.2.0-alpha technical preview results.

The benchmark is deterministic-heavy by design. It tests the shape of a future direct-baseline versus KORA-controlled evaluation where deterministic work should be resolved before model invocation is considered.

## Workload Description

The current workload is:

```text
experiments/workloads/deterministic_heavy_v0.json
```

It contains 20 manually defined tasks across deterministic-first categories such as arithmetic, string normalization, JSON validation, routing decisions, cache lookup, and schema checks.

The workload intentionally separates:

- tasks marked `requires_model: false`, which are counted as deterministic resolutions in the simulated KORA-controlled mode
- tasks marked `requires_model: true`, which are counted as fallback/model-invocation candidates

## Benchmark Modes

| Mode | Description | Real model calls |
|---|---|---|
| `dry-run` | Loads the workload, validates task shape, counts categories, and counts `requires_model` values. | No |
| `direct-baseline` | Simulates a naive baseline where every task causes one model invocation. | No |
| `kora-controlled` | Simulates deterministic-first KORA execution using workload metadata. | No |

## Current Result

| Metric | Value |
|---|---:|
| Total tasks | 20 |
| Direct-baseline simulated model invocations | 20 |
| KORA-controlled simulated model invocations | 4 |
| Deterministic resolutions | 16 |
| Fallback candidates | 4 |
| Avoided model invocations | 16 |
| Avoided invocation rate | 80% |

## Safe Interpretation

In a deterministic-heavy controlled benchmark skeleton, KORA-controlled execution avoided 16 of 20 simulated model invocations versus a naive direct baseline.

This result should be interpreted as a metadata-based benchmark skeleton result. It shows that the current workload and runner can reproduce a controlled simulated comparison, and it gives KORA a concrete baseline for future benchmark hardening.

## Explicit Non-Claims

This result does not claim:

- this is production cost reduction
- this is real API-cost reduction
- this is a production benchmark
- this is full KORA runtime integration
- this is a broad workload benchmark
- this proves general performance superiority
- this proves latency improvement
- this proves energy reduction

## Validation Commands

Benchmark commands:

```bash
python3 experiments/run_benchmark.py \
  --mode dry-run \
  --workload experiments/workloads/deterministic_heavy_v0.json \
  --output /tmp/kora_deterministic_heavy_v0.dry_run.json

python3 experiments/run_benchmark.py \
  --mode direct-baseline \
  --workload experiments/workloads/deterministic_heavy_v0.json \
  --output /tmp/kora_deterministic_heavy_v0.direct_baseline.json

python3 experiments/run_benchmark.py \
  --mode kora-controlled \
  --workload experiments/workloads/deterministic_heavy_v0.json \
  --output /tmp/kora_deterministic_heavy_v0.kora_controlled.json
```

JSON validation commands:

```bash
python3 -m json.tool /tmp/kora_deterministic_heavy_v0.dry_run.json > /tmp/kora_dry_run_check.json
python3 -m json.tool /tmp/kora_deterministic_heavy_v0.direct_baseline.json > /tmp/kora_direct_baseline_check.json
python3 -m json.tool /tmp/kora_deterministic_heavy_v0.kora_controlled.json > /tmp/kora_kora_controlled_check.json
```

Release validation commands:

```bash
./scripts/release_smoke.sh
python3 -m pytest -q
```

## Limitations

- The benchmark is simulated.
- No real model calls are made.
- No external API calls are made.
- No real API-cost measurement is included.
- No production cost reduction claim is supported.
- No full KORA runtime integration is implemented yet.
- The workload is intentionally small and deterministic-heavy.
- The current avoided invocation rate is based on workload metadata, not measured runtime routing.
- Correctness scoring against `expected_output` fields is not yet implemented as a benchmark result metric.

## Next Steps Toward v0.2.0-alpha

1. Expand workload size from 20 tasks to 100-500 tasks.
2. Add committed reproducible result artifacts only after a result artifact policy is decided.
3. Add a technical preview results document for controlled benchmark outputs.
4. Add stronger correctness checks against expected outputs.
5. Design a runtime-integrated KORA execution benchmark.
6. Add ablation modes later, such as deterministic-only, fallback-only, cache-disabled, and verifier-disabled variants.
