from __future__ import annotations

from pathlib import PureWindowsPath
from typing import Any


ACE_NAMES = {name.casefold() for name in ("ACE-BASE.sys", "ACE-ADVT.sys", "ACE-SSC-DRV64.sys", "WeGameDriver764.sys")}
WIFI_NAMES = {name.casefold() for name in ("rtwlane.sys", "vwififlt.sys", "vwifibus.sys", "wdiwifi.sys")}


def analyze_risk(data: dict[str, Any]) -> dict[str, Any]:
    drivers = data.get("drivers", {}).get("items", [])
    events = data.get("events", {}).get("items", [])
    adapters = data.get("network_adapters", {}).get("items", [])

    names = {
        PureWindowsPath(str(item.get("path", ""))).name.casefold()
        for item in drivers
        if item.get("exists")
    }
    ace_present = sorted(names & ACE_NAMES)
    wifi_present = sorted(names & WIFI_NAMES)
    relevant_adapters = [item for item in adapters if item.get("IsRelevant")]

    bugchecks = [
        item for item in events
        if "bugcheck" in str(item.get("ProviderName", "")).casefold() or item.get("Id") == 1001
    ]
    kernel_power = [
        item for item in events
        if "kernel-power" in str(item.get("ProviderName", "")).casefold() or item.get("Id") == 41
    ]
    whea = [item for item in events if "whea" in str(item.get("ProviderName", "")).casefold()]

    signals: list[str] = []
    if bugchecks:
        signals.append(f"Found {len(bugchecks)} recent BugCheck-related event(s).")
    if kernel_power:
        signals.append(f"Found {len(kernel_power)} recent Kernel-Power event(s).")
    if whea:
        signals.append(f"Found {len(whea)} recent WHEA hardware-error event(s).")
    if ace_present:
        signals.append("ACE or WeGame driver files are present: " + ", ".join(ace_present))
    if wifi_present:
        signals.append("Realtek or Windows Wi-Fi stack files are present: " + ", ".join(wifi_present))
    if relevant_adapters:
        adapter_names = [str(item.get("Name") or item.get("InterfaceDescription") or "unknown") for item in relevant_adapters]
        signals.append("Relevant network adapters were detected: " + ", ".join(adapter_names))

    if bugchecks and kernel_power and ace_present and wifi_present:
        level = "high"
        summary = (
            "Crash events and both anti-cheat and Wi-Fi driver-stack indicators are present. "
            "This supports the current investigation direction but does not prove root cause."
        )
    elif bugchecks or kernel_power or whea:
        level = "medium"
        summary = "Recent system-instability evidence exists and requires manual minidump and driver review."
    else:
        level = "low"
        summary = "No clear crash signal was found in the configured collection window."

    return {
        "level": level,
        "summary": summary,
        "signals": signals,
        "recommendations": [
            "Review BugCheckCode, probable cause, and stack modules in WinDbg.",
            "Compare Wi-Fi driver versions with the computer manufacturer's support page.",
            "Record game launcher and anti-cheat component versions before changing anything.",
            "Check WHEA, Display, Disk, and GPU-driver events before assuming a single-driver conflict.",
            "Require human confirmation and a backup before any driver, device, registry, or file change.",
        ],
    }
