# CLINC150 — direct vs KORA (real inference)

Real-inference smoke comparing two ways of classifying CLINC150 intents against a
**local vLLM server**:

- **direct** — every query is sent to the LLM.
- **kora** — a deterministic keyword router (`router.py`) answers easy queries
  for free; only the queries it abstains on are escalated to the LLM.

The point is to measure the routing economics: how many LLM calls / tokens the
router deflects, and at what accuracy cost.

## Environment

- **venv:** `~/kora-ai-champion/envs/kora-benchmark` (vllm 0.6.6.post1, datasets 5.0.0, openai 2.44.0)
- **model / server:** `Qwen/Qwen2.5-32B-Instruct` on `http://localhost:8000/v1` (api key `EMPTY`)
- **dataset cache:** `HF_HOME=/data/tta/hf-cache` (CLINC150 `clinc_oos` / `plus` config, offline)

### Starting the vLLM server

```bash
cd /data/tta/kora-runs
nohup ~/kora-ai-champion/envs/kora-benchmark/bin/python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-32B-Instruct \
  --tensor-parallel-size 2 \
  --port 8000 \
  --gpu-memory-utilization 0.90 \
  > /data/tta/kora-runs/vllm_server.log 2>&1 &
```

> **Note — guided decoding is disabled on purpose.** vLLM 0.6.6.post1's xgrammar
> backend crashes the engine (`TokenizerInfo has no attribute 'from_huggingface'`)
> on `response_format`/`guided_json` requests. The classifier therefore enforces
> JSON via the prompt and parses defensively in `LLMClassifier._parse_intent`.

## Running

```bash
HF_HOME=/data/tta/hf-cache \
~/kora-ai-champion/envs/kora-benchmark/bin/python \
experiments/clinc150_direct_vs_kora/run.py --n 20 --seed 0
```

Flags: `--n` sample size, `--seed` sampling seed, `--model`, `--base-url`,
`--min-score` / `--min-margin` (router confidence thresholds).

Results are written to `results/smoke_n{N}_seed{SEED}.json` with per-query records
for both arms plus an aggregate summary (accuracy, LLM calls, tokens, latency).

## Files

- `run.py` — runner: dataset sampling, both arms, aggregation, JSON output.
- `router.py` — `KeywordRouter`: keyword-overlap router built from intent labels.
- `results/` — output JSON.
