import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SERVER = Path(__file__).resolve().parents[1] / "entire" / "server"
sys.path.insert(0, str(SERVER))

from main import dispatch, serve
from process import CLI, ToolError
from tools import execute


class RecordedCLI(CLI):
    """Provider output double: proves adapter decisions, not Entire behavior."""

    def __init__(self, data=None, flags=None):
        self.data = data if data is not None else {}
        self.flags = flags if flags is not None else {
            "json", "compact", "limit", "page", "repo", "code", "author", "branch", "date",
            "no-pager", "session", "session-index", "transcript", "task", "line",
            "project", "status", "freshness", "cursor", "page-token",
        }
        self.calls = []

    def checkout(self, value):
        return str(Path(value).resolve())

    def run(self, args, cwd=None, executable="entire", excerpt=None):
        self.calls.append((args, cwd))
        if args[0] == "agent-help":
            return json.dumps({"command": "entire " + " ".join(args[1:-1]),
                               "flags": [{"name": name} for name in self.flags]})
        if args[0] == "version":
            return "Entire CLI test-version\n"
        if excerpt:
            return {"text": json.dumps(self.data), "offset_bytes": excerpt[0], "total_bytes": 2, "next_offset_bytes": None, "truncated": False}
        return json.dumps(self.data)


class AdapterTests(unittest.TestCase):
    def test_repo_path_is_required_instead_of_process_cwd(self):
        with self.assertRaisesRegex(ToolError, "Missing required"):
            execute("entire_status", {})

    def test_zero_exit_json_error_is_not_disabled_status(self):
        cli = RecordedCLI({"enabled": False, "error": "not a git repository"})
        with self.assertRaises(ToolError) as result:
            execute("entire_status", {"repo_path": tempfile.gettempdir()}, cli)
        self.assertEqual(result.exception.code, "not_git_repository")

    def test_fallback_session_is_not_identified_as_caller(self):
        cli = RecordedCLI({"session_id": "other-session", "resolution": "other-worktree"})
        result = execute("session_read", {"repo_path": tempfile.gettempdir()}, cli)
        self.assertFalse(result["data"]["verified_caller"])
        self.assertIn("Select the intended session", result["data"]["warning"])

    def test_verified_session_is_recognized_without_fallback_warning(self):
        for resolution in ("caller-env", "ancestry"):
            with self.subTest(resolution=resolution):
                result = execute("session_read", {"repo_path": tempfile.gettempdir()}, RecordedCLI({"resolution": resolution}))
                self.assertTrue(result["data"]["verified_caller"])
                self.assertNotIn("warning", result["data"])

    def test_search_preserves_optional_field_absence_and_quotes_query_as_data(self):
        query = 'retry; "quotes" $(literal) --generate'
        hit = {"id": "commit-id", "type": "commit"}
        cli = RecordedCLI({"results": [hit]})
        result = execute("search", {"repo_path": tempfile.gettempdir(), "query": query}, cli)
        self.assertEqual(result["data"]["results"], [hit])
        args, cwd = cli.calls[-1]
        self.assertEqual(args[-2:], ["--", query])
        self.assertEqual(cwd, str(Path(tempfile.gettempdir()).resolve()))

    def test_code_search_rejects_history_only_filters(self):
        with self.assertRaisesRegex(ToolError, "history-only"):
            execute("search", {"repo_path": tempfile.gettempdir(), "query": "Token", "mode": "code", "page": 2}, RecordedCLI())

    def test_transcript_requires_target_and_preserves_selected_session(self):
        cli = RecordedCLI()
        with self.assertRaisesRegex(ToolError, "explicit checkpoint"):
            execute("checkpoint_read", {"repo_path": tempfile.gettempdir(), "view": "transcript"}, cli)
        execute("checkpoint_read", {"repo_path": tempfile.gettempdir(), "target": "abc123def456", "view": "transcript", "session_index": 0}, cli)
        args = cli.calls[-1][0]
        self.assertIn("--session-index=0", args)
        self.assertIn("--transcript", args)
        self.assertNotIn("--generate", args)

    def test_targeted_checkpoint_preserves_every_contributing_session(self):
        sessions = [{"id": f"session-{i}"} for i in range(15)]
        result = execute("checkpoint_read", {"repo_path": tempfile.gettempdir(), "target": "abc123def456"}, RecordedCLI({"sessions": sessions}))
        self.assertEqual(result["data"]["sessions"], sessions)

    def test_large_text_can_be_read_in_bounded_excerpts(self):
        args = ["-c", "import sys;sys.stdout.write('a'*1100000+'end')"]
        first = CLI().run(args, executable=sys.executable, excerpt=(0, 1024))
        last = CLI().run(args, executable=sys.executable, excerpt=(1100000, 1024))
        self.assertEqual(len(first["text"]), 1024)
        self.assertEqual(first["next_offset_bytes"], 1024)
        self.assertTrue(first["truncated"])
        self.assertEqual(last["text"], "end")
        self.assertIsNone(last["next_offset_bytes"])
        self.assertEqual(first["total_bytes"], last["total_bytes"])

    def test_transcript_pages_preserve_multibyte_characters(self):
        text = "a" * 1023 + "\U0001f600" + "end"
        args = ["-c", "import sys;sys.stdout.buffer.write(" + repr(text.encode()) + ")"]
        first = CLI().run(args, executable=sys.executable, excerpt=(0, 1024))
        second = CLI().run(args, executable=sys.executable, excerpt=(first["next_offset_bytes"], 1024))
        self.assertEqual(first["text"] + second["text"], text)
        self.assertEqual(first["next_offset_bytes"], 1023)
        inside = CLI().run(args, executable=sys.executable, excerpt=(1025, 1024))
        self.assertEqual(inside["offset_bytes"], 1023)
        self.assertEqual(inside["text"], "\U0001f600end")

    def test_missing_cli_capability_fails_before_command_execution(self):
        cli = RecordedCLI(flags={"limit"})
        with self.assertRaises(ToolError) as result:
            execute("search", {"repo_path": tempfile.gettempdir(), "query": "retry"}, cli)
        self.assertEqual(result.exception.code, "unsupported_cli")
        self.assertEqual(len(cli.calls), 1)

    def test_trail_listing_requires_project_and_disallows_other_view_filters(self):
        with self.assertRaisesRegex(ToolError, "explicit project"):
            execute("trail_read", {"repo_path": tempfile.gettempdir()}, RecordedCLI())
        with self.assertRaisesRegex(ToolError, "do not apply"):
            execute("trail_read", {"repo_path": tempfile.gettempdir(), "project": "gh/example", "cursor": "next"}, RecordedCLI())

    def test_write_options_and_unknown_tools_cannot_reach_cli(self):
        for name, args in (("checkpoint_read", {"generate": True}), ("run", {"command": "enable"})):
            with self.subTest(name=name), self.assertRaises(ToolError):
                execute(name, {"repo_path": tempfile.gettempdir(), **args}, RecordedCLI())

    def test_stdio_recovers_after_invalid_json_and_responds_to_notifications_silently(self):
        source = io.StringIO('not-json\n' + json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + '\n' + json.dumps({"jsonrpc": "2.0", "id": 7, "method": "tools/list"}) + '\n')
        output = io.StringIO()
        serve(source, output)
        responses = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(len(responses), 2)
        self.assertEqual(responses[0]["error"]["code"], -32700)
        self.assertEqual(responses[1]["id"], 7)
        self.assertEqual(len(responses[1]["result"]["tools"]), 7)

    def test_protocol_negotiates_only_supported_versions(self):
        self.assertEqual(dispatch("initialize", {"protocolVersion": "2024-11-05"})["protocolVersion"], "2024-11-05")
        self.assertNotEqual(dispatch("initialize", {"protocolVersion": "unknown"})["protocolVersion"], "unknown")

    @unittest.skipUnless(shutil.which("git"), "Git is required for real checkout isolation")
    def test_two_real_git_checkouts_do_not_inherit_mcp_cwd(self):
        with tempfile.TemporaryDirectory() as directory:
            roots = [Path(directory) / name for name in ("first repo", "second-repo")]
            for root in roots:
                subprocess.run(["git", "-c", "init.defaultBranch=main", "init", "-q", str(root)], check=True)
                nested = root / "nested"
                nested.mkdir()
                self.assertEqual(CLI().checkout(str(nested)), str(root.resolve()))
            self.assertNotEqual(CLI().checkout(str(roots[0])), CLI().checkout(str(roots[1])))

    @unittest.skipUnless(shutil.which("git"), "Git is required for inherited-environment isolation")
    def test_inherited_git_directory_cannot_override_selected_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second, plain = [Path(directory) / name for name in ("one", "two", "plain")]
            for root in (first, second):
                subprocess.run(["git", "init", "-q", str(root)], check=True)
            plain.mkdir()
            with patch.dict(os.environ, {"GIT_DIR": str(first / ".git"), "GIT_WORK_TREE": str(first)}):
                self.assertEqual(CLI().checkout(str(second)), str(second.resolve()))
                with self.assertRaises(ToolError) as error:
                    CLI().checkout(str(plain))
                self.assertEqual(error.exception.code, "not_git_repository")

    def test_cli_uses_argv_without_a_shell(self):
        value = 'data;$(literal) "quotes"'
        output = CLI().run(["-c", "import json,sys;print(json.dumps(sys.argv[1]))", value], executable=sys.executable)
        self.assertEqual(json.loads(output), value)

    @unittest.skipUnless(os.environ.get("ENTIRE_LIVE_TEST") == "1", "Set ENTIRE_LIVE_TEST=1 for installed CLI checks")
    def test_live_entire_in_clean_repo_reports_missing_setup_without_changing_it(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(["git", "-c", "init.defaultBranch=main", "init", "-q", directory], check=True)
            with self.assertRaises(ToolError) as result:
                execute("entire_status", {"repo_path": directory})
            self.assertEqual(result.exception.code, "setup_required")
            self.assertFalse((Path(directory) / ".entire").exists())


if __name__ == "__main__":
    unittest.main()
