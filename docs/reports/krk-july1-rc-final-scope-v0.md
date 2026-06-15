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
| Runtime-integrated dry-run route evaluation | Goal 053 executable dry-run workflow path with 18 evidence records, 100% acceptable route rate, 0% unsafe misroute rate, and 100% dry-run execution success rate. |
| Bounded H100 subset evidence | Goal 050 public-safe bounded measurement for four GPU-selected public matrix items. |
| Expanded H100 evaluation status | Goal 055 prepared expanded bounded H100 routed-subset evidence, but it was not run because safe CUDA/H100 runtime was unavailable. |
| Bounded provider-routed validation | Public-safe bounded validation for three provider-selected public matrix items. |
| Expanded provider-routed validation | Goal 054 public-safe expanded bounded provider validation for 12 provider-selected public matrix variants. |
| Evidence package | Current KRK evidence package and performance table. |
| Performance table | Current table summarizing deterministic-heavy, route-selectivity, runtime-integrated dry-run, H100 subset, expanded H100 status, and provider-path evidence. |
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

The July 1 RC scope is an evidence-centered KRK package. It demonstrates deterministic-first routing concepts with bounded deterministic-heavy evidence, four public dry-run matrix route-selectivity profiles, runtime-integrated dry-run route-selectivity evidence, bounded H100-routed subset measurement from Goal 050, expanded bounded provider-routed validation from Goal 054, and a prepared-but-not-measured expanded H100 status from Goal 055.

The RC does not claim production readiness, production savings, customer savings, infrastructure savings, H100 superiority, provider superiority, broad workload superiority, or replacement of existing model serving/provider routing systems.
