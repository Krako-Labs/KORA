# Group 110 Codex Inner Loop Ownership

Status: implemented with local validation passing and PR open.

## Objective

Group 110 creates the repo-grounded operating layer that lets Codex own the inner development loop for future bounded KORA work blocks.

This group adds operating docs, a queue, a self-review protocol, risk classification, escalation gates, approval packet rules, a multi-agent operating model, a reusable run report template, and a dependency-free validator with focused tests.

## Why This Replaces Micro-Task Orchestration

Earlier KORA work often depended on Albert or ChatGPT to schedule each small implementation step. Group 110 shifts ordinary bounded work into a repo-local Codex loop: read instructions, choose a bounded queue item when approved, implement, validate, repair safely, self-review, classify risk, produce an approval packet, open a PR, and stop.

## Why ChatGPT Should Not Be The Inner-Loop Planner

ChatGPT can provide approval gates, strategic direction, and escalation decisions, but the repo itself should hold the operating rules needed for day-to-day bounded implementation. Repo-local docs reduce drift, make expectations reviewable in PRs, and let Codex ground future work in versioned instructions rather than private chat history.

## Files Added

- `AGENTS.md`
- `docs/context/CODEX_INNER_LOOP_QUEUE.md`
- `docs/context/CODEX_SELF_REVIEW_PROTOCOL.md`
- `docs/context/CODEX_RISK_CLASSIFICATION.md`
- `docs/context/CODEX_ESCALATION_GATES.md`
- `docs/context/CODEX_APPROVAL_PACKET.md`
- `docs/context/CODEX_MULTI_AGENT_OPERATING_MODEL.md`
- `docs/reports/codex_inner_loop_run_template.md`
- `scripts/validate_codex_inner_loop_docs.py`
- `tests/test_codex_inner_loop_docs.py`
- `docs/reports/group110_codex_inner_loop_ownership.md`

## Files Updated

- `OPEN_THIS_FIRST.md`
- `REVIEW_HUB.md`
- `docs/README.md`
- `docs/context/NEXT_GOAL_QUEUE.md`

## Queue Summary

The new queue includes seven future public-safe work blocks:

- `CIL-001` bounded validation report verifier.
- `CIL-002` bounded validation failure classifier.
- `CIL-003` bounded validation profile registry.
- `CIL-004` first-run CLI smoke validation expansion.
- `CIL-005` source-install readiness check.
- `CIL-006` PR approval packet checker.
- `CIL-007` report consistency checker.

Each queue item records objective, risk level, allowed files, forbidden files/actions, validation commands, repair limits, expected outputs, stop gates, claim boundaries, and expected completion status.

## Self-Review Protocol Summary

The self-review protocol requires checks for changed files vs allowed scope, forbidden paths/actions, validation results, report consistency, breadcrumb consistency, local-only ChatGPT context, provider/H100/server/model/semantic/human/production gates, release/repo-setting gates, uncertainty notes, and final classification.

Final classifications are:

- `merge-ready`
- `needs-r1`
- `needs-cto-review`
- `blocked`

## Risk Classification Summary

Risk levels are:

- low risk: validators, tests, local runners/verifiers, report templates, breadcrumbs, internal runbooks, approval packet checkers.
- medium risk: minor README updates, examples guide updates, install guide improvements, user-facing CLI message changes, validation profile registry changes.
- high risk: public positioning changes, claim expansion, benchmark interpretation, H100/provider/server execution, release/PyPI publication, major public docs rewrite, file movement, repo settings, external side effects, actual multi-agent execution, auto-merge.

## Escalation Gate Summary

Codex may implement within allowed files, test, validate, make small repairs, update reports/breadcrumbs, self-review, create an approval packet, open a PR, and stop.

Codex must stop for merge, release/tag/GitHub Release/PyPI, repo settings, issues/project boards/collaborators, provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, production validation, public claim expansion, major file movement, large public-facing document replacement, local-only ChatGPT context changes, or background/auto-merge automation.

## Approval Packet Summary

The approval packet requires decision needed, risk level, final status classification, changed files, validation summary, repair attempts, failures encountered, self-review summary, claim-boundary audit, forbidden-action audit, uncertainty notes, Codex recommendation, and Albert action options: Merge / Request R1 / Stop / CTO Review.

## Multi-Agent Operating Model Summary

