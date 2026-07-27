# Tasks: Chat-companion backend

**Feature**: `016-chat-companion-backend` · **Plan**: [plan.md](./plan.md)

## Fase 1 — Portas e domínio

- [x] **T101** `backend/config.py`: settings via env (LLM_ADAPTER, OPENAI_*, LLM_MODEL, DATABASE_URL, ALLOWED_ORIGINS, RATE_LIMIT_*, ALLOW_BYOK) com defaults seguros. (FR-011)
- [x] **T102** `backend/llm.py`: `LLMPort` + `EchoAdapter` + `OpenAICompatAdapter` (reuso do harness-zero) com suporte a **BYOK** por chamada. (FR-006)
- [x] **T103** `backend/store.py`: `StorePort` + `MemoryStore` + `PostgresStore` (Neon; cria tabelas na subida). (FR-003, FR-004)
- [x] **T104** `backend/capabilities.py`: registro capítulo→capacidade + `gating(chapter, mode)`; rótulos/descrições para o widget. (FR-002, FR-005)
- [x] **T105** `backend/ragindex.py`: índice leve do texto do livro (busca em `livro/**.md`). (FR-008, Princípio I)
- [x] **T106** `backend/tools.py`: `ToolPort` com tools **seguras** (hora, buscar_no_livro, calcular), cada uma amarrada a uma capacidade; schemas dialeto OpenAI. (FR-008, FR-005)
- [x] **T107** `backend/loop.py`: `run_turn` (loop de tool-calling) recebendo só as tools das capacidades ativas. (FR-005, FR-006)

## Fase 2 — API

- [x] **T201** `backend/app.py`: FastAPI + CORS + rate limit + endpoints `GET /health`, `GET /capabilities`, `POST /session`, `POST /chat`, `GET /history`, `DELETE /session/{id}`; composition root (escolhe adapters por env). (FR-001,002,004,007,009,010)
- [x] **T202** Persistir user/assistant no store a cada `/chat`; injetar system prompt de tutor + contexto do capítulo. (FR-001, FR-003)

## Fase 3 — Deploy e docs

- [x] **T301** `requirements.txt`, `Procfile`, `railway.json`, `runtime.txt`, `.env.example`. (FR-012)
- [x] **T302** `chat-companion/README.md`: arquitetura + **passo-a-passo Neon + Railway** + variáveis de ambiente + como testar. (FR-012)
- [x] **T303** `.gitignore`: garantir `chat-companion/**/.env` e artefatos fora do versionamento. (FR-011)

## Fase 4 — Verificação

- [x] **T401** `backend/tests/test_smoke.py`: com `echo`+memória — `/chat` responde, gating progressivo esconde tool futura, `/history` retorna, `/capabilities` correto, rate limit 429. (SC-001..006)
- [x] **T402** Rodar os testes (sem rede, sem DB) verdes; subir o app local e conferir `/health` e `/capabilities`. (SC-006)
- [x] **T403** Revisão: zero segredo no repo; zero identificador interno de modelo; `.env` ignorado. (FR-011, FR-013, SC-007)

## Fase 5 — Registro e merge

- [x] **T501** `livro/HISTORICO.md`: edição 0.12 (backend do chat-companion) + modelo de IA (A3).
- [x] **T502** Commit na branch `016-…`, merge para `main` (`--no-ff`), push. (Princípio VII) — não dispara deploy do Pages (fora dos paths); Railway é deploy manual do autor.
