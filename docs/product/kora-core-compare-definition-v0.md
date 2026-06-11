# KORA Core Compare Definition v0

Status: alpha surface definition. This is not a completed command spec.

## Definition

`compare` is the KORA Core workflow for comparing route options, target options, policies, or baselines before execution.

Compare should answer:

> Which execution paths are available, what would each policy select, and what evidence supports the comparison?

## Inputs

Possible future inputs:

- inspected workload.
- route policy.
- baseline policy.
- target registry.
- benchmark profile.
- evidence schema.

## Expected Output

Compare should summarize:

- policies compared.
- route distribution.
- accepted and rejected target classes.
- deterministic/cache/CPU/provider/GPU/fallback counts when measured.
- metrics that are measured.
- metrics that are not measured yet.
- claim boundary.

## Current Alpha Status

Current implementation does not expose a first-class top-level `compare` command.

Current public materials that support future compare work:

- deterministic-heavy benchmark docs.
- KRK routing benchmark methodology.
- KRK extended matrix fixtures.
- KRK performance table package.
- KRK claim boundary table.

## Relationship To KRK

Compare uses KRK route decisions or dry-run route decisions as comparison data.

KRK decides routes. Compare organizes those decisions across baselines, policies, targets, or workload profiles.

## Roadmap

Near-term compare work should:

- compare `all_gpu`, `static_heuristic`, `provider_first_with_gpu_fallback`, and `KRK` policies in dry-run mode.
- keep oracle labels out of router-visible input.
- report measured route metrics only after a runner exists.
- mark unmeasured metrics as not measured.

## Claim Boundary

Compare must not turn dry-run route selectivity into production savings, broad superiority, or provider replacement claims.
