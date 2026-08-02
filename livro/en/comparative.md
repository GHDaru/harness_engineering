<!-- i18n fonte:benchmark/comparativo.md edicao:0.67 hash:a3570821 -->
# Consolidated Comparison — Rounds 1, 2, ext-1 and ext-2

> 15 harnesses evaluated by systematic code reading, 12 dimensions (0–3) + 2 supplementary. Round 1: 2026-07-24 (opencode, gemini-cli, OpenHarness). Round 2: 2026-07-24 (Codex CLI, Goose, Aider, OpenHands, OpenClaw, Hermes, IronClaw, n8n). Round **ext-1**: 2026-07-31 (**Grok Build**, **Pi**). Round **ext-2**: 2026-08-02 (**Kimi Code**, **QM** — the latter inaugurating the *organizational agents* category). See the [methodology](../../benchmark/README.md) (in Portuguese).

<div data-viz="benchmark-codigo"></div>

## Category: coding harnesses

| # | Dimension | opencode | gemini-cli | OpenHarness | **Codex CLI** | **Goose** | **Aider** | **OpenHands*** | **Grok Build** | **Pi** | **Kimi Code** |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Loop | 3 | 3 | 2 | 3 | 3 | 2 | 2 | 3 | 3 | 3 |
| 2 | Context | 3 | 3 | 2 | 3 | 3 | **3** | 3 | 3 | 3 | 3 |
| 3 | Compaction | 3 | 3 | 3 | 3 | 3 | 2 | 2 | 3 | **3⭐** | 3 |
| 4 | Tools | 2 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 3 | 3 |
| 5 | MCP | 3 | 3 | 2 | 3 | 3 | **0** | 3 | 3 | **0** | 2 |
| 6 | Permissions/sandbox | 2 | 3 | 2 | **3⭐** | 2 | 2 | 3 | **3⭐** | 1 | 2 |
| 7 | Memory/state | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 2 |
| 8 | Planning | 2 | 3 | 2 | 2 | 2 | 2 | 1 | 3 | 1 | 3 |
| 9 | Subagents | 2 | 3 | 3 | 3 | 3 | 2 | 2 | **3⭐** | 1 | 3 |
| 10 | Verification/evals | 2 | 3 | 2 | 3 | 3 | 3 | 0* | 2 | 3 | 2 |
| 11 | Extensibility | 3 | 3 | 3 | 3 | 3 | 3 | 3 | **3⭐** | **3⭐** | 3 |
| 12 | Interfaces | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | **3⭐** |
| | **Total** | **31** | **36** | **29** | **35** | **34** | **28** | **27*** | **35** | **26** | **32** |

\* OpenHands: the repo evaluated is the control-plane (Agent Canvas); the core (loop, condenser, SWE-bench evals) migrated to `software-agent-sdk` — the total underestimates the full project. The SDK joins the queue.

**Reading of round ext-1 (2026-07-31):**
1. **The two extremes of the spectrum arrived together.** Grok Build (35) ties with Codex CLI, covering everything with industrial depth — including reading its competitors' artifacts (AGENTS/CLAUDE/Cursor/`.mcp.json`) and porting codex's and opencode's tools. Pi (26) scores 3 on **everything it accepts** and 0–1 on everything it refuses by manifesto — the jagged profile is not immaturity, it is a thesis ("adapt pi to your workflows, not the other way around"), and every exclusion exists as a tested example extension.
2. **Dimension 6 keeps separating product from project** — and Grok Build raises the bar: shell authorization by **AST** (tree-sitter-bash), closing the `mv secret x && cat x` bypass, kernel-enforced fail-closed sandbox. Pi is the deliberate counterexample (1): it outsources the boundary to the OS and argues that in-process sandboxing is theater.
3. **Behavioral evals are still the most common gap** — Grok Build has 26k mechanism tests and zero competence tests (score 10 = 2); Pi, going the other way, is the only one in the round with an A/B bench for harness configurations (`evalHarnessTable`) and eval artifacts in the native session format.

