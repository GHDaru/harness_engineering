<!-- i18n fonte:livro/capitulos/04-compactacao.md edicao:0.88 hash:ff70d88a -->
# 04 — Compaction

> **State of the art captured in 2026-07** · last revised 2026-08-12 · [history and expiration log](../historico.html)
>
> Didactic layer v4 — see [Editorial Guide §2.1](../editorial-guide.md).
> scaffold: completo
>
> **Pilot chapter of skeleton v3** — body with the state of the art; per-repository treatment in Appendix A (online supplement, updated with each benchmark round).

## Learning objectives

By the end of this chapter, you should be able to:
1. **Explain** why compaction exists and which constraints it balances (fidelity × cost × cache);
2. **Compare** the four layers of the aggressiveness ladder and **justify** their ordering;
3. **Analyze** a real harness's compaction implementation and locate its choices on the ladder (Appendix A as the answer key);
4. **Implement** truncation with edge preservation and summarization with a preserved tail (step 5 of harness-zero);
5. **Evaluate** when a compaction has failed (loss of a decision, of file state or of the goal) — and **anticipate** what changes when the provider compacts for you.

## The agent that undid its own fix

Turn 38. The agent has found the bug, edited `auth.py`, run the test and watched it pass. Two neighboring files to adjust and it is done.

Turn 40. The window fills up. The harness compacts: it summarizes the previous 39 turns into half a page and carries on.

Turn 41. The agent opens `auth.py`, looks, and **undoes the fix**. It rewrites the function back to the earlier version, runs the test, watches it fail, and starts investigating the bug it had already solved.

The summary said, in all honesty: *"edited auth.py to fix the expired cookie"*. That is correct. What it did not say was **how the file looked after the edit** — and the model, without that, did what anyone would do: it went to check, read code it did not recognize as its own, and "fixed" it.

Compaction did not lose the conversation. It lost the **state**. And the worst part is that it had no way of knowing: a free-prose summary has no mandatory field for "current situation of the files".

This chapter is about what gets thrown away when everything no longer fits, and about why the order in which you throw things away matters more than the compression ratio.

## The problem

Every agent conversation grows until it no longer fits in the model's context window. Compaction is the set of strategies for continuing to work when that happens — without losing what matters. It is the dimension where the evaluated harnesses converge the most: all of them arrived, independently, at the same layered architecture.

The constraints in tension:
- **Fidelity**: the summary cannot lose decisions, file state or the task's goal.
- **Cost**: summarizing via LLM (Large Language Model) is expensive; truncating is cheap but destructive.
- **Cache**: compacting invalidates the cached prefix — it should happen as little as possible and at controlled moments.

## Scientific foundations

