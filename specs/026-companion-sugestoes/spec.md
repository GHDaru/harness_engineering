# Feature Specification: Companion — envio de sugestões (E05)

**Feature Branch**: `026-companion-sugestoes` · **Created**: 2026-07-28

## Requisitos
- **FR-001**: O backend DEVE expor `POST /suggestion` `{session_id, texto, pagina?}` que **persiste** a sugestão (Postgres/memória) e, se SMTP configurado (env), **envia email** ao autor (`SUGGESTION_EMAIL_TO`, default ghdaru@gmail.com).
- **FR-002**: O widget DEVE ter um botão **💡 Sugerir** que abre um mini-form (textarea) e envia; feedback de sucesso/erro; rate limit aplicado.
- **FR-003**: Sem segredo no repo (SMTP só por env: SMTP_HOST/PORT/USER/PASS); falha de email NUNCA perde a sugestão (persistida antes); sem identificador interno de modelo.
- **FR-004**: `GET /suggestions?token=` (admin, token por env) lista as sugestões (fallback de leitura sem email).

## Sucesso
- SC-001: sugestão enviada → gravada (tabela suggestions) e email disparado quando SMTP presente.
- SC-002: widget mostra confirmação; sem SMTP, ainda grava (e o autor lê via /suggestions?token=).
- SC-003: testes smoke verdes (memória, sem rede).
