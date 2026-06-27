# KORA First Paper Related Work Map

## Purpose

This document maps reference categories needed before submission. It does not add citations yet. References should be collected, verified, and added later with accurate BibTeX or venue metadata.

Reference scaffold docs:

- [KORA first paper reference plan](kora-first-paper-reference-plan.md)
- [KORA first paper reference tracker](kora-first-paper-reference-tracker.md)
- [KORA first paper bibliography notes](kora-first-paper-bibliography-notes.md)

## Related Work Categories

### LLM Serving and Inference Systems

Purpose:

Cite systems that optimize serving, inference throughput, scheduling, batching, and runtime efficiency.

Use this category as background for model-serving efficiency. Avoid claiming that KORA outperforms these systems unless direct evidence is collected later.

### LLM Agents and Tool Routing

Purpose:

Cite work on routing tasks through tools, planners, agent loops, or execution policies.

Use this category to position KORA near tool-using systems while emphasizing that the paper focuses on deterministic-first execution control before model invocation.

### Programmatic / Deterministic AI Workflows

Purpose:

Cite work where deterministic code, typed interfaces, policy checks, structured execution, or programmatic control complements model inference.

Use this category to explain why structured work should not always begin with model inference.

### Caching and Retrieval-Augmented Generation

Purpose:

Explain how KORA differs from caching and RAG:

- KORA is not just cache lookup.
- KORA controls execution path before model invocation.
- KORA includes validation, telemetry, and model escalation boundaries.

Caching and RAG may reduce repeated work or ground generation, but KORA's paper should frame its contribution as execution-control routing before inference.

### Workflow Orchestration and DAG Execution

Purpose:

Cite task graph, workflow, and DAG execution systems as background, while positioning KORA for AI execution control.

Use this category to explain how KORA borrows the discipline of explicit execution paths while adapting it to model-call boundaries and validation counters.

### Evaluation and Reproducibility

Purpose:

Cite work on reproducible benchmarks, synthetic workloads, artifact reporting, and transparent evaluation.

Use this category to justify local/no-network validation, aggregate counter reporting, and clear claim boundaries.

## Reference Collection TODO

- Collect 15-25 references.
- Prefer peer-reviewed or official project papers/docs.
- Avoid unsupported comparisons.
- Add BibTeX later.
- Verify all citations before submission.
- Do not add fake citations.
- Do not invent paper titles.
- Do not cite sources without verifying later.

## Verification Pass 1 Mapping

The first verified reference pass collected 10 citation candidates:

- LLM serving and inference systems: vLLM/PagedAttention, MLPerf Inference, ONNX Runtime.
- Agent/tool routing and orchestration: LangGraph official docs.
- Programmatic / deterministic AI workflows: DSPy.
- Caching and retrieval-augmented generation: RAG foundational paper.
- Workflow orchestration and DAG execution: Apache Airflow DAG docs, Snakemake.
- Evaluation and reproducibility: MLPerf Inference, ACM Artifact Review and Badging.
- Local model runtime systems: llama.cpp official repository.

These references are candidates for manuscript integration. They should not be used to support production, API-cost, energy, or broad workload superiority claims.

## Manuscript v0.2 Mapping

Manuscript v0.2 integrates the first verified reference pass as preliminary citation labels:

- LLM serving and inference systems: [R01], [R02], [R03].
- Agent/tool routing and programmatic AI workflows: [R04], [R05].
- Retrieval-augmented generation: [R06].
- Workflow and DAG orchestration: [R07], [R08].
- Local model/runtime systems: [R03], [R09].
- Benchmarking and artifact evaluation: [R02], [R10].

These labels remain preliminary until final citation style and bibliography normalization are complete.

## Verification Pass 2 Mapping

The second verified reference pass collected 8 additional citation candidates:

- Agent/tool routing and orchestration: ReAct, Toolformer.
- Programmatic / deterministic AI workflows: PAL.
- Caching and retrieval-augmented generation: GPTCache.
- Local model runtime systems: Ollama official docs and repository.
- Evaluation and reproducibility: NeurIPS reproducibility program report.
- Systems artifact evaluation practices: USENIX NSDI artifact guidance, MLSys artifact evaluation guidance.

These references are not yet integrated into manuscript v0.2. They should be used in a later manuscript pass only as background, positioning, reproducibility, or future-work context. They should not support production, API-cost, energy, broad superiority, artifact approval, or submission-readiness claims.

## Manuscript v0.3 Integration Planning

The [manuscript v0.3 reference integration plan](kora-first-paper-manuscript-v0-3-reference-integration-plan.md) maps `[R11]` through `[R18]` to future manuscript decisions.

Summary:

- Integrate `[R11]`, `[R12]`, and `[R13]` if v0.3 expands agent/tool-use and programmatic workflow related work.
- Keep `[R14]`, `[R15]`, and `[R16]` optional unless caching, local runtime, or reproducibility sections expand.
- Defer `[R17]` and `[R18]` until target venue or artifact package planning.

## Manuscript v0.3 Integration Status

Manuscript v0.3 now integrates `[R11]`, `[R12]`, and `[R13]` as related-work background for agent/tool-use and program-aided language-model workflows.

`[R14]` through `[R18]` remain tracker/audit-only, optional, or deferred. They should not be used to support production, API-cost, energy, broad superiority, artifact approval, or submission-readiness claims.

## Benchmark-Construction Reference Pass Mapping

The benchmark-construction reference pass collected 6 additional citation candidates:

- Benchmark-suite construction and broad task design: BIG-bench.
- Holistic and multi-metric language-model evaluation: HELM.
- Software-engineering task benchmark construction: SWE-bench.
- Agent benchmark construction: AgentBench.
- Dynamic benchmark methodology: Dynabench.
- Behavior-oriented evaluation and test design: CheckList.

These references are tracker/audit entries only for now. They may support a later benchmark-methodology section, but they should not be used to imply KORA has production benchmark evidence, production cost reduction, real API-cost reduction, energy reduction, or broad workload superiority.
