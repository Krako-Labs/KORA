# KORA Public Language Guide

## Purpose

This is a practical copywriting guide for public KORA communication.

Use it with `docs/claims/kora-claim-registry.md` when drafting README copy, GitHub Discussions, social posts, Telegram updates, investor/EIC language, partner outreach, and paper-related text.

## Approved Short Descriptions

README:

> Most AI apps call the model too soon. KORA is an open-source AI Execution Control Layer that routes work before model inference.

GitHub Discussions:

> KORA helps developers put execution control before inference: task graphs, deterministic-first execution, validation, telemetry, and model escalation only when needed.

X/Twitter:

> Most AI apps call the model too soon. KORA changes the default. Structure first. Inference second.

LinkedIn:

> KORA is an open-source execution-control layer for AI workloads. It turns requests into task graphs, runs deterministic work first, validates the path, records telemetry, and escalates to a model only when needed.

Telegram:

> KORA is open-source execution control for AI workloads. Clone the repo, run the alpha, inspect the path, and bring a workload: https://github.com/Krako-Labs/KORA

Investor intro:

> KORA is building open-source execution control for AI workloads: infrastructure that turns requests into task graphs, routes deterministic work before model invocation, and preserves validation and telemetry before inference escalation.

EIC/grant intro:

> KORA is an open-source AI infrastructure project focused on execution control before inference escalation, with bounded public alpha evidence and a roadmap toward runtime-integrated real model-call evaluation.

Partner intro:

> KORA explores how AI systems can control execution before inference escalation through task graphs, deterministic-first execution, validation, fallback, and telemetry.

Paper intro:

> KORA studies execution control for AI systems by converting requests into task graphs, routing deterministic work before model invocation, and preserving validation and telemetry for reproducible evaluation.

## Approved Migration Note

> KORA has moved into its official Krako Labs home at https://github.com/Krako-Labs/KORA.

> Same code, same history, bigger mission.

Do not make Krako the main README narrative. In the KORA README, Krako belongs near the bottom in an Ecosystem / Related Projects section.

## Approved Benchmark Wording

Short version:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

Technical version:

> On `experiments/workloads/deterministic_heavy_v1_100.json`, generated from seed `42`, the direct-baseline mode counted 100 simulated model invocations while KORA-controlled mode counted 20. Deterministic outputs checked: 80. Mismatches: 0. Fallback/model-candidate skipped: 20.

Social media version:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload. This is alpha benchmark evidence, not a production claim.

Paper-safe version:

> KORA reduced model invocations by 80% in the current reproducible deterministic-heavy benchmark workload, with 80 deterministic outputs checked and 0 mismatches.

Investor/EIC-safe version:

> KORA's current public evidence is a reproducible deterministic-heavy benchmark workload where model invocations were reduced by 80%. The next evidence track is runtime-integrated validation with real model calls.

## Three Additional Bounded Evaluation Summaries (2026-10-28)

Only these three categories may be quoted from the bounded research update: **KECB v0.6**, **50,000 counted offline checks/events**, and **CacheEval**. Keep the exact task definition, denominator, baseline parity, and source limitations next to numerical figures.

Use [the detailed evaluation note](../benchmarks/kora-bounded-evaluation-results.md) and [claim registry](kora-claim-registry.md) before using them in posts or slides. These are author-reported private research results, not independently published and reproduced benchmark artifacts.

## Prohibited Rewrites

Do not rewrite:

- "KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload" as "KORA reduces production AI costs by 80%."
- "80 of 100 simulated model invocations avoided" as "80% cost reduction."
- "simulated model invocation" as "real API call."
- "benchmark workload" as "production workload."
- "interest" as "partnership."
- "planned validation" as "validated."

## Next Possible Claim

Future conditional language after runtime-integrated real model-call validation:

> KORA reduced measured model invocations by X% in a runtime-integrated benchmark using real model calls.

Do not use this as a current claim. It requires merged evidence, documented methodology, validation commands, reviewed results, and claim-registry approval.

## Public Contributor Role Boundary Language

Approved language:

> These are unpaid early open-source contributor roles, not employment positions.

> Future paid roles, grants, internships, or contributor programs may be considered if funding becomes available, but they are not guaranteed.

## Partner / Government / Institution Language

Allowed:

- early interest
- exploratory discussion
- potential pilot candidate
- LOI candidate

Forbidden unless documented and approved:

- validated by
- partnered with
- officially backed by
- government-approved

## Paper / Publication Language

Verified public preprint:

> KORA's research paper, *KORA: Deterministic-First Execution Control for AI Workloads*, is available as an [arXiv preprint (2610.35869)](https://arxiv.org/abs/2610.35869).

Use **"arXiv preprint"** or **"publicly available research paper"**. The paper reports bounded simulated-invocation reduction on a deterministic-heavy workload and synthetic local/no-network validation; these are not production savings or quality claims.

Do not say "peer-reviewed", "accepted conference paper", "independently validated", or "formal artifact-evaluated" without separate evidence and approval.

Before quoting the paper's correctness figures as independently replicated by repository benchmark scripts, follow the [evidence alignment notes](../research-paper.md).

## Example LLM Prompt For Safe KORA Writing

```text
You are writing public KORA content.

Use these approved one-liners:
- Most AI apps call the model too soon.
- KORA is an open-source execution-control layer that turns AI requests into structured execution paths before inference.
- KORA routes deterministic work away from unnecessary model invocation through task graphs, validation, fallback, and telemetry.

Preserve this benchmark wording exactly unless asked to omit the benchmark:
"KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload."

Do not rewrite simulated benchmark evidence as production evidence, cost reduction, real API-cost reduction, energy reduction, partner validation, government validation, investor commitment, or publication proof.

If a draft mentions numbers, partners, grants, investors, institutions, papers, or adoption, mark it for maintainer review.

If evidence is missing, write "needs review" instead of inventing support.
```
