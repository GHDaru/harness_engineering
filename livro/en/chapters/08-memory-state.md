<!-- i18n fonte:livro/capitulos/08-memoria-estado.md edicao:0.83 hash:bfeeaa6f -->
# 08 — Memory and State

> **State of the art captured in 2026-07** · last revised 2026-08-12 · [history and expiration log](../historico.html)
>
> Didactic layer v4 — see [Editorial Guide §2.1](../editorial-guide.md).
> scaffold: completo
>
> Skeleton v3 — body with the state of the art; per-repository treatment in Appendix A (online supplement).

## Learning objectives

By the end of this chapter, you should be able to:
1. **Distinguish** the problem's three layers, session state, long-term memory and workspace state, and the requirement specific to each;
2. **Explain** why memory is **not** RAG (Retrieval-Augmented Generation), and why versionable markdown beat vector databases in the coding domain;
3. **Derive** a recall policy from the recency × importance × relevance formula, and a forgetting policy from usage;
4. **Assess** the impact of **reversibility** on the risk calculus of permissions;
5. **Implement** harness-zero's session persistence (SQLite adapter plus `/resume`) in step 4.

## Forty minutes, nine files, and the terminal that closed

The agent worked for forty minutes. It edited nine files, ran the suite three times, found that the bug was in two places and fixed both. You went for coffee.

When you came back, the terminal had closed. System update, dropped SSH session, take your pick.

You run `--resume`. And it works: the conversation comes back whole, with the tool calls, the results, the reasoning. Relief.

Then you run `git status`.

```text
modified:   auth.py
modified:   session.py
modified:   tests/test_login.py
Untracked:  auth.py.orig
```

Three files modified **mid-edit**, and no clue which state was the good one. The conversation was restored; the **workspace** was not. And worse: the restored conversation says the work is finished, because from its point of view it is.

Notice that two different things had to survive the same accident, and only one did. That is what this chapter separates: **session state** and **workspace state** are two problems, with two owners and two undo trails.

## The problem

The model forgets everything between calls; the harness remembers for it.

"Memory and state" covers three layers with different requirements.

**Session state** is the conversation itself: messages, tool calls, metadata. It has to survive restarts and allow resuming, branching and reverting.

**Long-term memory** is facts that cross sessions: user preferences, project decisions, lessons learned. It has to be **selectable**, because not everything belongs in every context, and **updatable**, because facts change.

**Workspace state** is what the agent *did* to the files. It has to be **reversible**: undoing an agent's changes matters as much as making them. It is the layer that was missing in the opening scene.

The thesis that unifies the three: the context window is volatile, expensive memory, everything that has to last lives **outside** it, and the harness decides what to bring back and when.

## Scientific foundations

Agent memory has a mature literature, and it supplies the exact vocabulary for what harnesses do in practice.

