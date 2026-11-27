# KORA Five-Minute First Value Quickstart

Status: public-safe local quickstart.

This quickstart gives a fresh-clone user the shortest current path to understand what KORA does through real repo-owned functionality.

## What You Will See

The workflow runs four steps over committed public KRK fixtures:

1. Inspect available execution paths and workload profiles.
2. Compare a direct model-candidate path with a KRK-routed path.
3. Run the public-safe KRK dry-run fixture workflow.
4. Generate a report with route decisions and output-fidelity summary metrics.

It requires no provider credentials, no GPU, and no network access after dependencies are installed.

## Install

Use Python 3.10 or later. Check the interpreter with `python3 --version`, then run these commands in a macOS or Linux shell.

```bash
git clone https://github.com/Krako-Labs/KORA.git
cd KORA
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -e .
```

KORA uses `pyproject.toml` packaging. The installed console script is `kora`, and the module entrypoint `python3 -m kora` remains available.

## Run

From the repository root:

```bash
kora inspect
kora compare
kora run
kora report \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

If you prefer the Python module form, the equivalent commands are:

```bash
python3 -m kora inspect
python3 -m kora compare
python3 -m kora run
python3 -m kora report \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

Compatibility wrapper:

```bash
python3 scripts/kora_five_minute_demo.py \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

Expected result:

- step count: `4`.
- commands required: `1`.
- required user decisions: `0`.
- total fixture items: `18`.
- dry-run execution success rate: `1.0000`.
- unsafe misroute rate: `0.0000`.
- acceptable output rate: `1.0000`.

Goal 070C validated this editable-install path in a temporary clean virtual environment. Native Windows and WSL-specific validation are deferred.

## Inspect

The inspect step reports the local execution paths KORA can route across in the public fixtures:

- `deterministic`
- `cache`
- `CPU`
- `provider`
- `GPU`
- `fallback`

This is a local dry-run inspection. It does not call providers or use GPU hardware.

## Compare

The compare step contrasts:

- a direct model-candidate path for each public fixture item.
- the KRK-routed path selected from router-visible metadata.

In the current public fixture set, KRK routes `11 / 18` items to deterministic, cache, CPU, or fallback paths rather than provider/GPU-class paths. This is an execution-path routing opportunity count, not a production savings claim.

## Run

The run step executes the existing runtime-integrated dry-run evaluator over the four public matrix profiles:

- mixed-realistic
- GPU-heavy
- cache-heavy
- adversarial

It creates route-specific dry-run evidence records without provider calls or GPU execution.

## Report

The report step reuses the output-fidelity evaluator and summarizes:

- route decisions.
- dry-run execution success.
- unsafe misroute rate.
- exact output-contract matches.
- structured-equivalent acceptable route changes.
- degraded and failed output counts.

The generated Markdown report is written to the `--md-out` path.

## Replay a support-routing policy change

From the same checkout and activated environment, run two policies against the same 24 public requests. The baseline policy is a historical comparison. The freshness policy requires a valid date for routes that depend on time-sensitive facts.

```bash
results=$(mktemp -d)
replay_policy() {
  python -m experiments.blind_routing.run --split all \
    --rules "experiments/blind_routing/${1}_rules.json"
}

replay_policy baseline > "$results/baseline.json" &&
replay_policy freshness > "$results/freshness.json" &&
replay_policy baseline > "$results/rollback.json" &&
cmp "$results/baseline.json" "$results/rollback.json" && echo "Rollback reproduced the baseline"

python - "$results" <<'PY'
import json
import sys
from pathlib import Path

for policy in ("baseline", "freshness"):
    report = json.loads((Path(sys.argv[1]) / f"{policy}.json").read_text())
    score = report["summary"]["false_bypass"]
    print(f"{policy}: {score['count']}/{score['denominator']} answered when deferral was required")
PY
```

On the committed cases, the baseline answers 8 of the 10 requests that require deferral. The freshness policy answers 0 of those 10. A successful rollback reproduces the first output byte for byte. The [routing evaluation](../experiments/blind_routing/README.md) defines the metrics and test cases.

To inspect how a read-only lookup handles a change in permission or an expired record, run the separate [support-tier example](../examples/support_tier_shadow/README.md).

```bash
kora run support_tier_shadow
```

Read the seven events in `results`. Revoking access yields `denied`, and an expired record yields `refresh_required`. The example calls the original lookup on every event, including the repeat marked `would_reuse`. Expect `origin_calls: 7` and `actual_origin_calls_skipped: 0`. Both exercises run locally with synthetic data.

## Claim Boundary

This quickstart demonstrates local first value over public fixtures. It does not claim production adoption, production readiness, production cost reduction, customer savings, provider superiority, H100 superiority, broad workload superiority, or real API/GPU cost reduction.

## Next Interface Direction

The first official CLI surface now exposes the same flow as:

```bash
kora inspect
kora compare
kora run
kora report
```

The current implementation keeps `scripts/kora_five_minute_demo.py` as a compatibility wrapper. Future work should polish install-package ergonomics, command output formatting, and user-provided workload selection.
