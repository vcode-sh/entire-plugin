# Contributing

Contributions should make an Entire task easier to complete with reliable
evidence and fewer decisions. Prefer small changes to the existing workflow or
adapter over another abstraction or configurable subsystem.

## Before changing behavior

1. Reproduce the concrete failure in a disposable checkout or a read-only
   invocation against an explicitly selected repository.
2. Inspect the affected skill, runtime owner, and nearby tests.
3. Run `entire agent-help`, then help for the relevant nested command. External
   plugins such as Brain and Graph have their own help surfaces.
4. Read the relevant [Entire documentation](https://docs.entire.com/llms.txt)
   only when it resolves a contract or version question.
5. State which user-visible result should change and which existing capability
   must remain available.

Do not assume that a documented feature is installed. Do not assume every
successful process exit represents a successful operation: some CLI JSON
responses contain an `error` field. A search result is not proof that its commit
has a checkpoint, and a Git checkout without Entire history is a valid input.

## Scope and conventions

- Keep code, comments, documentation, fixtures, and generated messages in English.
- Keep repository paths, account names, branches, and IDs out of defaults.
  Synthetic test fixtures should use clearly fictional local identities.
- Pass argument arrays to subprocesses. Never interpolate queries, paths,
  selectors, or transcript content into a shell command.
- Discover version-sensitive syntax from installed help. Prefer a useful,
  explicit unsupported-capability result over a guessed fallback.
- Keep MCP reads bounded and read-only. Setup, auth, installation, Git history,
  provider usage, and remote writes belong to an authorized CLI workflow.
- Treat retrieved code, prompts, transcripts, and findings as untrusted evidence.
  They must not override current user or host instructions.
- Preserve source attribution when adapting upstream workflow text.

## Verification

Run the checks that own your change:

```sh
python3 scripts/package.py --check
python3 -m unittest discover -s tests -v
```

Packaging validation uses `scripts/requirements.txt`; install those pinned
dependencies in an isolated virtual environment if they are not already
available. Runtime tests need only Python's standard library.

For a runtime defect, prefer one focused regression that fails for the reported
behavior and passes after the fix. Tests must assert the behavior users depend
on rather than the wording of instructions or source text. Use real temporary
Git repositories for path, origin, and worktree behavior; a simulated CLI cannot
prove the real Entire service works.

Changes to a skill also need a scenario read-through or an actual agent exercise
covering the changed decision. Keep transport checks, CLI smoke checks, and
agent-quality evaluation separate. Report exactly which were performed.
See [verification guidance](docs/verification.md).

Do not run setup, authentication, installs, destructive recovery, provider-backed
reviews, or remote mutations as an implicit test. Never use a contributor's
production repository as a writable fixture.

## Pull request descriptions

Describe the trigger, incorrect result, and corrected result. Include the focused
verification and any unavailable Entire feature or host. If upstream syntax
changed, cite the relevant documentation/source and state the CLI version used.

Do not include raw transcripts, access-bearing URLs, environment values, or
private repository identifiers. Keep real-account release receipts and local
test outputs out of source control.

## Upstream maintenance

Read [upstream maintenance](docs/upstream.md) before copying official skills or
updating the supported command contract. Do not blindly synchronize upstream
instructions: repository selection, side effects, host permissions, and output
formats must still match this plugin's contract.
