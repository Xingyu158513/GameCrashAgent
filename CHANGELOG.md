# Changelog

All notable changes will be documented here.

## [Unreleased]

### Planned

- Portable Windows release archive.
- Additional diagnostic profiles based on validated public issues.

## [0.2.1] - 2026-07-18

### Fixed

- Redact valid IPv6 addresses, including compressed, scoped, and IPv4-mapped forms, before reports are shared.
- Preserve non-address text containing colons, such as event timestamps and Windows paths.

## [0.2.0] - 2026-07-15

### Added

- Privacy redaction enabled by default.
- Markdown and JSON report formats.
- Command-line options for config, output, format, and redaction mode.
- Standard-library unit tests.
- Windows GitHub Actions workflow.
- Privacy, security, support, and contribution policies.

### Changed

- Rebuilt corrupted source strings as UTF-8-safe English messages.
- Clarified that risk signals do not prove root cause.
