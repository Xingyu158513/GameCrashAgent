# Contributing

Thank you for helping improve GameCrashAgent.

## Before opening code

- Search existing issues.
- For a new collector or a change to the safety boundary, open a design issue first.
- Never post raw private logs, minidumps, credentials, or unredacted reports.

## Development setup

```powershell
git clone <repository-url>
cd GameCrashAgent
python -m unittest discover -s tests -v
python -m compileall -q gamecrashagent main.py
```

The runtime must remain standard-library only unless a maintainer approves a dependency through a design issue.

## Pull-request requirements

- Preserve the read-only default.
- Add tests for behavior changes.
- Use UTF-8 text files.
- Keep analysis language conservative; signals are not proof of root cause.
- Update privacy documentation if a new field is collected.
- Do not silently broaden the collection scope.

## Commit guidance

Use focused commits with an imperative subject, for example:

```text
Add redaction for Windows user-profile paths
```
