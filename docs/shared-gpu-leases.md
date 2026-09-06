# Cooperative shared GPU usage board

Use `scripts/gpu_lease.py` as a standalone Linux-host utility. It does not install
KORA in a native inference server or alter model execution. All projects using the
shared GPU must agree to consult and acquire the same board before launching work.

Default state directory: `~/krako-resource-control`; override with
`KRAKO_GPU_STATE`. All cooperating clients must use the same host account/state
directory. This is not multi-user authentication or OS-level GPU isolation.

## Operations

```sh
python3 scripts/gpu_lease.py status
python3 scripts/gpu_lease.py acquire --project example --owner operator \
  --purpose benchmark --minutes 20 --unit example-benchmark.service
python3 scripts/gpu_lease.py heartbeat --lease-id ID
python3 scripts/gpu_lease.py release --lease-id ID
```

Status reports declared owner/project/purpose, start, expected end, heartbeat and
overdue state alongside actual GPU memory, utilization, PID and cgroup.
`STATUS.json` and `STATUS.md` refresh on a status query; check the sample timestamp.
`active.json` is the current lease, protected by a file lock and atomic replacement.
`history.jsonl` records acquired, heartbeat and released events with elapsed lease
duration. Duration includes setup and idle time; it is not measured GPU-hours.

An optional `services.json` maps exact systemd service names to declared project/
owner labels for existing long-running services. Unknown processes remain visibly
unregistered. A GPU at zero utilization may still be occupied by a loaded model.

## Conflict and handover rules

- Concurrent acquisitions cannot both succeed.
- An existing lease blocks acquisition even after its expected end. No automatic
  stealing, expiry cleanup, process termination or service replacement occurs.
- GPU processes without a lease also block acquisition.
- `--handover-service exact.service` admits only observed processes in that exact
  service cgroup. This flag does not authorize stopping that service.
- A release requires the matching lease ID and no remaining GPU processes, except
  the originally declared handover service via `--restored-service exact.service`.
- The operator must verify restored service health/model before release; the utility
  checks process ownership, not HTTP application readiness.
- Lease IDs prevent accidental mismatched release, not malicious use by another
  person with write access to the same state directory.

Failing GPU observation fails the command. The utility never claims GPU availability
merely because a lease file is absent. It currently observes NVIDIA compute-process
records; it is not a comprehensive accounting system for graphics/MIG/multiple GPUs.

## Adoption and limits

Project-root operating instructions should require status, acquisition, recorded
lease ID, progress heartbeats, owned-process shutdown/restoration, then release.
Existing processes bypassing the convention are visible but not forcibly stopped.
All old launchers are not automatically integrated by installing this script.

Notification here means the shared board and project operating records. There are
no external chat messages, email, queue, dashboard, billing or preemption.
Tests cover concurrent acquisition, exact cgroup admission, stale-lease refusal,
mismatched release and release history using an explicitly mocked observation.
