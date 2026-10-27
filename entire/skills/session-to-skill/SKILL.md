---
name: session-to-skill
description: Use when the user asks to turn an Entire session, a successful task, or a repeated recorded workflow into a reusable agent skill. Produces a source-backed draft rather than installing or publishing it automatically.
---

# Turn a proven workflow into a skill

Read [execution rules](../using-entire/references/execution.md).

1. Resolve the exact session/checkpoint through [session-handoff](../session-handoff/SKILL.md).
   Confirm identity and read the relevant contributors. For a repeated workflow,
   compare additional user-named or closely related precedents before generalizing.
2. Extract the reusable objective, prerequisites, decision points, successful
   steps, relevant failure paths, and meaningful verification. Separate proven
   steps from untested suggestions and task-specific accidents.
3. Remove secrets, customer details, creator-specific paths, account IDs,
   repository names and incidental branch assumptions. Parameters belong only
   where real users need them; do not replace one brittle recipe with dozens
   of speculative options.
4. Draft an English `SKILL.md` with a specific matching name/description,
   when-to-use boundary, concise workflow, side effects, evidence requirements,
   and references. Require installed help for version-sensitive CLI syntax.
   Keep exact commands only when their meaning and current support are verified.
5. Present the draft or save it to the user's specified source location. If an
   actual skill-authoring workflow is available, follow it for validation and
   placement. Do not edit installed caches, overwrite unrelated skills, install
   globally, or publish without the corresponding scope.

Validate the draft with a realistic sample input and expected observable result.
Report whether that was a manual walkthrough or an actual execution; a source
text check does not prove an agent will follow the skill successfully.
