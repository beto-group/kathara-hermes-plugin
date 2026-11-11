#!/usr/bin/env python3
"""
60-Second Interactive Showcase Demo for Hermes Hackathon Judges.
Demonstrates live route evaluation, AST substrate extraction, D8 Gate checks,
and leaderboard reward minting on the Kathara Grid.
"""

import sys
import time
from pathlib import Path

# Ensure local package importable when running from repository root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hermes_kathara.client import KatharaClient
from hermes_kathara.circuit import KatharaCircuitRunner


def print_banner():
    banner = """
    ╔═════════════════════════════════════════════════════════════════╗
    ║        KATHARA GRID // NOUS HERMES AUTONOMOUS CIRCUIT           ║
    ║   Opening the LLM Black Box: Executable Subagent Architecture   ║
    ╚═════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    print_banner()

    agent_id = "agent/hermes-judge"
    print(f"[*] Initializing client connection as [{agent_id}]...")
    client = KatharaClient(agent_profile=agent_id)

    # 1. MCP Handshake
    print(f"[*] Connecting to remote grid at {client.endpoint}...")
    init_res = client.initialize()
    print(f"    ✓ Connected! Server: {init_res['serverInfo']['name']} v{init_res['serverInfo']['version']} (Protocol {init_res['protocolVersion']})")

    # Ensure operator ToS consent for the demo runner
    client.call_tool("kathara_confirm_tos", {"operator_handle": agent_id, "agreed": True})

    # 2. Browse Tools & Resources
    tools = client.list_tools()
    resources = client.list_resources()
    print(f"    ✓ Discovered {len(tools)} Circuit Tools and {len(resources)} Native Resources.")

    # 3. Route Deliberation (Black Box Opened)
    goal = "Synthesize and verify Creator Gate invariant assertion"
    print(f"\n[D5 Laya Vortex] Evaluating candidate execution routes for goal: '{goal}'...")
    eval_res = client.call_tool("kathara_evaluate_routes", {"goal": goal, "component": "portal-api"})
    candidates = eval_res.get("candidate_paths", [])
    for p in candidates:
        star = "★ SELECTED" if p.get("status") == "selected" else "  candidate"
        print(f"    [{star}] {p['id'].upper():12s} | Score: {p.get('score')} | Cost: ${p.get('cost_usd', 0):.4f} | Blast Radius: {p.get('blast_radius')}")

    # 4. Read Substrate
    print("\n[D1 Abzu Seed] Extracting physical AST substrate from 'portal-api' without shell pollution...")
    sub_res = client.call_tool("kathara_read_substrate", {"component": "portal-api", "start_line": 1, "end_line": 10})
    target_file = sub_res.get("resolved_file", "/opt/data/dev.beto.group/portal-api.py")
    print(f"    ✓ Extracted lines 1-10 from {target_file}:")
    for line in sub_res.get("content", "").splitlines()[:5]:
        print(f"      | {line}")

    # 5. D6 Markdown Task Note Creation
    print("\n[D6 Enki Mind] Minting persistent Markdown task note...")
    task_res = client.call_tool("kathara_create_task", {
        "title": "Hermes Hackathon Golden Circuit Verification",
        "goal": goal,
        "component": "portal-api"
    })
    task_id = task_res.get("task_id", "TASK-DEMO-JUDGE")
    print(f"    ✓ Created task note: {task_id} ({task_res.get('path')})")

    # 6. D8 Shamash Gate Verification
    print("\n[D8 Shamash Gate] Running deterministic compiler and assertion checks...")
    gate_res = client.call_tool("kathara_verify_gate", {
        "task_id": task_id,
        "component": "portal-api",
        "target_file": target_file
    })
    print(f"    ✓ Verdict: {gate_res.get('verdict')} (Attestation: {gate_res.get('attestation')})")
    print(f"      Details: {gate_res.get('details')}")

    # 7. Settle Contributor Rewards & Tier Status
    print("\n[D11 Nanna Feedback] Querying Contributor Telemetry & Leaderboard...")
    tier_status = client.call_tool("kathara_get_tier_status", {"operator_handle": agent_id})
    print(f"    ★ Active Tier: {tier_status.get('tier', '🌱 NPC')} | Multiplier: {tier_status.get('multiplier', '1.0x')}")
    print(f"    ★ Verified Events: {tier_status.get('verified_events', {})}")

    # 8. Live Visualizer Link
    print("\n" + "=" * 65)
    print("  ★ Telemetry Pulses Emitted to Live Visualizer HUD:")
    print("  ★ https://dev.beto.group/components/lexicon-sphere-viz/")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()

