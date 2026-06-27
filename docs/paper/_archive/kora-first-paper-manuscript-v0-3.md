# KORA: Deterministic-First Execution Control for AI Workloads

## Abstract

Model-first AI systems often call models too early: every request becomes a prompt even when the work is structured, deterministic, policy-driven, or validation-oriented. KORA introduces deterministic-first execution control, an execution-control layer placed before inference. Requests are represented as structured task paths, deterministic and structured routes are attempted first, validation checks confirm expected outcomes, and model escalation is used only when a request cannot be handled safely without inference. This manuscript v0.3 integrates the first verified reference pass and selected agent/tool-use references from the second verified reference pass. It evaluates KORA through the current public evidence: a reproducible deterministic-heavy benchmark and a synthetic customer-support local/no-network validation workload. In the deterministic-heavy benchmark, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline, with zero mismatches. The customer-support workload shows that KORA can measure avoided model-call events in synthetic local/no-network validation. These results support model invocation reduction and validation/reporting visibility in documented workloads. They are not production cost proof, real API-cost proof, energy evidence, production validation, or broad workload superiority evidence.

## 1. Introduction

Many AI systems treat every request as a model invocation. A request enters the application, the application builds a prompt, the model produces a response, and downstream logic validates or formats the result. This model-first pattern is easy to adopt, but it makes inference the default execution path even when the requested work does not require open-ended model reasoning.

This default is unnecessary for many deterministic, structured, validation, policy, and routing tasks. Password reset instructions, policy lookups, report formatting, schema validation, routing decisions, and budget checks often have known rules or expected output properties. A model may still be needed for ambiguous, context-heavy, generative, or policy-sensitive cases, but those cases should be explicit escalations rather than the default for the entire workload.

KORA inserts an execution-control layer before inference. Instead of treating the model as the first stop, KORA represents requests as task paths, attempts deterministic or structured handling when appropriate, validates the route outcome, records counters, and escalates only when deterministic handling is insufficient.

Structure first. Inference second.

This paper draft makes four contributions:

- It defines KORA's deterministic-first execution-control model for routing AI work before inference.
- It distinguishes KORA from related systems that optimize model serving, orchestrate workflows, structure agent execution, retrieve context, or provide local inference runtimes.
- It reports the current reproducible deterministic-heavy benchmark result: an 80% model invocation reduction with zero mismatches in the documented workload.
- It summarizes a synthetic customer-support local/no-network validation workload that measures avoided model-call events, deterministic routes, and model escalations without external providers, API keys, private data, or network calls.

## 2. Background and Related Work

KORA is related to model-serving systems, workflow orchestration systems, agent and programmatic AI frameworks, retrieval-augmented generation, local runtime systems, and artifact-evaluation practices. The relationship is complementary: KORA focuses on deciding whether inference is needed for a request before model invocation, while many related systems optimize or organize execution once a model, workflow, or retrieval path is already selected.

### 2.1 LLM Serving and Inference Systems

LLM serving systems optimize the execution of model inference. vLLM and PagedAttention address efficient memory management for large language model serving [R01]. MLPerf Inference provides benchmark framing for inference performance and comparability [R02]. ONNX Runtime provides an official inference runtime and optimization stack [R03].

KORA does not claim to improve serving internals, scheduler design, batching, memory management, kernel performance, or model runtime efficiency. Those systems matter after a model invocation is needed. KORA focuses on the preceding control question: whether a request should reach inference at all.

### 2.2 Workflow and DAG Orchestration

Workflow systems such as Apache Airflow describe computation in DAG-oriented workflows [R07]. Snakemake provides a workflow-engine model for reproducible pipelines [R08]. These systems show the value of explicit execution structure, dependency ordering, and reproducible task paths.

KORA borrows the discipline of explicit execution paths, but its scope is narrower and AI-specific. It applies task-path structure to model-call boundaries, deterministic route validation, model escalation, and aggregate counters. KORA is not a general-purpose workflow scheduler and does not claim to replace workflow or DAG systems.

### 2.3 Agent/Tool Routing and Programmatic AI Workflows

Graph-based and agent-oriented frameworks can coordinate state, tools, and execution graphs. LangGraph documents graph-based agent execution primitives [R04]. DSPy describes declarative language-model pipelines and programmatic composition around model calls [R05].

