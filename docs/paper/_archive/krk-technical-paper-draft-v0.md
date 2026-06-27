# KRK Technical Paper Draft v0

Status: public-safe working draft. This is not submission-ready.

## Abstract

AI workloads increasingly span deterministic logic, caches, CPU-local execution, hosted providers, GPU-class targets, and fallback paths. Many systems still treat model execution as the default first step, even when parts of a workload can be resolved by deterministic or structured routes. The KORA Routing Kernel, or KRK, introduces deterministic-first execution routing for AI workloads. KRK routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths, and records evidence about the route decision. This draft positions KRK as the first technical wedge toward KORA Core, an open-source AI workload execution layer. Current public evidence is bounded: in a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline, with zero deterministic mismatches. Routing accuracy, bounded GPU-routed subset metrics, and provider-backed validation remain future experiments.

## 1. Introduction

KORA's north star is to make AI workloads routable. The core idea is that AI execution should not begin with an automatic model call. A workload may contain deterministic logic, cacheable work, CPU-local computation, provider-suitable work, GPU-suitable work, or unsafe and unavailable paths that require fallback.

KRK, the KORA Routing Kernel, is the first technical wedge toward this direction. It focuses on execution-path routing before the broader KORA Core surface expands into inspect, compare, run, report, and doctor workflows.

This draft explains KRK as a deterministic-first execution routing kernel and summarizes the current public evidence package. It does not claim production readiness, infrastructure savings, or superiority over model serving systems, API routers, or provider platforms.

## 2. Background and Motivation

AI application stacks are becoming more heterogeneous. Developers can choose local model runtimes, hosted providers, cache layers, deterministic tools, batch execution, GPU serving stacks, and fallback services. Without explicit routing, those choices are often hidden in application code or reduced to a default provider call.

That creates several problems:

- model execution may happen before simpler paths are tried.
- benchmark artifacts may report outcomes without explaining route selection.
- fallback behavior may be hard to reproduce.
- GPU-class execution may be treated as a capacity question rather than a selectivity question.
- public claims may drift beyond measured evidence.

KRK is motivated by the need to make the execution path explicit, explainable, and measurable.

## 3. Problem: AI Execution Path Fragmentation

Execution fragmentation means that a single workload can plausibly run through many different paths:

- deterministic logic.
- cache reuse.
- CPU-local execution.
- provider-backed model execution.
- GPU-class execution.
- fallback.

Each path has different privacy, latency, cost, quality, and availability implications. A routing kernel should not simply maximize use of one path. It should decide which path is justified for each workload item and leave evidence that reviewers can inspect.

For KRK, the central evaluation question is:

> Did KRK select an acceptable execution path for the workload?

## 4. KORA Routing Kernel

KRK means KORA Routing Kernel. It is the deterministic-first execution routing kernel inside KORA Core.

A KRK routing decision should include:

- workload identity.
- router-visible metadata.
- selected execution path.
- rejected or lower-priority paths.
- policy context.
- fallback classification when relevant.
- reproducibility metadata.
- claim boundary.

Oracle labels used for benchmark evaluation must remain separate from router-visible metadata. This prevents a benchmark harness from giving the router the answer it is supposed to infer.

## 5. Deterministic-First Routing

Deterministic-first routing asks whether a workload can be resolved before default model execution.

The routing preference is not a fixed universal order. It is a policy-governed evaluation of available paths:

- deterministic when known logic, rules, templates, or validation can resolve the request.
- cache when reuse is valid under the workload policy.
- CPU when local execution is adequate.
- provider when model execution is appropriate and allowed.
- GPU when workload shape, batch size, modality, or complexity justifies GPU-class compute.
- fallback when policy, safety, validation, malformed input, or target availability prevents a preferred route.

This framing makes KRK a routing kernel rather than a provider replacement.

## 6. Benchmark Methodology

The current KRK benchmark methodology separates router-visible metadata from oracle-only labels.

Router-visible metadata may include:

- input size.
- batch size.
- request modality.
- cache key availability.
- latency sensitivity.
- privacy preference.
- estimated complexity.

Oracle-only labels include:

- expected route.
- acceptable routes.
- disallowed routes.
- oracle reason.

Planned metrics include exact route accuracy, acceptable route rate, unsafe misroute rate, GPU false positives and false negatives, cache-hit correctness, fallback rates, and compute-weighted GPU demand. The current public package defines these metrics, but extended matrix results are not measured yet.

## 7. Evidence Package

The current public evidence package contains one measured deterministic-heavy benchmark path and several methodology artifacts.

Current deterministic-heavy benchmark:

| Metric | Value |
| --- | ---: |
| Total tasks | 100 |
| Deterministic/no-model tasks | 80 |
| Fallback/model-candidate tasks | 20 |
| Direct-baseline simulated model invocations | 100 |
| KORA-controlled simulated model invocations | 20 |
| Avoided simulated model invocations | 80 |
| Deterministic mismatches | 0 |

Approved bounded wording:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

The evidence package also includes:

- KRK architecture and quickstart docs.
- KRK extended matrix docs and fixture workloads.
- KRK routing benchmark methodology.
- KRK performance table package.
- KRK reproducibility matrix.
- KRK claim boundary table.

The current public package does not include measured routing accuracy, measured compute-weighted GPU demand, provider-backed validation, or public-safe H100 task count, runtime, throughput, and memory tables.

## 8. Limitations

The current evidence is alpha-stage and bounded.

Limitations:

- The deterministic-heavy benchmark is simulated.
- The evidence does not prove production behavior.
- The extended matrix fixtures are not yet connected to an evaluator.
- Route accuracy metrics are not measured yet.
- GPU-routed subset measurement is methodology-only in the current package.
- Provider-routed validation is not included in the current package.
- The current CLI exposes `examples`, `run`, `studio`, and `telemetry`; standalone KRK commands remain roadmap unless implemented and tested.

The paper must not imply production cost reduction, customer savings, infrastructure savings, broad workload superiority, H100 superiority, replacement of vLLM, OpenRouter, LiteLLM, OpenAI, Claude, Gemini, or formal validation.

## 9. Expansion Toward KORA Core

KRK is the first technical wedge toward KORA Core. KORA Core is the planned open-source AI workload execution layer.

Future KORA Core workflows may include:

- inspect.
- compare.
- run.
- report.
- doctor.

Future modules may include:

- KORA Workload Spec.
- KORA Target Registry.
- KORA Evidence Report.
- adapters.
- examples.
- developer preview materials.

These are expansion directions. They should not be described as complete unless the corresponding commands, tests, and docs exist.

## 10. Conclusion

KRK frames AI workload execution as an explicit routing problem. Instead of treating model execution as the default first step, KRK evaluates deterministic, cache, CPU, provider, GPU, and fallback paths and records bounded evidence about the decision.

The current evidence supports a narrow but useful claim: deterministic-first routing can avoid simulated model invocations in a reproducible deterministic-heavy benchmark. The next paper iteration should add measured route-selectivity results from the extended matrix, compute-weighted GPU demand, provider-routed sample validation, and bounded GPU-routed subset measurement before making stronger claims.
