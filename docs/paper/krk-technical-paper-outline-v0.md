# KRK Technical Paper Outline v0

Status: draft planning outline. This is not a submission-ready paper.

## Title Candidates

- KORA Routing Kernel: Deterministic-First Execution Routing for AI Workloads
- Making AI Workloads Routable with Deterministic-First Execution Routing
- KRK: An Execution-Path Routing Kernel for Heterogeneous AI Workloads

## Abstract Skeleton

AI workloads increasingly span deterministic logic, caches, CPU-local execution, model providers, GPU-class execution, and fallback paths. The KORA Routing Kernel, or KRK, explores deterministic-first execution routing as a way to make those paths explicit and reviewable. This draft presents KRK as the first technical wedge toward KORA Core, describes its execution paths and benchmark methodology, and summarizes current bounded alpha evidence. In the current deterministic-heavy public benchmark, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline, with zero deterministic mismatches. The paper should treat routing accuracy, provider-backed validation, and bounded GPU-routed subset measurement as future experiments until measured public evidence exists.

## 1. Introduction

- Motivate the north star: make AI workloads routable.
- Explain why model-first execution hides path selection.
- Introduce KRK as deterministic-first execution routing.
- State that KRK is the first technical wedge toward KORA Core.
- Preview current evidence and limitations.

## 2. Problem Statement

- AI execution paths are fragmenting across local runtimes, hosted providers, caches, CPU paths, GPU-class targets, and fallbacks.
- Developers need a way to decide when a workload requires model execution and when another path is sufficient.
- Benchmarking should measure route selectivity and evidence quality without turning early results into production claims.

## 3. KRK Design

- Define KORA Routing Kernel.
- Place KRK inside KORA Core.
- Describe routing input, route decision, explanation, and evidence output.
- Separate router-visible metadata from oracle-only benchmark labels.

## 4. Deterministic-First Routing

- Start with deterministic work before inference.
- Use cache when reuse is valid.
- Use CPU when local execution is adequate.
- Use provider or GPU-class execution only when workload shape and policy justify it.
- Use fallback when policy, safety, validation, or availability requires it.

## 5. Execution Paths

Execution paths:

- deterministic.
- cache.
- CPU.
- provider.
- GPU.
- fallback.

This section should define each path and explain what evidence should accompany the selected route.

## 6. Benchmark Methodology

- Use independent oracle labels for evaluation.
- Keep oracle labels out of router input.
- Compare against baseline policies such as `all_gpu`, `static_heuristic`, and `provider_first_with_gpu_fallback`.
- Track route accuracy, acceptable-route rate, unsafe misroute rate, cache correctness, fallback rates, and compute-weighted GPU demand.
- Version compute-weight formulas.

## 7. Evidence Summary

Current public evidence:

- deterministic-heavy 100-task benchmark.
- 80 deterministic/no-model tasks.
- 20 fallback/model-candidate tasks.
- 80 avoided simulated model invocations versus a naive direct baseline.
- 0 deterministic mismatches.
- KRK extended matrix docs and fixture workloads.
- KRK performance table package and claim boundary docs.

## 8. Limitations

- Current evidence is alpha-stage and bounded.
- Current deterministic-heavy evidence is simulated.
- Extended matrix fixtures are not yet connected to a runner.
- Routing accuracy metrics are not measured yet.
- Bounded GPU-routed subset metrics are not included in the current public package.
- The paper must not imply production readiness or broad workload superiority.

## 9. KORA Core Expansion

- KRK feeds future KORA Core workflows: inspect, compare, run, report, and doctor.
- Future KORA Core modules include Workload Spec, Target Registry, Evidence Report, adapters, examples, and developer preview materials.
- These should be framed as expansion work unless implemented and tested.

## 10. Conclusion

- Restate the contribution: deterministic-first execution routing for routable AI workloads.
- Emphasize evidence over claims.
- Point to next experiments.

## Next Experiments

- 100K routed workload dry-run.
- multi-profile matrix evaluator.
- oracle-label independence checks.
- compute-weighted GPU demand reporting.
- bounded GPU-routed subset measurement.
- provider-routed sample validation.
- adversarial fallback evaluation.
- service-replay profile.
