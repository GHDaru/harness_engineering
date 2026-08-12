<!-- i18n fonte:livro/capitulos/05-ferramentas.md edicao:0.82 hash:d90ed571 -->
# 05 — Tool Design

> **State of the art captured in 2026-07** · last revised 2026-08-12 · [history and expiration log](../historico.html)
>
> Didactic layer v4 — see [Editorial Guide §2.1](../editorial-guide.md).
> scaffold: completo
>
> Skeleton v3 — body with the state of the art; per-repository treatment in Appendix A (online supplement).

## Learning objectives

By the end of this chapter, you should be able to:
1. **Explain** why a tool's description is prompt engineering, not API documentation;
2. **Derive** a tool's schema from types, and justify why nobody writes JSON Schema by hand any more;
3. **Compare** the three scaling regimes: fixed catalog, tool search with deferred loading, and code-as-action;
4. **Implement** the harness-zero `ToolPort` with a derived schema and error-as-data (step 2);
5. **Assess** when to use individual tool calls and when to use code orchestrating tools in a sandbox.

## The parameter that was renamed, and nobody told the model

You wrote the search tool three months ago. The JSON Schema sits right above the function, written by hand, with the parameter named `padrao`. It has worked ever since.

Last week someone renamed the Python function's argument to `glob`, because `padrao` was vague. The tests passed: no test calls the function by argument name.

Today the agent is stuck. It reads the schema, complies perfectly, builds `{"padrao": "*.py"}`, and gets back `TypeError: buscar_arquivos() got an unexpected keyword argument 'padrao'`. It tries again. It tries a third time, now with different quoting, because the error does not say what is wrong. Twenty turns later you give up and go read the log.

The model did not get it wrong. **The tool's documentation and the tool diverged**, and nothing in the system had the duty to notice.

Keep the scene, because it is this chapter's whole argument: when the schema is written by hand, it is a second source of truth — and two sources of truth is one more than exists.

## The problem

Tools are the agent's hands: the contract through which the model acts on the world.

Tool design is deciding **which** ones exist, **how** their parameters are described to the model, **how** results and errors come back, and **when** each one is available.

Each of those decisions fails differently. A badly described tool produces wrong calls. Too large an arsenal dilutes the model's attention *and* blows the context budget before any useful work. Too small an arsenal forces workarounds through the shell.

## Scientific foundations

