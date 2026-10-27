---
name: diagnostics
description: Use when Entire history, session capture, provenance, search, or optional capabilities are unavailable or inconsistent, or when the user asks about captured token usage. Diagnose the selected environment without automatically repairing settings, hooks, authentication, or storage.
---

# Diagnose Entire and report real capability

Read [execution rules](../using-entire/references/execution.md) and
[result handling](../using-entire/references/results.md).

1. Establish the selected checkout's actual Git root, branch and available
   origin identity. Worktrees, subdirectories and a missing origin are legitimate
   cases. A non-repository directory is a context error, not a disabled project.
2. Inspect installed version, command-specific help and checkout-scoped status.
   Treat process failure, tool failure and embedded JSON `error` distinctly.
   State whether capture is enabled; do not infer that history exists or was
   uploaded solely from that flag.
3. Reproduce only the failed read with bounded scope. Separate local checkpoint
   storage, current session resolution, hosted indexing/access, network/keyring
   restrictions and absent Brain/Graph executables. Report the exact sanitized
   diagnostic and which independent read still works.
4. Use relevant official docs and installed diagnostic help for the next step.
   `doctor` may repair/discard state or delete branches. Do not assume its
   default is read-only on every host. Use a verified report-only path; never
   run force repair, enable/disable, cleanup, auth, install or settings writes
   automatically. Prepare a concrete, narrowly scoped repair separately.
5. Return what is available now, the specific unavailable capability, evidence,
   and the smallest next action. Do not claim a root cause that the diagnostic
   did not establish or prescribe reinstalling everything.

For token usage, discover `session tokens` or `checkpoint tokens`. Validate the
session resolution or explicit checkpoint first. Use captured usage metadata,
qualify missing providers/models or aggregation gaps, and distinguish estimates
from measured counts. Do not invent monetary cost from token totals or run a
provider operation merely to populate usage. Optional extension installation,
account/CI configuration and privacy changes are separate authorized tasks.
