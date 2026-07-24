# HARNESS_EVAL — OpenClaw

## Metadados

- **Repositório / versão avaliada:** github.com/openclaw/openclaw · snapshot 2026-07 (fork GHDaru/openclaw, commit 1e15b18b)
- **Linguagem / stack:** Node.js/TypeScript, monorepo pnpm (~11.900 arquivos .ts em `src/`, 23 pacotes, 159 extensions, ~506 MB)
- **Licença:** MIT (OpenClaw Foundation)
- **Data da avaliação:** 2026-07-24 (rodada 2)
- **Categoria:** agentes pessoais self-hosted — avaliado nas 12 dimensões + a 13ª da categoria (proatividade)
- **Posicionamento declarado:** assistente pessoal self-hosted, single-user; o "Gateway" (daemon local) é a infra, o assistente é o produto
- **Arquétipo observado:** a plataforma mais completa da categoria — profundidade de produto maduro em todas as dimensões

## Dimensões

### 1. Loop do agente — Nota: 3
`src/system-agent/` (agent-turn.ts, chat-engine.ts) + `src/gateway/agent-*.ts`: runs serializados por *session lane* com write-lock file-based entre processos; três streams de eventos (lifecycle/assistant/tool); watchdogs de sessão travada (`stalled`/`stuck`); timeout com abort; sistema duplo de hooks (Gateway + plugins: `before_prompt_build`, `before/after_tool_call`, `agent_end`...).

### 2. Entrega de contexto — Nota: 3
`buildAgentSystemPrompt` injeta os arquivos de workspace: **`SOUL.md`** (persona/voz — separada das regras), **`AGENTS.md`** (operacional), `USER.md`, `IDENTITY.md`, `TOOLS.md`, `MEMORY.md`, `HEARTBEAT.md`, `BOOTSTRAP.md` — com orçamentos (20k chars/arquivo, 60k total) e truncamento marcado. Contribuições provider-aware acima/abaixo do **cache boundary** do provedor. A separação persona × regras é a contribuição da categoria à disciplina.

### 3. Compactação — Nota: 3
`src/context-engine/` + `docs/concepts/compaction.md`: auto-compactação por limiar e reativa (reconhece dezenas de strings de erro de overflow de múltiplos provedores), preservando pares tool-call/result no split; modo `safeguard` com **auditoria de qualidade do resumo**; **memory flush silencioso antes de compactar** (salva notas duráveis antes de perder contexto); `keepRecentTokens` 20k; providers de compactação plugáveis. Distingue compaction (semântica) de pruning (trim de tool results).

### 4. Design de ferramentas — Nota: 3
Suíte ampla (`src/agents/openclaw-tools*.ts`): runtime (exec/process/terminal), files, web, browser CDP, mensageria, sessões/subagentes, cron, mídia (imagem/música/vídeo/TTS), `ask_user`. Catálogos grandes via **Tool Search** e **Code Mode** (o modelo escreve JS/TS sobre um catálogo oculto). **52 AgentSkills bundled** (SKILL.md com frontmatter, gating por requisitos de bin/env/os) injetadas como bloco compacto — o modelo lê a skill sob demanda.

### 5. MCP — Nota: 3
**Client E server** — o único da coorte completo nos dois papéis. Server (`openclaw mcp serve`): expõe conversas dos canais via stdio a Codex/Claude Code. Client: registry `mcp.servers` com stdio/SSE/streamable-http, OAuth PKCE em SQLite, mTLS, filtros de tools, probe/doctor — e **filtro de segurança de env** em stdio (bloqueia `NODE_OPTIONS`, `LD_*`, `DYLD_*`). Suporte a MCP Apps com sandbox de origem isolada.

### 6. Permissões e sandboxing — Nota: 3 ⭐ (o ponto crítico da categoria, resolvido)
Defesa em profundidade real (`docs/security/THREAT-MODEL-ATLAS.md`, `src/security/`, `src/pairing/`): (a) **DMs são input não confiável** — `dmPolicy: "pairing"` por default: remetente desconhecido recebe código de pareamento e a mensagem **não é processada** até aprovação (allowlist SQLite); (b) **sandbox** multi-backend (Docker default com `network:none`, `readOnlyRoot`, `capDrop:ALL`; SSH; OpenShell) com modo `non-main` que sandboxa toda sessão que não seja a principal do dono — exatamente o cenário de terceiros; (c) política de tools por sandbox (nega browser/cron/gateway), binds bloqueando `/etc`, `~/.ssh`, docker.sock; (d) `openclaw doctor` e `security audit` embutidos; modelo de ameaça formal documentado. Caveat honesto: `sandbox.mode` é `off` por default para a sessão main — a segurança de terceiros depende de ativar `non-main` (o doctor sinaliza).

