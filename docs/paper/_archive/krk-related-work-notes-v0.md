# KRK Related Work Notes v0

Status: public-safe related-work placeholders. This is not a completed literature review.

These notes identify adjacent system categories for a future KRK technical note. They should be expanded with citations and careful comparisons before submission.

## Model Serving Systems

Model serving systems focus on efficient model execution, batching, scheduling, throughput, memory use, and deployment operations.

Examples to review neutrally:

- vLLM.
- SGLang.

KRK should not claim to replace or outperform model serving systems. KRK is concerned with execution-path selection before and around model execution.

## API And Model Routers

API/model routers help applications select among providers, models, fallbacks, and policy constraints.

Examples to review neutrally:

- LiteLLM.
- OpenRouter.

KRK should not claim to replace or beat these systems. A future paper should explain whether KRK's deterministic-first routing layer is complementary, narrower, or differently scoped.

## Workflow Orchestration

Workflow orchestration systems structure tasks, dependencies, retries, schedules, and operational execution.

KRK is not a general workflow orchestrator. The relevant comparison is how a routing kernel decides execution paths for AI workload tasks and how that decision becomes evidence.

## Benchmark And Evaluation Harnesses

Benchmark and evaluation harnesses define workloads, metrics, reproducibility metadata, and result interpretation.

KRK should connect to this category through:

- oracle-label separation.
- public-safe benchmark fixtures.
- route correctness metrics.
- fallback classification.
- claim boundary tables.

## Local Model Runtimes

Local model runtimes allow models to run on local or developer-controlled machines.

Examples to review neutrally:

- Ollama.
- llama.cpp.

KRK should not claim to replace local runtimes. It can route to local runtime targets when policy and workload metadata justify that path.

## GPU Serving Stacks

GPU serving stacks support high-throughput or latency-sensitive model execution on GPU-class infrastructure.

KRK should frame GPU-class execution as a route that must be justified by workload shape, batch size, modality, policy, or complexity. The paper should not claim H100 superiority or GPU infrastructure reduction.

## Comparison Rules

Future related-work writing should:

- describe adjacent systems by category before naming examples.
- avoid "beats", "replaces", or "is cheaper than" language.
- state what KRK does differently only when the distinction is supported by implemented artifacts.
- keep early evidence bounded to deterministic-heavy benchmark results and methodology docs.
- avoid claiming production readiness or formal validation.
