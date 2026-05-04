# KORA EOD Report - v0.2.0-alpha Evidence Expansion

Date: 2026-05-04

Current public HEAD:

```text
origin/main 9a092d45065a25ab9a5e8723afecdc5c44be43dd
```

Previous release:

```text
v0.1.1-alpha
```

## Executive Summary

KORA completed the post-`v0.1.1-alpha` evidence expansion work needed to move the benchmark track toward `v0.2.0-alpha`. The day started with the first 20-task simulated benchmark skeleton and ended with a reproducible 100-task deterministic-heavy workload, a workload generator, tracked benchmark summaries, and an updated technical preview results document.

The current primary benchmark evidence is now the reproducible `deterministic_heavy_v1_100` workload. In that controlled benchmark skeleton, simulated KORA-controlled execution avoids 80 of 100 simulated model invocations versus the naive direct baseline.

This remains simulated benchmark evidence. It is not production cost evidence, not real API cost evidence, and not full runtime-integrated benchmark evidence.

## Starting State

- `v0.1.1-alpha` was already published.
- The technical preview evidence centered on the initial 20-task deterministic-heavy workload.
- The benchmark runner supported `dry-run`, `direct-baseline`, and `kora-controlled` modes.
- No reproducible workload generator existed yet.
- No generated 100-task workload existed yet.
- The local `main` worktree had pre-existing dirty changes and had to remain untouched.

## Final State

- `origin/main` is at `9a092d45065a25ab9a5e8723afecdc5c44be43dd`.
- The v0.1.1 benchmark result summary is merged.
- The technical preview results skeleton is merged and updated with v1 evidence.
- The v0.2.0-alpha workload expansion plan is merged.
- A standard-library workload generator is merged.
- The reproducible 100-task deterministic-heavy v1 workload is merged.
- The v1 100-task benchmark summary is merged.
- Final validation passed:
  - regeneration comparison
  - release smoke
  - pytest, 42 tests

## Completed Task Range

| Task | Result |
|---|---|
| Task 072 | Added v0.1.1 benchmark result summary artifact. |
| Task 073 | Committed and pushed benchmark result summary branch. |
| Task 074 | Opened benchmark result summary PR and confirmed CI. |
| Task 075 | Merged benchmark result summary PR and verified `origin/main`. |
| Task 076 | Drafted technical preview results skeleton. |
| Task 077 | Committed and pushed technical preview results skeleton. |
| Task 078 | Opened technical preview results PR and confirmed CI. |
| Task 079 | Merged technical preview results PR and verified `origin/main`. |
| Task 080 | Designed deterministic-heavy workload expansion plan. |
| Task 081 | Committed and pushed workload expansion plan. |
| Task 082 | Opened workload expansion plan PR and confirmed CI. |
| Task 083 | Merged workload expansion plan PR and verified `origin/main`. |
| Task 084 | Added deterministic-heavy workload generator skeleton and v1 100-task workload. |
| Task 085 | Committed and pushed workload generator branch. |
| Task 086 | Opened workload generator PR and confirmed CI. |
| Task 087 | Merged workload generator PR and verified `origin/main`. |
| Task 088 | Added v1 100-task benchmark result summary. |
| Task 089 | Committed and pushed v1 benchmark summary branch. |
| Task 090 | Opened v1 benchmark summary PR and confirmed CI. |
| Task 091 | Merged v1 benchmark summary PR and verified `origin/main`. |
| Task 092 | Updated technical preview results with v1 100-task evidence. |
| Task 093 | Committed and pushed technical preview v1 update. |
| Task 094 | Opened technical preview v1 update PR and confirmed CI. |
| Task 095 | Merged technical preview v1 update PR and verified `origin/main`. |

## Merged PRs

| PR | Scope |
|---|---|
| #10 | v0.1.1 benchmark result summary |
| #11 | Technical preview results skeleton |
| #12 | Workload expansion plan for v0.2.0 |
| #13 | Workload generator and v1 100-task workload |
| #14 | v1 100-task benchmark summary |
| #15 | Technical preview v1 update |

## Artifacts Created Or Updated

- `docs/benchmarks/kora_benchmark_result_v0_1_1_alpha.md`
- `docs/technical_preview_results.md`
- `docs/benchmarks/workload_expansion_plan_v0_2_0.md`
- `experiments/generate_workload.py`
- `experiments/workloads/deterministic_heavy_v1_100.json`
- `tests/test_workload_generator.py`
- `docs/benchmarks/kora_benchmark_result_v1_100.md`

## Current v1 100-Task Benchmark Result

Workload:

```text
experiments/workloads/deterministic_heavy_v1_100.json
```

Generation:

```text
python3 experiments/generate_workload.py --count 100 --seed 42 --benchmark-name deterministic_heavy_v1
```

| Metric | Value |
|---|---:|
| Total tasks | 100 |
| Deterministic/no-model tasks | 80 |
| Fallback/model-candidate tasks | 20 |
| Direct-baseline simulated model invocations | 100 |
| KORA-controlled simulated model invocations | 20 |
| Avoided model invocations vs direct baseline | 80 |
| Avoided invocation rate | 0.8 |

## Safe Claim

```text
In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.
```

Use `simulated` and `controlled benchmark` language when describing this result.

## Claims Not To Make Yet

Do not claim:

- production cost reduction
- real API cost reduction
- production benchmark proof
- full runtime-integrated benchmark evidence
- broad workload superiority
- general performance superiority
- latency improvement
- energy reduction evidence
- paper-grade reproducibility

## Validation Results

| Check | Result |
|---|---|
| Workload regeneration comparison | Passed |
| v1 dry-run benchmark | Passed |
| v1 direct-baseline benchmark | Passed |
| v1 KORA-controlled benchmark | Passed |
| Release smoke | Passed |
| Pytest | Passed, 42 tests |
| Latest PR CI | Passed through PR #15 |

## Current Readiness Against v0.2.0-alpha

KORA has reached the near-term 100-task deterministic-heavy workload target for `v0.2.0-alpha` evidence development. The benchmark track now has a reproducible generator, a committed generated workload, current benchmark summaries, and a technical preview results document with updated claim boundaries.

The project is not yet ready for a `v0.2.0-alpha` release because correctness scoring, result generation automation, artifact policy, and release readiness documentation still need to be completed.

## Remaining Gaps Before v0.2.0-alpha

- stronger expected-output correctness checks
- result summary generation automation
- raw result artifact policy decision
- expanded correctness, error, and fallback cases
- release note and final readiness check

## Recommended Next Tasks

1. Add deterministic expected-output correctness checks to the benchmark runner.
2. Add automated benchmark result summary generation from result JSON.
3. Decide whether raw benchmark JSON outputs should stay generated-only or become committed artifacts.
4. Add expanded correctness, malformed input, and fallback candidate coverage.
5. Draft the `v0.2.0-alpha` release note after the correctness path lands.
6. Run a final readiness check before any `v0.2.0-alpha` tag.
7. Keep the technical preview document aligned with the latest verified benchmark evidence.

## Worktree Safety

The dirty local `main` worktree remained untouched. All implementation, documentation, PR, and verification work was done through clean temporary worktrees and branches.