### 7. Memória e estado — Nota: 3
Memória em markdown no workspace: `MEMORY.md` (curada, carregada no início), `memory/YYYY-MM-DD.md` (diárias, indexadas), com `memory_search` (busca híbrida vetorial+keyword) e backends plugáveis (SQLite builtin, LanceDB, Honcho, wiki com claims/evidence). **Dreaming**: consolidação em background agendada que promove itens qualificados a `MEMORY.md` — a memória "dorme e consolida". Import de memórias do Codex/Claude Code. Sessões por canal com chaves estruturadas, persistência SQLite por agente.

### 8. Planejamento — Nota: 3
Quatro camadas: `update_plan` tool (plano multi-step, um `in_progress` por vez), **Goals** (um objetivo durável por sessão com token budget e estados, injetado por turno, visível na UI), **Task Flow** (orquestração durável com steps e estado JSON) e standing orders (políticas persistentes). Estratificação tática × durável que os harnesses de código não têm.

### 9. Subagentes / orquestração — Nota: 3
`sessions_spawn` cria subagentes isolados com **conclusão push-based** (announce de volta ao solicitante; `sessions_yield` como espera sem polling); nesting configurável (depth 1–5); política de tools **degradada por profundidade** (subagentes nunca ganham `message`/`gateway`/`cron`). Runtime **ACP para harnesses externos** — OpenClaw orquestra Claude Code, Gemini CLI, opencode e Codex como subagentes. Multi-agente no mesmo Gateway + Swarm via Code Mode.

### 10. Verificação / evals — Nota: 3
~8.649 arquivos de teste; prompt snapshots com drift-check em CI; stack QA com canal sintético e catálogo YAML de cenários; **Personal Agent Benchmark Pack** — 10 cenários específicos da categoria (`personal-redaction-no-secret-leak`, `personal-approval-denial-stop`, `personal-no-fake-progress`, `personal-memory-preference-recall`...) rodáveis em modo mock. O primeiro benchmark comportamental *da categoria agente pessoal* que encontramos.

### 11. Extensibilidade — Nota: 3
Skills no padrão **AgentSkills** (agentskills.io) com 6 níveis de precedência e registry público (**ClawHub**) com trust envelope + scan de segurança (VirusTotal/ClawScan); 159 plugins (tools, canais, provedores, hooks, mídia) com Plugin SDK; dezenas de provedores LLM com failover e rotação de auth profiles.

### 12. Interfaces — Nota: 3
**~23 canais de chat** (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, Teams, Matrix, Feishu, LINE, WeChat, QQ...), Control UI web, WebChat, CLI completa, TUI, **voz** (Voice Wake + Talk Mode contínuo), apps nativos (iOS/Android/macOS/Windows), Live Canvas (A2UI).

### 13. Aprendizado / auto-melhoria (suplementar) — Nota: 1
O **Dreaming** consolida memória autonomamente e o Skill Workshop mantém fila de propostas de skills — mas não encontramos autoria autônoma de skills pelo agente (o ciclo fechado do Hermes). A verificar em reavaliação.

### 14. Proatividade / agendamento (suplementar, categoria) — Nota: 3
Dois mecanismos complementares: **Heartbeat** (turnos periódicos, default 30min, com `activeHours` timezone-aware e modo `isolatedSession`+`lightContext` que reduz o custo de ~100k para 2–5k tokens por batida) e **Cron** embutido no Gateway (SQLite, tipos `at`/`every`/`cron`/`on-exit`/`stream`, delivery por canal/webhook, staggering, watchdogs). Wake por eventos externos (Gmail Pub/Sub, webhooks).

## Síntese

| # | Dimensão | Nota |
|---|---|---|
| 1–12 | Todas as dimensões padrão | 3 |
| 13 | Aprendizado (suplementar) | 1 |
| 14 | Proatividade (suplementar) | 3 |
| | **Total (1–12)** | **36/36** |

- **Perfil/arquétipo:** o OpenClaw está para a categoria "agentes pessoais" como o gemini-cli está para a de código — nenhuma dimensão fraca, e profundidade de produto em todas. (Mesma nota metodológica: um teto perfeito na estreia da categoria mede também a régua.)
- **Pontos mais fortes:** segurança de terceiros (pairing + sandbox non-main + threat model formal); proatividade (heartbeat com contexto leve); MCP client+server.
- **Pontos mais fracos:** sandbox `off` por default na sessão main (segurança depende de configuração); complexidade total do sistema (~506 MB, curva de operação alta).
- **Recurso distintivo:** orquestrar **outros harnesses** (Claude Code, Gemini CLI, opencode, Codex) como subagentes via ACP — o agente pessoal como maestro de agentes de código.
- **"O que roubar":** memory flush antes de compactar; conclusão push-based de subagentes (sem polling); separação SOUL.md (persona) × AGENTS.md (regras); heartbeat com sessão isolada de contexto leve.
- **Cláusula de expiração:** Tool Search/Code Mode sobre catálogos grandes expiram com atenção robusta a listas longas de tools; o Dreaming expira se memória nativa de longo prazo dos modelos amadurecer. Pairing e sandbox **não expiram** — são fronteira com o mundo.
