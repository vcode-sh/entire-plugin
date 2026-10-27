---
name: using-entire
description: Use when Entire is explicitly mentioned, when the user asks what this plugin can do, or to route requests about recorded agent history, session handoffs, Trails, Brain, Graph, setup, or diagnostics. Match equivalent requests in the user's language. Do not trigger for unrelated research or simple code edits.
---

# Use Entire

Read [execution rules](references/execution.md) before using any workflow.
Entire is evolving: the installed CLI owns executable syntax; the documentation
explains concepts. Do not assume a feature is installed because it is documented.

## Start

1. Use the user's selected checkout, supplied explicitly to repository tools or
   as the CLI working directory. Never substitute the plugin directory, assume
   a default repository, or scan unrelated projects to choose one. If no checkout
   is selected, ask for it only when the requested action requires one.
2. Establish Git root, branch, origin identity, CLI version and relevant Entire
   capabilities. Distinguish a plain local Git repo, an enabled repo, and a
   hosted/indexed repo. A missing origin limits hosted discovery; it does not
   prove that local history is unavailable. Do not initialize or enable anything.
3. Discover the selected command's current help through the available help tool
   or `entire agent-help <command>`. Reuse help already read for this CLI version.
   Read nested help only for operations actually needed; avoid an all-command
   preflight before a small lookup.
4. Route to the matching skill. Return a useful result with its sources and
   limits; stop once the request is satisfied.

| User need | Skill |
| --- | --- |
| Find recorded work or indexed code | [search-history](../search-history/SKILL.md) |
| Reuse a similar task as a playbook | [recall](../recall/SKILL.md) |
| Follow how a feature evolved | [replay](../replay/SKILL.md) |
| Learn a repository topic from actual history and code | [teach](../teach/SKILL.md) |
| Why a line exists, checkpoint or session provenance | [explain-code](../explain-code/SKILL.md) |
| Prepare a handoff or continue a previous session | [session-handoff](../session-handoff/SKILL.md) |
| Inspect or manage a Trail and its findings | [trails](../trails/SKILL.md) |
| Fix and resolve existing Trail findings | [address-findings](../address-findings/SKILL.md) |
| Review changes with their recorded intent | [review-work](../review-work/SKILL.md) |
| Link a missed session to the correct repositories | [session-crosslink](../session-crosslink/SKILL.md) |
| Turn a proven session workflow into a reusable skill | [session-to-skill](../session-to-skill/SKILL.md) |
| Project memory or code relationship queries | [memory-and-graph](../memory-and-graph/SKILL.md) |
| Explain unavailable history, capture state, or token usage | [diagnostics](../diagnostics/SKILL.md) |

## Tools and CLI

Use the plugin's read tools with the explicit selected checkout. Consult their
actual schemas; do not invent names or parameters. Broader workflows and
authorized writes use the installed CLI in that same checkout. A read-only
tool cannot perform a write merely because a skill describes that workflow.
See the [tool map](references/tools.md) for the supported read boundaries.

Entire's native `entire mcp` server exposes only discovery and status and may
inherit the host's working directory. If using that server directly, validate
repository state through the CLI in the selected checkout. An embedded JSON
error is a failure even when the process returned zero or the MCP call succeeded.
MCP does not capture sessions; lifecycle hooks remain responsible for capture.

## Setup and troubleshooting

If Entire is missing, consult [installation](https://docs.entire.com/installation).
Prepare the installation method for the actual OS; do not execute a downloaded
installer, change PATH, install integrations, or upgrade without authorization.

If setup is incomplete, explain the exact missing component and prepare commands
from current help. Ask before setup, authentication, or destructive operations,
including `enable`, `disable`, `clean`, and `auth`. A request to create this
plugin does not authorize repository setup. Existing explicit authorization
for that exact operation is sufficient; do not ask twice.

For missing history, use [diagnostics](../diagnostics/SKILL.md). Treat setup,
capture, local history, hosted search, and optional extensions as separate
capabilities. Avoid a generic "reinstall/relogin" recommendation.

For repository hosting, mirrors, account access, agent hooks, CI or provider
configuration, use the relevant current documentation and exact CLI help.
Prepare the requested change and its side effects before acting. These are
supported guidance paths, not capabilities automatically configured by this plugin.

Use the [documentation map](references/documentation.md) to find current guidance.
