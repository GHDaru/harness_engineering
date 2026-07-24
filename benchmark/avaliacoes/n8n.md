# HARNESS_EVAL — n8n (nó AI Agent)

## Metadados

- **Repositório / versão avaliada:** github.com/n8n-io/n8n · snapshot 2026-07 (fork GHDaru/n8n, commit 55e92cc2); pacote avaliado: `packages/@n8n/nodes-langchain` v2.32.0 (135 nós de IA)
- **Linguagem / stack:** TypeScript sobre **LangChain JS** (`langchain` 1.2.30, `@langchain/classic` 1.0.27 — onde vivem AgentExecutor/createToolCallingAgent — + `@langchain/langgraph` 1.0.2 e ~20 pacotes de provider)
- **Licença:** ⚠️ **fair-code (Sustainable Use License)** — código-fonte legível, mas não open source OSI
- **Data da avaliação:** 2026-07-24 (rodada 2) · **Categoria:** harnesses embutidos (não ranqueado contra harnesses dedicados)
- **Pergunta da categoria:** não "quanto scaffolding tem", mas **o que o motor de workflow dispensa de scaffolding**

## Dimensões (resumo com evidência)

### 1. Loop do agente — Nota: 3 (a hipótese evoluiu)
A hipótese "o loop é do LangChain" vale integralmente só para as versões antigas: **V2** usa `AgentExecutor.fromAgentAndTools` clássico (`maxIterations` default 10, streaming via `streamEvents` v2). Mas a **V3** refuta parcialmente: ainda usa `createToolCallingAgent` do LangChain *para decidir* qual tool chamar, porém **não usa mais o AgentExecutor** — as tool calls viram `EngineRequest` devolvidos ao **motor de workflow do n8n**, que agenda os nós-tool e reentra no agente com `EngineResponse` (`ToolsAgent/V3/helpers/runAgent.ts`). O n8n **reinternalizou o loop de execução**: a decisão é do framework, a execução é do engine. Suporta fallback model e `continueOnFail` por item.

### 2. Entrega de contexto — Nota: 2
`ChatPromptTemplate`: system message livre (default trivial "You are a helpful assistant") + `{chat_history}` + input + **passthrough rico de binários** (imagens, PDFs com detecção de Responses API, texto inline). Sem arquivo de regras, sem hierarquia, sem injeção automática de contexto do workflow — o autor mapeia via expressões `{{ $json... }}`.

### 3. Compactação — Nota: 1
Inexistente no loop: apenas `contextWindowLength` (janela de N interações dos memory sub-nodes) e corte por `maxTokensFromMemory`. Sem rolling summary do histórico do agente.

### 4. Design de ferramentas — Nota: 3 ⭐ (o mecanismo distintivo)
`create-node-as-tool.ts` (packages/core): **qualquer nó marcado `usableAsTool` vira `DynamicStructuredTool`** — o traversal dos parâmetros coleta chamadas **`$fromAI('chave', 'descrição', tipo)`** e gera schema Zod automaticamente; os slots `$fromAI` são exatamente os argumentos que o LLM preenche. Tools nativas: ToolWorkflow (sub-workflow como tool), ToolHttpRequest, ToolCode (JS/Python), ToolVectorStore, ToolThink (scratchpad). Output Parser conectado injeta a tool `format_final_json_response` para saída estruturada.

### 5. MCP — Nota: 3
Bidirecional: **MCP Client Tool** (SSE + Streamable HTTP, Bearer/OAuth2, filtro de tools, cache de sessão por execução) e **MCP Server Trigger** (`McpTrigger` + `McpServer.ts`) — expõe as tools n8n conectadas como endpoint MCP para clientes externos. SDK oficial.

### 6. Permissões e sandboxing — Nota: 2
A permissão é **estrutural**: o autor do workflow escolhe quais nós ficam plugados na porta `AiTool` — allowlist por construção, sem aprovação por chamada dentro do loop. Mas há **HITL real**: nós `sendAndWait` (Slack, Outlook...) pausam a execução aguardando aprovação humana, propagados na V3 via `action.metadata.hitl` — e **HITL é proibido dentro de sub-agentes** (`assertNoHitlActions`). Nó **Guardrails** para filtragem de conteúdo; ToolCode em task-runner isolado.

