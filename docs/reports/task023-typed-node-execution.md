# Task 023: Typed Node Execution and Local Benchmark Foundation

Classification: **needs-cto-review**. Implemented and locally validated in a
separate worktree. Prepared for a review-only PR; merge is a separate gate.

Base: `4e5795c5e0c2c6732c878d30d057b7992c903027`.

## Change and reason

A graph-wide runtime cannot hand a typed intermediate result to a separately
selected runtime. This change adds an explicit, integrity-bound node plan and
a Host-owned coordinator using the existing trusted runtime interface.
No workflow-specific behavior is added to KORA Core.

The local benchmark collector persists actual elapsed times and exact fixture
quality checks. Model token/TTFT fields are null; it cannot establish model
performance or cross-hardware speed.

## Scope

- Host/validator integration and optional manifest property.
- Versioned node plan, node evidence and bounded local benchmark schemas.
- Coordinator with per-node schema checks, ancestor bindings, immutable plan
  copies, preselection and registry revalidation.
- Two-node synthetic fixture and focused failure-path tests.
- Reproduction instructions and three scenario specifications.

Existing packages retain their legacy semantics. No persistent workers, network
execution, inference, remote dispatch, UI, durable reuse, external corpus binding
or domain-specific Core code is added.

## Validation

- Full regression: **705 passed** in 21.13 seconds.
- Focused node/benchmark tests: **26 passed** in 2.28 seconds.
- Preregistered comparison fixture checks: **2 passed**.
- Offline release smoke: passed (no release performed).
- Ruff check: new coordinator, collector and focused tests passed.
- Isolated non-editable source installation: **6 checks passed**.
- Installed-package smoke from outside the checkout: two distinct trusted
  deterministic runtime identities; three runs passed exact output checks.
- Local smoke timing is fixture evidence only, not an inference benchmark.

Tests cover invalid contracts, missing/invalid bindings, type mismatches,
approval rejection, ambiguous runtimes, package tampering, registry tampering
between nodes, failed-node downstream suppression, persisted evidence corruption,
literal binding values and non-successful quality checks.

## Approval packet and self-review

Risk: medium, because this adds opt-in execution semantics and a new evidence
contract. Classification is needs-cto-review even though automated checks pass.
The compatibility decision is explicit rejection by older strict validators;
existing packages are unchanged.

Implementation/repair loop: initial coordinator tests, contract/accessor
hardening, then benchmark and failure-path checks. Formatting was repaired in
new files. No failed behavioral test required a semantic repair. Full
regressions progressed from 694 to 703, then 705 after the preregistered
comparison fixtures were added.
Source-install and installed smoke passed.

This is trusted synchronous execution, not sandboxing. There is no timeout,
transaction rollback, crash recovery or durable resume. On partial failure,
node evidence records successful upstream work; the legacy aggregate result is
not a partial-completion ledger. Read the detailed
[contract](../typed-node-execution.md) before extending the coordinator.

No claim of production readiness, semantic output quality, cost savings,
H100 parity, model capacity or GPU superiority follows. No provider/model/GPU
execution, release, tag, package publication, repository-settings change,
tracker mutation or merge was performed. Raw local benchmark evidence is kept
outside the public source tree.

The common model/artifact identities, six synthetic comparison cases and
measurement settings are now frozen in examples/benchmarks/three-environment.
Their execution support remains unverified. Next bounded work: review this node
contract before the separate worker/remote execution slice. The latter must introduce truthful activity/evidence contracts
rather than changing the current false-only activity fields silently.
