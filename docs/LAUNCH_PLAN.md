# Six-week public launch plan

## Week 1: identity and first release

- Create a public GitHub repository named `GameCrashAgent`.
- Make the first reviewed commit with the maintainer's real Git identity or GitHub noreply email.
- Push `main`, enable Issues and private vulnerability reporting, and confirm Actions can run.
- Create the `v0.2.0` release from the verified Windows archive.

Exit condition: a new user can understand, download, run, and remove the tool without private instructions.

## Week 2: recruit initial testers

- Invite five Windows 10/11 users with different hardware.
- Ask them to use the bug template and attach only manually reviewed, redacted evidence.
- Record installation failures, collection warnings, false-positive signals, and unclear documentation.

Exit condition: at least three independent machines complete a report.

## Week 3: close real issues

- Triage every issue within 72 hours.
- Add tests before each fix.
- Publish `v0.2.1` when the first validated fixes are ready.
- Document unsupported scenarios instead of guessing.

Exit condition: at least three public issues are resolved with reproducible evidence.

## Week 4: broaden safely

- Add one diagnostic profile only if multiple reports justify it.
- Keep new collection fields opt-in until privacy review is complete.
- Improve report explanations without presenting hypotheses as proven causes.

Exit condition: the new profile has fixtures, tests, privacy documentation, and a maintainer review.

## Week 5: maintainer automation

- Add issue-labeling guidance for redacted diagnostic reports.
- Add release-note generation and duplicate-issue review prompts.
- Document the planned Codex API workflow; do not send private reports automatically.

Exit condition: API-credit use cases are tied to public maintenance work, not a vague product idea.

## Week 6: apply

- Record stars, release downloads, external users, issues closed, releases, and contributors.
- Replace every placeholder in `CODEX_FOR_OSS_APPLICATION.md`.
- Review the application for accuracy and remove confidential information.
- Submit once, then continue maintaining the project while review is pending.
