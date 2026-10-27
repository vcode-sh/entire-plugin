---
name: session-handoff
description: Use when the user asks to hand off Entire session context, inspect an active or saved session, or continue previous agent work. Preparing a handoff does not authorize switching branches or messaging another chat.
---

# Prepare or resume a session handoff

Read [execution rules](../using-entire/references/execution.md).
Discover `session current`, `list`, `info`, and any relevant checkpoint command.

1. Resolve `session current --json` in the selected checkout when the user means
   this work. Check `resolution`: only `caller-env` or `ancestry` identifies the
   calling session. Validate its worktree and agent. Other resolutions are
   candidates, not proof that this is the user's intended session. Inspect
   bounded session-list metadata or ask a targeted question if still ambiguous;
   never silently choose an unrelated session from another worktree.
2. For a named session, read that exact ID. For a supplied checkpoint, enumerate
   its contributors and select relevant sessions explicitly using the
   [transcript rules](../using-entire/references/transcripts.md). Do not assume
   the latest contributor contains the original request. Prefer this
   conversation's known state when it is newer than stored history.
3. Inspect Git status and relevant diffs read-only. Separate committed work,
   uncommitted changes, and unrelated changes belonging to others.
4. Identify the selected session, agent, worktree and resolution briefly so a
   mistaken selection is visible. Draft a concise handoff containing the objective, decisions and constraints,
   exact repository/branch/session IDs, relevant changed files, completed work,
   verification and its limits, blockers, and concrete next steps. Include only
   facts established from the current session or inspected evidence.
5. Return the handoff in chat unless the user specified a file or destination.
   Do not create a checkpoint, commit, publish a transcript, or send messages
   merely to produce a handoff.

For actual continuation, use the handoff to continue the authorized task when
the current checkout already fits. Do not switch branches just to summarize or
resume reasoning. If `session resume` is necessary, discover its current help
and inspect the working tree first. It may switch branches, reset to an older
checkpoint, overwrite a session log, fetch, or launch an agent. Execute only
within the user's explicit scope and repository rules; preserve WIP. Do not
pass `--force` to bypass a consequential decision.
Attaching, adopting, or stopping sessions also changes state and needs task
authorization. Preparing context alone leaves those operations unnecessary.

When metadata or a transcript is unavailable, name the missing evidence and
hand off the known conversation/diff state. Never imply a successful transcript
handoff solely because `session current` returned an ID.
