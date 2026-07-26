# Plano — Cap. 08 (Memória e Estado)

## Fonte-base (código, já reunida)
- Rodada 1: opencode (SQLite/Drizzle, eventos replayáveis), gemini-cli (checkpoint git + `save_memory`), OpenHarness (memdir versionado + `relevance.py`/`usage.py`).
- Rodada 2: Aider ⭐ (git-native: auto-commit, `/undo`, `.aider.chat.history.md`); Hermes ⭐ (`MEMORY.md`+`USER.md` com nudges a cada 10 turnos, providers Honcho/mem0/supermemory, `session_search` FTS5); Codex (rollout jsonl por turno); OpenHands (event-stream JSON por conversa); OpenClaw (session lane + arquivos de workspace); ohmo (`SessionBackend`/`MemoryCommandBackend`); IronClaw (checkpoints + máquina de estados com leases).

## Pesquisa (concluída, verificada)
- Científico: MemGPT (2310.08560), Survey memória (2404.13501), CoALA (2309.02427), Generative Agents (2304.03442), MemoryBank (2305.10250), A-MEM (2502.12110), Mem0 (2504.19413), Reflexion (2303.11366).
- Indústria: docs de sessão/checkpoint/memory-tool/CLAUDE.md-hierarquia; context management (Anthropic); Letta (memory blocks; tiers core/recall/archival; "RAG is not agent memory"); mem0 (tipos de memória); Zep/Graphiti (grafo bi-temporal); LangMem/LangGraph (short-term thread × long-term store); AWS Bedrock AgentCore.

## Tradução em decisões (o que vai ao corpo)
1. **Contexto como recurso escasso com tiers** (MemGPT/Letta) — a moldura de 3 camadas ganha o vocabulário OS: RAM (contexto) ↔ recall ↔ archival; o agente paginando via tool.
2. **A fórmula de recall** (Generative Agents: recência×importância×relevância) — o `relevance.py`+`usage.py` do OpenHarness é a instância real.
3. **Esquecimento controlado** (MemoryBank forgetting curve) — memória não-usada é candidata a poda (usage tracking).
4. **Memória ≠ RAG** (Letta/AWS) — memória = retrieval + write path + state; explica por que markdown-versionável (write via edição de arquivo) venceu embeddings no código.
5. **Reversão do workspace** (Aider pioneiro → gemini-cli `/rewind` → Claude Code checkpointing) — reversibilidade muda o cálculo de risco.
6. **"Assuma interrupção"** (memory tool) — a etapa prática grava um log de progresso durável; conecta ao harness de longa duração.

## Passos
1. Escrever `08-memoria-estado.md` v3. 2. Atualizar `bibliografia.md`. 3. `node publicar/build.mjs` (link-check verde). 4. Commit na branch 003.
