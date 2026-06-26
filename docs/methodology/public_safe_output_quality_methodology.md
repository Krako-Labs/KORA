# Public-Safe Output-Quality Methodology

Status: methodology and future validation design only; no evaluation executed.

## Purpose

This document defines a public-safe methodology for how a later approved KORA goal could evaluate output quality for fixture-derived work.

Goal 105 does not execute evaluation, does not add runtime feature code, and does not add executable automation. It documents how future public-safe fixture-derived checks can separate route-only evidence from output-quality validation without expanding the claim boundary of Goal 103.

## Scope

This methodology applies to public fixture-derived work, especially synthetic fixtures that are already marked:

- `public_safe: true`
- `claim_scope: fixture_only`

The immediate reference fixture is:

- [KORA representativeness seed fixture v0](../../examples/workloads/kora-representativeness-seed-v0.json)

The immediate route-only reference is:

- [Goal 103 representativeness route-only evaluator](../reports/goal103_representativeness_route_only_evaluator.md)

## Route-Only Evidence

Route-only evidence describes how KORA classifies or groups work before any output-quality validation.

Allowed route-only evidence includes:

- route labels.
- route groups.
- shape validation.
- aggregate counters.

Examples from Goal 103 include:

- expected route labels such as `deterministic`, `cache`, `cpu`, `gpu`, `provider_needed`, `retrieval_needed`, `tool_needed`, and `fallback`.
- route groups such as `deterministic_local_route_candidates`, `provider_model_candidates`, `cache_reuse_candidates`, and `fallback_control_candidates`.
- shape validation that confirms required fixture fields, duplicate-id checks, allowed route-label vocabulary, `public_safe: true`, and `claim_scope: fixture_only`.
- aggregate counters over the public-safe seed fixture.

Route-only evidence answers routing and fixture-coverage questions. It does not prove output quality.

## Output-Quality Validation

Output-quality validation is a separate later step. A future approved goal could add public-safe fixture-derived checks only after the fixture includes expected outputs or acceptance criteria that are safe to publish.

Potential check types:

- deterministic expected-output checks for fixed classification, routing, normalization, or validation tasks.
- schema conformance checks for structured outputs.
- exact match where the fixture specifies a single canonical expected value.
- structured-equivalent match where field order, harmless formatting, or equivalent normalized values should not cause failure.
- fixture-level acceptance criteria that define what is checked, what is skipped, and what remains out of scope.
- optional later human review gate, only after explicit approval.
- optional later semantic review gate, only after explicit approval.

A public-safe fixture-derived check should report only bounded fixture-level results. It should avoid raw private inputs, raw provider responses, hidden infrastructure details, or production workload data.

## Fixture Requirements For A Later Goal

A later output-quality scaffold should require each checked item to declare enough public-safe information to make the expected result reviewable:

- stable fixture id.
- public-safe input.
- expected route label, if route behavior is also being checked.
- expected output or expected structured fields.
- check type, such as exact, schema, or structured-equivalent.
- acceptance criteria.
- public-safe rationale.
- explicit `claim_scope: fixture_only`.

Items without public-safe expected outputs should remain route-only or should be skipped by any future output-quality scaffold.

## Reporting Rules For A Later Goal

A future output-quality report should separate at least four result classes:

- route-only items, where only route labels, route groups, shape validation, and aggregate counters are reported.
- deterministic checked items, where expected-output or schema conformance checks were possible.
- skipped items, where public-safe expected outputs or acceptance criteria were not present.
- gated items, where human, semantic, provider, H100, GPU, server, or remote validation would require separate approval.

The report should include denominators for each class, so readers can see the difference between checked fixture items and route-only fixture items.

## What Is Not Allowed In Goal 105

Goal 105 does not allow:

- provider calls.
- H100/GPU/CUDA/server/remote execution.
- model inference.
- live semantic judging.
- human grading results.
- output-quality proof.
- broader workload representativeness proof.
- production workload proof.
- production readiness proof.
- cost-reduction proof.

Goal 105 also does not allow file moves, renames, archival, deletion, release, tag, GitHub Release, PyPI publication, repository settings change, issue creation, project-board creation, raw artifact upload, or local-only project context changes.

## Future-Goal Path

Goal 106 may implement a tiny fixture-based quality-check scaffold only after explicit approval.

A Goal 106 scaffold should remain narrow:

- public-safe fixture-derived checks only.
- no provider calls.
- no model inference.
- no H100/GPU/CUDA/server/remote execution.
- no semantic or human review results unless separately approved.
- no production workload proof.
- no output-quality proof; any later scaffold may report only exact bounded fixture-check results implemented and validated in that future goal.

Any semantic, human, provider, H100, GPU, server, remote, or production-like validation remains separately gated.

## Claim Boundary

This methodology supports future validation design only.

It does not prove output quality, broader workload representativeness, production workload handling, production readiness, production cost reduction, H100/GPU/CPU superiority, customer savings, provider replacement, GPU-serving replacement, or published `getkora`.
