# KORA Routable AI Workloads Master Plan v0.1

## North Star

Make AI workloads routable.

Docker made applications portable. KORA makes AI workloads routable.

KORA is the umbrella for a developer-facing movement and toolchain around routing AI execution. KORA Core is the open-source execution layer. The KORA Routing Kernel, or KRK, is the first technical wedge: a deterministic-first routing kernel for deciding when a workload can use deterministic, cached, local, provider, GPU, or fallback execution.

## Problem

AI execution is fragmenting. Developers now choose among local models, hosted providers, GPU servers, caches, deterministic tools, agent frameworks, RAG systems, and custom fallback paths. Most applications still treat execution as a direct model call, even when parts of the workload could be handled through deterministic logic, cached results, lower-cost local execution, or a safer fallback.

That fragmentation creates operational questions:

- Which target should run this workload?
- When is a model call required?
- What evidence explains the routing decision?
- How can teams compare paths without turning benchmarks into unsupported claims?
- How can an execution system preserve privacy, latency, quality, and cost signals without becoming a black box?

KORA starts from those routing questions.

## Why Not Start As A Hosted Gateway

KORA is not starting as a hosted gateway, cloud marketplace, or provider replacement because the first proof target is routing behavior, not hosted infrastructure. A hosted gateway would make the project look like an operational service before the routing kernel, workload spec, target registry, and evidence report are mature enough to support that posture.

The public alpha should stay focused on reproducible local behavior:

- route decisions.
- explanations.
- benchmark fixtures.
- evidence reports.
- public-safe examples.

Hosted execution, commercial infrastructure, and managed nodes may become future directions, but they should follow the routing kernel and evidence layer.

## KRK First

KRK is the KORA Routing Kernel. It is the deterministic-first execution routing kernel inside KORA Core.

The current alpha maps to KRK primitives:

- `route`: select an execution path.
- `explain`: describe the routing decision.
- `benchmark`: compare bounded workloads.
- `report`: produce evidence for review.

KRK should prove that execution can be routed and explained before KORA expands into broader workflow surfaces.

## KORA Core Second

KORA Core is the planned open-source AI workload execution layer. It should organize public developer workflows around:

- inspect.
- compare.
- run.
- report.

Those verbs are the product direction. The current alpha does not implement every future command implied by that model. Today, the implemented CLI surface is still KRK-oriented: route, explain, benchmark, and report.

## KORA Umbrella Long-Term

KORA is the umbrella and long-term category: routable AI workloads.

Long-term KORA should include:

- KORA Core.
- KORA Routing Kernel.
- KORA Workload Spec.
- KORA Target Registry.
- KORA Evidence Report.
- examples and developer preview kits.
- public-safe benchmark methodology.

## July Milestones

July 1 direction:

- validate KRK with bounded evidence.
- package KRK as a standalone app or CLI surface.
- produce a performance table with clear methodology and limits.

Mid-July direction:

- publish a KRK technical note or paper draft.
- explain deterministic-first routing, target selection, fallback behavior, and evidence reporting.

July 31 direction:

- expand KRK into KORA Core alpha.
- prepare KORA naming and repo structure.
- publish examples and developer preview materials when safe.
- package the public report, plan, and video narrative around evidence rather than unsupported claims.

## Examples Roadmap

Public examples should show the route from simple to realistic:

1. deterministic-only workload.
2. cache-friendly workload.
3. CPU-local workload.
4. provider-routed workload.
5. GPU-eligible workload with sanitized evidence.
6. fallback path with reproducible failure handling.

Each example should include inputs, route decision, evidence report, and claim boundary.

## Developer And Community Direction

The developer preview should invite reproducibility:

- clear install instructions.
- simple route/explain/benchmark/report commands.
- workload proposal template.
- target registry examples.
- evidence report examples.
- limitations and open questions.

KORA should communicate ambition through technical transparency, not unsupported production claims.

## Public-Safe Claim Boundary

Allowed public framing:

- KORA aims to make AI workloads routable.
- KRK is a deterministic-first execution routing kernel.
- KORA Core is the planned open-source AI workload execution layer.
- The current alpha focuses on routing and evidence.
- KORA can produce bounded, reproducible benchmark evidence.

Do not claim production cost reduction, broad superiority, customer savings, infrastructure savings, or replacement of provider/router systems.
