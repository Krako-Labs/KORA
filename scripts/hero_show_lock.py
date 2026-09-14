#!/usr/bin/env python3
"""Create or verify a local replay-only show-build lock; no inference or release."""
import argparse
import json
import os
from pathlib import Path

from kora.studio_festa import LOCK_ENV, create_show_lock, preflight


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["create", "check"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == "create":
            lock = create_show_lock()
            # Exclusive creation preserves all prior show builds and evidence.
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(json.dumps(lock, indent=2, sort_keys=True) + "\n")
            print(json.dumps({"status": "created", "software_sha256": lock["software_sha256"]}))
        else:
            result = preflight({**os.environ, LOCK_ENV: str(args.output)})
            print(json.dumps({"ready": result["ready"], "checks": result["checks"]}, sort_keys=True))
            return 0 if result["ready"] else 1
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({"status": "rejected", "reason": "show_lock_or_evidence_invalid"}))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
