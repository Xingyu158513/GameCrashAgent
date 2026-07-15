# Privacy

GameCrashAgent reads diagnostic metadata that may contain personal or device identifiers. It never uploads a report automatically.

## Data read by default

- recent minidump filenames, sizes, and timestamps;
- selected Windows System event fields and messages;
- network-adapter names, descriptions, status, driver information, and MAC address;
- configured driver file paths, versions, companies, sizes, and timestamps.

Minidump contents are not opened or parsed.

## Standard redaction

Standard redaction is enabled by default and replaces common usernames, computer names, Windows user-profile paths, IPv4 addresses, and MAC addresses. Redaction is best effort because arbitrary event providers may embed identifiers in unexpected formats.

Before attaching a report to a public issue:

1. open both generated reports;
2. search for your username, computer name, email address, IP addresses, and private paths;
3. remove any remaining private information;
4. attach only the smallest evidence needed to reproduce the problem.

`--redaction none` is intended only for local private analysis.

## Maintainer policy

Maintainers should immediately remove or hide public reports that expose secrets or unnecessary personal data. Public issue templates must never ask for raw minidump files, account credentials, authentication tokens, or complete unredacted event-log exports.
