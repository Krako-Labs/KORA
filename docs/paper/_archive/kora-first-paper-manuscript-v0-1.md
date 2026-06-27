# KORA: Deterministic-First Execution Control for Reducing Model Invocations in AI Workloads

## Abstract

Model-first AI systems often call models too early: every request becomes a prompt even when the work is structured, deterministic, policy-driven, or validation-oriented. This default makes inference the first operation rather than a conditional operation, increasing latency exposure and reducing visibility into what parts of a workload actually require model reasoning. KORA introduces deterministic-first execution control, an execution-control layer placed before inference. Requests are represented as structured task paths, deterministic and structured routes are attempted first, validation checks confirm expected outcomes, and model escalation is used only when a request cannot be handled safely without inference. This manuscript draft evaluates KORA through the current public evidence: a reproducible deterministic-heavy benchmark and a synthetic customer-support local/no-network validation workload. In the deterministic-heavy benchmark, KORA reduced model invocations by 80%, from 100 baseline model calls to 20 KORA-controlled model calls, with zero mismatches. In the customer-support workload, local/no-network validation records 8 avoided model-call events across 12 synthetic requests, with 8 deterministic routes and 4 model escalations. These results support model invocation reduction and validation/reporting visibility in documented workloads. They are not production cost proof, real API-cost proof, energy evidence, production validation, or broad workload superiority evidence.

## 1. Introduction

Many AI systems treat every request as a model invocation. A request enters the application, the application builds a prompt, the model produces a response, and downstream logic validates or formats the result. This model-first pattern is easy to adopt, but it makes inference the default execution path even when the requested work does not require open-ended model reasoning.

This default is unnecessary for many deterministic, structured, validation, policy, and routing tasks. Password reset instructions, policy lookups, report formatting, schema validation, routing decisions, and budget checks often have known rules or expected output properties. A model may still be needed for ambiguous, context-heavy, generative, or policy-sensitive cases, but those cases should be explicit escalations rather than the default for the entire workload.

KORA inserts an execution-control layer before inference. Instead of treating the model as the first stop, KORA represents requests as task paths, attempts deterministic or structured handling when appropriate, validates the route outcome, records counters, and escalates only when deterministic handling is insufficient.

Structure first. Inference second.

This paper draft makes four contributions:

- It defines KORA's deterministic-first execution-control model for routing AI work before inference.
- It describes route classes, validation boundaries, model escalation, and telemetry counters for comparing model-first and KORA-controlled execution.
- It reports the current reproducible deterministic-heavy benchmark result: an 80% model invocation reduction with zero mismatches in the documented workload.
- It summarizes a synthetic customer-support local/no-network validation workload that measures avoided model-call events, deterministic routes, and model escalations without external providers, API keys, private data, or network calls.

## 2. Motivation

Model-first systems waste model calls when a workload contains repeated or structured work. In a deterministic-heavy workload, sending every request to a model means that simple routing, lookup, formatting, and validation tasks pay inference latency and model-call overhead even when the expected behavior is already known.

KORA is motivated by workloads where many requests fall into deterministic or structured classes:

- FAQ and help-center routing
- policy lookup
- structured validation
- report formatting
- budget guard checks
- retry decisions
- support triage

These tasks do not eliminate the need for models. They make the need for models conditional. When a request has a known route, a deterministic handler, and a validation rule, KORA can avoid a model-call event. When a request is ambiguous, missing context, policy-sensitive, or generative, KORA can escalate to a model-required path.

The latency direction follows from this distinction. Deterministic routes can avoid inference latency because they do not wait for a model response. Model-required routes may include routing or validation overhead before escalation. This manuscript therefore discusses latency direction but does not claim a measured universal speedup. p50/p95 latency measurement remains future evidence.

## 3. System Overview

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

## 4. Execution Model

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

## 5. Evaluation Methodology

This manuscript v0.1 uses two current public workloads.

The deterministic-heavy benchmark contains 100 tasks. The direct baseline counts one model call for each task. The KORA-controlled path routes deterministic work before inference and records model calls only for the remaining model-candidate routes. This benchmark is appropriate first evidence because it isolates the central hypothesis: deterministic-heavy workloads should not require a model call for every request.

The synthetic customer-support triage workload contains 12 synthetic requests across deterministic FAQ, deterministic policy, structured lookup, and model-required route classes. It is evaluated through local/no-network validation. This means it uses synthetic data, deterministic local validation paths, aggregate counters, and no external providers, API keys, private data, network calls, raw provider responses, or production traffic.

