# Provider Routing Readiness Checklist

Status: pre-access readiness.

## Ready Now

- [x] Planning documents exist for GPU/API benchmark preparation.
- [x] Provider routing matrix separates deterministic, cache, local, GPU, cloud, and external API routes.
- [x] Dry-run provider routing harness exists under `experiments/provider_routing/`.
- [x] Example config uses placeholders only.
- [x] Dry-run CLI emits synthetic summaries.
- [x] Tests cover config validation, dry-run routing, and placeholder-only config safety.
- [x] Current claim boundary is documented.

## Blocked Until Formal Access

- [ ] H100 login/access confirmation.
- [ ] H100 driver and runtime verification.
- [ ] GPU disk and environment smoke test.
- [ ] AWS generative AI access confirmation.
- [ ] Azure generative AI access confirmation.
- [ ] OpenAI API credential smoke test.
- [ ] Claude API credential smoke test.
- [ ] Gemini API credential smoke test.
- [ ] Provider-hosted model smoke test if applicable.
- [ ] Cost controls and quota limits documented.
- [ ] Data handling and logging policy approved.
- [ ] Real benchmark workload and artifact freeze policy approved.

## Future Smoke Test Task

Task 522: H100 access/environment smoke test.

Expected scope:

- Confirm formal access.
- Verify GPU count and driver visibility.
- Verify disk availability.
- Verify Python/runtime basics.
- Run no real benchmark.
- Commit no credentials, host secrets, or raw sensitive environment dumps.

Task 523: AWS/Azure/API credential smoke test.

Expected scope:

- Confirm credentials are formally provided.
- Verify each provider with minimal smoke test only.
- Record model IDs and quota/budget limits.
- Run no real benchmark.
- Commit no secrets or raw provider responses.

## Future Real Benchmark Task

Task 524: runtime-integrated hybrid benchmark.

Expected scope:

- Integrate deterministic, cache, local model, H100, cloud, and external API routes.
- Add explicit opt-in gates for real calls.
- Capture provider accounting fields.
- Produce reviewable benchmark evidence only after smoke tests pass.
- Update public claims only after evidence review.
