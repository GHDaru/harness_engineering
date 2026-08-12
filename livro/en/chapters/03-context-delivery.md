<!-- i18n fonte:livro/capitulos/03-entrega-de-contexto.md edicao:0.82 hash:7e301192 -->
# 03 — Context Delivery

> **State of the art captured in 2026-07** · last revised 2026-08-12 · [history and expiration log](../historico.html)
>
> Didactic layer v4 — see [Editorial Guide §2.1](../editorial-guide.md).
> scaffold: completo
>
> Skeleton v3 — body with the state of the art; per-repository treatment in Appendix A (online supplement).

## Learning objectives

By the end of this chapter, you should be able to:
1. **Explain** why context is a budget managed at runtime, not a warehouse, and what *context rot* is;
2. **Compose** a system prompt in layers ordered by volatility, aware of caching;
3. **Design** a cascade of context files (global → project → package → personal) with declared precedence;
4. **Implement** the harness-zero context assembler (step 3) with a project rules file;
5. **Assess** a real AGENTS.md against the authoring practices: lean, executable commands, grown from evidence of failure.

## The bill that quadrupled without anyone changing anything

Two quiet weeks of use. In the third, the agent's bill quadruples.

Nobody changed the model, nobody changed the volume of work, nobody added a tool. The team looks for a leak, looks for an infinite loop, looks for someone running evals in production. Nothing.

What changed was one line. Someone thought it useful for the agent to know the time, and added, at the top of the system prompt:

```text
Date and time: 2026-08-12T14:07:33
```

One line, in the wrong place. The provider's cache works **by prefix**: it reuses the identical beginning across calls and charges little for it. A value that changes every second, placed at the top, guarantees that **no** call shares a prefix with the previous one. The cache never hits, and everything is billed as new.

This is not an optimization detail. The **order** in which context is assembled is a cost decision, and this chapter is about building that order on purpose.

## The problem

The model only knows what the harness shows it.

Context delivery is the engineering of deciding **what** goes into each call — system prompt, project rules, environment state, memories, instructions from external servers —, **in what order**, and **how that changes** mid-conversation without breaking the provider's cache or confusing the model.

There are three classic sub-problems: where the project rules live and how they are discovered; whether the system prompt should vary per model; and how to report state changes mid-conversation without invalidating the cached prefix.

## Scientific foundations

