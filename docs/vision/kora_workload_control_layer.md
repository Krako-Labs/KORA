# KORA Workload Control Layer

Status: current vision document grounded in implemented examples and bounded evidence.

## Summary

KORA is an AI Workload Control Layer. It helps developers inspect work before sending it to a model, identify deterministic candidates, preserve provider/model fallback for ambiguous work, and report route rationale.

This vision is grounded in the current offline examples and evidence already present in the repository. It does not claim production readiness, model replacement, automatic savings, benchmark superiority, or broad workload superiority.

## Current AI Stack

Many AI applications are built around a model-centric path:

```text
request -> prompt -> model -> output
```

That path is useful for open-ended generation and semantic judgment. It is less precise for work that can be represented as routing, validation, policy, classification, cache reuse, or deterministic processing.

## Model-Centric Architectures

In a model-centric architecture, a provider/model call is often the default unit of work. This can hide important distinctions:

- some tasks are bounded classification.
- some tasks are validation or policy checks.
- some tasks are repeated lookups.
- some tasks are static transforms.
- some tasks need provider/model fallback.
- some tasks are ambiguous and should be escalated with rationale.

When every task is treated as a model problem, developers lose visibility into which work actually needed inference.

## Workload-Centric Architectures

A workload-centric architecture starts by asking what kind of work is being requested:

```text
request -> workload/task -> route decision -> deterministic handler or provider-needed fallback -> report
```

The unit of control is the workload task, not the model call. A workload-centric system can keep deterministic work explicit while preserving fallback for tasks that genuinely require a model.

## Why Control Matters

Control matters because AI systems are workflows, not only prompts. A system may need to:

- classify an input.
- validate a schema.
- route an incident.
- reuse a cached answer.
- apply a policy.
- transform a document.
- decide that semantic judgment or open-ended generation requires provider/model fallback.

KORA's role is to make these decisions explicit and reportable.

## What KORA Contributes Today

Current implemented examples demonstrate:

- KORA Doctor can inspect bundled offline sample workloads and identify deterministic candidates and provider-needed candidates without making provider calls.
- KORA Doctor Report Pack can aggregate counters across four bundled offline sample workloads.
- Deterministic Classification Pack can route synthetic classification tasks through KORA `TaskGraph` paths while preserving provider-needed fallback cases.
- First-value CLI commands can inspect, compare, run, and report over committed public fixtures.

Current evidence is bounded to offline examples, synthetic workloads, and public fixtures.

## Safe Boundaries

KORA currently does not claim:

- production cost reduction proof.
- broad workload superiority.
- production readiness.
- benchmark superiority.
- automatic savings.
- model replacement.
- production diagnostic accuracy.
- real API-cost proof.
- production proxy readiness.

Supported wording:

> KORA helps make AI workloads routable and controllable.

> In offline sample workloads, KORA Doctor identifies deterministic candidates and provider-needed candidates without making provider calls.

> In the deterministic classification example pack, KORA routes sample classification tasks to deterministic handlers while preserving provider-needed fallback cases.

## Direction

The near-term direction is examples-first:

- make KORA Doctor easier to run and inspect.
- keep deterministic classification examples visible.
- improve report readability.
- keep claim boundaries close to every example.
- add evidence only when backed by reproducible fixtures or validation reports.

The long-term direction is to help teams design AI systems around workload control instead of default model invocation.
