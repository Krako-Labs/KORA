#!/usr/bin/env python3
"""Execute one reviewed owned-GPU packet inside its leased systemd unit."""

import argparse
import json
import os
import signal
from pathlib import Path

from kora.hero_live_execution import LiveServiceRequest
from kora.hero_remote_execution import (
    RemoteConfig,
    VllmController,
    run_remote_execution,
)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--packet", required=True, type=Path)
    p.add_argument("--request", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--runtime-log", required=True, type=Path)
    args = p.parse_args()
    if args.output.exists():
        p.error("output already exists")
    config = RemoteConfig.model_validate_json(args.packet.read_text())
    service = LiveServiceRequest.model_validate(
        json.loads(args.request.read_text())["service"]
    )
    cancelled = [False]

    def cancel(signum, frame):
        cancelled[0] = True

    signal.signal(signal.SIGTERM, cancel)
    signal.signal(signal.SIGINT, cancel)
    controller = VllmController(config, args.runtime_log)
    result = run_remote_execution(
        config, service, controller, cancelled=lambda: cancelled[0]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temp = args.output.with_suffix(".tmp")
    temp.write_text(
        json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    )
    os.replace(temp, args.output)
    print(
        json.dumps(
            {
                "run_id": result["run_id"],
                "verification": result["verification"],
                "actual_execution": result["actual_execution"],
            }
        )
    )
    return 0 if result["verification"]["objective_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
