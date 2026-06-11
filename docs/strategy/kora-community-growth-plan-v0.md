# KORA Community Growth Plan v0

Status: planning document. This plan does not create community channels, repos, PRs, releases, or GitHub settings.

## Purpose

KORA community growth should start from reproducibility, examples, and claim-safe workload proposals.

The community should understand:

- KORA as the umbrella.
- KORA Core as the OSS AI workload execution layer.
- KRK as the deterministic-first routing kernel.
- Krako as future commercial infrastructure context, not the current OSS claim.

## Community Thesis

KORA should invite developers to ask:

> Can this AI workload be routed better than a default model-first path?

Community growth should be built around public-safe artifacts:

- example workloads.
- route explanations.
- benchmark methodology.
- evidence reports.
- claim boundaries.

## Developer Adoption Path

Recommended first path:

1. clone the repo.
2. install in editable mode.
3. run `python3 -m kora --help`.
4. list examples.
5. run the offline examples.
6. read the KRK evidence package.
7. propose a sanitized workload.

The path should stay local-first and no-network by default.

## OSS Growth Path

Early contribution areas:

- docs clarity.
- examples.
- workload fixtures.
- target metadata examples.
- evidence report formatting.
- benchmark methodology review.
- issue triage.
- public-safe claim review.

Avoid making early contribution depend on:

- private resources.
- provider credentials.
- raw logs.
- production data.
- GPU access.
- repo write access.

## Community Path

Recommended community loops:

- "bring a workload" discussions.
- monthly reproducibility review.
- good-first-issue examples.
- workload proposal reviews.
- evidence package reviews.
- public claim boundary reviews.

Community norms:

- sanitize workloads before sharing.
- publish commands and expected outputs.
- distinguish measured values from placeholders.
- state unsupported claims plainly.
- keep internal operations out of public issues.

## Examples Path

Example roadmap:

1. deterministic-only example.
2. cache-heavy example.
3. CPU-local dry-run example.
4. provider-routed dry-run example.
5. GPU-eligible dry-run example.
6. adversarial fallback example.
7. service-replay placeholder with sanitized data.

Each example should include:

- workload input.
- expected route behavior.
- evidence output.
- reproduction command.
- claim boundary.

## Registry Path

### Workload Spec Future

The Workload Spec should let contributors describe workload shape, routing hints, policy constraints, and evidence expectations.

Community use:

- submit sanitized workload examples.
- validate required fields.
- compare workloads across profiles.

### Target Registry Future

The Target Registry should let contributors describe execution targets without exposing private details.

Community use:

- define local, provider, GPU-class, CPU, cache, and fallback target metadata.
- validate which target details are public-safe.
- avoid hardcoding secrets or local-only paths.

### Evidence Registry Future

The Evidence Registry should index reproducible evidence packages.

Community use:

- list evidence package metadata.
- show which values are measured, simulated, or methodology-only.
- link claim boundaries to evidence.
- keep raw artifacts out unless reviewed and frozen.

## Recommended Repo Strategy For Community

Near term:

- keep the current single repo.
- reduce contributor confusion with docs and labels.
- keep examples small and runnable.

Medium term:

- consider umbrella + core if community docs and implementation docs become hard to navigate together.

Longer term:

- consider workloads or registry repos only after contribution volume and review policy justify the extra overhead.

## Public-Safe Community Language

Use:

> KORA helps developers explore routable AI workloads through deterministic-first routing, public-safe examples, and bounded evidence.

Avoid:

- claims that KORA is production-ready.
- claims that KORA proves cost savings.
- claims that KORA replaces provider routers or model serving systems.
- requests for private datasets or credentials in public channels.

## Success Signals

Healthy early signals:

- contributors can run examples without help.
- new workload proposals are sanitized and reproducible.
- evidence package docs are cited in issues.
- claim boundaries are preserved in community posts.
- examples grow without forcing a repo split too early.
