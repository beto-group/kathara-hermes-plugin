#!/usr/bin/env python3
"""
60-Second Interactive Showcase Demo for Hermes Hackathon Judges.
Demonstrates live route evaluation, AST substrate extraction, D8 Gate checks,
and leaderboard reward minting on the Kathara Grid.
"""

import sys
import time
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
    print(f"    ✓ Extracted lines 1-10 from {sub_res.get('path')}:")
    for line in sub_res.get("content", "").splitlines()[:5]:
        print(f"      | {line}")

    # 5. D8 Shamash Gate Verification
    print("\n[D8 Shamash Gate] Running deterministic compiler and assertion checks...")
    gate_res = client.call_tool("kathara_verify_gate", {"task_id": "TASK-DEMO-JUDGE", "component": "portal-api"})
    print(f"    ✓ Verdict: {gate_res.get('verdict')} ({gate_res.get('details')})")

    # 6. Settle Contributor Rewards
    print("\n[D11 Nanna Feedback] Settling task invariant and minting $KI tokens...")
    reward_res = client.call_tool("kathara_reward_bounty", {
        "task_id": "TASK-DEMO-JUDGE",
        "recipient": agent_id,
        "weight_delta": 0.08,
        "reason": "Live Hackathon Judge demonstration pass"
    })
    print(f"    ★ Awarded: +{reward_res.get('tokens_awarded')} $KI Tokens!")
    print(f"    ★ New Balance: {reward_res.get('new_total_tokens')} $KI (Tier: {reward_res.get('tier')})")

    # 7. Live Visualizer Link
    print("\n" + "=" * 65)
    print("  ★ Telemetry Pulses Emitted to Live Visualizer HUD:")
    print("  ★ https://dev.beto.group/components/lexicon-sphere-viz/")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()

