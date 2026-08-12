<!-- i18n fonte:livro/capitulos/17-protocolos.md edicao:0.82 hash:c4d7fabd -->
# 17 — The Protocol Layer: the connective tissue between harnesses

> **State of the art captured in 2026-07** · last revised 2026-08-12 · [history and expiration log](../historico.html)
>
> Didactic layer v4 — see [Editorial Guide §2.1](../editorial-guide.md).
> scaffold: completo

## Learning objectives

By the end of this chapter, you should be able to:
1. **Explain** why the protocol layer is what turns a market of silos into an ecosystem, and why each protocol standardizes a different *boundary* of the harness;
2. **Distinguish** the boundaries covered by MCP (Model Context Protocol), A2A (Agent-to-Agent), ACP (Agent Client Protocol), agentskills.io and AGENTS.md, including the two classic confusions;
3. **Analyze** the adoption matrix measured in code and locate a real harness in it;
4. **Evaluate** a protocol's health by measured adoption and governance, rather than by marketing;
5. **Decide** which protocols a new harness needs to speak in order not to be left out of other people's composition architectures.

## The best harness in the comparison, and nobody can plug it in

Suppose you evaluated six coding harnesses rigorously. You read all the code, built the ruler, gave the scores. One of them won on three technical dimensions: the edit format is the best-measured on the market, the context management is the most economical, the behavior in a large repository is the most predictable.

You adopt it. Six months later, the team is migrating to another one.

Not because it got worse. Because the architecture changed around it. The team started running the agent inside the editor, and it does not speak the protocol the editor uses. Then it started orchestrating two agents in parallel, one driving the other, and it cannot be driven. Then it standardized internal tools behind common servers, and it does not know how to consume them.

The harness is still technically excellent. It just does not **fit**.

This chapter is about the fit. Chapters 02 to 16 deal with what happens *inside* a harness; this one deals with what happens **between** them.

## The problem

Without shared protocols, every harness is a silo. Its tools, its project instructions, its subagents and its skills only work inside it.

The protocol layer is what turns that market of silos into an ecosystem. Each protocol standardizes a different boundary: agent↔tool, agent↔agent, agent↔editor, agent↔user. Added to those are the cross-cutting formats for procedural knowledge (SKILL.md) and project instructions (AGENTS.md).

The practical consequence is the one in the scene above. In a market that *composes* harnesses, not speaking the protocols is not losing a feature. It is being left out of other people's architectures.

## Industry sources

