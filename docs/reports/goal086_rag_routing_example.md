# Goal 086 RAG Routing Example

## Motivation

Goal 086 adds a concrete offline RAG routing example to show KORA inside a retrieval-style workflow. The example demonstrates workload control before provider/model generation by separating exact deterministic answers, cache hits, retrieval-needed cases, and provider-needed fallback cases.

This is a first-value OSS example. It is not a production RAG claim.

## User-Facing Walkthrough

Run the example from a current source checkout:

```bash
python3 examples/rag_routing/run.py
```

Expected high-level output:

```text
KORA RAG Routing Example

Total queries: 7
Deterministic answered: 2
Cache hits: 1
Retrieval-needed: 2
Provider-needed: 2
Avoided simulated provider/model invocations: 3
Provider calls actually made: 0
```

Write structured outputs:

```bash
python3 examples/rag_routing/run.py \
  --json-out /tmp/kora_goal086_rag_routing.json \
  --report-md /tmp/kora_goal086_rag_routing.md
```

Run through the KORA example runner:

```bash
python3 -m kora run rag_routing
```

## Implementation Summary

- Added `examples/rag_routing/`.
- Added a small offline corpus fixture in `corpus.json`.
- Added query fixtures and route expectations in `queries.json`.
- Added expected counters in `expected_counters.json`.
- Added `examples/rag_routing/run.py`.
- Added the deterministic `rag_route_query` executor handler.
- Added tests in `tests/test_rag_routing_example.py`.
- Added the `rag_routing` entry to `python3 -m kora examples list`.
- Updated README/docs and continuation breadcrumbs.

The example uses KORA `TaskGraph` execution for every non-cache query. Cache hits reuse a prior routed result inside the same offline example run. No external APIs are called.

## Route Examples

Deterministic answer:

- query: `What is the refund window?`
- route: `deterministic_answer`
- handler: `exact_faq_answer`
- provider calls: `0`

Cache hit:

- query: repeated `What is the refund window?`
- route: `cache_hit`
- handler: `cache_reuse`
- provider calls: `0`

Retrieval-needed:

- query: `How long are audit logs retained?`
- route: `retrieval_needed`
- handler: `retrieve_from_corpus`
- retrieved document: `doc-security-retention`
- provider calls: `0`

Provider-needed:

- query: `Write a persuasive apology email about a delayed renewal.`
- route: `provider_needed`
- handler: `provider_needed_fallback`
- provider calls actually made: `0`

## Evidence Counters

Using `examples/rag_routing/queries.json` and `examples/rag_routing/corpus.json`:

- total queries: `7`
- deterministic answered: `2`
- cache hits: `1`
- retrieval-needed: `2`
- provider-needed: `2`
- avoided simulated provider/model invocations: `3`
- provider calls actually made: `0`

The counters are sample-fixture counters only.

## Validation Results

Final validation was run from the Goal 086 worktree:

```bash
python3 examples/rag_routing/run.py
```

Result: passed. The command reported `Total queries: 7`, `Deterministic answered: 2`, `Cache hits: 1`, `Retrieval-needed: 2`, `Provider-needed: 2`, and `Provider calls actually made: 0`.

```bash
python3 examples/rag_routing/run.py --json-out /tmp/kora_goal086_rag_routing.json --report-md /tmp/kora_goal086_rag_routing.md
```

Result: passed. The command wrote JSON and Markdown outputs and reported the same counters.

```bash
python3 -m kora examples list
```

Result: passed. The output includes `rag_routing: offline RAG routing control example`.

```bash
python3 -m pytest tests/test_rag_routing_example.py tests/test_openai_proxy_demo_cli.py tests/test_first_value_cli.py tests/test_executor.py
```

Result: passed with `36 passed in 11.33s`.

```bash
python3 scripts/check_markdown_links_goal082b.py
```

Result: passed with `Goal 082B markdown links OK`.

```bash
git diff --check
```

Result: passed with no output.

## Limitations

- The corpus is small and synthetic.
- Retrieval-needed means the example found a document-grounded route; it does not claim retrieval accuracy.
- Provider-needed means a real system would likely need provider/model handling; no provider/model call is made here.
- Cache reuse is local to one example run.
- The example does not implement a production RAG service, vector database, embedding model, or HTTP endpoint.

## Claim Boundaries

Supported narrow wording:

> In this offline RAG-routing example, KORA routes sample queries across deterministic, cache, retrieval-needed, and provider-needed paths without making provider calls.

Not claimed:

- production RAG readiness.
- retrieval accuracy.
- automatic cost reduction.
- real API-cost proof.
- benchmark superiority.
- broad workload superiority.
- production validation.

## Recommended Next Goal

Goal 087 should refresh the public reviewer walkthrough and example catalog now that KORA has first-class examples for deterministic classification, KORA Doctor, OpenAI-style proxy control, and RAG routing.
