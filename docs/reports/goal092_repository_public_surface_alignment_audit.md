# Goal 092 Repository Public Surface Alignment Audit

Current public HEAD: `2972973d732624353bd722d648886eed4d6d9e6c`

Status: audit and proposal only. This goal did not change repository settings, move root files, restructure directories, create a release, create a tag, create a publication, or change product claims.

## Summary

The README and new documentation index now present KORA as an AI Workload Control Layer, but the broader public surface still mixes the newer positioning with older inference, benchmark, release, and research-oriented material. A new visitor can reach a correct first impression from the README, but the GitHub About text, root document list, and large docs tree still make the project look like a benchmark-heavy research repository rather than an examples-first workload-control project.

The safest next step is a staged cleanup plan that changes metadata first, then adds link-preserving orientation stubs, then proposes file moves only after explicit approval.

## GitHub About and Metadata Assessment

Observed public metadata:

| Surface | Current value | Assessment |
| --- | --- | --- |
| Repository visibility | public | Correct for the public project. |
| Default branch | `main` | Correct. |
| Description | `An Inference Operating System that reduces unnecessary LLM calls by structuring intelligence before scaling it.` | Conflicts with the current AI Workload Control Layer positioning. It also foregrounds avoided calls and system identity before the bounded examples-first story. |
| Homepage | empty | Acceptable, but could later point to docs or a project page if one exists. |
| Topics | `agent-framework`, `ai-infrastructure`, `cost-optimization`, `inference`, `json-schema`, `large-language-models`, `llm`, `open-source`, `orchestration`, `task-graph` | Several topics are still useful, but the set over-weights inference and cost framing while missing workload-control and routing language. |

Proposed repository description:

> AI Workload Control Layer for routing deterministic, reusable, retrieval-needed, tool-needed, and provider-needed work before model invocation.

Proposed topics:

- `ai-infrastructure`
- `workload-routing`
- `ai-workload-control`
- `task-graph`
- `deterministic-routing`
- `llm-infrastructure`
- `retrieval-routing`
- `tool-routing`
- `python`
- `open-source`

Do not change these settings in this goal. The description and topics should be applied only after owner approval.

## Root Directory Audit

