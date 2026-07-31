<!-- i18n fonte:livro/capitulos/15-harness-embutido.md edicao:0.61 hash:bf3517fb -->
# 15 — The Embedded Harness: agents inside workflow engines

> **State of the art captured in 2026-07** · last revised 2026-07-28 · [history and expiration log](../historico.html)
>
> Chapter derived from the evaluation of workflow engines in the benchmark; per-repository evidence in Appendix A (online supplement, updated each benchmark round).

## Learning objectives

By the end of this chapter, you should be able to:
1. **Explain** the inversion that defines the category — the workflow contains the harness, not the other way around — and why it raises the question "which dimensions of the scaffolding are essential, and which are replaceable by the environment?";
2. **Identify** which dimensions of the scaffolding the workflow environment does away with (compaction, planning, context delivery, granular permissions) and **justify** why each one becomes dispensable;
3. **Analyze** the implementation of a real agent node (n8n's AI Agent, Appendix A as the answer key) and locate where the loop, the tools and the permissions live;
4. **Evaluate** when to use an embedded harness versus a dedicated one, as a function of task duration and autonomy — and recognize the ceiling of the substitution;
5. **Apply** the category's exportable ideas to a dedicated harness: deriving tools from existing surfaces (the `$fromAI` pattern) and durable human-in-the-loop.

## The problem

In the previous chapters, the harness contains the work: the loop drives, the tools act, the workflow emerges from the model's decisions. Tools like **n8n** invert the relationship — **the workflow contains the harness**. An "agent node" is a step inside a graph designed by a human, surrounded by triggers (webhook, cron, chat), integrations and error handling that the workflow engine already provided before AI existed.

This inversion raises the question that gives the category its meaning: **which dimensions of the scaffolding are essential, and which are replaceable by the environment?**

## The state of the art

### What the environment does away with

The evaluation of the category's representative (n8n, see Appendix A) confirms the thesis with uncomfortable precision: the weak dimensions of the embedded harness are exactly the ones the environment does away with.

| Dimension dispensed | Why the environment dispenses it |
|---|---|
| Compaction | Event-triggered executions are short — context does not accumulate |
| Planning | The plan *is* the workflow graph, drawn by the human on the canvas |
| Context delivery | Context arrives mapped from previous steps via expressions |
| Granular permissions | The topology is already the allowlist |

The last point deserves emphasis: in the embedded harness, **permission is topology**. There is no per-call approval inside the loop — the LLM (Large Language Model) can only invoke what the author plugged into the canvas. It is an allowlist by construction, decided visually by a human, complemented by real human-in-the-loop: nodes that pause execution durably, awaiting approval on a channel (Slack/Outlook), instead of the CLIs' synchronous approval prompt.

And the strong dimensions are where the engine has a structural advantage: **tools** (the pre-existing integrations become a tool pool), **memory** (pluggable database backends), **interfaces** (hosted chat, webhooks, embeddable widget), **MCP (Model Context Protocol)** (client *and* server) and **subagents** (agent-as-tool and sub-workflows). No dedicated harness has a tool pool the size of a converted integration ecosystem — because none has a pre-existing ecosystem to convert.

### The borrowed loop — and the re-internalization trajectory

The embedded harness typically does not write its own loop: it borrows it from a framework (in the case observed, LangChain JS). But the trajectory measured in the benchmark points in a clear direction: the workflow engine starts by outsourcing the loop and **re-internalizes the half that matters to a workflow engine — the scheduling of execution**. The framework still decides *which* tool to call; the *execution* of the call becomes the engine's responsibility again, as it schedules the nodes and re-enters the agent. (Code detail in Appendix A, finding 1.) The implication: workflow engines tend to absorb ever more of the harness, not the other way around.

### The ceiling of the substitution

But the substitution has a ceiling: **without compaction or planning, the agent node serves short automations, not long autonomous work**. An embedded agent that had to refactor a repository for hours would collapse the context window with no defense. The two layers do not compete — they complement each other by task duration and autonomy: the dedicated harness for long, open-ended work; the embedded one for pinpoint decisions inside structured processes.

### Implications

1. **For those building a dedicated harness**: the `$fromAI` pattern (Appendix A, finding 2) shows how to derive tools from existing surfaces without writing wrappers; durable HITL (pausing execution for days awaiting approval on a channel) is superior to the CLIs' synchronous approval prompt.
2. **For those building on top of workflow engines**: the category's gaps (compaction, plan mode) are the obvious roadmap — and the loop's re-internalization trajectory suggests the engines will absorb ever more of the harness, not the other way around.
3. **For the book's taxonomy**: "how much harness is needed" is a function of the *execution environment*, not a universal constant. The benchmark's ruler measures scaffolding that is present; this category reminds us that scaffolding absent-by-design is not a gap — as long as the task class is respected.

### Executive summary

The embedded harness is not an incomplete dedicated harness: it is a category in which the execution environment replaces, by construction, half of the scaffolding's dimensions — the plan becomes a graph, permission becomes topology, context becomes mapped expressions. The substitution holds as long as the task class is respected: pinpoint decisions inside structured processes, not long autonomous work. **What to steal** today: automatic derivation of tools from existing integrations (the `$fromAI` pattern) and durable human-in-the-loop instead of synchronous approval.

> **See also**: the living collection [Awesome Harness Engineering — Production Infrastructure & Operations](https://github.com/GHDaru/awesome-harness-engineering#production-infrastructure--operations) gathers more consultable resources for this dimension, curated by problem.

## Check your understanding

1. State the inversion that defines the category and explain why it turns the benchmark's "weak dimensions" into "dimensions dispensed by the environment". (If needed, re-read "What the environment does away with".)
2. Why does permission-as-topology do away with per-call approval inside the loop — and which mechanism complements this allowlist when a human decision is genuinely needed mid-execution?
3. A team wants to use a workflow engine's agent node to refactor a repository for hours. Explain, in terms of compaction and planning, why this collapses — and what the correct division between embedded and dedicated harness would be for that task.
4. Name the two ideas from the category worth exporting to a dedicated harness and what each one replaces or improves. (Hint: tool derivation and HITL.)

---

## Appendix A — n8n (AI Agent node)

> Per-repository evidence, with paths — supplementary material (online version), expanded each benchmark round. The full n8n evaluation (29/36) is in `../../benchmark/avaliacoes/n8n.md`.

### Anatomy of the agent node (evidence: `packages/@n8n/nodes-langchain`)

n8n implements the agent as a "cluster node": a root **AI Agent** node with typed ports into which sub-nodes are plugged — model (`AiLanguageModel`), memory (`AiMemory`), tools (`AiTool`), output parser. Three code findings structure the chapter:

**1. The loop is borrowed — and is being handed back.** The V2 generation delegates everything to LangChain JS (`AgentExecutor.fromAgentAndTools`, `maxIterations` 10). But V3 changed the design: LangChain still *decides* which tool to call (`createToolCallingAgent`), yet the *execution* became the responsibility of the n8n engine — tool calls become `EngineRequest` objects returned to the engine, which schedules the nodes and re-enters the agent with `EngineResponse`. n8n started by outsourcing the loop and is **re-internalizing** the half that matters to a workflow engine: the scheduling of execution.

**2. The `$fromAI` bridge — the category's most exportable idea.** `create-node-as-tool.ts` turns **any of the 400+ integration nodes** marked `usableAsTool` into an agent tool: the parameter traversal collects `$fromAI('key', 'description', type)` expressions — the slots the LLM must fill — and generates the Zod schema automatically. No dedicated harness has a tool pool this size, because none has a pre-existing integration ecosystem to convert.

**3. Permission is topology.** There is no per-call approval inside the loop: the LLM can only invoke what the author plugged into the canvas's `AiTool` port. It is an allowlist by construction, decided visually by a human — complemented by real human-in-the-loop (`sendAndWait` nodes pause execution durably awaiting approval on Slack/Outlook, forbidden inside subagents) and a Guardrails node.

### The score (29/36) and the strength/weakness map

The evaluation's weak dimensions are the ones the environment dispenses: **compaction (1)** — event-triggered executions are short, context does not accumulate; **planning (1)** — the plan is the graph drawn on the canvas; **context delivery (2)** — context arrives mapped from previous steps via expressions; **granular permissions (2)** — the topology is already the allowlist.

And the strong ones are where the engine has a structural advantage: **tools (3)** — the integrations; **memory (3)** — pluggable database backends; **interfaces (3)** — hosted chat, webhooks, embeddable widget; **MCP (3)** — client **and** server: the `McpTrigger` exposes n8n's tools to external MCP clients; **subagents (3)** — agent-as-tool and sub-workflows.

*Cousins to evaluate in future rounds: Zapier Agents, Make, Dify, Flowise.*
