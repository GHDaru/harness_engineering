# HARNESS_EVAL — OpenHarness

## Metadados

- **Repositório / versão avaliada:** github.com/HKUDS/OpenHarness · v0.1.9
- **Linguagem / stack:** Python ≥3.10 (~46 mil linhas, 230 arquivos em `src/`), TUI React/Ink (TypeScript), dashboard React
- **Licença:** MIT
- **Data da avaliação:** 2026-07-24 (rodada 1, exploratória)
- **Posicionamento declarado:** "open-source Python port of Claude Code" — infraestrutura leve de agente para pesquisadores/builders entenderem harnesses de produção; inclui o agente pessoal `ohmo`
- **Arquétipo observado:** port didático fiel + plataforma multi-agente ambiciosa (Swarm) + agente de mensageria (ohmo)

## Dimensões

### 1. Loop do agente — Nota: 2
`engine/query.py` (`run_query`, ~39 KB): `while` async até `max_turns` ou ausência de tool-uses; **paralelismo quando todas as tools do turno são read-only** (`asyncio.gather`); sequência PreToolUse hook → permissão → execução → PostToolUse por chamada; retry com backoff, cost tracking. Legível e correto; sem durabilidade de loop nem detecção de repetição.

### 2. Entrega de contexto — Nota: 2
`prompts/context.py` agrega base + ambiente + `CLAUDE.md` (`claudemd.py`) + **memórias selecionadas por relevância** (`memory/relevance.py`) + personalização + skills + contexto de repo. Prompt único (não varia por modelo); sem hierarquia com imports; sem cache-awareness formal.

### 3. Compactação — Nota: 3
`services/compact/__init__.py` (1.725 linhas, "faithfully translated from Claude Code's compaction system"): **microcompact** (limpa outputs de `COMPACTABLE_TOOLS`), **full compact** (resumo LLM), **auto-compact** (limiar) e — cobertura que os pares tratam implicitamente — compactação **reativa** a erro "prompt too long". Hooks PRE/POST_COMPACT. Preserva task state entre sessões.

### 4. Design de ferramentas — Nota: 3
**43+ tools** (`tools/`, um arquivo cada) sobre `BaseTool` + `input_model` Pydantic (`to_api_schema()` deriva o JSON Schema); `is_read_only()` alimenta o paralelismo do loop. Categorias além do núcleo: multimodal (imagem), cron, times de agentes, tasks background, `tool_search`. Não varia por modelo.

### 5. MCP — Nota: 2
`mcp/client.py` (`McpClientManager`) sobre o SDK oficial: stdio + Streamable HTTP (sem SSE), status de conexão, auto-reconnect, degradação graciosa. Resources expostos como tools (`list/read_mcp_resource`), `mcp_auth`. Completo no essencial, menor em superfície que os pares.

### 6. Permissões e sandboxing — Nota: 2
`permissions/checker.py`: path rules glob, comandos negados, 3 modos (DEFAULT/PLAN/FULL_AUTO). Destaque: **`SENSITIVE_PATH_PATTERNS` hardcoded e indesligável** (`.ssh`, `.aws/credentials`, `.gnupg`, `.kube/config`, credenciais do próprio harness) — defesa explícita contra prompt injection. Sandbox via `sandbox-runtime`/Docker (`sandbox/adapter.py`) com allowlist de domínios; `trust_env=False` nas tools web (anti-SSRF). Sem parsing estrutural de shell nem trusted folders.

### 7. Memória e estado — Nota: 3
`memory/` (13 módulos): memória em markdown com **schema versionado, escrita atômica com file-lock, assinaturas**; `relevance.py` seleciona o que entra, `usage.py` rastreia uso. Sessões com metadados ricos (`services/session_storage.py`: permission_mode, read_file_state, skills invocadas, checkpoints de compactação); `-c/--continue`, `-r/--resume`, `/resume`.

### 8. Planejamento — Nota: 2
A implementação mínima e correta da equivalência plan-mode-é-permissão: `EnterPlanModeTool` seta `settings.permission.mode = PLAN` (bloqueia escritas); `ExitPlanModeTool` restaura. Todos em `TODO.md`; skill `plan` orientadora; decomposição pesada só no autopilot (fila de `RepoTaskCard`).

### 9. Subagentes / orquestração — Nota: 3
**Swarm** (`swarm/`, 11 módulos): times persistentes com `TeamRegistry`, **mailbox** para comunicação contínua inter-agente, ciclo de vida (`team_lifecycle.py`), **isolamento por worktree git**, sincronização de permissões entre membros; 3 backends (subprocesso, remoto, in-process). Tools de primeira classe (`team_create`, `send_message`). A aposta mais ambiciosa da coorte em multi-agente.

### 10. Verificação / evals — Nota: 2
121 arquivos de teste em ~31 subpastas espelhando cada subsistema; E2E com **chamadas reais de modelo** (`scripts/test_harness_features.py`) e testes contra skills/plugins reais do ecossistema Claude Code (compatibilidade testada, não prometida). Sem evals com juiz LLM nem baselines de regressão.

### 11. Extensibilidade — Nota: 3
Estratégia de **interoperabilidade**: skills no layout `SKILL.md` (carrega de `~/.claude/skills`, `~/.agents/skills`), plugins no formato `.claude-plugin/plugin.json` (12 plugins do Claude Code testados), hooks com **10 eventos + hot-reload** (`hooks/`). Provedores como workflows nomeados: Anthropic/OpenAI-compatible, Copilot OAuth, Kimi, GLM, Ollama...

### 12. Interfaces — Nota: 2
CLI Typer (`oh`) com headless (`-p`, `text|json|stream-json`) e `--dry-run`; duas TUIs (React/Ink + Textual); dashboard web do autopilot; e o distintivo **ohmo**: agente pessoal em **Telegram, Slack, Discord e Feishu** (`channels/`, `ohmo/gateway/`). Sem IDE, sem protocolos de agente.

## Síntese

| # | Dimensão | Nota |
|---|---|---|
| 1 | Loop do agente | 2 |
| 2 | Entrega de contexto | 2 |
| 3 | Compactação | 3 |
| 4 | Ferramentas | 3 |
| 5 | MCP | 2 |
| 6 | Permissões/sandbox | 2 |
| 7 | Memória/estado | 3 |
| 8 | Planejamento | 2 |
| 9 | Subagentes | 3 |
| 10 | Verificação/evals | 2 |
| 11 | Extensibilidade | 3 |
| 12 | Interfaces | 2 |
| | **Total** | **29/36** |

- **Perfil/arquétipo:** o melhor código para *estudar* engenharia de harness (port legível e comentado do Claude Code) + a aposta mais ousada em multi-agente (Swarm) — jovem como produto (v0.1.9).
- **Pontos mais fortes:** compactação (a documentação viva do sistema do Claude Code); Swarm (times, mailbox, worktrees); memória com relevância e rigor de formato.
- **Pontos mais fracos:** maturidade/estabilidade (pré-1.0, área ohmo/gateway em fluxo); sem evals comportamentais nem cache-awareness.
- **Recurso distintivo:** ohmo — o harness como colega de mensageria em 4 plataformas, com workspace de identidade próprio.
- **"O que roubar":** `SENSITIVE_PATH_PATTERNS` indesligável (a defesa mais barata e exportável da coorte); paralelismo automático de tools read-only; tracking de uso de memória para poda.
- **Cláusula de expiração:** o próprio projeto, em parte — como port didático, seu valor de "expor o que os produtos escondem" expira se os produtos abrirem; o Swarm, ao contrário, é aposta no futuro (coordenação multi-agente) e não prótese do presente.
