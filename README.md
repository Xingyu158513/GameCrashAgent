# GameCrashAgent

Privacy-first, read-only Windows game-crash evidence collection.

[![tests](https://github.com/Xingyu158513/GameCrashAgent/actions/workflows/tests.yml/badge.svg)](https://github.com/Xingyu158513/GameCrashAgent/actions/workflows/tests.yml)
[![release](https://img.shields.io/github/v/release/Xingyu158513/GameCrashAgent)](https://github.com/Xingyu158513/GameCrashAgent/releases/latest)

GameCrashAgent gathers the first layer of evidence for blue screens, black screens, and unexpected reboots that occur around games or game launchers. It generates Markdown and JSON reports without modifying drivers, devices, registry keys, system settings, or user files.

> 当前版本来自真实 Windows 游戏崩溃排查场景，现已作为开源版本发布。默认启用隐私脱敏，运行后仍应由用户检查报告，再决定是否分享。

## Why this project exists

Crash evidence is usually scattered across minidump metadata, Windows Event Logs, network adapters, and driver file versions. Collecting it manually is repetitive and easy to get wrong. GameCrashAgent creates a consistent evidence package for human or AI-assisted review while preserving a strict read-only boundary.

The initial investigation profile focuses on possible overlap between:

- game launcher or anti-cheat drivers;
- Realtek and Windows virtual Wi-Fi components;
- BugCheck, Kernel-Power, WHEA, display, disk, and GPU-driver events.

These signals support an investigation direction. They do not prove root cause.

## Safety boundary

GameCrashAgent does not:

- change system settings;
- enable or disable devices;
- install, update, or remove drivers;
- write to the registry;
- delete or upload files;
- execute or parse minidump contents;
- apply automated repairs.

PowerShell is used only for read-only queries: `Get-WinEvent`, `Get-NetAdapter`, and `Get-Item`.

## Privacy defaults

Standard redaction is enabled by default. It removes common:

- Windows usernames and user-profile paths;
- computer names;
- IPv4 and IPv6 addresses;
- MAC addresses.

Redaction reduces accidental disclosure but cannot guarantee that every identifier inside arbitrary event-log text is removed. Always review a report before publishing it. See [PRIVACY.md](PRIVACY.md).

## Requirements

- Windows 10 or Windows 11
- Python 3.11 or newer
- Administrator permission is recommended, but not required

The runtime uses only the Python standard library.

## Download

Download the verified Windows archive and its SHA-256 checksum from the [latest release](https://github.com/Xingyu158513/GameCrashAgent/releases/latest).

The archive still requires Python 3.11 or newer; it is not a standalone executable.

## Quick start

```powershell
python .\main.py
```

Default outputs:

```text
reports\latest_report.md
reports\latest_report.json
```

Other examples:

```powershell
# Markdown only
python .\main.py --format markdown

# Use a custom config and output path
python .\main.py --config .\config.json --output .\reports\case-001.md

# Local private analysis without redaction (do not share the result)
python .\main.py --redaction none
```

You can also run:

```powershell
.\scripts\run.ps1
```

## Test

```powershell
python -m unittest discover -s tests -v
python -m compileall -q gamecrashagent main.py
```

## Project structure

```text
gamecrashagent/
  cli.py          command-line entry point
  collectors.py   read-only Windows evidence collectors
  privacy.py      recursive privacy redaction
  reporting.py    Markdown and JSON rendering
  risk.py         conservative signal analysis
tests/            standard-library unit tests
examples/         sanitized sample output
scripts/          run and packaging helpers
```

## Current limitations

- Windows only.
- Does not parse minidump stacks.
- Does not prove causation.
- Event wording varies by Windows language and provider.
- Some evidence may be unavailable without administrator permission.
- The initial driver profile is intentionally narrow and must grow through real issue reports.

## Roadmap

- `v0.2`: privacy-first Markdown and JSON reports, tests, Windows CI, and a verified release archive
- `v0.2.1`: fixes driven by the first external tester reports
- `v0.3`: broader hardware profiles backed by public issue evidence
- `v0.4`: optional import of a user-provided WinDbg text summary
- `v0.5`: explicit-consent support-bundle export

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Any change that introduces system mutation, upload behavior, or automatic remediation requires a separate design discussion and must not be enabled by default.

## License

MIT. See [LICENSE](LICENSE).
