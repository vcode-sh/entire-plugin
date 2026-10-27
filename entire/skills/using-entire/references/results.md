# Interpret results without inventing history

Check the command result before interpreting its data. A command may exit zero
with an embedded `error`, and a successful MCP transport may contain a failed
tool result. Preserve the diagnostic while withholding credentials and raw data.

| Observed result | Meaning and useful next step |
| --- | --- |
| Not a Git repository | Resolve the selected checkout; do not recommend enabling Entire in the plugin or home directory. |
| Git repo without origin | Local inspection may still work. Hosted scope needs a verified repository identity; do not invent one. |
| Entire disabled | Capture is disabled in this checkout. Existing local or hosted history may still exist. Explain before proposing setup. |
| `setup_required` / `not set up` | This is a Git checkout without local Entire setup. Keep it separate from a configured but disabled repository; do not initialize it automatically. |
| Missing CLI or unsupported command/flag | State the available version and capability. Use a supported smaller path, or explain the prerequisite; do not upgrade automatically. |
| Missing login or access denied | Distinguish authentication, authorization and execution-host network/keyring restrictions. Do not switch accounts or run login automatically. |
| Empty successful search/list | Report the query and scope. Refine once when useful; do not say work never happened. |
| Commit has no checkpoint trailer | The commit exists without the requested checkpoint linkage. Read its Git diff/message for code facts; do not claim to know recorded intent. |
| Checkpoint or transcript not available | Report which source is missing; use available metadata or another relevant hit. A partial answer is better than invented session content. |
| Local storage reports `object not found` or similar | This is a read failure, not an empty history. Report the exact sanitized diagnostic, try an already-authorized independent hosted read if useful, and leave repair to a separately scoped task. |
| `why` returns only file/line | No provenance evidence was supplied. Use relevant Git history or search; label any intent inferred from code. |
| Optional snippet/files/author absent | Use the fields actually returned. A title, score or date alone does not establish a technical decision. |
| Pagination token or partial-region warning | State incomplete coverage. Follow a bounded next page only when the question needs it. |

Metadata JSON does not automatically contain transcript bytes. Use the relevant
read mode and [transcript handling](transcripts.md) only when more context is
needed. Never use `--generate` or a repair command to make a read look successful.
