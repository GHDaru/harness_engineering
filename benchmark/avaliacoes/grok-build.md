# HARNESS_EVAL — Grok Build (xAI)

> Rodada **ext-1** (2026-07-31) — promoção Radar→corpus (spec 064). Leitura sistemática de código no fork congelado.

## Metadados

- **Repositório / versão ou commit avaliado:** [github.com/xai-org/grok-build](https://github.com/xai-org/grok-build) · fork `GHDaru/grok-build`, commit `dd04f39` (export "Synced from monorepo", `SOURCE_REV 2a28b4a8`) · versão `0.2.116`
- **Linguagem / stack:** Rust 2024 (toolchain pin 1.92.0), 76 crates de workspace, ~1,48M linhas; TUI ratatui; MCP via `rmcp`; parsing de shell com **tree-sitter-bash**; scripting Rhai; SQLite (FTS5+vec0)
- **Licença:** Apache-2.0 (first-party); ports in-tree de codex e opencode sob suas licenças. **Contribuições externas não aceitas** (`CONTRIBUTING.md`)
- **Data da avaliação:** 2026-07-31 (aberto em 2026-07-15)
- **Posicionamento declarado:** TUI full-screen que entende o codebase, edita, executa shell, busca na web e gerencia tarefas longas — interativo, headless ou embutido via ACP
- **Arquétipo observado:** **produto de plataforma máximo** — o oposto simétrico do Pi na mesma rodada: cobre todas as dimensões com profundidade industrial, ao custo de uma base que só o dono do monorepo mantém.

## Dimensões

### 1. Loop do agente — Nota: 3
`acp_session_impl/turn.rs` (2.906 linhas): loop com `max_turns` configurável (CLI/frontmatter, herdado por subagentes), retry do sampler com 15 tentativas, jitter e header `x-should-retry` do servidor. O destaque é a **detecção de estagnação em duas camadas**: no cliente, `IdenticalToolCallRun` injeta um nudge explicativo após 8 tool calls idênticas e encerra em 16 (4 para no-ops); no servidor, sinais SSE de "doom loop" abortam o stream no meio e re-amostram quase sem espera ("loops são estocásticos — esperar não compra nada"). Crash handler async-signal-safe; turno não é retomável pós-crash (só workflows têm replay — ver distintivo).

### 2. Entrega de contexto — Nota: 3
Templates MiniJinja com variáveis que resolvem o toolset em runtime — **o prompt varia com as tools ativas**, não só com o modelo (`prompt/context.rs`); presets de comportamento versionados por tool (`versions.rs`) permitem pinar contratos para modelos antigos. Descoberta hierárquica multi-vendor: AGENTS.md/CLAUDE.md/CLAUDE.local.md + `.grok|.claude|.cursor/rules/`, cada vendor gateável (`compat.rs`); injeção como system-reminder **com escape do `<` inicial** para AGENTS.md hostil não forjar framing. Lacuna real: cache-awareness — `prompt_cache_key` existe no tipo e é sempre `None`; sem breakpoints de cache no backend Anthropic.

### 3. Compactação — Nota: 3
Crate dedicada (`xai-grok-compaction`) com três gatilhos (pré-sampling a 85%, pós-tool-outputs, troca de modelo que encolhe a janela) + caminho reativo classificando "prompt too long" como erro determinístico. Sumário LLM de 7 seções obrigatórias com re-tentativa se sair raso (<500 chars). Truncamento com derramamento em arquivo (MCP 20KB; bash 200KB truncado **pelo meio**, preservando início e fim). Requinte único no corpus: **prefire two-pass** — a primeira passada da compactação roda em paralelo 10% antes do limiar, escondendo a latência.

### 4. Design de ferramentas — Nota: 3
**~50 built-ins** em 8 categorias (núcleo, tarefas/concorrência, agendamento, planejamento, multimodal — imagem/vídeo —, memória, meta-tools MCP, e **ports das tools do codex e do opencode** no mesmo registry). Schema derivado de tipos (`schemars` draft-07); `ToolKind::is_read_only()` com match **exaustivo sem `_`** (tool nova é forçada a se classificar) e override por metadata testado; execução paralela via `FuturesUnordered` com resultados fora de ordem casados por slot e tools interruptíveis (`tokio::select!` contra interjeição do usuário).

### 5. MCP — Nota: 3
Cliente sobre `rmcp` com stdio, Streamable HTTP e SSE (com wrapper de backoff próprio para o reconnect-loop do rmcp — e teste de regressão do flood); **OAuth completo** (RFC 8414/9728, DCR, PKCE) com dedup de flow entre processos; `grok mcp doctor`; timeouts por servidor e por tool; lê `.mcp.json` e configs de Claude/Cursor. Meta-tools `search`/`use` fazem descoberta lazy para não inflar o prompt. Sem consumo de resources/prompts e sem modo servidor.

### 6. Permissões e sandboxing — Nota: 3 ⭐
A dimensão mais forte — 28k linhas só em `permission/`. Seis modos com pipeline de 5 etapas onde **deny rules e hooks valem até no yolo**; admins travam o bypass via `requirements.toml`. O diferencial: **autorização de shell por AST** (tree-sitter-bash, allowlist de node kinds), `shell_access.rs` fechando o bypass `mv secret x && cat x` e escalando para Ask quando o cwd fica "unpinnable" (`cd`/`env -C`), e `exec_risk.rs` cobrindo vetores obscuros (`sort --compress-program`, `git -c core.fsmonitor`, textconv, aliases `!`). Sandbox de SO fail-closed: Landlock/Seatbelt, deny kernel-enforced (bind-over de bubblewrap — **sem bwrap no Linux, recusa iniciar**), rede de filhos por seccomp, hooks do próprio agente write-denied pelo kernel. `RuleAction` default = Deny por CWE-1188. Trusted folders unificam MCP+LSP+hooks.

### 7. Memória e estado — Nota: 3
Diretório por sessão com fonte autoritativa em JSONL, resume por id/título com busca full-text, fork. **Checkpoints de três domínios por prompt** (snapshots de arquivo + hunks + HEAD/index do git — restaurados juntos), com suporte a **jj** além de git. Memória de longo prazo experimental: MEMORY.md global e por workspace (hash da identidade do repo — clones/worktrees compartilham), índice FTS5+vetorial com MMR, e o passe reflexivo "**dream**" que consolida contradições com gates de tempo/sessões. Até o SQLite é cuidadoso: WAL vs rollback conforme o filesystem (NFS causa SIGBUS).

### 8. Planejamento — Nota: 3
Plan mode com **enforcement real**: máquina de 4 estados; edições fora do `plan.md` são rejeitadas antes de executar **em qualquer modo de permissão, inclusive always-approve**; saída com preview scrollável e feedback inline por linha que volta ao modelo. Duas fugas documentadas com honestidade (bash não inspecionado para redirects; subagente write-capable escapa do tracker do pai). Além disso um **goal mode** com papéis LLM separados (planner/strategist/verifier/classifier), auto-pausa por estagnação de fingerprint e regras anti-"test theater" notáveis.

### 9. Subagentes / orquestração — Nota: 3 ⭐
`spawn_subagent` com tipos built-in e custom (`.grok/agents/*.md`), `capability_mode` **intersectado** com o toolset do tipo, herança de MCP por frontmatter, profundidade máxima 1, `resume_from`, contratos de I/O entre personas. **O anúncio dos worktrees se confirma no código**: `WorktreeBuilder…worktree_kind(WorktreeKind::Subagent)` (`handle_request.rs:302`) sobre a crate `xai-fast-worktree` — worktrees CoW com snapshots BTRFS O(1), overlayfs, metadata SQLite com auto-GC e merge de volta como operação de protocolo (`x.ai/git/worktree/apply`). Não é "temos worktrees": é worktree barato o bastante para o agente usar sem pensar.

### 10. Verificação / evals — Nota: 2
Escala industrial no mecanismo: 26.734 testes, harness PTY com baselines, fuzzing do renderer markdown, testes de segurança dirigidos (bypass de shell, templates encriptados). **LSP pós-edição de verdade**: `LspDiagnosticsReminder` relê o arquivo após cada edit e devolve os diagnósticos como system-reminder no resultado da tool. Mas **zero evals comportamentais** no tree — nenhuma suíte de tarefas, golden transcripts ou regressão de competência para um sistema cheio de heurísticas delicadas (nudge em 8, limiar 85%, classificador LLM de auto-mode). O rigor valida o mecanismo, não a competência. (Ressalva: o repo é export do monorepo; se os evals existem lá, o artefato público não é auditável nessa dimensão.)

### 11. Extensibilidade — Nota: 3 ⭐
**14 eventos de hook** com aliases por vendor (snake_case, camelCase, nomes do Cursor), fontes mescladas de `~/.grok`, `~/.claude/settings.json`, `.cursor/hooks.json` e plugins — o Grok Build é o harness mais **poliglota em compat** do corpus (lê regras, permissões, marketplaces e MCP configs dos ecossistemas vizinhos, e porta as tools do codex e do opencode). Skills com 7+ tiers de descoberta e **budget de contexto** para a listagem; plugins com marketplace por repo git (pin por SHA verificado pós-fetch), trust em duas fases; 3 backends de API de modelo (chat completions, Responses, Messages) com headers extras.

### 12. Interfaces — Nota: 3
TUI ratatui com dashboard multi-sessão, panes de tasks/todos, command palette e **renderização de Mermaid** (stack vendorizada); headless com 4 formatos de saída (schema alinhado ao formato de mensagens do Claude Code) e flags dedicadas; **ACP como protocolo primário** — `grok agent stdio` (Zed/Neovim/Emacs) e `grok agent serve` (WebSocket com estado que sobrevive a reconexão), com extensões proprietárias `x.ai/*`. Sem A2A; sem SDK first-party (a via é ACP); npm é wrapper de binário.

## Dimensões suplementares

### 13. Aprendizado / auto-melhoria — Nota: 2
O passe "**dream**": consolidação reflexiva agendada do MEMORY.md (merge, resolução de contradições — "fato recente desmente o antigo, fica só a verdade atual" —, datas relativas→absolutas), com locks e gates. Não escreve skills a partir da experiência; a skill `create-workflow` que orienta o agente a escrever scripts Rhai é de autoria humana.

### 14. Proatividade / agendamento — Nota: 3
Três mecanismos: tools de **scheduler** expostas ao modelo (intervalos ≥60s, `durable` entre sessões, journal de ocorrências para idempotência, cap de 50 tarefas/7 dias), `/loop` no TUI, e a tool **`monitor`** (cada linha de um comando longo vira notificação injetada na conversa, com controle de volume automático). Intervalos, não cron — dito explicitamente no código; sem webhooks.

## Síntese

### Tabela de notas

| # | Dimensão | Nota |
|---|---|---|
| 1 | Loop do agente | 3 |
| 2 | Entrega de contexto | 3 |
| 3 | Compactação | 3 |
| 4 | Ferramentas | 3 |
| 5 | MCP | 3 |
| 6 | Permissões/sandbox | 3⭐ |
| 7 | Memória/estado | 3 |
| 8 | Planejamento | 3 |
| 9 | Subagentes | 3⭐ |
| 10 | Verificação/evals | 2 |
| 11 | Extensibilidade | 3⭐ |
| 12 | Interfaces | 3 |
| | **Total (0–36)** | **35** |

### Leitura

- **Perfil/arquétipo:** plataforma máxima — empata com o Codex CLI (35) logo abaixo do gemini-cli (36), chegando ao corpus **duas semanas** depois de abrir o código. A tese do cap. 14 (convergência) em forma extrema: além de convergir nas features, ele **lê os artefatos dos concorrentes** (AGENTS/CLAUDE/Cursor/`.mcp.json`) e embute ports das tools deles.
- **3 pontos mais fortes:** autorização de shell por AST com fecho de bypass real (tree-sitter + `shell_access` + `exec_risk`, sandbox kernel-enforced fail-closed); detecção de loop em duas camadas com nudge antes do hard stop (cliente + sinal de servidor); subagentes em worktree com infraestrutura de verdade (`xai-fast-worktree`: CoW, BTRFS O(1), auto-GC, merge por protocolo).
- **2 pontos mais fracos:** ausência total de evals comportamentais no tree (26k testes de mecanismo, zero de competência); cache-awareness essencialmente ausente (`prompt_cache_key` sempre `None`) e complexidade beirando o insustentável para qualquer um fora do monorepo (config.rs de 523KB; subsistemas sobrepostos: plan mode + goal mode + workflows; 4 detectores de estagnação) — coerente com "external contributions are not accepted".
- **Recurso distintivo:** o **motor de workflows Rhai** com journal append-only e **replay determinístico** (divergência por `req_hash` falha ruidosamente), budget de agentes reservado antes do fan-out (painel que estouraria é rejeitado antes de lançar filhos) e `validate_only`. Semântica de durable execution (Temporal) dentro de um harness de código — nenhum outro avaliado tem orquestração multi-agente programável, com budget hard e retomável.
- **"O que roubar":** (1) o nudge de estagnação em dois limiares (~120 linhas: avisar aos 8, matar aos 16, limiar 4 para no-ops); (2) o gate de acesso a arquivo via AST de shell — a classe de bypass que quase todo harness deixa aberta; (3) o journal de host calls com replay determinístico para orquestração multi-agente sobreviver a quedas.
- **Cláusula de expiração:** os 4 detectores de estagnação e o classificador LLM de auto-mode existem porque os modelos atuais entram em loop e pedem julgamento externo — melhoram os modelos, encolhe essa camada. O prefire de compactação e o budget de skills existem porque a janela é cara. Os templates XOR-ofuscados ("obfuscation, not security", admite o código) tendem a cair com a maturidade do produto aberto.
