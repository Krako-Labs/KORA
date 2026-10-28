# KORA Research Paper and Reproducibility

**Paper:** [KORA: Deterministic-First Execution Control for AI Workloads](https://arxiv.org/abs/2610.35869)
**Author:** Albert Heekwan Kim
**Identifier:** arXiv:2610.35869
**Status:** Public arXiv preprint. This is not a peer-reviewed acceptance or a formal artifact-evaluation result.

<br />

## What the Paper Describes

KORA places a deterministic-first control layer before model inference. It structures work into task paths, attempts deterministic or structured handling first, validates outcomes, records telemetry, and escalates to model-candidate paths when needed.

The paper discusses two *bounded* evidence shapes:

- A deliberately deterministic-heavy 100-task synthetic benchmark, counting 100 simulated model invocations in the naive model-first baseline and 20 in the controlled path. **80 simulated invocations are avoided** in that workload.
- A separate 12-request synthetic customer-support local/no-network validation workload, used to exercise route and avoided-call accounting. This is not live provider or production evidence.

Neither result proves production cost reduction, broad workload superiority, real API-provider savings, energy reduction, or general output quality.

<br />

## Reproduce the Repository's Public 100-Task Counter Benchmark

The version-controlled benchmark uses seed `42` and the file `experiments/workloads/deterministic_heavy_v1_100.json`. From a source checkout:

```bash
python3 experiments/generate_workload.py --count 100 --seed 42 --benchmark-name deterministic_heavy_v1 --output /tmp/kora_deterministic_heavy_v1_100.regenerated.json
cmp experiments/workloads/deterministic_heavy_v1_100.json /tmp/kora_deterministic_heavy_v1_100.regenerated.json

python3 experiments/run_benchmark.py --mode direct-baseline --workload experiments/workloads/deterministic_heavy_v1_100.json --output /tmp/kora_direct_baseline.json
python3 experiments/run_benchmark.py --mode kora-controlled --workload experiments/workloads/deterministic_heavy_v1_100.json --output /tmp/kora_controlled.json
```

The commands reproduce **simulated invocation accounting**. They do not call a model or measure billed cost. See the [benchmark report](benchmarks/kora_benchmark_result_v1_100.md) for its full command set, validation status, and limitations.

<br />

## Evidence Alignment Note

The paper describes evaluation at the level of task categories including FAQ-style lookup, policy/rule checking, schema/format validation, and transformation. The repository's original `deterministic_heavy_v1_100.json` generator has ten concrete categories, including arithmetic, normalization, validation, routing, cache lookup, and unit conversion. These descriptions should **not** be treated as a verified category-by-category mapping without a separately published reconciliation.

The paper reports 80 deterministic outputs checked and zero mismatches in its bounded subset. The older [repository benchmark report](benchmarks/kora_benchmark_result_v1_100.md) originally said that correctness scoring was not yet reported. A 2026-10-28 replay against public `origin/main` at `40ca43e8` ran its seeded workload generator, verified the generated JSON byte-for-byte, and reproduced 80 deterministic expected-output checks with zero mismatches using `experiments/run_benchmark.py --mode kora-controlled`. The benchmark report records this as a dated update. These are **fixture-derived deterministic checks**, not proof of model-output quality, broader tasks, or real-provider correctness.

Do not add the two evidence paths together or describe them as independent production validations.

<br />

## Code, Sources, and Claim Boundaries

- [KORA source](https://github.com/Krako-Labs/KORA)
- [Paper on arXiv](https://arxiv.org/abs/2610.35869)
- [Benchmark report](benchmarks/kora_benchmark_result_v1_100.md)
- [Public claim registry](claims/kora-claim-registry.md)
- [Public language guide](claims/kora-public-language-guide.md)
