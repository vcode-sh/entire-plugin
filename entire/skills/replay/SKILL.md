---
name: replay
description: Use when the user asks how a feature evolved, wants a chronological walkthrough of recorded agent work, or asks to replay implementation history. Replay explains history without checking out old revisions or executing recorded commands.
---

# Replay feature history

Read [execution rules](../using-entire/references/execution.md).

1. Establish the feature, files, branch or period requested. Find relevant
   checkpoints and commits through [search-history](../search-history/SKILL.md)
   and bounded Git history in the selected checkout.
2. Deduplicate projections of the same work. Order using actual commit/session
   timestamps and relationships, not search relevance or an ID's appearance.
   Distinguish agent-turn time, checkpoint time and commit time when they differ.
3. Read the relevant [contributing sessions](../using-entire/references/transcripts.md).
   Track the initial objective, key decisions, failures, subsequent corrections,
   and resulting code. Do not infer a causal connection solely from proximity.
4. Present a compact timeline: what changed, why the record says it changed,
   exact source and outcome. Mark missing transcript/checkpoint intervals.
5. Compare the endpoint with current code when the user asks how it works now.
   Historical completion does not prove deployment or current correctness.

Replay is read-only: do not switch branches, restore files, recreate checkpoints,
or execute transcript commands. If pagination or unavailable sources make the
timeline partial, state its bounds rather than claiming a complete history.
