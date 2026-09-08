# Specul.AI Editorial v1 workload template

This is a bounded KORA integration template for an independently developed editorial service. It freezes only the upstream revision and semantic node contract. The Specul.AI repository, production database, article text, provider credentials, raw model responses and browser state are not vendored here.

Baseline comparison must retain the upstream service's existing deterministic control plane. KORA economics may count only incremental routing, local execution, exact reuse and context/call differences introduced by KORA. Calibration against an already-reviewed article validates the harness only and must not be reported as savings evidence.

## Execution-policy boundary

The template names a frontier BYOK route without embedding a provider or credential. KORA already has provider adapters that can be injected by an authorized harness. A local-only control may route both tiers to an explicitly configured loopback model. Missing credentials fail closed; the example has no hidden provider fallback.

A successful local exact-repeat is evidence about reuse for that frozen input only. It is not evidence of frontier API cost savings. A frontier economics claim requires a separately measured BYOK run with the same workload and quality contract.

## Exact-reuse contract

`cacheable: true` means only that an already validated result may be reused when the complete node execution identity is exact: instruction, dependencies, bounded input, output schema, token budget, route, adapter class, provider/local endpoint identity, and model identity. It does not authorize semantic-similarity reuse. Any changed workload, model, route, endpoint, schema, or execution contract invalidates the exact key. Credentials are never part of the recorded identity.

## Runnable harness

The example runner accepts a bounded workload JSON and explicit policy. It never reads the Specul.AI repository directly.

```bash
python examples/solutions/specul-editorial-v1/run.py \
  --workload /path/to/workload.json \
  --policy local-control \
  --cache-dir /path/to/private-cache \
  --output /path/to/private-run.json
```

Available policies are `frontier-baseline`, `kora-local-first`, `local-control`, and `local-control-no-reuse`. Frontier policies require either `OPENAI_API_KEY` or the safer `KORA_OPENAI_API_KEY_FILE`, plus `KORA_OPENAI_MODEL`; `kora-local-first` also requires a non-secret `KORA_OPENAI_CACHE_ID` that the operator changes whenever the remote model/config identity may have changed; local policies require the loopback local-model environment documented by the local adapter; exact-reuse policies also require a non-secret `KORA_LOCAL_OPENAI_RUNTIME_ID` that changes whenever the local serving identity/configuration changes. Missing configuration fails closed. The output file may contain generated content and therefore belongs in private evidence unless it has been separately reviewed for publication.