- [ecosystem map 2026](https://www.digitalapplied.com/blog/ai-agent-protocol-ecosystem-map-2026-mcp-a2a-acp-ucp)
- [Zylos: MCP/A2A/ACP convergence](https://zylos.ai/research/2026-03-26-agent-interoperability-protocols-mcp-a2a-acp-convergence/)
- [Zuplo: where ACP ended up](https://zuplo.com/blog/agent-protocol-stack-mcp-a2a-acp-2026)
- [Agent Skills: format and adoption](https://atlan.com/know/ai-agent/ai-agent-skills/what-are-agent-skills/)
- [AGENTS.md guide 2026](https://codersera.com/blog/agents-md-complete-guide-2026/)
- [Zed ACP](https://tessl.io/blog/zed-debuts-agent-client-protocol-to-connect-ai-coding-agents-to-any-editor/)
- **See also**: the living collection [Awesome Harness Engineering — Skills & MCP](https://github.com/GHDaru/awesome-harness-engineering#skills--mcp) gathers more resources for this dimension, curated by problem.

The adoption matrix in the next section is the benchmark's own evidence (`benchmark/avaliacoes/`).

## In practice: a protocol is this, in bytes

"Protocol" sounds abstract until you see the traffic. It is worth looking at two different boundaries side by side, because the difference between them becomes obvious in the shape of the messages.

**Vertical boundary, MCP.** The agent wants a tool that is not its own. First it asks what exists:

```jsonc
// agent → MCP server
{"jsonrpc":"2.0","id":1,"method":"tools/list"}

// server → agent
{"jsonrpc":"2.0","id":1,"result":{"tools":[
  {"name":"fetch_ticket",
   "description":"Fetches a support ticket by id",
   "inputSchema":{"type":"object","properties":{"id":{"type":"string"}},
                  "required":["id"]}}
]}}
```

And then it uses it:

```jsonc
// agent → MCP server
{"jsonrpc":"2.0","id":2,"method":"tools/call",
 "params":{"name":"fetch_ticket","arguments":{"id":"T-4471"}}}

// server → agent
{"jsonrpc":"2.0","id":2,"result":{"content":[
  {"type":"text","text":"T-4471: login fails after password change. Open."}
]}}
```

Notice what the protocol standardizes: **discovery** (`tools/list`) and **the call** (`tools/call`), with the schema coming from the server. It is exactly the contract of chapter 05, now crossing a process boundary. The agent does not need to know who implements `fetch_ticket`, and the server does not need to know which model is on the other side.

**Composition boundary, ACP.** Here it is not the agent asking for a tool. It is a **client driving an entire agent**:

```jsonc
// client (editor, or another harness) → agent
{"jsonrpc":"2.0","id":7,"method":"session/prompt",
 "params":{"sessionId":"s-19","prompt":[
   {"type":"text","text":"the test_login test is failing, fix it"}]}}

// agent → client, streaming, while it works
{"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"s-19",
 "update":{"sessionUpdate":"tool_call","title":"pytest test_login",
           "status":"in_progress"}}}

{"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"s-19",
 "update":{"sessionUpdate":"tool_call_update","status":"completed"}}}

// and when it finishes
{"jsonrpc":"2.0","id":7,"result":{"stopReason":"end_turn"}}
```

The two exchanges use the same transport, JSON-RPC, and solve problems of opposite natures.

In MCP, the agent commands and the tool obeys. In ACP, the client commands and **the agent obeys**. Note the `stopReason` on the last line: it is the typed termination label from chapter 02, now exposed at the boundary, because whoever is driving needs to know *why* the turn ended.

And note the `session/update`. The protocol does not return only the result, it returns the **progress**. An agent that can only answer at the end cannot be driven by an editor, because the editor needs to show something while it waits. That observability requirement is the reason ACP spread among harnesses and not only among editors: whoever orchestrates another agent has the same problem as whoever displays it.

## The state of the art

### The map: one protocol per boundary

| Protocol | Boundary | Origin / governance | Status (2026) |
|---|---|---|---|
| **MCP** (Model Context Protocol) | agent ↔ **tools/data** | Anthropic → universal adoption (OpenAI, Google, Microsoft) | mature; ~97M downloads |
| **A2A** (Agent-to-Agent) | agent ↔ **agent** (cross-organization delegation) | Google → **Linux Foundation** (v1.0 in 2026) | consolidating; absorbed IBM's ACP (Agent Communication Protocol) |
| **ACP** (Agent Client Protocol) | agent ↔ **editor/client** | Zed | rapid adoption among coding harnesses |
| **agentskills.io** (Agent Skills / SKILL.md) | portable **procedural knowledge** | Anthropic (open spec, Dec/2025) | ~40 compatible products in 6 months |
| **AGENTS.md** | portable **project instructions** | community → **Agentic AI Foundation** (Linux Foundation) | 60,000+ repositories; 20+ tools read it natively |
| AG-UI | agent ↔ **user interface** | community (CopilotKit) | emerging |
| ACP-IBM (Agent Communication Protocol) | agent ↔ agent | IBM | **discontinued**, merged into A2A (Aug/2025) |

Two confusions to clear up, and both cost newcomers time.

The first: **"ACP" names two distinct protocols**. IBM's covered agent-to-agent communication and was discontinued in favor of A2A. Zed's covers agent-to-editor, is alive and expanding. In this book, ACP means Zed's.

The second: **MCP and A2A do not compete**. MCP is the vertical connection, from agent to tool. A2A is the horizontal one, from agent to peer agent. A real system uses both, as the stack below makes visible.

### The adoption matrix, measured in code and not in marketing

This chapter's differentiator is crossing the protocols with the **11 harness evaluations of the benchmark**, plus the 4 frameworks from the frameworks-1 round, with per-file evidence in `benchmark/avaliacoes/`. No external comparison has this column of truth.

| Harness | MCP client | MCP server | ACP | A2A | SKILL.md / agentskills | AGENTS.md (or equiv.) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| opencode | ✅ | — | ✅ (Zed) | — | partial | ✅ AGENTS.md |
| gemini-cli | ✅ | — | ✅ | ✅ **client+server** | ✅ | GEMINI.md |
| OpenHarness | ✅ | — | — | — | ✅ (Claude format) | CLAUDE.md |
| Codex CLI | ✅ | ✅ | — | — | ✅ | ✅ AGENTS.md |
| Goose | ✅ | ✅ (`goose mcp`) | ✅ (whole desktop) | — | ✅ | ✅ AGENTS.md + .goosehints |
| Aider | ❌ | ❌ | — | — | — | ✅ (reads it) |
| OpenHands | ✅ | ✅ (FastMCP) | ✅ (profiles) | — | ✅ (org repos) | microagents |
| OpenClaw | ✅ | ✅ | ✅ (orchestrates third parties) | — | ✅ (52 bundled) | ✅ AGENTS.md + SOUL.md |
| Hermes | ✅ | ✅ | ✅ | — | ✅ (core of learning) | ✅ AGENTS.md + SOUL.md |
| IronClaw | ✅ | — | — | — | ✅ (OpenClaw compat) | identity files |
| n8n | ✅ | ✅ (Trigger) | — | — | — | — |
| *frameworks:* | | | | | | |
| LangGraph | ❌ | ❌ (paid server only) | ❌ | ❌ | ❌ | — |
| OpenAI Agents SDK (Software Development Kit) | ✅ | — | ❌ | — | partial | sandbox agents only |
| CrewAI | ✅ (mandatory) | — | ✅ **client+server** | — | ✅ | ✅ **auto-generated** |
| software-agent-sdk | ✅ (OAuth) | — | ❌ | ✅ (uses harnesses as engine) | ✅ (spec) | ✅ |

**MCP won in practice.** Ten out of eleven speak it, and the only exception is a declared philosophical choice. Between rounds 1 and 2 the pattern migrated from "client" to "client and server": the harness stopped merely consuming tools and became, itself, a consumable service.

**agentskills.io is the fastest standardization we have measured.** A spec from December 2025, eight of our eleven compatible by July 2026. The prediction in ch. 12, that "an MCP of extensibility is forming", came true. And with a structural detail worth retaining: skills are portable markdown, so the same skill runs in different harnesses. The self-improving learning of ch. 16 writes in *that* format, which makes knowledge learned by one agent transferable to another, in principle.

**ACP is the most important silent protocol of the cohort.** Six out of eleven speak it, and three of them (OpenClaw, OpenHands, Goose) use it to **orchestrate other harnesses** as subagents, making Claude Code, Codex, Gemini CLI and opencode interchangeable parts. What was born as "agent↔editor" became, in practice, the composition bus between harnesses. It was the `session/update` from the example above that made this possible.

**A2A left the one-vendor bet behind**, updated in the frameworks-1 round. gemini-cli used to be the only harness to implement it, and **CrewAI** came in with native client and server (full AgentCard, JWS, gRPC/REST), the second measured implementer and the first framework. Governance at the Linux Foundation and the absorption of ACP-IBM keep pointing to A2A as the candidate for the inter-organizational boundary. In product harnesses, however, that boundary still barely exists.

**AGENTS.md consolidated as the neutral standard.** The AGENTS/CLAUDE/GEMINI.md fragmentation described in ch. 03 is resolving: Codex, Goose, opencode, OpenClaw and Hermes converged on AGENTS.md, now under the Agentic AI Foundation, with the proprietary files becoming aliases.

### The stack: how the protocols compose

A complete agentic system in 2026 uses the whole stack, one layer per boundary:

```
[user]
   │  AG-UI / chat channels / TUI            (interface)
[harness A]
   │  ACP                                     (composition: A drives B as a subagent)
[harness B]
   │  A2A                                     (delegation to another org's agent)
[remote agent]
   │  MCP                                     (each agent reaches its own tools)
[tools/data]

cross-cutting: AGENTS.md (per-project instructions) · SKILL.md (portable procedures)
```

### Implications for harness engineering

**Protocol is a survival dimension, not a feature dimension.** Aider is a technical reference on three dimensions and is out of the entire composition ecosystem for speaking neither MCP nor ACP. It is the scene that opened this chapter, with a name.

**The expiration clause does not apply here.** Protocols are a boundary with the world, not a prosthesis for a model limitation. They are the scaffolding that *remains* when models improve, which is why investing in protocol is the harness investment with the longest half-life (ch. 14).

**For the benchmark**, the matrix above becomes a permanent section of the comparison, updated each round. Protocols do not get 0–3 scores like harnesses. They are evaluated by **measured adoption**, which is the matrix, and by **governance health**, where a neutral foundation counts for more than a single vendor.

**Addendum (2026-07-31).** The MCP **2026-07-28** spec ([announcement](https://blog.modelcontextprotocol.io/posts/2026-07-28/)) reinforces this chapter's thesis from another angle. A stateless core, an extensions framework and the **first formal deprecation policy**, of 12 months, are the typical behavior of a protocol leaving adolescence and entering the infrastructure phase: disciplined versioning starts to matter more than new features. The cohort's adoption of the new version enters the matrix next round.

On the same day, on the other boundary (spec 065): the [A2A specification](https://a2a-protocol.org/latest/specification/) confirms **v1.0 stable under the Linux Foundation**, organized in three layers — data model in Protobuf/JSON Schema, abstract operations and JSON-RPC/gRPC/REST bindings — with **v1.0.1 already bringing a formal extension mechanism**. The two boundary winners reached, in the same quarter, the same stage: formal extensions instead of features in the core.

### Executive summary

The protocol layer already has one winner per boundary. MCP on the vertical, agent to tool, with near-total adoption. ACP as the composition bus between harnesses. agentskills.io as the portable format for procedural knowledge. AGENTS.md as the neutral standard for project instructions. A2A remains the consolidating bet for the inter-organizational boundary, sustained more by governance (Linux Foundation, absorption of ACP-IBM) than by measured adoption in product harnesses.

The engineering decision is asymmetric: protocols are the harness component with the longest half-life, immune to the expiration clause, and the adoption matrix, not marketing, is the instrument for re-evaluating them each round.

**What to steal:**

- **Expose the termination label at the boundary**, like ACP's `stopReason`. Whoever drives your agent needs to know why it stopped.
- **Emit progress as a stream** (`session/update`), not only a final result. That is what makes an agent drivable.
- **Let the server declare the tool schema** (`tools/list`), instead of baking it into the client.
- **Prefer the cross-cutting markdown format** (AGENTS.md, SKILL.md) to the proprietary file, because it is what travels across harnesses.

## Check your understanding

1. A colleague claims that "A2A will replace MCP". Why does the claim confuse the boundaries, and how does the stack show that a real system uses both?
2. "ACP" appears twice in the protocol table, with opposite statuses, "rapid adoption" and "discontinued". Explain the difference between the two protocols and say which of them this book calls ACP.
3. You are designing a new harness. Which protocols are mandatory today, which one is still a bet, and what does the Aider exception teach about the cost of speaking none?
4. Why does the expiration clause (ch. 14) not apply to the protocol layer, when it applies to almost everything else in the harness?
5. Looking at the two message exchanges in the "In practice" section: which one would you implement first in a new harness, and why?

---

## Verification answers

**1.** Because the two solve different boundaries, and substitution only makes sense between things that solve the same one. MCP is vertical: the agent reaches tools and data, and the tool obeys. A2A is horizontal: one agent delegates to another agent, typically in another organization, and both sides are peers. In the stack, a remote agent reached over A2A uses **its own** MCP to reach its tools. Both appear in the same stack, at distinct layers, and neither takes the other's place.

**2.** IBM's ACP (Agent Communication Protocol) covered agent-to-agent communication and was **discontinued in August 2025**, with its capabilities absorbed by A2A. Zed's ACP (Agent Client Protocol) covers agent-to-client, that is, an editor or another harness driving an agent, and is in rapid adoption: six of the eleven measured harnesses speak it. In this book, **ACP always means Zed's**, and the table keeps the other one labeled `ACP-IBM` precisely so the acronym does not mislead.

**3.** Mandatory today: **MCP as a client**, to reach third-party tools, and increasingly **MCP as a server**, so that your harness is consumable by others. Then **ACP**, if you want your agent to run inside editors or be orchestrated by another harness. And **AGENTS.md**, which is cheap and already a neutral standard under a foundation. Still a bet: **A2A**, whose inter-organizational boundary barely exists in product harnesses, although its governance is the most solid of the set. The Aider lesson is the harshest in the chapter: technical excellence on internal dimensions **does not compensate** for the absence of protocol, because the cost does not show up as a missing feature, it shows up as absence from the architectures other people build.

**4.** Because the expiration clause applies to components that exist **to make up for a model limitation**, and disappear when the limitation does: compaction exists because the window is finite, plan mode exists because the model acts rashly. A protocol does not make up for a model limitation. It solves the **boundary between distinct systems**, which keeps existing regardless of how good the model gets. Two separate processes will need a contract even if both are perfect, and that is why protocol is the harness investment with the longest half-life.

**5.** The defensible answer is **MCP as a client**, and the reason is asymmetric return: with few lines your harness gains access to a whole ecosystem of tools you did not write, and the measured adoption (ten out of eleven) guarantees the investment will not be orphaned. ACP comes next, and depends on ambition: it requires your agent to know how to **report progress as a stream**, which usually forces refactoring in the loop rather than just adding an adapter. If your answer was ACP because you want to be orchestrated from the start, it also holds up — provided you noticed that the real cost is in `session/update`, not in the transport.
