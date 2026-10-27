---
name: review-work
description: Use when the user asks to review changes using Entire's recorded intent, recap agent activity, or inspect existing Trail review evidence. Do not automatically run paid or multi-agent reviews.
---

# Review work with intent

Read [execution rules](../using-entire/references/execution.md).

1. Establish the requested commit, branch range, checkpoint, or Trail. Inspect
   local status and the bounded diff without switching branches.
2. Find the linked sessions/checkpoints through current CLI help. Read the
   original request and relevant decisions, then compare them with the actual
   diff and current callers. Recorded intent is context, not proof of correctness.
   Use [transcript selection](../using-entire/references/transcripts.md) for
   multi-session checkpoints. When a commit lacks linkage, review its code and
   state that recorded intent was unavailable; do not abandon the whole review.
3. Report concrete defects and missing acceptance evidence in scope. Include
   file locations, triggers, impact, and the smallest useful verification.
   Keep unresolved product intent separate from implementation defects.
4. Summarize what was inspected and any history or runtime evidence unavailable.
   A historical passing test does not certify the reviewed revision.

Do not infer a base branch name. Use the user's range or verified repository/
Trail metadata. For a multi-repository Trail, follow each requested change and
identify any unavailable checkout. Link actionable findings to the reviewed
revision and explain the trigger and consequence; avoid speculative style issues.

For an activity recap, discover `recap` and use bounded, static output with the
requested time window. Compose the requested summary from that evidence.
Use `dispatch` only when the user specifically wants provider-generated
Dispatches and its data/usage scope is authorized. Drafts are not published.

`review` and `investigate` can launch multiple agents or consume provider usage.
Do not run them for an ordinary review unless explicitly requested or already
authorized. Check installed experimental help before invoking either; do not
install providers or change review configuration as a side effect.
