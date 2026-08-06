<!-- i18n fonte:livro/apendice-supply-chain.md edicao:0.71 hash:131c8808 -->
# Appendix — The harness supply chain

> Map captured on **2026-08-02** (rounds ext-2/ext-3). Like every state of the art in this book, it expires: check it against the [History](../historico.html).

When this study began, the corpus was a list of **competitors**: alternative products solving the same problem. Rounds ext-2 and ext-3 revealed something else: the harnesses became **suppliers to one another** — `package.json` dependencies, vendored forks, subprocesses, resumed foreign sessions. This appendix shows the work: who consumes whom, through which mechanism, with the evidence for each link. "Supply chain" here is the manufacturing image (factory A makes the part factory B assembles), and also the security sense of the term: **whoever embeds, inherits the risks**.

## The map (evidence per link)

Each row is a link verified by code reading at the frozen commit of the corresponding evaluation (paths relative to each repo's root).

| Consumer | Supplier | What it consumes | Mechanism | Evidence |
|---|---|---|---|---|
| **QM** | **Pi** | the **default** agent engine — with the consumer's **own security patch** applied | npm dependency on a repackaged fork (`qm-pi-coding-agent-0.82.0-security.2`) | `package.json:58` |
| **QM** | Claude Code | alternative engine | `@anthropic-ai/claude-agent-sdk` + in-process MCP server bridging tools | `package.json:50`; `src/harness/claude-harness.ts` |
| **QM** | Codex CLI | alternative engine | `@openai/codex` dependency | `package.json:60` |
| **QM** | opencode | alternative engine | `opencode-ai` + plugin/SDK | `package.json:61-62,72` |
| **Kimi Code** | **Pi** | the entire TUI | **vendored** fork of `pi-tui`, with a public acknowledgment | `packages/pi-tui/`; `README.md:122` |
| **software-agent-sdk** | Codex CLI, gemini-cli | whole harnesses as executors | **ACP** subprocesses orchestrated by `ACPAgent` | `openhands/agent_server/conversation_service.py:723`; `event_service.py:873` |
| **Grok Build** | Claude Code, Codex, Cursor | the competitors' **sessions** (resumable) and their context artifacts (AGENTS.md/CLAUDE.md/`.cursor`) | reading native formats + session picker | `crates/codegen/xai-grok-pager/src/views/session_picker.rs` |
| **n8n** | LangChain | the AI Agent node's foundation — currently being **re-internalized** (V3) | `@langchain/*` dependencies | `packages/@n8n/nodes-langchain/package.json` |
| **Pi** | ← third parties | the xAI provider reaches Pi **from outside**, via a community package | extension mechanism (`pi-xai-oauth`) | radar 2026-08-01 |
| **Traycer** | Claude Code | GUI+TUI engine: resume/fork, lifecycle hooks, remote management of its MCP/plugins/skills | SDK + PTY `claude --resume --fork-session` + hooks → `traycer` CLI | `protocol/src/host/agent/tui/unary-schemas.ts:48-80`; `clients/traycer-cli/src/commands/agent-activity-from-hook.ts` |
| **Traycer** | Codex CLI | GUI+TUI engine | `codex app-server` (JSON-RPC) + PTY `codex resume` | `protocol/src/host/agent/tui/unary-schemas.ts:70-80` |
| **Traycer** | opencode | engine **and substrate of its own inference** (per-user OpenCode server behind the Traycer backend) | PTY + server spawn with an account header | `protocol/src/common/schemas.ts:70-76`; `agent-runtime.ts:839-849` |
| **Traycer** | **Pi** (and the Oh My Pi fork) | GUI engines — the fork *alone* motivated protocol version v6.0 | Pi's native RPC | `agent-runtime.ts:925-946`; `provider-schemas.ts:80-135` |
| **Prime Agent** | **Pi** | **the entire base** — Pi's four packages, with the tool set collapsed into a single `ipython` and two new layers on top | thesis fork; LICENSE with dual copyright (Mario Zechner + Prime Intellect) | `LICENSE`; `packages/{agent,ai,coding-agent,tui}/package.json`; `README.md` |
| **Traycer** | **Hermes**, **Kimi Code**, Cursor, +ACP | GUI engines (8+ providers via ACP: `hermes acp`, `kimi acp`, `grok agent stdio`, `qwen --acp`…) | ACP stdio processes / `@cursor/sdk` | `agent-runtime.ts:851-941`; `protocol/src/host/agent/shared.ts:35-43` |

Add the **editorial production** links: Traycer materializes skills from public registries (anthropics/skills, vercel-labs) pinned by hash in a lockfile (`skills-lock.json`) for the agents that write its own repo — harness consumption starting before the product even exists.

## The extreme case: Traycer, the cockpit that is all chain

Round **ext-3** evaluated [Traycer](../avaliacao-traycer.html) (18/36) — a product whose *entire* proposition is consuming other harnesses: a multiplayer cockpit (~513k open lines) that catalogs, in its own wire contract, the resume/fork semantics of **18 competing CLIs/SDKs**, with 6 provider enums frozen per protocol version. It **did not pass the inclusion test** of ch. 01 §4 — the four harness pieces are not in the open code: the Host that runs loop, context and control is a signed closed binary with a mandatory cloud (the repo's own `AGENTS.md` says so; full evidence in the evaluation). The record stays for two reasons: it is the corpus's best-documented case of **"open source" as a client-distribution strategy**, and it is proof that the orchestration layer — buying, driving and reselling the work of other harnesses — became a standalone product.

## Three readings

1. **"What is it made of?" became an evaluation question.** A harness is no longer described only by what it does, but by the links it embeds. Pi today feeds **at least five systems** (QM as engine, Kimi Code as TUI, Traycer as provider, the Oh My Pi fork — and Prime Agent as its entire base); a failure, a CVE or a license change in that single link propagates through the whole chain, exactly as in physical industry.
2. **The session became an integration interface.** Three different consumers (Grok Build, Traycer, QM) treat other harnesses' *sessions* as resumable artifacts — via native formats, versioned resume/fork anchors, or "tape" re-seeding. It is an emerging pattern with no standard: each one solves it by reverse-engineering the neighbor. If a session-interchange format ever standardizes (ch. 17), much of this map becomes compatibility code — the expiration clause applied to this very appendix.
3. **Enforcement does not travel down the chain.** When QM runs Pi, the permissions are QM's (Pi has none); when Traycer drives 18 harnesses, the permission mode is a **relay** — and Traycer's A2A instruction even tells derived agents to operate in `full_access` by default. Whoever consumes a harness inherits its capabilities, but does **not** automatically inherit its controls — the weakest link in the chain sets the risk for the whole.

## The counterpoint that confirms it

The two most-consumed suppliers on the map are also the ones that take the *classic* supply chain most seriously: Pi pins dependencies and allowlists lifecycle scripts (`--ignore-scripts` everywhere); QM audits its supplier to the point of **patching it** (the security patch on line 58). The lesson closes the circle of ch. 07: in the era when your neighbor's harness is your dependency, supply-chain security stopped being an npm topic and became a topic of **agent architecture**.

---

> **See also**: the full evaluations of each link are in the [Appendix — The study](appendix-study.md); the editorial reading of the trend is in the [Comparison](comparative.md) (round ext-2) and in chapter [14 — Convergences](14-convergences.md).
