# KORA First Paper Table Specifications

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

| Statement | Current status | Evidence available | Evidence still needed |
|---|---|---|---|
| Deterministic-heavy model invocation reduction | Supported for current benchmark | Reproducible 100-task deterministic-heavy benchmark | Repeated runs and final paper command transcript |
| Synthetic local/no-network validation | Supported for current examples | Local/no-network examples with aggregate counters | Expanded workloads and clean reproduction transcript |
| Real provider validation | Not supported yet | None in current public evidence | Runtime-integrated real provider commands, reviewed counters, sanitized report |
| Real API-cost reduction | Not supported yet | None in current public evidence | Explicit cost methodology, measured or configured pricing, reviewed report |
| Production cost reduction | Not supported yet | None in current public evidence | Production methodology, traffic, baseline, measured results, review |
| Energy reduction | Not supported yet | None in current public evidence | Energy measurement methodology and results |
| Broad workload superiority | Not supported yet | Deterministic-heavy and synthetic customer-support evidence only | Broader workload suite and comparative methodology |

## Table 4 - Route Type and Expected Latency Direction

| Route type | Baseline behavior | KORA behavior | Expected latency direction | Measured yet? |
|---|---|---|---|---|
| Deterministic FAQ | Baseline model call | KORA deterministic fast path | Expected faster by avoiding inference | No |
| Policy lookup | Baseline model call | KORA policy fast path | Expected faster by avoiding inference | No |
| Structured lookup | Baseline model call | KORA structured handler | Expected faster by avoiding inference | No |
| `model_required` | Baseline model call | KORA routing plus model escalation | May add routing overhead before escalation | No |

## Table 5 - Future Evidence Roadmap

| Evidence item | Purpose | Status |
|---|---|---|
| Expanded 100-request customer-support workload | Broaden application-shaped local/no-network validation | Needed |
| Ollama/local model validation | Measure local runtime model-call events | Needed |
| p50/p95 latency | Support measured latency claims or boundaries | Needed |
| Repeated runs | Improve reproducibility confidence | Needed |
| Real provider/API-cost technical report | Separate future provider/cost evidence from first paper | Future work |
| Energy/sustainability paper | Separate future energy methodology and evidence | Future work |
