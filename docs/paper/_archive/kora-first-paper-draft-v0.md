# KORA: Deterministic-First Execution Control for Reducing Model Invocations in AI Workloads

## Abstract

Model-first AI systems often turn each request directly into a prompt, even when the requested work is structured, deterministic, policy-driven, or validation-oriented. This default makes model invocation the first step rather than a conditional step, increasing latency exposure, resource use, and execution opacity for workloads that contain repeatable fast paths. KORA adds an execution-control layer before inference. Requests are represented as structured execution paths, deterministic-first routing handles work that can be resolved without inference, and model escalation is used only when a request cannot be safely handled through deterministic or structured logic. This draft evaluates the current KORA evidence through two public, reproducible paths: a deterministic-heavy benchmark and a synthetic customer-support local/no-network validation workload. In the deterministic-heavy benchmark, KORA reduced model invocations by 80%, from 100 baseline model calls to 20 KORA-controlled model calls, with zero mismatches. In the customer-support triage workload, local/no-network validation records 8 avoided model-call events across 12 synthetic requests, with 8 deterministic routes and 4 model escalations. These results show model invocation reduction and validation/reporting plumbing in documented workloads. They do not prove production cost reduction, real API-cost reduction, energy reduction, production validation, or broad workload superiority.

## 1. Introduction

LLM-first applications often treat every request as a prompt. A user request enters the system, a prompt is assembled, the model is called, and the result is returned or post-processed. This pattern is simple, but it makes inference the default even when the request could have been handled through structured execution.

Many AI tasks are deterministic, structured, policy-driven, cacheable, or validation-oriented. Examples include FAQ routing, policy lookup, structured validation, report formatting, retry decisions, and support triage. These tasks may benefit from explicit execution control before inference.

Model calls introduce latency, resource use, and opacity. They can be necessary for ambiguous, generative, or context-heavy work, but they are not always the right first operation. KORA proposes a different default:

Structure first. Inference second.

KORA turns AI requests into structured execution paths before inference. It routes deterministic and structured work first, validates outcomes, records telemetry, and escalates to a model only when needed.

## 2. Motivation

Default model-first execution is wasteful for deterministic-heavy workloads because every request pays the cost and latency exposure of a model path, even when the work is predictable.

Tasks that do not need model calls by default include:

- FAQ routing
- policy lookup
- structured validation
- report formatting
- budget guard
- retry decision
- support triage

These tasks often have explicit route classes, validation rules, or known response structures. A model may still be useful when the request is ambiguous, missing context, asks for an exception, or requires synthesis. The motivation for KORA is not to remove models, but to make model invocation conditional.

## 3. KORA Architecture

KORA sits between request intake and model invocation.

The current architecture can be described through six public components:

- request intake
- task graph
- deterministic/structured handlers
- validation/policy layer
- model escalation
- telemetry and counters
- report generation

Request intake turns an incoming task into an explicit execution path. The task graph describes the steps available to the request. Deterministic or structured handlers resolve work that can be handled without inference. The validation/policy layer checks whether the deterministic path is safe and expected. Model escalation handles work that cannot be safely resolved through deterministic logic. Telemetry and counters record what happened. Report generation turns aggregate local/no-network validation counters into reviewer-facing summaries.

## 4. Execution Model

The direct baseline path sends every request to the model:

```text
request -> model -> output
```

The KORA-controlled path routes the request through execution control first:

```text
request -> task graph -> deterministic route or model escalation -> validation -> telemetry
```

The current paper draft uses four route concepts:

- deterministic route: a request handled through known logic, templates, rules, or validation checks
- structured lookup: a request routed to a known structured handler or lookup placeholder
- policy route: a request handled through explicit policy rules or policy tables
- `model_required` route: a request escalated because deterministic handling is not sufficient

The KORA-controlled path should avoid model-call events for deterministic, structured lookup, and policy routes when validation succeeds. The `model_required` route still uses model escalation.

## 5. Evaluation Methodology

This draft uses two current public workloads.

The deterministic-heavy benchmark contains 100 tasks. The baseline counts one model call for each task. The KORA-controlled path routes deterministic work before inference and records KORA-controlled model calls for the remaining model-candidate routes.

