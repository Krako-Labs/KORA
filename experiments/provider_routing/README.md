# AI Champion Provider Routing Dry Run

This directory contains a dry-run-only provider routing experiment skeleton for the AI Champion GPU/API benchmark track.

The harness prepares routing logic before real GPU, cloud, or external API access is formally available. It does not call H100 servers, AWS, Azure, OpenAI, Claude, Gemini, provider-hosted models, local model runtimes, or active network endpoints. All outputs are synthetic dry-run summaries.

## Files

- `config.example.yaml`: JSON-compatible YAML with placeholder-only provider definitions.
- `run_dry_run.py`: dependency-free CLI that loads the example config, validates provider definitions, simulates routing, and emits a synthetic summary.

## Dry-Run Command

```bash
python3 experiments/provider_routing/run_dry_run.py \
  --config experiments/provider_routing/config.example.yaml \
  --output /tmp/kora_ai_champion_provider_routing.dry_run.json
```

The output is safe for local inspection but remains synthetic. Do not treat it as real benchmark evidence.

## Simulated Routes

The dry-run config covers these planned routing categories:

- `deterministic`
- `cache`
- `local_small_model`
- `local_h100_model`
- `aws_model`
- `azure_model`
- `openai_api`
- `claude_api`
- `gemini_api`

Only `deterministic` and `cache` are marked `ready_dry_run`. All local model, GPU, cloud, and external API providers are marked `planned_blocked` until access, credentials, endpoints, smoke tests, logging policy, and benchmark approval are active.

## Future Real-Provider Activation Path

Real-provider execution requires a separate task after access is formally available:

1. Keep this example config secret-free and committed as documentation.
2. Create an ignored local config outside version control for real endpoint and credential references.
3. Run provider-specific smoke tests that prove authentication and minimal request paths without running benchmarks.
4. Add explicit real-run gates in code that default to disabled.
5. Record provider versions, model identifiers, quota limits, data policy, and cost controls.
6. Run the real benchmark only after the smoke tests pass and the claim boundaries are updated.

Until those steps are complete, this experiment remains a dry-run planning harness only.