| Root item | Classification | Rationale | Later action |
| --- | --- | --- | --- |
| `README.md` | keep at root | Primary public landing page now matches the AI Workload Control Layer positioning. | Keep as the public first stop. |
| `pyproject.toml` | keep at root | Standard Python project metadata. | Keep. |
| `kora/` | keep at root | Main package source. | Keep. |
| `tests/` | keep at root | Standard test location. | Keep. |
| `.github/` | keep at root | Issue templates, PR template, and CI workflow belong at root. | Keep, but later review template wording for current positioning. |
| `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `GOVERNANCE.md` | keep at root | Standard project governance and legal surfaces. | Keep. |
| `docs/` | keep at root | Main documentation tree. | Keep; later add clearer top-level buckets. |
| `examples/` | keep at root | Public first-value examples are central to the current narrative. | Keep; later separate flagship and older examples. |
| `scripts/` | keep at root | Development and validation utilities. | Keep, but later document which scripts are public reviewer paths. |
| `ARCHITECTURE-OVERVIEW.md` | requires link-preserving stub if moved | Useful but older language emphasizes layered inference architecture and references older docs. | Later move body under docs architecture area and leave a short root stub. |
| `EXECUTIVE-SUMMARY.md` | requires link-preserving stub if moved | Starts with older inference-first framing, which conflicts with current README positioning. | Later replace root file with a short pointer or move to docs strategy/history after approval. |
| `VISION.md` | requires link-preserving stub if moved | Still useful but broader and more philosophical than the current first impression should be. | Later move under docs vision/history and leave pointer. |
| `ROADMAP.md` | requires link-preserving stub if moved | Older versioned roadmap does not reflect the latest examples-first public path. | Later move under docs planning/history or refresh after approval. |
| `OPEN_THIS_FIRST.md` | keep at root | Active project breadcrumb used for continuation. | Keep, but keep it concise and current. |
| `REVIEW_HUB.md` | keep at root | Active review and continuation surface. | Keep, but later reduce older evidence density or add a clear current-review section. |
| `CHANGELOG.md` | keep but de-emphasize | Contains release-preparation and benchmark-heavy material. It is normal at root but not a first-read document. | Keep; later make current status clearer at top. |
| `artifacts/` | move to docs later | Root artifacts make the repo look evidence-output-first. | Later move to `docs/evidence/artifacts/` or add a root README explaining scope. |
| `experiments/` | keep but de-emphasize | Useful reproducibility area, but it pushes benchmark/research framing in the root list. | Later add a stronger README boundary or consider docs-linked organization. |
| `assets/` | keep but de-emphasize | Brand assets are harmless but not part of first-value onboarding. | Keep or later consolidate with docs assets after link audit. |
| `studio/` | requires further review | Product surface is substantial and may deserve its own narrative. Moving it may break local workflows. | Do not move without a dedicated Studio review goal. |
| `tools/` | keep but de-emphasize | Small utility area. | Keep; later document utility scope. |

## Examples Directory Audit

| Example path | Classification | Assessment | Later action |
| --- | --- | --- | --- |
| `examples/kora_doctor/` | flagship example | Strong first-value workload inspection path. | Keep prominent. |
| `examples/deterministic_classification/` | flagship example | Clear deterministic routing example pack. | Keep prominent. |
| `examples/openai_compatible_proxy/` | flagship example | Good bridge from common request shape to workload routing, with explicit boundaries. | Keep prominent. |
| `examples/rag_routing/` | flagship example | Good retrieval-needed versus provider-needed illustration. | Keep prominent. |
| `examples/agent_workflow_optimization/` | flagship example | Good multi-step workflow routing illustration. | Keep prominent. |
| `examples/cache_reuse/` | flagship example | Good repeated-work reuse illustration. | Keep prominent. |
| `examples/hello_kora/` | older first-run example | Useful minimal graph example, but less aligned with current flagship narrative. | Candidate for older/basic grouping. |
| `examples/direct_vs_kora/` | older first-run example | Useful contrast example, but not part of current README path. | Candidate for older/basic grouping. |
| `examples/retry_demo/` | older first-run example | Useful runtime behavior demo, not first-read material. | Candidate for older/basic grouping. |
| `examples/customer_support_triage_fake_validation/` | validation example | Name and purpose read like validation scaffolding. | Candidate for validation grouping. |
| `examples/real_model_call_validation_fake/` | validation example | Name is confusing for public first impression because it combines real/fake wording. | Candidate for validation grouping or rename proposal after approval. |
| `examples/real_workload_harness/` | validation or benchmark example | Harness-oriented, not newcomer-first. | Candidate for validation grouping. |
| `examples/runtime_integrated_benchmark/` | benchmark example | Benchmark-facing, not part of the current quickstart. | Candidate for benchmark grouping. |
| `examples/stress_test/` | validation or benchmark example | Useful for stress behavior, not first-value onboarding. | Candidate for validation grouping. |
| `examples/workloads/` | validation or benchmark fixtures | Fixture data supports older evidence paths. | Candidate for docs/evidence or examples/validation grouping. |

Recommended future organization, pending approval:

- `examples/flagship/` or a README-only grouping for current first-value examples.
- `examples/basic/` for minimal graph and contrast examples.
- `examples/validation/` for validation harnesses and fixture-oriented examples.
- `examples/benchmarks/` for benchmark-specific examples.
- Link-preserving stubs or README redirects for any moved example paths.

## Docs Directory Audit Summary

High-priority user-facing docs:

- `docs/README.md`
- `docs/vision/kora_workload_control_layer.md`
- `docs/examples/kora_example_guide.md`
- `docs/packaging/getkora_distribution_strategy.md`
- `docs/claims/kora-claim-registry.md`
- `docs/claims/kora-public-language-guide.md`
- `docs/quickstart-five-minute-first-value.md`
- `docs/FAQ.md`
- `docs/glossary.md`

Evidence and report docs:

- `docs/evidence/`
- `docs/reports/`
- `docs/benchmarks/`
- `docs/metrics/`
- generated evidence summaries under `docs/evidence/generated/`

Historical, planning, and operating docs:

- `docs/planning/`
- `docs/progress/`
- `docs/implementation/`
- `docs/strategy/`
- `docs/eod/`
- `docs/project-operating-system/`
- older release and readiness reports under `docs/reports/`

Product or surface-specific docs:

- `docs/kora-studio/`
- `docs/product/`
- `docs/design/`
- `studio/`

Possible future archive buckets:

- `docs/archive/reports/` for older release-readiness and planning reports.
- `docs/archive/evidence/` for superseded evidence snapshots that are not part of the current reviewer path.
- `docs/archive/strategy/` for older roadmap, manifesto, launch, and planning material.
- `docs/examples/validation/` for validation and benchmark organization guides.

The docs tree is functional but very broad. The main risk is not that docs are wrong; it is that a new visitor cannot easily tell which docs are current user-facing docs versus historical evidence or planning material.

## Public First Impression

| Surface | Visitor impression | Alignment |
| --- | --- | --- |
| Repo About | Older inference-operating-system and cost framing. | Needs metadata update after approval. |
| Root directory list | Looks broad, research-heavy, and evidence-heavy despite the improved README. | Needs staged root de-emphasis and stubs. |
| README | Clear and current: AI Workload Control Layer, source install, flagship examples, claim boundaries. | Aligned. |
| `examples/` | README is aligned, but directory list mixes flagship examples with older validation and benchmark examples. | Needs later organization or labels. |
| `docs/` | New docs index is aligned, but the tree contains many historical, planning, evidence, and product docs at similar prominence. | Needs index and archive strategy. |

## Recommended Staged Cleanup Plan

1. Metadata-only goal: update repository description and topics after explicit approval.
2. Root orientation goal: add or refresh short root stubs for older root docs without moving files.
3. Examples organization goal: add grouping language and optionally create link-preserving stubs before any path moves.
4. Docs navigation goal: add a current-docs path, evidence path, and archive path to `docs/README.md`.
5. Archive proposal goal: propose exact moves for older reports and planning docs, including redirect/stub plan and link-check plan.
6. Studio surface review goal: audit whether Studio should remain a root product surface or move under a separate documented path.

## Risks of Moving Files

- Existing external links to root docs or example paths may break.
- Internal docs links may break if moves happen without a link audit.
- Tests or scripts may reference example paths directly.
- README quickstart commands can break if examples move.
- Historical reports may lose context if archived without clear index entries.
- Moving Studio or experiment directories may break local workflows.

Any move should use a dedicated PR, run link validation, run example smoke checks, and include stubs for likely public links.

## Items Not To Change Without Approval

- GitHub repository description, homepage, and topics.
- Root file moves or root directory moves.
- Example path moves.
- Docs archive moves.
- Studio path or product-surface changes.
- Release, tag, publication, or package distribution state.
- Package name or install guidance.
- Claim registry and public language boundary changes.

## Recommended Next Goal

Goal 093 should be a metadata-only owner-approved update: change the GitHub repository description and topics to match the AI Workload Control Layer positioning, then verify the public About panel and stop. It should not move files or rewrite docs.
