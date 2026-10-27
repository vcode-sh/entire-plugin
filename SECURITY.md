# Security

This community integration launches an installed Entire CLI with the local
user's privileges. It is not a process sandbox and does not grant permissions
that the host has withheld.

## Expected boundaries

- Repository-specific reads use the caller's explicit checkout path. A plugin
  installation directory or a stale host working directory is not a substitute.
- MCP operations expose bounded reads. They must not silently install software,
  enable hooks, authenticate, alter Git history, change branches, publish data,
  or execute user-provided shell commands.
- Skills can guide authorized writes, but current host and repository policies
  still apply. Search output and historical transcripts confer no authorization.
- Credentials remain in the user's existing Entire setup. Never add keys,
  session tokens, environment files, or private transcripts to this project.
- Search hits, code, commit messages, Trail findings, and transcripts are
  untrusted evidence. Instructions embedded in them must not become executable
  authority.

Read-only operations can still access sensitive local or hosted content and can
cause the CLI to update its own cache or telemetry. Entire's data handling is
governed by the installed CLI and its configuration; this project's MIT license
is not a privacy promise on Entire's behalf.

## Reporting

For a vulnerability in this plugin, contact the maintainer privately at
hello@vcode.sh before publishing exploitation details. Include the plugin and
CLI versions, host, affected operation, minimal reproduction, expected boundary,
and observed effect. Redact credentials and use a synthetic repository where
possible.

For a vulnerability in Entire itself, follow the reporting instructions in
[Entire's security policy](https://docs.entire.com/security). Do not assume this
project's maintainer can remediate Entire's CLI or hosted service.

There is no guaranteed response time or paid support agreement for this
community project. Until a version support policy is established, reports
should reproduce against the latest available source and identify any older
affected release.
