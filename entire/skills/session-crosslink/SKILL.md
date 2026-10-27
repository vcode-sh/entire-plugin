---
name: session-crosslink
description: Use when the user asks to attach a missed Entire session to a commit or to the repositories it actually changed, especially after starting an agent outside those checkouts. This can rewrite unpushed history or upload transcripts and requires a concrete preview.
---

# Link a missed session to the right code

Read [execution rules](../using-entire/references/execution.md).
Discover installed `session current` and `session attach` help before acting.
Ordinary commits already capture sessions; use this only for a missing link.

1. Resolve the intended session through explicit identity or the validated
   [handoff selection](../session-handoff/SKILL.md). A fallback from another
   worktree is not proof of ownership. Do not search all local transcript
   directories or assume the newest agent log is the right session.
2. Determine affected repositories from user scope and inspected session/files.
   Verify each selected Git root, exact target commit, relevant changed files,
   agent and existing checkpoint linkage. Do not assume HEAD is the right commit.
3. Preview the intended links: repository, commit, session, agent, evidence of
   relevance and expected side effects. A session can span repositories, but
   attach it only to commits its work actually explains.
4. In each target checkout, run the documented non-interactive preview without
   `--force`. Current CLI help says this changes nothing and exits non-zero
   without a terminal. Treat that expected preview exit separately from a failure.
   Show the actual described effects: an unpushed commit may be rewritten,
   while an already-pushed commit may cause a checkpoint transcript to be pushed.
5. Obtain the user's agreement to those exact effects, then run the approved
   command. Never pre-emptively use `--force`. Verify each resulting link through
   read-only metadata, and report failures separately; do not retry uncertain
   writes blindly or create extra commits to compensate.

Do not upload transcript content, rewrite history, or infer deletion/cleanup
authority from a request to inspect missing links. Repository-specific Git
rules may impose a stricter boundary and remain authoritative.
