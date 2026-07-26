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

> Atualização (livro vivo, 2026-07): a lacuna registrada nas rodadas anteriores foi **preenchida** — o MCP acumulou um SoK, benchmarks de *tool poisoning* e auditorias empíricas de servidores. O padrão continua sendo *spec de indústria*; a academia entrou pela porta da **segurança**.

- ⭐ ✓ **Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions** (Hou et al.) — arXiv [2503.23278](https://arxiv.org/abs/2503.23278); também ACM TOSEM. O SoK canônico: ciclo de vida do servidor + taxonomia de ameaças por fase.
- ⭐ ✓ **MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers** (Wang, Gao et al.) — arXiv [2508.14925](https://arxiv.org/abs/2508.14925). 45 servidores reais / 353 tools; sucesso de até ~73%; modelos mais capazes foram mais suscetíveis.
- ✓ **Model Context Protocol (MCP) at First Glance: Studying the Security and Maintainability of MCP Servers** (Hasan, Li, Fallahzadeh, Rajbahadur, Adams, Hassan) — arXiv [2506.13538](https://arxiv.org/abs/2506.13538). 1.899 servidores auditados: 7,2% com vulns gerais, 5,5% com *tool poisoning*.
- ✓ **MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits** (Radosevich & Halloran) — arXiv [2504.03767](https://arxiv.org/abs/2504.03767). Exploits via tools legitimamente registradas; ferramenta MCPSafetyScanner.
- ✓ **A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, and ANP** (Ehtesham, Singh et al.) — arXiv [2505.02279](https://arxiv.org/abs/2505.02279). Escolher o protocolo pelo contexto de confiança (liga ao cap. 17).
- ✓ **Not what you've signed up for: …Indirect Prompt Injection** (Greshake et al.) — arXiv [2302.12173](https://arxiv.org/abs/2302.12173). A base first-principles: conteúdo recuperado é canal de instrução.
- ~ **Threat Modeling and Analysis of Vulnerabilities to Prompt Injection with Tool Poisoning** — arXiv [2603.22489](https://arxiv.org/abs/2603.22489); MDPI *J. Cybersecurity and Privacy* 6(3):84 (2026). STRIDE+DREAD sobre componentes MCP. *(ID e veículo verificados; lista de autores não confirmada por snippet.)*

Fontes da indústria (docs/vendor/praticantes) na linha do Cap. 06 abaixo.

## Cap. 07 — Permissões e Sandboxing

- ⭐ ✓ **Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection** (Greshake et al.) — arXiv [2302.12173](https://arxiv.org/abs/2302.12173). O paper que definiu a ameaça.
- ✓ **A Systematic Survey of Security Threats and Defenses in LLM-Based AI Agents: A Layered Attack Surface Framework** — arXiv [2604.23338](https://arxiv.org/abs/2604.23338).
- ✓ **A Survey on Agentic Security: Applications, Threats and Defenses** — arXiv [2510.06445](https://arxiv.org/abs/2510.06445).
- ✓ **Safety and Security Threats of Computer-Using Agents** — arXiv [2505.10924](https://arxiv.org/abs/2505.10924).

## Cap. 08 — Memória e Estado

- ⭐ ✓ **MemGPT: Towards LLMs as Operating Systems** (Packer et al.) — arXiv [2310.08560](https://arxiv.org/abs/2310.08560). Contexto como RAM escassa; tiers recall/archival; o agente pagina via tool ("context page faults").
- ⭐ ✓ **Generative Agents: Interactive Simulacra of Human Behavior** (Park et al.) — arXiv [2304.03442](https://arxiv.org/abs/2304.03442); UIST '23. O *memory stream* e o recall por **recência × importância × relevância** + consolidação por reflexão.
- ⭐ ✓ **Cognitive Architectures for Language Agents (CoALA)** (Sumers et al.) — arXiv [2309.02427](https://arxiv.org/abs/2309.02427). A taxonomia episódica/semântica/procedural + working memory (base Tulving).
- ✓ **A Survey on the Memory Mechanism of LLM-based Agents** (Zhang et al.) — arXiv [2404.13501](https://arxiv.org/abs/2404.13501); ACM TOIS. Fontes · formas · operações (escrita/gestão/leitura).
- ✓ **MemoryBank: Enhancing LLMs with Long-Term Memory** (Zhong et al.) — arXiv [2305.10250](https://arxiv.org/abs/2305.10250); AAAI '24. Esquecimento controlado por curva de Ebbinghaus (tempo × frequência de acesso).
- ✓ **Reflexion: Language Agents with Verbal Reinforcement Learning** (Shinn et al.) — arXiv [2303.11366](https://arxiv.org/abs/2303.11366); NeurIPS '23. Auto-reflexão verbal persistida em buffer episódico (ponte com o cap. 16).
- ✓ **A-MEM: Agentic Memory for LLM Agents** (Xu et al.) — arXiv [2502.12110](https://arxiv.org/abs/2502.12110). Notas estruturadas auto-organizadas (Zettelkasten).
- ✓ **Mem0: Production-Ready AI Agents with Scalable Long-Term Memory** (Chhikara et al.) — arXiv [2504.19413](https://arxiv.org/abs/2504.19413); ECAI '25. Pipeline extrair→consolidar→recuperar; benchmark LoCoMo.
- ✓ **A Survey on the Memory Mechanism** e surveys de evolução: **From Storage to Experience** — arXiv [2605.06716](https://arxiv.org/abs/2605.06716); **From Human Memory to AI Memory** — arXiv [2504.15965](https://arxiv.org/abs/2504.15965); **Governing Evolving Memory in LLM Agents (SSGM)** — arXiv [2603.11768](https://arxiv.org/abs/2603.11768) (também cap. 16).
- ~ **Zep: A Temporal Knowledge Graph Architecture for Agent Memory** — arXiv [2501.13956](https://arxiv.org/abs/2501.13956). Grafo bi-temporal; fatos desatualizados invalidados, não deletados. *(ID recorrente em buscas; não aberto byte-a-byte pelo proxy.)*

## Cap. 09 — Planejamento

- ⭐ ✓ **ReAct: Synergizing Reasoning and Acting in Language Models** (Yao et al.) — arXiv [2210.03629](https://arxiv.org/abs/2210.03629); ICLR '23. Intercalar razão e ação no mesmo loop.
- ⭐ ✓ **Understanding the Planning of LLM Agents: A Survey** (Huang et al.) — arXiv [2402.02716](https://arxiv.org/abs/2402.02716). Taxonomia de cinco vias (decomposição · seleção · módulo externo · reflexão · memória).
- ✓ **Plan-and-Solve Prompting** (Wang et al.) — arXiv [2305.04091](https://arxiv.org/abs/2305.04091); ACL '23. Plano explícito antes de resolver (escopo conhecido).
- ✓ **Tree of Thoughts** (Yao et al.) — arXiv [2305.10601](https://arxiv.org/abs/2305.10601); NeurIPS '23. Busca sobre planos com backtracking.
- ✓ **ADaPT: As-Needed Decomposition and Planning** (Prasad et al.) — arXiv [2311.05772](https://arxiv.org/abs/2311.05772); NAACL Findings '24. Decompor só quando o executor falha.
- ✓ **Beyond Entangled Planning: Task-Decoupled Planning for Long-Horizon Agents** — arXiv [2601.07577](https://arxiv.org/abs/2601.07577). DAG de sub-objetivos com contexto escopado (−82% tokens).
- ✓ **PlanGenLLMs: A Modern Survey of LLM Planning Capabilities** (Wei et al.) — arXiv [2502.11221](https://arxiv.org/abs/2502.11221); ACL '25. Seis critérios de avaliação de plano.
- ✓ **PLANET: Benchmarks for Evaluating LLMs' Planning Capabilities** — arXiv [2504.14773](https://arxiv.org/abs/2504.14773).
- ✓ **PlanBench** (Valmeekam et al.) — arXiv [2206.10498](https://arxiv.org/abs/2206.10498); NeurIPS '22 Datasets. Modelos crus falham em geração de plano → validadores externos.
- ✓ **TravelPlanner** (Xie et al.) — arXiv [2402.01622](https://arxiv.org/abs/2402.01622); ICML '24. Agentes perdem o fio de múltiplas restrições → externalizar rastreio.

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

**Cap. 06 (MCP):** [Arquitetura MCP (spec)](https://modelcontextprotocol.io/docs/learn/architecture) · [Transportes (spec)](https://modelcontextprotocol.io/docs/concepts/transports) · [Introducing MCP (Anthropic)](https://www.anthropic.com/news/model-context-protocol) · [OpenAI adota MCP (TechCrunch)](https://techcrunch.com/2025/03/26/openai-adopts-rival-anthropics-standard-for-connecting-ai-models-to-data/) · [Google embraces MCP (The New Stack)](https://thenewstack.io/google-embraces-mcp/) · [MCP GA no Copilot Studio (Microsoft)](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/model-context-protocol-mcp-is-now-generally-available-in-microsoft-copilot-studio/) · [MCP Auth spec (Descope)](https://www.descope.com/blog/post/mcp-auth-spec) · [Tool Poisoning (Invariant Labs)](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) · [Line jumping (Trail of Bits)](https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/) · [The lethal trifecta (Willison)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · [MCP Registry (preview)](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/) · [MCP → Agentic AI Foundation (Anthropic)](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)

**Cap. 08 (Memória/estado):** [Manage sessions (Claude Code)](https://code.claude.com/docs/en/sessions) · [Checkpointing (Claude Code)](https://code.claude.com/docs/en/checkpointing) · [File-checkpointing (Agent SDK)](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing) · [How Claude remembers your project](https://code.claude.com/docs/en/memory) · [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) · [Managing context (context editing + memory)](https://www.anthropic.com/news/context-management) · [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) · [Memory blocks (Letta)](https://www.letta.com/blog/memory-blocks/) · [RAG is not agent memory (Letta)](https://www.letta.com/blog/rag-vs-agent-memory/) · [Memory types (mem0)](https://docs.mem0.ai/core-concepts/memory-types) · [Graphiti knowledge-graph memory (Neo4j)](https://neo4j.com/blog/developer/graphiti-knowledge-graph-memory/) · [LangMem SDK (LangChain)](https://www.langchain.com/blog/langmem-sdk-launch) · [Memory vs RAG (AWS Bedrock AgentCore)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-ltm-rag.html)

**Cap. 09 (Planejamento):** [Permission modes / plan mode (Claude Code)](https://code.claude.com/docs/en/permission-modes) · [Best practices — Explore/Plan/Code/Commit](https://code.claude.com/docs/en/best-practices) · [Todo tracking (Agent SDK)](https://docs.claude.com/en/docs/agent-sdk/todo-tracking) · [The "think" tool](https://www.anthropic.com/engineering/claude-think-tool) · [Extended/interleaved thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking) · [GitHub Spec Kit](https://github.com/github/spec-kit) · [Spec-driven development (GitHub Blog)](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) · [Kiro specs](https://kiro.dev/docs/specs/) · [Multi-agent research system (Anthropic)](https://www.anthropic.com/engineering/multi-agent-research-system) · [Don't Build Multi-Agents (Cognition)](https://cognition.com/blog/dont-build-multi-agents)

**Cap. 07 (Segurança):** [Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) · [How we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude) · [Agent approvals & security (Codex)](https://developers.openai.com/codex/agent-approvals-security) · [Agents Rule of Two (Meta)](https://ai.meta.com/blog/practical-ai-agent-security/) · [The lethal trifecta (Willison)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) · [New prompt injection papers](https://simonwillison.net/2025/Nov/2/new-prompt-injection-papers/) · [OpenClaw attacks (The Hacker News)](https://thehackernews.com/2026/06/new-attacks-trick-openclaw-ai-agent.html)

## Pedagogia (fundamenta o método do livro, não o conteúdo)

- ✓ **Blueprints for complex learning: The 4C/ID-model** (van Merriënboer et al.) — [ETR&D](https://link.springer.com/article/10.1007/BF02504993).
- ✓ **Cognitive Architecture and Instructional Design: 20 Years Later** (Sweller, van Merriënboer & Paas, 2019) — [EPR](https://link.springer.com/article/10.1007/s10648-019-09465-5).
- ⏳ *Ten Steps to Complex Learning* (3ª ed., 2018, Routledge); *Understanding by Design* (Wiggins & McTighe); Diátaxis (diataxis.fr).
