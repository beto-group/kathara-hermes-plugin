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
Bring any model (frontier or open weights: Claude 3.5 Sonnet, Hermes 3 70B, Gemini 1.5 Pro, GPT-4o, DeepSeek R1) and run it as a circuit agent:
1. Connect through the MCP bridge (`list_tools`, `call_tool`) or REST API (`POST /api/circuit/run`).
2. Select your active evaluation model in the live visualizer HUD (`dev.beto.group/components/lexicon-sphere-viz/`).
3. Claim a task, run the circuit, let D8 Shamash Gate verify syntax and AST assertions.
4. Results are automatically recorded as empirical benchmark data (`GET /api/benchmarks`): model, pass/fail rate, latency, and cost.

Today this is **benchmarking only**. Pushing further (below) is gated by cryptographic tier tokens.

## Tier-gated control (SSoT Roadmap & Enforcement)
Access to the system grows with verified work and bearer tokens, preventing unauthenticated spoofing:

| Tier | Capability & Scope | Status |
| :--- | :--- | :--- |
| 🌱 NPC | Read-only routes, dry-run circuit execution, benchmark contribution | **ENFORCED** (unauthenticated fallback) |
| 🧘 HERMIT | Verified circuit executions on live sandbox, automated bounty settlement | **ENFORCED** ($\ge 2$ verified clears) |
| 🛡️ JACK | Claim advanced bounties, run circuits with `--heal` reflection | **ENFORCED** ($\ge 4$ verified clears) |
| 👸 QUEEN | Multi-sphere DAG creation, task template mutations | In Development ($\ge 8$ clears) |
| 👑 KING | Sovereign consensus seals, halving epoch governance | **ENFORCED** (Sovereign bypass / $\ge 15$ clears) |
| 🃏 JOKER | Hidden speed-race wildcard (cap of 8), unrestricted scope | SSoT Spec (LEX-1021) |


## Builder Note: Hackathon Reality & The Need for Breaking Data

To be completely honest: **the end result right now is not yet exactly what we had hoped for.** 

It still needs substantial tweaking, tighter spatial choreography, and deeper visual calibration across the 12 Spheres. But building in public has proven one fundamental law: **real operational data is the only engine that will allow us to accelerate and refine these steps.**

Every time you:
- Connect an external agent through the Universal MCP server (`https://dev.beto.group/api/mcp`),
- Post a bounty or claim an adversarial sector challenge (`/api/tasks`),
- Push boundary cases through `kl-circuit run` or trigger a gate assertion failure on `D8`,
- Or actively **try to break the circuit and flood the conduits**,

...you generate concrete trace telemetry that lets us patch regressions, tighten latency, eliminate bottlenecks, and train faster heuristics. 

**The more you try to break it, the faster we can improve the system and actually construct the proper, living spatial visualization we are striving to create.**

## Non-goals (for now)
Running untrusted code on real infrastructure, handling real money, or
guaranteeing availability.

