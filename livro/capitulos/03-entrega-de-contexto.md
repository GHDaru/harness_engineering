# 03 — Entrega de Contexto

## O problema

O modelo só sabe o que o harness mostra. "Entrega de contexto" é a engenharia de decidir **o que** entra em cada chamada — system prompt, regras do projeto, estado do ambiente, memórias, instruções de servidores externos — **em que ordem**, e **como isso muda** no meio de uma conversa sem quebrar o cache do provedor nem confundir o modelo.

Sub-problemas clássicos:
- Onde vivem as regras do projeto e como são descobertas (arquivo na raiz? hierarquia de diretórios? global do usuário?).
- O prompt de sistema deve ser o mesmo para todos os modelos, ou adaptado por família?
- Como informar mudanças de estado (data, modo, skills disponíveis) mid-conversation sem invalidar o prefixo cacheado?

## Padrões de implementação

- **Arquivo de instruções de projeto** — o padrão consagrado: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` na raiz (e ancestrais) do repositório, lido antes de qualquer tarefa.
- **Descoberta hierárquica** — global do usuário → diretórios pais → projeto → subpastas, com precedência definida.
- **Prompt por família de modelo** — cada família responde melhor a instruções diferentes; harnesses maduros mantêm variantes.
- **Montagem em camadas** — base + ambiente (cwd, git, plataforma, data) + regras + memórias + skills + instruções MCP.
- **Cache-awareness** — tratar o prefixo do contexto como imutável dentro de uma "época" e injetar mudanças apenas em fronteiras seguras.

## Como os harnesses estudados implementam

### opencode — contexto como álgebra tipada
A montagem vive em `packages/opencode/src/session/system.ts`: environment (modelo, cwd, worktree, git, data) + skills + instruções MCP. O diferencial nº 1: **prompts base por família de modelo** em `session/prompt/*.txt` — ~10 variantes (`anthropic.txt`, `gpt.txt`, `codex.txt`, `gemini.txt`, `kimi.txt`, `beast.txt`...), selecionadas por substring do model id. As regras de projeto (`AGENTS.md` globais e ascendentes) são agregadas por `session/instruction.ts` como "Context Sources" ordenadas. O diferencial nº 2 é conceitual: a V2 (`CONTEXT.md`) trata o contexto como uma **álgebra de fontes tipadas** com snapshots, "Context Epochs" (baseline de cache do provedor) e mensagens de sistema mid-conversation entregues apenas em fronteiras seguras de turno — a formalização mais rigorosa de cache-awareness entre os harnesses estudados.

### gemini-cli — hierarquia com imports
A montagem (`packages/core/src/prompts/promptProvider.ts`) é dinâmica por modo (interactive/plan/yolo), tools habilitadas e modelo — com blocos modernos vs. legados (`snippets.ts` / `snippets.legacy.ts`) conforme a capacidade do modelo. As regras de projeto usam `GEMINI.md` **hierárquico**: `utils/memoryDiscovery.ts` varre global (`~/.gemini`), diretórios pais e subpastas; `memoryImportProcessor.ts` processa `@imports` (um arquivo de contexto pode incluir outros); tudo é achatado por `flattenMemory` (`config/memory.ts`). Aceita override total do system prompt por arquivo (`GEMINI_SYSTEM_MD` → `.gemini/system.md`) e injeção just-in-time (`tools/jit-context.ts`).

### OpenHarness — o port fiel, com memória relevante
`src/openharness/prompts/context.py` agrega: prompt base (`system_prompt.py`) + ambiente (`environment.py`) + `CLAUDE.md` descoberto (`claudemd.py`) + **memórias selecionadas por relevância** (`memory/relevance.py` decide o que entra, `usage.py` marca o que foi usado) + regras de personalização + seção de skills + contexto de repo ativo (issue/PR). CLI aceita `-s/--system-prompt` e `--append-system-prompt`. A seleção de memórias por relevância é o toque próprio: em vez de injetar toda a memória, escolhe o subconjunto pertinente à tarefa.

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Arquivo de regras | `AGENTS.md` (global + ascendentes) | `GEMINI.md` hierárquico + `@imports` | `CLAUDE.md` |
| Prompt por modelo | ~10 variantes por família | moderno vs. legado por capacidade | prompt único |
| Cache-awareness | Context Epochs (formal, V2) | implícito | implícito |
| Seleção de memória | — | índice global + projeto | por relevância |
| Override pelo usuário | config/flags | arquivo `system.md` completo | flags CLI |

Três abordagens para o mesmo arquivo-de-regras — `AGENTS.md`, `GEMINI.md`, `CLAUDE.md` — que são, na prática, o mesmo artefato com nomes de marca diferentes. A pressão por um padrão neutro (o nome `AGENTS.md` vem ganhando adoção cross-vendor) é um dos movimentos a acompanhar no capítulo 14.
