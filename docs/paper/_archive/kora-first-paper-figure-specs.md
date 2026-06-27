# KORA First Paper Figure Specifications

## Purpose

This document defines planned figures for the first KORA paper. It is a drafting aid for turning the manuscript v0.1 evidence and architecture into clear, claim-safe visuals.

## Figure 1 - Model-First vs KORA-Controlled Execution

### Goal

Show the central contrast between a model-first application path and the KORA-controlled path.

### Message

Model-first execution sends each request directly to inference. KORA inserts execution control before inference and routes deterministic or structured work before model escalation.

### Visual Layout

Model-first path:

```text
Request -> Prompt -> Model -> Output
```

KORA-controlled path:

```text
Request -> Task Graph -> Deterministic/Structured Route -> Validation -> Output
Request -> Task Graph -> Model Escalation -> Validation -> Output
```

### Labels

- Request
- Prompt
- Model
- Task Graph
- Deterministic/Structured Route
- Model Escalation
- Validation
- Output

### Data Source

Architecture and execution model described in the paper manuscript and existing paper outline.

### Claim Boundary

This figure explains architecture, not production evidence.

## Figure 2 - KORA Execution-Control Layer

### Goal

Show the components of the KORA execution-control layer.

### Message

KORA coordinates task graph routing, deterministic handlers, validation boundaries, model escalation, telemetry, and reporting.

### Visual Layout

Use a left-to-right flow or layered system diagram with the execution-control layer between request intake and model invocation.

### Labels

- Task graph
- Deterministic handlers
- Policy/validation layer
- Model escalation
- Telemetry/counters
- Report generation

### Data Source

Paper manuscript, local validation reviewer packet, and validation report design.

### Claim Boundary

This figure describes system structure only.

## Figure 3 - Deterministic-Heavy Benchmark Result

### Goal

Visualize the core benchmark result that supports the approved public claim.

### Message

In the deterministic-heavy benchmark, KORA-controlled execution records fewer model invocations than the direct baseline while preserving expected outputs.

### Visual Layout

Use a simple bar chart:

- `baseline_model_calls = 100`
- `kora_model_calls = 20`
- `avoided_model_calls = 80`

Add a small annotation:

- `mismatch_count = 0`

Do not convert model-call reduction into cost or energy units.

### Labels

- Baseline model calls
- KORA-controlled model calls
- Avoided model calls
- Mismatches

### Data Source

Deterministic-heavy benchmark result documented in the evidence summary.

### Claim Boundary

This figure supports the approved benchmark claim only.

## Figure 4 - Customer-Support Triage Synthetic Workload

### Goal

Show how the synthetic customer-support workload divides requests into deterministic routes and model escalations.

### Message

The local/no-network customer-support validation path measures route outcomes and avoided model-call events in a synthetic application-shaped workload.

### Visual Layout

Use a stacked bar, flow chart, or small route-class diagram showing:

- 12 total requests
- 8 deterministic routes
- 4 model escalations
- avoided model-call events: 8
- local/no-network label

### Labels

- Synthetic customer-support workload
- Deterministic routes
- Model escalations
- Avoided model-call events
- Local/no-network validation

### Data Source

Customer-support triage workload spec and local validation reviewer packet.

### Claim Boundary

Synthetic local/no-network validation only.

## Figure 5 - Route-Type Latency Direction

### Goal

Show expected latency direction by route type without claiming measured latency.

### Message

Deterministic routes are expected to avoid inference wait time, while model-required routes may add routing overhead before model escalation.

### Visual Layout

Use a small matrix or flow table:

- deterministic FAQ: likely faster by avoiding inference
- policy lookup: likely faster by avoiding inference
- structured lookup: likely faster by avoiding inference
- `model_required`: may add routing overhead before escalation

### Labels

- Route type
- Baseline behavior
- KORA behavior
- Expected latency direction
- Measured yet?

### Data Source

Paper manuscript latency-direction discussion and table specifications.

### Claim Boundary

This is expected direction, not measured latency yet.

## Figure Style Notes

- White background or dark technical style is acceptable.
- Avoid cost or energy icons unless those measurements are separately validated.
- Label synthetic/local/no-network evidence clearly.
- Use exact approved counters.
- Keep route diagrams readable in both paper PDF and README previews.
- Do not imply production validation or real provider validation.
