#!/usr/bin/env bash
# Reproduce KORA's credential-free routing result and verify it matches the
# committed numbers. No API key, no GPU, no LLM calls.
#
# Usage:  ./reproduce.sh
# Requires: Python 3.10+, pyyaml.
set -euo pipefail
cd "$(dirname "$0")"

echo "==> Regenerating the 330-case workload from the spec (deterministic)..."
python generate.py --profile full --out /tmp/kora_regen_full.json >/dev/null
if command -v md5sum >/dev/null; then
  A=$(md5sum workloads/full.json | awk '{print $1}')
  B=$(md5sum /tmp/kora_regen_full.json | awk '{print $1}')
  if [ "$A" = "$B" ]; then
    echo "    OK: regenerated workload is byte-identical to the committed full.json"
  else
    echo "    WARN: regenerated workload differs (likely email_validator/phonenumbers"
    echo "          version skew). Pin versions from full.json's 'generated_with'."
  fi
fi

echo "==> Running deterministic routing only (0 LLM calls, no key)..."
python run.py --routing-only --workload workloads/full.json --out /tmp/kora_routing.json >/dev/null

echo "==> Verifying routing metrics against the committed result..."
python - << 'PYEOF'
import json, sys
got = json.load(open("/tmp/kora_routing.json"))["routing"]
ref = json.load(open("results/routing_only.json"))["routing"]
keys = ["precision", "recall", "tp", "fp", "tn", "fn"]
ok = all(abs(got[k]-ref[k]) < 1e-9 if isinstance(got[k],float) else got[k]==ref[k] for k in keys)
print("    committed : precision=%.3f recall=%.3f (tp=%d fp=%d tn=%d fn=%d)" %
      (ref["precision"],ref["recall"],ref["tp"],ref["fp"],ref["tn"],ref["fn"]))
print("    reproduced: precision=%.3f recall=%.3f (tp=%d fp=%d tn=%d fn=%d)" %
      (got["precision"],got["recall"],got["tp"],got["fp"],got["tn"],got["fn"]))
if ok:
    print("\n✅ REPRODUCED: routing metrics match exactly (deflection 76.7%, no LLM, no key).")
    sys.exit(0)
else:
    print("\n❌ MISMATCH: routing metrics differ from the committed result.")
    sys.exit(1)
PYEOF

echo ""
echo "Accuracy numbers require model calls. To reproduce those:"
echo "  export BEDROCK_KEY=...   # your AWS Bedrock key"
echo "  ./run_all_models.sh && python aggregate_results.py"
echo "Or inspect the committed results/full_*.json (every wrong answer is listed)."
