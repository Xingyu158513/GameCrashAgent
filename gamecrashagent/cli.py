from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from . import __version__
from .collectors import collect_all
from .privacy import redact_data
from .reporting import build_json_report, build_markdown_report
from .risk import analyze_risk


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = PROJECT_ROOT / "config.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gamecrashagent",
        description="Collect read-only Windows game-crash evidence and generate privacy-redacted reports.",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to JSON configuration.")
    parser.add_argument("--format", choices=("markdown", "json", "both"), default="both")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "reports" / "latest_report.md")
    parser.add_argument("--json-output", type=Path, default=PROJECT_ROOT / "reports" / "latest_report.json")
    parser.add_argument(
        "--redaction",
        choices=("standard", "none"),
        default="standard",
        help="Privacy redaction is enabled by default. Use 'none' only for local private analysis.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def load_config(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Configuration file was not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Configuration contains invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError("Configuration root must be a JSON object.")
    return data


def run(args: argparse.Namespace) -> list[Path]:
    config = load_config(args.config)
    data = collect_all(config)
    data["risk"] = analyze_risk(data)
    if args.redaction == "standard":
        data = redact_data(data)
    else:
        data["privacy"] = {
            "redacted": False,
            "mode": "none",
            "notice": "This report may contain identifying system information. Do not share it publicly.",
        }

    written: list[Path] = []
    if args.format in ("markdown", "both"):
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(build_markdown_report(data), encoding="utf-8")
        written.append(args.output)
    if args.format in ("json", "both"):
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(build_json_report(data), encoding="utf-8")
        written.append(args.json_output)
    return written


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        written = run(args)
    except (RuntimeError, OSError) as exc:
        print(f"GameCrashAgent failed: {exc}", file=sys.stderr)
        return 1

    for path in written:
        print(f"Created: {path}")
    if args.redaction == "standard":
        print("Privacy redaction was applied. Review the report before sharing it.")
    else:
        print("WARNING: privacy redaction was disabled. Keep this report private.")
    return 0
