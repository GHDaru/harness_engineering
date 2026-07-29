# Spec 047: Streaming SSE do companion

**Feature Branch**: `047-companion-sse` · **Criada em**: 2026-07-29

## Requisitos

- FR-001 (backend): novo endpoint `POST /chat/stream` — mesmas validações, gating, rate-limit e BYOK do `/chat` —, resposta `text/event-stream` com eventos JSON: `{delta}` (trecho de texto), `{trace}` (tool call executada), `{done, ...}` (fim, com capacidades) e `{erro}` (falha sem stack).
- FR-002 (portas): `LLMPort` ganha `stream()` — no `OpenAICompatAdapter` via SSE do endpoint OpenAI-compatible (`stream: true`, agregando deltas de `tool_calls` por índice); no `EchoAdapter` em pedaços (testável sem rede). O loop ganha `run_turn_stream()` (gerador), preservando `MAX_TURNS` e o trace.
- FR-003 (widget): o companion consome o stream via `fetch` + `ReadableStream`, renderizando o texto incrementalmente (textContent durante o stream; markdown ao final). Falha do stream → **fallback automático** para o `/chat` clássico (compatibilidade com backend antigo no ar).
- FR-004: persistência inalterada (mensagem do assistente gravada ao final do stream); `/chat` clássico permanece.
- FR-005: testes do backend passam; teste novo do stream com EchoAdapter; teste manual do widget contra backend local.

## Fora de escopo

- WebSockets; streaming das ferramentas (só o texto final é transmitido em delta).
