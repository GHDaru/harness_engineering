# Feature Specification: Fix — itálico no markdown do chat-companion

**Feature Branch**: `022-companion-markdown` · **Created**: 2026-07-27

**Input**: O widget renderiza `**negrito**` e `` `código` `` mas não o **itálico** `*x*` — os asteriscos vazavam no texto do tutor.

## Requisitos
- **FR-001**: `fmt()` DEVE converter `*itálico*` em `<em>` (após o negrito, sem tocar em `**`).
- **FR-002**: NÃO DEVE quebrar identificadores `snake_case` (sem itálico por `_`).
- **FR-003**: Escapar antes (segurança) — mantido; sem identificador interno de modelo.

## Sucesso
- SC-001: `*client*` → itálico; `**x**` negrito; `` `tool_call_id` `` intacto (verificado).
- SC-002: build verde; deploy do widget.
