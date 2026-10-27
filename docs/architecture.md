# Architecture

## Owners

The plugin has three responsibilities:

1. A local MCP adapter provides explicit repository context and bounded read
   operations through the installed Entire CLI.
2. Skills turn a user's task into a small sequence of evidence reads and,
   where authorized, documented CLI actions.
3. Packaging validates the installable files and creates an archive. It does not
   install Entire, set up repositories, or publish source.

The CLI owns Entire behavior and authentication. This project does not reimplement
its search service, checkpoint store, Trail model, agent capture hooks, or
provider-backed generation.

## Repository context

Every repository-specific adapter call receives an explicit `repo_path`.
Resolve and validate that path before running the CLI. Derive the repository
root and identity from that checkout rather than from the plugin's startup
directory. Paths and remote identities are different values: a local path
selects the checkout; a forge-prefixed identity selects hosted repository scope.

Do not persist the last repository as a global default. Independent clients and
worktrees can operate concurrently. A call for one checkout must not affect the
next call's working directory or repository scope.

No origin, no checkpoint coverage, disabled capture, missing access, unavailable
optional plugins, and an invalid Git directory are different conditions. They
must not collapse into the same advice to enable or authenticate.

## Command boundary

The adapter uses argument arrays and a per-call working directory. It must not
accept an arbitrary shell command or arbitrary CLI argument list as a tool.
Read tools discover supported syntax from the installed help surface and return
an actionable capability error when the required operation is unavailable.

Bound execution time, output, result count, and transcript reads. Preserve CLI
errors without dumping credentials or unrelated transcript content. Inspect
JSON error envelopes as well as exit status.

Mutations remain visible in skills. A request to inspect a Trail does not
authorize creating it; a handoff does not authorize switching branches; a
commit does not authorize a push. A setup request must identify its scope rather
than treating the presence of this plugin as blanket consent.

## Evidence boundary

Keep four kinds of evidence distinct:

- Recorded intent: what the inspected prompt or session actually says.
- Current source: what the selected checkout currently implements.
- Verification: the command, revision, and environment actually checked.
- Inference: a reasoned conclusion that is not directly recorded.

A successful search can return ordinary commits without linked checkpoints.
An enabled status is not proof of complete capture. A passing transport test
does not prove the agent selected the correct workflow. Missing graph edges do
not prove missing relationships.

## Runtime and distribution

Python's standard library is the runtime boundary; no package-manager download
belongs in MCP startup. The host must provide Python and Entire on its execution
machine. Source and account-release tooling are separate from the installable
plugin so contributors do not inherit the creator's account identity or machine.
