# KRK July 1 RC Final Scope v0

Status: final scoped package for July 1 RC decision.

## Included Scope

| Area | Included scope |
| --- | --- |
| KRK definition | KRK means KORA Routing Kernel: a deterministic-first routing kernel for AI workloads. |
| Deterministic-heavy evidence | Existing deterministic-heavy benchmark evidence with bounded simulated invocation counters. |
| Route-selectivity metrics | Four public dry-run matrix profiles with generated JSON and Markdown metrics. |
| Four matrix profiles | mixed-realistic, GPU-heavy, cache-heavy, and adversarial public alpha fixtures. |
| Dry-run evaluator | `python3 -m kora.matrix_evaluator` route-selectivity path using router-visible metadata and oracle labels after routing. |
| Bounded H100 subset evidence | Public-safe bounded measurement for four GPU-selected public matrix items. |
| Bounded provider-routed validation | Public-safe bounded validation for three provider-selected public matrix items. |
| Evidence package | Current KRK evidence package and performance table. |
| Performance table | Current table summarizing deterministic-heavy, route-selectivity, H100 subset, and provider-path evidence. |
| Technical paper draft | Included as draft context only, not as a final paper submission claim. |
| KORA Core roadmap | Included as roadmap direction for inspect, compare, run, and report workflow expansion. |

## Excluded Scope

| Area | Excluded claim or action |
| --- | --- |
| Production savings | No production savings claim is approved. |
| 10x savings | No 10x savings claim is approved. |
| Customer evidence | No customer evidence or customer savings claim is approved. |
| Broad workload superiority | Current evidence does not cover broad workload superiority. |
| H100 superiority | Current H100 evidence is subset-bounded and does not prove H100 superiority. |
| Provider superiority | Current provider evidence is subset-bounded and does not prove provider superiority. |
| Full KORA Core implementation | KORA Core workflow implementation remains incomplete and roadmap-scoped. |
| Existing routing system replacement | KRK is not positioned as a replacement for existing model serving or provider routing systems. |
| Release or tag | No release or tag is included unless explicitly approved later. |

## Final RC Scope Statement

The July 1 RC scope is an evidence-centered KRK package. It demonstrates deterministic-first routing concepts with bounded deterministic-heavy evidence, four public dry-run matrix route-selectivity profiles, bounded H100-routed subset measurement, and bounded provider-routed validation.

The RC does not claim production readiness, production savings, customer savings, infrastructure savings, H100 superiority, provider superiority, broad workload superiority, or replacement of existing model serving/provider routing systems.
