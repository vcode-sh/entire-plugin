---
name: explain-code
description: Use when the user asks Entire why code exists, what changed at a file or line, or what intent and sessions are associated with a commit or checkpoint.
---

# Explain code with recorded intent

Read [execution rules](../using-entire/references/execution.md).
Discover `why`, `checkpoint explain`, and relevant session commands first.

1. Resolve the actual file and line in the selected checkout. Read the current
   code around it so a historical explanation is tied to the present source.
2. Use `entire why path/to/file.ts:42 --json` if installed help supports it.
   If the user supplies a commit/checkpoint, inspect that exact target instead.
3. Check whether the result actually contains commit/checkpoint evidence.
   `why` returning only the requested file/line supplies no provenance. A commit
   without a checkpoint trailer supplies no recorded session intent. Handle
   those cases explicitly with [result handling](../using-entire/references/results.md).
4. Read available checkpoint metadata and scoped prompts. Metadata-only JSON
   does not contain transcripts. Use the documented transcript output and
   [session selection](../using-entire/references/transcripts.md) only when the
   reasoning cannot be established from scoped context.
5. If provenance is missing, inspect the relevant Git history or use a focused
   [history search](../search-history/SKILL.md). Avoid reconstructing the whole
   repository's history for a line-level question.
6. Explain the original problem, the recorded decision, and how the current
   code relates to it. Cite actual file locations and checkpoint/commit IDs.
   Clearly label inference where no recorded intent is available.

Do not generate or overwrite a stored AI summary to answer an ordinary code
explanation. Do not treat a transcript's claims about tests or deployment as
verification of the current checkout or production environment.

For a pasted snippet, locate the actual current file and range first. If several
locations match and would lead to different histories, ask which one; do not
attach provenance from an arbitrary textual match. Explain a range through its
relevant commits without asserting one line lookup covers every line.
