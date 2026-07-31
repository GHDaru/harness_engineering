# HARNESS_EVAL — Pi (Earendil Labs)

> Rodada **ext-1** (2026-07-31) — primeira promoção Radar→corpus (spec 064). Leitura sistemática de código no fork congelado.

## Metadados

- **Repositório / versão ou commit avaliado:** [github.com/badlogic/pi-mono](https://github.com/badlogic/pi-mono) · fork `GHDaru/pi`, commit `7846534` (2026-07-31)
- **Linguagem / stack:** TypeScript 5.9 (Node ≥22.19), monorepo npm workspaces (`agent`, `ai`, `coding-agent`, `tui`, `evals`, `protocol`, `server`, `client`, `storage`); Vitest (370 arquivos de teste), Biome, Bun para binários
- **Licença:** MIT (Mario Zechner, 2025)
- **Data da avaliação:** 2026-07-31
- **Posicionamento declarado:** *"Pi is a minimal terminal coding harness. Adapt pi to your workflows, not the other way around."* (`packages/coding-agent/README.md`)
- **Arquétipo observado:** **produto minimalista-militante** — um harness completo de produção que trata metade das dimensões deste benchmark como *anti-features* e as empurra para uma superfície de extensão de primeira classe.

## Dimensões

### 1. Loop do agente — Nota: 3
`packages/agent/src/agent-loop.ts` (793 linhas): duplo loop com streaming por deltas, **steering mid-loop** (`getSteeringMessages()` injeta mensagens do usuário entre turnos), execução paralela de tools com opt-out sequencial, retry em dois níveis (`packages/ai/src/utils/retry.ts`: backoff exponencial; `agent-session.ts` re-tenta o turno após overflow de contexto). Joia rara: `failToolCallsFromTruncatedMessage()` — se `stopReason === "length"`, **recusa a leva inteira de tool calls**, porque JSON truncado pode validar contra o schema e estar silenciosamente incompleto. Sem limite de turnos (grep `maxTurns` → zero): a parada é do caller — coerente com a filosofia, mas um loop patológico só para no Ctrl+C.

### 2. Entrega de contexto — Nota: 3
`packages/coding-agent/src/core/system-prompt.ts`: o prompt base **medido em ~460 tokens** (a alegação "<1k" confirmada — para a porção autoral). O prompt é *derivado do tool set*: cada tool contribui seu `promptSnippet`; guidelines entram condicionadas ao conjunto ativo; o bloco de skills só aparece se `read` estiver ativa (não anuncia capacidade inalcançável). Descoberta hierárquica de `AGENTS.md`/`CLAUDE.md` da raiz ao cwd (`resource-loader.ts`), com dedup de worktrees aninhadas. **Ressalva central**: os context files são concatenados inline sem orçamento — no próprio repo do Pi o `AGENTS.md` tem ~2.700 tokens; o prompt real é ~6× o slogan. A minimalidade é do harness, não do contexto.

### 3. Compactação — Nota: 3 ⭐
`core/compaction/` + `docs/compaction.md` (402 linhas): limiar por `contextWindow - reserveTokens`, corte que caminha de trás acumulando `keepRecentTokens` e **nunca separa toolResult da sua chamada**; sumário estruturado fixo (Goal/Constraints/Progress/Decisions/Next/Critical + `<read-files>`/`<modified-files>` **cumulativos entre compactações encadeadas**); split turns com merge de dois sumários; prompt de sumarização explicitamente anti-continuação; recuperação reativa de overflow com re-tentativa; sumarização de ramos abandonados no `/tree`. Substituível por extensão (`session_before_compact`). Das 18 avaliações do estudo, é a implementação mais completa da dimensão.

### 4. Design de ferramentas — Nota: 3
7 built-in (`read`, `bash`, `edit`, `write`, `grep`, `find`, `ls`), **default de 4** (`sdk.ts:245`) — a alegação confirmada. Schemas TypeBox; multi-edit numa chamada com casamento contra o arquivo original; `bash` trunca preservando as últimas linhas e derrama o output completo em arquivo temporário informando o path; conjunto read-only explícito (`createReadOnlyToolDefinitions`). O padrão `promptSnippet`/`promptGuidelines` acopla descrição de prompt à definição da tool — prompt e tool set nunca dessincronizam.

### 5. MCP — Nota: 0 (por decisão)
Zero código, zero dependência (`grep -rni mcp packages/*/src` → nada). Política declarada: *"**No MCP.** Build CLI tools with READMEs (see Skills), or build an extension that adds MCP support."* — o substituto é CLI + README exposto como skill, executado via `bash`.

### 6. Permissões e sandboxing — Nota: 1
Sem sistema de aprovação, allowlist ou parsing de comandos. O que existe: **Project Trust** (`project-trust.ts`) — guarda de *carregamento de inputs* (settings/extensions/skills do repo só carregam com aprovação; `trust.json` por diretório), explicitamente **não** um boundary de segurança; e o hook `beforeToolCall` com `{block, reason}`, sobre o qual o exemplo `permission-gate.ts` (34 linhas) constrói um gate. `docs/security.md` é o manifesto: *"A partial in-process sandbox would be easy to misunderstand as a security boundary… Real isolation needs to come from the operating system"* — isolamento real terceirizado a container/micro-VM (`docs/containerization.md`). Nota 1: o gancho existe e o trust é real, mas a política não vem no produto — e `AGENTS.md` carrega **mesmo sem trust** (superfície de injection aceita por design).

### 7. Memória e estado — Nota: 2
Sessões JSONL **em árvore** (`id`/`parentId`; branching in place) com migração automática de formato v1→v3, `/resume` com busca, `/fork`, `/tree` com sumarização de ramo, `/export`/`/share`; backend SQLite opcional. **Sem memória de longo prazo** (nenhum arquivo auto-gerenciado, só `AGENTS.md` manual) e sem checkpointing de workspace — as duas metades ausentes da dimensão.

### 8. Planejamento — Nota: 1
*"**No plan mode.** Write plans to files… **No built-in to-dos. They confuse models.**"* (README). No core, nada. Como exemplo de primeira classe: `examples/extensions/plan-mode/` (desativa `edit`/`write`, filtra `bash` por allowlist read-only, persiste estado na sessão, `/plan` `/todos`) — **testado** em `test/plan-mode-extension.test.ts`. Nota 1 pela existência mantida e testada fora do core.

### 9. Subagentes / orquestração — Nota: 1
*"**No sub-agents.** Spawn pi instances via tmux, or build your own."* No core, nada. Exemplo completo: `examples/extensions/subagent/` — cada subagente é um **processo `pi` separado** (isolamento real), com 4 definições (`scout/planner/reviewer/worker`), 3 workflows encadeados, streaming, paralelismo e custo por agente. O design doc `harness-v2.md` prevê a primitiva (lanes).

### 10. Verificação / evals — Nota: 3
Duas camadas no mesmo repo: (a) 370 arquivos de teste com **faux provider** (`ai/src/providers/faux.ts`) — regra do `AGENTS.md`: nenhum teste usa API real — e regressões nomeadas por issue; (b) `packages/evals`: roda `AgentSession` reais contra modelos reais, anexa **sessões nativas** como artefato (abríveis no TUI via `/import`) e `evalHarnessTable()` compara N configurações de harness (prompt/tools/skills/modelo) no Vitest. Sem LSP/lint pós-edição (via `bash`, como um humano).

### 11. Extensibilidade — Nota: 3 ⭐
A dimensão-tese. `ExtensionAPI` com **28 eventos** (até o nível de request do provider) e ~25 registradores (tools — inclusive **substituindo built-ins** —, comandos, atalhos, flags, renderers, provedores); ~80 exemplos; doc de 2.984 linhas. **Skills lazy** com compatibilidade agentskills.io (com divergência documentada e justificada), carregadas pelo próprio modelo via `read`, `/skill:nome` para forçar; gerenciador de pacotes (`pi install npm:…/git:…`); prompt templates; ~30 provedores de modelo com registro preguiçoso e OAuth por assinatura. O detalhe que fecha o argumento: **cada feature recusada existe como exemplo funcional e testado** — o manifesto é falsificável e foi falsificado pelos próprios autores.

### 12. Interfaces — Nota: 3
Quatro modos: TUI sobre framework próprio (renderização diferencial, synchronized output, imagens inline); `-p`/`--mode json` headless (JSONL); **modo RPC** (JSONL sobre stdio com framing estrito, para integração não-Node); SDK embutível (`createAgentSession`, `SessionManager.inMemory()`). Stack experimental de sessões remotas (`protocol`/`server`/`client`, CBOR + framing próprio). Sem ACP/A2A.

## Dimensões suplementares

### 13. Aprendizado / auto-melhoria — Nota: 2
O posicionamento declarado ("self extensible coding agent") com mecanismo **conversacional**: 7 das ~18 linhas do system prompt são um índice dos próprios docs/exemplos; o ciclo pedir→ler docs→escrever extensão→`/reload`→usar é real e **testado** (`evals/src/extensions.eval.ts` com passo `{type:"reload"}`). Sem captura autônoma de skills a partir da experiência.

### 14. Proatividade / agendamento — Nota: 1
Nada no core. Padrão canônico como exemplo: `file-trigger.ts` (45 linhas — sistema externo acorda o agente via arquivo) + `pi.sendUserMessage(…, {deliverAs})`. *"No background bash. Use tmux."*

## Síntese

### Tabela de notas

| # | Dimensão | Nota |
|---|---|---|
| 1 | Loop do agente | 3 |
| 2 | Entrega de contexto | 3 |
| 3 | Compactação | 3⭐ |
| 4 | Ferramentas | 3 |
| 5 | MCP | 0 |
| 6 | Permissões/sandbox | 1 |
| 7 | Memória/estado | 2 |
| 8 | Planejamento | 1 |
| 9 | Subagentes | 1 |
| 10 | Verificação/evals | 3 |
| 11 | Extensibilidade | 3⭐ |
| 12 | Interfaces | 3 |
| | **Total (0–36)** | **26** |

### Leitura

- **Perfil/arquétipo:** o **contraponto metodológico do corpus** — nota máxima em 7 dimensões e quase-zero nas outras 5, por decisão documentada e não por imaturidade. O perfil serrilhado é a tese: *"aggressively extensible so it doesn't have to dictate your workflow"*.
- **3 pontos mais fortes:** compactação de produção (corte seguro, split turns, arquivos cumulativos — `core/compaction/`); superfície de extensão que **prova as próprias exclusões** (plan mode, subagentes, permission gate e sandbox existem como exemplos testados); testabilidade em duas camadas (faux provider determinístico + evals model-backed com sessões nativas como artefato).
- **2 pontos mais fracos:** o minimalismo é do prompt, não do sistema (55k LOC no coding-agent; context files concatenados sem orçamento — o slogan esconde onde a complexidade foi parar); ausência total de boundaries mesmo baratos (sem allowlist, sem limite de turnos, `AGENTS.md` carregado sem trust — a segurança é 100% terceirizada ao SO).
- **Recurso distintivo:** **o harness usa a si mesmo como skill** — o system prompt indexa os próprios docs com paths resolvidos em runtime, e `/reload` fecha o ciclo "peça a feature → ele lê a doc → escreve a extensão → recarrega → usa".
- **"O que roubar":** (1) `failToolCallsFromTruncatedMessage()` — falhar a leva inteira em `stopReason: length` (~25 linhas que eliminam corrupção silenciosa de edits); (2) `promptSnippet` nas tool definitions com gating pelo conjunto ativo — o prompt encolhe quando tools saem e nunca dessincroniza; (3) `evalHarnessTable()` + artefatos de eval no formato nativo de sessão (evals falhos abrem no TUI).
- **Cláusula de expiração:** a aposta inteira é que **modelos melhores precisam de menos harness** — se modelos passarem a seguir skills lazy com confiabilidade, o gap para harnesses ricos fecha "de graça"; se a janela de contexto continuar cara, a falta de orçamento nos context files cobra juros. O supply-chain hardening (deps pinadas, allowlist de lifecycle scripts, `--ignore-scripts` em tudo) mostra onde os autores acham que o boundary é real — essa assimetria (rigor na cadeia de suprimento, recusa do teatro in-process) é a aposta a observar.
