# Tasks: Widget do chat-companion

**Feature**: `017-widget-chat-companion` · **Plan**: [plan.md](./plan.md)

## Fase 1 — Assets do widget

- [x] **T101** `publicar/tema/companion.css`: launcher flutuante + painel (cabeçalho, capacidades, mensagens, input); theme-aware; responsivo (mobile ~full); legível sobre a capa. (FR-001,002,009)
- [x] **T102** `publicar/tema/companion.js`: launcher abre/minimiza; `session_id` em localStorage; render do cabeçalho de capacidades (mapa + chapter + mode); `POST /chat`, `GET /history`, `POST /session`; estado "enviando"; seletor de modo; degradação graciosa. (FR-001..008)

## Fase 2 — Integração no motor

- [x] **T201** `publicar/sumario.json`: `"companion_backend": "https://harnessengineering-production.up.railway.app"`. (FR-007)
- [x] **T202** `publicar/build.mjs`: derivar `chapter` por item (título "NN — …" → NN; capa/aparato → 0); espelhar `capabilities` (chave/rótulo/descrição/libera); injetar `window.COMPANION` + `<link>`/`<script>` do widget em `pagina()` e `paginaSplash()`; copiar `companion.css`/`companion.js` para `assets/`. (FR-003, FR-007)

## Fase 3 — Verificação

- [x] **T301** `node build.mjs`: build verde; `companion.js/.css` em `docs/assets/`; `window.COMPANION` presente nas páginas e na splash; link-check sem quebras. (FR-010)
- [x] **T302** Screenshots (Playwright): launcher fechado na splash; painel aberto (cabeçalho de capacidades) numa página de capítulo; mobile sem overflow. (SC-001,002,006)
- [x] **T303** Revisão: sem identificador interno de modelo; sem segredo; a11y (aria-label, foco). (FR-010, SC-006)

## Fase 4 — Registro e merge

- [x] **T401** `livro/HISTORICO.md`: edição 0.13 (widget do companion) + modelo de IA (A3).
- [x] **T402** Commit na branch `017-…`, merge para `main` (`--no-ff`), push → dispara o deploy do site. (Princípio VII)
