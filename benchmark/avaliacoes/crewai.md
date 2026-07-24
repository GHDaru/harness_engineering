# FRAMEWORK_EVAL — CrewAI

## Metadados

- **Repositório / versão avaliada:** github.com/crewAIInc/crewAI · v1.15.6 (fork GHDaru, commit b3aaaab) — monorepo com 6 pacotes (`crewai`, `crewai-core`, `crewai-tools` ~79 tools, `cli`, `crewai-files`, `devtools`)
- **Linguagem / stack:** Python · **Licença:** MIT (com suíte comercial AMP) · **Data:** 2026-07-24 (rodada frameworks-1)
- **Filosofia declarada:** multi-agente por papéis (Crews: role/goal/backstory + tasks) + orquestração event-driven (Flows)
- **Origem:** vendor único (CrewAI Inc.), caminho ergonômico convergindo para o SaaS AMP

## Eixo A — Primitivas (18/18)

### A1. Loop / orquestração — 3
Executor **100% próprio — zero LangChain** (`crew_agent_executor.py`, 1.648 linhas): dispatch duplo — tool-calling nativo quando o LLM suporta, fallback para loop ReAct clássico (parse de `Thought:/Action:` com json_repair), com fallback *cruzado* em erro. Três primitivas: **Crews** (sequential/hierarchical), **Flows** (grafo event-driven `@start/@listen/@router`, runtime de 3.771 linhas) e **LiteAgent** (`Agent.kickoff()` solo). Executor experimental em state machine (3.232 linhas) como futuro.

### A2. Estado e durabilidade — 3
Flow state Pydantic ou dict com `@persist` (SQLite, após cada método) e **resume cross-processo** (`Flow.from_pending()` + `resume(feedback)`). Acima disso, um sistema novo de **checkpoint universal por evento** (`src/crewai/state/`): ~50 tipos de evento disparam snapshot do `RuntimeState` inteiro, com fork e restore — e uma TUI de checkpoints na CLI. Memória **unificada** (`unified_memory.py`: remember/recall/forget/scope) — os antigos Short/Long/Entity Memory foram removidos.

### A3. Tools e schemas — 3
Pydantic puro (`args_schema` gerado por introspecção via `create_model`), com governança real de execução: `cache_function`, `max_usage_count`, `result_as_answer` (curto-circuita o loop), reprompt em `ValidationError`. Catálogo `crewai-tools` com **79 diretórios** (busca, scraping, RAG por tipo de arquivo, bancos, sandboxes E2B/Daytona, multimodal). Interop bidirecional com LangChain como opcional.

### A4. Multi-agente — 3
Delegação implementada **como tools comuns** (`DelegateWorkTool`/`AskQuestionTool`): matching de `role` em texto livre cria uma Task sintética e chama o coworker recursivamente (robusto: role errado devolve erro i18n com a lista, não exceção — mas frágil por depender do LLM acertar o nome). Modo hierárquico com manager sintetizado (e proibido de ter tools próprias).

### A5. Human-in-the-loop — 3
Três superfícies: `Task(human_input=True)` (re-roda o loop até aprovação), decorator `@human_feedback` em Flows (**pausa persistida em SQLite e retomada em outro processo**), e hooks de tool/LLM com `request_human_input`. `HumanInputProvider` é Protocol — plugável para Slack/HTTP.

### A6. Streaming / eventos — 3
Event bus singleton com 20 módulos de tipos de evento, handlers sync/async, **grafo de dependências entre handlers** e modo `replay()` (base do checkpoint). Streaming de tokens real (`kickoff(stream=True)` → output iterável; `LLMThinkingChunk` para reasoning).

## Eixo B — Fronteiras

- **Impõe (rígido):** `role`/`goal`/`backstory` obrigatórios sem default — não existe agente sem persona; `Task` exige `description` + `expected_output`. A metáfora de RPG é estrutural. Escapes existem (LiteAgent, Flows com Python puro), mas ignoram metade do framework.
- **Deixa aberto:** executor trocável, `HumanInputProvider`/`FlowPersistence`/checkpoint provider como ABCs, hooks before/after de LLM e tool, guardrails custom, i18n de todos os prompts.
- **Lock-in:** LangChain **removido**; LiteLLM rebaixado a fallback opcional (17 provedores com clientes nativos próprios). O lock-in real é **comercial**: tracing first-party aponta para o backend AMP, CLI cheia de `login/deploy/org/enterprise`, telemetria anônima por default (desligável). O framework roda 100% offline — mas o caminho ergonômico leva ao plano pago.

## Eixo C — Protocolos

| MCP client | MCP server | A2A | ACP | SKILL.md | AGENTS.md |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✅ **obrigatório** (3 transportes, cache, retry, filtros, `Agent(mcps=[...])`) | — | ✅ **client E server** (AgentCard completo, JWS, gRPC/REST; extra `[a2a]`) | — | ✅ (skills com progressive disclosure + CLI create/install/publish) | ✅ **gerado por `crewai create`** em todo projeto novo |

Achado para o cap. 17: o CrewAI quebra o "A2A é aposta de um só" — é o segundo implementador medido, e o primeiro *framework*, com client e server. E o template de `AGENTS.md` auto-gerado (com seção "Patterns to NEVER use") é adoção ativa do padrão, não passiva.

## Eixo D — Produção (11/12)

### D1. Observabilidade — 2
Telemetria OTel anônima própria + tracing rico via event bus — mas o destino first-party é o backend AMP (gate `CREWAI_TRACING_ENABLED`); sem exporter OTel genérico de traces de agente. Compensa com **18 integrações** documentadas plugando via `BaseEventListener` (o desenho certo).

### D2. Testes e evals — 3
313 arquivos de teste, **598 cassettes VCR**, pytest-randomly (ordem aleatória), mypy strict, ruff com bandit, pip-audit. Evals em duas camadas (`crewai test` + `AgentEvaluator` com 6 métricas LLM-as-judge) — ainda sob `experimental/`.

### D3. Ergonomia — 3
`crewai create crew` → 2 YAMLs de ~18 linhas + ~48 linhas de Python decorado; variantes 100% declarativas (crew em JSONC, flow em YAML). ~10 linhas de código estrutural até uma crew útil.

### D4. Ecossistema — 3
CLI com ~45 comandos (incluindo TUIs de run/memória/checkpoint, `train`, `replay`, `chat`); templates; marketplace de skills (inclusive plugin para Claude Code); adapters para LangGraph e OpenAI Agents SDK.

## Síntese

- **Totais:** A **18/18** · D **11/12**
- **Perfil:** o framework certo para multi-agente por papéis com prototipagem rápida — e o CrewAI de 2026 é outro produto: sem LangChain, LLM clients nativos, checkpoint universal, MCP obrigatório e A2A bidirecional. Engenharia séria (cassettes, mypy strict) sob uma fronteira conceitual deliberadamente rígida.
- **O que roubar:** checkpoint-por-evento com replay do bus; grafo de dependências entre event handlers; `AGENTS.md` auto-gerado em cada projeto novo com anti-padrões da versão.
- **Teste decisivo:** difícil *sem* ele: crew hierárquica com delegação, memória unificada e HITL persistido em ~70 linhas. Difícil *com* ele: qualquer agente que não caiba na ontologia papel/tarefa (o escape via Flows abandona metade do valor).
- **Riscos:** dois executores + dois loops + duas rotas de LLM coexistindo (superfície de manutenção); módulos gigantes crescendo rápido; caminho de produção convergindo para o SaaS.
