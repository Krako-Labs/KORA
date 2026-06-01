# AI Champion GPU/API Test Plan

Status: planning and dry-run readiness only.

This plan prepares the AI Champion GPU/API benchmark track before formal access to GPU servers, cloud generative AI resources, or external LLM APIs is available. It does not authorize real GPU execution, cloud model calls, external API calls, model downloads, production benchmark claims, or raw benchmark artifact publication.

## Current Approved Claim

Safe public wording remains:

> In a reproducible 100-task deterministic-heavy benchmark workload, KORA-controlled execution avoided 80 of 100 simulated model invocations versus a naive direct baseline.

This claim is based on deterministic-heavy simulated model invocation accounting. It is not real API-cost evidence, production cost evidence, production benchmark evidence, broad workload superiority evidence, energy evidence, or government validation.

## Planned Future Resources

The following resources are expected or possible but blocked until formally allocated:

- H100 class GPU capacity, expected as two H100 GPUs.
- Usage window expected from 2026-06-01 through 2026-06-30.
- Approximately 2,500 GB disk capacity.
- GPU server network details, credentials, and access policy are not committed in this repository.
- AWS and Azure generative AI resources may become available.
- External LLM APIs may include OpenAI, Claude, Gemini, and provider-hosted models.

Treat all listed resources as unavailable for benchmark execution until access, credentials, quotas, cost controls, and smoke tests are complete.

## Dry-Run Harness

The prepared dry-run harness is:

```bash
python3 experiments/provider_routing/run_dry_run.py \
  --config experiments/provider_routing/config.example.yaml \
  --output /tmp/kora_ai_champion_provider_routing.dry_run.json
```

The harness validates placeholder provider definitions and simulates routing among:

- `deterministic`
- `cache`
- `local_small_model`
- `local_h100_model`
- `aws_model`
- `azure_model`
- `openai_api`
- `claude_api`
- `gemini_api`

All output is synthetic and dry-run only. The script must not initiate network, provider, GPU, cloud, or local model runtime calls.

## Blocked Real Execution

Real execution remains blocked until all of the following are true:

- GPU access is formally allocated.
- Cloud/API accounts, credentials, quotas, budgets, and data policy are approved.
- Provider-specific smoke tests pass.
- Local configs are stored outside version control or in ignored paths.
- Real-run code paths have explicit opt-in gates that default to disabled.
- Benchmark scope, prompts, workload, cost accounting, logging, and artifact policy are reviewed.

## Future Smoke Test Task

Task 522 should perform the H100 access/environment smoke test. It should verify only minimal environment facts such as login, driver visibility, GPU count, disk availability, Python environment, and no-benchmark dry-run readiness. It should not run real benchmarks.

Task 523 should perform AWS/Azure/API credential smoke tests. It should verify authentication and minimal non-benchmark request wiring only after credentials are formally provided and cost controls are active.

## Future Real Benchmark Task

Task 524 should integrate the runtime hybrid benchmark after smoke tests pass. It should define the real workload, provider matrix, routing policy, accounting fields, output artifact policy, and public claim review before any result is published.

## Evidence Policy

Raw generated benchmark outputs should stay in `/tmp` or another ignored path unless a later release process explicitly selects frozen evidence. Do not commit secrets, API keys, credentials, private host details, raw provider responses, or local-only ChatGPT context.
