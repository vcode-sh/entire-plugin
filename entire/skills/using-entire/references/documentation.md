# Documentation map

Checked against the public documentation and Entire CLI 0.12.2 on 2026-10-27.
These are navigation pointers, not frozen command specifications. Fetch only
the relevant page, and prefer installed help for executable commands.

- [Complete index](https://docs.entire.com/llms.txt)
- [Introduction](https://docs.entire.com/)
- [Installation](https://docs.entire.com/installation)
- [Quickstart](https://docs.entire.com/quickstart)
- [Agent help](https://docs.entire.com/cli-reference/agent-help)
- [Native MCP server](https://docs.entire.com/cli-reference/mcp)
- [Official skills](https://docs.entire.com/learn/skills-overview)
- [Official skills source](https://github.com/entireio/skills)
- [Code and history search](https://docs.entire.com/guides/search/search-in-cli)
- [Inspect checkpoints](https://docs.entire.com/guides/checkpoints/inspect-in-cli)
- [Inspect sessions](https://docs.entire.com/guides/sessions/inspect-sessions-in-cli)
- [Session command and resolution semantics](https://docs.entire.com/cli-reference/session)
- [Resume sessions](https://docs.entire.com/guides/sessions/resume-sessions)
- [Trails](https://docs.entire.com/guides/trails/overview)
- [Trail commands](https://docs.entire.com/cli-reference/trail)
- [Trail gates](https://docs.entire.com/guides/trails/gates)
- [Agent configuration](https://docs.entire.com/guides/trails/agents)
- [Dispatches](https://docs.entire.com/guides/dispatches/dispatches-in-cli)
- [Brain workflows](https://docs.entire.com/guides/brain/quickstart)
- [Graph reference](https://docs.entire.com/cli-reference/graph)
- [Codex integration](https://docs.entire.com/agents/codex)
- [All supported agents](https://docs.entire.com/agents/overview)
- [Repository hosting and mirrors](https://docs.entire.com/guides/repositories/overview)
- [CI integrations](https://docs.entire.com/guides/ci/overview)
- [Settings and generated files](https://docs.entire.com/guides/configuration/overview)
- [Account projects](https://docs.entire.com/guides/configuration/projects)
- [Privacy and redaction](https://docs.entire.com/guides/configuration/privacy-and-redaction)
- [Security and privacy](https://docs.entire.com/security)

The `.md` version of a page is available when the rendered page cannot be read.
Brain and Graph are separate Entire CLI plugins; do not claim they are installed
or install them just because this package includes a workflow for them.

## Official workflow coverage

The official skills index was checked against source commit
`fe5266f76d846222c73b080ce39fd803dd705198`. The package keeps existing skill names
and combines two closely related provenance workflows instead of adding aliases.

| Official workflow | This package |
| --- | --- |
| using-entire | using-entire |
| search | search-history |
| explain / what-happened | explain-code |
| recall | recall |
| replay | replay |
| teach | teach |
| review | review-work |
| session-handoff | session-handoff |
| address-findings | address-findings |
| session-crosslink | session-crosslink |
| session-to-skill | session-to-skill |

Diagnostics/token insights and optional Brain/Graph workflows are additional
entry points. Hosting, mirrors, settings, integrations and account operations
are guided through current documentation and CLI help from using-entire; no
plugin installation silently configures them.

## Compatibility decisions

- CLI help is authoritative for execution. Documentation and upstream skills
  can lag: for example, current Trail listing requires `--project`, uses
  `--limit`, and accepts lifecycle filters `open`/`closed`. Do not copy an older
  `--status any -n` listing recipe into a new release without checking help.
- `session current` has an explicit `resolution`; only `caller-env` and
  `ancestry` identify the caller. A cross-worktree fallback is not equivalent.
- Checkpoint metadata and transcript modes are distinct. A transcript defaults
  to the latest contributor unless an available session index is selected.
- Current `session attach` can rewrite unpushed history or push a transcript
  link for a pushed commit. Its documented non-interactive preview is mandatory
  before agreeing to the exact write. An old "amends HEAD" explanation is incomplete.
- `session resume` may reset to an older checkpoint or overwrite a session log;
  it is not merely an agent launcher or read operation.
- Core MCP status success is not repository proof: a JSON error may accompany
  exit zero. Validate scope and the result before interpreting `enabled`.

When updating, fetch only the sources affected by the change, compare installed
help, recheck relevant behavior, and record the tested CLI version. Do not
claim a version range supported from one successful local run.
