# Goal 082A README Refresh Proposal

Status: proposal only. Do not treat this as a completed README rewrite.

## Current README Problem Summary

The current public presentation is still weighted toward benchmark and evidence history. That history is important, but the first screen does not yet make the new examples-driven value obvious enough for a developer asking, "What can I try right now?"

The README should move toward KORA as a routing/control platform with runnable first-value examples, while keeping all claims inside current evidence boundaries.

## Proposed New README Positioning

Suggested positioning:

> KORA helps developers make AI workloads routable. It shows which tasks can run through deterministic handlers, cache reuse, local transforms, or explicit provider/model fallback before teams commit to deeper integration.

Supporting line:

> Current examples are offline and synthetic. They demonstrate routing and control surfaces, not production diagnostic accuracy or cost proof.

## Proposed Top-of-README Structure

1. Product identity:
   - `KORA`
   - `Make AI workloads routable.`
2. One-paragraph value proposition:
   - deterministic candidates.
   - provider-needed candidates.
   - route rationale.
   - offline first-value examples.
3. Quick start:
   - `python3 -m kora examples list`
   - `python3 examples/kora_doctor/run.py`
   - `python3 examples/deterministic_classification/run.py`
4. What KORA shows:
   - deterministic handlers.
   - cache reuse opportunities.
   - static transforms.
   - provider/model fallback boundaries.
5. Example catalog.
6. Evidence and claim boundaries.
7. Roadmap and contribution path.

## Proposed Examples Section

Suggested section title:

```markdown
## Try the Examples
```

Suggested wording:

```markdown
KORA includes offline examples that show the routing/control surface without requiring provider credentials.

- KORA Doctor: inspect sample workloads and see deterministic candidates, provider-needed candidates, route rationale, counters, and next steps.
- Deterministic Classification Pack: route support tickets, issues, incidents, documents, and log events through deterministic handlers with explicit provider-needed fallback cases.
- First-value CLI: inspect, compare, run, and report the public fixture path.
```

Suggested commands:

```bash
python3 -m kora examples list
python3 examples/kora_doctor/run.py
python3 examples/kora_doctor/run.py --all
python3 examples/deterministic_classification/run.py
```

## Proposed Safe Claims Section

Suggested section title:

```markdown
## Current Evidence Boundaries
```

Suggested wording:

```markdown
Current public examples are offline and synthetic. They support narrow claims about KORA's routing/control surfaces:

- KORA can identify deterministic candidates and provider-needed candidates in bundled sample workloads.
- KORA can execute deterministic sample tasks through KORA TaskGraph paths.
- KORA examples can preserve explicit provider-needed fallback cases while making zero provider calls.

They do not prove production diagnostic accuracy, automatic cost reduction, real API-cost reduction, benchmark superiority, broad workload superiority, or production readiness.
```

## Exact Wording Suggestions

Use:

- `KORA helps make AI workloads routable.`
- `offline example`
- `synthetic sample workload`
- `deterministic candidate`
- `provider-needed candidate`
- `provider calls actually made: 0`
- `route rationale`
- `next-step recommendations`

Avoid:

- `reduces cost`
- `proves savings`
- `production diagnostic`
- `benchmark-leading`
- `better than providers`
- `production-ready`
- `automatic optimization`

## What Should Wait Until Later Evidence

Do not add these claims until separate evidence exists:

- production diagnostic accuracy.
- automatic cost reduction.
- real API-cost proof.
- benchmark superiority.
- broad workload superiority.
- production proxy readiness.
- arbitrary repository inspection.
- real customer workload conclusions.

## Risks And Overclaim Boundaries

Primary risk: examples can be misread as production validation. The README should repeatedly label them as offline, synthetic, and first-value examples.

Second risk: avoided provider/model invocation counts can be misread as real cost reduction. The README should call them `simulated` or `within these offline samples`.

Third risk: KORA Doctor can be misread as a complete repository diagnostic. The README should say it currently inspects bundled sample workloads and gives route rationale, not arbitrary-project diagnostic guarantees.
