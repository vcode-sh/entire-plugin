---
name: teach
description: Use when the user wants to learn how a topic works in a repository through its actual code, recorded decisions, and implementation examples. Do not use for generic tutorials unrelated to the selected project.
---

# Teach from code and recorded decisions

Read [execution rules](../using-entire/references/execution.md).

1. Use the user's question and apparent familiarity to choose a useful depth.
   Clarify only if different interpretations would materially change the lesson.
2. Find the real behavior owner in current code and a small set of relevant
   historical sources using [search-history](../search-history/SKILL.md) or
   [explain-code](../explain-code/SKILL.md). Optional Graph can narrow code
   locations if already available; it is not a prerequisite.
3. Build the explanation around one real flow: entry point, important decisions,
   data/side effects, failure behavior, and where the result appears. Ground
   examples in actual symbols and paths, with recorded intent cited separately.
4. Explain why a decision was made only when a source supports it. When history
   is unavailable, teach observed behavior and label inferred rationale.
5. Finish with a concrete way to explore or verify the concept and the limits
   of available evidence. An optional exercise must be safe, scoped, and clearly
   separate from work the user actually asked the agent to perform.

Do not write a generic textbook chapter, invent architecture, execute historical
deployment commands, or edit code just to make the lesson illustrative.
