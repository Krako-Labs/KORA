# KRK Paper Claim Boundary v0

Status: claim boundary for KRK technical paper drafts.

## Allowed Statements

- KRK introduces deterministic-first execution routing for AI workloads.
- KRK routes workload tasks across deterministic, cache, CPU, provider, GPU, and fallback paths.
- KRK is the first technical wedge toward KORA Core.
- KRK can be evaluated with bounded reproducible benchmark evidence.
- The current public evidence is alpha-stage and bounded.
- The current public package defines benchmark methodology for route selectivity and future matrix evaluation.

## Exact Approved Benchmark Wording

Use this exact wording when summarizing the current deterministic-heavy benchmark:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

Optional supporting sentence:

> The same current public evidence package reports zero deterministic mismatches for that workload.

## Prohibited Statements

Do not claim:

- production cost reduction.
- 10x savings.
- customer savings.
- infrastructure savings.
- broad workload superiority.
- H100 superiority.
- replacement of vLLM, OpenRouter, LiteLLM, OpenAI, Claude, Gemini, or other systems.
- production readiness.
- formal validation.

## What The Paper Must Not Imply

The paper must not imply that:

- deterministic-heavy benchmark evidence generalizes to all workloads.
- simulated avoided model invocations are the same as measured billing reduction.
- methodology docs are the same as measured route-accuracy results.
- GPU-routed subset methodology is completed GPU measurement.
- KORA Core inspect, compare, run, report, and doctor workflows are complete unless the corresponding implementation and tests exist.
- KRK is a hosted gateway or cloud marketplace.

## How To Phrase Limitations

Use direct limitation language:

- "Current evidence is alpha-stage and bounded."
- "The deterministic-heavy benchmark is simulated."
- "Routing accuracy metrics are not measured yet."
- "The extended matrix fixtures are not yet connected to a runner."
- "Bounded GPU-routed subset measurement remains future work in the current public package."
- "Provider-routed validation is not included in the current public package."

Avoid vague limitation language:

- "early results prove the approach."
- "validated in realistic environments."
- "ready for production."
- "cost-saving."
- "better than existing routers."

## Paper Review Checklist

- [ ] The approved benchmark wording is exact.
- [ ] Every stronger statement has a public evidence source.
- [ ] Future experiments are labeled as future experiments.
- [ ] Related-work language is neutral.
- [ ] No private resource details, raw logs, local paths, credentials, or internal operations appear.
- [ ] The draft does not treat roadmap CLI surfaces as implemented commands.
