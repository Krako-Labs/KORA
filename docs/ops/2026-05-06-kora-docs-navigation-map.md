# KORA Docs Navigation Map

Date: `2026-05-06`

## 1. Purpose

This is a maintainer-facing navigation map derived from the repository hygiene audit.

It exists to help maintainers improve documentation discoverability without deleting, moving, or renaming files before review.

Primary source:

- [KORA Repository Hygiene And File Organization Audit](2026-05-06-kora-repository-hygiene-audit.md)

## 2. Current Docs Folder Map

| Folder path | Purpose | Audience | Evidence value | Cleanup risk | Recommended next action |
|---|---|---|---|---|---|
| `docs/claims` | Canonical claim registry and public language | maintainers, community, public writers, investors/EIC/partners | High | Low if treated as canonical | Link from README, reports, community docs |
| `docs/community` | Public-safe community workflow, open roles, and AI-assisted contribution guidance | contributors and maintainers | High | Low/medium due overlap with ops docs | Add community index later |
| `docs/ops` | Operating system, migration, GitHub setup, audits | maintainers, operators | High | Medium due many dated docs | Add ops index later; keep dated history |
| `docs/paper` | Paper authorship and contribution policy | researchers, contributors, paper readers | High | Low now; likely to grow | Add paper index before more paper docs |
| `docs/benchmarks` | Benchmark summaries and workload plans | developers, researchers, reviewers | High | Medium due overlap with reports/experiments README | Add benchmark index and canonical evidence path |
| `docs/reports` | Readiness, release, policy, and validation reports | maintainers, reviewers, diligence readers | High | Medium due mixed report types | Add reports index; preserve all release evidence |
| `docs/status` | Earlier status closeout reports | maintainers, internal continuity | Medium/high | Medium due overlap with reports | Decide later whether status closeout stays separate |
| `docs/specs` | Architecture, contracts, governance, studio specs | technical maintainers, architects | High | Medium due broad Krako/studio scope | Add specs index and status notes |
| `docs/vision` | Category thesis and future vision docs | public readers, investors/EIC, community | High | Low | Link from README and claim docs |
| `docs/metrics` | Metrics reports and CSV artifacts | technical reviewers, benchmark reviewers | Medium/high | Medium due overlap with artifacts/metrics | Review artifact policy and source-of-truth |
| `docs/progress` | Historical progress reports | maintainers, continuity | Medium | Medium if duplicated with status closeout/reports | Preserve; index later |
| `docs/strategy` | Strategy and pitch source material | maintainers, investor/EIC prep | Medium/high | High if private strategy accumulates publicly | Review public/private boundary before linking broadly |
| root-level `docs/*.md` | Foundational docs, architecture, philosophy, benchmark, research | developers, researchers, public readers | High | Medium due flat structure and duplicate root docs | Index first; move only after review |

## 3. Navigation Principles

- Do not delete evidence docs casually.
- Prefer linking before moving.
- Prefer dated audit docs for operational history.
- Public-facing docs should be easy to find.
- Internal-facing docs should be clearly marked if needed.
- Claim-sensitive docs must link to the [claim registry](../claims/kora-claim-registry.md).
- Historical docs can remain valuable even when superseded.

## 4. Link Improvement Candidates

- Root `README.md` should link to `docs/README.md`.
- `CONTRIBUTING.md` should link to open roles and the AI-assisted contribution guide.
- Community docs should link to the claim registry.
- Paper docs should link to the authorship policy.
- Ops docs should link to the GitHub setup plan.
- Benchmark docs should link to the approved benchmark claim.
- Release/readiness reports should link to the claim registry rather than repeating claim boundaries in isolation.
- `experiments/README.md` should link to benchmark summaries and artifact policy.
- `docs/README.md` should remain the public navigation entrypoint.

## 5. Cleanup Candidate Staging

### Safe Link-Only Changes

- Add README link to docs index.
- Add links from contributor docs to community/open roles docs.
- Add links from benchmark docs to benchmark artifact policy.
- Add links from reports to claim registry.
- Add links from ops docs to manual setup checklist and hygiene audit.

### Needs Review Before Move/Rename

- Root strategic docs such as `VISION.md`, `ROADMAP.md`, `GOVERNANCE.md`, and `EXECUTIVE-SUMMARY.md`.
- Root appendix files.
- Older root-level docs duplicated under `docs/`.
- status closeout files split across `docs/status` and `docs/reports`.
- Strategy files under root and `docs/strategy`.

### Archive Candidates

- Legacy pitch source copies after public/private review.
- Older progress/status closeout drafts after a history index exists.
- Superseded planning docs after canonical links are created.

### Removal Candidates Requiring Explicit Approval

- Generated artifacts that are not selected evidence.
- Obsolete duplicate docs after preservation and redirects/links are in place.
- Unused scripts only after technical ownership review.

## 6. Recommended Next Tasks

- Task 135: add README link to docs index and safe cross-links.
- Task 136: create PR template and CODEOWNERS draft.
- Task 137: private community operations material.
- Task 138: GitHub manual setup execution log.
