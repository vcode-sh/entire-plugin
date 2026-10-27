---
name: trails
description: Use when the user asks to inspect, create, update, or work through an Entire Trail, its changes, review findings, approvals, or merge requirements.
---

# Work with Entire Trails

Read [execution rules](../using-entire/references/execution.md).
Discover `trail` and the exact nested command before acting.

## Read and assess

- Resolve the project from current CLI/origin context or the supplied Trail
  URL. Listing requires an explicit `--project gh/<owner>` or
  `--project et/<project>` even inside a repository. `--repo` only filters it.
- A project Trail number and a change number are different identifiers.
  Follow installed help's URL-to-selector mapping; never pass a raw URL as a
  positional selector. Use the URL printed by `trail show` when linking back.
- A whole project Trail may contain several changes across repositories.
  Enumerate its returned changes, preserve their repository/branch/revision
  identity, and use each change's returned URL. Cover all requested changes;
  report those needing another checkout instead of silently omitting them.
- Inspect the intended outcome, linked changes, findings, approval state, and
  required checks. Use bounded listing/show/approvals output and a bounded
  watch only if status tracking was requested.
- Compare actionable findings with current source and the revision reviewed.
  Stale does not mean resolved. Distinguish observed defects, disputed
  findings, missing evidence, and merge blockers.
- Finding-list defaults may hide stale or dismissed items. Inspect installed
  freshness/lifecycle filters and paginate deliberately when the request is to
  audit all findings. Do not conflate status, freshness, severity, or a missing
  page. A successful empty list proves only that selected scope/filter.
- Entire approvals and GitHub approvals are separate. Green Entire gates
  alone do not prove GitHub merge requirements are satisfied.

## Authorized changes

For a planning-only Trail, prepare title, problem, outcome, and acceptance
criteria. Check current `trail create` help for `--no-branch` to avoid publishing
or linking a branch when the request only authorizes capturing intent.
Default creation can publish a branch: do not assume publishing is implied.

For requests to fix findings, follow [address-findings](../address-findings/SKILL.md).
Before any edit, verify the selected checkout's repository, branch and relevant
revision against the target change. Do not switch branches or apply a patch
to a different checkout merely to make the command succeed. Comments and other
messages require explicit messaging authorization.

Linking branches, changing gates or agents, approving, merging, and closing
work require their own task scope. Never approve or merge solely because all
review signals are green. Follow the checkout's Git and production rules.
