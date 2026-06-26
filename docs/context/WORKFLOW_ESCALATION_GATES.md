# implementation workflow Escalation Gates

Status: approval boundaries for KORA implementation workflow work.

## implementation workflow May Do Without Additional Approval

When the task brief authorizes a bounded public-safe work block, the implementation workflow may:

- implement within allowed files.
- add or update tests.
- add validators.
- make small repairs within allowed scope.
- update docs, reports, and breadcrumbs.
- rerun validation commands.
- perform self-review.
- create an approval packet.
- open a PR and stop.

## implementation workflow Must Stop For Approval

the implementation workflow must stop for explicit Albert approval before:

- merge.
- release, tag, GitHub Release, release asset, or PyPI publication.
- repository settings or metadata changes.
- GitHub issues, project boards, or collaborator changes.
- provider calls.
- H100/GPU/CUDA/server/remote execution.
- model inference.
- semantic judging or human grading.
- production validation.
- public claim expansion.
- major file movement, archive, delete, or rename.
- large public-facing document replacement.
- local-only project context changes.
- auto-merge, self-merging agent, scheduler, daemon, background runner, GitHub Actions workflow, remote runner, provider-calling runner, or H100 runner.

## Stop Classifications

- Use `needs-cto-review` when approval is needed for a risky but reviewable direction.
- Use `blocked` when the task cannot proceed safely without external approval or missing information.

## Claim Boundary Reminder

Escalation gates protect KORA against unsupported claims: no output-quality proof, broader workload representativeness proof, production proof, production cost reduction, customer savings, H100/GPU/CPU superiority, provider replacement, GPU-serving replacement, or published `getkora` claim without separate approval and evidence.
