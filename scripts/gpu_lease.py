#!/usr/bin/env python3
"""Cooperative single-GPU lease and live usage board. Never kills workloads."""

import argparse
import datetime as dt
import fcntl
import getpass
import json
import os
import subprocess
import time
import uuid
from pathlib import Path

ROOT = Path(
    os.environ.get("KRAKO_GPU_STATE", str(Path.home() / "krako-resource-control"))
)


def stamp(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).isoformat()


def observe():
    gpu = subprocess.check_output(
        [
            "nvidia-smi",
            "--query-gpu=uuid,name,memory.total,memory.used,utilization.gpu",
            "--format=csv,noheader,nounits",
        ],
        text=True,
        timeout=10,
    ).strip()
    raw = subprocess.check_output(
        [
            "nvidia-smi",
            "--query-compute-apps=pid,used_memory",
            "--format=csv,noheader,nounits",
        ],
        text=True,
        timeout=10,
    )
    jobs = []
    for line in raw.splitlines():
        pid, memory = [x.strip() for x in line.split(",")]
        try:
            group = Path("/proc", pid, "cgroup").read_text().strip()
        except FileNotFoundError:
            continue
        jobs.append({"pid": int(pid), "memory_mib": memory, "cgroup": group})
    return {"sampled_at": stamp(time.time()), "gpu_csv": gpu, "processes": jobs}


def check_busy(sample, allowed):
    # Exact cgroup component membership; never accept substring service names.
    unexpected = [
        p
        for p in sample["processes"]
        if not allowed or allowed not in p["cgroup"].split(":")[-1].split("/")
    ]
    if unexpected:
        raise RuntimeError("unregistered-or-unapproved GPU processes; no takeover")


def write_json(path, value):
    temp = path.with_suffix(".tmp")
    with temp.open("w") as f:
        json.dump(value, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("status")
    ac = sub.add_parser("acquire")
    ac.add_argument("--project", required=True)
    ac.add_argument("--owner", required=True)
    ac.add_argument("--purpose", required=True)
    ac.add_argument("--minutes", type=int, required=True)
    ac.add_argument("--unit", required=True)
    ac.add_argument("--handover-service", default="")
    for action in ["heartbeat", "release"]:
        p = sub.add_parser(action)
        p.add_argument("--lease-id", required=True)
        if action == "release":
            p.add_argument("--restored-service", default="")
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    with (ROOT / "board.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        path = ROOT / "active.json"
        lease = json.loads(path.read_text()) if path.exists() else None
        sample = observe()
        now = time.time()
        registry_path = ROOT / "services.json"
        registry = (
            json.loads(registry_path.read_text()) if registry_path.exists() else {}
        )
        for process in sample["processes"]:
            components = process["cgroup"].split(":")[-1].split("/")
            service = next((x for x in components if x.endswith(".service")), None)
            process["service"] = service
            if lease and lease["unit"] in components:
                process["declared_project"] = lease["project"]
                process["declared_owner"] = lease["owner"]
            else:
                process.update(
                    registry.get(
                        service,
                        {
                            "declared_project": "unregistered",
                            "declared_owner": "unknown",
                        },
                    )
                )
        board = {
            "lease": lease,
            "overdue": bool(lease and now > lease["expected_end_epoch"]),
            "observed": sample,
            "note": "Unleased GPU processes are occupied, never free. Cooperative, not GPU isolation.",
        }
        if args.action == "status":
            write_json(ROOT / "STATUS.json", board)
            lines = [
                "# H100 usage status",
                "",
                "Sampled: " + sample["sampled_at"],
                "",
                "GPU: " + sample["gpu_csv"],
                "",
            ]
            if lease:
                lines += [
                    "Project: " + lease["project"],
                    "Owner: " + lease["owner"],
                    "Purpose: " + lease["purpose"],
                    "Started: " + lease["started_at"],
                    "Expected end: " + lease["expected_end"],
                    "Elapsed minutes: "
                    + str(round((now - lease["started_epoch"]) / 60, 1)),
                    "Overdue: " + str(board["overdue"]),
                ]
            else:
                lines += [
                    "No declared lease. Inspect observed processes before acquiring."
                ]
            lines += [
                "",
                "Observed processes:",
                json.dumps(sample["processes"], indent=2),
            ]
            (ROOT / "STATUS.md").write_text("\n".join(lines) + "\n")
            print(json.dumps(board, indent=2))
            return
        if args.action == "acquire":
            if lease:
                raise RuntimeError(
                    "lease exists; expired leases are not automatically stolen"
                )
            if not 1 <= args.minutes <= 240:
                raise RuntimeError("minutes must be 1..240")
            check_busy(sample, args.handover_service)
            lease = {
                "schema_version": 1,
                "lease_id": str(uuid.uuid4()),
                "project": args.project,
                "owner": args.owner,
                "unix_user": getpass.getuser(),
                "purpose": args.purpose,
                "unit": args.unit,
                "started_at": stamp(now),
                "started_epoch": now,
                "expected_end": stamp(now + 60 * args.minutes),
                "expected_end_epoch": now + 60 * args.minutes,
                "heartbeat_at": stamp(now),
                "handover_service": args.handover_service,
            }
            write_json(path, lease)
        else:
            if not lease or lease["lease_id"] != args.lease_id:
                raise RuntimeError("lease ownership mismatch")
            if args.action == "heartbeat":
                lease["heartbeat_at"] = stamp(now)
                write_json(path, lease)
            else:
                if (
                    args.restored_service
                    and args.restored_service != lease["handover_service"]
                ):
                    raise RuntimeError("unexpected restored service")
                check_busy(sample, args.restored_service)
                lease["ended_at"] = stamp(now)
                lease["elapsed_seconds"] = now - lease["started_epoch"]
                path.unlink()
        record = {
            "event": args.action,
            "at": stamp(now),
            "lease": lease,
            "observed": sample,
        }
        with (ROOT / "history.jsonl").open("a") as history:
            history.write(json.dumps(record) + "\n")
            history.flush()
            os.fsync(history.fileno())
        print(json.dumps(record, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.SubprocessError) as exc:
        raise SystemExit(str(exc))
