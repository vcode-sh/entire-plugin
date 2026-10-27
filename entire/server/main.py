"""Dependency-free stdio MCP server for Entire's read-only workflow adapter."""

import json
from pathlib import Path
import sys

from process import ToolError
from schema import definitions
from tools import execute


SUPPORTED_PROTOCOLS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")
VERSION = json.loads((Path(__file__).resolve().parents[1] / "plugin.json").read_text())["version"]


def tool_result(value, error=False):
    return {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}],
            "structuredContent": value, "isError": error}


def dispatch(method, params):
    if method == "initialize":
        requested = params.get("protocolVersion")
        return {"protocolVersion": requested if requested in SUPPORTED_PROTOCOLS else SUPPORTED_PROTOCOLS[0],
                "capabilities": {"tools": {}}, "serverInfo": {"name": "entire-community", "version": VERSION}}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": definitions()}
    if method == "tools/call":
        try:
            return tool_result(execute(params.get("name"), params.get("arguments", {})))
        except ToolError as error:
            return tool_result({"error": {"code": error.code, "message": str(error)}}, True)
    raise ToolError("method_not_found", "Unsupported MCP method.")


def serve(source, output):
    while True:
        line = source.readline(1_048_578)
        if not line:
            return
        if not line.strip():
            continue
        if not line.endswith("\n") and len(line.encode("utf-8")) > 1_048_576:
            while line and not line.endswith("\n"):
                line = source.readline(1_048_578)
            output.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Request exceeds 1 MiB."}}) + "\n")
            output.flush()
            continue
        request_id = None
        try:
            if len(line.encode("utf-8")) > 1_048_576:
                raise ValueError("Request exceeds 1 MiB.")
            request = json.loads(line)
        except (ValueError, json.JSONDecodeError):
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Invalid or oversized JSON request."}}
        else:
            if not isinstance(request, dict) or request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str) or not request.get("method") or not isinstance(request.get("params", {}), dict) or not (request.get("id") is None or type(request.get("id")) in (str, int)):
                response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid request."}}
            elif "id" not in request:
                continue
            else:
                request_id = request["id"]
                try:
                    result = dispatch(request["method"], request.get("params", {}))
                    response = {"jsonrpc": "2.0", "id": request_id, "result": result}
                except ToolError:
                    response = {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "Method not found."}}
                except Exception:
                    response = {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32603, "message": "Internal adapter error; no traceback or environment was returned."}}
        output.write(json.dumps(response, ensure_ascii=False) + "\n")
        output.flush()


if __name__ == "__main__":
    serve(sys.stdin, sys.stdout)
