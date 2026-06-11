# KRK Public Evidence Boundary v0

## Purpose

This boundary defines what KRK H100 and GPU-class evidence may publish safely.

The public evidence goal is route selectivity:

> KORA benchmarks when GPU-class compute should be used, not raw GPU usage.

## Public-Safe Fields

Public summaries may include:

- benchmark profile name.
- workload item count.
- public fixture path.
- policy IDs.
- route distribution.
- exact route accuracy.
- acceptable route rate.
- unsafe misroute rate.
- GPU false positive count.
- GPU false negative count.
- fallback counts.
- compute-weighted GPU demand.
- sanitized bounded measurement summaries.
- formula version.
- claim level.
- public repo commit.
- limitations.

## Private-Only Fields

Do not publish:

- private resource allocation details.
- server names.
- IP addresses.
- SSH users.
- credentials.
- raw GPU logs.
- raw provider responses.
- private endpoints.
- local-only private paths.
- private operating notes.
- unsanitized raw artifacts.

## Raw Artifact Handling

Raw artifacts should remain local or private unless a later review explicitly selects and sanitizes them for public release.

Public evidence should prefer:

- generated summaries.
- reduced tables.
- schema-validated reports.
- fixture references.
- methodology notes.

## Sanitized Summary Requirements

Every public summary should state:

- benchmark profile.
- route policy.
- route distribution.
- metric definitions.
- artifact boundary.
- reproduction path.
- claim boundary.

## Prohibited Claims

Do not claim:

- production cost reduction.
- 10x savings.
- real API-cost reduction.
- customer savings.
- infrastructure savings.
- broad workload superiority.
- H100 superiority.
- replacement of vLLM, OpenRouter, LiteLLM, OpenAI, Claude, Gemini, or other systems.
- formal external validation.

## Approved Bounded Language

Approved:

> KRK can be evaluated as an execution-path routing kernel across deterministic, cache, CPU, provider, GPU, and fallback paths.

Approved:

> KRK benchmark methodology can compare route selectivity and prepare bounded GPU-routed subset measurement.

Approved:

> KORA benchmarks when GPU-class compute should be used, not raw GPU usage.

These statements do not imply production savings, customer savings, infrastructure reduction, or broad workload superiority.
