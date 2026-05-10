# KORA Contributor Pathway

## Purpose

This document helps developers, technical reviewers, and AI app builders find the right way to participate in KORA.

KORA is an open-source execution-control layer for AI workloads. The best early contributions make the public docs, examples, tests, validation paths, and synthetic workload specs easier to understand and verify.

## Who This Is For

- AI app developers
- infrastructure engineers
- Python developers
- documentation contributors
- benchmark/workload contributors
- technical reviewers

## Where To Start

1. Read the [README](../../README.md).
2. Run the local examples.
3. Review the [local validation reviewer packet](../benchmarks/local-validation-reviewer-packet.md).
4. Pick a small contribution.
5. Open an issue or PR.
6. Propose a workload through the recommended discussion route once enabled.

## Communication Routes

- Questions: GitHub Discussions Q&A, once enabled.
- Workload proposals: GitHub Discussions Workload Proposals, once enabled.
- Bugs: GitHub Issues.
- Security issues: follow [SECURITY.md](../../SECURITY.md).
- PRs: small, scoped pull requests.

For current route guidance, see [Contact and Discussion Routes](contact-and-discussion-routes.md).

## Good First Contribution Areas

- documentation polish
- examples
- tests
- synthetic workload specs
- validation report templates
- README clarity
- reviewer packet improvements
- local/no-network validation docs
- KORA Studio planning docs and mock data only

## What Not To Start With

- real provider adapters
- API cost claims
- production cost claims
- benchmark claim rewrites
- release/tag/version work
- repository settings
- security-sensitive changes
- large architecture rewrites
- private internals/campaign docs

## Public/Private Boundary

The public KORA repository contains technical truth, docs, examples, tests, validation paths, issue templates, and public contribution guidance.

The private internals repository contains internal messaging, community coordination, social planning, launch operations, and other non-public operating material.

Contributors should not add private campaign materials or internal workflow notes to public KORA. Keep public docs focused on technical behavior, reproducible examples, contribution guidance, and claim-safe validation language.

## Claim Safety

Approved public alpha claim:

> KORA reduced model invocations by 80% in a reproducible deterministic-heavy benchmark workload.

Local validation wording:

> KORA's local no-network validation examples show that KORA can measure avoided model-call events in synthetic workloads.

Explicit non-claims:

- no production cost reduction proof
- no real API-cost reduction proof
- no production benchmark proof
- no full runtime-integrated real-provider benchmark evidence
- no broad workload superiority proof
- no energy reduction evidence
- no formal government validation
- no signed partner validation unless actually signed and documented
- no guaranteed adoption or funding

## Contribution Size

Prefer small PRs. A good first PR usually changes one concern, touches a small number of files, and is easy to verify.

Include tests or docs when they are relevant. Avoid bundling unrelated changes such as documentation cleanup, runtime behavior, formatting, and benchmark wording in the same PR.

## Review Expectations

Reviewers will expect:

- CI/tests should pass.
- No secrets.
- No raw provider responses.
- No private data.
- No unsupported claims.
- Public/private boundary respected.

## KORA Studio Participation

KORA Studio work should be decomposed into small issues before implementation. Useful early tasks are planning, static fixtures, and local-only prototypes, such as:

- validation report viewer
- sample JSON fixtures
- static UI mockups
- local dashboard prototype
- report packet viewer
- no real provider integration at first

This is future planning. It is not a claim that KORA Studio already exists as a product.

### What is a deterministic route?

A deterministic route is a path where KORA can handle a request through structured logic, policy rules, validation, or templating — without calling a model.

Examples include FAQ responses, policy lookups, structured validation, report formatting, and simple routing decisions.

If a request cannot be safely handled through a deterministic path, KORA can escalate it to a model-call path.
