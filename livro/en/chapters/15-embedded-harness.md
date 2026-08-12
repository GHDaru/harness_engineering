<!-- i18n fonte:livro/capitulos/15-harness-embutido.md edicao:0.85 hash:71cd01dc -->
# 15. The Embedded Harness: agents inside workflow engines

> **State of the art captured in 2026-07** · last revised 2026-08-12 · [history and expiration log](../historico.html)
>
> Didactic layer v4, see [Editorial Guide §2.1](../editorial-guide.md).
> scaffold: proprio
>
> Chapter derived from the evaluation of workflow engines in the benchmark; per-repository evidence in Appendix A (online supplement, updated each benchmark round).

## Learning objectives

By the end of this chapter, you should be able to:
1. **Explain** the inversion that defines the category (the workflow contains the harness, not the other way around) and why it raises the question "which dimensions of the scaffolding are essential. And which are replaceable by the environment?";
2. **Identify** which dimensions of the scaffolding the workflow environment does away with (compaction, planning, context delivery, granular permissions) and **justify** why each one becomes dispensable;
3. **Analyze** the implementation of a real agent node (n8n's AI Agent, Appendix A as the answer key) and locate where the loop, the tools and the permissions live;
4. **Evaluate** when to use an embedded harness versus a dedicated one, as a function of task duration and autonomy, and recognize the ceiling of the substitution;
5. **Apply** the category's exportable ideas to a dedicated harness: deriving tools from existing surfaces (the `$fromAI` pattern) and durable human-in-the-loop.

## Four minutes, and none of it was solved

Someone drags an agent node into a workflow. Wires one end to Postgres, the other to Slack, writes three lines of instructions and publishes.

Four minutes. It is in production, answering customers.

Notice what that person did **not** do. No context assembler, no permission policy, no memory, no thought about compaction. Eleven chapters of this book did not happen, and the agent works.

The temptation is to conclude that the eleven chapters were unnecessary. The right conclusion is different: **none of it was solved, all of it was assumed by the platform**. Context is whatever the workflow mapped; permission is the topology of the connected nodes. Memory is whatever the engine persists between runs; and compaction does not exist because the conversation was not supposed to grow.

The question this chapter asks is the only one that matters: **what happens at message 200?**

## In practice: the same agent, written twice

This chapter asks for no new code. The exercise is comparing what you built with what the platform delivers, and the comparison fits in a table.

Take the ch. 02 agent (the twenty-line loop, with brakes, policy and trace) and put it next to three workflow nodes doing the same thing. For each dimension in the book, ask who provides it: you, the platform, or nobody.

The result has three columns, and the third is the lesson. **Who provides** tells you what you did not have to build. **How** tells you how much of it is configurable. And **what you gave up being able to change** is the price, and it is the column no vendor material has.

Draw that table for your case before deciding. It answers the message-200 question without your having to get there.

## The problem

In the previous chapters, the harness contains the work: the loop drives, the tools act, the workflow emerges from the model's decisions. Tools like **n8n** invert the relationship — **the workflow contains the harness**. An "agent node" is a step inside a graph designed by a human. Surrounded by triggers (webhook, cron, chat), integrations and error handling that the workflow engine already provided before AI existed.

This inversion raises the question that gives the category its meaning: **which dimensions of the scaffolding are essential, and which are replaceable by the environment?**

## The state of the art

### What the environment does away with

The evaluation of the category's representative (n8n, see Appendix A) confirms the thesis with uncomfortable precision. The weak dimensions of the embedded harness are exactly the ones the environment does away with.

| Dimension dispensed | Why the environment dispenses it |
|---|---|
| Compaction | Event-triggered executions are short, context does not accumulate |
| Planning | The plan *is* the workflow graph, drawn by the human on the canvas |
| Context delivery | Context arrives mapped from previous steps via expressions |
| Granular permissions | The topology is already the allowlist |

The last point deserves emphasis: in the embedded harness, **permission is topology**. There is no per-call approval inside the loop, the LLM (Large Language Model) can only invoke what the author plugged into the canvas. It is an allowlist by construction, decided visually by a human, complemented by real human-in-the-loop. Nodes that pause execution durably, awaiting approval on a channel (Slack/Outlook), instead of the CLIs' synchronous approval prompt.

And the strong dimensions are where the engine has a structural advantage: **tools** (the pre-existing integrations become a tool pool). **memory** (pluggable database backends), **interfaces** (hosted chat, webhooks, embeddable widget), **MCP (Model Context Protocol)** (client *and* server) and **subagents** (agent-as-tool and sub-workflows). No dedicated harness has a tool pool the size of a converted integration ecosystem, because none has a pre-existing ecosystem to convert.

### The borrowed loop, and the re-internalization trajectory

The embedded harness typically does not write its own loop: it borrows it from a framework (in the case observed, LangChain JS). But the trajectory measured in the benchmark points in a clear direction. The workflow engine starts by outsourcing the loop and **re-internalizes the half that matters to a workflow engine, the scheduling of execution**. The framework still decides *which* tool to call; the *execution* of the call becomes the engine's responsibility again, as it schedules the nodes and re-enters the agent. (Code detail in Appendix A, finding 1.) The implication: workflow engines tend to absorb ever more of the harness, not the other way around.

### The ceiling of the substitution

But the substitution has a ceiling: **without compaction or planning, the agent node serves short automations, not long autonomous work**. An embedded agent that had to refactor a repository for hours would collapse the context window with no defense. The two layers do not compete, they complement each other by task duration and autonomy: the dedicated harness for long, open-ended work; the embedded one for pinpoint decisions inside structured processes.

### Implications

1. **For those building a dedicated harness**: the `$fromAI` pattern (Appendix A, finding 2) shows how to derive tools from existing surfaces without writing wrappers. Durable HITL (pausing execution for days awaiting approval on a channel) is superior to the CLIs' synchronous approval prompt.
2. **For those building on top of workflow engines**: the category's gaps (compaction, plan mode) are the obvious roadmap. And the loop's re-internalization trajectory suggests the engines will absorb ever more of the harness, not the other way around.
3. **For the book's taxonomy**: "how much harness is needed" is a function of the *execution environment*, not a universal constant. The benchmark's ruler measures scaffolding that is present; this category reminds us that scaffolding absent-by-design is not a gap, as long as the task class is respected.

### Executive summary

The embedded harness is not an incomplete dedicated harness: it is a category in which the execution environment replaces. By construction, half of the scaffolding's dimensions, the plan becomes a graph, permission becomes topology, context becomes mapped expressions. The substitution holds as long as the task class is respected: pinpoint decisions inside structured processes, not long autonomous work. **What to steal** today: automatic derivation of tools from existing integrations (the `$fromAI` pattern) and durable human-in-the-loop instead of synchronous approval.

> **See also**: the living collection [Awesome Harness Engineering. Production Infrastructure & Operations](https://github.com/GHDaru/awesome-harness-engineering#production-infrastructure--operations) gathers more consultable resources for this dimension, curated by problem.

## Check your understanding

1. State the inversion that defines the category and explain why it turns the benchmark's "weak dimensions" into "dimensions dispensed by the environment". (If needed, re-read "What the environment does away with".)
2. Why does permission-as-topology do away with per-call approval inside the loop, and which mechanism complements this allowlist when a human decision is genuinely needed mid-execution?
3. A team wants to use a workflow engine's agent node to refactor a repository for hours. Explain, in terms of compaction and planning, why this collapses, and what the correct division between embedded and dedicated harness would be for that task.
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

---

## Verification answers

**1.** The inversion is: in a dedicated harness the agent **provides** the dimensions; in an embedded one the environment **assumes** them. It turns a low score into something else because the benchmark ruler measures what the system implements, and here what matters is what the system **needs** to implement. There is no context assembler because the workflow author maps context by hand; there is no per-call permission policy because permission is already the topology. Calling that a "weak dimension" would be judging a car by its lack of oars. What the ruler should record, then, is not the score but **who provides** — which is why the category has its own archetype in ch. 01.

**2.** Because the allowlist is **structural**: at design time the workflow author chose exactly which nodes the agent reaches, and no others exist from its point of view. There is nothing to approve at runtime because there is no way to request what is not connected. It is the cleanest case of a policy that does not depend on the model's obedience, and it works only because the action set is closed in advance — a condition a terminal harness with a shell never has.

The complementary mechanism is **human-in-the-loop with durable pause**: when a decision really does need a person, the workflow suspends execution, notifies, and resumes when the answer arrives, possibly hours later. It is the difference between asking and **waiting**, and it is what a blocking `input()` does not do.

**3.** It collapses for two compounding reasons. The conversation grows with nobody managing it: there is no compaction ladder, so the run either blows the window or starts carrying a history that degrades quality, which is ch. 03's *context rot*. And there is no planning or persisted task list, so a task lasting hours loses the constraints stated at the beginning, which is exactly the defect ch. 09 attacks.

The signal to migrate is the same in both cases: **when the task stops fitting in one run**. An embedded agent is excellent for single-message, event-triggered work, and it is the wrong tool for long, stateful sessions. The choice is not about quality, it is about the shape of the task.

**4.** The first is **deriving tools from components that already exist**: any node in the system becomes an agent tool, with the schema derived from the node definition. It replaces the manual work of writing and maintaining tools one by one, and it is the ch. 05 derived-schema idea raised one level — instead of deriving from a function signature, it derives from a component definition.

The second is **human-in-the-loop with durable pause**, which improves ch. 07's inline approval exactly where it is weakest: approval requiring someone present right now does not survive asynchronous work. A dedicated harness stealing that idea would trade "block waiting for an answer" for "suspend and resume", and would get ch. 13's headless mode for free.
