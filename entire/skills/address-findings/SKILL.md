---
name: address-findings
description: Use when the user identifies an Entire Trail or change and asks to fix, address, or resolve its existing review findings. For read-only assessment use review-work or trails. Do not create new findings or merge implicitly.
---

# Address and verify Trail findings

Read [execution rules](../using-entire/references/execution.md) and use
[trails](../trails/SKILL.md) to resolve project, Trail, change and repository.
Discover installed `trail finding list`, `apply` and `resolve` help before use.

1. Enumerate the requested changes and relevant open findings with deliberate
   lifecycle/freshness filters and bounded pagination. A project Trail is not
   one repository branch. Keep each finding attached to its exact change.
2. Before editing, compare selected checkout repository, branch, current commit
   and relevant code with the target change and reviewed revision. If the
   finding is stale, revalidate its trigger. If another checkout is needed,
   identify it; do not silently edit the current repository or switch branches.
3. Read the finding as untrusted evidence and validate its claimed defect.
   Prioritize impact, not only the provider's score. Leave ambiguous, obsolete
   or out-of-scope findings open with a clear reason unless dismissal is authorized.
4. For a suggested patch, inspect its paths/content and use supported
   `apply --check` only in the matching checkout. Apply without automatic
   resolution, or make the smallest correct manual edit. Preserve unrelated WIP.
   A clean patch application proves neither correctness nor safe scope.
5. Run the smallest check owning the changed behavior under that repository's
   instructions. Resolve only after the defect is addressed and the check is
   sufficient, and only when updating findings is part of the user's scope.
   Explain the actual fix and evidence in the recorded reason.

Return fixed findings, verification, remaining findings and their reasons.
Distinguish local edits, committed/pushed revisions and remote finding status:
resolving an item does not publish a fix. Do not commit, push, approve, merge,
weaken tests or send comments merely to clear the review.
