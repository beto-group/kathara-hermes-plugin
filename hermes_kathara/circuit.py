"""
High-level Kathara Subagent Circuit runner for Hermes agents.
Manages the deterministic pipeline: D5 -> D6 -> D1 -> D7 -> D8 -> D10.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional
from .client import KatharaClient


class KatharaCircuitRunner:
    """Orchestrates multi-agent execution across the 12 Spheres."""

    def __init__(self, client: Optional[KatharaClient] = None):
        self.client = client or KatharaClient()

    def run_goal(
        self,
        goal: str,
        component: str = "portal-api",
        target_file: str = "portal-api.py",
        diff_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute an end-to-end circuit for a user goal:
        1. [D5] Evaluate candidate routes (Alpha vs Gamma vs Beta).
        2. [D5] Create persistent Markdown task note.
        3. [D1] Read substrate code slices.
        4. [D7] Apply unified diff if provided.
        5. [D8] Run Shamash Gate compiler/test assertions.
        6. [D10] Deploy release.
        """
        start_time = time.time()
        journal = []

        # Step 1: D5 Route Deliberation
        eval_res = self.client.call_tool("kathara_evaluate_routes", {"goal": goal, "component": component})
        candidate_paths = eval_res.get("candidate_paths", [])
        selected_path = candidate_paths[0]["name"] if candidate_paths else "Path-Alpha"
        journal.append(f"Step 1 [D5 Laya Vortex]: Evaluated {len(candidate_paths)} candidate routes. Selected {selected_path}.")

        # Step 2: D5 Task Creation
        task_res = self.client.call_tool("kathara_create_task", {
            "title": f"Hermes Circuit: {goal[:45]}",
            "goal": goal,
            "component": component,
        })
        task_id = task_res.get("task_id", f"TASK-{int(time.time())}")
        journal.append(f"Step 2 [D5 Enki Mind]: Initialized task note {task_id}.")

        # Step 3: D1 Substrate Inspection
        sub_res = self.client.call_tool("kathara_read_substrate", {
            "component": component,
            "start_line": 1,
            "end_line": 60,
        })
        journal.append(f"Step 3 [D1 Abzu Seed]: Extracted {sub_res.get('total_lines', 0)} AST lines from {component}.")

        # Step 4: D7 Diff Manifestation (if diff supplied)
        if diff_text:
            diff_res = self.client.call_tool("kathara_submit_diff", {
                "task_id": task_id,
                "component": component,
                "target_file": target_file,
                "diff_text": diff_text,
            })
            journal.append(f"Step 4 [D7 Inanna Vessel]: Diff registered. Result: {diff_res.get('status', 'recorded')}.")

        # Step 5: D8 Shamash Gate Invariant Check
        gate_res = self.client.call_tool("kathara_verify_gate", {
            "task_id": task_id,
            "component": component,
            "target_file": target_file,
        })
        gate_passed = gate_res.get("verdict") == "PASS"
        journal.append(f"Step 5 [D8 Shamash Gate]: Verification {gate_res.get('verdict', 'UNKNOWN')}.")

        # Step 6: D10 Softmax Release
        if gate_passed:
            rel_res = self.client.call_tool("kathara_deploy_release", {
                "task_id": task_id,
                "component": component,
                "action": "reload",
            })
            journal.append(f"Step 6 [D10 Utu Avatar]: Release sealed. Signal: {rel_res.get('status', 'released')}.")

        elapsed = round(time.time() - start_time, 2)

        return {
            "ok": gate_passed,
            "task_id": task_id,
            "selected_path": selected_path,
            "elapsed_s": elapsed,
            "gate_verdict": gate_res.get("verdict", "FAIL"),
            "execution_journal": journal,
        }

