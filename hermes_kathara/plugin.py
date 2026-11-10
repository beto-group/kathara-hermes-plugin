"""
Hermes Kathara Plugin: Tool definition & execution adapter for Nous Hermes.
Supports native Hermes function calling schemas (<tools> XML / JSON schema).
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from .client import KatharaClient


class HermesKatharaPlugin:
    """Plugin wrapper providing Kathara 12-Sphere capabilities to Nous Hermes."""

    def __init__(
        self,
        endpoint: str = KatharaClient.DEFAULT_ENDPOINT,
        agent_profile: str = "agent/hermes-agent",
    ):
        self.client = KatharaClient(endpoint=endpoint, agent_profile=agent_profile)

    def get_hermes_tool_definitions(self) -> List[Dict[str, Any]]:
        """Return tool schemas in standard Hermes / OpenAI function-calling format."""
        raw_tools = self.client.list_tools()
        formatted = []
        for t in raw_tools:
            formatted.append({
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "parameters": t.get("inputSchema", {
                        "type": "object",
                        "properties": {},
                    }),
                },
            })
        return formatted

    def get_hermes_xml_prompt(self) -> str:
        """Return Hermes-compatible <tools> XML specification block."""
        tools = self.get_hermes_tool_definitions()
        xml_lines = ["<tools>"]
        for t in tools:
            fn = t["function"]
            xml_lines.append(json.dumps(fn, indent=2))
        xml_lines.append("</tools>")
        xml_lines.append(
            "\nFor each function call, return a json object with function name and arguments within <tool_call></tool_call> tags:"
        )
        xml_lines.append("<tool_call>\n{\"name\": <function-name>, \"arguments\": <args-json-object>}\n</tool_call>")
        return "\n".join(xml_lines)

    def execute_tool_call(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call emitted by Hermes and return structured output."""
        return self.client.call_tool(name, arguments)

    # Convenience shortcuts mapped to the 12 Spheres
    def evaluate_routes(self, goal: str, component: str = "portal-api") -> Dict[str, Any]:
        """D5 Laya Vortex: Score candidate routes (Path-Alpha vs Beta vs Gamma)."""
        return self.client.call_tool("kathara_evaluate_routes", {"goal": goal, "component": component})

    def read_substrate(self, component: str, start_line: int = 1, end_line: int = 100) -> Dict[str, Any]:
        """D1 Abzu Seed: Safely inspect AST substrate code slices without shell pollution."""
        return self.client.call_tool("kathara_read_substrate", {
            "component": component,
            "start_line": start_line,
            "end_line": end_line,
        })

    def submit_diff(self, task_id: str, component: str, target_file: str, diff_text: str) -> Dict[str, Any]:
        """D7 Inanna Vessel: Register a scoped unified diff and log to task journal."""
        return self.client.call_tool("kathara_submit_diff", {
            "task_id": task_id,
            "component": component,
            "target_file": target_file,
            "diff_text": diff_text,
        })

    def verify_gate(self, task_id: str, component: str) -> Dict[str, Any]:
        """D8 Shamash Gate: Deterministic compiler checks, syntax verification, and test invariants."""
        return self.client.call_tool("kathara_verify_gate", {"task_id": task_id, "component": component})

    def list_tasks(self, sector: str = "all", status: str = "open_bounty") -> Dict[str, Any]:
        """D5 Task Board: List open bounties across sectors."""
        return self.client.call_tool("kathara_list_tasks", {"sector": sector, "status": status})

    def claim_task(self, task_id: str) -> Dict[str, Any]:
        """D6 Enki Mind: Claim a task and lock it for your Hermes agent profile."""
        return self.client.call_tool("kathara_claim_task", {
            "task_id": task_id,
            "claimed_by": self.client.agent_profile,
        })

    def reward_bounty(self, task_id: str, weight_delta: float = 0.05, reason: str = "") -> Dict[str, Any]:
        """D11 Nanna Cycle: Settle verified task and mint $KI tokens."""
        return self.client.call_tool("kathara_reward_bounty", {
            "task_id": task_id,
            "recipient": self.client.agent_profile,
            "weight_delta": weight_delta,
            "reason": reason or "Verified task completed via Hermes",
        })

    def get_leaderboard(self) -> Dict[str, Any]:
        """D11 Rewards: Query current daily leaderboard standings."""
        return self.client.call_tool("kathara_get_leaderboard", {})
