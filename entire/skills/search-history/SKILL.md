---
name: search-history
description: Use when the user wants Entire to find previous agent work, decisions, similar tasks, feature history, or indexed code across specified repositories. Do not trigger for unrelated internet research or simple local text searches.
---

# Search recorded work

Read [execution rules](../using-entire/references/execution.md).
Discover `search` and any follow-up command through installed `agent-help`.

1. Start with the user's terms and the current repository unless they requested
   broader scope. Use a small compact JSON page when supported, for example:
   `entire search "retry backoff" --json --compact --limit 5`.
2. Inspect available result type, ID, repository, branch, date, snippet, and
   touched files. Fields are optional; do not infer absent content. Summarize
   useful results; do not dump JSON. Add supported author, branch,
   date, or repository filters when they help answer the question.
3. Read a promising checkpoint or commit with `checkpoint explain` only when
   snippets leave a real gap. For another repository, use its exact returned
   forge-prefixed slug and full checkpoint ID or commit SHA. Do not substitute
   a session, repo, or PR ID where a checkpoint ID is required.
4. A commit without a checkpoint trailer is still a code-history result, not a
   recorded conversation. Use its diff/message when relevant, label the missing
   linkage, and try the next promising result only if it could answer the gap.
   For session hits, resolve associated checkpoints using the supported session
   filter or session metadata before reading them. Prefer scoped prompts; full
   transcripts are a follow-up when the question needs them.
5. If there is no useful match, refine the terms or ask for materially missing
   scope. Expand to other repositories only when relevant to the request.
   State indexing or access limitations and fall back to source/Git evidence.

Use [result handling](../using-entire/references/results.md) for empty results,
read failures, unavailable transcripts, optional fields and incomplete coverage.
Do not retry the same failing read indefinitely or run setup to populate results.

For indexed code search, discover `search --code` and use exact identifiers or
error strings. Do not combine checkpoint-only filters with code mode unless
installed help permits it. For text in the local working tree, use `rg`.

For a playbook, follow [recall](../recall/SKILL.md). For feature history, follow
[replay](../replay/SKILL.md). Reuse already-read search results rather than
restarting discovery. Deduplicate checkpoint/commit/session projections of the
same work before presenting them as independent precedents.
Return source IDs or verified links and distinguish historical evidence from
the current implementation.
