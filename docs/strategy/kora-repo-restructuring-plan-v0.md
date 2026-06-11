# KORA Repo Restructuring Plan v0

Status: planning document. This document does not rename, split, create, push, or configure repositories.

## Purpose

This plan describes possible post-July repository structures for KORA. It is a decision framework, not an execution request.

## Current Structure

Current public structure:

- `KORA`: main public repository.
- Current implementation: KRK-oriented alpha.
- Current docs: KORA umbrella, KORA Core, KRK, workload spec, target registry, evidence docs, examples, and paper prep.

Current strengths:

- one repo is easy to clone.
- docs, examples, tests, and code are close together.
- early contributors can run one setup path.
- current KRK evidence can remain tied to the implementation that produced it.

Current friction:

- KORA, KORA Core, KRK, Studio planning, paper docs, and old alpha materials all live together.
- the repo can look broader than the implemented surface.
- future workload and registry artifacts may outgrow one repo.

## Future Structure Options

### Option A: Single Repo

Keep everything in `KORA`.

Possible layout:

```text
KORA/
  kora/
  examples/
  docs/
  tests/
  experiments/
```

Pros:

- easiest for early adoption.
- simplest issue tracker and contribution path.
- fewer release and dependency coordination problems.
- best while implementation and naming are still stabilizing.

Cons:

- docs can become crowded.
- KRK, KORA Core, examples, registries, and Studio planning can blur together.
- future high-volume workloads or registry entries may bloat the repo.

### Option B: Umbrella + Core

Use one umbrella/community repo and one core implementation repo.

Possible future layout:

```text
kora/
kora-core/
```

Where:

- `kora` holds umbrella docs, community, roadmap, governance, and registry indexes.
- `kora-core` holds KORA Core implementation, KRK, CLI, tests, and core examples.

Pros:

- clearer movement versus implementation boundary.
- easier to keep KORA Core implementation focused.
- community docs can grow without crowding the code repo.

Cons:

- requires migration work.
- splits issues, docs, and release attention.
- may be premature before KORA Core commands are stable.
- can confuse early adopters if split before the product surface is clear.

### Option C: Umbrella + Core + Workloads

Use separate repos for umbrella docs, core implementation, and workload/evidence fixtures.

Possible future layout:

```text
kora/
kora-core/
kora-workloads/
```

Possible later additions:

```text
kora-target-registry/
kora-evidence-registry/
```

Pros:

- workload fixtures can scale independently.
- registries can have their own governance and review rules.
- core implementation stays small.
- evidence packages can be reviewed without changing engine code.

Cons:

- too much overhead for the current alpha.
- requires strong contribution workflows.
- can fragment a young community.
- cross-repo tests and releases become harder.

## Recommended Approach

Recommended path:

1. Stay single-repo through the current KRK and KORA Core alpha cycle.
2. Cleanly organize docs and package boundaries inside the current repo.
3. Prepare for "umbrella + core" only after KORA Core has tested inspect/compare/run/report surfaces.
4. Add a separate workload or registry repo only when fixture volume, review process, or release cadence makes it necessary.

Short version:

> Keep one repo now. Prepare for umbrella + core later. Delay workload and registry repos until the community and artifact volume justify them.

## Proposed Internal Structure Before Any Split

Within the current repo, make the boundaries visible:

```text
docs/strategy/
docs/product/
docs/architecture/
docs/evidence/
docs/paper/
examples/
experiments/
kora/
tests/
```

Future internal namespaces may include:

```text
kora/krk/
kora/core/
kora/workloads/
kora/targets/
kora/evidence/
```

These should be introduced only with implementation work and tests.

## Developer Adoption Path

The adoption path should stay simple:

1. clone the current repo.
2. install locally.
3. run a deterministic example.
4. run the runtime benchmark example.
5. inspect the KRK evidence package.
6. bring a sanitized workload.

Repo restructuring should not make this path harder.

## Examples Path

Examples should progress from simple to realistic:

- deterministic-only.
- cache-heavy.
- provider-routed dry-run.
- GPU-eligible dry-run.
- adversarial fallback.
- service-replay placeholder with sanitized fixtures.

Examples can remain in the main repo until their volume or review model requires a separate workload repo.

## Registry Path

Future registries:

- Workload Spec registry.
- Target Registry.
- Evidence Registry.

Recommended sequence:

1. define schemas in the main repo.
2. create small public-safe examples in the main repo.
3. add validation tooling.
4. split registries only after review and versioning policy are stable.

## Explicit Non-Actions

This plan does not authorize:

- repo renames.
- repo splits.
- new GitHub repo creation.
- GitHub settings changes.
- releases.
- PRs.
- pushes.

Any repo restructuring must be a later explicit goal.
