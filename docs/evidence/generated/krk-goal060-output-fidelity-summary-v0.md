# KRK Output Fidelity Summary v0

Status: generated baseline-equivalence and output-fidelity evidence.

This summary compares deterministic public fixture baseline outputs with KRK-routed outputs using rule-based comparison only. It does not use provider calls, GPU execution, private logs, or a semantic model judge.

## Run Summary

- final classification: `BASELINE_EQUIVALENCE_OUTPUT_FIDELITY_MEASURED`
- claim level: `baseline_equivalence_output_fidelity_measured`
- execution mode: `local_deterministic_fixture_rule_based`
- total evaluated items: `18`
- baseline success count: `18`
- KRK success count: `18`
- exact match count: `17`
- structured equivalent count: `1`
- semantic equivalent count: `0`
- degraded count: `0`
- failed count: `0`
- exact match rate: `0.9444`
- acceptable output rate: `1.0000`
- degradation rate: `0.0000`
- failure rate: `0.0000`

## Workload Sources

| Profile | Matrix file | Items |
| --- | --- | ---: |
| `mixed-realistic` | `examples/workloads/krk-mixed-routing-matrix-alpha.json` | `6` |
| `GPU-heavy` | `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json` | `4` |
| `cache-heavy` | `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json` | `4` |
| `adversarial` | `examples/workloads/krk-adversarial-routing-matrix-alpha.json` | `4` |

## Per-Route Fidelity

| KRK route | Total | Exact | Structured equivalent | Semantic equivalent | Degraded | Failed | Acceptable output rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| deterministic | 2 | 2 | 0 | 0 | 0 | 0 | 1.0000 |
| cache | 3 | 3 | 0 | 0 | 0 | 0 | 1.0000 |
| CPU | 2 | 2 | 0 | 0 | 0 | 0 | 1.0000 |
| provider | 3 | 2 | 1 | 0 | 0 | 0 | 1.0000 |
| GPU | 4 | 4 | 0 | 0 | 0 | 0 | 1.0000 |
| fallback | 4 | 4 | 0 | 0 | 0 | 0 | 1.0000 |

## Baseline vs KRK Delta

- route changed count: `1`
- acceptable route changed count: `1`
- route changed degraded count: `0`
- baseline success minus KRK success: `0`

## Claim Boundary

Public fixture-derived baseline equivalence and output fidelity evidence only. This output uses deterministic rule-based comparison against committed public matrix fixtures. It does not claim production proof, production cost reduction, customer savings, energy reduction, broad workload superiority, real API/GPU cost reduction, semantic-model-judge validation, provider superiority, H100 superiority, or production readiness.