Agentic and tool-using language model systems provide further context. ReAct combines reasoning traces with actions to let language models interact with external environments and tools [R11]. Toolformer studies how language models can learn to use external tools through a model-centered training procedure [R12]. These systems help frame the broader space of model-mediated reasoning, actions, and tool use.

Program-aided language model workflows provide another adjacent pattern. PAL uses language models to generate programs that are executed by an interpreter, separating some reasoning work into executable program structure [R13]. This is relevant background for programmatic AI workflows, but it is not evidence for KORA's model-call avoidance result.

KORA is adjacent to this space but emphasizes a different default. Agent and programmatic AI systems often organize model-centered workflows, generated programs, or tool-use behavior. KORA's central concern is deterministic-first execution control: using task structure, deterministic handlers, policy checks, and validation boundaries before deciding whether model inference is needed. KORA is complementary to these approaches: rather than teaching a model to reason through actions, use tools, or generate programs, KORA controls the execution path around the model and routes deterministic work before inference when possible. This paper does not claim that KORA replaces or outperforms agent frameworks, tool-use systems, or program-aided language model workflows.

### 2.4 Retrieval-Augmented Generation

Retrieval-augmented generation grounds model outputs by retrieving external knowledge before generation [R06]. RAG is useful when a model still needs to generate or reason with retrieved context.

KORA is not a RAG replacement. RAG improves context selection for model use. KORA decides whether a task needs inference at all. A future system could use both: KORA could route deterministic work without inference and escalate retrieval-grounded questions to a RAG path when model reasoning is required.

### 2.5 Local Model and Runtime Systems

Local runtime systems make it possible to run inference locally. The llama.cpp project provides local LLM inference in C/C++ [R09]. ONNX Runtime is also relevant as an inference runtime [R03].

This paper uses local/no-network validation for current public evidence, but it does not present local model runtime validation as complete. Local runtime references are included as future-work context only. KORA does not currently claim measured local model performance, local runtime superiority, or integration evidence from llama.cpp, ONNX Runtime, Ollama, or other local runtimes.

### 2.6 Benchmarking and Artifact Evaluation

Benchmark and artifact practices matter because KORA's current evidence depends on reproducible commands, synthetic workloads, aggregate counters, and explicit claim boundaries. MLPerf Inference is relevant as benchmark-methodology context [R02]. ACM Artifact Review and Badging provides a public framework for artifact and reproducibility expectations [R10].

KORA has not undergone formal artifact evaluation or external validation. This paper uses those references only to motivate transparent reporting: reproducible commands, clear workload boundaries, local/no-network labels, and explicit non-claims.

## 3. KORA Execution Model

KORA is an execution-control layer between request intake and model invocation. Its current public design uses a small set of concepts:

- task graph: the structured representation of possible work paths
- deterministic route: a path resolved through known logic, rules, templates, or validation checks
- structured lookup: a path that maps to a known lookup or backend placeholder
- policy/validation: checks that confirm the route and output properties are acceptable
- model escalation: the boundary used when deterministic handling is not sufficient
- telemetry/reporting: counters and reports that summarize route decisions and validation outcomes

The high-level flow is:

```text
Request -> Task Graph -> Deterministic/Structured Route -> Validation -> Output
                         -> Model Escalation -> Validation -> Output
```

KORA is not a claim that every task can be handled deterministically. It is a control layer for deciding which tasks should be handled deterministically and which tasks should escalate to inference.

The direct baseline path sends every request to the model:

```text
request -> model -> output
```

The KORA-controlled path routes through execution control before inference:

```text
request -> task graph -> deterministic route or model escalation -> validation -> telemetry
```

An avoided model-call event occurs when the baseline would count a model call for a request, but the KORA-controlled path handles the request through a deterministic or structured route without model escalation.

Current route classes include:

- deterministic route: known logic, templates, rules, or validations handle the request
- structured lookup: the request maps to a known structured handler or lookup placeholder
- policy route: explicit policy logic or policy tables handle the request
- `model_required` route: deterministic handling is not sufficient, so the request escalates

The main metrics are:

- `baseline_model_calls`: model-call events counted by the direct baseline path
- `kora_model_calls`: model-call events counted by the KORA-controlled path
- `avoided_model_calls`: `baseline_model_calls - kora_model_calls`
- `avoided_model_call_rate`: `avoided_model_calls / baseline_model_calls`
- `deterministic_routes`: requests handled through deterministic routing
- `model_escalations`: requests escalated to the model-call path
- `mismatch_count`: benchmark outputs that did not match expected results

