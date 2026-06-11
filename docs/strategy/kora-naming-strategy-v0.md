# KORA Naming Strategy v0

Status: planning document. This document does not rename repositories, packages, releases, or GitHub organizations.

## Purpose

KORA needs a naming system that can support the current KRK-oriented alpha, the KORA Core execution layer, future workload and registry artifacts, and a broader developer community.

The naming strategy should make the hierarchy easy to understand:

```text
KORA
  -> KORA Core
    -> KRK
```

## Canonical Names

### KORA

KORA is the umbrella name and movement.

Public meaning:

> Make AI workloads routable.

KORA should refer to the overall category, community, documentation family, examples, future registries, and long-term ecosystem around routable AI workloads.

Use KORA when talking about:

- the movement.
- the broad project.
- community and ecosystem.
- category language.
- public-facing narrative.

### KORA Core

KORA Core is the planned open-source AI workload execution layer.

KORA Core should be the name for the main OSS engine that eventually owns:

- inspect.
- compare.
- run.
- report.
- Workload Spec.
- Target Registry.
- Evidence Report.
- adapters.
- examples.

Use KORA Core when talking about the OSS execution layer rather than the full movement.

### KRK

KRK means KORA Routing Kernel.

KRK is the deterministic-first execution routing kernel inside KORA Core. It routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

Use KRK when talking about:

- route selection.
- route explanation.
- deterministic-first routing.
- routing benchmark methodology.
- route selectivity evidence.
- the current technical wedge.

### Krako

Krako is a future commercial execution infrastructure company name.

Public KORA docs should keep Krako separate from OSS KORA claims unless a specific public product, repo, or integration is explicitly approved.

Use Krako carefully for:

- future infrastructure company context.
- commercial execution infrastructure direction.
- long-term ecosystem separation.

Do not use Krako to imply that KORA Core is a hosted commercial product today.

## Supporting Artifact Names

### KORA Workload Spec

The KORA Workload Spec should describe workload inputs, routing metadata, target requirements, policy hints, and evidence fields.

Recommended public shorthand:

- "KORA Workload Spec"
- "Workload Spec" after first mention.

### KORA Target Registry

The KORA Target Registry should describe execution target metadata for deterministic, cache, CPU, provider, GPU, and fallback paths.

Recommended public shorthand:

- "KORA Target Registry"
- "Target Registry" after first mention.

### KORA Evidence Registry

The KORA Evidence Registry is a future concept for indexed, reproducible evidence packages.

It should not be presented as implemented yet.

Potential scope:

- benchmark evidence summaries.
- route-selectivity results.
- workload fixture references.
- reproducibility metadata.
- claim boundary status.

Recommended public shorthand:

- "KORA Evidence Registry"
- "Evidence Registry" after first mention.

## Current Public Naming

Current repo and public narrative:

- repo: `KORA`.
- README title: KORA Core.
- current implementation: KRK-oriented alpha.
- current top-level CLI: `examples`, `run`, `studio`, `telemetry`.
- current product direction: KORA Core `inspect -> compare -> run -> report`.

This is acceptable for the current transition period as long as docs clearly distinguish current implementation from future roadmap.

## Naming Rules

Use:

- "KORA" for the umbrella.
- "KORA Core" for the OSS execution layer.
- "KRK" or "KORA Routing Kernel" for routing-kernel work.
- "Krako" only for future commercial infrastructure context.

Avoid:

- using KORA Core to imply every future workflow is already implemented.
- using KRK as the name for the whole project.
- using Krako as a substitute for KORA.
- naming public docs in a way that suggests a repo split already happened.

## Recommended Near-Term Public Wording

Use this pattern:

> KORA makes AI workloads routable. KORA Core is the planned open-source AI workload execution layer. The current alpha focuses on the KORA Routing Kernel, a deterministic-first routing kernel for routing workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.

## Open Naming Decisions

- Whether the package name remains `kora` when KORA Core matures.
- Whether KRK becomes a subpackage, command namespace, or standalone package.
- Whether future registries live in the main repo or separate repos.
- Whether KORA Studio remains inside the main repo or becomes a separate preview surface later.

## Recommendation

Keep current public naming stable through the next alpha cycle.

Do not rename repos immediately. Use docs, examples, and module boundaries to teach the hierarchy first. Revisit repo names only after KORA Core has a tested inspect/compare/run/report alpha surface and KRK has an evidence package strong enough to stand on its own.