- **Context degrades with position and with volume** — *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)): information in the middle of long contexts is poorly used. The design consequence is direct: what matters goes to the edges, with the system prompt at the start and the current task at the end, and "send everything" is an anti-pattern with empirical grounding.
- **Context engineering as a discipline** — the survey [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) systematizes the area (RAG, memory, tool-integrated reasoning) and legitimizes the term the industry adopted.
- **Less context, better agents** — [arXiv 2606.10209](https://arxiv.org/abs/2606.10209) measures, in long-running agents, what Anthropic calls *context rot*: aggressive curation beats full windows.

(Full bibliography: `livro/bibliografia.md`.)

## Industry sources

- **[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** (Anthropic Engineering): names the successor to prompt engineering. The work is **curating the optimal set of tokens at inference time**, and the text names *context rot* as an engineering fact. The decision that follows: the window is a budget, and the goal is the smallest set of high-signal tokens.
- **[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)** + **[Lessons from building Claude Code: prompt caching is everything](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything)**: the cache is **by prefix**, so assembly order is a cost decision. The write-up lists the classic invalidators — timestamp at the top, request ID in the tool list, non-deterministic re-serialization of history — and treats **cache hit rate as a first-class harness metric**, with about 59% reduction in billable input.
- **[AGENTS.md](https://agents.md/)** + **[Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/)**: the "README for agents" was **donated to the Linux Foundation** in December 2025, with OpenAI, Anthropic and Block as co-founders, and more than 60,000 projects use it. Context by repository file became neutral, portable infrastructure, so investing in that pipeline is safe.
- **[How Claude remembers your project](https://code.claude.com/docs/en/memory)**: formalizes the **cascade** global → project → local, with the nearest file winning and the personal one outside version control.
- **[AGENTS.md Field Guide 2026](https://www.iuriio.com/blog/posts/2026/05/agents-md-field-guide-2026)** (practitioner): the authoring side. Start at around 30 lines, cap at 150–200 at the root, exact commands before prose, nest per package in a monorepo, and **grow it only from evidence of recurring failure**. The common mistake is treating it as documentation.
- **See also**: the living collection [Awesome Harness Engineering — Context Delivery & Compaction](https://github.com/GHDaru/awesome-harness-engineering#context-delivery--compaction) gathers more resources for this dimension, curated by problem.

## In practice: assemble by volatility, and prove it worked

The naive assembler concatenates whatever shows up:

```python
def montar_contexto(tarefa: str) -> str:
    return "\n".join([
        f"Date and time: {datetime.now().isoformat()}",  # ← changes every call
        LEIA("identidade.md"),
        f"Directory: {os.getcwd()}",
        LEIA("AGENTS.md"),
        tarefa,
    ])
```

It is correct and expensive. The first line invalidates everything that comes after it.

The fix is not removing the timestamp: sometimes the agent really does need to know the time. The fix is **ordering by volatility** — what almost never changes first, what changes every turn last:

```python
CAMADAS = [
    ("identidade", lambda _: LEIA("identidade.md")),         # changes on release
    ("ambiente",   lambda _: f"OS: {platform.system()}"),    # changes per machine
    ("projeto",    lambda _: cascata_agents_md()),           # changes on commit
    ("memoria",    lambda s: memorias_relevantes(s)),        # changes per session
    ("volatil",    lambda _: f"Now: {datetime.now():%H:%M}"),  # changes always
]

def montar_contexto(sessao) -> str:
    return "\n\n".join(f"## {nome}\n{fn(sessao)}" for nome, fn in CAMADAS)
```

The timestamp is still there, now **at the end**. Everything above it is byte-for-byte identical across turns, and it is exactly that "everything above" that the cache charges little for.

Now the part almost nobody does: **proving it**. Prefix stability is an invariant, and an invariant without a test is a hope.

```python
def test_prefixo_estavel():
    a = montar_contexto(sessao)
    time.sleep(1.1)                      # time passes: the volatile layer changes
    b = montar_contexto(sessao)

    comum = os.path.commonprefix([a, b])
    assert comum, "the two contexts diverge at the very first byte"

    # the common prefix must cover everything except the volatile layer
    corte = a.index("## volatil")
    assert len(comum) >= corte, (
        f"prefix diverged at {len(comum)}, earlier than expected ({corte}).\n"
        f"from here on: {a[len(comum):len(comum)+80]!r}"
    )
```

The error message is the useful part. When someone adds a `request_id` in the middle of assembly six months from now, the test will not merely say "failed": it prints **the offset where the two contexts diverged and the next 80 characters**, which is the culprit's name.

That is what the team in the opening scene lacked. They found the line after three weeks and a bill; with this assertion, they would have found it at commit time.

## The state of the art

### 1. Context is a managed budget, and retrieval became just-in-time

The modern consensus inverted the instinct that more context is better. The harness actively manages the window: rule-based pruning, awareness of what is left, on-demand retrieval.

Two implementations stand out in the benchmark. One gives the model the structure of an entire repository for about a thousand tokens, built by syntactic analysis and graph ranking, with no explorer agent at all — static just-in-time retrieval. The other loads rules per subdirectory **as the agent navigates**, rather than everything up front.

### 2. Prefix stability became an architectural requirement

It is the "In practice" section promoted to a principle. Cache-awareness stopped being an optimization and reorganized assembly: layers by volatility, deterministic serialization, zero volatile content at the top.

The two most rigorous formalizations in the corpus treat the prefix as an **immutable baseline**, delivering state changes only at safe turn boundaries, and declare the three layers of the example above under those names. One of them takes the idea further: the fork that curates skills **inherits the parent's prefix**, saving about 26%.

### 3. The rules file standardized, and became a cascade

The naming fragmentation of the discipline's early days is resolved by neutral governance. The portable format is read natively by nearly the whole corpus, with the proprietary names becoming aliases.

The mature pattern is the **cascade with declared precedence**: global, project, package and personal, with the nearest one winning and the personal one outside version control. There is composition by import, and there is the authoring practice that separates a useful file from dead documentation — growing it **from evidence of failure**, the way code grows from bugs.

### 4. The new frontiers

Three recent movements have not yet become consensus.

**Prompt per model family**, with one harness keeping about ten variants and another taking it to the extreme with instructions **coming from the server**: the backend delivers the base prompt per model, with even a configurable personality.

**Separating persona from rules**, a contribution from the personal-agent category: one file for voice and identity, another for the operational rules.

**Context with a trust class**: personal or injected content travels in envelopes that preserve its origin, so the harness knows what is your instruction and what is a third party's text. It is context delivery meeting the security of ch. 07.

> **The counterpoint: the minimal harness (Pi)** — *addendum from round ext-1, 2026-07-31.* While this chapter describes ever richer assemblers, [Pi](https://github.com/badlogic/pi-mono) bets in the opposite direction: a base system prompt **measured at ~460 tokens**, derived from the tool set (each tool contributes its snippet, and guidelines only enter if the corresponding tool is active), with skills announced **by name and description only** — the body is loaded by the model itself when the task calls for it.
>
> Editorial honesty requires the two caveats that reading the code revealed. First: the same assembler concatenates the cascade's `AGENTS.md` files **without a budget**, which in Pi's own repository adds about 2,700 tokens, six times the slogan — the minimalism is the harness's, not the context's. Second: minimalism is not the absence of engineering, and Pi's compaction is the most complete in the corpus (see [evaluation](../../../benchmark/avaliacoes/pi.md)).
>
> The underlying bet is falsifiable and worth tracking: **better models would need less harness**. If that is true, part of this chapter expires. If the window stays expensive, the missing budget charges interest.

### Executive summary

What is most modern: budget and just-in-time retrieval instead of volume; a stable prefix as a requirement, with cache hit rate treated as an indicator; a rules file in a cascade under neutral governance; and the three frontiers (prompt per model, separated persona, trust class). The minimalist counterpoint shows the other end of the spectrum and proves that the tension between budget and richness is still open.

**What to steal:**

- **The repository map**, as a cheap alternative to agent-driven exploration.
- **The three volatility layers** in system prompt assembly.
- **The discipline of growing the rules file only from recurring failure.**
- **The prompt snippet attached to the tool definition**, which keeps prompt and tool set from drifting apart.
- **The prefix-stability test** from the "In practice" section. It is the cheapest piece in this chapter.

## Hands-on — harness-zero, step 3

In step 3 (`harness-zero/etapas/03-contexto/`) you build the harness-zero assembler: a system prompt in layers ordered by volatility, discovery of an `AGENTS.md` at the target project's root, the `/contexto` window to see what was assembled, and the prefix-stability test written above.

Completion exercise: the cascade discovery function ships with one level only. You implement the precedence global → project → package → personal, with the nearest one winning.

And keep this pending item noted, because the next chapter collects on it: this step's `read_file` reads **any** path the model asks for. The wound is opened here and closed in ch. 07.

## Check your understanding

1. Why is a timestamp at the top of the system prompt expensive, and where should it go?
2. Your agent repeatedly ignores a project convention. What is the right answer according to modern authoring practice, and what is the wrong one?
3. A harness wants to tell the model that the date changed mid-conversation. Describe two strategies with different cache costs.
4. The prefix-stability test passes today. Someone adds a spent-token counter to the environment layer. Does the test still pass? Why?

---

## Appendix A — How each repository handles context delivery

> Per-harness evidence, with paths — online supplement, expanded with each benchmark round.

### opencode (round 1) — typed algebra and Context Epochs
`packages/opencode/src/session/system.ts` assembles environment + skills + MCP (Model Context Protocol) instructions; **~10 prompts per model family** in `session/prompt/*.txt` (anthropic, gpt, codex, gemini, kimi, beast...), selected by model-id substring; global/ancestor `AGENTS.md` aggregated by `session/instruction.ts`. V2 (`CONTEXT.md`) formalizes context as an algebra of "Context Sources" with snapshots, **Context Epochs** (cache baseline) and mid-conversation system messages only at safe boundaries.

### gemini-cli (round 1) — hierarchy with @imports
`prompts/promptProvider.ts` assembles by mode/tools/model (modern × legacy snippets); hierarchical `GEMINI.md` (`memoryDiscovery.ts`: global → parents → subfolders) with `@imports` (`memoryImportProcessor.ts`) and `flattenMemory`; full override via `GEMINI_SYSTEM_MD`; just-in-time injection (`tools/jit-context.ts`).

### OpenHarness (round 1) — aggregation with relevant memory
`src/openharness/prompts/context.py`: base + environment + `CLAUDE.md` + **memories selected by relevance** (`memory/relevance.py`, with `usage.py` tracking usage) + skills + active repo context; `-s/--append-system-prompt` on the CLI.

### Codex CLI (round 2) — central AGENTS.md + server-driven prompts
`core/src/agents_md.rs`: hierarchical discovery with merge from project-root to cwd; the system prompt **varies by model and comes from the backend** (`ModelInfo.base_instructions` via `models-manager`, with a template and `Personality::Friendly/Pragmatic`); environmental context via `WorldState`.

### Goose (round 2) — incremental hints and hardening
`SystemPromptBuilder` with override + extras; multi-file hints (**`.goosehints` AND `AGENTS.md`**, `CLAUDE.md` via config) respecting `.gitignore`; **`SubdirectoryHintTracker`** loads subdirectory hints as the agent navigates; anti prompt-injection sanitization of Unicode tags; per-turn "top of mind".

### Aider (round 2) — the repo-map ⭐
`aider/repomap.py`: definition/reference tags via tree-sitter (per-language `.scm` queries) → file→file graph → **personalized PageRank** (chat files and mentioned idents bias the ranking; ×10/×50/×0.1 multipliers) → rendering under budget with binary search (~1024 tokens; `map_mul_no_files=8` with no files in the chat) → mtime-keyed cache. The entire context-first path in one file.

### OpenHands/Canvas (round 2) — organizational skills
`app_conversation/skill_loader.py`: skills auto-discovered from the conventional repositories **`owner/.openhands` and `owner/.agents`** across all the user's organizations (GitHub/GitLab/Azure), with KeywordTrigger/TaskTrigger and a marketplace — team context versioned and loaded for all members.

### OpenClaw (round 2) — identity workspace with budgets
`buildAgentSystemPrompt` injects `SOUL.md` (persona), `AGENTS.md` (rules), `USER.md`, `IDENTITY.md`, `TOOLS.md`, `MEMORY.md`, `HEARTBEAT.md`, `BOOTSTRAP.md` — with budgets (20k chars/file, 60k total) and marked truncation; provider-aware contributions **above/below the cache boundary**.

### Hermes (round 2) — three layers by volatility ⭐
`agent/system_prompt.py` + `prompt_builder.py`: `stable` (identity/SOUL.md + guidance + skill index) → `context` (the project's AGENTS.md/.cursorrules) → `volatile` (memory, USER.md, timestamp) — explicit design for prefix-cache; persona migratable from OpenClaw.

### IronClaw (round 2) — context as a policy decision
`LoopPromptPort` (crates/ironclaw_loop_host): resolves identity, personal context (**opt-in per run profile, not per channel**), skills and security; injected/personal content travels in **prompt envelopes** with an unforgeable trust class — separating what the loop requests from what the host allows it to see.

### ohmo (round 2.5) — the minimal correct version
`ohmo/prompts.py`: ordered concatenation base → soul → identity → user → BOOTSTRAP → workspace → memory; the rigorous decision `include_project_memory=False` (the personal agent does not read a project's CLAUDE.md — tested).

### Pi (round ext-1) — the prompt derived from the tool set ⭐
`core/system-prompt.ts`: base **measured at ~460 tokens**, assembled from the tool definitions' own `promptSnippet`s with dedup and guidelines conditional on the active set (deactivate the tool, the prompt shrinks); skills announced only as `<name/description/location>` and loaded by the model via `read` (block omitted if `read` is not active); `AGENTS.md`/`CLAUDE.md` cascade global→root→cwd with dedup of nested worktrees (`resource-loader.ts`) — yet concatenated **with no budget** (see the box in the chapter body); full override via `.pi/SYSTEM.md`.

### n8n (round 2) — the embedded minimum
`ToolsAgent/common.ts`: `ChatPromptTemplate` with a free-form system message + history + rich binaries (images/PDF); no rules file and no hierarchy — the context comes mapped from the workflow by its author.

### Frameworks (frameworks round) — open by design
LangGraph and the Agents SDK (Software Development Kit) leave assembly to the dev (static or callable instructions); CrewAI imposes role/goal/backstory as structural context; the software-agent-sdk provides a Jinja preset with a documented escape hatch (`prompt_dir` + `_prompt_preset() -> None`).

---

## Verification answers

**1.** Because the provider's cache is **by prefix**: it reuses the identical beginning across calls. A value that changes every second at the top guarantees that no call shares a prefix with the previous one, and the whole context is billed as new. Its place is the **last layer**, after everything stable, so that the invalidated part is only the part that has to change. The same reasoning applies to a request ID in the tool list and to any non-deterministic re-serialization of history.

**2.** The right answer is to **add one specific rule to the project file, because of that failure**, with the exact command or convention, and nothing more. The wrong one is dumping documentation: turning the file into a project manual. The reason is budget and signal. Every line of the file enters **every** call, so generic documentation competes with the task for space and dilutes the instructions that matter. The rules file grows the way code grows: from a reproduced incident, not from a wish to be complete.

**3.** The expensive one: **rewrite the prefix**, updating the date wherever it sits and invalidating the cache from there on. The cheap one: deliver the change **at the end**, as a state message at a turn boundary, leaving the prefix intact. The second is the corpus pattern and has a name in the harnesses that formalize it — the prefix is treated as an immutable baseline, and state changes only enter at safe points. Choosing between them trades immediacy against cost, and the case where the expensive one is justified is when the information **must** be read before what is already in the context.

**4.** **It still passes, and that is the problem.** The test asserts that the common prefix covers everything up to the volatile layer; a token counter inside the *environment* layer sits **before** that cut, so divergence happens early and the `len(comum) >= corte` assertion fails — provided the value changes between the two assemblies. If the counter is the same on both turns of the test, and in a synthetic test it usually is, the prefix stays identical and the test passes, while in production it breaks every turn. That is this verification's honest limitation: it proves stability **for the variations the test provokes**, not for all of them. The defense is the same as in ch. 11: a test measures what someone decided to vary, and that is why the assertion prints the divergence offset — so the investigation is cheap when the bill, rather than the test, raises the alarm.
