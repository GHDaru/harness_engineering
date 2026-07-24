# HARNESS_EVAL — gemini-cli

## Metadados

- **Repositório / versão avaliada:** github.com/google-gemini/gemini-cli · snapshot 2026-07 (main)
- **Linguagem / stack:** TypeScript, npm workspaces (`packages/core` + `packages/cli` + sdk, a2a-server, vscode-ide-companion)
- **Licença:** Apache-2.0
- **Data da avaliação:** 2026-07-24 (rodada 1, exploratória)
- **Posicionamento declarado:** produto — CLI de agente do Google Gemini
- **Arquétipo observado:** produto de plataforma com o regime de controle (policy/sandbox) e verificação (evals/baselines) mais rigoroso da coorte

## Dimensões

### 1. Loop do agente — Nota: 3
`packages/core/src/core/client.ts` (`MAX_TURNS=100`) com abstração de turno (`turn.ts`). **Next-speaker check** (`utils/nextSpeakerChecker.ts`): mini-prompt com schema `{reasoning, next_speaker}` decide se o modelo continua sozinho — re-invoca o stream recursivamente. `LoopDetectionService` aborta loops repetitivos. Separação core/cli limpa.

### 2. Entrega de contexto — Nota: 3
`prompts/promptProvider.ts` monta o prompt por modo/tools/modelo (snippets modernos vs. legados). `GEMINI.md` **hierárquico** (`utils/memoryDiscovery.ts`: global → pais → subpastas) com `@imports` (`memoryImportProcessor.ts`) e achatamento (`flattenMemory`). Override total via `GEMINI_SYSTEM_MD`. Injeção just-in-time (`tools/jit-context.ts`).

### 3. Compactação — Nota: 3
`context/chatCompressionService.ts`: dispara a 50% da janela, preserva últimos 30%, orçamento dedicado para function responses (50k), salvamento de outputs truncados. Camadas extras únicas: **tool distillation** e **output masking**. `/compress` manual, hooks `PreCompressTrigger`.

### 4. Design de ferramentas — Nota: 3
~20–25 tools como classes declarativas (`BaseDeclarativeTool` + `Invocation`), registro filtrado por allow/deny (`maybeRegister` em `config/config.ts`), declarações **por família de modelo** (`definitions/model-family-sets/`). Extras: shell com processos background, web search com grounding, tracker opcional (6 tools, dependências + grafo).

### 5. MCP — Nota: 3
`tools/mcp-client.ts` + `mcp-client-manager.ts`: stdio + SSE + Streamable HTTP. OAuth de nível corporativo (`mcp/`): callback local, storage de tokens, **Google auth e impersonation de service account**. Namespacing por servidor, prompts MCP, `/mcp`. Eval de prompt injection via MCP.

### 6. Permissões e sandboxing — Nota: 3
A referência da coorte. **Policy engine determinístico** (`policy/policy-engine.ts`): regras priorizadas com wildcards, **parsing estrutural de shell** (redirecionamentos, wrappers), regras em TOML. 4 `ApprovalMode` (default/autoEdit/yolo/plan). **Sandbox de SO**: 6 perfis Seatbelt (`sandbox-macos-*.sb`) + Docker/Podman com proxy. **Trusted folders** gatekeepam hooks/agents. Message-bus de confirmações.

### 7. Memória e estado — Nota: 3
Memória em `GEMINI.md` (tool `save_memory`, global + índice de projeto, auto-memory com evals). **Checkpointing git** (`services/gitService.ts`): snapshot antes de edições → `/restore` e `/rewind` desfazem o workspace, não só a conversa. `/resume`, gravação de chat (`chatRecordingService.ts`).

### 8. Planejamento — Nota: 3
`ApprovalMode.PLAN` + `enter/exit-plan-mode`; prompt lista as tools do modo; **`getApprovedPlanPath()` gatekeepa a execução** — só se implementa plano aprovado. `write-todos` + tracker com dependências e visualização. Eval própria (`evals/plan_mode.eval.ts`). Fecha as três garantias: read-only imposto, plano persistido, aprovação explícita.

