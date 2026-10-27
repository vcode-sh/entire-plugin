# Version 0.2.0 verification

Checked on 2026-10-27 using Entire CLI 0.12.2 on Linux. These results describe
the source and adapter, not universal host compatibility or provider writes.

## Executed evidence

- Nineteen focused runtime tests passed, including installed Entire status in
  a fresh temporary Git checkout. No Entire setup was enabled for the test.
- Real temporary Git repositories established checkout separation, subdirectory
  resolution and protection against inherited Git location overrides.
- Regression cases covered embedded JSON errors, literal shell metacharacters,
  absent optional search fields, current-session fallback identity, unsupported
  CLI flags, targeted metadata with fifteen sessions, long transcript excerpts,
  UTF-8 page boundaries and MCP request handling.
- The server initialized and discovered all seven tools while launched outside
  the selected checkout. Real CLI help, status, search, current-session metadata,
  file provenance and an empty Trail list returned through the adapter.
- A plain second Git checkout returned `setup_required`; a non-Git directory
  returned `not_git_repository`, both as failed tool results rather than false
  claims about configured capture.
- Local checkpoint listing in the selected configured checkout reported
  `history_unavailable` from `object not found`. This failure was preserved.
  No successful live linked-checkpoint transcript read was established.
- Eight agent reasoning exercises used supplied synthetic results. They covered
  wrong-worktree handoff, missing checkpoint linkage, multiple contributing
  sessions, a Trail spanning repositories, precedent applicability, embedded
  errors, absent Brain, and stale findings on a different branch.
- A separate adapter review found Git environment leakage, detail truncation
  and missing transcript paging. Fixes and the subsequent UTF-8 boundary fix
  passed focused regression and delta review.

## Limits

The synthetic agent exercises prove decisions under supplied evidence, not live
provider state. Fake CLI responses in unit tests prove adapter behavior only.
Brain/Graph, authenticated setup, capture hooks, signed releases, remote finding
updates, merges, transcript upload and public publication were not exercised.
No macOS, Windows or browser-only host support was established by these checks.
No test enabled capture, created a manual checkpoint, committed, pushed, changed
authentication or repaired an existing repository.

Package validation and installed-host readback are required after the final
archive is built; report those separately from source and direct-process checks.

## Version 0.2.1 distribution follow-up

The source includes a local Codex marketplace catalog. On the installed CLI,
`codex plugin marketplace add . --json` registered it and
`codex plugin list --marketplace entire-community --available --json` discovered
`entire@entire-community` at version 0.2.1. The temporary test registration was
removed afterward. This establishes catalog registration and discovery, not a
fresh desktop installation or a new chat's connection.

The private account release was saved and its portable and generated compatibility
MCP configurations were read back consistently. The already-running creating chat
still used its older loaded MCP process; a fresh host connection remains a separate
check. No existing process or other plugin was stopped to force an update.
