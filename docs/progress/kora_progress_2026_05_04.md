# KORA Progress Report - 2026-05-04

Date: 2026-05-04

Current public HEAD:

```text
origin/main d9761245d2eb5a59a07c6bde5295a98582945f11
```

## Executive Summary

KORA moved from CI-only validation into a benchmark-backed skeleton path. The repository now has GitHub Actions CI on `main`, an `experiments/` benchmark structure, a deterministic-heavy workload, and a benchmark runner with three simulated modes:

- `dry-run`
- `direct-baseline`
- `kora-controlled`

The current deterministic-heavy workload contains 20 tasks. In the simulated direct baseline, every task is counted as one model invocation. In the simulated KORA-controlled mode, tasks marked `requires_model: false` are counted as deterministic resolutions and tasks marked `requires_model: true` are counted as fallback/model-invocation candidates.

This produces an initial controlled benchmark result: 20 simulated direct-baseline model invocations versus 4 simulated KORA-controlled model invocations, with 16 avoided simulated invocations. This is useful evidence for the benchmark pipeline, but it is not yet a production cost, real API, or full runtime integration claim.

## Completed Tasks

| Task | Result |
|---|---|
| Task 034 | Added minimal GitHub Actions CI workflow. |
| Task 035 | Committed and pushed CI workflow branch. |
| Task 036 | Opened CI PR and confirmed GitHub Actions green. |
| Task 037 | Merged CI PR and verified `origin/main`. |
| Task 038 | Designed benchmark skeleton structure. |
| Task 039 | Committed and pushed benchmark skeleton branch. |
| Task 040 | Opened benchmark skeleton PR and confirmed CI green. |
| Task 041 | Merged benchmark skeleton PR and verified `origin/main`. |
| Task 042 | Added dry-run benchmark runner skeleton. |
| Task 043 | Committed and pushed dry-run runner branch. |
| Task 044 | Opened dry-run runner PR and confirmed CI green. |
| Task 045 | Merged dry-run runner PR and verified `origin/main`. |
| Task 046 | Added simulated direct-baseline benchmark mode. |
| Task 047 | Committed and pushed direct-baseline branch. |
| Task 048 | Opened direct-baseline PR and confirmed CI green. |
| Task 049 | Merged direct-baseline PR and verified `origin/main`. |
| Task 050 | Added simulated KORA-controlled benchmark mode. |
| Task 051 | Committed and pushed KORA-controlled branch. |
| Task 052 | Opened KORA-controlled PR and confirmed CI green. |
| Task 053 | Merged KORA-controlled PR and verified `origin/main`. |

## Merged PRs

| PR | Summary | Merge Commit |
|---|---|---|
| #2 | GitHub Actions CI | `804704006235463b6d85fc28b40077182212ed78` |
| #3 | Benchmark experiment skeleton | `0ea5421111d9f2d9f668c88e0053adc31a1c36b4` |
| #4 | Dry-run benchmark runner | `0ee771d8daa8ebf083c76d56770ed3559ddb4f9d` |
| #5 | Direct baseline benchmark mode | `46ba4445955157722363188d86d61b2287cd1215` |
| #6 | KORA-controlled benchmark mode | `d9761245d2eb5a59a07c6bde5295a98582945f11` |

## Current Benchmark Modes

| Mode | Purpose | Real model calls |
|---|---|---|
| `dry-run` | Load workload, validate shape, count tasks/categories/metadata. | No |
| `direct-baseline` | Simulate naive baseline where every task causes one model invocation. | No |
| `kora-controlled` | Simulate deterministic-first execution from workload metadata. | No |

## Current Benchmark Result

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
| Avoided model invocation rate | 0.8 |

## Safe Claim Wording

Safe wording:

```text
KORA now has a CI-validated benchmark skeleton with a deterministic-heavy workload and simulated direct-baseline versus KORA-controlled benchmark modes. On the current 20-task workload, the metadata-based KORA-controlled simulation counts 16 deterministic resolutions and 4 fallback candidates, avoiding 16 simulated model invocations versus the naive direct baseline.
```

Short claim:

```text
KORA has an initial reproducible benchmark skeleton showing 80% simulated model invocation avoidance on a deterministic-heavy controlled workload.
```

Use the word `simulated` when describing this result.

## Claims Not To Make Yet

Do not claim:

- production cost reduction
- actual API cost reduction
- real model invocation reduction in deployment
- latency improvement
- energy reduction
- broad benchmark superiority
- full KORA runtime benchmark integration
- paper-grade evaluation completeness

## Validation Commands And Results

Commands run on latest `origin/main`:

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

Results:

| Check | Result |
|---|---|
| Dry-run benchmark | Passed |
| Direct-baseline benchmark | Passed |
| KORA-controlled benchmark | Passed |
| KORA-controlled JSON validation | Passed |
| Release smoke | Passed |
| Pytest | Passed, 35 tests |

## Next Recommended Tasks

1. Decide whether benchmark results should remain generated-only or whether a result artifact should be committed under a non-ignored path.
2. Add a benchmark result summary markdown if the result is intended to be reviewed publicly.
3. Prepare `v0.1.1-alpha` release notes focused on CI and benchmark skeleton progress.
4. Run one more clean verification from latest `origin/main`.
5. Consider tagging `v0.1.1-alpha` after clean verification and release note review.

## Limitations

- The benchmark is simulated.
- No real model calls are made.
- No external APIs are used.
- No production cost claim is supported.
- No full KORA runtime integration is implemented.
- The workload has only 20 manually defined tasks.
- The current avoided invocation rate is based on workload metadata, not measured runtime routing.