**Reading of round ext-2 (2026-08-02):**
1. **The second verticalized vendor confirms the pattern — and the divergence.** Kimi Code (32) repeats Grok Build's move (own model → own harness, open), but with the opposite bet: where xAI went for the maximal platform in Rust with a kernel-enforced sandbox, Moonshot went for **structured autonomy** — a goal mode with a state machine and budgets (turns/tokens/time), a swarm of up to 128 subagents, cron exposed to the model — on top of weak enforcement (no OS sandbox; bash authorized by string glob in the production engine, with the AST parser ready but only consumed in the experimental v2). The detail nobody else has: **harness↔API co-design** — the Kimi API gained the `dynamically_loaded_tools` capability to serve the harness's *progressive tool disclosure*, with documented degradation for other providers. The vendor changed the model to serve the harness.
2. **Cross-pollination inside the corpus became routine**: Kimi Code's TUI is a vendored fork of `pi-tui` (acknowledged in the README); QM brings Pi, OpenCode, Codex and Claude Code as pluggable *engines*. The corpus stopped being a list of competitors and became a supply chain.
3. **Behavioral evals remain the divider** in ext-2 as well: Kimi Code has 1,137 mechanism test files and zero competence evals; QM, going the other way, runs **multiplayer E2E against real Slack with an LLM judge** — the most complete implementation of dimension 10 outside gemini-cli.

## Category: organizational agents *(new in ext-2)*

| # | Dimension | **QM** |
|---|---|:---:|
| 1 | Loop | 3 |
| 2 | Context | **3⭐** |
| 3 | Compaction | 3 |
| 4 | Tools | 3 |
| 5 | MCP | 1 |
| 6 | Permissions/sandbox | 3 |
| 7 | Memory/state | 3 |
| 8 | Planning | 1 |
| 9 | Subagents | 2 |
| 10 | Verification/evals | **3⭐** |
| 11 | Extensibility | 3 |
| 12 | Interfaces | 3 |
| | **Total (1–12)** | **31** |
| 13 | **Learning** (suppl.) | 2 |
| 14 | **Proactivity** (suppl.) | **3⭐** |

QM (Y Combinator) inaugurates the category: the first harness in the corpus whose unit of design is the **organization**, not one user's session — scopes (person/team/room/org), context filtered by the *entitlement* of everyone present in the conversation (`context-filter.ts`), recipient consent for autonomous deliveries, and auditing as core primitives. The agent loop is a **swappable dependency** (Pi, OpenCode, Codex or Claude Code by configuration), with the session portable across engines via a re-seedable "tape". It is the loop-commoditization thesis written in `package.json` — and the reason the category is new: on the classic dimensions it scores like a mature harness (31/36), but what defines it does not fit them.

## Category: self-hosted personal agents

| # | Dimension | **OpenClaw** | **Hermes** | **IronClaw** | **ohmo¹** |
|---|---|:---:|:---:|:---:|:---:|
| 1–5 | Loop/Context/Compact./Tools/MCP | 3,3,3,3,3 | 3,3,3,3,3 | 3,3,3,3,3 | 3,3,3,3,3 |
| 6 | Permissions/sandbox | 3 | 3 | **3⭐⭐** | 2 |
| 7 | Memory/state | 3 | 3 | 3 | 3 |
| 8 | Planning | 3 | 2 | 2 | 2 |
| 9 | Subagents | 3 | 3 | 2² | 3 |
| 10 | Verification/evals | 3 | 3 | 3 | 3 |
| 11 | Extensibility | 3 | 3 | 3 | 3 |
| 12 | Interfaces | 3 | 3 | 3 | 3 |
| | **Total (1–12)** | **36** | **35** | **34** | **34** |
| 13 | **Learning** (suppl.) | 1 | **3⭐⭐** | 2 | 2 |
| 14 | **Proactivity** (suppl.) | 3 | 2 | 3 | 3 |

¹ dedicated evaluation (2026-07-24) of OpenHarness's personal app — gap concentrated in dim. 6 (the gateway's permission/sandbox config is dead code; no dial between deny-all and full_auto). ² a score-3 design, but `spawn_subagent` is disabled in production.

## Category: embedded harnesses

