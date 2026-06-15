# KORA Five-Minute First Value Quickstart

Status: public-safe local quickstart.

This quickstart gives a fresh-clone user the shortest current path to understand what KORA does through real repo-owned functionality.

## What You Will See

The workflow runs four steps over committed public KRK fixtures:

1. Inspect available execution paths and workload profiles.
2. Compare a direct model-candidate path with a KRK-routed path.
3. Run the public-safe KRK dry-run fixture workflow.
4. Generate a report with route decisions and output-fidelity summary metrics.

It requires no provider credentials, no GPU, and no network access.

## Run

From the repository root:

```bash
python3 -m kora inspect
python3 -m kora compare
python3 -m kora run
python3 -m kora report \
  --json-out /tmp/kora-first-value.json \
  --md-out /tmp/kora-first-value.md
```

If the package console script is installed in your environment, the equivalent commands are:

```bash
kora inspect
kora compare
kora run
kora report \
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
