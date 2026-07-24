# HARNESS_EVAL — Codex CLI (OpenAI)

## Metadados

- **Repositório / versão avaliada:** github.com/openai/codex · snapshot 2026-07 (fork GHDaru/codex, commit 000d254; dev build `0.0.0`)
- **Linguagem / stack:** Rust — monorepo com **97 crates** (`codex-rs/`); o crate `core` sozinho tem ~50k linhas; SDKs Python/TypeScript
- **Licença:** Apache-2.0
- **Data da avaliação:** 2026-07-24 (rodada 2) · **Categoria:** harnesses de código
- **Posicionamento declarado:** motor único por trás de Codex CLI (TUI), extensão IDE e Codex Web/Cloud
- **Arquétipo observado:** o harness de contenção — engenharia de segurança e robustez de nível de sistema operacional

## Dimensões (resumo com evidência)

### 1. Loop do agente — Nota: 3
Arquitetura de tarefas (`SessionTask` trait: Regular/Review/Compact/UserShell) com `run_turn` (`core/src/session/turn.rs`, 2.581 linhas); streaming via SSE **e WebSocket com fallback automático WS→HTTPS**; retry com backoff honrando `Retry-After`; `CancellationToken` hierárquico para interrupção graciosa; cada turno persistido em rollout jsonl (recuperável). Lacuna pontual: sem detector explícito de loop repetitivo (mitigado por budgets).

### 2. Entrega de contexto — Nota: 3
**AGENTS.md** como mecanismo central com descoberta hierárquica e merge (`core/src/agents_md.rs`); system prompt **varia por modelo e é server-driven** (`ModelInfo.base_instructions` vem do backend via `models-manager`, com template de instruções e até **personalidade** configurável Friendly/Pragmatic); contexto ambiental via `WorldState`.

### 3. Compactação — Nota: 3
`core/src/compact.rs` + `compact_remote_v2.rs`: auto-compact a 90% da janela com **três estratégias — local e remota v1/v2 (a compactação executada pelo backend)**; janelas versionadas com prefill tracking; injeção controlada pré/mid-turn; truncamento com `TruncationPolicy`. A compactação remota é única na coorte.

### 4. Design de ferramentas — Nota: 3
Crate `tools/` dedicado com schemas tipados; `unified_exec` (shell persistente com stdin); **`apply_patch` de primeira classe** (crate próprio com parser streaming e gramática formal `apply_patch.lark`, variando por modelo); `tool_search`/`tool_discovery` para expor subconjuntos dinâmicos (economia de contexto); **code-mode com V8 embutido** (tools chamadas via JavaScript).

### 5. MCP — Nota: 3
**Cliente E servidor** (`rmcp-client/`, `mcp-server/` — o Codex se expõe como servidor MCP). Quatro transportes (stdio, streamable HTTP, in-process, process-executor); **OAuth completo** com refresh transactions e store locking; elicitation; prewarm/refresh de servidores; templates de aprovação por tool MCP.

### 6. Permissões e sandboxing — Nota: 3 ⭐ (hipótese confirmada: a referência do mercado)
Contenção multi-plataforma nativa (`sandboxing/`, `linux-sandbox/`, `windows-sandbox-rs/`): **macOS** Seatbelt via `sandbox-exec` com path hardcoded anti-tampering e políticas `.sbpl` de FS+rede; **Linux** bubblewrap embutido + **seccomp** para rede + `NO_NEW_PRIVS`, com Landlock como backend legado; **Windows** com read grants. Acima da contenção: approval modes (incluindo `Granular` por categoria), `SandboxPolicy` (ReadOnly/WorkspaceWrite/DangerFullAccess), **motor de regras Starlark** (`execpolicy/`) por comando, `assess_patch_safety` validando confinamento de escritas, e **network-proxy** para rede mediada. Três camadas independentes: política + aprovação + contenção de SO.

### 7. Memória e estado — Nota: 3
Rollouts jsonl com scanner reverso + índice + espelho **SQLite** (`state_db`) para busca; `resume`/`fork` de sessão; reconstrução de sessão a partir do rollout; e um subsistema separado de **memórias de longo prazo** (`memories/` com escrita, pruning e workspace roots).

### 8. Planejamento — Nota: 2
Tool `update_plan` (checklist estruturado visível na TUI) + `ReviewTask`. Sem plan mode dedicado com aprovação de plano antes da execução.

### 9. Subagentes / orquestração — Nota: 3
Duas gerações de API multi-agente (`multi_agents_v2`: spawn, send_message, followup, interrupt, wait); ~100 perfis built-in de subagentes em TOML; **grafo de agentes persistido** (`agent-graph-store`), identidade de agente, comunicação inter-agente, hooks SubagentStart/Stop; `ThreadManager` coordenando threads paralelas.

### 10. Verificação / evals — Nota: 3
~440 arquivos de teste + **~660 snapshots insta**; suíte de integração E2E que roda turnos reais com backend mockado; testes de política de sandbox por plataforma; parity tests da compactação remota; CI multi-camada (nextest por plataforma, Bazel, postmerge).

### 11. Extensibilidade — Nota: 3
**Hooks completos** (crate `hooks/`: PreToolUse, PostToolUse, PreCompact, SessionStart/End, UserPromptSubmit, Stop, SubagentStart/Stop, com decisões Approve/Block/Deny/Ask); plugins com manifest e marketplace; skills; provedores configuráveis (ollama, lmstudio, aws); profiles; SDKs Python/TS; **App Server JSON-RPC** como espinha dorsal programática.

### 12. Interfaces — Nota: 3
Um único motor Rust serve: TUI (ratatui), `codex exec` headless (saída humana e JSONL), extensão IDE via App Server, **app desktop**, **cloud/web** (`cloud-tasks` com TUI de tarefas remotas), Codex como servidor MCP, e remote control.

### 13. Aprendizado / auto-melhoria (suplementar) — Nota: 1
Subsistema `memories/write` grava memórias automaticamente com pruning — aprendizado de fatos, não de procedimentos (sem autoria autônoma de skills).

## Síntese

| Dimensões 1–12 | **Total: 35/36** (único ponto fora do teto: planejamento) |
|---|---|

- **Perfil/arquétipo:** o harness-fortaleza — assume o pior caso em cada camada (rede, FS, comando, extensão) e ainda entrega superfície de produto completa (CLI/IDE/desktop/cloud) sobre um core único.
- **Pontos mais fortes:** contenção em três camadas independentes (política Starlark + aprovação granular + sandbox de SO nativo por plataforma); compactação remota v2; MCP client+server com 4 transportes.
- **Pontos mais fracos:** planejamento (todo tool, sem plan mode); docs locais são stubs (a documentação real é externa).
- **Recurso distintivo:** system prompt **server-driven por modelo** — a entrega de contexto parcialmente operada pelo backend, não pelo binário.
- **"O que roubar":** execpolicy em Starlark (regras de comando programáveis); fallback de transporte WS→HTTPS no streaming; `tool_discovery` para catálogos dinâmicos.
- **Cláusula de expiração:** aprovações e execpolicy expiram com confiabilidade calibrada dos modelos; o sandbox de SO **não expira** — e a compactação remota inverte a cláusula: em vez de esperar o modelo dispensar o componente, move o componente para o lado do modelo.