- **The window is not uniform**. *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)) showed that models use the beginning and end of the context best and degrade in the middle. It is the empirical basis for two of the ladder's practices: preserving the recent *tail* intact and truncating outputs while keeping start+end.
- **Context as virtual memory**. *MemGPT* ([arXiv 2310.08560](https://arxiv.org/abs/2310.08560)) framed the operating-systems analogy: the window is "RAM", external storage is "disk", and the harness pages between them. Recent work takes the analogy to its literal limit (*demand paging*, [arXiv 2603.09023](https://arxiv.org/abs/2603.09023)).
- **Compacting is a budget decision**. *ContextBudget* ([arXiv 2604.01664](https://arxiv.org/abs/2604.01664)) treats context management as explicit allocation per content type — what products implement as thresholds and budgets.

(Full bibliography and validation status: `livro/bibliografia.md`.)

## Industry sources

- **[Compaction — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/compaction)** (Anthropic, official): compaction has reached **the API level** (beta `compact-2026-01-12`) — the provider summarizes automatically upon hitting the configured threshold and returns a "compaction block". It is vendor confirmation of this chapter's central trend (see The state of the art).
- **Claude Code operating practices** ([CometAPI](https://www.cometapi.com/what-is-auto-compact-in-claude-code/), [okhlopkov](https://okhlopkov.com/claude-code-compaction-explained/), [hyperdev](https://hyperdev.matsuoka.com/p/how-claude-code-got-better-by-protecting)): the practitioners' convergent recommendation is the same one the harnesses encode — **what needs to survive compaction should not live in the conversation**: conventions go to the context file (CLAUDE.md/AGENTS.md, reinjected every session) and progress state goes to files the agent rereads after the compact. Compaction defines, by exclusion, what deserves persistence.
- **See also**: the living collection [Awesome Harness Engineering — Context Delivery & Compaction](https://github.com/GHDaru/awesome-harness-engineering#context-delivery--compaction) gathers more resources for this dimension (patterns, articles and implementations), curated by problem.

## In practice: the ladder, with the numbers on each rung

The aggressiveness ladder is a sequence of attempts, from cheapest to most expensive, and each rung only runs if the previous one was not enough. Written out, it fits in one function:

```python
ORCAMENTO = 100_000        # tokens the model may see

def compactar(historico: list[Message]) -> list[Message]:
    """Returns the VIEW sent to the model. The persisted record does not change."""
    v = truncar_saidas(historico)          # 1. cheap, local, no LLM
    if custa(v) <= ORCAMENTO:
        return v

    v = podar_resultados_antigos(v)        # 2. cheap, drops old content
    if custa(v) <= ORCAMENTO:
        return v

    return sumarizar(v)                    # 3. expensive: one LLM call
```

The first two rungs cost microseconds; the third costs a model call and a few seconds. That alone would justify the order. But there is a better reason, and it is **destructiveness**.

```python
def truncar_saidas(h, teto=4_000):
    """Cuts the tool output keeping both edges: the head says what it is,
    the tail says how it ended. The middle of a log rarely decides anything."""
    out = []
    for m in h:
        if m.papel == "tool" and len(m.conteudo) > teto:
            cabeca, cauda = m.conteudo[: teto // 2], m.conteudo[-teto // 2 :]
            ref = arquivar(m.conteudo)     # the full text goes to disk, not to the bin
            m = m.com(conteudo=f"{cabeca}\n… [{ref}] …\n{cauda}")
        out.append(m)
    return out
```

Note the `arquivar`. The modern refinement of rung 1 is **not discarding**, rather than cutting better: the full content goes to a referenceable file, and the model can ask for it back if it needs to. Truncation stops being loss and becomes pagination.

The third rung is where the opening scene happens, and it is where the shape of the summary decides everything:

```python
def sumarizar(h, cauda=8):
    antigos, recentes = h[:-cauda], h[-cauda:]     # the tail goes through intact
    resumo = llm.completar(
        PROMPT_DE_RESUMO, antigos,
        formato={                                   # MANDATORY fields
            "objetivo_do_usuario": str,             # why we are here
            "decisoes": list[str],                  # what has been decided
            "estado_dos_arquivos": dict[str, str],  # ← what turn 40 lacked
            "pendencias": list[str],                # what is left to do
        })
    return [Message("system", render(resumo)), *recentes]
```

`estado_dos_arquivos` is the difference between the summary that saves and the summary that sabotages. A free-prose summary writes *"edited auth.py"*; a summary with a mandatory field is forced to write *"auth.py: `max_age` corrected to 3600, test passing"*. The first is true and does not stop the agent from undoing it; the second does.

The intact tail has the same nature. The last turns go through **unsummarized**, because they hold the work in progress, and summarizing what is happening right now is the fastest way to lose the thread.

And the invariant running across all three rungs is in the first function's comment: compaction changes the **view** sent to the model, **never** the persisted record from ch. 08. Whoever confuses the two discovers, at the first incident, that they compacted the only copy.

## The state of the art

### The consolidated pattern: the aggressiveness ladder

Harnesses apply the strategies as a ladder, from cheapest to most expensive — this is the industry consensus, verified in every benchmark round:

1. **Truncate tool outputs at the source**: limit lines/bytes before they enter the history, preserving start and end (*Lost in the Middle* justifies the edges). The modern refinement: **do not discard** — move the full content to referenceable files (opencode) or keep the raw output outside the model's view but visible in the UI (Goose).
2. **Prune / microcompact**: erase the *content* of old tool results (the model rarely rereads a `cat` from 30 turns ago), keeping the record of the call. Newer intermediate layers: *tool distillation* and *output masking* (gemini-cli).
3. **LLM summarization (full compact)**: summarize the old portion while preserving an intact tail (typically 20–30% or a 2k–20k token budget). The state of the art has three refinements: a **structured summary** with mandatory fields (user intent, pending tasks, code state — Goose and software-agent-sdk), a **cheap auxiliary model** for the summary (Hermes), and a **memory flush before compacting** — saving durable notes before losing the context (OpenClaw).
4. **Automatic trigger + reactive path**: a trigger by window percentage (50–90% depending on the project) and, covering the failure case, compaction **reactive** to the API's "prompt too long" error (OpenHarness, OpenClaw).

### The two modern frontiers

**1. Auditable compaction, with tombstones.** The most advanced implementation measured in the benchmark does not mutate the history. The log is append-only and forgetting is an **event**, a tombstone in the same sense distributed databases give the word.

The model's view is derived by applying the tombstones. Nothing is lost for audit, and the formal invariants become **testable code**: pairing between call and result, batch atomicity.

From that comes a distinction worth stealing, between a **soft** and a **hard** trigger. If compacting now would violate an invariant, the soft trigger waits for the next turn; the hard one forces an explicit reset. A related refinement is the **effectiveness circuit-breaker**: compare size before and after and give up on the compaction that did not compact.

**2. Compaction is migrating to the provider.** The cache also became a protocol contract: the MCP 2026-07-28 spec added `ttlMs` and `cacheScope` to `tools/list` responses, with the protocol taking over what used to be harness heuristics.

There are two independent signals in the same year. One harness in the corpus implements **remote compaction**, with the backend compacting; and compaction appeared as a feature of the **API itself** ([docs](https://platform.claude.com/docs/en/build-with-claude/compaction), beta `compact-2026-01-12`).

It is the expiration clause in motion, with an interesting inversion. Instead of the component disappearing as the model improves, it **changes owner**: it leaves the harness and goes to the platform.

What remains to the harness when the provider compacts is three concrete things. Deciding *what to protect*, such as skills, task state and memory files. Deciding *when to trust*, by auditing the summary's quality. And keeping the reactive path for when remote compaction fails.

> **Addendum (2026-07-31, full text verified): the third way, compaction learned in training.** The [CompactionRL](https://arxiv.org/abs/2607.05378) preprint (Tsinghua/Z.AI, 06-Jul-2026) proposes the next step of the migration: training the model by RL **with compaction inside the loop**.
>
> In the paper's words, *"CompactionRL incorporates compaction into rollout collection, and reconstructs the agent context from a summary once context budget is exhausted"* (§1), and summarization becomes *"a learned part of the model rather than an inference-time heuristic"*, with a **task**-level reward. The Table 2 numbers are always measured against the same model *already using inference-time compaction*, which is the honest comparison.
>
> If the line holds, compaction does not only change owner: it changes **layer**, from the harness to the weights.

### The third frontier: compaction stops being involuntary (round ext-4, 2026-08)

The launch of **Prime Agent** (Aug/2026) came with a direct accusation aimed at this chapter: *"fixed tool-calling schemas and context compaction force the model to work around its own scaffolding instead of leveraging it"*.

Reading the code ([full evaluation](../../../benchmark/avaliacoes/prime-agent.md)) shows that **the accusation is rhetorical and the code says otherwise**. The difference between the two is the finding.

Compaction was **neither eliminated nor weakened**. Prime Agent is built on Pi, and the 1,398 lines of `core/compaction/` are there intact, with safe cutting, turn splitting, cumulative files and reactive overflow recovery, further improved with custom instructions.

What changed is **who is in charge**. The compact and status functions (`skills/compact/`) became callable **by the agent itself**, with a handler that **schedules rather than executes**, because executing on the spot would abort the REPL cell that requested the compaction. And they run even with automatic compaction turned off, under twelve test cases.

The caveat to record is therefore precise: **compaction stops being an involuntary harness event and becomes one mechanism among others, available to the agent**. It also gains a new role, that of a distillation trigger: every compaction becomes an opportunity for the agent to extract learning from what is about to be summarized.

What the ladder did not foresee was the **inversion of control**, rather than its own obsolescence. Until now, the harness compacts *in* the agent; here, the agent compacts *itself*.

And the gap the reading found is revealing. The announcement mentions a subagent acting as the REPL's garbage collector, and **there is nothing of the sort in the code**: searching for `garbage`, `prune` and `evict` across the code directories returns nothing. Context-as-a-variable solves access to the past; it does **not** solve the growth of the namespace it creates.

### Executive summary

Convergence on the ladder is nearly total. The pattern is consolidated, and a new harness that does not implement it needs to justify itself.

The differences that remain are fidelity refinements: structuring the summary, auditing its quality, never discarding. And the big open question is one of **market architecture**: how much of the ladder survives in the harness when the platform offers compaction as a service. The addendum above sharpens the question, because after migrating to the provider, compaction starts migrating to the **weights**.

**What to steal:**

- **Tombstones over an append-only log**, with the view derived and nothing lost for audit.
- **Memory flush before compacting**: save the durable notes while the context still exists.
- **A structured summary** with mandatory fields, above all the state of the files.
- **An effectiveness circuit-breaker**: if compacting did not shrink anything, compacting again will not either.
- **An intact tail**, because work in progress does not survive a summary.

> **Editorial caveat (2026-08-06).** This Executive summary was confronted in round ext-4 and **upheld**, with the qualification from the previous section: the ladder is still the pattern, but *authority* over when to apply it has started migrating to the agent. If the pattern repeats in other harnesses, the synthesis changes, and this paragraph will be rewritten, not amended.

## Hands-on — harness-zero, step 5

In step 5 of the `harness-zero/` project (`harness-zero/etapas/05-compactacao/`) you implement the ladder from the "In practice" section in your own harness, in this order:

1. tool output truncation preserving head and tail;
2. pruning of old tool results, beyond a budget;
3. LLM summarization of the head of the history, preserving the tail;
4. automatic triggering by an estimated-token threshold.

Add a **visible indicator in the chat** when compaction happens: it is the reader's observation window, and without it compaction is invisible exactly when understanding it matters most.

Completion exercise: the skeleton of the prune function ships ready. You write the selection of what to protect.

## Check your understanding

1. Why truncate tool outputs **before** summarizing via LLM, and not the other way around?
2. A harness summarized the history and the agent, on the next turn, rewrote a file that was already correct. What information did the compaction probably lose, and which state-of-the-art mechanism prevents it?
3. Your provider now offers compaction in the API. Which of the ladder's responsibilities do you **transfer** and which do you **keep** in the harness?
4. Compaction runs for the second time in the same session. What class of defect only appears then, and why?
---

## Appendix A — How each repository handles compaction

> Per-harness evidence, with paths — supplementary material (online version), expanded with each benchmark round. The chapter's base source: the code of these repositories.

### opencode (round 1) — three mechanisms + managed files
`packages/opencode/src/session/compaction.ts` (+ `overflow.ts`, `summary.ts`): (a) automatic summarization on overflow with a **dedicated `compaction` agent**, tail under budget (`preserveRecentBudget`, 2k–8k tokens), a new Context Epoch and optional auto-continue; (b) back-to-front **prune** marking tool outputs beyond 40k tokens as `compacted` (`PRUNE_PROTECT`), protecting skills; (c) truncation at the source (`tool/truncate.ts`) preserving start+end and moving the full text to "Managed Tool Output Files".

### gemini-cli (round 1) — compression + distillation + masking
`packages/core/src/context/chatCompressionService.ts`: fires at 50% of the limit (`DEFAULT_COMPRESSION_TOKEN_THRESHOLD = 0.5`), preserves the last 30% (`COMPRESSION_PRESERVE_THRESHOLD`), its own budget for function responses (50k) and saving of truncated outputs. Extra layers: `toolDistillationService.ts` and `toolOutputMaskingService.ts`. Manual `/compress`, `ChatCompressed` event, `PreCompressTrigger` hooks.

### OpenHarness (round 1) — the faithful translation of Claude Code
`src/openharness/services/compact/__init__.py` (1,725 lines; docstring: "Faithfully translated from Claude Code's compaction system"): **microcompact** (clears `COMPACTABLE_TOOLS`), **full compact** (LLM summary), **auto-compact** (threshold) and compaction **reactive** to "prompt too long" (`_is_prompt_too_long_error`). `PRE_COMPACT`/`POST_COMPACT` hooks; preserves task state and channel logs.

### Codex CLI (round 2) — local + remote v1/v2
`core/src/compact.rs`, `compact_remote_v2.rs`, `compact_token_budget.rs`: auto-compact at ~90% of the window; three strategies — local (`SUMMARIZATION_PROMPT`) and **remote v1/v2** (the backend compacts, via `ResponsesStreamRequest::RemoteCompactionV2`, with its own retry); versioned windows with prefill tracking; controlled pre/mid-turn injection; `TruncationPolicy` for outputs.

### Goose (round 2) — structured summary + middle-out
`crates/goose/src/context_mgmt/mod.rs`: threshold at 0.8 of the window; `StructuredSummary` (user_intent, files, pending_tasks, current_work); if summarization overflows, **progressive "middle-out" removal** of tool-responses (0→100%); **incremental summarization of tool-call/response pairs** in batches of 10 protecting the last N; visibility metadata preserves the raw output in the UI; respects `provider.manages_own_context()`.

### OpenClaw (round 2) — safeguard + memory flush
`src/context-engine/` + `docs/concepts/compaction.md`: automatic by threshold and reactive (recognizes dozens of overflow error strings from multiple providers), split preserving tool-call/result pairs; `safeguard` mode with **summary quality auditing**; **silent memory flush before compacting**; `keepRecentTokens` 20k; pluggable compaction providers; the compaction (semantic) × pruning (in-memory trim) distinction.

### Hermes (round 2) — pluggable engine + auxiliary model
`agent/context_engine.py` (interface `should_compact`/`compress`/`prune`) + `trajectory_compressor.py` (~1.6k lines): summarization of old tool-responses via a **cheap auxiliary model** (default Gemini Flash, up to 50 concurrent requests); manual `/compress`; `/usage` and `/insights` expose the window.

### IronClaw (round 2) — pure policy + circuit-breaker
`crates/ironclaw_agent_loop/src/strategies/compaction.rs` (+ `active_task_compaction.rs`): the strategy is **pure policy** (returns Skip or the `drop_through_seq` limit; mutation only in the host); `PromptContextTokenBudget` with `preserve_tail_tokens`; an **effectiveness circuit-breaker** (compares the post-compaction estimate against `CompactionEffectivenessBaseline`); a variant that preserves the active task; the host refuses to compact through non-user messages.

### software-agent-sdk (frameworks round) — tombstones + testable invariants ⭐
`openhands-sdk/openhands/sdk/context/condenser/`: forgetting via **tombstones** (`Condensation` event) over an append-only log; triggering for three reasons (REQUEST/TOKENS/EVENTS) with **hard/soft** (`condensation_requirement`) and `hard_context_reset()` for the pathological case; `keep_first` + recursive re-summarization of summaries; a structured prompt (`summarizing_prompt.j2`: USER_CONTEXT, TASK_TRACKING with exact IDs, CODE_STATE, TESTS, CHANGES); invariants in `context/view/properties/` (tool_call_matching, batch_atomicity...) **tested against real LLMs** (`tests/integration/tests/c01..c05`); `pipeline_condenser` for composition.

### Aider (round 2) — classic summarization done well
`aider/history.py` (`ChatSummary`): keeps the tail (~half the budget), summarizes the head via LLM with a split after an `assistant` message, **recursive** up to depth 3, with a fallback model list.

### n8n (round 2) — the absence that confirms the category
No compaction in the loop (the memory sub-nodes' `contextWindowLength` + `maxTokensFromMemory` only) — consistent with short, event-triggered executions; it is the "embedded harness" category's ceiling for long tasks.

### LangGraph / OpenAI Agents SDK / CrewAI (frameworks round) — the dividing line
LangGraph: **zero native support** (a docstring suggesting `pre_model_hook`); Agents SDK (Software Development Kit): only `OpenAIResponsesCompactionSession` as an optional session; CrewAI: nothing. Compaction is the dimension that most separates "framework" from "ready-made harness".

---

## Verification answers

**1.** For cost and for destructiveness, and the second reason is the decisive one. Truncating is local, calls no model, and in its modern refinement **loses nothing**: the full content goes to a referenceable file. Summarizing costs an LLM call, takes seconds and is **irreversible in the view** — whatever the summary did not capture does not come back. Running the expensive rung before the cheap one means paying more to lose more, and on top of that summarizing megabytes of tool output that truncation would have removed for free. The ladder is ordered by increasing damage, and cost merely follows.

**2.** Compaction lost the **state of the files**: it recorded that an edit happened and not how the file ended up. It is the worst thing a free-prose summary does, because the sentence *"edited auth.py"* is true and useless. The state-of-the-art mechanism that prevents it is the **structured summary with mandatory fields**, forcing the model to fill in the current state of the code, the decisions taken and the pending items. A mandatory field cannot be dropped for the sake of elegant prose. The complementary defense is the **intact tail**: the last turns go through unsummarized, and they are where the work in progress is described precisely.

**3.** You transfer the **expensive** rung: summarization, where the provider has a real advantage, because it sees the whole conversation on its side and can compact without an extra round trip. You keep the **cheap, local** rungs — truncating tool output at the source and pruning old results — because they depend on knowledge only the harness has: which outputs are from your tools, what has already been archived to disk, what your product's budget is. And above all you keep the **record invariant**: the provider compacts its view; the durable log is still yours, and it is what audit, resume and revert come from. Outsourcing compaction without keeping the record means being left without the only copy.

**4.** The class of defect is the **orphaned result**: a tool result whose corresponding call has already left the history. On the first compaction, call and result are usually in the same summarized block, and the pair stays coherent. On the second, the first pass's summary has already replaced part of the history, and the pairing can break: a result is left without its call, or a call without its result, and the model receives a history that is not even syntactically valid for the API. It is a dated, real case in the corpus, and it exposes what the chapter long failed to discuss: compaction is a **repeated** operation, and what breaks is not compacting, it is **compacting what was already compacted**.
