from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .common import run_powershell_json


def collect_all(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "minidumps": collect_minidumps(config),
        "events": collect_system_events(config),
        "network_adapters": collect_network_adapters(config),
        "drivers": collect_driver_status(config),
    }


def collect_minidumps(config: dict[str, Any]) -> dict[str, Any]:
    directory = Path(config.get("minidump_dir", r"C:\Windows\Minidump"))
    limit = max(0, int(config.get("minidump_limit", 5)))
    result: dict[str, Any] = {"directory": str(directory), "items": [], "errors": []}

    try:
        if not directory.exists():
            result["errors"].append(f"Directory does not exist or is inaccessible: {directory}")
            return result

        dumps = sorted(directory.glob("*.dmp"), key=lambda path: path.stat().st_mtime, reverse=True)
        for path in dumps[:limit]:
            stat = path.stat()
            result["items"].append(
                {
                    "name": path.name,
                    "path": str(path),
                    "size_bytes": stat.st_size,
                    "modified_time": stat.st_mtime,
                    "modified_time_text": _format_timestamp(stat.st_mtime),
                }
            )
    except PermissionError:
        result["errors"].append(f"Permission denied while reading: {directory}")
    except OSError as exc:
        result["errors"].append(f"Failed to read minidump metadata: {exc}")
    return result


def collect_system_events(config: dict[str, Any]) -> dict[str, Any]:
    hours = max(1, min(168, int(config.get("event_log_hours", 6))))
    log_name = str(config.get("event_log_name", "System"))
    providers = [str(value) for value in config.get("event_providers", [])]
    provider_array = "@(" + ",".join(_ps_quote(provider) for provider in providers) + ")"

    command = f"""
$ErrorActionPreference = 'Stop'
$providers = {provider_array}
$startTime = (Get-Date).AddHours(-{hours})
Get-WinEvent -FilterHashtable @{{LogName={_ps_quote(log_name)}; StartTime=$startTime}} -ErrorAction Stop |
    Where-Object {{
        $providerName = [string]$_.ProviderName
        $message = [string]$_.Message
        ($providers -contains $providerName) -or
        ($providers | Where-Object {{ $providerName -like "*$_*" -or $message -like "*$_*" }})
    }} |
    Select-Object -First 200 @{{Name='TimeCreated'; Expression={{$_.TimeCreated.ToString('s')}}}},
        Id, LevelDisplayName, ProviderName, LogName,
        @{{Name='Message'; Expression={{([string]$_.Message -replace '\r?\n', ' ')}}}} |
    ConvertTo-Json -Depth 3
"""
    items, error = run_powershell_json(command, timeout=60)
    return {
        "log_name": log_name,
        "hours": hours,
        "providers": providers,
        "items": items,
        "errors": [error] if error else [],
    }


def collect_network_adapters(config: dict[str, Any]) -> dict[str, Any]:
    keywords = [str(value) for value in config.get("network_keywords", [])]
    command = """
$ErrorActionPreference = 'Stop'
Get-NetAdapter -IncludeHidden |
    Select-Object Name, InterfaceDescription, Status, MacAddress, LinkSpeed, DriverInformation, ifIndex |
    ConvertTo-Json -Depth 4
"""
    items, error = run_powershell_json(command, timeout=30)
    normalized: list[dict[str, Any]] = []
    for item in items:
        haystack = " ".join(
            str(item.get(key, "")) for key in ("Name", "InterfaceDescription", "DriverInformation")
        )
        matches = [keyword for keyword in keywords if keyword.casefold() in haystack.casefold()]
        normalized.append({**item, "MatchedKeywords": matches, "IsRelevant": bool(matches)})

    return {
        "keywords": keywords,
        "items": normalized,
        "errors": [error] if error else [],
    }


def collect_driver_status(config: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {"items": [], "errors": []}
    for configured_path in config.get("driver_paths", []):
        driver_path = str(configured_path)
        path = Path(driver_path)
        item: dict[str, Any] = {
            "path": driver_path,
            "exists": path.exists(),
            "size_bytes": None,
            "modified_time_text": None,
            "version": None,
            "product_version": None,
            "company_name": None,
            "description": None,
            "errors": [],
        }
        if path.exists():
            try:
                stat = path.stat()
                item["size_bytes"] = stat.st_size
                item["modified_time_text"] = _format_timestamp(stat.st_mtime)
            except OSError as exc:
                item["errors"].append(f"Failed to read file metadata: {exc}")

            rows, error = _read_version_info(driver_path)
            if error:
                item["errors"].append(error)
            elif rows:
                version = rows[0]
                item["version"] = version.get("FileVersion")
                item["product_version"] = version.get("ProductVersion")
                item["company_name"] = version.get("CompanyName")
                item["description"] = version.get("FileDescription")
        result["items"].append(item)
    return result


def _read_version_info(path: str) -> tuple[list[dict[str, Any]], str | None]:
    command = f"""
$ErrorActionPreference = 'Stop'
(Get-Item -LiteralPath {_ps_quote(path)}).VersionInfo |
    Select-Object FileVersion, ProductVersion, CompanyName, FileDescription |
    ConvertTo-Json -Depth 2
"""
    return run_powershell_json(command, timeout=20)


def _ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).astimezone().isoformat(timespec="seconds")
