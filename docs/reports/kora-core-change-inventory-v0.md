# KORA Core Change Inventory v0

Status: merge-readiness inventory for the local Goal 030-037 branch. This is not a release note, tag, PR, or merge action.

## Scope

This inventory covers the local branch:

- `goal029_krk_kora_core_north_star_realignment`

Compared against:

- `origin/main`

Included goal commits:

| Goal | Commit | Subject |
| --- | --- | --- |
| Goal 030 | `50bd6a6` | `docs: realign KORA around KRK and routable workloads` |
| Goal 031 | `d61c709` | `docs: add KRK extended H100 test matrix` |
| Goal 032 | `20d6286` | `docs: polish KRK standalone alpha surface` |
| Goal 033 | `e5d4861` | `docs: add KRK performance table package` |
| Goal 034 | `7b2dc23` | `docs: add KRK technical paper draft package` |
| Goal 035 | `e73987e` | `docs: define KORA Core alpha surface` |
| Goal 036 | `3ac52c5` | `docs: add KORA naming and restructuring strategy` |
| Goal 037 | `4185a08` | `docs: add July 31 KORA deliverable package` |

## Summary

The branch realigns the public repo around:

- KORA as the umbrella for routable AI workloads.
- KORA Core as the planned open-source AI workload execution layer.
- KRK as the deterministic-first routing kernel inside KORA Core.
- the current implementation as a KRK-oriented alpha with bounded evidence.

The branch is documentation-heavy. It adds public-safe architecture, product, evidence, paper, report, strategy, and example workload materials. It does not rename repos, create repos, push, open PRs, merge, tag, or release.

## Modified Existing Files

| File | Purpose |
| --- | --- |
| `README.md` | Reframes the public hero around KORA Core, routable AI workloads, KRK alpha primitives, current CLI reality, roadmap separation, and evidence links. |
| `docs/README.md` | Adds navigation links for new strategy, product, architecture, evidence, reports, and paper docs. |

## Claims

| File | Purpose |
| --- | --- |
| `docs/claims/kora-core-alpha-claim-boundary-v0.md` | Defines supported and unsupported public claims for the KORA Core alpha framing. |

## Strategy Docs

| File | Purpose |
| --- | --- |
| `docs/strategy/kora-routable-ai-workloads-master-plan-v0-1.md` | Establishes the public north star, Docker analogy, KRK-first path, KORA Core expansion, examples roadmap, and community direction. |
| `docs/strategy/kora-naming-strategy-v0.md` | Defines KORA, KORA Core, KRK, Krako, Workload Spec, Target Registry, and Evidence Registry naming rules. |
| `docs/strategy/kora-repo-restructuring-plan-v0.md` | Compares single repo, umbrella + core, and umbrella + core + workloads structures; recommends staying single-repo near term. |
| `docs/strategy/kora-post-july-roadmap-v0.md` | Defines the post-July roadmap from KRK stabilization to KORA Core, registries, evidence, community, and repo-structure decisions. |
| `docs/strategy/kora-community-growth-plan-v0.md` | Defines developer adoption, OSS growth, examples, registry, and community feedback paths. |

## Product Docs

| File | Purpose |
| --- | --- |
| `docs/product/kora-routing-kernel-definition-v0.md` | Defines KRK as deterministic-first execution routing kernel and maps current route/explain/benchmark/report primitives. |
| `docs/product/kora-core-expansion-plan-v0.md` | Describes KORA Core as the planned OSS execution layer around inspect, compare, run, and report. |
| `docs/product/krk-quickstart-v0.md` | Documents the current KRK alpha quickstart and exact CLI reality. |
| `docs/product/krk-july1-release-candidate-v0.md` | Adds KRK July 1 release-candidate checklist and blockers. |
| `docs/product/kora-core-alpha-surface-v0.md` | Defines the KORA Core alpha surface and separates current implementation from roadmap. |
| `docs/product/kora-core-user-workflow-v0.md` | Defines the intended user workflow from workload review to report. |
| `docs/product/kora-core-inspect-definition-v0.md` | Defines inspect as a read-only workload understanding workflow. |
| `docs/product/kora-core-compare-definition-v0.md` | Defines compare as a route policy, target, and evidence comparison workflow. |
| `docs/product/kora-core-run-definition-v0.md` | Defines run as future workload execution under explicit policy and target constraints. |
| `docs/product/kora-core-report-definition-v0.md` | Defines report as bounded evidence generation. |

