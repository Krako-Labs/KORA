# KORA First Paper Outline

## Working Title Options

Recommended primary title:

KORA: Deterministic-First Execution Control for Reducing Model Invocations in AI Workloads

Other options:

- Structure First, Inference Second: Execution-Control Routing for AI Workloads
- Reducing Unnecessary Model Calls with Deterministic-First AI Execution
- KORA: An Execution-Control Layer for Model-Efficient AI Workloads
- Fast Paths Before Inference: Model Invocation Reduction in AI Systems

## Thesis

Most AI applications call a model too early. KORA introduces an execution-control layer that routes deterministic and structured work before inference and escalates to a model only when needed.

## Abstract Draft

Many model-first AI systems convert each request directly into a prompt, even when part of the workload can be handled through structured rules, validation, or deterministic routing. KORA introduces deterministic-first execution control: requests are represented as controlled execution paths, deterministic work is routed before inference, and model escalation is reserved for cases that need it. This paper compares a baseline path against a KORA-controlled path using a reproducible deterministic-heavy benchmark and a synthetic customer-support local/no-network validation workload. In the deterministic-heavy benchmark, KORA reduced model invocations by 80% while preserving expected benchmark outcomes with zero mismatches. The customer-support workload shows how local/no-network validation can measure avoided model-call events, deterministic routes, and model escalations in an application-shaped synthetic workload. These results are evidence of model invocation reduction and validation plumbing in documented workloads; they are not production cost reduction proof or real API-cost proof.

## Contributions

- Execution-control architecture for routing AI requests before inference.
- Deterministic-first routing model for structured or policy-bound work.
- Model escalation boundary for requests that cannot be safely handled deterministically.
- Telemetry and counter reporting for baseline model calls, KORA-controlled model calls, avoided model calls, validation outcomes, and route classes.
- Reproducible deterministic-heavy benchmark evidence showing an 80% model invocation reduction.
- Synthetic application-shaped validation workload for customer-support triage using local/no-network execution.

## Paper Structure

1. Introduction
2. Motivation
3. KORA Architecture
4. Execution Model
5. Evaluation Methodology
6. Results
7. Discussion
8. Limitations
9. Future Work
10. Conclusion

## Key Claims

- KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.
- KORA's local no-network validation examples show that KORA can measure avoided model-call events in synthetic workloads.
- In the customer-support triage synthetic workload, the local validation path records 8 avoided model-call events out of 12 requests.
- KORA provides a provider-neutral model-call adapter boundary for measuring model-call events in validation harnesses.
- KORA separates deterministic routes from model escalations in the current local/no-network validation examples.

## Limitations

- Current evidence uses synthetic workloads.
- Current evidence does not use production traffic.
- Current evidence does not prove real API-cost reduction.
- Current evidence does not include energy measurement.
- Local/no-network validation is not real provider validation.
- The customer-support triage evidence is application-shaped but not a production benchmark.
- Latency direction for deterministic fast paths is expected from avoiding model calls, but p50/p95 latency evidence should be captured before stronger latency claims are made.