### 9. Subagentes / orquestração — Nota: 3
`invoke_agent` sobre `AgentRegistry` (`agents/registry.ts`); 5 built-in (codebase-investigator, generalist, cli-help, browser, skill-extraction), cada um com modelo e política próprios; `AgentTerminateMode` (GOAL/MAX_TURNS/TIMEOUT). **A2A**: client com auth plugável + `a2a-server` expondo o próprio agente. Evals de delegação.

### 10. Verificação / evals — Nota: 3
Quatro suítes: `evals/` (~45 testes com **juiz LLM** — frugalidade, plan mode, delegação, shell safety, **injection via MCP**, sandbox recovery), `integration-tests/` (E2E com respostas gravadas `.responses`), `memory-tests/` e `perf-tests/` (baselines nightly). Comportamento do agente como superfície de regressão — único da coorte.

### 11. Extensibilidade — Nota: 3
**Extensions** (`gemini-extension.json`): um pacote agrega MCP servers, comandos TOML, hooks, políticas, skills e temas (`/extensions install/enable/link`). Hooks com registry/planner/aggregator e **gate de confiança** (`trustedHooks.ts`). Skills dinâmicas (`activate-skill`). Provedores: ecossistema Google (ancorado em modelo — o limite da nota não vem daqui, mas é o trade-off a registrar).

### 12. Interfaces — Nota: 3
TUI React/Ink com ~40 slash commands; **headless de primeira classe** (`-p` + `--output-format stream-json` NDJSON); VS Code companion (diffs, arquivos abertos); GitHub Action oficial; **ACP + A2A server**; SDK embutível.

### 13. Aprendizado / auto-melhoria (suplementar; retro 2026-07-24) — Nota: 3 ⭐
"Auto Memory" (experimental, off por default): no boot da sessão, com gates de elegibilidade (sessão ociosa ≥3h, ≥10 mensagens, throttle 30min, lock), o agente `skill-extraction-agent.ts` (~490 linhas, quase tudo prompt curatorial: "Default to NO SKILL", 5 perguntas de bloqueio, anti-padrões explícitos) lê transcrições passadas e produz **SKILL.md completos** + patches de memória em unified-diff — que caem numa **inbox** e só são aplicados com promoção humana (`/memory inbox`). Dedupe contra skills existentes, sandbox de escrita, dois evals dedicados. Design distinto do Hermes: curadoria autônoma, aplicação humana.

## Síntese

| # | Dimensão | Nota |
|---|---|---|
| 1 | Loop do agente | 3 |
| 2 | Entrega de contexto | 3 |
| 3 | Compactação | 3 |
| 4 | Ferramentas | 3 |
| 5 | MCP | 3 |
| 6 | Permissões/sandbox | 3 |
| 7 | Memória/estado | 3 |
| 8 | Planejamento | 3 |
| 9 | Subagentes | 3 |
| 10 | Verificação/evals | 3 |
| 11 | Extensibilidade | 3 |
| 12 | Interfaces | 3 |
| | **Total** | **36/36** |

- **Perfil/arquétipo:** o harness mais completo da rodada 1 — nenhuma dimensão abaixo de "referência" na coorte atual. (Nota metodológica: um 36/36 na primeira rodada indica também que a régua precisa de harnesses mais fortes por dimensão — é esperado que notas caiam quando Codex CLI e outros entrarem.)
- **Pontos mais fortes:** policy engine + sandbox de SO (contenção real); regime de evals com juiz LLM e baselines nightly; checkpointing git com `/rewind`.
- **Pontos mais fracos:** ancoragem no ecossistema Google (neutralidade de provedor); complexidade total do sistema (a superfície de configuração é grande).
- **Recurso distintivo:** as quatro suítes de verificação — comportamento do agente sob regressão contínua.
- **"O que roubar":** parsing estrutural de shell antes de julgar comandos; trusted folders para código de extensão; checkpoint git antes de cada edição.
- **Cláusula de expiração:** next-speaker check (expira com protocolos de turno nativos); compressão a 50% (expira com contexto longo barato); plan mode imposto (expira se modelos planejarem sob risco espontaneamente).
