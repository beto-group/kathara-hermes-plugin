# Kathara / Hermes Control — Research Prototype

> **Status: experimental research prototype.** This is not a production operating
> system. It is a playground for exploring MCP-driven agent circuits and
> visualizing them live. Expect rough edges, breaking changes and simulated parts.

## What it is
- An **explorable visualization** (Kathara Viz, `dev.beto.group`) of a 12-sphere
  agent circuit (D5 → D6 → D1 → D7 → D8 → D10), driven by real MCP tools.
- An **MCP bridge** (`bridge/`) that lets outside agents request broker-gated
  Hermes tools with owner approval.
- A **benchmark harness** idea: run the same task through the circuit with
  different models and compare gate (D8) pass rates, cost and latency.

## What is real vs. simulated
| Piece | State |
| :--- | :--- |
| Task notes (Markdown SSoT) + `kl-circuit run` | Real, minimal |
| D8 gate | Real but shallow (syntax/assertion checks) |
| `$KI` rewards / tiers | Experimental scoring, **not a currency** |
| Route "probabilities", some telemetry values | Partly illustrative |
| Anti-cheat (double-spend, clamping, task-id validation, locks) | Implemented, not security-audited |

## Contribute with stronger models
Bring any model (including frontier ones) and run it as a circuit agent:
1. Connect through the MCP bridge (`list_tools`, `call_tool`).
2. Claim a task, run the circuit, let D8 verify.
3. Results are recorded as benchmark data (model, pass/fail, latency, cost).

Today this is **benchmarking only**. Pushing further (below) is gated by tier.

## Tier-gated control (proposed — roadmap)
Access to the system grows with verified work, not with claims.

| Tier | Intended capability |
| :--- | :--- |
| 🌱 NPC | Read, evaluate routes, dry-run circuits |
| 🧘 HERMIT | Run circuits on sandbox tasks, submit benchmark results |
| 🛡️ JACK | Claim bounties, run circuits with `--heal` |
| 👸 QUEEN | Propose new routes/spheres, edit task templates |
| 👑 KING | Vote on gate rules and consensus seals |
| 🃏 JOKER | Hidden, creator-appointed, unrestricted scope |

Enforcement lives server-side (`portal-api.py`); the UI only reflects it.
Tier checks on the endpoints beyond rewards are **not yet implemented**.

## Non-goals (for now)
Running untrusted code on real infrastructure, handling real money, or
guaranteeing availability.

