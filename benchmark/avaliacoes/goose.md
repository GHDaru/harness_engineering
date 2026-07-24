# HARNESS_EVAL — Goose (Block / AAIF)

## Metadados

- **Repositório / versão avaliada:** github.com/block/goose · v1.44.0 (fork GHDaru/goose, commit 0038bc7)
- **Linguagem / stack:** Rust — workspace com 12 crates; `agent.rs` com 4.424 linhas; desktop Electron via ACP
- **Licença:** Apache-2.0 (doado à Linux Foundation / AAIF)
- **Data da avaliação:** 2026-07-24 (rodada 2) · **Categoria:** harnesses de código
- **Posicionamento declarado:** agente de IA extensível e aberto
- **Arquétipo observado:** o harness **MCP-nativo** — o protocolo não é integração, é a espinha dorsal

## Dimensões (resumo com evidência)

### 1. Loop do agente — Nota: 3
Loop totalmente streaming (`reply` retorna `BoxStream<AgentEvent>`, `crates/goose/src/agents/agent.rs`); **dois níveis de retry** (transiente por provedor + retry de tarefa via `RetryManager` com `SuccessCheck` que reseta a conversa); `DEFAULT_MAX_TURNS = 1000` configurável por recipe; `MAX_EMPTY_TURN_RETRIES`; **`RepetitionInspector`** detectando loops repetitivos; cancelamento com `CancellationToken`.

### 2. Entrega de contexto — Nota: 3
`SystemPromptBuilder` com override total + extras nomeados; hints de projeto multi-arquivo (**`.goosehints` E `AGENTS.md`** por default, `CLAUDE.md` suportado via config) respeitando `.gitignore`; **carregamento incremental de hints de subdiretório conforme o agente navega** (`SubdirectoryHintTracker`) — hierarquia dinâmica, não estática; sanitização anti prompt-injection de tags Unicode; contexto "top of mind" por turno.

### 3. Compactação — Nota: 3
Auto-compactação a 80% da janela com **summary estruturado** (`StructuredSummary`: user_intent, files, pending_tasks, current_work); se a sumarização estoura, **remoção progressiva "middle-out"** de tool-responses (0→100%); **sumarização incremental de pares tool-call/response** em batches de 10 protegendo os N últimos; metadados de visibilidade preservam o histórico bruto na UI; respeita `provider.manages_own_context()`.

### 4. Design de ferramentas — Nota: 3 ⭐ (hipótese MCP-nativo confirmada)
**Toda tool é MCP por design**: os built-ins de `goose-mcp` (memory, computercontroller, tutorial...) são servidores `rmcp::ServerHandler` reais servidos **in-process sobre `DuplexStream`** (stdio virtual) — e podem rodar standalone (`goose mcp <server>`). Até as tools de primeira classe (developer/shell/edit, todo, skills) são "platform extensions" que falam `McpClientTrait`. Uma única abstração para toda a superfície de ferramentas.

### 5. MCP — Nota: 3
`ExtensionConfig` cobre stdio, StreamableHTTP (com Unix socket), builtin, platform, frontend e **InlinePython**; gestão dinâmica em runtime (tools `manage_extensions`/`search_available_extensions`); **verificação de malware de extensões antes do carregamento**; ecossistema documentado de 70+ extensões.

### 6. Permissões e sandboxing — Nota: 2
Modos `GooseMode` (Auto/Approve/Chat-only); **`permission_judge` usa um LLM para classificar tools como read-only** (auto-aprova leitura); `ToolPermissionStore` persiste allow/deny por assinatura com expiração. Mas o isolamento de execução é leve — o `developer` roda shell direto; contenção fica a cargo de Docker externo.

### 7. Memória e estado — Nota: 3
`SessionManager` com fork, resume, `parent_session_id`, `schedule_id`, custo acumulado e nomeação automática de sessão via LLM; **duas camadas de memória** — extensão MCP `memory` (fatos chave/valor) e `chatrecall` (busca semântica em conversas passadas carregando resumos como contexto); importação de formatos externos de sessão.

### 8. Planejamento — Nota: 2
**Recipes** declarativos (YAML/JSON com instructions, parâmetros tipados, settings, `response.json_schema`, retry) + extensão `todo` + `final_output_tool` para saída estruturada. Sem plan mode de duas fases (plan→approve→execute).

### 9. Subagentes / orquestração — Nota: 3
`summon` delega a subagentes (Agent filho com recipe/config próprios, eventos streamados de volta); **SubRecipes** com composição hierárquica e execução paralela/sequencial; extensão `orchestrator` gerenciando múltiplas sessões (lead/worker: list/start/send/interrupt/stop).

### 10. Verificação / evals — Nota: 3
**Harbor** (`evals/harbor/`): benchmark estilo terminal-bench (89 tasks) comparando harnesses/modelos/builds com pass-rate, custo, tokens e turns — **com leaderboard real no README** (stock ~50.6%, code-mode 57.3%) e LLM-judges de pós-processamento; `goose-self-test.yaml`; crates dedicados de teste; cobertura unitária forte (a compactação tem ~15 testes inline).

### 11. Extensibilidade — Nota: 3
Três eixos: extensões MCP (6 tipos de transporte/origem); recipes/skills; e provedores — nativos + **37 provedores declarativos por JSON** (adicionar um provider OpenAI-compatible é criar um arquivo). `CUSTOM_DISTROS.md` permite distros brandeadas; `goose-sdk` para embutir.

### 12. Interfaces — Nota: 3
CLI completo + TUI; **desktop Electron falando ACP** com o core (o binário embarcado — sem servidor separado); headless via recipes + scheduler embutido; gateway Telegram e bot Discord; modo servidor MCP/ACP puro.

### 13. Aprendizado / auto-melhoria (suplementar) — Nota: 1
Memória de fatos + chatrecall (recall semântico de conversas) — aprendizado passivo; sem autoria autônoma de skills.

## Síntese

| Dimensões 1–12 | **Total: 34/36** (abaixo do teto: sandboxing e plan mode) |
|---|---|

- **Perfil/arquétipo:** a aposta de que padrão aberto vence integração proprietária — tudo é MCP, até o que é interno; governança de fundação (Linux Foundation) coerente com a tese.
- **Pontos mais fortes:** arquitetura MCP-uniforme; compactação em três técnicas complementares; Harbor com leaderboard público.
- **Pontos mais fracos:** contenção de execução (shell direto no host); sem plan mode de duas fases.
- **Recurso distintivo:** servidores MCP internos servidos in-process sobre `DuplexStream` — o custo de rede do protocolo eliminado sem abrir mão da uniformidade.
- **"O que roubar":** provedores declarativos por JSON; permission judge por LLM para classificar read-only; hints incrementais por subdiretório; verificação de malware de extensões.
- **Cláusula de expiração:** o permission judge por LLM é uma prótese dupla (usa um modelo para compensar a falta de metadados de outra época — expira quando tools declararem efeitos formalmente); recipes não expiram (são workflow, não muleta).
