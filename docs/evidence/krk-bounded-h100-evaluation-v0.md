# KRK Bounded H100 Evaluation v0

Status: bounded GPU-routed subset measurement.

This document summarizes a bounded H100 evaluation for the KRK-selected GPU subset from the public matrix fixtures. The purpose is to validate that KRK-selected GPU subset items can be executed and measured, not to benchmark raw GPU performance.

## Purpose

KRK routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths. The route-selectivity evaluator identified the public matrix items whose expected route is GPU. This evaluation executes only that bounded subset and records public-safe aggregate measurements.

## Subset Selection

The measured subset came from public KRK matrix fixtures after route-selectivity evaluation.

| Request | Profile | Workload class | Expected route |
| --- | --- | --- | --- |
| cache-003 | cache-heavy | cache-miss-complex | GPU |
| gpu-001 | GPU-heavy | large-batch-generation | GPU |
| gpu-002 | GPU-heavy | multimodal-transform | GPU |
| mixed-004 | mixed-realistic | large-batch-embedding-like | GPU |

Subset count: 4.

## Execution Mode

The evaluation used a bounded CUDA execution path for the selected subset. It did not call external providers, run production traffic, or publish raw environment logs.

The measurement records:

- runtime.
- request throughput.
- compute-weight throughput.
- bounded workload memory allocation.
- public-safe GPU class.

## Results

| Metric | Value |
| --- | ---: |
| Subset count | 4 |
| Total compute weight | 58 |
| Runtime seconds | 0.035312 |
| Throughput, requests/second | 113.277481 |
| Throughput, compute weight/second | 1642.523477 |
| Bounded workload peak allocation MB | 240.000 |
| CUDA context memory used before MB | 525.062 |
| CUDA context memory used after MB | 525.062 |

Generated summaries:

- [Generated H100 bounded JSON summary](generated/krk-h100-bounded-summary-v0.json)
- [Generated H100 bounded Markdown summary](generated/krk-h100-bounded-summary-v0.md)

## What This Proves

This supports a bounded statement that KRK-selected GPU subset items from the public matrix fixtures were executed in an H100-class environment and summarized with runtime, throughput, and memory measurements.

It connects the dry-run route-selectivity evidence to a small measured execution path.

## What This Does Not Prove

This does not prove:

- production cost reduction.
- customer savings.
- provider superiority.
- GPU superiority.
- broad workload superiority.
- infrastructure savings.
- production readiness.

## Public Boundary

The committed summary intentionally excludes raw logs, infrastructure identifiers, server names, IPs, user names, SSH details, private resource details, and local-only paths.

## Claim Level

`bounded_h100_routed_subset_measured`
