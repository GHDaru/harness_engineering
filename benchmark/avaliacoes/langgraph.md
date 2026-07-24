# FRAMEWORK_EVAL — LangGraph

## Metadados

- **Repositório / versão avaliada:** github.com/langchain-ai/langgraph · langgraph 1.2.9 (fork GHDaru, commit 1e1ca88) — monorepo: core (~28k LOC), prebuilt, checkpoint (+postgres/sqlite/conformance), cli, sdk-py; **~63k LOC de testes (2,3× o código)**
- **Linguagem / stack:** Python (JS em repo separado) · **Licença:** MIT (servidor `langgraph-api` é externo e comercial) · **Data:** 2026-07-24 (rodada frameworks-1)
- **Filosofia declarada:** *"low-level orchestration framework for building stateful agents"* — assume não ser harness pronto
- **Origem:** LangChain Inc.

## Eixo A — Primitivas (16/18)

### A1. Loop / orquestração — 3
A primitiva real é **Pregel/BSP** (supersteps + channels + reducers), com `StateGraph` como açúcar. Roteamento estático, condicional e dinâmico (`Command(goto=...)`), fan-out map-reduce via `Send` (com timeout por task), e por nó: retry policy, cache policy, timeout com heartbeat, error handler, `defer`. API funcional (`@entrypoint`/`@task`) dá o mesmo motor sem grafo. **Porém**: o "agente pronto" (`create_react_agent`) está **formalmente deprecado** — migrou para `langchain.agents`; o LangGraph está se esvaziando deliberadamente da camada de agente.

### A2. Estado e durabilidade — 3 ⭐⭐ (hipótese confirmada: a referência do mercado)
`BaseCheckpointSaver` com 24+ métodos (incluindo `copy_thread`, `prune`, histórico incremental por canal), 3 backends oficiais + variantes *shallow* + **suíte de conformidade publicável** para savers de terceiros. `durability` em três modos (sync/async/exit) com retomada automática pós-falha. **Time-travel** real: `get_state_history`, replay por `checkpoint_id`, fork via `update_state`, `bulk_update_state`. Memória longa com **busca vetorial nativa** (`BaseStore` + pgvector/HNSW + TTL). E raridades de segurança: serializer criptografado (AES) e **allowlist de desserialização** msgpack — mitigação que quase nenhum concorrente tem.

### A3. Tools e schemas — 2
Definição 100% herdada do `langchain-core` (não há `@tool` neste repo). O que o LangGraph adiciona é execução de qualidade: `ToolNode` paralelo com tratamento de erro configurável, injeções ocultas (`InjectedState`, `InjectedStore`, `ToolRuntime` com stream_writer), tools retornando `Command` (handoff). Sem permissões/políticas por tool.

### A4. Multi-agente — 2
Primitivas genuinamente composicionais: qualquer grafo compilado é nó de outro (namespace de checkpoint próprio), handoff via `Command(goto, graph=PARENT)`, `Send` para fan-out. **Mas os padrões não estão aqui**: supervisor, swarm e Deep Agents são pacotes/repos separados; o dev recebe mecanismos, não padrões — e `examples/` está oficialmente arquivado.

### A5. Human-in-the-loop — 3
`interrupt()` como **primitiva de linguagem**: chamada de dentro de qualquer nó, persiste o estado, o processo pode morrer, e `Command(resume=valor)` retoma dias depois em outra máquina — com semântica de reexecução do nó documentada com honestidade e resolução por ordem ou por id. Breakpoints estáticos e `update_state` para o humano editar antes de retomar.

### A6. Streaming / eventos — 3
**7 modos** combináveis e tipados (values/updates/checkpoints/tasks/debug/messages/custom), cada evento com namespace de subgrafo (streaming hierárquico nativo); `stream_events` v3 com **transformers plugáveis** (o dev define seus próprios tipos de evento). `RemoteGraph` replica a API contra servidor.

## Eixo B — Fronteiras

- **Impõe:** o modelo BSP inteiro — nós não se chamam, escrevem em canais; estado tipado com reducers; tudo precisa serializar; `thread_id` obrigatório com checkpointer. **O loop do agente é seu** — quem escreve model→tools→model é o dev.
- **Deixa aberto (demais):** gestão de contexto/compactação — **zero suporte nativo** (uma menção em docstring sugerindo `pre_model_hook`); permissões/sandbox/política de tools — inexistentes. Os dois maiores gaps para harness de longa duração.
- **Lock-in:** o README diz "can be used without LangChain" — verdade para o pacote `langchain`, **falso para `langchain-core`** (obrigatório: mensagens, Runnable, BaseTool permeiam o núcleo). Tudo no repo é MIT; a fronteira paga é o servidor externo (`langgraph-api`: assistants, crons, Studio, `/mcp`). LangSmith não é dependência (tracing via callbacks, opt-in).

## Eixo C — Protocolos

| MCP client | MCP server | A2A | ACP | SKILL.md | AGENTS.md |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ❌ (adapter em outro repo) | ❌ (feature do servidor **pago**) | ❌ zero | ❌ | ❌ | só como guia de contribuição |

O mais fraco da coorte em protocolos: o único "protocolo" próprio é o REST do LangGraph Server — padrão de facto, não aberto.

## Eixo D — Produção (10/12)

### D1. Observabilidade — 2
Callbacks próprios sobre langchain-core; **sem OTel nativo** (só um teste de compatibilidade com instrumentação de terceiro); caminho feliz é LangSmith. Os stream modes `checkpoints`/`tasks`/`debug` funcionam como telemetria estruturada caseira de qualidade.

### D2. Testes — 3
Exemplares: 145 arquivos, ~63k linhas (2,3× o código), matriz de checkpointers/stores com containers reais, **testes de migração de checkpoint** e de deprecação, snapshots, benchmarks versionados com CI dedicado.

### D3. Ergonomia — 2
API concisa (~20-25 linhas para um grafo custom), mas **o repositório não ensina**: `examples/` declaradamente arquivado apontando para API deprecada; docs vivas só externas. Onboarding pelo código-fonte tem custo real.

### D4. Ecossistema — 3
Monorepo bem fatiado com versionamento independente por camada, política de deprecação explícita e testada, conformance suite para storage de terceiros, núcleo 1.x estável.

## Síntese

- **Totais:** A **16/18** · D **10/12**
- **Perfil:** quem adota LangGraph em 2026 adota um **runtime durável**, não um harness — durabilidade, estado e HITL são de classe própria e difíceis de replicar; a camada de agente (loop pronto, padrões multi-agente, contexto, políticas) foi deslocada para `langchain`/Deep Agents ou fica por sua conta.
- **O que roubar:** a suíte de conformidade para backends de terceiros; allowlist de desserialização; `interrupt()` como primitiva de linguagem; variantes shallow de checkpointer.
- **Teste decisivo:** difícil *sem* ele: time-travel com fork de estado num workflow multi-agente durável. Difícil *com* ele: um agente de código de longa duração — sem compactação nativa, a janela estoura e o framework não te salva.
- **Risco:** a dependência estrutural de `langchain-core` + a gravitação comercial do servidor externo definem o teto de neutralidade.
