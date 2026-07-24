# 08 — Memória e Estado

## O problema

O modelo esquece tudo entre chamadas; o harness lembra por ele. "Memória e estado" cobre três camadas com requisitos diferentes:

1. **Estado de sessão** — a conversa em si: mensagens, tool-calls, metadados. Precisa sobreviver a reinícios e permitir retomar (`resume`), ramificar e reverter.
2. **Memória de longo prazo** — fatos que atravessam sessões: preferências do usuário, decisões do projeto, aprendizados. Precisa ser selecionável (nem tudo entra em todo contexto).
3. **Estado do workspace** — o que o agente *fez* nos arquivos. Precisa ser reversível: desfazer as mudanças de um agente é tão importante quanto fazê-las.

## Padrões de implementação

- **Sessão em armazenamento estruturado** (SQLite/JSON) com retomada e hierarquia pai/filho para subagentes.
- **Memória em markdown versionável** — legível por humanos, editável, diffável; o padrão dominante sobre bancos vetoriais nos harnesses de código.
- **Seleção por relevância** — injetar no contexto só as memórias pertinentes à tarefa.
- **Checkpointing de workspace via git** — snapshot antes de cada edição; desfazer vira operação de VCS.

## Como os harnesses estudados implementam

### opencode — estado como banco de dados
Persistência em **SQLite via Drizzle** (`packages/core/database`, `core/session/sql.ts`): sessões, mensagens e partes são linhas tipadas. Sessões têm `parentID` (hierarquia para subagentes), suportam revert (`session/revert.ts`) e **compartilhamento** (`share/`, `sync/`). A V2 (`CONTEXT.md`) leva o desenho a "infra de dados": inbox durável de prompts, eventos replayáveis com cursores (`sessions.events({sessionID, after})`), snapshots de contexto persistidos entre reinícios de processo. É o modelo de estado mais robusto dos três — o harness como sistema distribuído com estado durável.

### gemini-cli — o workspace reversível
Memória de longo prazo nos próprios `GEMINI.md` (tool `save_memory`, global em `~/.gemini` + índice de projeto, com auto-memory testada em evals). O recurso distintivo é o **checkpointing baseado em git** (`services/gitService.ts` + `chatRecordingService.ts`): snapshots do workspace antes de edições, habilitando `/restore` e `/rewind` — desfazer as mudanças do agente no disco, não só na conversa — além de `/resume` de sessões. Um agente cujas ações são reversíveis muda o cálculo de risco de tudo o mais (permissões podem ser mais frouxas quando desfazer é barato).

### OpenHarness — memória como arquivo, com disciplina
`src/openharness/memory/` (13 módulos): memória persistente em markdown (`MEMORY.md`/memdir por projeto) com **schema versionado, escrita atômica com file-lock e assinaturas** — tratando arquivos de memória com o rigor de um formato de dados. `relevance.py` seleciona o que entra no contexto; `usage.py` marca uso (fecha o ciclo: memória não usada é candidata a poda). Sessões persistidas com metadados ricos (`services/session_storage.py`): modo de permissão, estado de arquivos lidos, skills invocadas, checkpoints de compactação. Retomada via `-c/--continue`, `-r/--resume`, `/resume`.

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Sessão | SQLite + eventos replayáveis | gravação + resume | JSON + metadados ricos |
| Memória longa | — (regras via AGENTS.md) | GEMINI.md + save_memory | memdir com schema e locks |
| Seleção | — | índice hierárquico | por relevância + tracking de uso |
| Reversão | revert de sessão | **git checkpoint: /rewind do disco** | checkpoints de compactação |
| Compartilhamento | sessões compartilháveis | — | — |

As três camadas do problema receberam três campeões diferentes: opencode venceu em *estado de sessão* (durabilidade de banco), gemini-cli em *estado de workspace* (reversão via git), OpenHarness em *memória de longo prazo* (relevância + rigor de formato). Nenhum dos três usa banco vetorial para memória — no domínio de código, markdown versionável venceu embeddings, pelo menos por enquanto. O harness ideal desta dimensão combinaria os três; é exatamente o tipo de síntese que o benchmark existe para apontar.
