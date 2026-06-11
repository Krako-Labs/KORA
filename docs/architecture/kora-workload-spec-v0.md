# KORA Workload Spec v0

## Purpose

The KORA Workload Spec is a public-safe architecture draft for describing routable AI workloads.

It is not a production standard yet. It is a working format for examples, benchmark fixtures, route explanations, and evidence reports.

## Workload Fields

Suggested workload fields:

- `workload_id`: stable identifier.
- `name`: human-readable name.
- `description`: short workload description.
- `input_type`: prompt, document, event, batch, task graph, or other input class.
- `inputs`: public-safe sample inputs or input references.
- `expected_output`: output class or validation shape.
- `deterministic_steps`: steps that can run before model escalation.
- `validation`: checks that must pass before output is accepted.

## Target Fields

Suggested target fields:

- `target_id`: registry identifier.
- `target_type`: deterministic, cache, CPU, provider, GPU, or fallback.
- `capabilities`: supported execution features.
- `constraints`: known limits.
- `privacy_class`: public, local, private, or restricted.

## Policy Fields

Suggested policy fields:

- `max_latency_ms`.
- `max_estimated_cost`.
- `allow_provider_call`.
- `allow_gpu`.
- `require_deterministic_first`.
- `fallback_required`.
- `evidence_required`.

## Hints

Workloads may include routing hints:

- privacy sensitivity.
- cost sensitivity.
- latency sensitivity.
- quality threshold.
- reproducibility requirement.
- preferred target class.

Hints guide routing. They are not claims that a route is optimal.

## Public-Safe YAML Example

```yaml
workload_id: support_triage_demo_v0
name: Support triage demo
description: Classify a support request with deterministic checks before model escalation.
input_type: ticket
inputs:
  sample_ticket: "Customer asks whether a password reset email was sent."
expected_output:
  type: classification
  labels:
    - account_access
    - billing
    - technical_support
deterministic_steps:
  - normalize_text
  - match_known_intents
validation:
  required_fields:
    - label
    - confidence
policy:
  require_deterministic_first: true
  allow_provider_call: true
  allow_gpu: false
  fallback_required: true
  evidence_required: true
hints:
  privacy: local_safe_example
  cost_sensitivity: medium
  latency_sensitivity: medium
  quality_threshold: demo_only
```

## Boundary

The spec should not include secrets, private logs, private server details, raw GPU artifacts, or customer data.
