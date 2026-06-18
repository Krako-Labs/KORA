# Goal 087 Agent Workflow Optimization Example

## Motivation

Goal 087 adds a concrete offline agent workflow optimization example to show KORA inside multi-step agent-style workflows. The example demonstrates workload control before provider/model reasoning or generation by separating deterministic steps, cache hits, local tool/action steps, and provider-needed fallback steps.

This is a first-value OSS example. It is not a production agent claim.

## User-Facing Walkthrough

Run the example from a current source checkout:

```bash
python3 examples/agent_workflow_optimization/run.py
```

Expected high-level output:

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

Write structured outputs:

```bash
python3 examples/agent_workflow_optimization/run.py \
  --json-out /tmp/kora_goal087_agent_workflow.json \
  --report-md /tmp/kora_goal087_agent_workflow.md
```

Run through the KORA example runner:

```bash
python3 -m kora run agent_workflow_optimization
```

## Implementation Summary

- Added `examples/agent_workflow_optimization/`.
- Added workflow fixtures in `workflows.json`.
- Added expected counters in `expected_counters.json`.
- Added `examples/agent_workflow_optimization/run.py`.
- Added the deterministic `agent_route_step` executor handler.
- Added tests in `tests/test_agent_workflow_optimization_example.py`.
- Added the `agent_workflow_optimization` entry to `python3 -m kora examples list`.
- Updated README/docs and continuation breadcrumbs.

The example uses KORA `TaskGraph` execution for every non-cache workflow step. Cache hits reuse prior deterministic results inside the same offline example run. No external APIs are called.

## Workflow Examples

Support ticket resolution:

- deterministic classification step.
- cache hit for the repeated classification step.
- tool-needed account lookup step.
- provider-needed resolution-planning step.

Documentation update:

- deterministic required-field validation step.
- deterministic static transform step.
- tool-needed local document-index update step.
- provider-needed release-note writing step.

Incident response:

- deterministic policy-check step.
- cache hit for the repeated policy-check step.
- tool-needed local incident-log query step.
- provider-needed root-cause reasoning step.

## Evidence Counters

Using `examples/agent_workflow_optimization/workflows.json`:

- total workflow steps: `12`
- deterministic steps: `4`
- cache hits: `2`
- tool-needed steps: `3`
- provider-needed steps: `3`
- avoided simulated provider/model invocations: `6`
- provider calls actually made: `0`

The counters are sample-fixture counters only.

## Validation Results

Final validation was run from the Goal 087 worktree:

```bash
python3 examples/agent_workflow_optimization/run.py
```

Result: passed. The command reported `Total workflow steps: 12`, `Deterministic steps: 4`, `Cache hits: 2`, `Tool-needed steps: 3`, `Provider-needed steps: 3`, and `Provider calls actually made: 0`.

```bash
python3 examples/agent_workflow_optimization/run.py --json-out /tmp/kora_goal087_agent_workflow.json --report-md /tmp/kora_goal087_agent_workflow.md
```

Result: passed. The command wrote JSON and Markdown outputs and reported the same counters.

```bash
python3 -m kora examples list
```

Result: passed. The output includes `agent_workflow_optimization: offline agent workflow control example`.

```bash
python3 -m pytest tests/test_agent_workflow_optimization_example.py tests/test_rag_routing_example.py tests/test_openai_proxy_demo_cli.py tests/test_first_value_cli.py tests/test_executor.py
```

Result: passed with `41 passed in 12.71s`.

```bash
python3 scripts/check_markdown_links_goal082b.py
```

Result: passed with `Goal 082B markdown links OK`.

```bash
git diff --check
```

Result: passed with no output.

## Limitations

- The workflows are small synthetic fixtures.
- Tool-needed means a local action/tool step is identified; no external tool or API is invoked.
- Provider-needed means a real system would likely need provider/model reasoning or generation; no provider/model call is made here.
- Cache reuse is local to one example run.
- The example does not implement production agent orchestration, autonomous execution, or an HTTP service.

## Claim Boundaries

Supported narrow wording:

> In this offline agent-workflow example, KORA routes sample workflow steps across deterministic, cache, tool-needed, and provider-needed paths without making provider calls.

Not claimed:

- production agent readiness.
- autonomous agent reliability.
- automatic cost reduction.
- real API-cost proof.
- benchmark superiority.
- broad workload superiority.
- production validation.

## Recommended Next Goal

Goal 088 should refresh the public reviewer walkthrough and example catalog now that KORA has first-class examples for deterministic classification, KORA Doctor, OpenAI-style proxy control, RAG routing, and agent workflow optimization.
