"""Validate source independently; optionally build and inspect one plugin archive."""

import argparse
import json
import re
import zipfile
from pathlib import Path

import jsonschema
import yaml
from PIL import Image


project = Path(__file__).resolve().parents[1]
root = project / "entire"
manifest = json.loads((root / "plugin.json").read_text())
mcp = json.loads((root / "mcp.json").read_text())
for filename, value in (("plugin.schema.json", manifest), ("mcp.schema.json", mcp)):
    jsonschema.Draft202012Validator(
        json.loads((project / "scripts" / filename).read_text())
    ).validate(value)

assert manifest["name"] == root.name
assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
interface = manifest["extensions"]["com.openai"]["interface"]
assert 0 < len(interface["shortDescription"]) <= 30
assert interface["category"] == "Developer Tools"
assert isinstance(interface["capabilities"], list)
assert all(isinstance(value, str) and value for value in interface["capabilities"])
assert manifest["extensions"]["com.openai"]["requires_local_executor"] is True
assert len(interface["defaultPrompt"]) <= 3
assert all(0 < len(value) <= 128 for value in interface["defaultPrompt"])

for field in ("logo", "composerIcon", "logoDark", "composerIconDark"):
    path = (root / interface[field]).resolve()
    assert path.is_relative_to(root)
    assert path.stat().st_size <= 5 * 1024 * 1024
    with Image.open(path) as icon:
        assert icon.format == "PNG"
        assert 48 <= icon.width == icon.height <= 4096
        icon.verify()

skills = sorted(root.glob("skills/*/SKILL.md"))
assert skills, "At least one workflow skill is required."
names = set()
for path in skills:
    text = path.read_text()
    assert path.stat().st_size < 1024 * 1024
    assert text.startswith("---\n")
    frontmatter = yaml.safe_load(text.split("---", 2)[1])
    assert frontmatter["name"] == path.parent.name
    assert isinstance(frontmatter["description"], str) and frontmatter["description"].strip()
    assert frontmatter["name"] not in names
    names.add(frontmatter["name"])

files = sorted(path for path in root.rglob("*") if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc")
assert all(not path.is_symlink() for path in root.rglob("*"))
for path in files:
    assert not any(part in {"node_modules", ".git", "__pycache__"} for part in path.parts)
    assert not path.name.startswith(".env")
    if path.suffix == ".py":
        compile(path.read_text(), str(path), "exec")
    if path.suffix not in {".md", ".py", ".json"}:
        continue
    text = path.read_text()
    assert all(line == line.rstrip() for line in text.splitlines()), path
    assert text.endswith("\n"), path
    if path.suffix != ".md":
        continue
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if re.match(r"^[a-z]+:", link):
            continue
        target = (path.parent / link.split("#")[0]).resolve()
        assert target.is_relative_to(root) and target.is_file(), (path, link)

server = mcp["mcpServers"]["entire"]
assert server["command"] == "python3"
assert server["args"] == ["${PLUGIN_ROOT}/server/main.py"]
assert (root / "server/main.py").is_file()
catalog = json.loads((project / ".agents/plugins/marketplace.json").read_text())
entry = next(value for value in catalog["plugins"] if value["name"] == manifest["name"])
assert entry["source"]["path"].startswith("./")
assert (project / entry["source"]["path"]).resolve() == root
assert entry["category"] == interface["category"]
assert entry["policy"] == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}

parser = argparse.ArgumentParser(description=__doc__)
mode = parser.add_mutually_exclusive_group(required=True)
mode.add_argument("--check", action="store_true", help="Validate source without building or overwriting an archive.")
mode.add_argument("--build", action="store_true", help="Validate, build a new versioned archive, and inspect it.")
args = parser.parse_args()
output = None
source_output = None
if args.build:
    output = project / "dist" / f"entire-{manifest['version']}.zip"
    source_output = project / "dist" / f"entire-plugin-source-{manifest['version']}.zip"
    output.parent.mkdir(exist_ok=True)
    assert not output.exists(), f"Refusing to overwrite {output}; choose a new version or output."
    assert not source_output.exists(), f"Refusing to overwrite {source_output}; choose a new version or output."
    with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(root.parent))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        actual = set(archive.namelist())
        expected = {str(path.relative_to(root.parent)) for path in files}
        assert actual == expected
        assert {name.split("/")[0] for name in actual} == {manifest["name"]}
        assert json.loads(archive.read("entire/plugin.json")) == manifest
        assert json.loads(archive.read("entire/mcp.json")) == mcp
    source_files = list(files)
    for directory in ("scripts", "tests", "docs"):
        source_files.extend(path for path in (project / directory).rglob("*")
                            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc")
    source_files.append(project / ".agents/plugins/marketplace.json")
    source_files.extend(project / filename for filename in
                        ("README.md", "CONTRIBUTING.md", "SECURITY.md", "LICENSE", "CHANGELOG.md", ".gitignore"))
    assert all(path.is_relative_to(project) and not path.is_symlink() for path in source_files)
    with zipfile.ZipFile(source_output, "x", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_files):
            archive.write(path, Path("entire-plugin") / path.relative_to(project))
    with zipfile.ZipFile(source_output) as archive:
        assert archive.testzip() is None
        assert "entire-plugin/release.json" not in archive.namelist()
        assert not any("/dist/" in name or "/.env" in name for name in archive.namelist())

print(json.dumps({
    "archive": str(output) if output else None,
    "source_archive": str(source_output) if source_output else None,
    "version": manifest["version"],
    "skills": sorted(names),
    "mcp_servers": list(mcp["mcpServers"]),
    "subtitle_characters": len(interface["shortDescription"]),
    "files": len(files),
    "bytes": output.stat().st_size if output else None,
}, indent=2))