- **The evolution of tool use** — [arXiv 2603.22862](https://arxiv.org/abs/2603.22862) traces the trajectory from single-tool call to multi-tool orchestration, the backdrop of "code-as-action".
- **Tool learning as a field** — the tool learning survey ([repo](https://github.com/quchangle1/LLM-Tool-Survey)) organizes how agents learn to select and compose tools.

(Full bibliography: `livro/bibliografia.md`.)

## Industry sources

- **[Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)** (Anthropic Engineering): the canonical source. Tools are *"contracts between deterministic systems and non-deterministic agents"*; the description is prompt engineering, with small refinements yielding large accuracy gains; the return should be optimized for **information density per token**; and the cycle is *prototype → evaluate → collaborate*, with the model itself rewriting the tools from eval transcripts.
- **[Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)** (Anthropic): loading every definition and passing intermediates through the context is the bottleneck. Exposing each tool as a TypeScript file that the agent orchestrates via code took one case from **~150,000 to ~2,000 tokens (−98.7%)**.
- **[Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)** + **[Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)**: dynamic discovery. Send everything, mark the non-critical with `defer_loading: true`, and the model sees only the search plus the essentials. A multi-server setup spends ~55k tokens on definitions before doing any work, and tool search cuts that by more than 85%.
- **[Programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)**: the model writes Python that calls the tools in a sandbox and returns only the distillate. About 38% fewer input tokens on a benchmark with 75 tools, and 20–40% typical in production with 10 to 49 tools.
- **[Code Mode](https://blog.cloudflare.com/code-mode-mcp/)** (Cloudflare): the same thesis, from an infrastructure vendor, with a different argument — **training distribution**. LLMs write code against known APIs better than they fill in synthetic schemas. Industry convergence, not one vendor's quirk.
- **[Apply Patch](https://developers.openai.com/api/docs/guides/tools-apply-patch)** + **[GPT-5.1 for developers](https://openai.com/index/gpt-5-1-for-developers/)** (OpenAI): an editing tool **trained into the model**, in the V4A diff format. It explains why ad-hoc search/replace formats lose to the format the model saw in training.
- **See also**: the living collection [Awesome Harness Engineering — Tool Design](https://github.com/GHDaru/awesome-harness-engineering#tool-design) gathers more resources for this dimension, curated by problem.

## In practice: the same tool, three times

Let us write `buscar_arquivos` three times. With each version a different problem appears — and the third is what separates a tool that works from a tool that does not blow up the context.

**Version 1: the hand-written schema.** It is how almost everyone starts, and it is the scene that opened this chapter.

```python
SCHEMA = {
    "name": "buscar_arquivos",
    "description": "Searches files",
    "parameters": {
        "type": "object",
        "properties": {"padrao": {"type": "string"}},   # ← source of truth #2
        "required": ["padrao"],
    },
}

def buscar_arquivos(glob: str) -> list[str]:            # ← source of truth #1
    return [str(p) for p in Path(".").rglob(glob)]
```

Two declarations of the same contract, in two places, with nothing binding them. Rename one and the agent breaks at runtime, with a message that helps nobody. And look at the description: *"Searches files"* is all the model knows. It does not know whether globs are accepted, whether it recurses, whether it honors `.gitignore` — so it guesses.

**Version 2: the derived schema.** The contract gets a single source.

```python
@tools.tool
def buscar_arquivos(glob: str) -> list[str]:
    """Searches files by glob pattern, recursively, from the project root.
    Example patterns: '*.py', 'src/**/*.ts'. Ignores .git/."""
    return [str(p) for p in Path(".").rglob(glob)]
```

The decorator reads the signature and the docstring and **produces** the JSON Schema. It is what harness-zero step 2 implements, in three `inspect` calls:

```python
def _schema_da_funcao(fn) -> dict:
    sig = inspect.signature(fn)
    props, req = {}, []
    for nome, par in sig.parameters.items():
        props[nome] = {"type": _json_type(par.annotation)}
        if par.default is inspect.Parameter.empty:
            req.append(nome)
    return {
        "name": fn.__name__,
        "description": inspect.getdoc(fn) or fn.__name__,
        "parameters": {"type": "object", "properties": props, "required": req},
    }
```

Renaming `glob` now changes the schema along with it, because the schema **is** the signature. The opening scene stops being possible.

And notice where the docstring ended up: it became the description the model reads. That changes what you write in it. It is no longer documentation for whoever maintains the code, it is a **prompt**: example patterns, what the tool ignores, what it does not do. That is the chapter's sentence — a tool's description is prompt engineering, and the docstring is where it lives.

**Version 3: what goes back to the model is not what the function returns.** Here is the problem that only shows up in a real repository.

```python
@tools.tool
def buscar_arquivos(glob: str) -> Observacao:
    """Searches files by glob pattern, recursively. E.g. '*.py'."""
    achados = [str(p) for p in Path(".").rglob(glob)]
    return Observacao(
        dado=achados,                                  # complete, for the harness
        para_o_modelo=_resumir(achados),               # trimmed, for the context
    )

def _resumir(achados: list[str], teto: int = 50) -> str:
    if len(achados) <= teto:
        return "\n".join(achados)
    return (
        "\n".join(achados[:teto])
        + f"\n… and {len(achados) - teto} more files."
        + "\n(refine the pattern to see the rest)"
    )
```

Do the arithmetic with real numbers. A medium monorepo answers `**/*.ts` with about 4,100 paths. At 15 tokens per path, that is **~60,000 tokens** entering the context at once, for a question that is almost always settled by the first fifty. The trimmed version costs **~400**.

The 150× saving is not the main point. The point is the separation: the harness still holds the whole list in `dado`, to paginate, filter, or pass to another tool; the **model** receives the distillate. Two audiences, two formats, one return value.

It is the code translation of the rule Anthropic calls information density per token — and it is the idea Appendix A records under the name `to_llm_content` in software-agent-sdk.

## The state of the art

### 1. The consensus core, and the end of the hand-written schema

Harnesses converged on a core of about ten tools: read, write and edit file, glob, grep, shell, web fetch and search, todo, and delegate. It is the minimum kit of a coding agent.

And nobody writes JSON Schema by hand. The source of truth is the language's type system, with a decorator or a class doing the derivation. Appendix A has the inventory of which library each project uses.

The modern quality refinement is version 3 above: **separating what goes back to the model's context from the structured data**. It is where the difference between a good harness and an expensive one shows up first.

### 2. Tool context became a scarce resource, and there are three scaling regimes

The default of dumping every definition into the system prompt is dead. The choice today is by catalog size.

**Fixed catalog**, in the tens of tools: still acceptable to send everything.

**Tool search with deferred loading**, in the hundreds, typical of anyone plugging in several MCP servers: three to five tools stay hot and the rest load on demand.

**Code-as-action**, for pipelines with bulky data: the model writes code that orchestrates the tools in a sandbox and returns the distillate. It is version 3 taken to the limit, with the trimming done by program instead of by a fixed function.

The metric the industry started reporting is not accuracy in isolation. It is **accuracy per token of definition**.

### 3. The editing interface is trained, not invented

The chapter's most counterintuitive lesson: the best code-editing format is not the one you design, it is the one the **model saw in training**.

Hence one vendor shipping `apply_patch` as a native tool, hence a harness giving `apply_patch` to one model family and `edit`/`write` to another, and hence a project measuring empirically which format each model applies well, with a metric dedicated to it.

The corollary dismantles a common intuition: tool selection **varies by model family**. There is no "best interface"; there is the best interface for whoever is on the other side.

And a tool error comes back as **data**, so the model can self-correct, never as an exception that takes down the loop. Note that version 1 above violated this twice: the error propagated as a `TypeError` *and* said nothing about what to do.

### Executive summary

What is most modern: type-derived schemas with data/context separation; the three scaling regimes chosen by catalog size; and the editing interface as something trained, not designed.

**What to steal:** the `dado` × `para_o_modelo` separation, which is density control per token; tool search with deferred loading once the catalog passes the tens; measuring the edit format per model family instead of choosing by taste; and error-as-data, always.

## Hands-on — harness-zero, step 2

Step 2 (`harness-zero/etapas/02-tools/`) replaces step 1's hand-written schemas with a `ToolPort`: a tool is a typed function, and the schema is derived from the annotations via `inspect`, exactly as in the block above.

You add `read_file` alongside `get_time` and `somar`, with errors coming back as text to the model. The `/tools` window shows the derived schemas, so you can confirm that the signature and the contract are the same thing.

Completion exercise: the deriver ships skeletal, handling simple types only. Extend it to composite types (`list[str]`, `Optional[int]`), without duplicating the schema anywhere.

## Check your understanding

1. Why is a tool's description prompt engineering and not API documentation?
2. Your agent has access to eight MCP servers, more than 200 tools, and spends 55k tokens before acting. Which scaling regime do you adopt, and what stays loaded?
3. Why can giving `apply_patch` to a model beat a search/replace format you designed carefully?
4. In version 3 of the example, why does the function return both fields instead of simply returning the trimmed list?

---

## Appendix A — How each repository handles tools

> Per-harness evidence, with paths — online supplement, expanded each round.

### opencode (round 1)
~14 tools + 3 experimental (`tool/`), Effect Schema, separate `.txt` descriptions; **per-model selection** (`registry.ts`: GPT gets `apply_patch` instead of `edit`/`write`); embedded ripgrep; experimental `lsp`, `plan_exit`, `code-mode` (V8).

### gemini-cli (round 1)
~20–25 tools as declarative classes (`BaseDeclarativeTool` + `Invocation`), filtered registration (`maybeRegister`), declarations per model family; shell with background processes, web search with grounding, optional tracker (6 tools).

### OpenHarness (round 1)
**43+ tools** (`tools/`, `BaseTool` + Pydantic `input_model` → `to_api_schema()`); `is_read_only()` feeds the loop's parallelism; multimodal, cron, teams, `tool_search`.

### Codex CLI (round 2)
`tools/` crate with typed schemas; `unified_exec` (persistent shell with stdin); **first-class `apply_patch`** (streaming parser + `apply_patch.lark` grammar, varying by model); `tool_search`/`tool_discovery`; **code-mode with embedded V8**.

### Goose (round 2) ⭐ MCP-native
Every tool is MCP: `goose-mcp` built-ins are `rmcp::ServerHandler` served in-process over `DuplexStream`; even developer/shell/edit are "platform extensions" speaking `McpClientTrait`.

### OpenClaw (round 2)
Broad suite (`openclaw-tools*.ts`): runtime/files/web/CDP browser/media; **Tool Search** and **Code Mode** (JS/TS over a hidden catalog); 52 AgentSkills injected as a compact block, read on demand.

### Hermes (round 2)
~40+ tools in **composable toolsets** with dynamic postures; `execute_code` (Python calling tools via RPC, "zero-context-cost turns"); per-provider `schema_sanitizer`.

### Aider (round 2) ⭐ edit formats
Instead of JSON tools, **edit formats** (`*_coder.py`): whole/diff (fuzzy SEARCH-REPLACE)/udiff/patch; per-model selection; **benchmark-validated** (`percent_cases_well_formed`).

### software-agent-sdk (frameworks round) ⭐ data×context
Action/Observation/Executor contract; `Observation.to_llm_content` separates what goes back to the model from the structured data; toolsets (one `create` → several tools); MCP-style annotations; `ClientToolSpec` (tool executes on the client's machine).

### IronClaw (round 2)
Tools as **capabilities with typed descriptors** declaring `EffectKind`, credentials and network policy; visibility × authority separation (a hidden capability fails closed); obligations (redaction/limits) before any effect.

### n8n (round 2)
`create-node-as-tool.ts`: **any `usableAsTool` node becomes a tool** via `$fromAI('chave','desc',tipo)` → derived Zod schema; ToolWorkflow (sub-workflow as tool), ToolHttpRequest, ToolCode, ToolThink.

### Frameworks (frameworks round)
Agents SDK (Software Development Kit): `@function_tool` (Pydantic + griffe with docstring auto-detection), 13 types incl. hosted; LangGraph: inherits `@tool` from langchain-core, adds `ToolNode` (execution, injections); CrewAI: Pydantic `BaseTool`/`@tool`, `crewai-tools` catalog with 79 directories.

---

## Verification answers

**1.** Because the reader of the description is the model, and it is the description that decides **whether** and **how** the tool gets called. API documentation is consulted by someone who already decided to use the function; a tool's description is what produces the decision. Hence the practical consequences: small wording refinements change the hit rate, argument examples are worth more than formal prose, and what the tool *does not* do has to be written down, because silence becomes assumption. In version 1 of the example, *"Searches files"* made the model guess; in version 2, the docstring states the pattern format and what is ignored.

**2.** **Tool search with deferred loading.** What stays hot is the minimum the agent uses on almost every turn — the tool-search tool itself, plus the three to five local core tools (read file, edit, shell) — and the remaining 200-plus are marked to load on demand. What you are saving is not money in the abstract: it is 55k tokens that would leave the window **before** the first useful work, competing with the code the agent needs to see. If a bulky return accompanies the large catalog, the next regime is code-as-action.

**3.** Training distribution. The model saw a given diff format millions of times during training and has essentially never seen yours. Familiarity outweighs design quality: a worse but known format is applied correctly more often than a better, novel one. The corollary is uncomfortable and true — choosing the editing interface is not the architect's matter of taste, it is a **measurement** per model family, and that is why a dedicated metric for it exists.

**4.** Because the two audiences have opposite needs and there is only one return value. The **harness** needs the complete list: to paginate, to filter, to pass to another tool, to display in the interface. The **model** needs the minimum sufficient to decide the next step, and every extra path competes for window space with the code it came to read. Returning only the trimmed list would fix the cost and destroy the information; returning only the whole list preserves the information and blows the context. The separation is what lets you optimize one side without losing the other — and it is why this field has a name of its own in mature harnesses.
