# Tasks: Tela-capa full-screen (splash)

- [x] T001 [US1] `build.mjs`: novo template `paginaSplash()` (full-screen, sem sidebar, fundo escuro) — capa grande + título + subtítulo + descrição + créditos + CTAs (Entrar no livro → sumario.html; Benchmark; Guia); meta OG mantidas. (FR-001/005/007/008)
- [x] T002 [US1] `build.mjs`: gerar `index.html` via `paginaSplash`; gerar **`sumario.html`** via `pagina()` com o conteúdo do índice atual (título+subtítulo+lista de partes). (FR-002)
- [x] T003 [US1] `build.mjs`: marca (sidebar) → `sumario.html` + link discreto "capa" → `index.html`; paginação: Sumário↔1º capítulo. (FR-003/004)
- [x] T004 `build.mjs`: incluir `sumario.html` no conjunto de páginas válidas do gate de link-check. (FR-006)
- [x] T005 [US1] CSS `estilo.css`: `.splash` full-screen (100svh), 2 colunas → empilha no mobile; capa até ~78svh; botão primário grande. (FR-005)
- [x] T006 Revisão developmental (v1.2.0) + build verde + verificação visual desktop/375px (screenshots) — SC-001..006.
- [x] T007 Registrar edição no `HISTORICO.md` (agente/modelo — A3).
