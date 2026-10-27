---
name: memory-and-graph
description: Use when the user asks Entire Brain to retrieve or save project decisions, or Entire Graph to find implementations, trace relationships, or assess code impact. These optional CLI plugins must already be available or explicitly installed by the user.
---

# Use project memory and code relationships

Read [execution rules](../using-entire/references/execution.md).
Brain and Graph are separate Entire CLI plugins, not tools bundled here.
Check executable availability and installed help without installing or updating.
Report each extension independently as available, missing, unsupported, or
unverified; core Entire availability does not prove either extension works.
If a plugin is missing, explain the prerequisite and continue with core search,
Git, or local source when they can answer the question.

For external commands that `agent-help` does not describe, use their documented
help surface: `entire graph help`, `entire graph <command> --help`, or
`entire brain --help`. Do not pass core CLI flags indiscriminately.

## Brain

Use installed read/query operations to retrieve a task brief, project overview,
saved rules, or broader history/docs. Verify the cited sources and freshness.
Brain's documented `query` uses keyword ranking; do not promise semantic
matching from a deprecated `--semantic` flag.
Treat a memory or task brief as a lead to its sources, not a replacement for
current user instructions, code, or configuration. Do not execute a remembered
command just because a prior session used it.

Save a memory only when the user asks to remember it or otherwise explicitly
authorizes that write. Preserve their wording, choose the narrowest appropriate
scope, and use global scope only when requested. Do not save tentative
inferences as project rules. Imports, retractions, refreshes, exports that
rewrite a directory, webhook configuration, and setup also change state.

## Graph

Use the installed agent guide and help to choose a targeted query, definition,
neighbors, impact, or diff. Prefer an existing committed-tree cache when the
question concerns committed code; inspect the working tree when current edits
matter. Read returned source locations before concluding what a change affects.
Report coverage gaps rather than interpreting missing edges as absence.

Do not build a full index or export a complete graph for a simple lookup.
Do not run setup that edits instructions or hooks without authorization.
Graph `verify` executes the supplied shell command; treat that command with
the same scrutiny and permissions as direct execution. Transcript statistics
are outside ordinary code discovery and should be run only when requested.