- **The window as RAM.** [MemGPT: LLMs as Operating Systems, arXiv 2310.08560](https://arxiv.org/abs/2310.08560) treats context as scarce main memory, backed by two external levels (*recall* of recent history and searchable *archival*), with the **agent** paging data through tool calls. What to evict and what to fetch is decided by the agent, not by a fixed pipeline.
- **The canonical taxonomy.** [CoALA, arXiv 2309.02427](https://arxiv.org/abs/2309.02427) separates **episodic** memory (past experience), **semantic** (knowledge of the world or the user) and **procedural** (skills and code), plus working memory. At write time, decide *what kind* of memory that fact is, because each kind is retrieved differently. The [memory mechanisms survey, arXiv 2404.13501](https://arxiv.org/abs/2404.13501) organizes the subsystem by sources, forms and operations — budget effort per operation, not only for the search index.
- **The recall formula.** [Generative Agents, arXiv 2304.03442](https://arxiv.org/abs/2304.03442) stores observations in a dated *memory stream* and retrieves by a score combining **recency × importance × relevance**, with exponential recency decay, importance scored by an LLM (Large Language Model) and relevance by embedding. It is the concrete formula a harness should implement, and it introduces **consolidation by reflection**: synthesizing higher-level reflections from clusters of observations.
- **Controlled forgetting.** [MemoryBank, arXiv 2305.10250](https://arxiv.org/abs/2305.10250) decays or reinforces each memory's strength along an Ebbinghaus curve, crossing elapsed time with access frequency. Unused memory is a pruning candidate, and usage tracking is what closes the loop.
- **Memory as learning.** [Reflexion, arXiv 2303.11366](https://arxiv.org/abs/2303.11366) converts outcome feedback into verbal self-reflection, persisted in an episodic buffer and re-injected on the next attempt: improving without updating weights. Recent architectures ([A-MEM, arXiv 2502.12110](https://arxiv.org/abs/2502.12110); [Mem0, arXiv 2504.19413](https://arxiv.org/abs/2504.19413)) treat writing as a pipeline of extracting, consolidating and linking, with the memory network self-organizing. It is the bridge to ch. 16.

(Full bibliography and pointers: `livro/bibliografia.md`.)

## Industry sources

- **Session as a durable event log.** [Manage sessions](https://code.claude.com/docs/en/sessions): each session is continuously written to disk as **JSONL** per project, one line per message, tool use or metadata. "Resuming" is **restoring complete state** — tool calls, results, permission mode, active goal — not replaying text. The harness owns a private durable log, not a stable public schema.
- **Workspace reversal as a separate trail.** [Checkpointing](https://code.claude.com/docs/en/checkpointing) captures the code state before each prompt, and `/rewind` restores code, conversation **or** both. The [Agent SDK file-checkpointing](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing) exposes it as a reusable primitive. Undoing the *code* is a separate store from undoing the *conversation*, joined by the prompt index. It is the direct answer to the opening scene.
- **Durable memory as files with precedence.** [How Claude remembers your project](https://code.claude.com/docs/en/memory): a hierarchy of markdown files with declared precedence, a `#` shortcut to append a line of memory, and `/memory` to edit. Cross-session memory is **markdown in precedence tiers**, versionable, auditable and scoped, re-read at launch as always-on context.
- **The memory tool and "assume interruption".** [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool): the model requests operations (`view`, `create`, `str_replace`) in a `/memories` directory that persists across conversations, but execution is **client-side** — your app implements the storage, and with it the protection against path traversal, the size limits and the expiry. The system injects the instruction to assume the window may be reset at any moment. Paired with [context management](https://www.anthropic.com/news/context-management), it gives two levels: short-term hygiene inside the window and an external long-term store outside it. The pattern from the [long-running harnesses essay](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) is the same: a structured progress log, read at the start and updated at the end of every session.
- **Memory is not RAG.** The distinction became an industry thesis. RAG is *stateless* reading; memory is reading **plus a write path plus state management**: admission, resolution of conflicting facts, invalidation. Products expose self-editable blocks with core, recall and archival tiers; route each fact to a tier with its own lifetime; model memory as a **bi-temporal graph**, where an outdated fact is *invalidated* rather than deleted; and separate short-term per thread from long-term per namespace ([AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-ltm-rag.html); [mem0](https://docs.mem0.ai/core-concepts/memory-types)). You cannot "buy" memory by bolting on a vector store: you need a pipeline for writing, updating and invalidating.
- **See also**: the living collection [Awesome Harness Engineering — Memory & State](https://github.com/GHDaru/awesome-harness-engineering#memory--state) gathers more resources for this dimension, curated by problem.

## In practice: the port that separates the ephemeral from the durable

harness-zero so far keeps the conversation in an in-memory list. Close the process and it is gone. Step 4 introduces the book's third port, and it has three methods:

```python
class StorePort(Protocol):
    def append(self, session_id: str, msg: Message) -> None: ...
    def history(self, session_id: str) -> list[Message]: ...
    def sessions(self) -> list[dict]: ...
```

Notice what is **not** here. There is no `save_everything()`, no `flush()`, no explicit transaction. The contract is **append-only**: each message is written when it happens, and the history is derived by reading. That choice is the whole chapter in three lines — the durable thing is a log, and state is a **projection** of it.

The in-memory adapter serves as contrast, and exists so the reader sees the port working before trusting it:

```python
class StoreEmMemoria:
    def __init__(self) -> None:
        self._por_sessao: dict[str, list[Message]] = {}

    def append(self, session_id, msg):
        self._por_sessao.setdefault(session_id, []).append(msg)

    def history(self, session_id):
        return list(self._por_sessao.get(session_id, []))
```

Correct, fast and useless for the opening problem. Swapping in SQLite changes no line of the loop:

```python
class StoreSQLite:
    def __init__(self, caminho="sessoes.db"):
        self._db = sqlite3.connect(caminho, check_same_thread=False)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS mensagens (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                papel      TEXT NOT NULL,
                conteudo   TEXT NOT NULL,
                criado_em  TEXT NOT NULL DEFAULT (datetime('now'))
            )""")
        self._db.execute("CREATE INDEX IF NOT EXISTS ix_sessao ON mensagens(session_id, id)")

    def append(self, session_id, msg):
        self._db.execute(
            "INSERT INTO mensagens (session_id, papel, conteudo) VALUES (?,?,?)",
            (session_id, msg.papel, json.dumps(msg.conteudo)))
        self._db.commit()          # commit per message: durability > throughput
```

The per-message `commit()` is the decision the opening scene justifies. It is slow in a benchmark and right in an incident: whatever is written **is** written when the power goes.

And now the part that closes the scene. Persisting the conversation does **not** persist the workspace, and the second trail is of another nature:

```python
def checkpoint(projeto: Path, rotulo: str) -> str:
    """Workspace snapshot before each turn, outside the user's own git history."""
    subprocess.run(["git", "add", "-A"], cwd=projeto, check=True)
    sha = subprocess.run(["git", "stash", "create"], cwd=projeto,
                         capture_output=True, text=True).stdout.strip()
    if sha:                                     # empty when nothing changed
        subprocess.run(["git", "update-ref", f"refs/harness/{rotulo}", sha], cwd=projeto)
    return sha
```

Three details are worth reading. `stash create` does **not** touch the user's index or working tree: it only produces an object. `update-ref` stores that object under `refs/harness/`, outside `refs/heads/`, so no `git log` or `git branch` of the user's gets polluted. And the empty return when nothing changed avoids creating a checkpoint for a turn that only talked.

Two trails, two stores, one shared index — the turn number. That is what lets `/rewind` restore **code, conversation or both**, the primitive the state of the art has consolidated.

## The state of the art

### 1. Three layers, three champions, and no vector database

The three layers got different champions in the cohort. **Session state** was solved with database durability: replayable events, per-turn rollout, event stream. **Long-term memory** was solved with relevance and format rigor: a versioned memory directory, with separate modules for relevance and usage. **Workspace state** was solved with git.

And the finding that persists: **none of the coding harnesses uses a vector database** for memory.

In the coding domain, versionable markdown beat embeddings. The reason is exactly what the "memory is not RAG" thesis predicts: code memory needs a *write path*, because the agent edits the file, and auditability, because someone will want to know why it believes that.

### 2. The recall formula and forgetting moved from paper to code

One harness in the corpus has both sides implemented in separate files: one selects by relevance what enters the context, the other marks usage, and unused memory becomes a pruning candidate. It is the forgetting curve in practice.

Another formalizes **active maintenance**: a single tool edits the memory files, with periodic nudges every ten turns, and a text search over the session database provides **cross-session recall**. It is MemGPT's archival tier built on text search, not vector search.

### 3. Reversibility became a primitive, and it changes the risk calculus

Workspace checkpointing stopped being a feature and became a primitive. One harness pioneered it years ago, with git-native state and an atomic commit per round; another established the snapshot-restore command; and the most mature in the corpus exposes separate trails for code and conversation, as in the example above.

The design consequence is the chapter's most interesting: **an agent whose actions are reversible changes the risk calculus of everything else**. Permissions can be looser when undoing is cheap, which links this dimension directly to ch. 07.

### 4. Pluggable providers, and the harness as a memory server

The emerging frontier is memory as a pluggable service, with harnesses accepting external providers behind their own layer and products positioning themselves as a universal layer consumable by any harness.

The design tension for the coming rounds: keep memory as a **versionable local file**, auditable and portable, or outsource it to a managed store, with a bi-temporal graph and scale. In code, the file still wins; outside it, the pendulum is less clear.

### Executive summary

What is most modern: the operating-system tier framing, with the agent paging between window, recall and archival; recall by recency, importance and relevance, with forgetting by usage; workspace reversal as a primitive that loosens permissions; and the hard distinction between memory and RAG.

**What to steal:**

- **Persist the session as an append-only log**, and derive state by reading it. Resuming is restoring state, not replaying text.
- **Treat memory as versionable markdown** with usage tracking.
- **Separate the code undo trail from the conversation trail**, joined by the turn index.
- **Store the checkpoint outside `refs/heads/`**, so as not to pollute the history of whoever uses the repository.
- **For long-running agents, write a durable progress log** assuming the window disappears at any moment.

## Hands-on — harness-zero, step 4

Step 4 (`harness-zero/etapas/04-sessoes/`) gives harness-zero persistence: the `StorePort` from the example above, with a SQLite adapter storing messages and tool calls as typed rows, and `/resume` restoring the complete state of a previous session.

It is faithful to hexagonal *by refactoring*: the pain that makes the port necessary is reopening the process and losing the conversation, and it only appears after it hurts.

Completion exercise: persistence covers the happy path. You add a minimal memory file, read at the start, and a progress log updated at the end — the "assume interruption" pattern in its simplest form.

## Check your understanding

1. Why is agent memory not the same thing as RAG, and what does that explain about the choice of versionable markdown over a vector database in coding harnesses?
2. You have 10,000 memories and room for 20 in the context. What score do you use to choose, and how do you decide what to prune over time?
3. Your agent gained workspace checkpointing. What decision *from another dimension* does that let you loosen, and why?
4. In the example, why is the checkpoint stored in `refs/harness/` rather than as a commit on a branch?

---

## Appendix A — How each repository handles memory and state

> Per-harness evidence, with paths — online supplement, expanded each round.

### opencode (round 1) — state as a database
Persistence in **SQLite via Drizzle** (`packages/core/database`, `core/session/sql.ts`): sessions, messages and parts are typed rows. Sessions have a `parentID` (hierarchy for subagents), support revert (`session/revert.ts`) and **sharing** (`share/`, `sync/`). V2 (`CONTEXT.md`) takes the design to "data infrastructure": a durable prompt inbox, replayable events with cursors (`sessions.events({sessionID, after})`), context snapshots persisted across restarts. Round 1's most robust state model — the harness as a distributed system with durable state.

### gemini-cli (round 1) — the reversible workspace
Long-term memory in the `GEMINI.md` files themselves (`save_memory` tool, global in `~/.gemini` + project index, with auto-memory tested in evals). The distinctive feature is **git-based checkpointing** (`services/gitService.ts` + `chatRecordingService.ts`): workspace snapshots before edits, enabling `/restore` and `/rewind` — undoing the agent's changes on disk, not just in the conversation — plus `/resume`.

### OpenHarness (round 1) — memory as files, with discipline
`src/openharness/memory/` (13 modules): persistent memory in markdown (`MEMORY.md`/per-project memdir) with **versioned schema, atomic file-locked writes and signatures**. `relevance.py` selects what enters the context; `usage.py` marks usage (unused memory is a pruning candidate). Sessions persisted with rich metadata (`services/session_storage.py`): permission mode, read-file state, invoked skills, compaction checkpoints. Resume via `-c/--continue`, `-r/--resume`, `/resume`.

### Aider (round 2) ⭐ git-native state — the reversal pioneer
`aider/repo.py`: **atomic auto-commit per round** with an LLM-generated message, configurable authorship attribution, `aider_commit_hashes` tracking what the AI did, `dirty_commit` isolating pending changes. `/undo`, `diff` and `blame` become the memory interface; complemented by `.aider.chat.history.md` and `--restore-chat-history`. **Anticipated by years** the "git checkpoint" that gemini-cli and Claude Code consecrated.

### Hermes (round 2) ⭐ multi-layer memory with cross-session recall
`MEMORY.md` (agent notes) + `USER.md` (user profile) edited by a single tool with **periodic nudges** (every 10 turns); pluggable external providers (**Honcho, mem0, supermemory**); and **`session_search`** — an FTS5 index over the session SQLite with three modes (discovery/BM25, windowed recall, LLM summarization) for cross-session recall. MemGPT's archival layer on textual search.

### Codex CLI (round 2) — per-turn rollout jsonl
Each turn is persisted as **rollout jsonl** (recoverable); `SessionTask` (Regular/Review/Compact/UserShell) organizes the task machine. Durable, resumable session state integrated into the loop (`core/src/session/`).

### OpenHands (round 2) — persisted event-stream
`openhands/app_server/event/` persists each `Event` as JSON per conversation, with pagination, filters and trajectory export. The control plane consumes/persists events; the action-observation loop runs in the SDK. Event sourcing as the state's backbone.

### OpenClaw (round 2) — session lanes and workspace files
Runs serialized per *session lane* with a file-based write-lock between processes; workspace files (`MEMORY.md`, `USER.md`, `IDENTITY.md`…) injected with budgets (20k chars/file, 60k total) and marked truncation. Per-channel conversation persistence.

### ohmo (round 2) — session/memory backends as plugins
Implements OpenHarness's `SessionBackend` and `MemoryCommandBackend` as first-class plugins (without touching the core), plus a **multi-session pool** (`RuntimeBundle` per `session_key`, recreated when the cwd changes). Proof that the app/engine boundary was designed.

### IronClaw (round 2) — resumable state via checkpoints
Resumable state via **checkpoints**; a Queued→Running→Blocked→Completed state machine with **leases/heartbeats** and "one active run per canonical thread". The `LoopExit` carries only durable references — the loop never mutates state; the `LoopExitApplier` validates host-owned evidence before applying.

### n8n (round 2) — the workflow engine's memory
Memory via *memory sub-nodes* (`contextWindowLength` window, `maxTokensFromMemory` cutoff); workflow state persisted by the engine across executions. Short by nature — event-triggered executions do not accumulate long context (compaction score 1, by design).

### Frameworks (frameworks round)
LangGraph: **checkpointer** (short-term, thread-scoped) + per-namespace **store** (long-term cross-thread); LangMem: semantic/episodic/procedural memories as tools; Agents SDK and CrewAI: session/short-term state with persistence hooks. The short × long term distinction is a framework primitive — what the code harnesses implement by hand, the frameworks expose as an API.

---

## Verification answers

**1.** Because RAG is **stateless reading**: a query retrieves passages and injects them into the context, and nothing the agent concludes goes back into the index. Memory is reading **plus a write path plus state management** — admission of what deserves remembering, resolution of facts that contradict each other, and invalidation of what stopped being true. In the coding domain that explains the choice of versionable markdown: the agent **edits** the memory file, the diff shows what it came to believe and when, and `git blame` answers why. A vector database gives retrieval and none of the three: writing to it means reindexing, and nobody can audit what changed.

**2.** The score is **recency × importance × relevance**: recency with exponential decay, importance scored once at write time, relevance computed against the current task. All three are necessary because each alone fails in a known way — recency alone forgets what is permanent, importance alone always brings the same twenty, relevance alone brings what matches by word rather than by usefulness. Pruning is by **lack of use**, not by age: record access, let strength decay over time and reinforce on each read. An old memory consulted weekly is worth more than a recent one nobody opened, and the forgetting curve is exactly what encodes that.

**3.** It lets you loosen **permissions** (ch. 07). The cost of a wrong decision is the product of two things: the probability of it happening and the cost of reverting. When reverting becomes one command, the second drops near zero for the whole class of actions that only touch project files, and insisting on human approval for each of them spends attention where there is no longer proportional risk. The caveat that blocks the lazy reading: this holds **only** for effects the checkpoint reaches. Network, production database, email sent and key published do not come back with `/rewind`, and for those the calculus has not changed at all.

**4.** For three reasons, and the third is the decisive one. First, **not polluting**: refs under `refs/heads/` show up in `git branch`, in `git log --all` and in completion, and the user would end up living with dozens of branches that are not theirs. Second, **not interfering**: `stash create` produces the object without touching the index or the working tree, so the agent can snapshot in the middle of a user's `rebase` without ruining it. Third, and decisive: `refs/harness/` is a **harness namespace**, which makes cleanup trivial and safe — deleting everything under it never deletes anyone's work. Storing tool state in the user's namespace is the same class of mistake as writing cache inside the source directory.
