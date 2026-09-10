# Specul.AI Editorial v1 workload template

This is a bounded KORA integration template for an independently developed editorial service. It freezes only the upstream revision and semantic node contract. The Specul.AI repository, production database, article text, provider credentials, raw model responses, and browser state are not vendored here.

Baseline comparison must retain the upstream service's existing deterministic control plane. KORA economics may count only incremental routing, exact reuse, context, call, and explicitly attributable execution differences introduced by KORA. Calibration against already-reviewed material validates the harness only and must not be reported as savings evidence.

## Execution-policy boundary

The runnable policies are deliberately explicit:

- `frontier-baseline` routes semantic work to the configured frontier adapter with full context and disables exact reuse. It is the quality/economics control.
- `kora-auto` keeps semantic execution on the frontier route, uses compact `brief+deps` context, and enables identity-bound exact-result reuse. S5 observed first-run token reduction with this policy, but semantic non-regression was not established, so the observed economics delta is not quality-preserving savings evidence.
- `kora-local-first` is a bounded quality-sensitive experiment: the routine tier may start on an explicitly configured loopback local adapter and fall back to frontier execution, while frontier-tier work remains frontier. S5 does not establish that this policy is automatically preferable.
- `kora-quality-auto` is an experimental compact-context frontier policy that can retain full context for declared quality-sensitive nodes. It is not an accepted S5 economics result.
- `local-control` and `local-control-no-reuse` are local-only mechanism controls. They do not establish frontier economics or broad local-model quality.

Missing required configuration fails closed. The example has no hidden remote fallback.

## Exact-reuse and invalidation contract

`cacheable: true` means only that an already validated result may be reused when the complete relevant execution identity is exact: instruction, dependencies, bounded input, output schema, token budget, route, adapter identity, provider/local serving identity, and model identity. It does not authorize semantic-similarity reuse. Any relevant workload, model, route, endpoint/serving identity, schema, or execution-contract change invalidates the exact key. Credentials are never part of recorded cache identity.

S5 separately confirmed exact repeat reuse and changed-input invalidation in bounded evidence. Those mechanism results do not establish semantic equivalence for approximate inputs.

## Quality and human-review boundary

Structural/provenance validation is necessary but not sufficient for a semantic quality claim. For meaningful A/B evaluation, retain machine evidence and human-readable actual outputs so a maintainer can inspect source fidelity and completeness directly. Automated semantic review may supplement that inspection but does not override a visible defect.

Context reduction must therefore be treated as quality-sensitive. A smaller prompt is not automatically a better KORA decision, and a later quality gate may legitimately choose full context when semantic coverage cannot be preserved safely.

## Runnable harness

The example runner accepts a bounded workload JSON and explicit policy. It never reads the Specul.AI repository directly.

```bash
python examples/solutions/specul-editorial-v1/run.py \
  --workload /path/to/workload.json \
  --policy kora-auto \
  --cache-dir /path/to/private-cache \
  --output /path/to/private-run.json
```

Frontier policies require either `OPENAI_API_KEY` or `KORA_OPENAI_API_KEY_FILE`, plus `KORA_OPENAI_MODEL`. Exact frontier reuse additionally requires a non-secret `KORA_OPENAI_CACHE_ID` that changes whenever the remote serving identity/configuration may have changed. Local policies require the loopback local-model environment documented by the local adapter; exact local reuse additionally requires a non-secret `KORA_LOCAL_OPENAI_RUNTIME_ID` that changes whenever the local serving identity/configuration changes.

The output file may contain generated content and therefore belongs in private evidence unless it has been separately reviewed for publication.
