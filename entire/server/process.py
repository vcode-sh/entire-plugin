"""Bounded, non-interactive CLI execution for read-only tools."""

import codecs
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


class ToolError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def classify(message):
    lower = message.lower()
    for needle, code in (
        ("no entire-checkpoint trailer", "no_checkpoint"),
        ("not a git repository", "not_git_repository"),
        ("not set up", "setup_required"),
        ("object not found", "history_unavailable"),
        ("no active session", "session_unavailable"),
        ("keychain", "access_unavailable"),
        ("network is not allowed", "access_unavailable"),
        ("authentication required", "authentication_required"),
        ("not authenticated", "authentication_required"),
        ("unknown flag", "unsupported_cli"),
        ("unknown command", "unsupported_cli"),
    ):
        if needle in lower:
            return code
    return "cli_error"


def diagnostic(message):
    message = re.sub(r"(https?://)[^\s/@]+:[^\s/@]+@", r"\1[redacted]@", message)
    message = re.sub(r"(?i)(bearer\s+)[^\s]+", r"\1[redacted]", message)
    return message.strip()[:1500]


class CLI:
    def run(self, args, cwd=None, executable="entire", excerpt=None):
        location_overrides = {"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",
                              "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                              "GIT_CONFIG", "GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS",
                              "GIT_NAMESPACE", "GIT_SHALLOW_FILE", "GIT_PREFIX"}
        env = {key: value for key, value in os.environ.items()
               if key not in location_overrides and not key.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"))}
        env.update(ENTIRE_NO_AUTO_UPDATE="1", GIT_TERMINAL_PROMPT="0")
        try:
            with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
                result = subprocess.run(
                    [executable, *args], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                    stdout=stdout, stderr=stderr, timeout=40, check=False,
                )
                total = stdout.seek(0, 2)
                offset, maximum = excerpt if excerpt else (0, 1_048_577)
                offset = min(offset, total)
                if excerpt:
                    for _ in range(3):
                        stdout.seek(offset)
                        first = stdout.read(1)
                        if not offset or not first or first[0] & 0xC0 != 0x80:
                            break
                        offset -= 1
                stdout.seek(offset)
                stderr.seek(0)
                output = stdout.read(maximum)
                errors = stderr.read(4096).decode("utf-8", errors="replace")
            if not excerpt and len(output) > 1_048_576:
                raise ToolError("output_too_large", "CLI output exceeds 1 MiB. Narrow the query or use a specific session/checkpoint.")
            text = output.decode("utf-8", errors="replace")
            if result.returncode:
                message = diagnostic(errors or text or f"{executable} exited with code {result.returncode}.")
                raise ToolError(classify(message), message)
            if excerpt:
                decoder = codecs.getincrementaldecoder("utf-8")("replace")
                text = decoder.decode(output, final=offset + len(output) >= total)
                end = offset + len(output) - len(decoder.getstate()[0])
                return {"text": text, "offset_bytes": offset, "total_bytes": total,
                        "next_offset_bytes": end if end < total else None,
                        "truncated": offset > 0 or end < total}
            return text
        except FileNotFoundError:
            raise ToolError("executable_missing", f"{executable} is not available on the MCP host's PATH.") from None
        except subprocess.TimeoutExpired:
            raise ToolError("timeout", "The read exceeded 40 seconds. Narrow the request; no automatic retry or repair was attempted.") from None
        except OSError as error:
            raise ToolError("execution_unavailable", diagnostic(str(error))) from None

    def checkout(self, value):
        path = Path(value).expanduser()
        if not path.is_absolute() or not path.is_dir():
            raise ToolError("invalid_repo_path", "repo_path must be an existing absolute checkout directory on the MCP host.")
        root = self.run(["-C", str(path), "rev-parse", "--show-toplevel"], executable="git").strip()
        return str(Path(root).resolve())

    def help(self, command, cwd=None):
        if command and not re.fullmatch(r"[a-z0-9-]+(?: [a-z0-9-]+)*", command):
            raise ToolError("invalid_argument", "command must be a space-separated CLI command path, without flags.")
        value = self.run(["agent-help", *command.split(), "--json"], cwd)
        try:
            data = json.loads(value)
        except json.JSONDecodeError:
            raise ToolError("unsupported_cli", "The installed CLI did not return structured agent-help.") from None
        expected = "entire" + (" " + command if command else "")
        if not isinstance(data, dict) or data.get("command") != expected:
            raise ToolError("unsupported_cli", "Installed help did not resolve the requested command.")
        return data

    def read(self, command, cwd, flags=None, target=None, optional=None, text=False, excerpt=None):
        help_data = self.help(command, cwd)
        available = {flag["name"] for flag in help_data.get("flags", [])}
        flags = dict(flags or {})
        for key, value in (optional or {}).items():
            if key in available:
                flags[key] = value
        missing = set(flags) - available
        if missing:
            raise ToolError("unsupported_cli", "Installed CLI lacks required flags: " + ", ".join(sorted(missing)))
        args = command.split()
        for key, value in flags.items():
            if value is not None:
                args.append(f"--{key}" if value is True else f"--{key}={value}")
        if target is not None:
            args.extend(["--", target])
        output = self.run(args, cwd, excerpt=excerpt) if text else self.run(args, cwd)
        if text:
            return output
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            raise ToolError("invalid_cli_output", "The CLI returned non-JSON output; it was not treated as an empty result.") from None
        if isinstance(data, dict) and data.get("error"):
            message = diagnostic(str(data["error"]))
            raise ToolError(classify(message), message)
        return data
