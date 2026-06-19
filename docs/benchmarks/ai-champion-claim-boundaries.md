# Provider Routing Claim Boundaries

Status: public wording guardrail for pre-access GPU/API benchmark preparation.

## Safe Public Wording

The current approved claim remains:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

For Task 521 additions, safe wording is:

- KORA has a dry-run provider routing harness for planned provider routing GPU/API benchmark work.
- The harness validates placeholder provider definitions and emits synthetic dry-run summaries.
- The harness covers planned routes for deterministic, cache, local model, H100, AWS, Azure, OpenAI, Claude, and Gemini providers.
- Real GPU/API benchmark execution remains blocked until access, credentials, smoke tests, and benchmark approval are complete.

## Forbidden Claims

Do not claim:

- production cost reduction proof
- real API-cost reduction proof
- production benchmark proof
- broad workload superiority proof
- energy reduction evidence
- formal government validation
- real GPU/API benchmark results
- real H100 performance results
- real cloud/provider model quality results
- real latency comparisons
- real provider cost comparisons

## Required Qualifiers

Use these qualifiers when discussing Task 521 outputs:

- synthetic
- dry-run only
- planning harness
- placeholder config
- blocked real execution
- not production evidence
- not real API/GPU benchmark evidence

## Publication Review Gate

Before publishing any future real benchmark claim, require:

- workload version and benchmark scope review
- provider identity and model version review
- raw artifact handling decision
- cost accounting method review
- reproducibility instructions
- claim-to-evidence audit
- secret scan
- legal/data policy review where applicable
