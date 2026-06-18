# Agent Workflow Optimization Example

This offline example shows KORA controlling a multi-step agent-style workflow. It routes classification, validation, static transform, and policy-check steps to deterministic handlers; repeated deterministic steps to cache reuse; explicit local action steps to tool-needed handling; and ambiguous planning or open-ended generation steps to provider-needed fallback.

It does not call external APIs and does not require provider credentials.

Current availability: run this example from a current `Krako-Labs/KORA` checkout installed from source. Plain `python3 -m pip install kora` installs a different PyPI project and should not be used for these examples. Future package distribution is planned as `getkora`, but this README does not claim that package is published.

## Quick Run

```bash
python3 examples/agent_workflow_optimization/run.py
```

Write structured JSON and a report:

```bash
python3 examples/agent_workflow_optimization/run.py \
  --json-out /tmp/kora_goal087_agent_workflow.json \
  --report-md /tmp/kora_goal087_agent_workflow.md
```

Run through the KORA example runner:

```bash
python3 -m kora run agent_workflow_optimization
```

## Expected Output

```text
KORA Agent Workflow Optimization Example

Total workflow steps: 12
Deterministic steps: 4
Cache hits: 2
Tool-needed steps: 3
Provider-needed steps: 3
Avoided simulated provider/model invocations: 6
Provider calls actually made: 0
```

## Expected Counters

- total workflow steps: `12`
- deterministic steps: `4`
- cache hits: `2`
- tool-needed steps: `3`
- provider-needed steps: `3`
- avoided simulated provider/model invocations: `6`
- provider calls actually made: `0`

Expected counters are in [expected_counters.json](expected_counters.json). Workflow fixtures are in [workflows.json](workflows.json).

## Claim Boundary

In this offline agent-workflow example, KORA routes sample workflow steps across deterministic, cache, tool-needed, and provider-needed paths without making provider calls.

This example does not claim production agent readiness, autonomous agent reliability, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.
