# FRAMEWORK_EVAL — OpenAI Agents SDK (Python)

## Metadados

- **Repositório / versão avaliada:** github.com/openai/openai-agents-python · v0.18.3 (fork GHDaru, commit 5976333)
- **Linguagem / stack:** Python (~18.6k linhas em `src/agents/`; deps mínimas: openai, pydantic, griffe, **mcp obrigatório**)
- **Licença:** MIT · **Data:** 2026-07-24 (rodada frameworks-1)
- **Filosofia declarada:** primitivas mínimas (Agent, Runner, handoffs, guardrails) — sucessor do Swarm
- **Origem:** vendor único (OpenAI)

## Eixo A — Primitivas (18/18)

### A1. Loop / orquestração — 3
`Runner.run/run_sync/run_streamed` sobre um `AgentRunner` **substituível**; loop explícito em `run.py` (modelo → output_type termina → handoff troca agente → tools e repete), `max_turns` com handlers de erro interceptáveis (e desativável); `Agent` é dataclass declarativa com `tool_use_behavior` configurável e `as_tool()`. O `run_internal/` com 21 módulos (tool_caller, approvals, session_persistence...) mostra loop maduro, não um while de 50 linhas.

### A2. Estado e durabilidade — 3
Duas camadas: **`RunState`** (`run_state.py`, 3.787 linhas — o maior arquivo do SDK) — snapshot serializável *no meio do turno* com **schema versionado** (v1.13) e resume real via `Runner.run(agent, state)`; e **`Session`** (Protocol de 4 métodos) com 9 backends (SQLite, Redis, SQLAlchemy, MongoDB, Dapr, Encrypt, OpenAI Conversations, compaction session...). Temporal via integração externa oficial (extra `[temporal]`).

### A3. Tools e schemas — 3
`@function_tool` deriva schema de type hints (Pydantic) e docstrings (griffe, com **auto-detecção de estilo** google/numpy/sphinx); 13 tipos de tool incluindo hosted (WebSearch, Computer, CodeInterpreter, Shell com política de rede, ApplyPatch); `is_enabled`/`needs_approval` por tool; guardrails por tool; `as_tool()` com input estruturado e propagação de stream.

### A4. Multi-agente — 3
**Handoffs** como primitiva distinta: implementados como tool call (`transfer_to_<agent>`) que troca o agente corrente preservando histórico, com `input_filter` (ex.: `remove_all_tools`), payload tipado validado, prompt prefix recomendado, e histórico **aninhável** em vez de linearizado (`nest_handoff_history`). Orquestração via código documentada como cidadã de primeira classe (17 padrões em `agent_patterns/`).

### A5. Human-in-the-loop — 3 ⭐ (o diferencial da coorte)
Fluxo completo: `needs_approval` → o run **pausa** com `RunResult.interruptions` → `result.to_state()` serializa → `state.approve/reject` (com decisões *sticky* que sobrevivem à serialização) → `Runner.run(agent, state)` retoma. Cobre function tools, MCP, shell/patch, agentes aninhados (aprovação sobe ao run externo) e funciona em streaming. Pausa/aprova/retoma atravessando processo e disco — quase nenhum concorrente entrega isso.

### A6. Streaming / eventos — 3
Três níveis: `raw_response_event` (deltas token-a-token), `run_item_stream_event` (semântico: tool_called, handoff_occured, mcp_approval_requested...) e `agent_updated_stream_event` (troca por handoff). Cancelável; HITL e guardrails funcionam em streaming.

## Eixo B — Fronteiras

- **Impõe:** o **schema de itens da Responses API** permeia tudo (`TResponseInputItem`, reasoning items, hosted tools) — providers alheios entram por *conversão*, não por abstração neutra. Default: Responses API + modelo OpenAI.
- **Deixa aberto:** `Model`/`ModelProvider` são ABCs limpas; **LiteLLM e any-llm first-class** (100+ modelos) com testes de integração; guardrails em três níveis (agente, run, tool) como primitiva.
- **Lock-in real:** funciona com qualquer modelo, mas fora da OpenAI perde-se uma fatia grande da superfície (hosted tools, conversations, realtime) — agnosticismo verdadeiro na execução, assimétrico em recursos.

## Eixo C — Protocolos

| MCP client | MCP server | A2A | ACP | SKILL.md | AGENTS.md |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✅ 3 transportes + hosted + filtering/retry/aprovação | — | ❌ zero (nem da própria casa é o caminho) | — | parcial (skills inline no ShellTool) | ✅ só nos Sandbox Agents (spec embutida no prompt) |

## Eixo D — Produção (11/12)

### D1. Observabilidade — 2
Tracing nativo ligado por default com spans automáticos e ABCs públicas de processor/exporter — mas o destino default é a **plataforma OpenAI** e **não há exporter OTel nativo**; o ecossistema compensa (~28 integrações externas: Langfuse, LangSmith, Datadog, Logfire...).

### D2. Testes — 3
295 arquivos com `FakeModel` determinístico e snapshot testing, mais `integration_tests/` contra API real (providers, packaging, realtime).

### D3. Ergonomia — 3
5–13 linhas até um agente útil; **216 exemplos** organizados por tema; REPL embutido; visualização de grafo; docs traduzidas (ja/ko/zh) e `llms.txt` para consumo por LLMs.

### D4. Ecossistema — 3
Extras modulares (litellm, temporal, viz, voice, realtime, sandbox providers: Daytona, E2B, Modal, Cloudflare...); duas trilhas de voz (VoicePipeline STT→agent→TTS e RealtimeAgent); e os **Sandbox Agents** (beta) — manifesto de workspace, snapshots, memória em duas fases, Docker/local — o SDK invadindo o território dos harnesses de código.

## Síntese

- **Totais:** A **18/18** · D **11/12**
- **Perfil:** o framework certo para agentes conversacionais/de processo com aprovação humana no meio — HITL serializável, handoffs e sessions são o trio que o distingue; e os Sandbox Agents sinalizam a ambição de virar harness completo.
- **O que roubar (para harnesses prontos):** o `RunState` serializável com schema versionado (pausa de dias entre aprovação e retomada); auto-detecção de estilo de docstring para schema; guardrails em três níveis.
- **Teste decisivo:** difícil de construir *sem* ele: pausar um run multi-agente no meio de um turno, gravar em disco, aprovar amanhã e retomar exatamente de onde parou. Difícil de construir *com* ele: qualquer coisa que dependa de recursos simétricos entre provedores.
- **Riscos:** 3.787 linhas de serialização manual num schema já em v1.13 (regressão silenciosa em upgrades); vocabulário Responses como acoplamento estrutural.
