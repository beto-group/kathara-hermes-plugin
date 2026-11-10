"""
Zero-dependency HTTP JSON-RPC 2.0 client for the Kathara Remote Grid MCP Server.
Connects 24/7 over public HTTPS without SSH keys or local environment setup.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional


class KatharaClient:
    """Client for connecting to the remote Kathara Grid MCP Server."""

    DEFAULT_ENDPOINT = "https://dev.beto.group/api/mcp"

    def __init__(
        self,
        endpoint: str = DEFAULT_ENDPOINT,
        agent_profile: str = "agent/hermes-agent",
        timeout: float = 30.0,
    ):
        self.endpoint = endpoint.rstrip("/")
        self.agent_profile = agent_profile
        self.timeout = timeout
        self._req_id = 0

    def _next_id(self) -> int:
        self._req_id += 1
        return self._req_id

    def _rpc_call(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params or {},
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-Agent-Profile": self.agent_profile,
            "X-Kathara-Branch": self.agent_profile,
            "User-Agent": f"Hermes-Kathara-Client/1.0 ({self.agent_profile})",
        }

        req = urllib.request.Request(self.endpoint, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                res = json.loads(raw)
                if "error" in res:
                    raise RuntimeError(f"Kathara MCP Error {res['error'].get('code')}: {res['error'].get('message')}")
                return res.get("result", {})
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise ConnectionError(f"HTTP {e.code} connecting to Kathara Grid ({self.endpoint}): {err_body}")
        except urllib.error.URLError as e:
            raise ConnectionError(f"Failed to reach Kathara Grid ({self.endpoint}): {e.reason}")

    def initialize(self) -> Dict[str, Any]:
        """Perform MCP initialize handshake."""
        return self._rpc_call("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}, "resources": {}},
            "clientInfo": {"name": "hermes-kathara-client", "version": "1.0.0"}
        })

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all 13 active circuit tools from Kathara Grid."""
        res = self._rpc_call("tools/list")
        return res.get("tools", [])

    def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Call a specific tool on the Kathara Grid."""
        args = arguments or {}
        if "branch" not in args:
            args["branch"] = self.agent_profile
        res = self._rpc_call("tools/call", {"name": name, "arguments": args})
        content = res.get("content", [])
        if content and content[0].get("type") == "text":
            try:
                return json.loads(content[0]["text"])
            except Exception:
                return {"text": content[0]["text"]}
        return res

    def list_resources(self) -> List[Dict[str, Any]]:
        """Browse native MCP resources (task notes, leaderboard, telemetry)."""
        res = self._rpc_call("resources/list")
        return res.get("resources", [])

    def read_resource(self, uri: str) -> str:
        """Read a live resource from the Kathara Grid (e.g. kathara://leaderboard)."""
        res = self._rpc_call("resources/read", {"uri": uri})
        contents = res.get("contents", [])
        if contents:
            return contents[0].get("text", "")
        return ""

