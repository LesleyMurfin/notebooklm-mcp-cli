#!/usr/bin/env python3
"""Close Orca terminals on ORCA_WORKTREE_PATH. Used by orca.yaml archive hook."""
from __future__ import annotations

import json
import os
import subprocess
import sys


def main() -> int:
    mtl = os.environ.get("MTL_ENV_ID", "1522e07a-633a-4df5-8da0-f079198ef4d3")
    path = os.environ.get("ORCA_WORKTREE_PATH", "")
    try:
        data = json.load(sys.stdin)
    except Exception as exc:  # noqa: BLE001
        print(f"[orca archive] terminal list parse skip: {exc}")
        return 0

    closed = 0
    for term in (data.get("result") or {}).get("terminals") or []:
        if str(term.get("worktreePath") or "") != path:
            continue
        handle = term.get("handle")
        if not handle:
            continue
        result = subprocess.run(
            [
                "orca",
                "terminal",
                "close",
                "--environment",
                mtl,
                "--terminal",
                handle,
                "--json",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        print(f"[orca archive] close {handle} rc={result.returncode}")
        closed += 1
    print(f"[orca archive] closed_n={closed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
