#!/usr/bin/env bash
set -u
cd "$(dirname "$0")"

if [ -z "${BEDROCK_KEY:-}" ]; then echo "ERROR: BEDROCK_KEY 없음"; exit 1; fi
export BEDROCK_KEY

JUDGE="anthropic.claude-sonnet-4-6"
TS=$(date +%Y%m%d_%H%M%S)
LOG="results/full_run_${TS}.log"

# name|modelId  (name은 결과 파일명용)
MODELS=(
  "sonnet46|anthropic.claude-sonnet-4-6"
  "haiku45|anthropic.claude-haiku-4-5-20251001-v1:0"
  "llama3_70b|meta.llama3-3-70b-instruct-v1:0"
  "llama1_8b|meta.llama3-1-8b-instruct-v1:0"
  "novapro|amazon.nova-pro-v1:0"
)

echo "=== KORA model-diversity full run | judge=$JUDGE | k=1 | both conditions ===" | tee -a "$LOG"
echo "start: $(date)" | tee -a "$LOG"

for entry in "${MODELS[@]}"; do
  name="${entry%%|*}"; model="${entry#*|}"
  out="results/full_${name}.json"
  echo "" | tee -a "$LOG"
  echo ">>> [$name] $model  ($(date +%H:%M:%S))" | tee -a "$LOG"
  python run.py \
    --backend bedrock \
    --model "$model" \
    --judge-model "$JUDGE" \
    --workload workloads/full.json \
    --conditions both \
    --k 1 \
    --out "$out" 2>&1 | tee -a "$LOG"
  echo "<<< [$name] done -> $out  ($(date +%H:%M:%S))" | tee -a "$LOG"
done

echo "" | tee -a "$LOG"
echo "ALL DONE: $(date)" | tee -a "$LOG"
