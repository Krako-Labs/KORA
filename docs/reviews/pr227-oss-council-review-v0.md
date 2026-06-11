# PR 227 OSS Council Review v0

Status: internal public-safe review artifact. This document does not approve a release, tag, or automatic merge.

## PR Metadata

| Field | Value |
| --- | --- |
| PR | #227 |
| Title | docs: realign KORA around KRK and KORA Core alpha |
| URL | https://github.com/Krako-Labs/KORA/pull/227 |
| State | OPEN |
| Base | main |
| Head | goal029_krk_kora_core_north_star_realignment |
| Mergeability | MERGEABLE at review time |
| CI | `validate` passed at review time |

## Executive Verdict

ACCEPT with follow-up issues.

PR #227 is a credible public documentation reset. It gives KORA a sharper north star, makes KRK a believable first wedge, and separates current alpha behavior from the KORA Core roadmap clearly enough for public maintainer review.

No BLOCKER was found for a documentation merge. The main risk is not leakage or overclaiming; the main risk is that the branch creates a large conceptual surface before the implementation catches up. That risk is handled by explicit limitations and should become the next implementation work, not a merge blocker.

## OSS Founder Reviewer

Verdict: ACCEPT.

Assessment:

- The north star is sharp: "Make AI workloads routable."
- The Docker analogy is memorable and useful, provided it remains an analogy rather than a parity claim.
- KRK is a credible wedge because it narrows the broad KORA ambition to execution-path routing.
- KORA Core expansion feels natural: KRK decides routes; KORA Core grows into inspect, compare, run, and report.

Strongest part:

- The hierarchy now works: KORA -> KORA Core -> KRK.

Weakest part:

- The repository now carries a large number of new docs. A founder story is clear, but the contributor path may feel heavy without a shorter "start here" path.

Council label:

- SHOULD FIX after merge: add a shorter public "first reader path" that points to README, KRK quickstart, performance table, and KORA Core alpha surface.

## OSS Maintainer Reviewer

Verdict: ACCEPT.

Assessment:

- The docs index is much more useful than before.
- The current-vs-roadmap boundary is mostly clear.
- The examples are useful as fixture seeds, but they are not yet connected to a runner.
- Contributors can understand the strategy, but issue-worthy next tasks are still spread across several docs.

Strongest part:

- The PR packet, boundary audit, inventory, and readiness docs give maintainers enough context to review a large docs branch.

Weakest part:

- The next task list is not centralized as contributor-ready issues.

Council label:

- SHOULD FIX after merge: create issue candidates for matrix evaluator, inspect command, compare dry-run, evidence report generation, and docs link checks.

## Infra Engineer Reviewer

Verdict: ACCEPT.

Assessment:

- Execution-path fragmentation is a real infrastructure pain.
- The deterministic/cache/CPU/provider/GPU/fallback framing is practical.
- The docs correctly avoid pretending that GPU usage itself is the proof.
- The caveat that matrix metrics are not measured yet is important and visible.

Strongest part:

- KRK is framed as route selectivity, not capacity marketing.

Weakest part:

- There is no evaluator yet for the new KRK matrix fixtures, so the strongest infra proof is still future work.

Council label:

- SHOULD FIX after merge: implement the dry-run KRK matrix evaluator and produce route distribution/correctness tables.

## Platform Engineer Reviewer

Verdict: ACCEPT.

Assessment:

- The docs explain that KORA is not a hosted gateway, provider router, model serving stack, or workflow engine replacement.
- The differentiation is strongest when the docs say KRK decides whether an execution path is justified before default model execution.
- The risk is that readers may still compare KORA to existing model routers unless the boundary stays prominent.

Strongest part:

- The "why not hosted gateway now" section is useful and prevents premature product confusion.

Weakest part:

- The claim boundary is strong, but the comparison to adjacent systems could be made more direct in a single related-systems page.

Council label:

- NICE TO HAVE: add a public "KORA vs adjacent systems" note covering model serving, API routing, workflow orchestration, and local runtimes.

## DevRel Reviewer

Verdict: ACCEPT with one important follow-up.

Assessment:

- A developer can understand the core idea in five minutes from the README.
- The README correctly states that KRK primitives are not all top-level CLI commands.
- The docs index is comprehensive, but long.
- Quickstart and capability docs help, but they need a shorter path for new contributors.

Strongest part:

- README hero, current alpha section, and roadmap separation are much clearer.

Weakest part:

- The page now exposes many documents before the developer has a concrete first task.

Council label:

- SHOULD FIX after merge: add a concise "Start with KRK" route for developers with three links and one verified command path.

## Research Reviewer

