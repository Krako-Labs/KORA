# Goal 096 Documentation Navigation and Archive-Bucket Proposal

Current public HEAD: `424cc71860df32c3636ce29b67c02730ad4b28e8`

Status: proposal only. No files moved in this task. Task 096 did not move, archive, rename, or delete files; change repository settings; create a release; create a tag; create a GitHub Release; publish to PyPI; create GitHub issues; create project boards; upload release assets; or upload raw benchmark artifacts.

## Purpose

Goal 096 proposes a clearer public documentation navigation model after Goals 091B-095 aligned the README, docs index, examples index, repository metadata, root orientation stubs, and examples grouping around KORA as an AI Workload Control Layer.

The goal is to make the current reader path easier to scan while preserving historical, planning, evidence, and reference material in place. Movement requires later explicit Albert approval.

## Current Public Documentation Entry Points

| Entry point | Current role | Keep current-facing? |
| --- | --- | --- |
| `README.md` | Primary public landing page, source-install quick start, flagship examples, package boundary, and claim boundary. | Yes |
| `docs/README.md` | Main documentation index for readers who need more detail than the root README. | Yes |
| `examples/README.md` | Example catalog with flagship examples and grouped older examples. | Yes |
| `docs/examples/kora_example_guide.md` | Guided path through flagship examples and additional example groups. | Yes |
| `docs/vision/kora_workload_control_layer.md` | Current vision explanation for workload control before model invocation. | Yes |
| `OPEN_THIS_FIRST.md` | Public continuation breadcrumb for maintainers and review sessions. | Yes |
| `REVIEW_HUB.md` | Detailed public review and continuation hub. | Yes |

## Current Visitor Path

Recommended current visitor path:

1. Start with `README.md` to understand KORA as an AI Workload Control Layer.
2. Use the README source-install path and run the first-value examples.
3. Open `examples/README.md` for the flagship example catalog.
4. Use `docs/examples/kora_example_guide.md` for the recommended example order.
5. Read `docs/vision/kora_workload_control_layer.md` for the workload-control model.
6. Use `docs/README.md` as the broader documentation map.
7. Use `docs/reports/` and `docs/evidence/` only when reviewing evidence, history, or implementation reports.

This path preserves the current examples-first narrative and avoids making new readers begin in historical reports or benchmark-heavy material.

## Current Docs-Tree Confusion Points

The docs tree is useful but broad. Current confusion points:

- current user-facing docs, historical reports, implementation plans, evidence snapshots, and project operating materials appear at similar depth.
- `docs/reports/` contains both current reviewer reports and older release-readiness or planning reports.
- `docs/evidence/`, `docs/benchmarks/`, `docs/metrics/`, and generated evidence summaries are important for review but should not be mistaken for the first-run path.
- `docs/planning/`, `docs/progress/`, `docs/implementation/`, `docs/strategy/`, and `docs/eod/` contain planning or historical continuity material that can overwhelm a new visitor.
- root strategic documents now have orientation stubs, but future movement would still need link-preserving stubs or redirects before any future move.
- KORA Studio and paper-related docs are substantial surfaces and should not be moved or reclassified without dedicated review.

These are navigation problems, not validity problems. Older docs are not invalid; they need clearer reader routing.

## Proposed Documentation Navigation Buckets

| Proposed bucket | Reader intent | Current files or directories |
| --- | --- | --- |
| Current public entry path | Understand KORA quickly and run the first examples. | `README.md`, `docs/README.md`, `docs/vision/kora_workload_control_layer.md`, `examples/README.md`, `docs/examples/kora_example_guide.md`, `docs/packaging/getkora_distribution_strategy.md` |
| Examples and first-value path | Run and understand source-install examples. | `examples/kora_doctor/`, `examples/deterministic_classification/`, `examples/openai_compatible_proxy/`, `examples/rag_routing/`, `examples/agent_workflow_optimization/`, `examples/cache_reuse/`, `docs/quickstart-five-minute-first-value.md` |
| Evidence and reports path | Review bounded evidence, claim support, and validation history. | `docs/reports/`, `docs/evidence/`, `docs/benchmarks/`, `docs/metrics/`, `docs/claims/` |
| Historical/planning path | Preserve strategy, planning, progress, release-readiness, and implementation continuity. | `docs/planning/`, `docs/progress/`, `docs/implementation/`, `docs/strategy/`, `docs/eod/`, older files in `docs/reports/` |
| Project operations path | Continue project work and contribution/review operations. | `OPEN_THIS_FIRST.md`, `REVIEW_HUB.md`, `docs/project-operating-system/`, `docs/runbooks/`, `CONTRIBUTING.md`, `SECURITY.md`, `GOVERNANCE.md` |
| Product/surface-specific path | Keep specialized product, paper, and Studio material discoverable without making it the default first-read path. | `docs/kora-studio/`, `docs/product/`, `docs/design/`, `docs/paper/`, `studio/` |

