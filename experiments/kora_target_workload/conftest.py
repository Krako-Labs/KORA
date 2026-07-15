"""Make this experiment's own `kora` package win over the repo-root one.

The repo-root pyproject sets `pythonpath = ["."]`, which puts the repository
root on `sys.path` ahead of everything else. The root ships a `kora/` package
(cli, executor, adapters) and this directory ships a different `kora/` package
(dispatcher, format_rules, kb_match, policy_rules). Without this file the root
package shadows the local one, so running `pytest` from this directory failed
during collection with `ModuleNotFoundError: No module named 'kora.dispatcher'`.

Prepending this directory restores the local package, so a plain `pytest` in
this directory works with no environment setup and no flags.
"""

from __future__ import annotations

import sys
from pathlib import Path

_HERE = str(Path(__file__).resolve().parent)

if _HERE in sys.path:
    sys.path.remove(_HERE)
sys.path.insert(0, _HERE)
