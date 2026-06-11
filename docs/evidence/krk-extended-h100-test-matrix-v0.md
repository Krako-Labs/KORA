# KRK Extended H100 Test Matrix v0

## Purpose

This document defines the next public-safe evidence layer for KRK, the KORA Routing Kernel.

KRK should not prove that KORA uses GPU-class compute more. KRK should prove that KORA knows when GPU-class compute should be used.

Public-safe headline:

> KORA benchmarks when GPU-class compute should be used, not raw GPU usage.

## KRK Definition

KRK means KORA Routing Kernel.

KRK is a deterministic-first execution routing kernel. It routes workload tasks across:

- deterministic.
- cache.
- CPU.
- provider.
- GPU.
- fallback.

## Matrix Profiles

### Mixed-Realistic

A balanced workload profile containing deterministic, cacheable, CPU-local, provider-suitable, GPU-suitable, and fallback-required requests.

Purpose:

- test route selectivity across all execution paths.
- prevent benchmark design from overfavoring a single route.
- produce route-distribution evidence.

### GPU-Heavy

A workload profile where several requests are expected to be GPU-suitable because of input size, batch size, modality, or estimated complexity.

Purpose:

- measure whether KRK can identify GPU-suitable subsets.
- separate GPU false positives from GPU false negatives.
- prepare bounded GPU-routed subset measurement.

### Cache-Heavy

A workload profile with repeated or cache-key-available requests.

Purpose:

- test cache-hit correctness.
- avoid unnecessary provider or GPU routing.
- measure compute-weighted GPU demand reduction without claiming production savings.

### Adversarial

A workload profile containing ambiguous, unsafe, malformed, privacy-sensitive, or intentionally conflicting routing metadata.

Purpose:

- test fallback behavior.
- identify unsafe misroutes.
- exercise policy conflict handling.

### Service-Replay Placeholder

A future profile for sanitized replay of service-shaped workloads.

Purpose:

- preserve a path for later public-safe replay evidence.
- avoid raw logs, private records, server details, or customer data.

This placeholder is not evidence of production behavior.

## Phases

### Dry-Run Comparison Phase

Run all matrix profiles through dry-run routing policies:

- `all_gpu`.
- `static_heuristic`.
- `provider_first_with_gpu_fallback`.
- `KRK`.

The dry-run phase should not require GPU access. It validates labels, route selectivity, fallback classification, and report generation.

### Bounded GPU-Routed Subset Measurement Phase

After dry-run validation, select only the requests KRK routes to GPU for bounded measurement.

This phase should measure the selected subset, not claim that all workloads benefit from GPU execution.

### Public-Safe Reporting Phase

Publish sanitized summaries:

- route distribution.
- exact and acceptable route metrics.
- GPU false positive and false negative counts.
- compute-weighted GPU demand.
- fallback classifications.
- reproducibility metadata.
- claim boundary.

Do not publish raw logs, private endpoints, private resource details, credentials, or server-local artifacts.

## What This Proves

This matrix can support bounded claims that:

- KRK can be evaluated as an execution-path routing kernel.
- KRK can compare route selectivity across deterministic, cache, CPU, provider, GPU, and fallback paths.
- KRK can prepare a bounded GPU-routed subset for measurement.
- KRK can produce reproducible routing evidence for public review.

## What This Does Not Prove

This matrix does not prove:

- production cost reduction.
- 10x savings.
- customer savings.
- infrastructure savings.
- broad workload superiority.
- H100 superiority.
- replacement of vLLM, OpenRouter, LiteLLM, OpenAI, Claude, Gemini, or other systems.
- production readiness.
- formal external validation.
