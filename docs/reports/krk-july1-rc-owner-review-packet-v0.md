# KRK July 1 RC Owner Review Packet v0

Status: owner review packet refreshed for RC decision package.

## Executive Recommendation

Recommendation: GO WITH CAVEATS for the KRK July 1 RC.

The package is ready to be framed as a bounded KRK release-candidate package focused on deterministic-first routing, deterministic-heavy evidence, dry-run route-selectivity metrics over four public matrix profiles, bounded H100-routed subset measurement, bounded provider-routed validation, and explicit caveats.

The package is not ready to be framed as production proof, a broad KORA Core implementation release, production savings proof, customer savings proof, broad workload superiority proof, H100 superiority proof, provider superiority proof, or replacement proof for existing model serving/provider routing systems.

## Decision Options

### A. GO

Use only if the owner accepts the current bounded evidence package without caveats. Not recommended because runtime-integrated route-selectivity, broad workload representativeness, and output-quality validation are still missing.

### B. GO WITH CAVEATS

Recommended.

Rationale:

- route-selectivity metrics now exist for four public dry-run matrix profiles.
- generated JSON and Markdown evidence outputs are committed.
- deterministic-heavy evidence remains available and bounded.
- bounded H100-routed subset evidence exists for four GPU-selected public matrix items.
- bounded provider-routed validation exists for three provider-selected public matrix items.
- remaining gaps are explicit rather than hidden.

### C. NO-GO

Choose this if the desired RC must include production workload proof, customer proof, runtime-integrated route-selectivity, broader workload representativeness, output-quality validation, production readiness, or savings claims.

## What Is Ready

- KRK product definition.
- KRK quickstart and architecture docs.
- deterministic-heavy benchmark evidence.
- four public KRK matrix fixtures.
- dry-run route-selectivity metrics for mixed-realistic, GPU-heavy, cache-heavy, and adversarial profiles.
- bounded H100-routed subset measurement for the public matrix GPU-selected items.
- bounded provider-routed validation for the public matrix provider-selected items.
- JSON and Markdown generated evidence outputs.
- public/private and claim-boundary docs.

## What Is Not Ready

- runtime-integrated route-selectivity workflow.
- broad workload representativeness.
- output quality validation.
- final technical paper polish.
- contributor-facing preview issue set.

## Must Fix Before July 1

- Keep README and evidence docs aligned with the narrowed RC scope.
- Ensure all generated JSON files parse.
- Keep route-selectivity wording explicitly dry-run and fixture-scoped.
- Keep H100 and provider evidence wording subset-bounded.
- Re-run full tests and boundary scans before any PR or public announcement.

## Should Fix Before July 1

- Add a one-command regeneration wrapper for matrix outputs.
- Add a contributor-friendly issue list for the next evidence gaps.
- Refresh the technical paper draft with the route-selectivity results.
- Refresh the technical paper draft with bounded H100 and provider validation evidence.

## Can Wait Until After July 1

- broader service-replay profile.
- larger H100/provider samples.
- output-quality validation.
- KORA Core inspect/compare/run/report implementation.

## Claim Boundary

The owner decision should not imply production readiness, savings, infrastructure reduction, provider superiority, GPU superiority, broad workload superiority, customer proof, or replacement of existing model serving/provider routing systems.

## Owner Approval Checklist

- [ ] Approve GO WITH CAVEATS for the July 1 RC.
- [ ] Confirm no release or tag is approved by this package.
- [ ] Confirm public wording uses the claim package only.
- [ ] Confirm runtime-integrated, broader workload, and output-quality gaps remain visible.
- [ ] Confirm Goal 053 should handle PR readiness before any push or PR.
