# KORA v0.1.1-alpha Release Note

Release type: alpha maintenance / benchmark skeleton release

Release date: 2026-05-04

## Summary

KORA v0.1.1-alpha is a maintenance alpha focused on CI-backed release validation and the first reproducible benchmark skeleton.

This release keeps the v0.1.0-alpha terminal-first surface intact and adds GitHub Actions CI, an `experiments/` benchmark workspace, a deterministic-heavy workload, and a benchmark runner with simulated `dry-run`, `direct-baseline`, and `kora-controlled` modes.

The benchmark work is intentionally limited. It provides a controlled skeleton for comparing a naive direct baseline against metadata-based KORA-controlled execution, but it does not make production, real API, or full runtime integration claims.

## What Changed Since v0.1.0-alpha

- Added GitHub Actions CI for editable install, release smoke, and pytest validation.
- Added an initial benchmark experiment structure under `experiments/`.
- Added a deterministic-heavy workload draft with 20 tasks.
- Added a benchmark runner skeleton.
- Added `dry-run` mode for workload validation and task/category counting.
- Added `direct-baseline` mode to simulate one model invocation per task.
- Added `kora-controlled` mode to simulate deterministic-first execution from workload metadata.
- Added a 2026-05-04 progress report documenting the CI and benchmark milestone.

## GitHub Actions CI

The repository now includes minimal CI on push and pull request events targeting `main`.

The CI validation path runs:

```bash
python3 -m pip install -e ".[dev]"
./scripts/release_smoke.sh
python3 -m pytest -q
```

This makes the release smoke path and test suite part of the public validation loop before changes merge into `main`.

## Benchmark Experiment Skeleton

The new experiment structure is:

```text
experiments/
experiments/README.md
experiments/run_benchmark.py
experiments/workloads/deterministic_heavy_v0.json
experiments/results/.gitkeep
```

The first workload is deterministic-heavy by design. Most tasks are marked as cases that should be handled without model calls, while a smaller set is marked as future fallback/model-invocation candidates.

## Benchmark Modes

### Dry-Run

`dry-run` loads the workload, validates the task list, counts tasks by category, counts `requires_model` values, and writes a result JSON artifact.

Example:

```bash
python3 experiments/run_benchmark.py \
  --mode dry-run \
  --workload experiments/workloads/deterministic_heavy_v0.json \
  --output experiments/results/deterministic_heavy_v0.dry_run.json
```

### Direct Baseline

`direct-baseline` simulates a naive baseline where every workload task causes one model invocation. It does not call a real model and does not use external APIs.

Example:

```bash
python3 experiments/run_benchmark.py \
  --mode direct-baseline \
  --workload experiments/workloads/deterministic_heavy_v0.json \
  --output experiments/results/deterministic_heavy_v0.direct_baseline.json
```

### KORA-Controlled

`kora-controlled` simulates deterministic-first KORA execution using workload metadata:

- tasks with `requires_model: false` are counted as deterministic resolutions
- tasks with `requires_model: true` are counted as fallback/model-invocation candidates

Example:

```bash
python3 experiments/run_benchmark.py \
  --mode kora-controlled \
  --workload experiments/workloads/deterministic_heavy_v0.json \
  --output experiments/results/deterministic_heavy_v0.kora_controlled.json
```

## Current Controlled Benchmark Result

Workload:

```text
experiments/workloads/deterministic_heavy_v0.json
```

| Metric | Value |
|---|---:|
| Total tasks | 20 |
| Direct-baseline simulated model invocations | 20 |
| KORA-controlled simulated model invocations | 4 |
| Deterministic resolutions | 16 |
| Fallback candidates | 4 |
| Avoided model invocations vs direct baseline | 16 |
| Avoided invocation rate | 80% |

## Safe Claim Wording

Safe wording:

```text
In a deterministic-heavy controlled benchmark skeleton, KORA-controlled execution avoided 16 of 20 simulated model invocations versus a naive direct baseline.
```

Expanded wording:

```text
KORA v0.1.1-alpha includes a CI-validated benchmark skeleton with a deterministic-heavy workload and simulated direct-baseline versus KORA-controlled benchmark modes. On the current 20-task workload, the metadata-based KORA-controlled simulation counts 16 deterministic resolutions and 4 fallback candidates, avoiding 16 simulated model invocations versus the naive direct baseline.
```

Use the word `simulated` when describing the benchmark result.

## Validation Commands

Recommended validation before tagging:

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

python3 -m json.tool /tmp/kora_deterministic_heavy_v0.kora_controlled.json > /tmp/kora_kora_controlled_check.json

./scripts/release_smoke.sh

python3 -m pytest -q
```

Current verification status:

| Check | Result |
|---|---|
| Release smoke | Passed |
| Pytest | Passed, 35 tests |

## Limitations

- The benchmark is simulated.
- No real model calls are made.
- No external API calls are made.
- No real API-cost measurement is included.
- No production cost reduction claim is supported.
- No full KORA runtime integration is implemented yet.
- The workload is intentionally small and deterministic-heavy.

## What This Release Does Not Claim

This release does not claim:

- production cost reduction
- real API cost reduction
- production benchmark proof
- full runtime-integrated benchmark evidence
- latency improvement
- energy reduction
- broad benchmark superiority
- paper-grade evaluation completeness

## Next Planned Work

- Decide whether benchmark result artifacts should remain generated-only or be committed under a tracked path.
- Add a concise benchmark result summary markdown if the result should be reviewed publicly.
- Run one more clean verification from latest `origin/main` before tagging.
- Tag `v0.1.1-alpha` only after release note review and clean verification.
- Extend the benchmark runner toward real KORA runtime integration in a later alpha.
