"""Explicit read-only MCP tool contracts; no arbitrary command execution tool."""

from process import ToolError


def string(description="", choices=None):
    result = {"type": "string", "minLength": 1}
    if description:
        result["description"] = description
    if choices:
        result["enum"] = choices
    return result


def number(minimum=1, maximum=100):
    return {"type": "integer", "minimum": minimum, "maximum": maximum}


REPO = string("Absolute selected Git checkout directory on the MCP host, including linked worktrees. Never assume the MCP process cwd is the user's repo.")
LIMIT = number()
TOOLS = {
    "agent_help": ("Discover exact installed Entire CLI commands and flags. Optional repo_path provides repository context; never executes the requested command.", {
        "command": string("Space-separated command path, for example checkpoint explain; omit for overview."), "repo_path": REPO,
    }, []),
    "entire_status": ("Read Entire state in an explicit checkout. Logical CLI errors are errors, not disabled status. Includes the resolved checkout and CLI version.", {
        "repo_path": REPO,
    }, ["repo_path"]),
    "search": ("Search recorded agent work or indexed code. Repository-scoped by default; optional repo explicitly selects another scope. No full transcripts are requested.", {
        "repo_path": REPO, "query": string(), "mode": string(choices=["history", "code"]),
        "repo": string(), "limit": LIMIT, "page": number(1, 10000),
        "branch": string(), "author": string(), "date": string(choices=["week", "month"]),
    }, ["repo_path", "query"]),
    "checkpoint_read": ("Read checkpoint/commit metadata, scoped context or one selected transcript. Without target, lists bounded metadata. Never generates summaries or changes checkpoints.", {
        "repo_path": REPO, "target": string(), "view": string(choices=["metadata", "context", "transcript"]),
        "repo": string(), "session_id": string(), "session_index": number(0, 10000), "task": string(), "limit": LIMIT,
        "offset_bytes": number(0, 2147483647), "max_bytes": number(1024, 65536),
    }, ["repo_path"]),
    "session_read": ("Read current, listed or explicitly selected session metadata/transcript. Current-session fallbacks are labelled and must not be assumed to identify this chat.", {
        "repo_path": REPO, "view": string(choices=["current", "list", "info", "transcript"]),
        "session_id": string(), "limit": LIMIT,
        "offset_bytes": number(0, 2147483647), "max_bytes": number(1024, 65536),
    }, ["repo_path"]),
    "why": ("Read provenance for a file or line in the selected checkout. Missing attribution is reported as missing evidence, never invented intent.", {
        "repo_path": REPO, "file": string("File inside the selected checkout; relative paths are resolved against the checkout root."), "line": number(1, 10000000),
    }, ["repo_path", "file"]),
    "trail_read": ("Read project Trails, a Trail/change, findings or approvals. Listing requires an explicit project. No creation, comments, resolution, approval or merge.", {
        "repo_path": REPO, "view": string(choices=["list", "show", "findings", "approvals"]),
        "project": string(), "selector": string("CLI selector from installed help; do not pass a raw URL."),
        "repo": string(), "limit": LIMIT, "cursor": string(), "page_token": string(),
        "status": string(), "freshness": string(choices=["current", "stale", "any"]),
    }, ["repo_path"]),
}


def definitions():
    return [{"name": name, "description": desc, "inputSchema": {
        "type": "object", "properties": props, "required": required, "additionalProperties": False,
    }, "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": True}}
        for name, (desc, props, required) in TOOLS.items()]


def validate(name, args):
    if not isinstance(name, str) or name not in TOOLS:
        raise ToolError("unknown_tool", "Unknown tool; only the advertised read-only tools are available.")
    if not isinstance(args, dict):
        raise ToolError("invalid_argument", "Tool arguments must be an object.")
    _, props, required = TOOLS[name]
    if set(args) - set(props) or set(required) - set(args):
        raise ToolError("invalid_argument", "Missing required arguments or unrecognized arguments; consult tools/list.")
    for key, value in args.items():
        rule = props[key]
        if rule["type"] == "string":
            valid = isinstance(value, str) and bool(value.strip()) and "\x00" not in value and len(value) <= 8192
        else:
            valid = type(value) is int and rule["minimum"] <= value <= rule["maximum"]
        if not valid or "enum" in rule and value not in rule["enum"]:
            raise ToolError("invalid_argument", f"Invalid value for {key}.")
