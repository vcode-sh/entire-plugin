# Read tools and their CLI boundaries

Consult the actual installed tool schemas. Every repository-specific read needs
an explicit absolute selected `repo_path`; the server's inherited directory is
not a repository selector. Never hardcode a creator's machine path.

| Tool | Purpose and important scope |
| --- | --- |
| `agent_help` | Discover a space-separated command path. Supply `repo_path` when repository context matters. |
| `entire_status` | Establish Git/Entire state for the selected `repo_path`. Inspect errors and capability warnings. |
| `search` | Bounded history or code search; `mode` distinguishes them. History-only author/date/branch filters must not be carried into code mode. |
| `checkpoint_read` | Read metadata, scoped context, or transcript for an explicit target. Select `session_index` for relevant contributors and `task` only from returned metadata. |
| `session_read` | Read current/list metadata or an explicit session's info/transcript. Current resolution is evidence about identity, not an instruction to choose a fallback. |
| `why` | Inspect the selected checkout's file and optional line. A successful response without provenance is not a recorded explanation. |
| `trail_read` | List/show Trails, findings or approvals. List requires an explicit verified project; change selectors and project Trail selectors are different. |

These tools are read-only and are not a generic shell or full CLI proxy.
For unsupported reads and authorized writes, discover the installed CLI and run
it in the same selected checkout. Brain/Graph are optional external commands.
Setup, generation, attach/resume, publication, approval and merge are not made
safe or authorized by having a similarly named read tool.
