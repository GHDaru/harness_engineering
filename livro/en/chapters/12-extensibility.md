<!-- i18n fonte:livro/capitulos/12-extensibilidade.md edicao:0.86 hash:dc6a3e28 -->
# 12. Extensibility

> **State of the art captured in 2026-07** · last revised 2026-08-12 · [history and expiration log](../historico.html)
>
> Didactic layer v4, see [Editorial Guide §2.1](../editorial-guide.md).
> scaffold: lacuna
>
> Skeleton v3, body carries the state of the art; per-repository treatment in Appendix A (supplemented online).

## Learning objectives

By the end of this chapter, you should be able to:
1. **Explain** why extensibility is "open for extension, closed for modification": extension points instead of forking;
2. **Distinguish** the four extension axes (hooks · commands/skills · plugins · providers) and what each one solves;
3. **Compare** the three ecosystem strategies: depth, packaging, interoperability;
4. **Evaluate** extension code as an attack surface (the *trust triangle*) and the defenses (scanning, trust envelope, managed settings, least-privilege);
5. **Implement** a pre/post-tool hook subsystem with the hook's return value as the control channel in harness-zero (step 11).

## The fork that ended up three versions behind

The team wanted two simple things. That every edit go through the formatter before being written, and that nobody run `terraform apply` from the agent.

The harness could do neither. So someone did the obvious thing: they forked it.

It worked for three weeks. In the second month, upstream shipped a fix for a sandbox escape, and the merge conflicted in four files. Someone resolved it in a hurry. In the third month came the session format change, and the merge conflicted in eleven. Nobody resolved it.

Today the fork is three versions behind, missing a security fix that never arrived, and the two rules that motivated all of it are still there, working, locked inside a harness nobody can update any more.

The mistake was not forking. It was the harness not offering **a stable boundary where those two rules would fit**. Extensibility is exactly that: the set of points where third parties change behavior **without touching the code**, and without which forking is the only way out.

## The problem

No harness covers every workflow; extensibility decides whether the user **adapts** the harness or **abandons** it. The established axes:

1. **Hooks**: user code intercepting the lifecycle (before/after a tool, compaction, session).
2. **Skills / custom commands**: capabilities packaged as markdown/config, loaded on demand.
3. **Plugins / extensions**: distributable packages aggregating tools, commands, hooks, and config.
4. **Model providers**: the most strategic extension: does the harness work with any model, or is it one model's showcase?

The rule uniting all four is old: **open for extension, closed for modification**, the user extends without editing (or forking) the core.

## Scientific foundations

Honest editorial record (Principle I): **there is no academic canon of "agent harness extensibility"**, it is a real gap. The durable citations come from the classic software engineering of extensible architectures and from plugin-ecosystem security, which transfer directly.

