# KORA Workload Control Layer

KORA is an **AI Workload Control Layer**.

It is based on a simple observation: not every AI-system task should immediately become a model invocation.

Many useful AI workflows contain work that can be classified, reused, routed, retrieved, validated, or handled by tools before a provider/model call is needed.

![KORA Workload Control Layer Architecture](../assets/kora_workload_control_layer_architecture.svg)

[View the architecture diagram](../assets/kora_workload_control_layer_architecture.svg)

## Model-Centric Systems

A common AI application shape is:

```text
input -> model -> output
```

That shape is simple, but it hides several decisions:

- Is the task deterministic?
- Has the same work already been done?
- Does the task need retrieval?
- Does the task need a local tool?
- Does the task truly require provider/model reasoning or generation?

KORA makes those decisions explicit.

## Workload-Centric Systems

KORA starts from the workload, not the model.

A workload enters KORA and is routed across paths such as:

- deterministic handling
- cache reuse
- retrieval-needed handling
- tool-needed handling
- provider-needed fallback

This lets developers inspect what kind of work exists in an AI system before treating every request as a model task.

## What KORA Contributes Today

KORA currently provides offline examples and CLI surfaces that demonstrate:

- workload inspection with KORA Doctor
- deterministic classification
- OpenAI-style proxy routing
- RAG-style route separation
- agent workflow routing
- cache reuse

The examples are intentionally small and reproducible. They are meant to show where workload control fits, not to claim production completeness.

## What KORA Does Not Claim

KORA does not currently claim:

- production cost reduction proof
- real API-cost reduction proof
- production readiness
- benchmark superiority
- full OpenAI API compatibility
- production RAG, agent, or cache correctness
- model replacement

## Why It Matters

The future of AI infrastructure is not only better models.

It is also deciding when models should be used at all.
