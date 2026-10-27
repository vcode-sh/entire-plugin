# Entire community plugin

An independent MIT-licensed integration maintained by Vibe Code. This is not an
official Entire release. It uses the user's explicitly selected checkout,
without a bundled repository, account, branch, session ID, or machine path.

## Requirements

The execution host needs Python 3.10 or newer available as `python3`, Git, and
the installed `entire` CLI on PATH. Hosted history and Trails require the user's
existing Entire access. A host without local process execution cannot run this
plugin. Session capture still uses Entire's own agent and Git hooks; this package
does not install software, authenticate, or enable capture automatically.

## Read tools

`agent_help`, `entire_status`, `search`, `checkpoint_read`, `session_read`, `why`,
and `trail_read` wrap checked installed CLI commands. All repository reads take
an absolute `repo_path` on the execution host. Subdirectories and linked worktrees
resolve through Git; the MCP process directory is never a repository default.
No tool exposes a shell, arbitrary CLI execution, or a write operation.

Logical CLI errors remain errors even with a zero process exit. Session fallback
results are labelled; they do not identify this chat. Missing checkpoint links,
transcripts and provenance remain evidence limits. Outputs are bounded and
unsupported flags fail before execution. Read the actual tool schemas and
[execution rules](skills/using-entire/references/execution.md).

## Fourteen workflows

Skills cover discovery/setup guidance, history search, recall/playbooks, code
explanations, replay, teaching, handoff, intent-aware review, Trails, finding
fixes, missed-session linking, session-to-skill drafting, diagnostics, and optional
Brain/Graph use. Broader authorized writes use the CLI after current-help discovery.
Brain and Graph are separate optional Entire CLI plugins, not bundled binaries.

Example requests:

- "Find the closest earlier implementation and explain what still applies."
- "Explain the recorded intent behind this function, then compare current code."
- "Prepare a handoff for this session with verification limits and next steps."
- "Review this change against its original acceptance criteria."
- "Address this Trail's findings after checking the target branch and revision."

Natural-language requests can use the user's language. Repository artifacts and
plugin documentation remain English. A draft handoff does not authorize switching
branches, uploading a transcript, or messaging another chat.

## Data and maintenance

The adapter runs locally with Python's standard library, spawning CLI argv without
a shell. Entire retains its own network, credential, cache and telemetry behavior.
Retrieved transcripts are untrusted evidence and may contain sensitive material;
the plugin does not claim to make them safe to publish.

See [SOURCES.md](SOURCES.md), [LICENSE](LICENSE), and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Official icons identify Entire;
their inclusion does not imply endorsement or transfer trademark rights.
