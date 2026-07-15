from __future__ import annotations

import json
import subprocess
from datetime import datetime
from typing import Any


def now_local_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def run_powershell_json(command: str, timeout: int = 30) -> tuple[list[dict[str, Any]], str | None]:
    """Run a read-only PowerShell query and return a normalized list of objects."""
    preamble = """
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
"""
    try:
        completed = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                preamble + command,
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        return [], "PowerShell was not found. GameCrashAgent currently supports Windows only."
    except subprocess.TimeoutExpired:
        return [], f"PowerShell query exceeded the {timeout}-second timeout."

    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "PowerShell query failed."
        return [], message

    output = completed.stdout.strip()
    if not output:
        return [], None

    try:
        parsed = json.loads(output)
    except json.JSONDecodeError as exc:
        return [], f"PowerShell returned invalid JSON: {exc}"

    if isinstance(parsed, dict):
        return [parsed], None
    if isinstance(parsed, list):
        return [item for item in parsed if isinstance(item, dict)], None
    return [], "PowerShell JSON must contain an object or an array of objects."
