# Goal 088 Cache Reuse Example

## Motivation

Goal 088 makes cache reuse a first-class KORA example. Earlier examples used cache reuse as a supporting route inside proxy, RAG, and agent workflows. This example isolates the concept so a new user can see repeated or reusable work routed to cache hits without provider calls.

This is a first-value OSS example. It is not a production cache correctness or production cost reduction claim.

## User-Facing Walkthrough

Run the example from a current source checkout:

```bash
python3 examples/cache_reuse/run.py
```

Expected high-level output:

```text
KORA Cache Reuse Example

Total requests: 7
First-time deterministic handled: 3
Cache hits: 2
Provider-needed: 2
Avoided simulated provider/model invocations: 5
Provider calls actually made: 0
```

Write structured outputs:

```bash
python3 examples/cache_reuse/run.py \
  --json-out /tmp/kora_goal088_cache_reuse.json \
  --report-md /tmp/kora_goal088_cache_reuse.md
```

Run through the KORA example runner:

```bash
python3 -m kora run cache_reuse
```

## Implementation Summary

- Added `examples/cache_reuse/`.
- Added request fixtures in `requests.json`.
- Added expected counters in `expected_counters.json`.
- Added `examples/cache_reuse/run.py`.
- Reused KORA `TaskGraph` execution with the deterministic `classify_by_rules` handler for first-time deterministic requests.
- Added tests in `tests/test_cache_reuse_example.py`.
- Added the `cache_reuse` entry to `python3 -m kora examples list`.
- Updated README/docs and continuation breadcrumbs.

The example uses KORA `TaskGraph` execution for every non-cache request. Cache hits reuse prior deterministic results inside the same offline example run. No external APIs are called.

## Route Examples

First-time deterministic request:

- input: `Classify ticket: customer was charged twice for order 4815`
- route: `deterministic`
- handler: `classify_by_rules`
- provider calls: `0`

Exact repeated request:

- input: repeated `Classify ticket: customer was charged twice for order 4815`
- route: `cache_hit`
- handler: `cache_reuse`
- provider calls: `0`

Semantically equivalent repeated request:

- input: `Please classify: duplicate charge on order 4815`
- route: `cache_hit`
- handler: `cache_reuse`
- provider calls: `0`

Provider-needed request:

- input: `Draft a warm retention email for this account`
- route: `provider_required`
- handler: `provider_needed_fallback`
- provider calls actually made: `0`

## Evidence Counters

Using `examples/cache_reuse/requests.json`:

- total requests: `7`
- first-time deterministic handled: `3`
- cache hits: `2`
- provider-needed: `2`
- avoided simulated provider/model invocations: `5`
- provider calls actually made: `0`

The counters are sample-fixture counters only.

## Validation Results

Final validation was run from the Goal 088 worktree:

```bash
python3 examples/cache_reuse/run.py
```

Result: passed. The command reported `Total requests: 7`, `First-time deterministic handled: 3`, `Cache hits: 2`, `Provider-needed: 2`, and `Provider calls actually made: 0`.

```bash
python3 examples/cache_reuse/run.py --json-out /tmp/kora_goal088_cache_reuse.json --report-md /tmp/kora_goal088_cache_reuse.md
```

Result: passed. The command wrote JSON and Markdown outputs and reported the same counters.

```bash
python3 -m kora examples list
```

Result: passed. The output includes `cache_reuse: offline cache reuse routing example`.

```bash
python3 -m pytest tests/test_cache_reuse_example.py tests/test_agent_workflow_optimization_example.py tests/test_rag_routing_example.py tests/test_openai_proxy_demo_cli.py tests/test_first_value_cli.py tests/test_executor.py
```

Result: passed with `46 passed in 15.78s`.

```bash
python3 scripts/check_markdown_links_goal082b.py
```

Result: passed with `Goal 082B markdown links OK`.

```bash
git diff --check
```

Result: passed with no output.

## Limitations

- The request fixture is small and synthetic.
- Semantic reuse is represented by an explicit fixture-owned `semantic_cache_key`.
- Cache reuse is local to one example run.
- Provider-needed means a real system would likely need provider/model handling; no provider/model call is made here.
- The example does not implement a production cache service, cache invalidation, distributed cache, or HTTP endpoint.

## Claim Boundaries

Supported narrow wording:

> In this offline cache-reuse example, KORA routes repeated sample requests to cache hits without making provider calls and marks ambiguous/open-ended requests as provider-needed.

Not claimed:

- production cache correctness.
- automatic cost reduction.
- real API-cost proof.
- benchmark superiority.
- broad workload superiority.
- production validation.

## Recommended Next Goal

Goal 089 should refresh the public reviewer walkthrough and example catalog now that cache reuse is a first-class example alongside deterministic classification, KORA Doctor, OpenAI-style proxy control, RAG routing, and agent workflow optimization.
