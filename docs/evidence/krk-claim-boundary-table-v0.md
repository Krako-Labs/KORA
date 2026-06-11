# KRK Claim Boundary Table v0

Status: public-safe claim boundary.

This table separates supported KRK statements from unsupported interpretations. It should be used when writing README text, release notes, evidence summaries, and technical paper drafts.

| Statement | Status |
| --- | --- |
| KRK can route workload tasks. | Supported as the current alpha direction and execution-control surface. |
| KRK is a deterministic-first routing kernel. | Supported as the public architecture definition. |
| KRK produces benchmark evidence. | Supported for the deterministic-heavy public benchmark path. |
| KRK can produce bounded reproducible evidence. | Supported for the current deterministic-heavy workload and documented methodology. |
| KRK can compare execution-path selectivity. | Methodology defined; extended matrix measurement not yet implemented. |
| KORA benchmarks when GPU-class compute should be used. | Supported as a methodology direction, not as a completed GPU measurement. |
| KRK reduces production cost. | Not Supported. |
| KRK provides 10x savings. | Not Supported. |
| KRK proves customer savings. | Not Supported. |
| KRK replaces vLLM. | Not Supported. |
| KRK replaces OpenRouter or LiteLLM. | Not Supported. |
| KRK replaces GPT, Claude, or Gemini. | Not Supported. |
| KRK eliminates GPUs. | Not Supported. |
| KRK proves broad workload superiority. | Not Supported. |
| KRK proves H100 superiority. | Not Supported. |

## Approved Bounded Language

The current deterministic-heavy evidence may use this bounded language:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

## Required Qualifiers

When using the approved language, preserve these qualifiers:

- the workload is deterministic-heavy.
- the baseline is naive and simulated.
- the avoided invocations are simulated model invocations.
- the result is bounded alpha evidence.
- the result is not a production benchmark.

## Prohibited Interpretations

Do not rewrite the current evidence as:

- production savings proof.
- customer savings proof.
- infrastructure reduction proof.
- provider replacement proof.
- broad route-quality proof.
- GPU infrastructure reduction proof.