No files moved in this task. These are proposed buckets only.

## Candidate Archive Buckets

Candidate archive bucket proposals for a later owner-approved movement task:

| Candidate archive bucket | Candidate contents | Requirement before movement |
| --- | --- | --- |
| `docs/archive/reports/` | Older release-readiness reports, older PR packets, superseded EOD reports, and historical planning reports that are not part of the current reviewer path. | Full link inventory, link-preserving stubs or redirects, and report index update. |
| `docs/archive/evidence/` | Superseded evidence snapshots or generated summaries no longer used in the current evidence path. | Evidence-owner review and explicit note preserving the active evidence package. |
| `docs/archive/strategy/` | Older strategy, manifesto, roadmap, and launch-planning documents that predate the current AI Workload Control Layer narrative. | Root-stub review and clear historical-context labeling. |
| `docs/archive/planning/` | Older implementation plans, progress reports, and EOD material after current references are mapped. | Link check, breadcrumb review, and continuity note. |

These archive paths do not exist as active destinations in Task 096. This task creates no archive directories and moves no files.

## Files That Should Remain Current/Public-Facing

Keep these current-facing:

- `README.md`
- `docs/README.md`
- `examples/README.md`
- `docs/examples/kora_example_guide.md`
- `docs/vision/kora_workload_control_layer.md`
- `docs/packaging/getkora_distribution_strategy.md`
- `docs/claims/kora-claim-registry.md`
- `docs/claims/kora-public-language-guide.md`
- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- current flagship example READMEs under `examples/`

These files explain the current public positioning, source-install path, package boundary, example path, and claim boundaries.

## Files That Should Be Historical, Planning, Evidence, or Reference

Treat these as non-first-read material unless a reviewer is specifically checking history or evidence:

- older release-readiness reports under `docs/reports/`.
- older PR packets under `docs/reports/`.
- `docs/planning/`, `docs/progress/`, `docs/implementation/`, `docs/strategy/`, and `docs/eod/`.
- generated evidence summaries under `docs/evidence/generated/`.
- benchmark-specific material under `docs/benchmarks/`.
- metrics-specific material under `docs/metrics/`.
- KORA Studio and paper-specific docs until dedicated surface reviews decide their public routing.

These files should remain accessible and linkable. Proposed bucket labeling should make their purpose clear without implying they are invalid.

## Link-Preservation Requirements Before Any Future Movement

Before any future file movement:

1. Inventory every internal Markdown link to the candidate files and directories.
2. Search scripts, tests, docs, and README commands for hard-coded paths.
3. Identify likely public links from README, reports, PRs, and issue references.
4. Add link-preserving stubs or redirects at old paths when feasible.
5. Move one bucket at a time in a dedicated owner-approved PR.
6. Update `README.md`, `docs/README.md`, `OPEN_THIS_FIRST.md`, and `REVIEW_HUB.md` together.
7. Run markdown link validation and targeted example smoke checks after movement.
8. Keep historical context notes in moved documents so old reports remain understandable.

Link-preserving stubs or redirects are required before any future move.

## Boundary Confirmation

- No files moved in this task.
- No files were archived.
- No files were renamed.
- No files were deleted.
- No repository settings were changed.
- No GitHub issues were created.
- No project boards were created.
- No release was created.
- No tag was created.
- No GitHub Release was created.
- No PyPI publication was performed.
- No release assets were uploaded.
- No raw benchmark artifacts were uploaded.
- No package or version metadata was modified.

## Claim Boundary Confirmation

Goal 096 is documentation navigation planning only. It does not add claims of:

- production readiness.
- production cost reduction proof.
- real API-cost reduction proof.
- production benchmark proof.
- broad workload superiority.
- energy reduction.
- published `getkora`.
- release, tag, GitHub Release, or PyPI publication.

KORA remains source-install-first for latest-feature testing. `pip install kora` is not this project, and `getkora` is planned but not published.

## Recommended Next Step

Recommended later task:

- Goal 097 - Owner-approved documentation movement plan for one small bucket only, after Albert explicitly approves movement.

Suggested scope for that later task:

- pick one candidate bucket.
- perform a complete link inventory.
- propose exact old path to new path mappings.
- include link-preserving stubs or redirects.
- run link validation and targeted smoke checks.
- stop for review before broad movement.

Movement requires later explicit Albert approval.
