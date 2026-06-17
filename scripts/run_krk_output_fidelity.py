#!/usr/bin/env python3
"""Run KRK baseline equivalence and output fidelity evaluation."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from kora.output_fidelity import main


if __name__ == "__main__":
    raise SystemExit(main())
