# Task027 — S5 first real KORA Solution integration and economics

Status: **completed negative/learning sprint, pending maintainer merge approval**. The bounded S5 implementation and evidence package are complete. First-run context/token economics improved in the frozen final holdout, but semantic non-regression was **not established**; therefore S5 does not support a quality-preserving or general savings claim.

Base: `53ab9bd6323f7c1109a06a26270e432e8908c00a`.

## Objective

Use an independently developed Specul.AI Content OS editorial workflow as the first bounded real-service dogfooding workload for KORA. Preserve Specul as an independent upstream and measure only incremental KORA execution behavior rather than counting Specul's existing deterministic control plane as KORA savings.

## Frozen upstream and hard boundaries

- Product: Specul.AI Content OS / Publishing.
- Canonical upstream revision for S5: `de2f302326bb79ca541ccab099295c73fe2dce06`.
- Upstream remained read-only during S5.
- Existing Specul validation, state, versioning, and browser/draft controls are baseline capability and are not counted as KORA savings.
- No public production-readiness, customer-savings, quality-superiority, representativeness, or hardware-superiority claim follows from S5.
- Raw generated content, provider responses, credentials, private endpoints, and human-review artifacts remain outside the public repository unless separately reviewed and promoted.

## Implemented integration slice

The S5 branch adds a provider-neutral workload-economics runner, a loopback-only OpenAI-compatible local adapter, and an updated frontier adapter path. The runner records node routes, model calls, runtime-reported input/output tokens, elapsed time, exact-reuse hits, escalation events, provider token telemetry when available, and output digests. Semantic outputs are schema checked before they may be cached or propagated.

The public editorial template freezes the upstream revision and seven bounded semantic work units: research, synthesis, draft, claim review, editorial review, revision, and one bounded quality-repair step. Provenance fields are constrained to source IDs declared by the workload. The branch also adds node-specific output budgets and a richer bounded research-evidence contract.

Persistent exact-result reuse binds the complete relevant execution identity, including the node instruction, dependencies, token budget, output contract, bound workload input, route, adapter identity, and declared non-secret serving identity. Cache entries are checksum checked and schema revalidated before reuse. Credentials are not part of cache identity or cache records.

## Execution policies

- `frontier-baseline`: frontier semantic execution with full context and no exact-result reuse. This is the quality/economics control.
- `kora-auto`: frontier semantic execution with compact `brief+deps` context and persistent exact-result reuse. This was the primary S5 KORA comparison policy.
- `kora-local-first`: bounded quality-sensitive experimental policy. Routine work may start on the explicitly configured loopback local adapter and fail over to frontier execution; semantic/frontier work remains on the frontier route. S5 does **not** establish that local-first is automatically preferable.
- `kora-quality-auto`: frontier semantic execution with compact context while selectively retaining full context for the declared draft node. It is an experimental policy, not an accepted S5 economics result.
- `local-control` and `local-control-no-reuse`: local-only controls used to isolate exact-reuse behavior. They are not evidence of frontier economics or broad local-model quality.

All routes fail closed when their explicitly required configuration is absent; there is no hidden remote fallback.

## Calibration and local-control learning

Calibration used already-reviewed material only to repair and verify the harness and is not counted as savings evidence. Preserved failures included overly loose provenance constraints, oversized local context, output truncation, output-shape mismatch, and insufficient bounded research shape. These failures led to stricter provenance, schema, output-budget, and research-evidence contracts.

A separate local-only control demonstrated persistent exact-result reuse under unchanged execution identity and invalidation under changed workload/runtime identity. That result is mechanism evidence only, not a claim that local execution is preferable for the semantic workload.

## Frozen final holdout

The final S5 holdout was frozen before its output was reviewed. It is now seen data and must not be reused as an unseen holdout for later tuning.

Both first-run paths used seven semantic model calls and passed the declared structural/provenance quality gate:

| Metric | `frontier-baseline` | `kora-auto` | Observed delta |
|---|---:|---:|---:|
| Model calls | 7 | 7 | 0% |
| Input tokens | 38,558 | 22,226 | -42.36% |
| Output tokens | 13,439 | 12,190 | -9.29% |
| Wall time | 221,306 ms | 229,975 ms | +3.92% |
| Token-based list-price estimate used by the local evidence script | $0.423012 | $0.332704 | -21.35% |