### 7. Memória e estado — Nota: 3
Sub-nós de memória plugáveis (`BaseChatMemory`): buffer window, **Postgres, Redis, MongoDB, Xata, Zep, Motorhead**; sessão por `sessionKey` (default `{{ $json.sessionId }}`); `MemoryManager` para ler/editar histórico programaticamente; `loadMemory`/`saveToMemory` por item com contabilização no tracing.

### 8. Planejamento — Nota: 1
O Plan-and-Execute Agent existe mas é **legado** (só selecionável na V1, junto com ReAct/Conversational); V2/V3 convergiram para o Tools Agent puro. Planejamento ficou implícito no modelo (+ ToolThink opcional).

### 9. Subagentes / orquestração — Nota: 3
**AI Agent Tool** (`AgentTool.node.ts` v3): um agente completo como tool de outro — o V3 roda o loop do sub-agente inline (`resolveSubAgentRequest`, reentrando até produzir output), com proibição de HITL aninhado; **ToolWorkflow**: sub-workflows inteiros como tools. Orquestração hierárquica visual.

### 10. Verificação / evals — Nota: 2
Feature de produto **Evaluations** (nós Evaluation Trigger + Evaluation, UI dedicada enterprise) para rodar datasets contra workflows; suíte de evals com LLM-judge no AI Workflow Builder; testes de integração por workflow (`agent-v3-with-tool.json`, `sub-agent-with-inner-tool.json`...).

### 11. Extensibilidade — Nota: 3
O ponto mais forte: **os 400+ nós de integração do n8n viram pool de tools** sem escrever código (via `usableAsTool` + `$fromAI`); community nodes com scanner de segurança (`scan-community-package`); ~20 providers de modelo (`LmChat*`).

### 12. Interfaces — Nota: 3
**Chat Trigger** (app de chat hospedado + widget `@n8n/chat` embarcável + streaming), Manual Chat Trigger, webhooks arbitrários, editor visual (canvas) como interface de construção, MCP Server Trigger.

### 13. Aprendizado / auto-melhoria (suplementar) — Nota: 0
Inexistente.

## Síntese

| Dimensões 1–12 | **Total: 29/36** — na categoria embutidos (não comparável diretamente aos dedicados) |
|---|---|

- **Perfil/arquétipo:** o **harness invertido** — o workflow contém o harness. A tese da categoria se confirma: as dimensões fracas (compactação 1, planejamento 1, contexto 2) são exatamente as que o ambiente dispensa (execuções curtas acionadas por eventos não acumulam contexto; o plano *é* o grafo do workflow desenhado pelo humano; o contexto vem mapeado das etapas anteriores). As fortes (tools 3, memória 3, interfaces 3, MCP 3) são onde o motor de workflow tem vantagem estrutural sobre harnesses dedicados.
- **Pontos mais fortes:** `$fromAI` → Zod (400+ integrações como tools de graça); V3 reinternalizando o loop no engine (o LangChain decide, o n8n executa); MCP bidirecional.
- **Pontos mais fracos:** compactação ausente (limita tarefas longas); permissão só estrutural (sem granularidade por ação); planejamento abandonado no legado.
- **Recurso distintivo:** a permissão estrutural — o LLM literalmente não tem acesso ao que não foi plugado no canvas. É allowlist por topologia, decidida visualmente por um humano.
- **"O que roubar" (pelos harnesses dedicados):** o padrão `$fromAI` (derivar schema de tool de parâmetros existentes de integrações); HITL como pausa durável de execução (não prompt síncrono).
- **Lição para o livro (cap. 15):** o harness embutido demonstra que várias dimensões do scaffolding são substituíveis pelo ambiente — mas a substituição tem teto: sem compactação nem planejamento, o nó de agente serve automações curtas, não trabalho longo autônomo. As duas camadas (workflow engine e harness dedicado) não competem: se complementam por duração e autonomia da tarefa.
