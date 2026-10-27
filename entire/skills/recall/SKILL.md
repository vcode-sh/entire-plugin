---
name: recall
description: Use when the user asks whether similar work was done before, how the team solved a previous task, or wants a proven precedent turned into an actionable playbook. Match equivalent phrasing in the user's language. For a plain list of matches use search-history.
---

# Recall a useful precedent

Read [execution rules](../using-entire/references/execution.md).

1. Capture the task, constraints, and intended repository scope from the request.
   Reuse context already supplied. Do not impose a date window that would hide
   an older precedent without the user requesting one.
2. Use [search-history](../search-history/SKILL.md) for a small relevant page.
   If necessary, try one alternate phrasing or remove an unnecessarily narrow
   filter. Broaden repositories only when the task actually spans them.
3. Select the closest one to three distinct precedents by task similarity,
   using recency as a tie-breaker rather than proof of relevance. Resolve their
   type and inspect the relevant recorded context. A commit with no checkpoint
   may illustrate code, but it cannot establish the original reasoning.
4. Extract what worked, failed approaches, constraints, affected code and the
   verification actually performed. Omit categories unsupported by evidence.
5. Compare the precedent with the selected checkout: changed APIs, architecture,
   environments, permissions and product decisions can make old steps obsolete.

Return the nearest precedent with exact source IDs, a short reusable approach,
the important traps, and a concrete starting point for this task. Separate
historical facts from today's recommended adaptation. If no defensible
precedent exists, say what was searched and use current code to reason forward.
Do not fabricate a playbook or rerun historical commands automatically.
