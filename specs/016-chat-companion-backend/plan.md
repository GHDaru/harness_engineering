# Implementation Plan: Chat-companion backend

**Branch**: `016-chat-companion-backend` · **Date**: 2026-07-27 · **Spec**: [spec.md](./spec.md)

## Summary

Backend FastAPI que é o **harness-zero em produção**: reusa `LLMPort` e o loop de tool-calling do harness-zero, e antecipa duas portas que as etapas didáticas formalizarão depois — `StorePort` (persistência, etapa 04/cap. 08) e `ToolPort` (tools+gating, etapa 02/cap. 05). Atende o widget do site: tutor do livro + tools seguras, com **gating de capacidades por capítulo** (avançado vs progressivo), **identidade anônima por navegador**, **persistência em Neon Postgres** (fallback memória), **chave do projeto (NVIDIA NIM) + rate limit + BYOK**, **CORS** restrito. Entrega também os **arquivos e instruções de deploy** (Railway + Neon).

## Technical Context

- **Linguagem/stack**: Python 3.11+, FastAPI, Uvicorn, httpx, pydantic — mesma base do harness-zero. Persistência: `psycopg[binary]` v3 (Postgres/Neon).
- **Local**: `chat-companion/backend/` (deployable próprio, distinto das etapas didáticas autocontidas).
- **Portas (hexagonal)**:
  - `LLMPort` — `EchoAdapter` (sem rede) e `OpenAICompatAdapter` (NVIDIA NIM); BYOK por requisição.
  - `StorePort` — `MemoryStore` (dev/fallback) e `PostgresStore` (Neon; `CREATE TABLE IF NOT EXISTS` na subida).
  - `ToolPort` — registro de tools seguras (hora, busca no livro, cálculo), cada uma amarrada a uma capacidade.
- **Gating**: `capabilities.py` — registro capítulo→capacidade; `avancado` libera tudo, `progressivo` libera `libera_no_capitulo <= chapter`. Só tools de capacidades ativas entram no loop.
- **Rate limit**: janela por `session_id`+IP em memória (MVP single-instance), configurável; BYOK isenta.
- **Endpoints**: `GET /health`, `POST /chat`, `GET /capabilities`, `GET /history`, `DELETE /session/{id}`, `POST /session` (garante linha).

### Resposta à dúvida do autor — "endpoints diferentes?"

Sim. O widget conversa com o backend por vários endpoints com papéis distintos:

| Endpoint | Papel |
|---|---|
| `GET /health` | healthcheck do Railway |
| `GET /capabilities?chapter&mode` | mapa de capacidades (o que o widget mostra "posso fazer agora") |
| `POST /session` | garante a sessão anônima do navegador |
| `POST /chat` | o turno de conversa (tutor + loop de tools com gating) |
| `GET /history?session_id` | histórico para retomar |
| `DELETE /session/{id}` | apagar a sessão (LGPD) |

## Constitution Check

| Princípio | Conformidade |
|---|---|
| I. Evidência acima de retórica | ✓ Tutor responde do texto do livro (tool de busca no Markdown); sem alegações sobre harness sem fonte. |
| II. A fonte-base é o código | ✓ O companion **é** o harness-zero rodando; reusa `LLMPort`/loop reais. |
| III. Método pedagógico | ✓ Gating progressivo materializa *fading*/carga cognitiva: só o já ensinado fica ativo. |
| IV. Livro vivo | ✓ Edição registrada com modelo de IA (A3). |
| V. Segurança e credenciais | ✓ **Central**: chave só em env; `.env` gitignored; BYOK por requisição, nunca persistida; tools sandbox; CORS restrito. |
| VI. Neutralidade e acessibilidade | ✓ Custo zero (NVIDIA NIM gratuito, creditado); sem lock-in (OpenAI-compatible). |
| VII. Spec-driven e branch-per-melhoria | ✓ Feature na branch `016-…`, merge ao fim. |
| Restrições harness-zero (DDD leve, hexagonal por refatoração, anti-apodrecimento) | ✓ Portas nascem da necessidade real do companion; adapters plugáveis; **nota**: o companion (produção) roda à frente das etapas didáticas — a trilha ensina depois o que a produção já usa; documentado nas Assumptions. |
| Política de identidade de modelo | ✓ Sem identificador interno em código/README. |

**Resultado**: PASS. Tensão registrada (produção à frente do ensino) é intencional e documentada, não uma violação.

## Project Structure

```
chat-companion/
  README.md                 # arquitetura + deploy passo-a-passo (Neon + Railway)
  backend/
    app.py                  # FastAPI: endpoints + wiring (composition root)
    config.py               # settings via env (com defaults seguros)
    llm.py                  # LLMPort + EchoAdapter + OpenAICompatAdapter (BYOK)
    store.py                # StorePort + MemoryStore + PostgresStore (Neon)
    capabilities.py         # registro capítulo->capacidade + lógica de gating
    tools.py                # ToolPort: tools seguras + schemas + amarração à capacidade
    loop.py                 # run_turn (loop de tool-calling, do harness-zero)
    ragindex.py             # índice leve do texto do livro (busca no Markdown)
    requirements.txt
    Procfile                # web: uvicorn app:app --host 0.0.0.0 --port $PORT
    railway.json            # config de deploy (builder + healthcheck)
    runtime.txt             # versão do Python
    .env.example            # variáveis (sem segredos)
    tests/
      test_smoke.py         # echo + memória: chat, gating, history, capabilities (sem rede/DB)
```

## Design decisions

1. **Reuso real do harness-zero**: `LLMPort`/loop vêm do etapa 01 (com evolução mínima). O companion prova a tese "o processo do livro é um harness bem-instrumentado".
2. **Portas antecipadas, honestas**: `StorePort`/`ToolPort` existem aqui porque o *deploy* exige — e as etapas 02/04 depois ensinam a mesma dor. Registrado como tensão intencional, não improviso.
3. **Fallbacks que nunca quebram**: sem DB → memória; sem chave → echo. O serviço sobe em qualquer ambiente; a produção liga os adapters reais por env.
4. **Segurança por construção**: só tools sandbox; BYOK nunca persistida nem logada; CORS/rate-limit configuráveis; segredos só em env.
5. **Gating = pedagogia executável**: o modo progressivo espelha o *fading* do 4C/ID — o companion só oferece o que o leitor já viu.

## Complexity Tracking

*Sem violação constitucional. A única tensão (produção à frente das etapas didáticas) é intencional e documentada; não requer entrada de exceção.*