- **Extension points, not forks**: the open-closed principle (Meyer, 1988. Martin, 1996) and Eclipse's plug-in architecture ([Birsan, *ACM Queue* 2005](https://dl.acm.org/doi/10.1145/1053331.1053345)) provide the foundation, and the "*plug-in hell*" warning: poorly designed extension points become debt. Decision: expose explicit *seams* (events, well-known directories), not ad-hoc points.
- **Minimal core, pluggable extensions**: the Microkernel pattern (Buschmann et al., *POSA* v.1, 1996) and its agentic incarnation, [AIOS, arXiv 2403.16971](https://arxiv.org/abs/2403.16971) (a kernel that isolates scheduling/memory/tools from agent applications), support the "harness as microkernel" posture: a small core that serves as a socket.
- **Mechanism × policy**: [Hydra (Levin et al., SOSP '75)](https://dl.acm.org/doi/10.1145/800213.806531) is the origin of "separate mechanism from policy". Translated: the harness provides the *mechanism* (invoking a tool, dispatching a hook, loading a provider); the *extension* provides the policy. That is why adding a model provider can be "writing a file".
- **Third-party extensions are not trustworthy**: the best on-topic citation is [LLM (Large Language Model) Platform Security: ChatGPT Plugins, arXiv 2309.10254](https://arxiv.org/abs/2309.10254) (AIES '24): a platform/plugin/user *trust triangle* with concrete exploits (session hijacking via a malicious plugin). And the empirical base for over-privilege comes from browser-extension security ([Barth et al., NDSS '10](https://www.adambarth.com/papers/2010/barth-felt-saxena-boodman.pdf): 88% of extensions request more power than they need). Decision: least-privilege + isolation + verification, the same argument as ch. 06's *tool poisoning*.

(Full bibliography and pointers: `livro/bibliografia.md`.)

## Industry sources

- **Hooks: exit code as the control channel**: [Claude Code's hooks](https://code.claude.com/docs/en/hooks) expose ~31 lifecycle events (`PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `UserPromptSubmit`, `PreCompact`, `SubagentStop`…) where the harness runs user commands. The **exit code is the channel** (0 = proceed / JSON on stdout with allow-deny-ask; 2 = block with stderr fed back to the model). Decision: teams enforce policy (block `rm`, redact `.env`, auto-lint) **deterministically and without patching the harness**. And Codex implements the same pattern independently (hooks + `allow_managed_hooks_only` for enterprises), hooks are a **cross-vendor** standard, not one vendor's quirk.
- **Plugin = the packaging unit. Marketplace = the catalog**: the [Claude Code plugin model](https://code.claude.com/docs/en/discover-plugins): a plugin aggregates skills, subagents, hooks, MCP (Model Context Protocol), and LSP (Language Server Protocol) into an installable package (`/plugin install name@marketplace`). A [marketplace](https://code.claude.com/docs/en/plugin-marketplaces) is a git repo with `.claude-plugin/marketplace.json`. Installs at user/project/local/**managed** scope, with **pinning to SHAs** and a two-tier trust model (curated official marketplace + community with security triage). Decision: third-party extension becomes distributable **and governable** without forking.
- **Custom commands became a file-drop (and AGENTS.md is the open standard)**: in Claude Code, slash commands were [absorbed by skills](https://code.claude.com/docs/en/skills): dropping a file into `.claude/commands/` or `.claude/skills/` creates the command, with no registration or build. And [AGENTS.md](https://agents.md/) became the **open, multi-tool** config format, read by Codex, Cursor, Cline, Windsurf, Gemini CLI, and Claude Code. Decision: the extension point is "drop a file in a well-known directory", and the format is portable across harnesses.
- **Settings as an enforcement surface**: [Claude Code's config](https://code.claude.com/docs/en/settings) is a precedence stack (Managed &gt. CLI &gt; local &gt; project &gt; user); most keys override, but **permission rules merge**, and **managed settings cannot be overridden** (a security team denies tools/marketplaces for the whole company). Decision: config is not preference, it is enforcement (connects to ch. 07).
- **Extensibility is also a context budget**: [advanced tool use (Anthropic)](https://www.anthropic.com/engineering/advanced-tool-use) reframes it: with unlimited tool libraries, the extension must be **loaded on demand**, not registered up front. And plugins toggle on/off to control system-prompt cost. Decision: an extension point that always injects context does not scale, late loading is part of the design (connects to chs. 03 and 05).
- **See also**: the living collection [Awesome Harness Engineering: Debugging & Developer Experience](https://github.com/GHDaru/awesome-harness-engineering#debugging--developer-experience) gathers more consultable resources for this dimension (patterns, articles, and implementations), curated by problem.

## In practice: the hook whose return value is the control channel

A poor hook is an observer: it receives the event, does whatever it wants, and the harness carries on. It is good for logging and nothing else.

A useful hook **decides**, and the mechanism that makes it useful is the **return value**:

```python
@hooks.pre_tool
def formatar_antes_de_gravar(chamada: Chamada) -> Chamada | str | None:
    """Return contract:
       None            -> proceed unchanged
       Chamada         -> proceed with REWRITTEN arguments
       "block:reason"  -> do not execute, and the reason goes back as data
    """
    if chamada.nome != "editar":
        return None
    if chamada.args["path"].endswith(".py"):
        formatado = black.format_str(chamada.args["conteudo"], mode=black.Mode())
        return chamada.com(args={**chamada.args, "conteudo": formatado})
    return None


@hooks.pre_tool
def proibir_terraform(chamada: Chamada) -> str | None:
    if chamada.nome == "shell" and "terraform apply" in chamada.args["comando"]:
        return "block:terraform apply runs in the pipeline, not from the agent"
```

Both rules from the opening scene, in fifteen lines, with no fork.

Note what `block:` does: the reason **goes back to the model as data**, exactly like the tool error in ch. 05 and the plan-mode refusal in ch. 09. A hook that blocks silently produces an agent that tries again with different quoting.

And note where the hook lives: at the **boundary** between the loop and tool execution. It is not a patch inside the loop, it is a declared point. That is why the hook's author does not need to know how the loop works, and the loop's author can rewrite it without breaking the hook.

The bill remains, and it is why this chapter ends in ch. 07:

```python
# The hook runs with the harness's authority. It can read the arguments of
# any tool -- including file contents and any credentials passing through --
# and can rewrite them before execution.
```

A third-party plugin installed by one line of configuration has, by construction, the same reach as the code you wrote yourself. It is the same thesis as the supply-chain appendix, and it is why the plugin registry is an attack vector rather than a packaging detail.

```python
# GAP (step 11): write the auditor. It records in auditoria.jsonl every call
# and every hook verdict, with timestamp and plugin origin -- because
# extensibility without a trail is the ch. 07 surface with no sensor.
@hooks.post_tool
def auditar(chamada: Chamada, resultado: str) -> None:
    ...
```

## The state of the art

### 1. Three ecosystem strategies

Round 1's framing persists and got reinforced. **Depth**: hooks reach points the others don't expose, opencode transforms messages and the system prompt before sending, intercepts `permission.ask`, and registers auth providers. **Packaging**: the *extension* as a complete distribution unit (gemini-cli aggregates MCP+commands+hooks+policies into one package; Codex with a manifest + marketplace + App Server JSON-RPC (Remote Procedure Call)). **Interoperability**: adopting the leader's formats instead of inventing your own (OpenHarness with `SKILL.md`/`.claude-plugin`; IronClaw with a compatible `SKILL.md`).

### 2. The interoperability bet is winning, the "MCP of extensibility"

What in round 1 was the most underrated axis became the dominant trend: **extension formats are converging on standards portable across harnesses**. `SKILL.md`/AgentSkills (OpenClaw uses the `agentskills.io` standard. IronClaw declares compatibility with OpenClaw/Claude), `.claude-plugin` (adopted by OpenHarness), and above all **AGENTS.md** (read by six different harnesses) are doing for extensibility what MCP did for integration. Even the **hook vocabulary** converged. Codex's event set is practically OpenHarness's and Claude Code's (`PreToolUse`/`PostToolUse`/… with Approve/Block/Deny/Ask decisions). Extensibility is ceasing to be a per-harness silo.

### 3. Marketplaces and security scanning, round 1's gap closed

In round 1, only gemini-cli treated extension code as an attack surface. In round 2 that became the norm, exactly as the plugin *trust triangle* predicted: **OpenClaw** has the **ClawHub** registry with a *trust envelope* + scanning (VirusTotal/ClawScan). Claude Code has a curated official marketplace + community with security triage and **SHA pinning**; **n8n** runs `scan-community-package`; **Goose** checks extensions for malware before loading. Added to the **managed settings** that deny marketplaces enterprise-wide, extension distribution became infrastructure *with containment*, the least-privilege the over-privilege literature demands.

### 4. Provider-agnosticism became declarative config

The mechanism × policy separation applied to the model: adding a provider stopped being code and became a file. **Goose** has **37 declarative providers via JSON** (an OpenAI-compatible provider = one file). **opencode** has ~26 loaders + hundreds of models via models.dev; **Hermes** has a subclassable `ProviderProfile` (Nous Portal with 300+ models). The model-agnostic harness (treating the provider as pluggable policy) beat the single-vendor showcase.

### 5. The next frontier: the harness that extends itself

The embryo of self-extension is already visible: **IronClaw** has **automatic skill extraction** (`learning.rs`) with usage and confidence metrics, the harness observes its own work and writes new skills. It is the bridge to ch. 16 (learning) and to the Voyager/ToolMaker lineage: extensibility that doesn't wait for the user.

### Executive summary

What's most modern: format convergence (SKILL.md/.claude-plugin/AGENTS.md as portable standards); marketplaces with security scanning and managed settings; hooks with exit-code as a cross-vendor channel; declarative provider-agnosticism; and the beginning of self-extension. **What to steal:** expose explicit seams (named events, well-known directories) instead of ad-hoc points. Adopt portable formats instead of inventing your own; treat third-party extensions as untrusted (scan + least-privilege + managed deny); and make loading late so you don't blow the context.

## Hands-on, harness-zero, step 11

Step 11 (`harness-zero/etapas/11-hooks/`) gives harness-zero a **pre/post-tool hook** subsystem: before each tool call, hooks are registered functions (`@hooks.pre_tool`/`@hooks.post_tool`) and the **hook's return value is the control channel** (`"block:reason"` blocks and feeds the reason back to the model. A dict adjusts the arguments), the completeness exercise proposes the products' external variant: run a user command and read the exit code (0 proceeds; non-zero blocks with the stderr). It is the mechanism (the harness dispatches the hook) separated from the policy (the user decides what the hook does), the chapter's thesis in ~40 lines. Completeness exercise: you add a `PostToolUse` that runs a linter and returns the errors to the model, and a minimal trust gate (the hook only runs if the directory is trusted).

## Check your understanding

1. Why does "open for extension, closed for modification" lead to *hooks* and *plugins* instead of telling the user to fork the harness?
2. You are going to allow a third-party plugin marketplace. Name the central risk (with its name from the literature) and two concrete defenses. (*Trust triangle* / over-privilege; defenses: security scanning + SHA pinning + managed settings that deny + least-privilege.)
3. Your harness needs to support a new model provider without a release. Which design principle makes that "writing a file"?
---

## Appendix A — How each repository handles extensibility

> Per-harness evidence, with paths — supplemented online, expanded each round.

### opencode (round 1) — deep hooks and radical provider agnosticism
Plugins are functions returning `Hooks` (`packages/plugin/`): **~15 points**, including rare ones — transforming messages/system prompt before sending (`experimental.chat.messages.transform`), intercepting `permission.ask`, customizing compaction, and **registering auth providers** (`auth`). Custom tools auto-loaded from `tool/`. And **~26 provider loaders** + hundreds of models via models.dev, on the Vercel AI SDK (Software Development Kit) — the most model-agnostic in production.

### gemini-cli (round 1) — the all-in-one package
**Extensions** (`gemini-extension.json`): an installable package aggregates MCP servers, custom commands, hooks, **permission policies**, skills, and themes. Custom commands in TOML (`FileCommandLoader`). Hooks as a subsystem (`packages/core/src/hooks/`) with a **trust gate** (`trustedHooks.ts` — they only run in trusted folders). Providers: the Google ecosystem.

### OpenHarness (round 1) — compatibility as strategy
Markdown skills also loaded from `~/.claude/skills` and `~/.agents/skills` (`SKILL.md` layout); plugins in the `.claude-plugin/plugin.json` format (12 real plugins tested); hooks cover **10 events** with **hot-reload**. Providers as named "workflows" (Anthropic/OpenAI-compatible, Copilot, Kimi, GLM, Ollama…).

### Codex CLI (round 2) — full hooks + marketplace + App Server
**Full hooks** (`hooks/`: PreToolUse/PostToolUse/PreCompact/SessionStart-End/UserPromptSubmit/Stop/SubagentStart-Stop, with Approve/Block/Deny/Ask decisions) and the enterprise knob `allow_managed_hooks_only`; plugins with a manifest and marketplace; skills; configurable providers; profiles; Python/TS SDKs; the **App Server JSON-RPC** as the programmatic backbone.

### OpenClaw (round 2) ⭐ — registry with security scanning
Skills in the **AgentSkills** standard (`agentskills.io`) with 6 precedence levels and the public **ClawHub** registry with a *trust envelope* + scanning (VirusTotal/ClawScan); **159 plugins** (tools, channels, providers, hooks, media) with a Plugin SDK; dozens of LLM providers with failover and auth rotation.

### IronClaw (round 2) ⭐ — compatible and self-extending
A **`SKILL.md` format compatible** with OpenClaw/Claude; v2 skills with executable snippets, usage/confidence metrics, and **automatic skill extraction** (`learning.rs`); extensions via WASM/MCP/first-party **without restart**; configurable providers (NEAR AI, Gemini OAuth…).

### Goose (round 2) — declarative providers and branded distros
Three axes: MCP extensions (6 transport/origin types); recipes/skills; and providers — native + **37 declarative providers via JSON** (adding an OpenAI-compatible provider = creating a file). `CUSTOM_DISTROS.md` (branded distros); `goose-sdk` for embedding; extension malware checks before loading.

### Hermes (round 2) — ProviderProfile and plugins
A subclassable `ProviderProfile` (**Nous Portal** with 300+ models under subscription, OpenRouter, your own endpoint); a plugin system (20 directories, a toolset registry, session hooks); Anthropic/Bedrock/Codex/ACP (Agent Client Protocol) adapters.

### OpenHands (round 2) — marketplaces and dependency injection
Skill/plugin marketplaces (instance/org/personal); LLM + agent profiles; a pluggable Git-integrations layer; third-party agents via ACP; **sandbox/event-store backends swappable via dependency injection**; litellm for providers.

### n8n (round 2) ⭐ — the catalog as extensibility
The strongest point: **the 400+ integration nodes become a tool pool** without writing code (via `usableAsTool` + `$fromAI`); community nodes with a security scanner (`scan-community-package`); ~20 model providers (`LmChat*`).

### ohmo (round 2) — extra roots
`~/.ohmo/skills` and `~/.ohmo/plugins` as roots coexisting with the project's; plugins load tools, slash commands, and MCP servers; skills become channel commands; arbitrary per-channel `channel_configs`.

### Frameworks (frameworks round)
Frameworks expose extensibility as API: tool registration/`@tool`, lifecycle callbacks/hooks, provider adapters (litellm/model providers), and — increasingly — reading `AGENTS.md`. The portable format (AGENTS.md, SKILL.md) is what brings frameworks and coding harnesses together into a common ecosystem.

---

## Verification answers

**1.** Because a hook that only observes solves neither of the two problems that lead to forking. Whoever wants to format before writing needs to **rewrite the argument**; whoever wants to forbid a command needs to **prevent execution**. An observer can record that it happened, and that is too late. Making the return value the control channel gives both capabilities without inventing a new API: `None` proceeds, an object rewrites, a prefixed string blocks. And the block has to carry the **reason**, because the reason goes back to the model as data — without it, the agent gets an unexplained refusal and retries, which is the same mistake as treating a tool error as an exception.

**2.** The stable boundary is the contract between whoever extends and whoever maintains. It needs three properties. **Being declared**, with a name and a signature, not an arbitrary point in the code. **Being few points**, because every extension point is a commitment that constrains future refactoring. And **not leaking the implementation**: the hook receives the call and returns a decision, it does not receive the loop's internal object. Without that, the plugin author couples to your code, and you are back to the fork problem under a prettier name. The sign that the boundary is right is being able to rewrite the whole loop without breaking any existing hook.

**3.** That the plugin runs with the **harness's authority**, not a lesser one. It reads the arguments of every tool, which includes file contents and any credential passing through, and it can rewrite them before execution. Installing a plugin is therefore a decision of the same class as installing a code dependency, not an interface preference. The defenses are the ch. 07 ones applied to the extension mechanism itself: isolate the plugin where the language allows, mediate credentials so it never sees them, pin the version instead of accepting automatic updates, and **audit** — because extensibility without a trail is an attack surface with no sensor.
