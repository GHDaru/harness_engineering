# Plan — 054

## Backend (store + 4 endpoints + camada de prompt)
1. `store.py` (dois adapters): `record_consent(sid, versao)` · `add_nav(sid, slug)` · `nav_stats(limit)` · `set_goal(sid, texto)` · `get_goal(sid)`; Postgres: tabelas `consents`, `nav_events`, `goals` (FK sessions ON DELETE CASCADE — LGPD grátis).
2. `app.py`: `POST /consent` {session_id, versao} · `POST /telemetry` {session_id, slug} (slug sanitizado, melhor esforço) · `POST /objetivo` {session_id, texto ≤300} · `GET /objetivo` · `GET /telemetry?token=` (resumo por slug + total).
3. `_system_prompt` ganha `goal`: camada "Objetivo declarado do leitor: … Conecte respostas e planos a ele."; `_preparar_chat` busca `get_goal(sid)`; `_debug` ganha `objetivo` (bastidores).
4. Testes: consent/telemetry/objetivo persistem; objetivo entra no prompt (assert no debug) e no GET; resumo exige token.

## Widget/site (companion.js/css)
5. **Consent**: `CONSENT_V = "v1"`; banner fixo (todas as páginas) até aceitar; aceite → localStorage + POST /consent (silencioso) + oferta do tour. No chat sem aceite: cartão com o texto + botão no lugar do form (form/status ocultos).
6. **Telemetria**: no bootstrap, se aceito → sendBeacon(`/telemetry`) com slug do `body[data-slug]` (fallback fetch keepalive).
7. **Tour**: motor mínimo próprio — overlay + spotlight (box-shadow gigante) + cartão posicionado; passos declarativos {alvo?, titulo, texto}; pula alvo ausente; Esc/pular; `cmp_tour` marca visto; comando `/tour` e oferta pós-aceite.
8. **/plano**: paleta + submit route; com arg → POST /objetivo + sendMsg pedindo o plano; sem arg → GET /objetivo e instrução; bastidores (Memória) mostram objetivo (do debug).
9. E2E Playwright cobrindo o fluxo inteiro + regressões (paleta, bastidores).

## Riscos
- Banner × selo/консent duplo → um só ponto de verdade (`cmp_consent`), chat lê o mesmo.
- Telemetria sem consentimento → gate no cliente E no servidor não persiste sem consent? Servidor não sabe do aceite por sessão... sabe: consents por session_id — `POST /telemetry` só grava se houver consent da sessão (verificação barata; à prova de curl casual).
- Tour em página sem alvos (splash) → passos genéricos apenas.
