# Task 026 — S4 validation, publication and rehearsal

Status: in progress.
Base: `e0e85aff366adedccd454cda6d11955417421dd3`.
Feature freeze: no new product capability is part of this task.

## Objective

Produce a reproducible exhibition candidate from the merged three-system comparison
without expanding performance or quality claims. S4 closes validation, recovery,
documentation and rehearsal gaps. A failed or inaccessible gate stays visible.

## Acceptance matrix

| Gate | Required evidence | Current state |
|---|---|---|
| Source and regression | Clean source checkout, dependency install, full regression and static checks | Pending on an authorized execution host |
| Package install | Fresh environment install and packaged dashboard asset smoke | Pending |
| Three-system smoke | Fixed D, M and W runs with failures retained | Pending S4 rerun |
| Recovery | Controller restart, recorded-run recovery, worker restart and tunnel recovery | Pending |
| Visual interaction QA | Controls, changed input, cards, labels, history and JSON export inspected | Blocked: the available browser rejected private loopback navigation on 2026-09-07 |
| Older-device matrix | Representative devices measured or explicitly labelled inaccessible/incompatible | Blocked: no configured older-device endpoint |
| Half-day rehearsal | Fixed version operated for at least four hours with incident and recovery log | Pending |
| Public claim review | No broad quality, production, cost, energy or hardware-superiority claim | Pending final review |
| Final readiness | All mandatory gates passed or a maintainer explicitly reduces scope | Not ready |

## Frozen rehearsal protocol

1. Record commit, machine identities, runtime/model identities, configuration hashes
   and start time.
2. Start authenticated workers and SSH tunnels; verify health without exposing the
   loopback controller.
3. Run the fixed deterministic, model and mixed scenarios. Preserve blocked and
   failed rows in the denominator.
4. Exercise original, exact repeat and changed-input cases. Confirm repeats report
   zero new model calls only when the recorded reuse boundary is satisfied.
5. Restart the controller and confirm saved runs are labelled recorded; interrupt
   one disposable run and confirm it is labelled interrupted.
6. Restart one worker and confirm stale identity does not reuse prior model results.
7. Export JSON and reconcile its counts with visible cards and durable result lines.
8. Continue a minimum four-hour operating window. Record load caveats and incidents;
   do not infer hardware superiority from uncontrolled timings.
9. Stop owned benchmark services, restore any borrowed native service, verify its
   health and release its lease.

## Visual checklist

The reviewer must inspect the actual rendered page, not only API responses:

- scenario, input, repetition, reuse and changed-input controls;
- progress and final session state;
- all three result columns at supported viewport sizes;
- quality, elapsed time, calls, tokens and reused-node counters;
- blocked and failed native rows;
- comparison-configuration disclosure;
- saved-run ordering and recorded/interrupted labels;
- JSON export contents and filename;
- legibility, overflow, focus order and keyboard operation.

A screenshot alone is insufficient for interaction acceptance. API tests remain
useful evidence but do not pass this gate.

## Older-device protocol

For each representative device, record model identifier, chip, memory, OS, runtime,
model/quantization, workload, completion time, quality result, actual calls/tokens,
peak memory when available, errors and a reproducible command. “Inaccessible” and
“unsupported” are different outcomes; do not infer unsupported from missing access.
Older-device work must not change the frozen three-system implementation.

## Hard stops

- Do not add features after freeze; move them to a later sprint.
- Do not expose worker endpoints or the controller publicly for visual QA.
- Do not stop or replace an unrelated GPU service without an authorized window,
  live ownership checks, restoration and lease release.
- Do not mark exhibition-ready while visual QA, older-device labeling or the
  half-day rehearsal lacks evidence.
- Do not publish general quality, production, cost, energy or hardware claims from
  these synthetic fixtures.

## Initial S4 observation

A fresh browser attempt on 2026-09-07 could not navigate to the private loopback
dashboard because the browser environment blocked the local address. No policy
bypass, public exposure or alternate untrusted tunnel was attempted. The visual
gate remains open. Work on all independent gates may proceed in parallel when an
authorized execution host is connected.
