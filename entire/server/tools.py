"""Translate typed read requests into checked CLI argv in an explicit checkout."""

from pathlib import Path

from process import CLI, ToolError
from schema import validate


def allowed(args, keys):
    unexpected = set(args) - set(keys) - {"repo_path", "view", "limit"}
    if unexpected:
        raise ToolError("invalid_argument", "Arguments do not apply to this view: " + ", ".join(sorted(unexpected)))


def bounded(data, limit):
    if isinstance(data, list):
        return {"items": data[:limit], "returned": min(len(data), limit), "truncated": len(data) > limit}
    if isinstance(data, dict):
        data = dict(data)
        for key in ("items", "results", "checkpoints", "sessions"):
            if isinstance(data.get(key), list) and len(data[key]) > limit:
                data[key] = data[key][:limit]
                data["truncated"] = True
    return data


def execute(name, args, cli=None):
    validate(name, args)
    cli = cli or CLI()
    root = cli.checkout(args["repo_path"]) if "repo_path" in args else None
    if name == "agent_help":
        return {"repo_path": root, "data": cli.help(args.get("command", ""), root)}
    if name == "entire_status":
        data = cli.read("status", root, {"json": True})
        return {"repo_path": root, "cli_version": cli.run(["version"], root).splitlines()[0], "data": data}
    if name == "search":
        mode = args.get("mode", "history")
        if mode == "code" and any(k in args for k in ("page", "branch", "author", "date")):
            raise ToolError("invalid_argument", "Code search cannot use history-only pagination, author, branch or date filters.")
        flags = {"json": True, "limit": args.get("limit", 5)}
        for key in ("repo", "branch", "author", "date", "page"):
            if key in args:
                flags[key] = args[key]
        optional = {"compact": True} if mode == "history" else {}
        if mode == "code":
            flags["code"] = True
        data = cli.read("search", root, flags, args["query"], optional)
    elif name == "checkpoint_read":
        view = args.get("view", "metadata")
        target = args.get("target")
        if not target and view != "metadata":
            raise ToolError("invalid_argument", "Context/transcript reads require an explicit checkpoint or commit target.")
        if target and "session_id" in args:
            raise ToolError("invalid_argument", "session_id filters list metadata; it cannot be combined with a target.")
        if view != "transcript" and any(k in args for k in ("session_index", "task")):
            raise ToolError("invalid_argument", "session_index and task apply only to transcript reads.")
        if args.get("repo") and not target:
            raise ToolError("invalid_argument", "Cross-repository checkpoint reads require an explicit full target ID.")
        flags = {}
        if view == "metadata":
            flags["json"] = True
            if not target:
                flags["limit"] = args.get("limit", 10)
        if view == "transcript":
            flags["transcript"] = True
        for arg, flag in (("repo", "repo"), ("session_id", "session"), ("session_index", "session-index"), ("task", "task")):
            if arg in args:
                flags[flag] = args[arg]
        if view == "metadata" and any(k in args for k in ("offset_bytes", "max_bytes")):
            raise ToolError("invalid_argument", "Byte excerpts apply only to context/transcript reads.")
        data = cli.read("checkpoint explain", root, flags, target, {"no-pager": True}, text=view != "metadata",
                        excerpt=(args.get("offset_bytes", 0), args.get("max_bytes", 32768)))
    elif name == "session_read":
        view = args.get("view", "current")
        target = args.get("session_id")
        if (view in ("info", "transcript")) != bool(target):
            raise ToolError("invalid_argument", "Only info/transcript views require and accept session_id.")
        command = "session " + ("info" if view == "transcript" else view)
        if view != "transcript" and any(k in args for k in ("offset_bytes", "max_bytes")):
            raise ToolError("invalid_argument", "Byte excerpts apply only to transcript reads.")
        data = cli.read(command, root, {"transcript" if view == "transcript" else "json": True}, target, text=view == "transcript",
                        excerpt=(args.get("offset_bytes", 0), args.get("max_bytes", 32768)))
        if view == "current" and isinstance(data, dict):
            data = dict(data)
            matching_worktree = not data.get("worktree_path") or str(Path(data["worktree_path"]).resolve()) == root
            data["verified_caller"] = data.get("resolution") in ("caller-env", "ancestry") and matching_worktree
            if not data["verified_caller"]:
                data["warning"] = "This session is not verified as this chat in the selected checkout. Select the intended session explicitly before handoff or continuation."
    elif name == "why":
        file = Path(args["file"])
        file = (Path(root) / file).resolve() if not file.is_absolute() else file.resolve()
        if not file.is_relative_to(Path(root)) or not file.is_file():
            raise ToolError("invalid_file", "file must resolve to an existing file inside the selected checkout.")
        flags = {"json": True}
        if "line" in args:
            flags["line"] = args["line"]
        data = cli.read("why", root, flags, str(file.relative_to(root)))
        if isinstance(data, dict) and set(data) <= {"file", "line"}:
            data = {**data, "evidence": "No commit/checkpoint attribution was returned for this location."}
    elif name == "trail_read":
        view = args.get("view", "list")
        if view == "list":
            allowed(args, {"project", "repo", "status", "page_token"})
            if "project" not in args:
                raise ToolError("invalid_argument", "Trail listing requires an explicit project such as gh/<owner> or et/<project>.")
            if args.get("status") not in (None, "open", "closed"):
                raise ToolError("invalid_argument", "Trail lifecycle status is open or closed; omit it for all states.")
        elif view == "findings":
            allowed(args, {"project", "repo", "selector", "status", "freshness", "cursor"})
        else:
            allowed(args, {"project", "repo", "selector"})
        selector = args.get("selector")
        if selector and "://" in selector:
            raise ToolError("invalid_argument", "Resolve the URL to a project/change selector using installed trail help first.")
        flags = {"json": True}
        for arg, flag in (("project", "project"), ("repo", "repo"), ("status", "status"), ("freshness", "freshness"), ("cursor", "cursor"), ("page_token", "page-token")):
            if arg in args:
                flags[flag] = args[arg]
        if view in ("list", "findings"):
            flags["limit"] = args.get("limit", 10)
        command = "trail " + ({"findings": "finding list"}.get(view, view))
        data = cli.read(command, root, flags, selector)
    is_list = name == "search" or name == "trail_read" and args.get("view", "list") != "show" or name == "session_read" and args.get("view") == "list" or name == "checkpoint_read" and not args.get("target")
    return {"repo_path": root, "data": bounded(data, args.get("limit", 10)) if is_list else data}
