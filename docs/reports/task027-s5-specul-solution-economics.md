# Task027 — S5 first real KORA Solution integration and economics

Status: bounded local dogfooding complete; frontier BYOK economics blocked because no provider credential is configured in the authorized execution environment. Current KORA development cycle is not closed on frontier-cost evidence.
Base: `53ab9bd6323f7c1109a06a26270e432e8908c00a`.

## Objective

Use an independently developed Specul.AI Content OS editorial workflow as the first bounded real-service dogfooding workload for KORA. Preserve Specul as an independent upstream. Measure only the incremental effect of KORA routing/reuse/local execution relative to Specul's existing deterministic control plane.

## Frozen upstream

- Product: Specul.AI Content OS / Publishing.
- Canonical upstream revision for S5: `de2f302326bb79ca541ccab099295c73fe2dce06`.
- Upstream remains read-only during this sprint.
- Existing Specul deterministic validation/state/versioning work is baseline capability and must not be counted as KORA savings.

## In scope

1. Define a provider-neutral editorial workload contract and telemetry schema.
2. Add a bounded Specul adapter that accepts immutable brief/research/evidence inputs without modifying the Specul repo.
3. Support explicit execution policies for baseline-frontier and KORA-routed execution using already configured adapters/resources.
4. Record per-node execution kind, provider/model identity label, calls, input/output tokens, elapsed time, reuse, and quality checks.
5. Calibration on the already-reviewed upstream article is evaluator/harness validation only; no savings claim.
6. Run at least one fresh unseen editorial workload through both paths when configured resources are available.
7. Run exact-repeat and changed-input cases to verify reuse/invalidation boundaries.
8. Preserve failures and unfavorable results.
9. Produce a bounded S5 report and approval packet.

## Quality floor

The two compared paths receive the same workload inputs and are judged by the same structural/evidence requirements. No KORA result passes merely because it is cheaper. Existing Specul deterministic controls are not disabled in the baseline.

## Hard boundaries

- No write to the Specul.AI canonical repository or its production SQLite database.
- No Substack/social publication or browser mutation.
- No H100 use in S5 unless separately required and re-authorized.
- No broad production, customer-savings, quality-superiority, representativeness, or hardware-superiority claim.
- Raw provider responses, credentials, private endpoints, and private content are local evidence only.
- No Pack is promoted from this one Solution; only Pack candidates may be recorded.

## Done condition

S5 closes only when the integration contract is tested, calibration succeeds, a fresh baseline/KORA comparison is either completed or explicitly blocked with the exact resource reason, repeat/changed-input semantics are tested, full regression passes, and the evidence/claim boundary is reviewed. A negative economics result is still a valid S5 result.


## Implemented integration slice

The S5 branch adds a provider-neutral workload-economics runner and a loopback-only OpenAI-compatible local adapter. The runner records node route, provider/model labels, actual model calls, input/output tokens reported by the runtime, elapsed time, exact-reuse hits, and output digests. It supports a full-context control and a `brief+deps` compact-context policy. Semantic outputs are schema-checked before they may enter the exact-reuse cache.

The public Specul editorial template freezes only upstream revision `de2f302326bb79ca541ccab099295c73fe2dce06` and the six semantic work units: research, synthesis, draft, claim review, editorial review, and revision. No Specul source code, article text, database, credential, browser state, or raw model response is copied into the public repository.

## Calibration evidence

Calibration used the already-reviewed Specul article only to repair and verify the harness. Two early local calibration attempts exposed a provenance-contract defect: generated `claim_source_ids` could be dependency paths instead of source IDs. The attempts were retained locally as failed calibration evidence. The contract was tightened so synthesis/draft/revision preserve the upstream source-ID boundary. The third calibration passed the bounded title/article/provenance/resolved-findings checks for original, exact-repeat, and changed-input cases.

Calibration results are not used as economics evidence because the source article and its prior reviewed outcome were already known.

## Fresh local dogfooding control

A new unpublished Build-to-Insight editorial candidate was assembled from bounded excerpts of three existing KORA/Specul project records. It was not an existing Specul article and no external draft or publication action occurred. Early dogfooding attempts exposed real integration defects: oversized local context, overlong research output, loose provenance instructions, and an output-shape mismatch. Each failed closed and was repaired in the integration contract rather than hidden or counted as a result.

The final public harness uses a strict six-node semantic contract: research, synthesis, draft, claim review, editorial review, and revision. Provenance fields are dynamically constrained to the source IDs declared by the workload. Local output receives a compact type-shape hint, while KORA independently applies the full JSON Schema before a result can be cached or propagated.

Both successful comparison paths used the same existing Qwen3-30B-A3B Q4_K_M local runtime and the same compact semantic context. This control therefore isolates exact-result reuse; it does not measure frontier routing or API cost.