These metrics separate two questions: whether KORA reduced model-call events, and whether validation outcomes remained expected for the workload under test.

## 4. Evaluation Methodology

This manuscript v0.3 uses two current public workloads.

The deterministic-heavy benchmark contains 100 tasks. The direct baseline counts one model call for each task. The KORA-controlled path routes deterministic work before inference and records model calls only for the remaining model-candidate routes. This benchmark is appropriate first evidence because it isolates the central hypothesis: deterministic-heavy workloads should not require a model call for every request.

The synthetic customer-support triage workload contains 12 synthetic requests across deterministic FAQ, deterministic policy, structured lookup, and model-required route classes. It is evaluated through local/no-network validation. This means it uses synthetic data, deterministic local validation paths, aggregate counters, and no external providers, API keys, private data, network calls, raw provider responses, or production traffic.

The workloads show different levels of evidence. The deterministic-heavy benchmark supports the current approved benchmark claim. The customer-support workload shows an application-shaped local/no-network validation path and demonstrates how KORA records avoided model-call events, deterministic routes, and model escalations. Neither workload proves production behavior, real provider behavior, real API-cost reduction, energy reduction, or broad workload superiority.

## 5. Results

### 5.1 Deterministic-heavy benchmark

| Metric | Value |
|---|---:|
| Total tasks | 100 |
| Baseline model calls | 100 |
| KORA-controlled model calls | 20 |
| Avoided model calls | 80 |
| Avoided model-call rate | 80% |
| Mismatches | 0 |

This result supports the current approved public claim:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

The interpretation is intentionally narrow. In this benchmark, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline while preserving expected benchmark outputs with zero mismatches. This is benchmark evidence for the documented deterministic-heavy workload. It is not production evidence, not real provider validation, and not a cost or energy claim.

### 5.2 Customer-support triage synthetic workload

| Metric | Value |
|---|---:|
| Total requests | 12 |
| Baseline model calls | 12 |
| KORA-controlled model calls | 4 |
| Avoided model calls | 8 |
| Avoided model-call rate | 66.67% |
| Deterministic routes | 8 |
| Model escalations | 4 |

This is local/no-network validation only and not real provider validation. The workload uses synthetic customer-support requests to exercise deterministic FAQ, policy, structured lookup, and model-required route classes. The current example shows that KORA can measure avoided model-call events in a synthetic application-shaped workload without API keys, external providers, private data, or network calls.

### 5.3 Latency direction

This manuscript does not include measured latency evidence yet. The expected direction is route-dependent:

- deterministic fast paths can reduce latency by avoiding inference
- structured lookup and policy routes can avoid model wait time when validation succeeds
- model escalation paths may add orchestration overhead before inference

Measured p50/p95 latency remains future work. Until those measurements exist, KORA should not be described as universally faster across all workloads.

## 6. Limitations

Current limitations include:

- synthetic workloads
- limited workload diversity
- no production traffic
- no real provider validation
- no real API-cost proof
- no production benchmark proof
- no full runtime-integrated real-provider benchmark evidence
- no energy measurement
- no user study
- no broad workload superiority claim
- preliminary reference integration only
- final citation style and BibTeX still pending

The deterministic-heavy benchmark and customer-support triage workload are useful early evidence, but they are not sufficient for production, cost, energy, or broad generalization claims. They show that KORA can reduce model-call events in documented deterministic-heavy and synthetic local/no-network validation contexts.

The related-work references integrated in this draft provide background and positioning. They do not prove KORA's claims, do not establish superiority over cited systems, and do not replace final bibliography review.

## 7. Reproducibility and Artifact Notes

KORA's current public evidence is organized around reproducible commands, local/no-network examples, aggregate counters, and claim-safe reports. This aligns with systems-paper artifact discipline but does not constitute formal artifact evaluation. ACM artifact review and badging guidance is cited only as a reference point for transparent artifact practices [R10].

Current reproduction expectations for this draft are:

- run the deterministic-heavy benchmark in offline mode
- run the customer-support triage local/no-network validation example
- inspect aggregate counters and claim-boundary text
- avoid committing generated raw reports unless explicitly selected for review
- keep raw provider responses, credentials, private data, and production traffic out of public artifacts

