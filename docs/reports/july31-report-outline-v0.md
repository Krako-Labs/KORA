# July 31 Report Outline v0

Status: planning outline. This is not a final report, submission, PDF, or competition-result claim.

## Purpose

This outline packages the July 31 public-safe narrative for KORA:

- validate KRK first.
- expand KRK into KORA Core.
- show bounded evidence.
- explain the next development plan.

KRK means KORA Routing Kernel. It is the deterministic-first execution routing kernel inside KORA Core.

KORA Core is the planned open-source AI workload execution layer for inspect, compare, run, and report workflows.

## Working Title

KORA Core: Making AI Workloads Routable with the KORA Routing Kernel

## Executive Summary

KORA's north star is to make AI workloads routable.

The current public alpha focuses on KRK, the KORA Routing Kernel. KRK frames AI execution as a route decision across deterministic, cache, CPU, provider, GPU, and fallback paths. The July 31 package should explain that this is the first technical wedge toward KORA Core, not a final production platform.

Public-safe executive summary points:

- KORA makes AI workloads routable.
- KRK is the deterministic-first routing kernel inside KORA Core.
- The current alpha includes bounded deterministic-heavy benchmark evidence.
- The KRK technical paper draft explains the routing model and limitations.
- KORA Core expands KRK toward inspect, compare, run, and report.
- The next development plan focuses on executable route-selectivity evaluation, workload and target specs, evidence reporting, examples, and community feedback.

## 1. Problem Statement

AI execution is fragmenting across deterministic logic, caches, CPU-local paths, hosted providers, GPU-class targets, and fallback paths.

The July 31 report should frame the problem as execution-path selection:

- Developers need to know when a model call is necessary.
- Benchmark evidence should explain route decisions.
- GPU-class compute should be selected when justified by workload shape and policy, not treated as the default proof target.
- Claims should remain tied to reproducible artifacts.

## 2. KRK Implementation And Evidence

Explain KRK as:

- KORA Routing Kernel.
- deterministic-first execution routing kernel.
- first technical wedge toward KORA Core.
- current alpha surface for route, explain, benchmark, and report primitives.

Current implementation context:

- The top-level CLI currently exposes example-oriented commands.
- KRK standalone command names are documented alpha primitives and roadmap surfaces unless implemented and tested.
- Current evidence is deterministic-heavy and bounded.

## 3. KRK Performance And Evidence Table References

Reference these public evidence artifacts:

- [KRK July 1 evidence summary v0](krk-july1-evidence-summary-v0.md)
- [KRK performance table v0](../evidence/krk-performance-table-v0.md)
- [KRK evidence package v0](../evidence/krk-evidence-package-v0.md)
- [KRK reproducibility matrix v0](../evidence/krk-reproducibility-matrix-v0.md)
- [KRK claim boundary table v0](../evidence/krk-claim-boundary-table-v0.md)
- [KRK routing benchmark methodology v0](../evidence/krk-routing-benchmark-methodology-v0.md)
- [KRK extended H100 test matrix v0](../evidence/krk-extended-h100-test-matrix-v0.md)

Allowed bounded evidence statement:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

Preserve the qualifiers:

- deterministic-heavy workload.
- simulated model invocations.
- naive direct baseline.
- alpha-stage public evidence.
- not production proof.

## 4. Technical Paper Status

Reference:

- [KRK technical paper draft v0](../paper/krk-technical-paper-draft-v0.md)
- [KRK technical paper outline v0](../paper/krk-technical-paper-outline-v0.md)
- [KRK paper claim boundary v0](../paper/krk-paper-claim-boundary-v0.md)
- [KRK paper next experiments v0](../paper/krk-paper-next-experiments-v0.md)

The report should describe the paper as a working technical note draft, not a submission-ready paper.

## 5. KORA Core Expansion

Position the expansion as deliberate strategy:

1. Validate deterministic-first Routing Kernel behavior through KRK.
2. Use KRK as the first technical wedge.
3. Expand into KORA Core, the AI workload execution layer.

KORA Core workflow:

- inspect: understand workload shape, policy, targets, and evidence readiness.
- compare: compare route policies, target options, baselines, and evidence expectations.
- run: execute explicit workload paths under policy and target constraints.
- report: generate bounded, reproducible evidence.

Reference:

- [KORA Core alpha surface v0](../product/kora-core-alpha-surface-v0.md)
- [KORA Core user workflow v0](../product/kora-core-user-workflow-v0.md)
- [KORA Core expansion plan v0](../product/kora-core-expansion-plan-v0.md)

## 6. Examples And Developer Preview

The report should point to examples as a developer adoption path:

- deterministic-heavy benchmark.
- KRK matrix workload fixtures.
- local validation examples.
- future Workload Spec examples.
- future Target Registry examples.
- future Evidence Report examples.

The developer preview should focus on reproducibility, not broad performance claims.

## 7. Naming And Repo Strategy

Reference:

- [KORA naming strategy v0](../strategy/kora-naming-strategy-v0.md)
- [KORA repo restructuring plan v0](../strategy/kora-repo-restructuring-plan-v0.md)
- [KORA post-July roadmap v0](../strategy/kora-post-july-roadmap-v0.md)

Public-safe report message:

- KORA is the umbrella.
- KORA Core is the OSS execution layer.
- KRK is the routing kernel inside KORA Core.
- Repo restructuring is planned, not executed.

## 8. Limitations

State limitations directly:

- KORA Core inspect, compare, run, and report are not fully implemented as first-class workflow commands.
- Route accuracy metrics are not measured yet for the extended matrix.
- GPU-routed subset measurement is methodology-only in the current public package.
- Provider-backed validation remains incomplete.
- The current deterministic-heavy benchmark is bounded and simulated.
- The report package is planning/readiness material, not final validation.

## 9. Next Plan

The next plan should focus on:

- KRK extended matrix dry-run evaluator.
- route correctness metrics.
- compute-weighted GPU demand metric.
- bounded GPU-routed subset measurement.
- KORA Core inspect and compare implementation.
- Workload Spec, Target Registry, and Evidence Report schemas.
- examples and community feedback.

## Claim Boundary

Do not claim:

- production savings.
- 10x savings.
- customer-level savings.
- infrastructure savings.
- broad workload superiority.
- H100 superiority.
- final competition result.
- formal validation.
- replacement of model serving systems, API routers, or model providers.
