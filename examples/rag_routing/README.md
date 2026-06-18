# RAG Routing Example

This offline example shows KORA controlling a retrieval-style workflow. It routes exact FAQ/policy queries to deterministic answers, repeated queries to a local cache path, document-grounded queries to retrieval-needed handling over a small corpus, and ambiguous or open-ended generation queries to provider-needed fallback.

It does not call external APIs and does not require provider credentials.

Current availability: run this example from a current `Krako-Labs/KORA` checkout installed from source. Plain `python3 -m pip install kora` installs a different PyPI project and should not be used for these examples. Future package distribution is planned as `getkora`, but this README does not claim that package is published.

## Quick Run

```bash
python3 examples/rag_routing/run.py
```

Write structured JSON and a report:

```bash
python3 examples/rag_routing/run.py \
  --json-out /tmp/kora_goal086_rag_routing.json \
  --report-md /tmp/kora_goal086_rag_routing.md
```

Run through the KORA example runner:

```bash
python3 -m kora run rag_routing
```

## Expected Output

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

## Expected Counters

- total queries: `7`
- deterministic answered: `2`
- cache hits: `1`
- retrieval-needed: `2`
- provider-needed: `2`
- avoided simulated provider/model invocations: `3`
- provider calls actually made: `0`

Expected counters are in [expected_counters.json](expected_counters.json). Query fixtures are in [queries.json](queries.json). The offline corpus fixture is in [corpus.json](corpus.json).

## Claim Boundary

In this offline RAG-routing example, KORA routes sample queries across deterministic, cache, retrieval-needed, and provider-needed paths without making provider calls.

This example does not claim production RAG readiness, retrieval accuracy, automatic cost reduction, real API-cost proof, benchmark superiority, or broad workload superiority.
