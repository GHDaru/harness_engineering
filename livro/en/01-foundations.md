<!-- i18n fonte:livro/01-fundamentos.md edicao:0.82 hash:35d4caba -->
# 01 — Foundations

> **State of the art captured in 2026-07** · last revised 2026-08-12 · [history and expiration log](../historico.html)
>
> Didactic layer v4 — see [Editorial Guide §2.1](editorial-guide.md).
> scaffold: completo

## Three things called "agent"

Ask three engineers to define "AI agent" and you get three incompatible answers.

The first says it is a model with access to tools. The second says it is a system that pursues a goal without supervision. The third shows the product they use every day and says "this".

The three answers describe different things, and that is why discussions about agents go in circles: the parties are not talking about the same object. Worse, the confusion has a practical consequence. If you cannot say where the model ends and the rest begins, you cannot say what a failure should be attributed to, and you spend weeks swapping models to solve a context problem.

This chapter exists to make the conversation possible. It answers three questions: **what** a harness is, **where it came from** and what existed before, and **with what rigor** this book studies it.

## 1. What a harness is (definition)

The working definition comes from the curated list [awesome-harness-engineering](https://github.com/GHDaru/awesome-harness-engineering):

> **Harness engineering** is the discipline of designing the *scaffolding* — the support structure — that surrounds an AI agent (context delivery, tool interfaces, planning artifacts, verification loops, memory systems and sandboxes) and determines whether it succeeds or fails at real tasks.

With the guiding principle:

> The focus is the *harness*, not the model. Every component exists because the model cannot do it on its own, and the best harnesses are designed knowing that those components will become unnecessary as models improve.

Note the central term: **scaffolding**. It is the book's metaphor, the temporary structure raised around something under construction, which holds the work up and is then removed.

Keep the word. It comes back in the subtitle, in the title of every part, and in §8, when the scaffold gets an expiry date.

> **For those just arriving, an image that holds up the whole book.** Think of the model as a brilliant professional on their first day at a company they do not know: capable, but with no desk, no system access, no knowledge of house rules, and a memory that resets with every conversation.
>
> The harness is everything the company builds around them. The project dossier they read on arrival is the context (ch. 03). The tools on the bench are the tools (ch. 05). The badge that defines where they may enter is permissions (ch. 07). The notebook that survives the end of the shift is memory (ch. 08). The supervisor who reviews the delivery before it ships is verification (ch. 11). And the shift itself, the rhythm of working, checking and continuing, is the loop (ch. 02).
>
> When the chapters get technical, come back to this image: every dimension of the book is a piece of that office.

## 2. What existed before, and why it was not agents

"Software that acts for you" is an old idea. Earlier generations solved the problem **without a language model at the center of the decision loop**, and that is what separates them from an agent.

- **Expert systems** (1980s): hand-written `if-then` rules. They automated decisions, but did not interpret goals in natural language nor recover from unforeseen exceptions.
- **RPA, Robotic Process Automation** (UiPath, Automation Anywhere): robots that repeat clicks and keystrokes from a fixed *script*. Brittle to any screen change, with no goal and no recovery.
- **Intent chatbots**, from ELIZA to dialogue trees: they produced text, but **did not execute actions** in the world.
- **Coding assistants as autocomplete**: **GitHub Copilot** (technical preview in Jun/2021), powered by the **OpenAI Codex** model, a descendant of GPT-3 fine-tuned on code, suggested the next line *inside the editor*, with no plan, no tools and no verification loop.

None of them had the **four pieces** that define a harness today (§4). What they lacked was goal-oriented autonomy and the ability to act on the environment **and correct their own course**.

## 3. How we got here: the technical lineage

The move from "a model that answers" to "an agent that acts" was built in layers, each one removing an obstacle.

1. **Explicit reasoning.** *Chain-of-Thought* (Wei et al., 2022) showed that asking the model to "think step by step" improves reasoning tasks.
2. **The loop.** The decisive milestone was **ReAct**, *Synergizing Reasoning and Acting in Language Models* (Yao et al., [arXiv:2210.03629](https://arxiv.org/abs/2210.03629), Oct/2022; ICLR 2023), which interleaved **Thought → Action → Observation**. The model reasons, calls a tool, observes the result and continues. That cycle is the skeleton of nearly every modern harness (chapter 02).
3. **Tool calling.** What was missing was a reliable way for the model to *invoke* tools, solved when OpenAI launched **function calling** (Jun/2023): the model emits structured JSON to trigger functions (chapter 05).
4. **The autonomous wave, and its lesson.** With reasoning, action and tools in place, 2023 arrived: **AutoGPT** (Significant Gravitas, Mar/2023) and **BabyAGI** (Yohei Nakajima, Apr/2023), loops that decomposed themselves into subtasks and ran on their own. They "failed" in practical terms, going in circles, burning tokens and losing the thread, because they had *the loop* but **not** the other three pieces: context management, well-designed tools and control. The discipline's founding lesson is born there: **the model alone is not enough, the scaffolding around it is what decides success.**
5. **Maturity, the coding CLIs.** The four pieces were embedded in terminal tools wired to the file system and to Git: **Aider** (Paul Gauthier, Apr/2023), **Claude Code** (Anthropic, research preview in Feb/2025), **OpenAI Codex CLI** (open source, Apr/2025), plus projects such as **Cline**, **OpenHands** and **SWE-agent**.
6. **Standardization.** With agents proliferating, the protocols came. The **Model Context Protocol (MCP)**, opened by Anthropic (Nov/2024), standardized connection to tools and data (chapter 06). **AGENTS.md** consolidated as the "README for agents". **Agent2Agent (A2A (Agent-to-Agent))** (Google, Apr/2025; later donated to the Linux Foundation) addressed communication *between* agents (chapter 17).

**Timeline (milestones):** 1980s expert systems · 2000s–2010s RPA and chatbots · **Jun/2021** Copilot (autocomplete) · **Oct/2022** ReAct · **Mar–Apr/2023** GPT-4, AutoGPT, BabyAGI, Aider · **Jun/2023** function calling · **Nov/2024** MCP · **Feb/2025** Claude Code · **Apr/2025** Codex CLI and A2A.

> **A note on rigor.** "Codex" names three distinct things: the 2021 *model* (the basis of Copilot), OpenAI's Codex *product line* and the open source *Codex CLI* of 2025. The text keeps them separate. Dates and sources for this section are in the [Bibliography](bibliography.md), and items still to be verified are flagged there.

## 4. The constitutive definition: the four elements

The literature of the discipline converges on a definition of the harness as a **runtime layer** with four necessary and sufficient elements:

1. **Agent loop** — the cycle that alternates between invoking the model and executing what it decided, until a stopping criterion (ch. 02).
2. **Tool interface** — the contract through which the model acts on the world: read files, run commands, call APIs (ch. 05).
3. **Context management** — the assembly, prioritization and compression of what the model sees on each call (chs. 03–04).
4. **Control mechanisms** — permissions, approvals, sandboxes and limits that restrict what the agent may do (ch. 07).

A system missing any of the four **is not a complete harness**. A chatbot with tools but no loop is a "function caller". A loop without control is an incident waiting to happen. Tools without context management collapse on long tasks.

This is the operational definition that serves as the study's **inclusion test** (§5 and §6), and the next section shows how it decides in practice.

### The definition is converging from the outside, from five uncoordinated directions

It is worth enumerating them, because the strength of the argument lies in the number of independent sources.

**Microsoft**, announcing its Agent Framework, defines a harness as *"the **scaffolding** that turns a language model into an agent"*.

The survey by **Meng et al.** formalizes `H = (E, T, C, S, L, V)`: loop, tools, context, state, lifecycle, evaluation.

The **RUCAIBox** survey organizes the field into four axes with the same spine.

The `best-of-Agent-Harnesses` directory synthesizes *"the model thinks; the harness decides what that thinking is allowed to touch"*, and it is the only one that puts permission **inside** the definition rather than as a separate chapter.

And the most operational of all, because it defines by what can be **verified on the file system**: the [Harness Score](https://github.com/paladini/harness-score) measures six dimensions (context, skills, guardrails, sensors, CI, hygiene) that map almost cleanly onto the chapters of this book. The [Appendix — Measure your harness](appendix-harness-score.md) applies the ruler to this very repository, with the uncomfortable result it produced.

Five independent groups arriving at the same elements is the best available argument that the definition describes something real, and not an editorial cut of our own. The four pieces above are the shape this book gives that consensus.

## In practice: using the definition to decide

A definition is only worth something if it decides hard cases. Let us apply the four-piece test to three systems, one at a time, looking at what exists in the code.

**Case 1: a script that calls the model's API and executes whatever it asks for.**

```python
response = model.call(messages, tools=[run_shell])
for call in response.tool_calls:
    subprocess.run(call.args["command"], shell=True)   # no confirmation
```

- Loop? **No.** A single pass, with no result fed back.
- Tools? **Yes**, one.
- Context management? **No.** The messages go as they are.
- Control? **No.** `shell=True` with no confirmation and no sandbox.

Verdict: **a function caller**, not a harness. The loop is missing, which is what turns an answer into work, and the brake is missing too.

**Case 2: the same script, now with a loop and a limit.**

```python
for turn in range(MAX_TURNS):
    response = model.call(trim(messages, limit=100_000), tools=TOOLS)
    if not response.tool_calls:
        break
    for call in response.tool_calls:
        if not policy.allows(call):              # control
            result = "refused by policy"
        else:
            result = execute(call)
        messages.append(result)                  # feeds back
```

- Loop? **Yes**, with a stopping criterion and a cap.
- Tools? **Yes.**
- Context management? **Yes**, however primitive: `trim` decides what fits.
- Control? **Yes**, `policy.allows` before any effect.

Verdict: **a complete harness**, and deliberately ugly. The four pieces do not demand sophistication, they demand existence. That is why the inclusion test is useful: it separates category from quality.

**Case 3: a framework that exposes loop, state and tools as primitives, but runs nothing on its own.**

Here the four pieces are present **as possibility**, not as decisions taken. Whoever uses the library chooses the stopping policy, the context trimming and the permission rule.

Verdict: it enters the corpus as a **framework**, its own archetype (§5), and is evaluated by a different ruler. Comparing a framework's permission score with that of a finished product would compare potential with choice, which is why the benchmark scores **only compare within the same category**.

Keep the method of this exercise, because the book repeats it fifteen times: **ask for the four pieces, find the line of code that proves each answer, and only then classify.**

## 5. Where the harnesses in this study come from

The corpus is **open source** (the book's Principle II: the base source is the code) and splits into five archetypes, the same as chapter 00:

- **Coding harnesses** (opencode, gemini-cli, OpenHarness, Codex CLI, Goose, Aider, OpenHands, Grok Build, Pi, Kimi Code, Prime Agent): reference implementations that join the four pieces into an executable.
- **Self-hosted personal agents** (OpenClaw, Hermes Agent, IronClaw, ohmo): the harness in the service of one person, with its own identity, memory and channels.
- **Organizational agents** (QM): the harness in the service of an organization, with scopes, audience-based permissions and auditing as primitives, and the agent loop as a swappable engine.
- **Embedded harnesses** (n8n, AI Agent node): the loop as a component inside a larger product.
- **Frameworks** (LangGraph, CrewAI, OpenAI Agents SDK, Software Agent SDK): they expose loop, state and tools as programmable primitives.

The **inclusion test** is the definition in §4: whoever has loop, tools, context management and control gets in. Pure model libraries and mere single-tool *wrappers* stay out.

One criterion deserves careful reading, because a borderline case has already tested it: what is required is code **open and inspectable** at the cut-off date, not code **open to contribution**. A project may publish its source under a permissive license and refuse external contribution by written policy, and still get in, because what the study needs is to **read**, not to participate.

The evaluated list, with the repository and the commit read for each system, is in the [Comparative](comparative.md) and in the study appendix. Resources beyond the corpus are in the living collection [Awesome Harness Engineering](https://github.com/GHDaru/awesome-harness-engineering).

## 6. The study's method (rigor)

This book **reads the source code of real harnesses**, compares them by dimension and then **builds a harness from scratch**. This is not "an engineer's opinion": it is a hybrid research design resting on established methodological traditions. Making them explicit turns the book from a collection of impressions into an **auditable empirical study**, consistent with Principle I.

**In plain language, before the technical names.** The method has four steps:

1. choose systems that represent different *types* of harness, not the most famous ones;
2. read the code of each following **the same script of questions**, noting the exact file that proves each answer;
3. score against a fixed, published ruler, so that anyone can disagree while looking at the same evidence;
4. build a harness from scratch, to test whether the extracted patterns hold up.

The paragraphs that follow give the formal names of those choices and where each comes from. They are the genealogy of the rigor, and can be skimmed on a first pass.

**Two phases, two engines.**

- **Phase 1, descriptive and comparative:** a **multiple case study** (Yin) supported by **Mining Software Repositories** (Hassan, 2008), treating each repository as *primary data*. The unit of analysis is **the source code**, not marketing material nor observed behavior in use.
- **Phase 2, constructive and prescriptive:** `harness-zero` is an exercise in **Design Science Research** (Hevner et al., 2004; the DSRM process of Peffers et al., 2007), designing and evaluating an artifact that instantiates the principles extracted in Phase 1.

**How dimensions become measurement.** The comparison dimensions descend through **Goal–Question–Metric** (Basili, Caldiera & Rombach). For each harness goal (context, tools, permissions, memory, verification, loop, orchestration) questions are formulated and, for each question, **indicators observable in the code**: is there a compaction mechanism? what is the granularity of the permission model? is there a post-action verification layer?

**Selection by replication, not sampling.** Cases are chosen by Yin's **replication logic**, *literal* when the same pattern is expected and *theoretical* when a predictable difference is expected. The criteria are explicit: open and inspectable code at the cut-off date; membership in the "harness" class (§4); adoption relevance **or** architectural singularity; archetype diversity (§5). For each case we record **URL, commit or tag, and reading date**.

**Coding and synthesis.** The reading follows a protocol common to all cases (Runeson & Höst, 2009). It combines inductive coding inspired by *grounded theory* (Stol, Ralph & Fitzgerald, 2016) in the discovery of dimensions with fixed-grid *content analysis* (Hsieh & Shannon, 2005) in the scoring. The comparative synthesis is a **feature analysis** in the **DESMET** style (Kitchenham, Linkman & Law, 1997), in the tradition of *benchmarking* as an engine of scientific progress (Sim, Easterbrook & Holt, 2003).

**Threats to validity** (taxonomy of Cook & Campbell, 1979, adapted to case study):

| Type | Threat | Declared mitigation |
|---|---|---|
| Construct | the "dimensions" not capturing what defines a harness | GQM derivation; published operational definitions |
| Internal | attributing to "good practice" what is a historical accident of the project | single protocol; every claim traced to a snippet/commit |
| External / **obsolescence** | failure to generalize; the field changes in months | archetype-based selection; **cut-off date + fixed commits**; the **expiration clause** (§8) is the declared mitigation, not an ornament |
| Conclusion | treating qualitative scores as exact metrics | explicit scale and criteria (DESMET); no spurious numerical aggregation |

Thus every claim in the book traces back to **a datum in the repository** and to **a named procedure**. The operational details are in the [Comparative](comparative.md) and in the evaluation template; the references, in the [Bibliography](bibliography.md).

## 7. Taxonomy by problem

A convention inherited from the reference collection: organize the discipline **by the problem being solved, not by vendor or model**. It is the taxonomy that structures the chapters.

| Problem | Chapter |
|---|---|
| How the decision-action cycle works and when it stops | 02 — Agent Loop |
| What the model sees and how that is assembled | 03 — Context Delivery |
| What to do when the context window runs out | 04 — Compaction |
| How the model acts on the world | 05 — Tool Design |
| How to integrate external capabilities in a standardized way | 06 — MCP |
| What the agent may do, and where | 07 — Permissions and Sandboxing |
| What persists across turns and across sessions | 08 — Memory and State |
| How large work becomes verifiable steps | 09 — Planning |
| How to distribute work across multiple agents | 10 — Subagents and Orchestration |
| How to know whether the agent (and the harness) work | 11 — Verification and Evals |
| How third parties extend the harness | 12 — Extensibility |
| Through what surfaces humans and systems use the agent | 13 — Interfaces |

## 8. The expiration clause

The discipline's most important and least practiced thesis: **every harness component is a temporary prosthesis.**

Compaction exists because context windows are finite. *Plan mode* exists because models act rashly. The *policy engine* exists because models are not trustworthy with destructive commands. Each premise has a shelf life.

The practical corollary is a design requirement: every component should document **which model capability improvement would make it unnecessary**. Harnesses that fail to do this accumulate dead *scaffolding*, complexity that outlives the limitation that justified it.

As seen in §6, this clause is also the **declared mitigation** of the obsolescence threat: the book assumes it is dated. We return to it in chapter 14, where it gets a scoreboard.

## 9. Operational artifacts

The discipline has produced standard artifacts that reappear, with variations, in nearly every harness studied:

- **Project instructions file** (`AGENTS.md` / `CLAUDE.md` / `GEMINI.md`): rules, conventions and limits the agent reads before any task. Clear boundaries beat vague restrictions.
- **Plan artifact** (`PLAN.md`): created at the start of the task and updated during execution, with verifiable milestones and scope boundaries.
- **Implementation log** (`IMPLEMENT.md`): an *append-only* record of decisions and deviations from the plan.
- **Harness checklist** (`HARNESS_CHECKLIST.md`): a pre-production review covering instructions, tools, context, planning, permissions and verification, with the expiration table from §8.

These artifacts are the embryo of our evaluation instrument (see `benchmark/template/HARNESS_EVAL.md`).

## Check your understanding

1. A system has a loop, tools and context management, but executes any command with no confirmation and no sandbox. Is it a harness by the §4 test? And is it a good harness?
2. Why do the benchmark scores only compare systems within the same category?
3. The inclusion criterion requires code that is "open and inspectable", not "open to contribution". What kind of project does that distinction admit, and why is it the right choice for this study?
4. Pick any harness component and write its expiration clause: which model capability improvement would make it unnecessary?

---

*This chapter's sources (historical and methodological) are consolidated in the [Bibliography](bibliography.md), separating the **confirmed** ones from those still awaiting verification, faithful to Principle I.*

---

## Verification answers

**1.** By the §4 test, **no**: the control mechanisms are missing, and they are one of the four necessary pieces. The system is a loop without a brake, and the chapter describes it as "an incident waiting to happen". Notice that the question separates two things that are often confused: the four-piece test decides **category**, not **quality**. A harness can have all four pieces and be bad at all of them; a system can be excellent at three and not be a harness.

**2.** Because the categories answer different questions. A framework exposes the four pieces as **programmable possibility**, and whoever uses it decides the stopping policy and the permission rule. A finished product has already **made** those decisions, and can be judged by them. Giving both the same permission score would compare potential with choice. That is why the ruler holds within the archetype, and the comparison never aggregates the five into a single score.

**3.** It admits the project that publishes its source under a permissive license and, at the same time, **refuses external contribution** by written policy, publishing the code for transparency and local builds. It is the right choice because what this study needs to do with the code is **read** it: the unit of analysis in Phase 1 is the source code, and reading does not require the right to participate. A criterion demanding openness to contribution would exclude perfectly inspectable systems and would measure governance instead of architecture.

**4.** There is no single answer, and the value is in the form. A well-written clause names the **absent capability**, not the discomfort. "Compaction stops being necessary when the context window exceeds the typical size of a whole working session **and** the cost per token stops growing with length" is a clause. "Compaction goes away when models get better" is not: there is no way to tell whether it has already happened. The test of a good expiration clause is whether it can be **verified as met**.
