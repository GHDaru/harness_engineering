# Bibliografia científica do livro

> Regra editorial: nenhuma referência entra num capítulo sem status **✓ validada** (ID↔título confirmado por fonte independente). Nesta sessão o arXiv está bloqueado pela política de rede; a validação foi feita por busca cruzada (título retornado junto ao ID). Itens **⏳ pendentes** aguardam confirmação (rodar `verify` localmente ou conferir manualmente). ⭐ = âncora do capítulo.

## Status geral

| Status | Significado |
|---|---|
| ✓ | ID↔título confirmado por busca independente nesta sessão |
| ⏳ | Citada de memória ou de fonte única; confirmar antes de citar no corpo |

## Transversal / Fundamentos (caps. 00–01)

- ⭐ ✓ **From Question Answering to Task Completion: A Survey on Agent System and Harness Design** — arXiv [2606.20683](https://arxiv.org/abs/2606.20683). O survey exatamente no recorte do livro; candidata a espinha teórica do cap. 01.
- ✓ **Recursive Agent Harnesses** — arXiv [2606.13643](https://arxiv.org/abs/2606.13643). Achado da validação; avaliar aderência (harnesses compostos — conecta com caps. 10 e 15).
- ✓ **ReAct: Synergizing Reasoning and Acting in Language Models** (Yao et al.) — arXiv [2210.03629](https://arxiv.org/abs/2210.03629). O paper seminal do loop raciocínio+ação.
- ⏳ *A Review of Prominent Paradigms for LLM-Based Agents* — CoLing 2025 ([aclanthology](https://aclanthology.org/2025.coling-main.652.pdf)).

## Cap. 02 — Loop do Agente

- ✓ ReAct (acima).
- ✓ **LLM-based Agentic Reasoning Frameworks: A Survey** — arXiv [2508.17692](https://arxiv.org/abs/2508.17692).
- ✓ **A Comprehensive Survey on RL-based Agentic Search** — arXiv [2510.16724](https://arxiv.org/abs/2510.16724) (loop treinado, fronteira do capítulo).

## Cap. 03 — Entrega de Contexto

- ⭐ ✓ **A Survey of Context Engineering for Large Language Models** — arXiv [2507.13334](https://arxiv.org/abs/2507.13334).
- ✓ **Lost in the Middle: How Language Models Use Long Contexts** (Liu et al.) — arXiv [2307.03172](https://arxiv.org/abs/2307.03172). A base empírica do "posição importa" (justifica tail preservation e prompts em camadas).
- ✓ **Less Context, Better Agents: Efficient Context Engineering for Long-Horizon Tool-Using LLM Agents** — arXiv [2606.10209](https://arxiv.org/abs/2606.10209).

## Cap. 04 — Compactação

- ⭐ ✓ **MemGPT: Towards LLMs as Operating Systems** (Packer et al.) — arXiv [2310.08560](https://arxiv.org/abs/2310.08560). A formulação "memória virtual" que antecipou a escada de compactação.
- ✓ **ContextBudget: Budget-Aware Context Management for Long-Horizon Search Agents** — arXiv [2604.01664](https://arxiv.org/abs/2604.01664).
- ✓ **The Missing Memory Hierarchy: Demand Paging for LLM Context Windows** — arXiv [2603.09023](https://arxiv.org/abs/2603.09023).
- ✓ Lost in the Middle (cap. 03) — fundamenta *o que* preservar.

## Cap. 05 — Ferramentas

- ✓ **The Evolution of Tool Use in LLM Agents: From Single-Tool Call to Multi-Tool Orchestration** — arXiv [2603.22862](https://arxiv.org/abs/2603.22862).
- ⏳ *Tool Learning with LLMs: A Survey* (Qu et al.) — arXiv 2405.17935 (+ [repo](https://github.com/quchangle1/LLM-Tool-Survey)).
- ⏳ Gorilla / ToolLLM (papers seminais de tool-calling).

## Cap. 06 — MCP

- Lacuna acadêmica identificada (2×): specs (MCP) + análises de segurança de MCP a localizar. Cobrir com a spec oficial e literatura industrial até surgir survey.

## Cap. 07 — Permissões e Sandboxing

- ⭐ ✓ **Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection** (Greshake et al.) — arXiv [2302.12173](https://arxiv.org/abs/2302.12173). O paper que definiu a ameaça.
- ✓ **A Systematic Survey of Security Threats and Defenses in LLM-Based AI Agents: A Layered Attack Surface Framework** — arXiv [2604.23338](https://arxiv.org/abs/2604.23338).
- ✓ **A Survey on Agentic Security: Applications, Threats and Defenses** — arXiv [2510.06445](https://arxiv.org/abs/2510.06445).
- ✓ **Safety and Security Threats of Computer-Using Agents** — arXiv [2505.10924](https://arxiv.org/abs/2505.10924).

## Cap. 08 — Memória e Estado

- ⭐ ✓ **A Survey on the Memory Mechanism of LLM-based Agents** — arXiv [2404.13501](https://arxiv.org/abs/2404.13501).
- ✓ **From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms** — arXiv [2605.06716](https://arxiv.org/abs/2605.06716).
- ✓ **From Human Memory to AI Memory** — arXiv [2504.15965](https://arxiv.org/abs/2504.15965).
- ✓ **Governing Evolving Memory in LLM Agents (SSGM)** — arXiv [2603.11768](https://arxiv.org/abs/2603.11768) — também alimenta o cap. 16 (riscos de memória evolutiva).
- ✓ MemGPT (cap. 04).

## Cap. 09 — Planejamento

- ⏳ *Understanding the Planning of LLM Agents: A Survey* (Huang et al.) — arXiv 2402.02716.
- ✓ **PLANET: Benchmarks for Evaluating LLMs' Planning Capabilities** — arXiv [2504.14773](https://arxiv.org/abs/2504.14773).
- ✓ **Beyond Entangled Planning: Task-Decoupled Planning for Long-Horizon Agents** — arXiv [2601.07577](https://arxiv.org/abs/2601.07577).

## Cap. 10 — Subagentes e Orquestração

- ⏳ *LLM-based Multi-Agent Systems Survey* — arXiv 2412.17481.
- ✓ **D3MAS: Decompose, Deduce, Distribute** — arXiv [2510.10585](https://arxiv.org/abs/2510.10585).
- ✓ Recursive Agent Harnesses (transversal).

## Cap. 11 — Verificação e Evals

- ⭐ ✓ **Survey on Evaluation of LLM-based Agents** — arXiv [2503.16416](https://arxiv.org/abs/2503.16416).
- ✓ **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** — arXiv [2310.06770](https://arxiv.org/abs/2310.06770).
- ✓ **The 2025 AI Agent Index** — arXiv [2602.17753](https://arxiv.org/abs/2602.17753) (FAccT 2026).
- ⏳ tau-bench — arXiv 2406.12045 (não confirmado por busca; verificar).

## Cap. 16 — Aprendizado e Auto-melhoria

- ⭐ ✓ **A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve** — arXiv [2507.21046](https://arxiv.org/abs/2507.21046).
- ✓ **Voyager: An Open-Ended Embodied Agent with LLMs** — arXiv [2305.16291](https://arxiv.org/abs/2305.16291). A skill library auto-escrita que antecipou o Hermes em 3 anos.
- ✓ **Adaptation of Agentic AI: Post-Training, Memory, and Skills** — arXiv [2512.16301](https://arxiv.org/abs/2512.16301).
- ⏳ *Comprehensive Survey of Self-Evolving AI Agents* — arXiv 2508.07407.
- ✓ SSGM (cap. 08) — o risco do aprendizado permanente envenenado.

## Caps. 12, 13, 15, 17 — a lacuna registrada

Extensibilidade, interfaces, harnesses embutidos e protocolos têm literatura acadêmica **rarefeita** (buscas de 2026-07-25 não retornaram surveys dedicados). Registro editorial: o livro cobre essas dimensões com specs, evidência do benchmark e literatura industrial — e assinala a lacuna como oportunidade de pesquisa (possível seção "problemas em aberto" no cap. 14).

## Fontes da indústria por capítulo (docs de vendor e blogs de engenharia)

> Material comercial/industrial que fundamenta a seção "Fontes da indústria" de cada capítulo (esqueleto v3). URLs verificadas como existentes por busca; fetch direto a anthropic.com/openai.com retorna 403 (anti-bot) neste ambiente — conteúdo confirmado por snippets e citações de terceiros.

**Cap. 02 (Loop):** [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop) · [Loop engineering](https://claude.com/blog/getting-started-with-loops) · [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) · [Running agents (OpenAI Agents SDK)](https://openai.github.io/openai-agents-python/running_agents/) · [LoopAgent (Google ADK)](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/) · [Durable AI Loops (Restate)](https://www.restate.dev/blog/durable-ai-loops-fault-tolerance-across-frameworks-and-without-handcuffs) · [Durable Execution (Inngest)](https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents)

**Cap. 03 (Contexto):** [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Prompt caching (docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) · [Prompt caching is everything](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything) · [AGENTS.md](https://agents.md/) · [Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/) · [How Claude remembers your project](https://code.claude.com/docs/en/memory) · [AGENTS.md Field Guide 2026](https://www.iuriio.com/blog/posts/2026/05/agents-md-field-guide-2026)

**Cap. 04 (Compactação):** [Compaction (docs)](https://platform.claude.com/docs/en/build-with-claude/compaction) · [Auto Compact explained (CometAPI)](https://www.cometapi.com/what-is-auto-compact-in-claude-code/) · [Compaction explained (okhlopkov)](https://okhlopkov.com/claude-code-compaction-explained/) · [Protecting more context (hyperdev)](https://hyperdev.matsuoka.com/p/how-claude-code-got-better-by-protecting)

**Cap. 05 (Tools):** [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) · [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) · [Tool search tool (docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) · [Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) · [Programmatic tool calling (docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) · [Code Mode (Cloudflare)](https://blog.cloudflare.com/code-mode-mcp/) · [Apply Patch (OpenAI docs)](https://developers.openai.com/api/docs/guides/tools-apply-patch) · [GPT-5.1 for developers](https://openai.com/index/gpt-5-1-for-developers/)

**Cap. 07 (Segurança):** [Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) · [How we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude) · [Agent approvals & security (Codex)](https://developers.openai.com/codex/agent-approvals-security) · [Agents Rule of Two (Meta)](https://ai.meta.com/blog/practical-ai-agent-security/) · [The lethal trifecta (Willison)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · [New prompt injection papers](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/) · [OpenClaw attacks (The Hacker News)](https://thehackernews.com/2026/06/new-attacks-trick-openclaw-ai-agent.html)

## Pedagogia (fundamenta o método do livro, não o conteúdo)

- ✓ **Blueprints for complex learning: The 4C/ID-model** (van Merriënboer et al.) — [ETR&D](https://link.springer.com/article/10.1007/BF02504993).
- ✓ **Cognitive Architecture and Instructional Design: 20 Years Later** (Sweller, van Merriënboer & Paas, 2019) — [EPR](https://link.springer.com/article/10.1007/s10648-019-09465-5).
- ⏳ *Ten Steps to Complex Learning* (3ª ed., 2018, Routledge); *Understanding by Design* (Wiggins & McTighe); Diátaxis (diataxis.fr).
