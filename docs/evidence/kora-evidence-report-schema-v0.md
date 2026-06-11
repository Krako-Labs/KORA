# KORA Evidence Report Schema v0

## Purpose

Every KORA execution should leave evidence.

Evidence does not mean overclaiming. It means recording enough structured information for a developer or reviewer to understand what ran, why a route was selected, what happened, and what can be reproduced.

## Core Fields

Suggested report fields:

- `run_id`: unique execution identifier.
- `workload_id`: workload spec identifier.
- `target_id`: selected target identifier.
- `selected_route`: deterministic, cache, CPU, provider, GPU, or fallback.
- `routing_decision`: structured reason for route selection.
- `latency_ms`: measured latency when safe to report.
- `throughput`: measured throughput when safe to report.
- `estimated_cost`: estimated cost only when methodology is public-safe.
- `privacy_class`: public, local, private, or restricted.
- `fallback`: whether fallback occurred and why.
- `reproducibility`: commands, fixture IDs, code version, and environment class.
- `limitations`: known constraints and non-claims.

## Example Shape

```json
{
  "run_id": "demo-run-001",
  "workload_id": "support_triage_demo_v0",
  "target_id": "cpu_local_demo",
  "selected_route": "deterministic",
  "routing_decision": {
    "reason": "Known intent matched before model escalation.",
    "policy": "deterministic_first"
  },
  "latency_ms": 12,
  "throughput": null,
  "estimated_cost": null,
  "privacy_class": "public_demo",
  "fallback": {
    "used": false,
    "reason": null
  },
  "reproducibility": {
    "fixture": "examples/workloads/support_triage_demo_v0.json",
    "command": "python3 -m kora route examples/requests/simple-deterministic.json",
    "code_version": "public checkout"
  },
  "limitations": [
    "Demo evidence only.",
    "Not a production cost reduction claim."
  ]
}
```

## Bounded Claim Language

Evidence reports may support bounded statements about a specific workload, fixture, command, or benchmark. They must not be used to claim production cost reduction, broad workload superiority, customer savings, infrastructure savings, or replacement of other systems.

## Raw/Private Artifact Boundary

Public evidence reports should not include:

- raw private logs.
- raw GPU artifacts.
- private server details.
- credentials.
- local-only private paths.
- customer data.

Raw artifacts can exist in private or local workflows, but public summaries must be sanitized and reproducible.
