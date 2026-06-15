#!/usr/bin/env python3
"""Run the public-safe KORA five-minute first-value workflow."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kora.five_minute_first_value import main


if __name__ == "__main__":
    raise SystemExit(main())
