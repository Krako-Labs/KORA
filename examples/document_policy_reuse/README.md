# Compare document policy reuse paths

Compare exact node reuse with a whole-request cache and an equivalent manual node cache using a synthetic, read-only document-access workflow. This example executes the existing KORA economics runner without a model, provider, or network.

## Run

From the repository root, after installing KORA and its development dependencies:

```bash
python -m examples.document_policy_reuse.run
python -m pytest -q tests/test_document_policy_reuse_example.py
```

The report includes actual fixture adapter dispatches, reuse hits, output checks, and local p50/p95 latency for each path. It prints JSON to standard output.

## Compare the paths

| Path | Meaning |
| --- | --- |
| No reuse | Run all nodes on each request using the KORA runner. |
| Whole-request cache | Cache the final answer only for an identical full request and adapter version. |
| Manual node cache | Use an independent dictionary and the same input projection and cache scope. |
| KORA node cache | Use the runner's exact node reuse. |

The fixture classifies a fabricated document, determines the permitted read mode, and returns a notice code. It does not read or expose document content.

## Validation boundaries

The eleven phases exercise policy change, permission revocation and renewal, expiry, rollback, data changes, adapter version and principal/tenant separation. Each phase includes an exact repeat. Every answer is checked against an authored expected action; the first request in every phase must execute all nodes. The runner's dispatch count is checked against an independent adapter counter. Deterministic adapters explicitly report zero model calls.

These are author-defined regression cases, not independent human labels. The fixture supplies complete trusted context; an integration must obtain and validate that context from an authoritative source. Reuse is not an authorization service. No external agent or real model is compared. Local timings are host-dependent; fewer dispatches do not establish lower cost, and the manual cache can match KORA's call count.