The workloads show different levels of evidence. The deterministic-heavy benchmark supports the current approved benchmark claim. The customer-support workload shows an application-shaped local/no-network validation path and demonstrates how KORA records avoided model-call events, deterministic routes, and model escalations. Neither workload proves production behavior, real provider behavior, real API-cost reduction, energy reduction, or broad workload superiority.

## 6. Results

### 6.1 Deterministic-heavy benchmark

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

The interpretation is intentionally narrow. In this benchmark, KORA recorded 80 fewer model invocations than the direct baseline while preserving expected benchmark outputs with zero mismatches. This is benchmark evidence for the documented deterministic-heavy workload. It is not production evidence, not real provider validation, and not a cost or energy claim.

### 6.2 Customer-support triage synthetic workload

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

### 6.3 Latency direction

This manuscript does not include measured latency evidence yet. The expected direction is route-dependent:

- deterministic fast paths can reduce latency by avoiding inference
- structured lookup and policy routes can avoid model wait time when validation succeeds
- model escalation paths may add orchestration overhead before inference

Measured p50/p95 latency remains future work. Until those measurements exist, KORA should not be described as universally faster across all workloads.

## 7. Discussion

Reducing model invocations matters because model calls are not just a cost center. They can dominate latency exposure, add operational uncertainty, and make application behavior harder to inspect. When a request can be handled deterministically, a model-first path adds avoidable execution work and makes the system less explicit.

KORA improves execution visibility by recording how requests move through the control layer. Counters make it possible to distinguish deterministic routes, model escalations, avoided model-call events, validation passes, validation failures, fallbacks, and errors. This visibility is useful even before stronger real-provider or production claims are available.

Deterministic validation is also a safety boundary. A route should avoid a model only when a deterministic handler and validation rule can produce an expected outcome. Ambiguous or policy-sensitive requests should escalate instead of being forced through a deterministic path. This is why KORA should be understood as execution control rather than blanket model avoidance.

KORA also differs from simple caching and prompt routing. Caching reuses a previous result. Prompt routing selects a model or prompt path. KORA decides whether inference is needed at all for a request, using task structure, deterministic handlers, policy and validation checks, escalation boundaries, and telemetry.

The current evidence is strongest for deterministic-heavy workloads. Workloads dominated by genuinely open-ended model reasoning may benefit less, and KORA may add routing overhead when most requests still escalate. Future evaluation should therefore report workload composition, route classes, model escalation rates, validation outcomes, and latency measurements together.

KORA Studio is relevant as future visualization and developer workflow context. It may later display counters, route decisions, validation reports, and workload summaries. It is not evidence in this paper and should not be presented as an implemented product result.

## 8. Limitations

Current limitations include:

- synthetic workloads
- limited workload diversity
- no production traffic
- no real provider validation
- no real API-cost proof
- no energy measurement
- no user study
- no broad workload superiority claim

The deterministic-heavy benchmark and customer-support triage workload are useful early evidence, but they are not sufficient for production, cost, energy, or broad generalization claims. They show that KORA can reduce model-call events in documented deterministic-heavy and synthetic local/no-network validation contexts.

## 9. Future Work

Future work should expand both evidence and presentation:

- expanded 100-request customer-support workload
- RAG answer-routing workload
- agent budget-guard workload
- local model runtime validation, for example Ollama
- p50/p95 latency measurement
- repeated runs
- real provider/API-cost technical report
- energy/sustainability paper
- KORA Studio visualization and developer workflow

Each future step should preserve synthetic or sanitized data boundaries, avoid committing raw provider responses, and keep claim language tied to the evidence actually collected.

## 10. Conclusion

Model-first execution is not always necessary. Many AI workloads include structured, deterministic, policy-driven, or validation-oriented tasks that can be routed before inference.

KORA introduces deterministic-first execution control: it represents requests as structured task paths, attempts deterministic handling before inference, validates route outcomes, records counters, and escalates to a model only when needed. Current evidence shows model invocation reduction in a reproducible deterministic-heavy benchmark and measurable avoided model-call events in a synthetic customer-support local/no-network validation workload.

Future work should expand runtime validation, latency measurement, local model evaluation, real provider experiments, and visualization without weakening claim boundaries.

## Claim Boundary Note

This manuscript draft is based on reproducible benchmark and local/no-network validation evidence. It does not claim production cost reduction, real API-cost reduction, energy reduction, production validation, or broad workload superiority.
