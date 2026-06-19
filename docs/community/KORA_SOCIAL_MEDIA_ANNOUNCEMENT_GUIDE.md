# KORA Public Announcement Guide

Date: 2026-05-08

Current release: `v0.3.0-alpha`

Release URL: https://github.com/Krako-Labs/KORA/releases/tag/v0.3.0-alpha

## Purpose

This public guide provides short, claim-safe wording for announcing KORA in open-source channels.

It is not an internal campaign plan, posting calendar, or detailed operations library. Detailed operating material belongs outside the public KORA repository.

## Public-Safe Message Spine

Hook:

> Most AI apps call the model too soon.

Shift:

> KORA puts execution control before inference.

Mechanism:

- Task graphs.
- Deterministic-first execution.
- Validation before escalation.
- Telemetry around every path.
- Model calls only when needed.

Evidence:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

Next validation:

> KORA is expanding validation across real model-call paths, support triage, RAG routing, and agent budget-guard workloads.

CTA:

> Clone the repo. Run the alpha. Inspect the path. Bring a workload.

Tagline:

> Structure first. Inference second.

## Short Announcement

KORA `v0.3.0-alpha` is available as a GitHub prerelease.

Most AI apps call the model too soon. KORA changes the default: structure first, inference second.

KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

This is alpha benchmark evidence, not a universal production cost-reduction claim.

Release: https://github.com/Krako-Labs/KORA/releases/tag/v0.3.0-alpha

## Longer Announcement

Most AI apps call the model too soon.

Every request becomes a prompt. Every prompt becomes tokens. Every token becomes latency, cost, and infrastructure pressure.

KORA is an open-source execution-control layer for AI workloads. It turns a request into a task graph, runs deterministic work first, validates the path, records telemetry, and escalates to a model only when needed.

Current alpha evidence:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

This evidence is bounded to the current deterministic-heavy alpha benchmark. It should not be interpreted as production cost reduction proof, real API-cost reduction proof, production benchmark proof, broad workload superiority proof, or energy reduction evidence.

KORA is now expanding validation across real model-call runtime paths, customer-support triage, RAG answer routing, and agent budget-guard workloads.

Clone the repo. Run the alpha. Inspect the path. Bring a sanitized workload.

## Reproduction-Oriented Announcement

To inspect the current alpha path locally:

```bash
python3 -m kora --help
python3 -m kora examples list
python3 -m kora run direct_vs_kora -- --offline
python3 -m kora run runtime_integrated_benchmark -- --offline
```

Keep generated outputs local unless a maintainer asks for them. Do not share secrets, API keys, private user data, or proprietary datasets in public channels.

## Claim Boundaries

Do not say:

- KORA reduces production AI costs by 80%.
- KORA reduces real API costs by 80%.
- KORA reduces energy consumption by 80%.
- KORA is production-proven.
- KORA proves broad workload superiority.
- KORA has formal government or signed partner validation unless that validation is actually signed and documented.

## Visual References

Use the technical diagrams already committed under `docs/assets/`:

- `docs/assets/kora-execution-control-overview.svg`
- `docs/assets/kora-benchmark-evidence-card.svg`
- `docs/assets/kora-validation-roadmap.svg`
- `docs/assets/kora-help-test-flow.svg`
- `docs/assets/kora_workload_control_layer_architecture.svg`

Do not place image-generation prompts, private design prompts, or internal campaign art direction in the public KORA repository.
