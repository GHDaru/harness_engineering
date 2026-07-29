# Spec 049: Rate-limit persistente (derivado do store)

**Feature Branch**: `049-rate-limit-persistente` · **Criada em**: 2026-07-29

## Problema

O rate-limit do backend vive num deque em memória: **zera a cada deploy/restart** do Railway e não funcionaria com mais de uma instância.

## Decisão

A fonte da verdade do limite **por sessão** passa a ser o próprio store (`count_since(session_id, janela)` — já existia na porta desde a spec 016, em ambos adapters): mensagens `user` são persistidas no Postgres, logo a contagem **sobrevive a deploys e vale entre instâncias**, sem tabela nova nem migração. O deque em memória vira **guarda secundária por IP** (fator `RATE_LIMIT_IP_FACTOR`× o limite, default 3×) contra abuso multi-sessão de um mesmo IP — best-effort, documentado como tal.

## Requisitos

- FR-001: `/chat` e `/chat/stream` aplicam o limite por sessão via `count_since` (janela/limite das configs atuais); BYOK continua isento.
- FR-002: guarda por IP em memória com teto `RATE_LIMIT_MSGS × RATE_LIMIT_IP_FACTOR` (env, default 3).
- FR-003: sugestões mantêm o limitador atual (custo baixo; sem mudança).
- FR-004: teste novo simulando restart (limpar o deque) — o 429 por sessão continua vindo do store; suíte completa verde.

## Limitação conhecida

`delete_session` (direito ao esquecimento, LGPD) zera o histórico e, com ele, a contagem — a guarda por IP cobre o abuso desse atalho. Registrado como trade-off consciente: privacidade > contabilidade perfeita.
