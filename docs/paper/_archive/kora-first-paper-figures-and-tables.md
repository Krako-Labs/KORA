# KORA First Paper Figures and Tables

## Detailed Specifications

- [KORA first paper figure specifications](kora-first-paper-figure-specs.md)
- [KORA first paper table specifications](kora-first-paper-table-specs.md)

## Figure 1 - Model-First vs KORA-Controlled Execution

Describe the contrast between a model-first path and a KORA-controlled path.

Model-first path:

```text
request -> prompt -> model -> output
```

KORA-controlled path:

```text
request -> task graph -> deterministic route or model escalation -> validation -> telemetry
```

The figure should show that KORA inserts execution control before inference and records route decisions and counters.

## Figure 2 - KORA Execution-Control Architecture

Describe the main execution-control components:

- task graph
- deterministic handlers
- validation/policy
- model escalation
- telemetry/counters

The figure should emphasize the decision boundary between deterministic handling and model escalation.

## Figure 3 - Customer-Support Triage Routing

Describe the route classes in the synthetic customer-support triage workload:

- `deterministic_faq`
- `deterministic_policy`
- `structured_lookup`
- `model_required`

The figure should show deterministic FAQ, policy, and structured lookup requests bypassing model-call events, while `model_required` requests escalate.

## Table 1 - Deterministic-Heavy Benchmark Results

| Metric | Value |
|---|---:|
| Total tasks | 100 |
| Baseline model calls | 100 |
| KORA-controlled model calls | 20 |
| Avoided model calls | 80 |
| Avoided model-call rate | 80% |
| Mismatches | 0 |

## Table 2 - Customer-Support Triage Local Validation Results

| Metric | Value |
|---|---:|
| Total requests | 12 |
| Baseline model calls | 12 |
| KORA-controlled model calls | 4 |
| Avoided model calls | 8 |
| Avoided model-call rate | 66.67% |
| Deterministic routes | 8 |
| Model escalations | 4 |

## Table 3 - Claim Boundary Matrix

| Statement | Allowed? | Evidence needed | Current status |
|---|---|---|---|
| Model invocation reduction in benchmark | Yes | Reproducible deterministic-heavy benchmark counters | Supported: 80% reduction in current deterministic-heavy benchmark |
| Local/no-network validation | Yes | Local examples, synthetic workloads, aggregate counters | Supported for current local/no-network examples |
| Real provider validation | No, not yet | Runtime-integrated real provider commands, reviewed counters, sanitized report | Not available |
| Real API-cost reduction | No, not yet | Billing or explicitly configured cost methodology, baseline, reviewed report | Not available |
| Production cost reduction | No, not yet | Production methodology, traffic, baseline, measured results, review | Not available |
| Energy reduction | No, not yet | Energy measurement methodology and results | Not available |

## Table 4 - Route Type and Expected Latency Direction

| Route type | Baseline path | KORA path | Expected latency direction |
|---|---|---|---|
| Deterministic FAQ | Baseline model call | KORA fast path | Expected faster |
| Policy lookup | Baseline model call | KORA fast path | Expected faster |
| Structured lookup | Baseline model call | KORA handler | Expected faster |
| `model_required` | Baseline model call | KORA routing plus model escalation | KORA may add routing overhead |

These latency directions are hypotheses or expected directions until p50/p95 latency data is captured and reviewed.
