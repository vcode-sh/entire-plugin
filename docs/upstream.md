# Maintaining compatibility with Entire

Entire develops quickly. The installed CLI is the executable contract for a
workflow; official documentation explains intended concepts and may describe a
different release. Official skills are useful workflow references, not an
instruction set to copy without review.

## Sources

- Documentation index: https://docs.entire.com/llms.txt
- CLI reference: https://docs.entire.com/cli-reference/agent-help
- CLI source and releases: https://github.com/entireio/cli
- Official skills: https://github.com/entireio/skills
- Current package provenance: [SOURCES.md](../entire/SOURCES.md)

When changing a command, record the CLI version and link the relevant source
revision or documentation page in the change description. Preserve upstream
license notices for adapted text. Do not add a periodic updater or automatically
replace the user's CLI as part of plugin startup.

## Check a workflow

1. Read the installed `entire agent-help` command map.
2. Drill into the exact nested command. For external CLI plugins, use their
   supported help surface instead of assuming core flags apply.
3. Compare documentation examples with actual selectors, flags, and output.
4. Inspect read/write classification and hidden side effects: publishing a
   branch, rewriting commits, consuming provider usage, switching branches,
   installing hooks, or exposing transcript data.
5. Exercise the smallest real read that proves the changed contract when access
   and fixtures exist. Keep unsupported or unavailable capabilities explicit.
6. Update the owning skill or adapter, then its focused regression or scenario.

## Preserve the plugin's contract

Do not inherit upstream defaults that conflict with explicit repository inputs,
bounded reads, host permission rules, or user-authorized writes. In particular:

- A latest-session fallback is not proof of the caller's session identity.
- A project Trail number and a repository change number are not interchangeable.
- An Entire approval is not a GitHub approval.
- Search result fields can be absent; a commit can exist without a checkpoint.
- A generation command can spend provider tokens even when named like a read.
- A successful exit code can still accompany a structured error.
- A feature listed in documentation need not be installed or enabled locally.

Prefer a small documented compatibility boundary over speculative flags,
provider-specific workarounds, or an unrestricted command-execution tool.