The synthetic customer-support triage workload contains 12 synthetic requests across deterministic FAQ, deterministic policy, structured lookup, and model-required classes. It is evaluated through local/no-network validation, not real provider validation.

The core counters are:

- baseline model calls
- KORA-controlled model calls
- avoided model calls
- avoided model-call rate
- validation outcomes
- deterministic routes
- model escalations

The avoided model-call formula is:

```text
avoided_model_calls = baseline_model_calls - kora_model_calls
avoided_model_call_rate = avoided_model_calls / baseline_model_calls
```

The local/no-network validation boundary matters. These examples use synthetic data, deterministic local validation adapters, and aggregate counters. They do not use external providers, API keys, private data, network calls, raw provider responses, or production traffic.

## 6. Results

### Deterministic-heavy benchmark

| Metric | Value |
|---|---:|
| Total tasks | 100 |
| Baseline model calls | 100 |
| KORA-controlled model calls | 20 |
| Avoided model calls | 80 |
| Avoided model-call rate | 80% |
| Mismatches | 0 |

This deterministic-heavy benchmark provides the current approved public claim:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

The result should be interpreted as benchmark evidence for model invocation reduction in this documented workload. It is not production evidence.

### Customer-support triage synthetic workload

| Metric | Value |
|---|---:|
| Total requests | 12 |
| Baseline model calls | 12 |
| KORA-controlled model calls | 4 |
| Avoided model calls | 8 |
| Avoided model-call rate | 66.67% |
| Deterministic routes | 8 |
| Model escalations | 4 |

The customer-support triage result is synthetic local/no-network validation only. It shows that KORA can measure avoided model-call events, deterministic routes, and model escalations in an application-shaped workload without real provider calls.

## 7. Discussion

Model invocation reduction matters because model calls can dominate latency exposure, resource use, and operational complexity. When a request can be handled through deterministic execution, routing it through a model-first path adds avoidable work.

Deterministic paths can reduce latency for simple tasks because they do not wait on model inference. This draft treats that as an expected latency direction rather than a measured p50/p95 latency claim. Stronger latency claims require dedicated measurements.

KORA may add routing overhead when model escalation is still needed. For `model_required` routes, KORA performs classification, routing, or validation before escalating. That overhead may be worthwhile when it improves visibility and control, but it should be measured in future work.

Visibility into execution paths matters because it shows which requests were handled deterministically, which escalated to a model, which validations passed, and where fallback or errors occurred. KORA Studio may later visualize these counters and reports, but Studio planning is not implementation evidence and should not be presented as a shipped product result.

## 8. Limitations

Current limitations include:

- synthetic workloads
- not production traffic
- not real provider validation
- not real API-cost validation
- no energy measurements
- limited workload diversity
- no broad workload superiority claim
- no user study yet

The deterministic-heavy benchmark and customer-support triage workload are useful early evidence, but they do not establish universal behavior across all AI workloads.

## 9. Future Work

Future work should include:

- expanded customer-support workload
- RAG answer-routing workload
- agent budget guard workload
- local model runtime validation, for example Ollama
- p50/p95 latency measurement
- repeated runs
- real provider/API-cost technical report
- energy/sustainability paper
- KORA Studio as visualization layer

These steps should preserve the public/private boundary, use synthetic or sanitized data, and avoid upgrading claims until evidence exists.

## 10. Conclusion

Model-first execution is not always necessary. Many AI workloads contain structured, deterministic, policy-driven, or validation-oriented work that can be routed before inference.

KORA routes structured work before inference, validates execution paths, records counters, and escalates to a model only when needed. Current evidence shows model invocation reduction in a deterministic-heavy benchmark and measurable avoided model-call events in a synthetic customer-support local/no-network validation workload.

Future work will expand runtime validation, latency measurement, local model validation, and real provider experiments while preserving claim boundaries.

## Claim Boundary Note

This draft is based on reproducible benchmark and local/no-network validation evidence. It does not claim production cost reduction, real API-cost reduction, energy reduction, or production validation.