The multi-agent operating model is rules-only and does not create automation. It requires one writer per branch, read-only reviewer/checker agents by default, separate worktrees/branches/non-overlapping files for multiple builders, human-gated integrator/merge role, no auto-merge, and escalation to `needs-cto-review` or `blocked` for high-risk findings.

## Validator Behavior

`scripts/validate_codex_inner_loop_docs.py` is dependency-free and checks:

- required operating docs exist.
- queue doc includes at least six task ids.
- self-review protocol includes the four final classifications.
- risk classification includes low, medium, and high.
- escalation gates include required approval gates.
- approval packet includes Albert action options.
- multi-agent model includes one-writer-per-branch and read-only reviewer rules.
- run template includes loop count, repair attempts, validation results, and final classification.
- required docs include claim-boundary language.
- required docs do not contain hidden/bidi/control Unicode beyond normal LF/tab.

## Validation Results

| Command | Result |
| --- | --- |
| `python3 scripts/validate_codex_inner_loop_docs.py` | passed |
| `python3 -m pytest tests/test_codex_inner_loop_docs.py` | passed, `8 passed` |
| `python3 scripts/run_bounded_local_validation.py --profile kora-local-core --dry-run` | passed |
| `python3 scripts/check_markdown_links_goal082b.py` | passed |
| `git diff --check` | passed |
| `python3 -m pytest` | passed, `426 passed` |

Expected full-suite baseline after Goal 109 was `418 passed`; Group 110 observes `426 passed` after adding 8 validator tests.

## Loop Count And Repairs

- loop count: `1`.
- repair attempts: `0`.
- failures encountered: none.
- fixes applied: none.

## Final Status

- PR: `https://github.com/Krako-Labs/KORA/pull/262`
- branch: `codex/group110-codex-inner-loop-operating-layer`
- risk level: medium.
- final status classification: `needs-cto-review`.

Reason: this group is documentation/protocol and validator work only, but it changes the repo-local operating model for future Codex autonomy. Passing validation is not enough to mark this as merge-ready without owner/CTO review of the operating model.

## Claim Boundaries

Group 110 does not claim:

- output-quality proof.
- broader workload representativeness proof.
- production proof.
- production cost reduction.
- customer savings.
- H100/GPU/CPU superiority.
- provider replacement or GPU-serving replacement.
- that `getkora` is published.

This group creates repo-grounded Codex inner-loop operating guidance. It does not create production automation, auto-merge, background execution, provider calls, H100/server execution, multi-agent execution, or claim expansion.

## Approval Packet

- decision needed: review whether the repo-local Codex inner-loop operating model should be merged.
- risk level: medium.
- final status classification: `needs-cto-review`.
- changed files: listed above.
- validation summary: validator passed; focused validator tests passed with `8 passed`; dry-run bounded local validation runner passed; markdown links passed; `git diff --check` passed; full pytest passed with `426 passed`.
- repair attempts: `0`.
- failures encountered: none.
- self-review summary: scope is docs/protocol plus validator/tests; no runtime automation or external execution added.
- claim-boundary audit: no output-quality proof, broader workload representativeness proof, production proof, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, or published `getkora` claim added.
- forbidden-action audit: no merge, release, tag, GitHub Release, PyPI publication, issues, project boards, repo settings, collaborator changes, provider calls, H100/GPU/CUDA/server/remote execution, model inference, semantic judging, human grading, production validation, file movement, local-only ChatGPT context changes, scheduler, daemon, background runner, GitHub Actions workflow, remote runner, provider-calling runner, H100 runner, self-merging agent, or actual multi-agent execution.
- uncertainty notes: the operating model affects future Codex autonomy and should be reviewed by Albert/CTO before merge.
- Codex recommendation: CTO Review.
- Albert action options: Merge / Request R1 / Stop / CTO Review.

## Next Recommended Work Block

After review/merge, the next recommended work block is to run `CIL-001` or reconcile it with any existing bounded validation report verifier PR if one is already open. Do not start follow-on work without explicit approval.

## R1 Byte-Level Normalization

R1 normalized the Group 110 changed files for strict ASCII/LF content:

- UTF-8 text.
- LF line endings only.
- no CR.
- no BOM.
- no NUL.
- no C0/C1 control characters except LF and horizontal tab.
- no bidirectional formatting characters.
- no hidden Unicode separators.

The cleanup changed punctuation only in `OPEN_THIS_FIRST.md` and `docs/README.md`. Group 110 substance, risk classification, approval packet, self-review protocol, escalation gates, multi-agent operating model, and claim boundaries are unchanged.