These figures establish only that this frozen first-run KORA path reduced measured input tokens and the associated token-based list-price estimate. KORA was slightly slower in this run. The figures do **not** establish quality-preserving savings, customer savings, production savings, or general workload savings.

### Exact repeat and changed-input invalidation

For an identical repeat under the same frozen execution identity, `kora-auto` produced:

- 7/7 exact-reuse hits;
- 0 model calls;
- 0 input tokens;
- 0 output tokens;
- an output digest identical to its first run.

A changed-input probe produced 0 reuse hits and recomputed all seven model-backed nodes. These results support bounded persistent exact-result reuse and exact-key invalidation. They do not authorize semantic-similarity reuse.

## Semantic and human-review verdict

Structural/provenance checks alone were insufficient to establish non-regression. Independent blind semantic review in both candidate orders consistently preferred the full-context baseline. Human-readable direct comparison also remains a required acceptance input; machine counters or automated semantic review cannot override visible source-fidelity or completeness defects.

Observed KORA Auto gaps in the frozen final holdout included missing or distorted low-frequency but high-importance boundaries around attribution, freshness limits, interrupted-transfer incomplete-state handling, and protections governing existing external content. The compact path already retained multiple evidence items per source, so the lesson is not simply to increase summary count.

**S5 semantic non-regression: NOT ESTABLISHED.**

Therefore the observed 21.35% token-based list-price delta is **not** reported as quality-preserving savings. The correct bounded lesson is that context compression can reduce token economics, but compression must be gated by semantic coverage/fidelity rather than optimized for token reduction alone.

## Public claim boundary

S5 supports these bounded public statements:

1. Persistent exact-result reuse worked for an identical frozen execution identity.
2. Relevant changed input invalidated prior exact-result reuse and forced recomputation.
3. In the frozen final first-run holdout, compact context reduced measured input tokens and the local token-based list-price estimate.
4. Semantic non-regression was not established, so the first-run economics delta is failure/learning evidence rather than successful quality-preserving savings evidence.

S5 does not support claims of production readiness, customer savings, general percentage savings, representative editorial quality, general quality-preserving compression, local-model superiority, provider superiority, or hardware superiority.

## Human-readable evidence boundary

Actual baseline and KORA output artifacts were retained for direct maintainer review outside the public repository. Meaningful A/B acceptance requires the machine evidence plus readable actual outputs; a structural PASS or automated semantic-review PASS is not sufficient by itself.

## Pack candidates, not Packs

This Solution exposes candidate reusable patterns around semantic evidence extraction, provenance, context compaction, identity-bound exact-result reuse, provider/local routing, and quality-gated compression. None is promoted to a KORA Pack from this one Solution. Cross-Solution evidence is required first.

## Final validation

Final engineering validation was rerun against the complete S5 implementation/documentation diff under Python 3.13:

- Ruff on all changed Python files: PASS;
- targeted S5 tests: `40 passed`;
- full repository regression: `789 passed`;
- Python `compileall`: PASS;
- `git diff --check`: PASS;
- repository release smoke: PASS;
- fresh sdist and wheel build: PASS;
- required S5 package modules present in the wheel: PASS;
- isolated wheel install/import from a neutral working directory: PASS;
- Task027 changed-file scan for private `/Volumes/` or `/Users/` paths, high-confidence secret patterns, and prohibited assistant/tool names: PASS with zero findings.

A repository-wide hygiene scan also surfaced inherited legacy public-tree occurrences of private-path examples and prohibited assistant/tool names. The same locations are already present at `origin/main`; Task027 introduced none of them. They remain separate repository hygiene debt and are not treated as S5 evidence.

Package digests and detailed validation provenance are retained in the private closure summary.

## Classification

S5 is a **completed negative/learning sprint** after this engineering/evidence closure. Its negative semantic/economics verdict is an accepted sprint outcome, not a reason to rewrite the frozen holdout. PR #298 remains Draft/Open pending separate explicit maintainer merge approval.
