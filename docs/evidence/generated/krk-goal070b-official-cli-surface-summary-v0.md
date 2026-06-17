# KORA Five-Minute First Value Summary v0

Status: generated public-safe first-value workflow summary.

This summary records a local inspect, compare, run, and report workflow over committed public KRK fixtures. It requires no provider credentials, no GPU, and no network access.

## First-Value Metrics

- final classification: `FIVE_MINUTE_FIRST_VALUE_PATH_MEASURED`
- claim level: `five_minute_first_value_public_safe_demo`
- step count: `4`
- commands required: `1`
- required user decisions: `0`
- estimated time to first value: `approximately five minutes`
- works without provider credentials: `true`
- works without GPU: `true`
- network required: `false`

## Workflow Steps

| Step | Purpose | Status |
| --- | --- | --- |
| `inspect` | Inspect available KORA execution paths | `completed` |
| `compare` | Compare direct path with KRK-routed path | `completed` |
| `run` | Run public-safe KRK fixture workflow | `completed` |
| `report` | Generate route and output-fidelity summary | `completed` |

## Official CLI Commands

- `kora inspect`
- `kora compare`
- `kora run`
- `kora report`

## Route Summary

| Route | Count |
| --- | ---: |
| `deterministic` | `2` |
| `cache` | `3` |
| `CPU` | `2` |
| `provider` | `3` |
| `GPU` | `4` |
| `fallback` | `4` |

## Evidence Summary

- runtime total requests: `18`
- dry-run execution success rate: `1.0000`
- unsafe misroute rate: `0.0000`
- output exact match count: `17`
- output structured equivalent count: `1`
- output degraded count: `0`
- output failed count: `0`
- acceptable output rate: `1.0000`

## Claim Boundary

Five-minute first-value workflow evidence only. This output demonstrates a local inspect, compare, run, and report path over committed public fixtures. It does not claim production adoption, production readiness, production cost reduction, customer savings, provider superiority, H100 superiority, broad workload superiority, or real API/GPU cost reduction.