| n8n (AI Agent node) | Total 1–12: **29/36** | Strong: tools 3 (`$fromAI`→Zod over 400+ integrations), MCP 3 (client+server), memory 3, subagents 3, interfaces 3 · Weak **by design of the environment**: compaction 1, planning 1, context 2, permissions 2 (structural/topological) |
|---|---|---|

## Category: harness frameworks (round frameworks-1, FRAMEWORK_EVAL template)

| Axis | **LangGraph** | **OpenAI Agents SDK** | **CrewAI** | **software-agent-sdk** |
|---|:---:|:---:|:---:|:---:|
| A1 Loop/orchestration | 3 | 3 | 3 | 3 |
| A2 State/durability | **3⭐⭐** | 3 | 3 | 3 |
| A3 Tools/schemas | 2 | 3 | 3 | 3 |
| A4 Multi-agent | 2 | 3 | 3 | 3 |
| A5 Human-in-the-loop | 3 | **3⭐** | 3 | 3 |
| A6 Streaming/events | 3 | 3 | 3 | 3 |
| **Total A (0–18)** | **16** | **18** | **18** | **18** |
| D1 Observability | 2 | 2 | 2 | 2 |
| D2 Tests/evals | 3 | 3 | 3 | 3 |
| D3 Ergonomics | 2 | 3 | 3 | 3 |
| D4 Ecosystem | 3 | 3 | 3 | 3 |
| **Total D (0–12)** | **10** | **11** | **11** | **11** |

**Reading of round frameworks-1:**
1. **The primitives have become a commodity** (A is almost all 3s) — the real differentiation lives in axes B (boundaries) and C (protocols), which are descriptive: LangGraph imposes BSP and leaves context/permissions completely open; the Agents SDK imposes the Responses vocabulary; CrewAI imposes the role/task ontology; the OpenHands SDK imposes the entire event model.
2. **No framework has first-class open observability** (D1=2 across the board): each gravitates to its own platform (LangSmith, OpenAI, AMP, Laminar) — the "OTel for agents" space remains vacant.
3. **Protocols split the field**: CrewAI (mandatory MCP + **A2A client/server** + skills + auto-generated AGENTS.md) and software-agent-sdk (MCP OAuth + **ACP** + agentskills) are the polyglots; the Agents SDK speaks only MCP; **LangGraph speaks zero** — protocols are a feature of the paid server.
4. **The "two movements" prediction was confirmed in the code**: software-agent-sdk is the most advanced harness-turning-into-framework (everything became a pluggable ABC, and its `ACPAgent` orchestrates Claude Code/Gemini/Codex as engines); LangGraph makes the opposite move — **hollowing itself out** of the agent layer (create_react_agent deprecated toward the langchain package) to be just a durable runtime.
5. **Compaction remains the harness/framework dividing line**: only software-agent-sdk ships it ready-made (condenser with tombstones — the best measured in the entire benchmark); LangGraph/Agents SDK/CrewAI leave the context window to the user (the Agents SDK has only a compaction session; CrewAI nothing).

## Executive summary of round 2

**The hypotheses recorded in round 1 were confronted — 3 confirmed, 1 surprise:**

1. ✅ **Codex CLI = the new ceiling in containment** (35/36): Seatbelt + bubblewrap/seccomp + Landlock + Starlark execpolicy + network-proxy — three independent layers. gemini-cli is no longer the only "reference 3" on dimension 6.
2. ✅ **Goose = MCP-native confirmed** (34/36): even the internal tools are real MCP servers served in-process. The technical tie between Codex/Goose/gemini-cli at the top of the coding category indicates the product frontier is converging.
3. ✅ **Aider = the alternative path on context** (28/36): repo-map (tree-sitter + PageRank) is the reference in context delivery without an agent loop — and the benchmark's first **0** (MCP) shows the cost of the philosophy.
4. ⚠️ **OpenHands = methodological surprise** (27/36*): the repo became a control-plane; the core lives in an external SDK. Lesson: the unit of evaluation must track how projects decompose.

**The personal agents category debuted at an unexpectedly high level**: OpenClaw (36) is the "gemini-cli of the category"; Hermes (35) brings the only closed-loop implementation of **self-evolving learning** (dimension 13 promoted to template supplementary because of it); IronClaw (34) redefines the conceptual ceiling for security — a loop structurally incapable of acting without the kernel (a trust class unforgeable by types, approvals as per-invocation leases, fail-closed WASM) — something **no coding harness evaluated has**.

