# Entire community plugin

Use [Entire](https://docs.entire.com/) to recover the context behind code,
find earlier work, prepare session handoffs, and work through review findings.
This is an independent community integration maintained by Vibe Code, not an
official Entire release.

The plugin works with the repository you select. It does not contain a default
repository, account, organization, branch, or machine path. GitHub-backed and
Entire-native repository identities come from the selected checkout or an
explicit user-selected target. Available history and hosted actions depend on
that repository's Entire setup and the user's existing access.

## What it does

- Search recorded work and turn useful precedents into an actionable playbook.
- Explain code changes using recorded intent and current source evidence.
- Replay a feature's history or teach a topic from its canonical checkpoints.
- Prepare a handoff from the correct live session or contributing checkpoint sessions.
- Review changes against their original intent and address authorized Trail findings.
- Guide session linking and reusable-skill creation without silently rewriting history.
- Use separately installed Brain and Graph commands when they are available.

Repository-specific MCP reads take an explicit checkout path. The adapter runs
the installed CLI in that checkout instead of assuming the host launched the
server there. Skills handle broader CLI workflows and discover current help
before using commands. The adapter's read operations do not authorize setup,
authentication, commits, pushes, branch changes, or remote writes.

| MCP tool | Purpose |
| --- | --- |
| `agent_help` | Discover the installed CLI's command contract |
| `entire_status` | Inspect capture and repository state in the selected checkout |
| `search` | Find recorded work or indexed code with bounded results |
| `checkpoint_read` | Read a selected checkpoint or commit's linked context |
| `session_read` | Read current, listed, or selected session context |
| `why` | Inspect recorded provenance for a selected file or line |
| `trail_read` | Inspect Trail intent, changes, findings, and approvals |

Pass an absolute `repo_path` for repository reads. Tool schemas describe each
operation's selectors and limits; use `agent_help` for the installed command's
current behavior. No MCP tool accepts an arbitrary shell command or exposes a
write operation.

## Requirements

- A local execution host with Python 3.10 or newer available as `python3` and the Entire CLI.
- The `entire` executable available on that host's `PATH`.
- A local Git checkout for repository-specific operations.
- Existing Entire authentication and repository access for hosted features.

See the [official installation guide](https://docs.entire.com/installation) for
the CLI. Installing this plugin does not install Entire, authenticate an
account, enable repository hooks, or install Brain or Graph.

Session capture remains Entire's responsibility. Its agent and Git hooks must
be configured separately when capture is wanted. Search hits can exist without
a linked checkpoint; missing history must remain visible in the answer.

This is a local integration. A browser-only host without local process access
cannot run it. The implementation and test results do not establish universal
OS or host compatibility; see [verification](docs/verification.md).

## Try it

Select the checkout in your coding host and ask, for example:

> Have we solved a task like this before? Find the closest recorded example,
> explain what worked, and check which parts still apply to the current code.

> Explain why this function changed. Separate recorded intent from your inference.

> Prepare a handoff for this session: decisions, changed files, checks that ran,
> remaining uncertainty, and next steps. Do not switch branches or send it elsewhere.

> Review this diff against the original task. Identify concrete defects and
> acceptance criteria that still lack evidence.

> Inspect this Entire Trail and summarize the findings that still need action.

Natural-language requests can be written in your preferred language; source
artifacts and contributor documentation are English. A selected repository is
context for the task, not authorization to modify its configuration.

## Source and packages

Install from the public source catalog:

```sh
codex plugin marketplace add vcode-sh/entire-plugin
codex plugin add entire@entire-community
```

After cloning or extracting this source repository, register its local catalog:

```sh
codex plugin marketplace add .
codex plugin add entire@entire-community
```

Run these commands from the source repository root. They install this community
plugin through Codex; they do not enable Entire capture in any target checkout.
Start a new chat after installation or updating a previously loaded plugin.
For desktop versions using the plugin browser, select the **Entire Community**
source and install **Entire** there. Availability varies by client version;
consult [OpenAI's package and marketplace documentation](https://developers.openai.com/plugins/build/plugins)
and your installed `codex plugin --help` for the supported flow.

The source repository and the installable plugin are different artifacts:

```text
entire/        Installable plugin manifest, skills, runtime, and assets
scripts/       Validation and packaging tools
tests/         Runtime and contract regression tests
docs/          Contributor, architecture, and verification guidance
dist/          Locally generated plugin archives; not source
```

Build a local archive from a reviewed source tree:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/package.py --check
python3 -m unittest discover -s tests -v
.venv/bin/python scripts/package.py --build
```

If those build dependencies are already installed in your selected Python
environment, the equivalent validation/build commands are:

```sh
python3 scripts/package.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package.py --build
```

The runtime and runtime tests use Python's standard library. Packaging separately
uses pinned `jsonschema`, PyYAML, and Pillow dependencies in
`scripts/requirements.txt`; they are not MCP runtime dependencies.
See [contributing](CONTRIBUTING.md) and the [release process](docs/releases.md)
before saving an account release or publishing an archive.

A private plugin saved to its creator's account is not a public directory
listing, a public source repository, or proof of another host's connectivity.
This repository does not embed an account plugin ID or credentials in the
installable package.

## Trust and attribution

The plugin delegates to a local executable with your user privileges. Entire
may use network services, local credential stores, telemetry, and local caches
according to its own configuration. Review [Entire's privacy documentation](https://docs.entire.com/security)
and this project's [security guidance](SECURITY.md).

Software is MIT-licensed; see [LICENSE](LICENSE) and the upstream notice in
[THIRD_PARTY_NOTICES.md](entire/THIRD_PARTY_NOTICES.md). Entire's name and official
icons belong to their respective owner. The official icons identify the
integration; their inclusion does not imply endorsement or a trademark license.

Documentation and upstream provenance are recorded in
[SOURCES.md](entire/SOURCES.md). Use installed CLI help for executable syntax;
public documentation can describe features that are newer than the installed CLI.
