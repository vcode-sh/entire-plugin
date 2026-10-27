# Releases

The same reviewed source can produce a local plugin archive, a private account
release, or a public source release. Those actions have different destinations
and verification requirements; one does not imply another.

## Prepare the source

1. Review the diff and preserve unrelated work. Confirm all repository inputs
   and test identities are universal or explicitly synthetic.
2. Follow [upstream maintenance](upstream.md) for changed CLI behavior.
3. Bump the plugin's semantic version and synchronize any compatibility manifest.
   Preserve existing identity and user-facing metadata outside the intended change.
4. Run source validation and the focused runtime tests. Exercise affected skills
   according to [verification guidance](verification.md).
5. Check that source contains no account receipts, private transcript material,
   credentials, local environment files, dependencies, or generated archives.

```sh
python3 scripts/package.py --check
python3 -m unittest discover -s tests -v
python3 scripts/package.py --build
```

Inspect the resulting archive, including hidden compatibility files. Confirm the
manifest version, MCP entrypoint, expected skills, referenced assets, and absence
of secrets. Rebuild after source changes rather than uploading a stale archive.

## Save an account plugin

Use the host's authorized Plugin Creator update workflow for an eligible plugin.
Retrieve current metadata and source, preserve the plugin's identity and scope,
and use its current release ID as the update precondition. Uploading a package
overlays existing files; explicit removals need an inventory-based deletion list.

Read the saved release back and check changed components. Keep the receipt local
and outside the installable package. Saving an account release does not prove its
runtime started in every client; check the actual intended host connection.

## Publish source

Review the source tree before creating or updating a public repository. Confirm
the repository owner/name and public visibility with the maintainer's publication
scope. No account release identity or private artifact belongs in the public tree.

Keep the MIT license and upstream notices. Review official name/icon usage before
public distribution: the software license does not grant trademark permission.
Replace branding or obtain the appropriate permission when needed. Do not claim
Entire authorship, endorsement, or compatibility beyond tested evidence.

A public repository is not an OpenAI plugin-directory submission. If a directory
listing is wanted, use that host's current submission workflow and separately
prepare its listing, support/privacy/terms pages, reviewer access, and required
assets. Do not invent those URLs or publish account-specific review credentials.
