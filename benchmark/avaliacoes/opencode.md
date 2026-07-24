# HARNESS_EVAL — opencode

## Metadados

- **Repositório / versão avaliada:** github.com/anomalyco/opencode · v1.18.4 (V2 em transição, documentada em `CONTEXT.md`)
- **Linguagem / stack:** TypeScript + Effect-TS, runtime Bun, monorepo ~34 pacotes
- **Licença:** MIT
- **Data da avaliação:** 2026-07-24 (rodada 1, exploratória)
- **Posicionamento declarado:** produto — agente de código open source, provider-agnostic
- **Arquétipo observado:** produto cliente-servidor multi-superfície, com o desenho de contexto/estado mais formal da coorte

## Dimensões

### 1. Loop do agente — Nota: 3
Loop em `packages/opencode/src/session/processor.ts`: resposta do LLM consumida como `Stream` do Effect (`Stream.tap(handleEvent)` → `Stream.takeUntil(needsCompaction)` → `Stream.runDrain`), veredito explícito `continue | stop | compact`, retry por provedor (`SessionRetry.policy`), limite de passos. V2 formaliza durabilidade: inbox de prompts, eventos replayáveis com cursores.

### 2. Entrega de contexto — Nota: 3
`session/system.ts` monta environment + skills + instruções MCP. ~10 prompts por família de modelo (`session/prompt/*.txt`: anthropic, gpt, gemini, kimi...). `AGENTS.md` globais/ascendentes agregados por `session/instruction.ts`. V2: contexto como álgebra de "Context Sources" tipadas com snapshots e **Context Epochs** (cache-awareness formal) — único da coorte.

### 3. Compactação — Nota: 3
`session/compaction.ts` + `overflow.ts`: (a) sumarização automática em overflow com agente dedicado `compaction` e tail preservado (2k–8k tokens); (b) prune de tool outputs além de 40k tokens (`PRUNE_PROTECT`); (c) truncamento na origem com conteúdo integral movido para "Managed Tool Output Files" (nada se perde).

### 4. Design de ferramentas — Nota: 2
~14 tools + 3 experimentais (`tool/`), definidas com Effect Schema, descrições em `.txt` separados. Seleção por modelo (GPT recebe `apply_patch` em vez de `edit`/`write` — `registry.ts:293`). Ripgrep embutido. Arsenal enxuto e bem construído; menos categorias que os pares.

### 5. MCP — Nota: 3
`mcp/` (~1.000 linhas): stdio + Streamable HTTP + SSE com fallback, OAuth completo (PKCE, callback server, `opencode mcp auth`), reconexão, `ToolListChanged`, roots, prompts, resources e templates. Instruções do servidor entram no system prompt. A superfície de protocolo mais completa da coorte.

### 6. Permissões e sandboxing — Nota: 2
Rulesets com wildcards (`permission/`): `allow | ask | deny` last-match-wins, default `ask`, aprovação via `Deferred` + evento para a UI. Agentes com rulesets próprios; **subagentes derivam permissões restritas** (`agent/subagent-permissions.ts`). Porém **sem sandbox de SO no core** (containers só nos pacotes enterprise) — política sem contenção.

### 7. Memória e estado — Nota: 3
SQLite via Drizzle (`core/database`, `core/session/sql.ts`): sessões/mensagens/partes tipadas, hierarquia `parentID`, revert (`session/revert.ts`), compartilhamento (`share/`). V2: eventos duráveis replayáveis (`sessions.events`), snapshots entre reinícios. Sem memória de longo prazo dedicada (regras ficam em AGENTS.md).

### 8. Planejamento — Nota: 2
Plan mode como **agente `plan`** read-only; `plan_exit` (`tool/plan.ts`) escreve o plano em arquivo e transiciona para o agente `build` com aprovação do usuário. `todowrite` por sessão. Sem decomposição com dependências.

### 9. Subagentes / orquestração — Nota: 2
Tool `task` → sessão-filha com permissões derivadas, profundidade máxima 1, agentes definíveis em markdown (`primary|subagent|all`). Background experimental com retomada por `task_id`. Contido por design; sem comunicação inter-agente nem delegação remota.

### 10. Verificação / evals — Nota: 2
**LSP em runtime** (`lsp/`): edições disparam diagnósticos realimentados ao modelo — verificação do trabalho durante a tarefa, único da coorte. Política anti-mock explícita nos testes, `http-recorder` para provedores, typecheck obrigatório. Sem evals comportamentais nem baselines de regressão.

### 11. Extensibilidade — Nota: 3
Plugins = funções → `Hooks` com ~15 pontos, incluindo raros (transform de mensagens/system prompt, interceptar permissões, customizar compactação, **auth providers custom**). Tools do usuário auto-carregadas. **~26 loaders de provedor + centenas de modelos via models.dev** — o mais agnóstico de modelo em produção.

### 12. Interfaces — Nota: 3
Sete superfícies sobre a API HTTP tipada: TUI (SolidJS), **desktop Electron**, VS Code, GitHub Action, Slack, web/console, ACP (Zed). Sessões compartilháveis por link.

## Síntese

| # | Dimensão | Nota |
|---|---|---|
| 1 | Loop do agente | 3 |
| 2 | Entrega de contexto | 3 |
| 3 | Compactação | 3 |
| 4 | Ferramentas | 2 |
| 5 | MCP | 3 |
| 6 | Permissões/sandbox | 2 |
| 7 | Memória/estado | 3 |
| 8 | Planejamento | 2 |
| 9 | Subagentes | 2 |
| 10 | Verificação/evals | 2 |
| 11 | Extensibilidade | 3 |
| 12 | Interfaces | 3 |
| | **Total** | **31/36** |

- **Perfil/arquétipo:** produto multi-superfície com fundação formal — o harness que trata contexto e estado como problemas de sistemas distribuídos.
- **Pontos mais fortes:** álgebra de contexto com Context Epochs (`CONTEXT.md`); agnosticismo de provedor (~26 loaders); estado durável com eventos replayáveis.
- **Pontos mais fracos:** ausência de sandbox de SO no core; sem evals comportamentais.
- **Recurso distintivo:** Context Epochs — cache-awareness como conceito de primeira classe da arquitetura.
- **"O que roubar":** prompts por família de modelo; hooks profundos (transform de mensagens); truncamento que move conteúdo para arquivos em vez de descartar.
- **Cláusula de expiração:** prompts por família (expira com convergência de instruction-following); compactação em três camadas (expira com contexto longo barato).