**The embedded harness confirmed the category's thesis**: n8n's weak dimensions are exactly the ones the workflow engine dispenses with (short executions → no compaction; the plan is the drawn graph; permission is topology). And V3 revealed a move opposite to what was expected: n8n is *re-internalizing* the execution loop from LangChain into its own engine.

## Champions by dimension (overall, rounds 1+2)

| Dimension | Current reference | Mention |
|---|---|---|
| Loop | IronClaw (loop ≠ security perimeter) | opencode (durability), gemini-cli (next-speaker) |
| Context | Aider (repo-map) and opencode (epochs) | Codex (server-driven by model), Hermes (3 cache-aware layers) |
| Compaction | Codex (remote v2) and Goose (3 techniques) | IronClaw (effectiveness circuit-breaker) |
| Tools | Goose (MCP-uniform) and IronClaw (typed capabilities) | n8n (`$fromAI`), Aider (edit formats driven by eval) |
| MCP | Codex and OpenClaw (full client+server) | Goose (in-process) |
| **Permissions/sandbox** | **IronClaw** (authority kernel) | Codex (3 OS layers), OpenClaw (pairing) |
| Memory | Hermes (multi-layer + FTS5) | gemini-cli (git checkpoint), OpenClaw (Dreaming) |
| Planning | gemini-cli and OpenClaw (goals/task flow) | — the weakest dimension across the entire industry |
| Subagents | OpenClaw (push-based + third-party ACP) | Codex (graph store), OpenHarness (swarm) |
| Verification | gemini-cli (4 suites) and IronClaw (cross-tenant isolation) | Aider (benchmark driving design), Goose (leaderboard) |
| Extensibility | broad tie — it became a commodity | OpenClaw (ClawHub w/ scan), Goose (JSON providers) |
| Interfaces | OpenClaw (23 channels + voice + apps) | Codex (1 core → CLI/IDE/desktop/cloud) |
| **Learning (13)** | **Hermes** (autonomous) and **gemini-cli** (human inbox) — two level-3 designs | IronClaw (automatic extraction) |
| **Proactivity (14)** | OpenClaw (heartbeat w/ lightweight context) | IronClaw (routines engine) |

## Cross-cutting findings from round 2

1. **Planning is the industry's weakest dimension**: no new harness reached 3; the overall average of dimension 8 is the lowest in the benchmark. Everyone has a todo-list; almost no one has an enforced plan→approve→execute.
2. **MCP client+server became the standard among the mature**: Codex, OpenClaw, Hermes, OpenHands, n8n and IronClaw expose themselves as servers — in round 1, none of the three did this in core. The harness as a *consumable service* consolidated within months.
3. **ACP emerged as the harness-orchestration protocol**: OpenClaw, OpenHands and Goose orchestrate/integrate other harnesses (Claude Code, Codex, Gemini CLI, opencode) via ACP — ch. 14's prediction about "agent-as-a-service" was confirmed through a different route.
4. **The expiration clause gained an inverted case**: Hermes's learning loop does not wait for the model to improve — the model+harness pair writes its own scaffolding (skills). Self-expansion instead of expiration.
5. **Security now has two distinct paradigms**: containment by the OS (Codex — the process *cannot*) and authority architecture (IronClaw — the loop *cannot reach*). They are complementary, and no harness combines both yet.

## Recorded next steps

- **Retroactive re-evaluations**: dimension 13 on the round-1 harnesses (gemini-cli's `skill-extraction-agent` is a candidate for a 2); ohmo as a dedicated entry in the personal category.
- **Queue**: `OpenHands/software-agent-sdk` (the missing core), frameworks (LangGraph, CrewAI, Agents SDK — adapted template), Cline/Roo (IDE), mini-swe-agent (minimal harness), Crush, smolagents.
- **Methodological evolution**: from static to behavioral — running the harnesses on standardized tasks (Goose's Harbor and OpenClaw's Benchmark Pack are models to study).
