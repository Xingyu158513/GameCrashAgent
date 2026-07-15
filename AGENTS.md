# Repository instructions

- Preserve the read-only safety boundary. Do not add repair, deletion, upload, device-control, driver-installation, or registry-write behavior without a separate approved design.
- Treat all diagnostic data as sensitive. Standard redaction must remain the default.
- Use Python's standard library for runtime code.
- Use UTF-8 for every text file.
- Run `python -m unittest discover -s tests -v` and `python -m compileall -q gamecrashagent main.py` after code changes.
- Add or update tests for every behavioral change.
- Analysis must distinguish evidence, hypothesis, and proven root cause.
- Never add real user logs, minidumps, credentials, hostnames, usernames, IP addresses, or MAC addresses to fixtures.