## Architecture Docs

| File | Purpose |
| --- | --- |
| `docs/architecture/kora-workload-spec-v0.md` | Defines a public-safe v0 Workload Spec architecture and example. |
| `docs/architecture/kora-target-registry-v0.md` | Defines target registry concepts and target metadata fields. |
| `docs/architecture/krk-architecture-v0.md` | Explains KRK inputs, route decisions, execution path classes, explanations, and evidence flow. |

## Evidence Docs

| File | Purpose |
| --- | --- |
| `docs/evidence/kora-evidence-report-schema-v0.md` | Defines the public-safe evidence report schema fields and boundaries. |
| `docs/evidence/krk-extended-h100-test-matrix-v0.md` | Defines the extended KRK test matrix and bounded GPU-routed subset methodology. |
| `docs/evidence/krk-routing-benchmark-methodology-v0.md` | Defines route-selectivity methodology, oracle label separation, baselines, and metrics. |
| `docs/evidence/krk-performance-table-schema-v0.md` | Defines performance table schema for route distribution, correctness, fallback, and reproducibility. |
| `docs/evidence/krk-public-evidence-boundary-v0.md` | Defines public-safe vs private-only evidence handling and sanitized summary rules. |
| `docs/evidence/krk-capability-matrix-v0.md` | Summarizes KRK capabilities, evidence links, limitations, and next actions. |
| `docs/evidence/krk-performance-table-v0.md` | Packages current deterministic-heavy evidence and marks unmeasured metrics explicitly. |
| `docs/evidence/krk-evidence-package-v0.md` | Explains what currently counts as evidence and what does not. |
| `docs/evidence/krk-reproducibility-matrix-v0.md` | Maps evidence items to reproducibility status and limitations. |
| `docs/evidence/krk-claim-boundary-table-v0.md` | Separates supported KRK statements from unsupported interpretations. |

## Paper Docs

| File | Purpose |
| --- | --- |
| `docs/paper/krk-technical-paper-outline-v0.md` | Adds KRK technical paper outline and title candidates. |
| `docs/paper/krk-technical-paper-draft-v0.md` | Adds public-safe KRK technical paper draft. |
| `docs/paper/krk-related-work-notes-v0.md` | Adds neutral related-work category notes. |
| `docs/paper/krk-figures-and-tables-plan-v0.md` | Adds planned figures and tables for the technical note. |
| `docs/paper/krk-paper-claim-boundary-v0.md` | Defines claim boundaries specific to the paper. |
| `docs/paper/krk-paper-next-experiments-v0.md` | Defines next experiments needed before stronger claims. |

## Report Docs

| File | Purpose |
| --- | --- |
| `docs/reports/krk-july1-evidence-summary-v0.md` | Summarizes KRK July 1 status and current evidence. |
| `docs/reports/july31-report-outline-v0.md` | Adds July 31 public-safe report outline. |
| `docs/reports/july31-development-plan-outline-v0.md` | Adds next-round development plan outline. |
| `docs/reports/july31-five-minute-video-storyboard-v0.md` | Adds five-minute video storyboard. |
| `docs/reports/july31-evidence-package-index-v0.md` | Adds evidence package navigation index. |
| `docs/reports/july31-deliverable-readiness-checklist-v0.md` | Adds report, plan, video, evidence, docs, examples, paper, and boundary readiness checklist. |
| July 31 risk/gap register report | Adds risk and gap register for unimplemented surfaces, evidence gaps, and repo naming. |

## Example Workloads

| File | Purpose |
| --- | --- |
| `examples/workloads/krk-mixed-routing-matrix-alpha.json` | Adds small mixed-realistic KRK matrix fixture. |
| `examples/workloads/krk-gpu-heavy-routing-matrix-alpha.json` | Adds small GPU-heavy KRK matrix fixture. |
| `examples/workloads/krk-cache-heavy-routing-matrix-alpha.json` | Adds small cache-heavy KRK matrix fixture. |
| `examples/workloads/krk-adversarial-routing-matrix-alpha.json` | Adds small adversarial KRK matrix fixture. |

## Change Size

Current diff against `origin/main` before this merge-readiness packet:

- 48 changed files.
- 5,374 insertions.
- 13 deletions.

The merge-readiness packet itself adds four report documents.
