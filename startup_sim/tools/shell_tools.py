from __future__ import annotations

import os
import shlex
import subprocess
from typing import List

from agents import function_tool

ALLOWED = ["echo", "ls", "pwd", "cat", "grep", "sed", "awk"]


def _run_command(command: str) -> str:
    parts = shlex.split(command)
    if not parts:
        return "No command provided"
    if parts[0] not in ALLOWED:
        raise ValueError(f"Command '{parts[0]}' not allowed")

    if os.getenv("STARTUP_SIM_REAL_SHELL") != "1":
        return f"SIMULATED: {' '.join(parts)}"

    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except Exception as exc:  # pragma: no cover - defensive
        return f"Execution failed: {exc}"

    output = (result.stdout or "") + (result.stderr or "")
    return output[:4000]


@function_tool
def shell_run_safe(command: str) -> str:
    return _run_command(command)
