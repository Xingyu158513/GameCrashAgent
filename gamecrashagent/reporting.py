from __future__ import annotations

import json
from typing import Any

from . import __version__
from .common import now_local_iso


def build_json_report(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def build_markdown_report(data: dict[str, Any]) -> str:
    risk = data.get("risk", {})
    privacy = data.get("privacy", {})
    lines = [
        f"# GameCrashAgent v{__version__} Diagnostic Report",
        "",
        f"- Generated: {now_local_iso()}",
        "- Mode: read-only evidence collection",
        f"- Privacy redaction: {'enabled' if privacy.get('redacted') else 'disabled'}",
        "- Safety: no settings, devices, drivers, registry keys, or user files were modified.",
        "",
    ]
    lines.extend(_minidumps(data.get("minidumps", {})))
    lines.extend(_events(data.get("events", {})))
    lines.extend(_network(data.get("network_adapters", {})))
    lines.extend(_drivers(data.get("drivers", {})))
    lines.extend([
        "## Initial Risk Assessment",
        "",
        f"- Level: **{risk.get('level', 'unknown')}**",
        f"- Summary: {_clean(risk.get('summary', 'No assessment available.'))}",
        "",
        "### Evidence Signals",
        "",
    ])
    signals = risk.get("signals", [])
    lines.extend(f"- {_clean(signal)}" for signal in signals)
    if not signals:
        lines.append("- No configured high-confidence signal was collected.")
    lines.extend(["", "### Manual Next Steps", ""])
    lines.extend(f"- {_clean(item)}" for item in risk.get("recommendations", []))
    lines.extend(_errors(data))
    return "\n".join(lines).rstrip() + "\n"


def _minidumps(section: dict[str, Any]) -> list[str]:
    lines = ["## Recent Minidump Files", "", f"- Directory: `{_clean(section.get('directory', ''))}`", ""]
    items = section.get("items", [])
    if not items:
        return lines + ["No readable `.dmp` files were found.", ""]
    lines.extend(["| File | Size | Modified |", "|---|---:|---|"])
    for item in items:
        lines.append(f"| `{_clean(item.get('name', ''))}` | {_format_bytes(item.get('size_bytes'))} | {_clean(item.get('modified_time_text', ''))} |")
    return lines + [""]


def _events(section: dict[str, Any]) -> list[str]:
    lines = [
        "## Recent System Events",
        "",
        f"- Log: `{_clean(section.get('log_name', 'System'))}`",
        f"- Window: last {section.get('hours', '')} hour(s)",
        "",
    ]
    items = section.get("items", [])
    if not items:
        return lines + ["No matching event was found, or access was restricted.", ""]
    lines.extend(["| Time | ID | Level | Provider | Summary |", "|---|---:|---|---|---|"])
    for item in items[:80]:
        lines.append(
            f"| {_clean(item.get('TimeCreated', ''))} | {item.get('Id', '')} | {_clean(item.get('LevelDisplayName', ''))} | "
            f"`{_clean(item.get('ProviderName', ''))}` | {_trim(item.get('Message', ''), 180)} |"
        )
    if len(items) > 80:
        lines.append(f"| | | | | Showing 80 of {len(items)} collected events. |")
    return lines + [""]


def _network(section: dict[str, Any]) -> list[str]:
    lines = ["## Network Adapters", ""]
    items = section.get("items", [])
    if not items:
        return lines + ["No network-adapter data was collected.", ""]
    lines.extend(["| Relevant | Name | Description | Status | Link speed | Matched keywords |", "|---|---|---|---|---|---|"])
    for item in items:
        lines.append(
            "| {relevant} | `{name}` | {description} | {status} | {speed} | {keywords} |".format(
                relevant="yes" if item.get("IsRelevant") else "",
                name=_clean(item.get("Name", "")),
                description=_trim(item.get("InterfaceDescription", ""), 80),
                status=_clean(item.get("Status", "")),
                speed=_clean(item.get("LinkSpeed", "")),
                keywords=_clean(", ".join(item.get("MatchedKeywords", []))),
            )
        )
    return lines + [""]


def _drivers(section: dict[str, Any]) -> list[str]:
    lines = ["## Configured Driver Files", ""]
    items = section.get("items", [])
    if not items:
        return lines + ["No driver path was configured.", ""]
    lines.extend(["| Exists | Path | File version | Company | Modified | Size |", "|---|---|---|---|---|---:|"])
    for item in items:
        lines.append(
            "| {exists} | `{path}` | {version} | {company} | {modified} | {size} |".format(
                exists="yes" if item.get("exists") else "no",
                path=_clean(item.get("path", "")),
                version=_clean(item.get("version") or ""),
                company=_trim(item.get("company_name") or "", 50),
                modified=_clean(item.get("modified_time_text") or ""),
                size=_format_bytes(item.get("size_bytes")),
            )
        )
    return lines + [""]


def _errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for section_name, section in data.items():
        if not isinstance(section, dict):
            continue
        errors.extend(f"{section_name}: {error}" for error in section.get("errors", []))
        for item in section.get("items", []):
            if isinstance(item, dict):
                errors.extend(f"{section_name}: {error}" for error in item.get("errors", []))
    if not errors:
        return []
    return ["", "## Collection Warnings", "", *(f"- {_clean(error)}" for error in errors), ""]


def _format_bytes(value: Any) -> str:
    if value in (None, ""):
        return ""
    try:
        size = float(value)
    except (TypeError, ValueError):
        return _clean(value)
    units = ["B", "KB", "MB", "GB"]
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{size:.1f} {units[index]}"


def _clean(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def _trim(value: Any, limit: int) -> str:
    clean = _clean(value)
    return clean if len(clean) <= limit else clean[: limit - 3] + "..."
