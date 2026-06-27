# KORA First Paper Evidence Summary

## Evidence Overview

The first KORA paper should use the evidence that is already reproducible in the public repository: the deterministic-heavy benchmark, the customer-support triage synthetic local/no-network validation workload, and the validation/reporting infrastructure that records aggregate counters and claim boundaries.

The current evidence supports model invocation reduction claims in documented workloads. It does not support production cost, real API-cost, production validation, broad workload superiority, or energy claims.

## Deterministic-Heavy Benchmark

| Metric | Value |
|---|---:|
| Total tasks | 100 |
| Baseline model calls | 100 |
| KORA-controlled model calls | 20 |
| Avoided model calls | 80 |
| Avoided model-call rate | 80% |
| Mismatches | 0 |

Claim-safe interpretation:

KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload. This means the benchmark recorded 80 fewer model invocations in the KORA-controlled path than in the baseline path while preserving expected benchmark outputs with zero mismatches. It should not be interpreted as proof of production cost reduction, real API-cost reduction, production validation, broad workload superiority, or energy reduction.

## Customer-Support Triage Synthetic Workload

| Metric | Value |
|---|---:|
| Total requests | 12 |
| Baseline model calls | 12 |
| KORA-controlled model calls | 4 |
| Avoided model calls | 8 |
| Avoided model-call rate | 66.67% |
| Deterministic routes | 8 |
| Model escalations | 4 |

Claim-safe interpretation:

This is local/no-network validation only and not real provider validation. The workload uses synthetic customer-support requests to exercise deterministic FAQ, policy, structured lookup, and model-required route classes. The current example shows that KORA can measure avoided model-call events in a synthetic application-shaped workload without API keys, external providers, private data, or network calls.

## Validation Infrastructure

Current validation infrastructure includes:

- local/no-network validation examples
- Markdown report generation
- reviewer packet
- adapter selection skeleton
- blocked local runtime placeholder
- provider-neutral `ModelCallAdapter`
- deterministic local validation adapter
- explicit local runtime stub for deterministic in-process local/no-network validation
- fail-closed blocked adapter paths
- customer-support triage synthetic workload

## Reproduction Commands

```bash
python3 -m pytest
python3 -m kora examples list
python3 -m kora run runtime_integrated_benchmark -- --offline
python3 -m kora run customer_support_triage_fake_validation -- --offline
python3 -m kora run customer_support_triage_fake_validation -- --offline --report-md /tmp/kora_customer_support_validation.md
```

## Evidence Boundaries

The current evidence does not claim:

- production cost reduction proof
- real API-cost reduction proof
- production benchmark proof
- full runtime-integrated real-provider benchmark evidence
- broad workload superiority proof
- energy reduction evidence
- formal government validation
- signed partner validation unless actually signed and documented
- guaranteed adoption or funding
