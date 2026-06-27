# KORA First Paper Reviewer Questions

## Purpose

This document lists likely reviewer questions for the first KORA paper draft and draft claim-safe answers.

## Questions And Draft Answers

### 1. Is this just prompt routing?

No. The current KORA draft describes execution control before inference: task graphs, deterministic handlers, validation/policy checks, model escalation, telemetry, and report generation. Prompt routing may be one part of a model path, but KORA's focus is deciding whether a model path is needed at all.

### 2. How is KORA different from caching?

Caching reuses a previous result. KORA can route work through deterministic handlers, policy rules, structured lookups, validation checks, and model escalation boundaries. A deterministic route may be cacheable, but the KORA control layer is broader than cache reuse.

### 3. Are results real provider results?

No. The current paper draft uses a reproducible deterministic-heavy benchmark and local/no-network validation examples. The customer-support triage workload does not use real provider calls, API keys, private data, or network calls.

### 4. Does this prove cost reduction?

No. The current evidence measures model invocations or local/no-network model-call events. It does not prove production cost reduction or real API-cost reduction.

### 5. Does this prove energy reduction?

No. No energy measurement is included. Energy reduction should remain a future research question with a separate measurement methodology.

### 6. How are deterministic routes validated?

Current local/no-network examples validate deterministic routes through expected route metadata, deterministic handler checks, validation rules, and aggregate pass/fail counters. The validation is workload-specific and synthetic in the current evidence.

### 7. What happens when routing is wrong?

The current design expects validation failures, fallback counters, error counters, and model escalation boundaries to make routing outcomes visible. Stronger safety claims require additional tests and broader workload coverage.

### 8. What workloads benefit most?

Workloads with repeated deterministic, structured, policy-driven, cacheable, or validation-oriented requests are the likely best fit. The current evidence includes a deterministic-heavy benchmark and a synthetic customer-support triage workload.

### 9. What workloads do not benefit?

Workloads where most requests genuinely require open-ended model reasoning may benefit less. KORA may add routing overhead when a request still escalates to the model.

### 10. Is there latency overhead?

KORA can add routing and validation overhead, especially for requests that still require model escalation. Deterministic fast paths are expected to be faster than model-first paths, but p50/p95 latency measurements are still needed before stronger latency claims are made.

### 11. How reproducible are the results?

The current evidence is designed to be reproducible from public repository commands such as `python3 -m pytest`, `python3 -m kora examples list`, and the offline benchmark and validation examples. A clean command transcript is still a next evidence priority.

### 12. What is needed before production claims?

Production claims require production or production-like methodology, workload definitions, baselines, measured results, privacy review, and claim review. The current paper draft does not make production validation, production cost, real API-cost, or energy claims.

### 13. How does KORA handle ambiguous requests?

Ambiguous or policy-sensitive requests should escalate to a model-required path rather than being forced through a deterministic route. The customer-support triage synthetic workload includes model-required routes for ambiguous, unusual, sensitive, or incomplete requests.

### 14. Does KORA Studio prove the system works?

No. KORA Studio is currently planning documentation. It may later visualize execution paths, counters, and validation reports, but it is not current implementation evidence for the paper.
