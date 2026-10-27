# Verification

Verification should establish the claim being made, not accumulate overlapping
green checks. Use synthetic local repositories and sanitized fixtures by default.

## Package validation

```sh
python3 scripts/package.py --check
```

Validate manifests, skill frontmatter and references, contained assets, runtime
entrypoints, and archive composition. This check must not require an existing
account, install software, or build an archive merely to inspect source.

## Runtime regression tests

```sh
python3 -m unittest discover -s tests -v
```

Tests should own concrete boundary behavior, such as:

- Two different checkouts retain separate repository context.
- A non-Git path cannot masquerade as a disabled Entire repository.
- A JSON `error` is recognized even when the CLI exits successfully.
- Quotes and shell metacharacters in a query remain literal arguments.
- Missing checkpoint links and optional result fields remain valid outcomes.
- Session resolution does not silently select another worktree's session.
- Commands and transcript reads remain bounded.

Assert results, argument handling, or effects rather than source text. A fake
CLI can establish this adapter's behavior, but cannot establish real Entire
authentication, storage correctness, network access, or service availability.

## Real CLI smoke checks

When an existing Entire-enabled checkout is available and the user has permitted
read access, check the selected checkout explicitly. Discover help first. A
useful smoke exercise compares status, runs a small history query, and reads an
actual linked checkpoint when one exists. An empty Trail list proves only that
the read succeeded; it does not verify finding resolution or merging.

Do not enable capture or create a checkpoint to manufacture a passing result.
If the checkout lacks linked history or reports an error, record that limit and
use an approved synthetic fixture or another explicitly selected test repository.

## MCP host checks

From the intended host, establish initialization, tool discovery, a harmless
help call, and a repository-specific call with an explicit checkout path.
Repeat with a second synthetic checkout to catch process working-directory
leakage. Distinguish direct server-process checks from tools invoked through an
installed host connection.

## Skill scenarios

Run an agent exercise or a focused scenario review for changed decisions:

| Scenario | Required result |
| --- | --- |
| A similar task has recorded history | An evidence-backed playbook with current applicability checked |
| A matching commit has no checkpoint | A useful code/Git answer with recorded intent explicitly unavailable |
| Current session resolves to another worktree | No silent handoff of an unrelated session |
| A checkpoint has several contributing sessions | Relevant earlier rationale and current state are both considered |
| A transcript is missing | A bounded fallback that does not invent context |
| A Trail spans repositories | All requested changes are accounted for, including unavailable clones |
| Brain or Graph is absent | Accurate prerequisite status and a core-workflow fallback where possible |

A scenario checklist is not an executed agent evaluation. When reporting a
release, say whether each item was automated, manually executed, reviewed only,
or unavailable. Do not call OS support, remote writes, or production behavior
verified from local unit tests.
