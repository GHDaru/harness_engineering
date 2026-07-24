# Nota de pesquisa — Frameworks de harness: a camada "construa o seu"

> Data: 2026-07-24 · Método: pesquisa web + conhecimento consolidado; avaliação por código pendente (repos não forkados). Prepara a categoria "frameworks" do benchmark e o futuro capítulo "Construir vs. adotar".

## A tese da categoria

Frameworks não são harnesses: são **kits de primitivas para construir harnesses**. O usuário de um harness recebe loop+tools+UI prontos; o usuário de um framework recebe grafo/estado/abstrações e monta o resto. Por isso o template de 12 dimensões não se aplica direto — metade viraria "traga o seu". A pergunta certa é dupla: **o que o framework impõe** (e com que qualidade) e **o que deixa aberto** (e com que ergonomia).

## O panorama (2026)

| Framework | Origem | Filosofia | Estado |
|---|---|---|---|
| **LangGraph** | LangChain | grafo de estados explícito; checkpointing/persistência como núcleo | 1.0 GA (out/2025); líder em buscas e adoção enterprise |
| **CrewAI** | independente | multi-agente por papéis (personas + tasks); prototipagem rápida | v1.10 com MCP e **A2A nativos**; ~44k estrelas |
| **Microsoft Agent Framework** | Microsoft | fusão **Semantic Kernel + AutoGen** (1.0 em abr/2026); enterprise/.NET+Python | consolidação de dois legados em um |
| **OpenAI Agents SDK** | OpenAI | sucessor do Swarm; handoffs, guardrails, sessions; 100+ modelos não-OpenAI | v0.10; produção |
| **Claude Agent SDK** | Anthropic | o harness do Claude Code como biblioteca (subagentes hierárquicos, fallback chains) | ultrapassou AutoGen em deployments de produção (telemetria fev–abr/2026) |
| **Pydantic AI** | Pydantic | tipagem/validação como fundação; DX Python | V2 estável (jun/2026) |
| **Mastra** | ex-Gatsby | TypeScript-first; workflows + agentes + evals integrados | crescendo no ecossistema JS |
| **smolagents** | Hugging Face | **code-as-action** (o agente escreve Python em vez de JSON tool calls); minimalismo | nicho de pesquisa/edu |

Convergência já visível: **todos os principais têm MCP nativo** — a camada de frameworks foi a primeira a padronizar integralmente na camada de protocolos (cap. 17).

## Relação com as outras camadas (o mapa completo do livro)

```
Protocolos (cap. 17)      MCP · A2A · ACP · SKILL.md · AGENTS.md
        ↑ falados por ↑
Harnesses prontos         opencode, Codex, Goose, OpenClaw, Hermes...   ← benchmark, categorias 1–2
Harnesses embutidos       n8n (nó agente sobre LangChain)               ← benchmark, categoria 3
Frameworks                LangGraph, CrewAI, Agents SDK, Claude SDK...  ← benchmark, categoria 4 (esta nota)
        ↓ dois movimentos cruzados ↓
```

Dois movimentos tornam a fronteira harness/framework porosa — e são o achado central desta pesquisa:

1. **Harnesses virando frameworks**: o OpenHands extraiu o núcleo para `software-agent-sdk`; o Codex expõe App Server + SDKs; o Claude Code virou o Claude Agent SDK; o opencode V2 separa core/protocol/client. Os melhores harnesses estão se decompondo em frameworks + control-planes.
2. **Frameworks embutidos em produtos**: o nó de agente do n8n é LangChain por dentro (cap. 15). Quem avalia "o n8n" está avaliando também as escolhas do LangChain.

Consequência para o benchmark: avaliar frameworks fecha o ciclo — passaremos a conseguir rastrear *de onde vem* cada dimensão de um harness composto (própria, do framework, ou do motor que o hospeda).

## Instrumento: FRAMEWORK_EVAL (proposto)

Template adaptado criado em `benchmark/template/FRAMEWORK_EVAL.md`. Eixos: primitivas oferecidas (grafo/loop, estado/checkpointing, HITL, streaming, multi-agente), o que impõe vs. deixa aberto, protocolos falados, qualidade de produção (durabilidade, observabilidade, deploy), ergonomia (código mínimo até um agente útil) e ecossistema.

## Fila proposta (aguardando forks)

**Lote frameworks-1:** LangGraph (`langchain-ai/langgraph`), OpenAI Agents SDK (`openai/openai-agents-python`), Claude Agent SDK (`anthropics/claude-agent-sdk-python`), CrewAI (`crewAIInc/crewAI`) — os quatro cobrem as filosofias grafo, handoffs, harness-como-SDK e papéis.
**Lote frameworks-2:** Microsoft Agent Framework, Pydantic AI, Mastra, smolagents.
**Conexão direta:** `OpenHands/software-agent-sdk` (já na fila da categoria código) é também um framework — avaliá-lo com os dois templates será o teste de estresse do instrumento.

## Fontes

- [LangChain — The best AI agent frameworks in 2026](https://www.langchain.com/resources/ai-agent-frameworks)
- [Let's Data Science — AI Agent Frameworks 2026](https://letsdatascience.com/blog/ai-agent-frameworks-compared)
- [Alice Labs — 7 frameworks compared](https://alicelabs.ai/en/insights/best-ai-agent-frameworks-2026)
- [GuruSup — Best Multi-Agent Frameworks 2026](https://gurusup.com/blog/best-multi-agent-frameworks-2026)
- [OpenAgents — frameworks comparison](https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared)

> Ressalva: números (estrelas, versões, telemetria de adoção) vêm de fontes secundárias; validar nos repositórios quando entrarem no benchmark.