The paper still needs a final clean command transcript, final bibliography normalization, final figure/table review, and a final claim audit before submission.

## 8. Conclusion

Model-first execution is not always necessary. Many AI workloads include structured, deterministic, policy-driven, or validation-oriented tasks that can be routed before inference.

KORA introduces deterministic-first execution control: it represents requests as structured task paths, attempts deterministic handling before inference, validates route outcomes, records counters, and escalates to a model only when needed. Current evidence shows model invocation reduction in a reproducible deterministic-heavy benchmark and measurable avoided model-call events in a synthetic customer-support local/no-network validation workload.

KORA is complementary to model serving systems, workflow orchestrators, agent frameworks, RAG systems, and local runtimes. Future work should expand runtime validation, latency measurement, local model evaluation, real provider experiments, and visualization without weakening claim boundaries.

## References

This preliminary references section uses only verified entries from the first reference pass plus selected verified entries [R11], [R12], and [R13] from the second reference pass. Citation style and BibTeX are not final. See [KORA First Paper Citation Audit v0.1](kora-first-paper-citation-audit-v0-1.md) for citation consistency, traceability, and claim-boundary notes.

- [R01] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. "Efficient Memory Management for Large Language Model Serving with PagedAttention." SOSP 2023; arXiv:2309.06180. Source: https://arxiv.org/abs/2309.06180; https://doi.org/10.48550/arXiv.2309.06180
- [R02] Vijay Janapa Reddi et al. "MLPerf Inference Benchmark." arXiv:1911.02549, 2019; revised 2020. Source: https://arxiv.org/abs/1911.02549
- [R03] ONNX Runtime project. "ONNX Runtime" official documentation. Source owner: ONNX Runtime project / Microsoft. Date unavailable; accessed 2026-05-11. Source: https://onnxruntime.ai/docs/
- [R04] LangChain. "LangGraph Graph API overview." Official LangGraph documentation. Date unavailable; accessed 2026-05-11. Source: https://docs.langchain.com/oss/python/langgraph/graph-api
- [R05] Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, Keshav Santhanam, Sri Vardhamanan, Saiful Haq, Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, and Christopher Potts. "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines." arXiv:2310.03714, 2023. Source: https://arxiv.org/abs/2310.03714
- [R06] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Kuttler, Mike Lewis, Wen-tau Yih, Tim Rocktaschel, Sebastian Riedel, and Douwe Kiela. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS 2020; arXiv:2005.11401. Source: https://arxiv.org/abs/2005.11401; https://doi.org/10.48550/arXiv.2005.11401
- [R07] Apache Airflow project. "Dags." Apache Airflow 3.2.1 documentation. Source owner: Apache Software Foundation. Date unavailable; accessed 2026-05-11. Source: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html
- [R08] Johannes Koster and Sven Rahmann. "Snakemake-a scalable bioinformatics workflow engine." Bioinformatics 28(19), 2520-2522, 2012. Source: https://doi.org/10.1093/bioinformatics/bts480
- [R09] ggml-org. "llama.cpp: LLM inference in C/C++." Official GitHub repository. Date unavailable; accessed 2026-05-11. Source: https://github.com/ggml-org/llama.cpp
- [R10] Association for Computing Machinery. "Artifact Review and Badging - Current." Version 1.1, 2020. Source: https://www.acm.org/publications/policies/artifact-review-and-badging-current
- [R11] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. "ReAct: Synergizing Reasoning and Acting in Language Models." ICLR 2023; arXiv:2210.03629. Source: https://arxiv.org/abs/2210.03629; https://doi.org/10.48550/arXiv.2210.03629
- [R12] Timo Schick, Jane Dwivedi-Yu, Roberto Dessi, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. "Toolformer: Language Models Can Teach Themselves to Use Tools." arXiv:2302.04761, 2023. Source: https://arxiv.org/abs/2302.04761; https://doi.org/10.48550/arXiv.2302.04761
- [R13] Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, and Graham Neubig. "PAL: Program-aided Language Models." arXiv:2211.10435, 2022; revised 2023. Source: https://arxiv.org/abs/2211.10435; https://doi.org/10.48550/arXiv.2211.10435

## Claim Boundary Note

This manuscript draft is based on reproducible benchmark and local/no-network validation evidence. It does not claim production cost reduction, real API-cost reduction, energy reduction, production validation, broad workload superiority, formal artifact evaluation, or superiority over cited systems.