| Case | No-reuse local control | KORA exact-reuse local control | Bounded quality/evidence result |
|---|---:|---:|---|
| First execution | 6 model calls; 5,592 input tokens; 1,285 output tokens | 6 model calls; 5,592 input tokens; 1,285 output tokens | Outputs identical; declared source IDs preserved |
| Exact repeat after runner restart | 6 model calls; 5,592 input tokens; 1,285 output tokens | 0 model calls; 0 input tokens; 0 output tokens; 6 exact-reuse hits | Output identical to first run |
| Changed-input probe | 6 model calls; 5,783 input tokens; 1,407 output tokens | 6 model calls; 5,783 input tokens; 1,407 output tokens; 0 reuse hits | Outputs identical; changed workload fully invalidated reuse |

For the exact repeat only, this bounded local control observed a 100% reduction in model calls and runtime-reported input/output tokens relative to the no-reuse control. First execution and changed input showed **no** call or token reduction. This result is specific to one exact repeated workload and must not be generalized to first-run workloads, customer bills, production traffic, or other Solutions.

Exact reuse is persistent rather than process-local. The first run populated a bounded checksum-protected cache; a new runner process then loaded the same cache and completed all six nodes with zero model calls. A separate probe changed only the declared local runtime identity while keeping the workload, endpoint, and model label otherwise the same. All six nodes executed again with zero reuse hits, demonstrating that a changed runtime identity invalidates the prior exact-result entries.

The persistent key binds the node instruction, dependency set, token budget, output contract, complete bound input, route, adapter class, and declared non-secret execution identity. Cached results are checksum checked and schema revalidated before use. Credentials are not included in cache identity or cache records. A scan of the local cache evidence found no credential markers.

The final generated articles and raw model responses remain local evidence. The public quality statement is intentionally narrow: the outputs satisfied the declared structural/provenance contract, used only the allowed source IDs, and preserved required title/article/review fields. It is not broad editorial-quality or factual-correctness proof.

## Frontier BYOK gate

S5 rechecked the authorized execution environments without exposing secret values. No OpenAI, Anthropic, Gemini, or Google provider credential is currently configured for this KORA Project 2 execution environment, and no project-local credential configuration exists. No key was searched for outside the project boundary, copied from another project, generated, or embedded.

Therefore the intended frontier baseline versus local-first/frontier-escalation economics run is **not measured yet**. No API-cost or frontier-call-reduction percentage is claimed from S5 at this point. Once an explicit BYOK credential is registered for KORA, the same frozen workload contract can run the frontier comparison without changing Specul upstream.

## Current implementation boundary

The implementation now includes a runnable public Specul editorial harness, a provider-neutral economics runner, a loopback-only local-model adapter, persistent exact-result storage, identity-bound invalidation, dynamic provenance schemas, explicit frontier/local policies, and fail-closed missing-credential behavior. The Specul.AI upstream repository and production database remain unchanged.

Frontier comparison policies require both an explicitly configured BYOK credential and an explicitly selected frontier model. The exact-reuse local-first policy additionally requires an explicit non-secret remote cache identity so an operator can invalidate prior frontier results when the remote serving identity/configuration may have changed. Missing configuration fails before a result file is created. No remote provider request has been made in this S5 checkpoint.

## Pack candidates, not Packs

This first Solution exposes candidate reusable patterns around evidence extraction/provenance, semantic review, context compaction, identity-bound exact-result reuse, and provider/local routing. None is promoted to a KORA Pack from one Solution. Cross-Solution reuse must be demonstrated first.

## Current stop gate

The Solution integration, local-model execution, persistent repeat/invalidation behavior, failure preservation, and local control comparison are complete for this bounded slice. The broader S5 frontier-economics objective remains blocked until an explicit BYOK credential is registered in the authorized KORA execution environment. No frontier API economics or production savings claim is supported yet. Merge remains a separate maintainer approval gate.

## Final validation for this checkpoint

Validation used a supported Python 3.13 environment on the authorized development host:

- targeted S5 and adjacent-provider tests: `44 passed`;
- full repository regression: `773 passed`;
- targeted Ruff on all changed Python implementation/example/test files: PASS;
- Python compile check: PASS;
- `git diff --check`: PASS;
- repository release smoke under Python 3.13: PASS;
- fresh sdist and wheel build: PASS;
- economics runner, local OpenAI-compatible adapter, and updated OpenAI adapter present in the built wheel: PASS;
- isolated wheel installation and import: PASS;
- public documentation/example private-path and credential-pattern scans: PASS.

The first release-smoke attempt during development inherited an unsupported system Python 3.9 and failed on existing Python-3.10+ syntax. The same smoke completed under the supported Python 3.13 validation environment. No Python 3.9 compatibility claim follows.

Classification for this checkpoint: **blocked** on the missing BYOK frontier execution required to finish S5 economics. The local implementation and dogfooding evidence are reviewable, but S5 is not complete and this checkpoint must not be merged as if frontier economics had passed.