Verdict: ACCEPT.

Assessment:

- The technical paper draft can become credible if the next experiments are executed.
- The methodology docs correctly separate router-visible metadata from oracle-only labels.
- Current deterministic-heavy evidence is bounded and not overextended.
- Missing metrics are visible: exact route accuracy, acceptable route rate, unsafe misroute rate, cache correctness, fallback rates, and compute-weighted GPU demand.

Strongest part:

- The evidence package distinguishes measured, methodology-only, and not-measured fields.

Weakest part:

- The paper remains a positioning draft until matrix metrics and provider-backed sample validation exist.

Council label:

- SHOULD FIX after merge: prioritize next experiments before calling the paper submission-ready.

## VC / Category Reviewer

Verdict: ACCEPT.

Assessment:

- "Make AI workloads routable" is category-capable language.
- The Docker analogy is useful but should remain carefully bounded.
- KRK is a focused wedge, and KORA Core gives the expansion path.
- The category is plausible because the docs define a workflow, artifacts, registries, and evidence, not just a slogan.

Strongest part:

- Wedge-to-platform path is legible: KRK -> KORA Core -> KORA ecosystem.

Weakest part:

- The market/category story will need working workflow verbs, not only definitions.

Council label:

- SHOULD FIX after merge: demonstrate the first KORA Core inspect/compare path so the category language has a runnable product surface.

## Boundary Auditor

Verdict: ACCEPT.

Assessment:

- No new public-unsafe material was identified in the review docs.
- PR #227 already documents known historical scan matches and separates them from new branch content.
- The changed-file scan from Goal 039 found claim-boundary/prohibited-claim wording and a URL false positive, not private leakage or secrets.
- PR #227 does not rename repos, create repos, tag, release, or merge.

Council label:

- ACCEPT.

## Strongest Parts

- Clear north star: make AI workloads routable.
- KRK is a focused technical wedge.
- KORA Core expansion is coherent.
- README avoids presenting future workflow verbs as implemented.
- Evidence docs mark missing measurements explicitly.
- PR packet and merge readiness docs make the large branch reviewable.
- Claim boundary is repeated in the right places.

## Weakest Parts

- The branch is documentation-heavy and can feel large for first-time contributors.
- New matrix fixtures do not yet have an evaluator.
- KORA Core workflow verbs are still mostly definitions.
- The technical paper draft needs more measured route-selectivity evidence.
- Historical repo docs still create noisy broad-scan output.

## Must-Fix Before Merge

No MUST FIX item was found.

## Blockers

No BLOCKER item was found.

## Should-Fix After Merge

- Add a short "Start with KRK" reader path.
- Create contributor-ready issues for matrix evaluator and KORA Core inspect/compare.
- Implement the KRK matrix dry-run evaluator.
- Generate route distribution and correctness tables.
- Add a small related-systems comparison note.
- Keep historical scan cleanup as a separate scoped hygiene task.

## Nice-To-Have

- Add a diagram or table that maps KRK primitives to current CLI commands and roadmap commands.
- Add a single "What is implemented today?" page.
- Add doc link checking in CI.
- Add reviewer-oriented examples for the four matrix workload fixtures.

## Naming Risks

NICE TO HAVE:

- KORA, KORA Core, and KRK are now internally consistent, but new readers may still need a one-screen glossary.

ACCEPT:

- Krako is treated as separate future infrastructure context, not as a public OSS claim.

## README Risks

SHOULD FIX:

- The README is clearer, but it still has a lot of setup and historical context. A shorter first-run route would improve developer conversion.

ACCEPT:

- The README correctly says current KRK primitives are not all top-level CLI commands.

## Claim Risks

ACCEPT:

- The branch keeps evidence bounded to the deterministic-heavy benchmark and does not turn it into production proof.

SHOULD FIX:

- Keep future docs from restating prohibited claims too often; prefer short boundary language to reduce scan noise.

## Evidence Risks

SHOULD FIX:

- The biggest evidence gap is executable route-selectivity evaluation for the KRK matrix fixtures.

ACCEPT:

- Current evidence docs label unmeasured items clearly.

## Developer Adoption Risks

SHOULD FIX:

- The docs need a tighter beginner path from README to first verified command to evidence review.

NICE TO HAVE:

- Add good-first-issue candidates tied directly to the new docs.

## Final Recommendation

ACCEPT for merge after maintainer review.

Recommended next goal:

- Goal 041 - Merge PR #227, if the owner wants to accept this docs package now.

Alternative next goal:

- Goal 041 - Apply PR #227 Review Fixes, if the owner wants the "Start with KRK" path and contributor issue list before merge.
