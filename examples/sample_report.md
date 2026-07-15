# GameCrashAgent v0.2.0 Diagnostic Report

- Generated: 2026-07-15T12:00:00+08:00
- Mode: read-only evidence collection
- Privacy redaction: enabled
- Safety: no settings, devices, drivers, registry keys, or user files were modified.

## Recent Minidump Files

- Directory: `C:\Windows\Minidump`

| File | Size | Modified |
|---|---:|---|
| `071526-10000-01.dmp` | 3.8 MB | 2026-07-15T11:40:00+08:00 |

## Recent System Events

- Log: `System`
- Window: last 6 hour(s)

| Time | ID | Level | Provider | Summary |
|---|---:|---|---|---|
| 2026-07-15T11:40:02 | 1001 | Error | `Microsoft-Windows-WER-SystemErrorReporting` | The computer rebooted from a bugcheck. |
| 2026-07-15T11:39:58 | 41 | Critical | `Microsoft-Windows-Kernel-Power` | The system rebooted without cleanly shutting down. |

## Network Adapters

| Relevant | Name | Description | Status | Link speed | Matched keywords |
|---|---|---|---|---|---|
| yes | `Wi-Fi` | Realtek Wireless LAN Adapter | Up | 433 Mbps | Realtek Wireless, Wi-Fi |

## Configured Driver Files

| Exists | Path | File version | Company | Modified | Size |
|---|---|---|---|---|---:|
| yes | `C:\Windows\System32\drivers\rtwlane.sys` | 1.0.0.0 | Example Vendor | 2026-01-01T00:00:00+08:00 | 1.2 MB |

## Initial Risk Assessment

- Level: **medium**
- Summary: Recent system-instability evidence exists and requires manual minidump and driver review.

This example is synthetic and contains no real user's diagnostic data.
