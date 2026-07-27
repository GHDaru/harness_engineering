# Tasks: Landing / hero de capa no site

**Feature**: `012-landing-capa` · Tests: n/a (gate = build + verificação visual Playwright).

## Phase 1: Setup — assets

- [x] T001 `git mv "publicar/tema/Engenharia de Harness.png" publicar/tema/capa.png` (nome sem espaços — FR-001).
- [x] T002 Gerar `publicar/tema/capa-social.png` (1200×630, capa contida em fundo escuro) via Chromium/Playwright (FR-005).

## Phase 2: Foundational — motor copia os assets

- [x] T003 Em `publicar/build.mjs`, copiar `tema/capa.png` e `tema/capa-social.png` para `docs/assets/` (junto de estilo.css/app.js) (FR-007).

## Phase 3: User Story 1 — hero no index (P1) 🎯 MVP

- [x] T004 [US1] Em `publicar/build.mjs`, adicionar a **hero** no corpo do `index.html`: `<img>` da capa com `alt` descritivo + título + subtítulo + CTA "Começar a ler" (→ `00-introducao.html`) + atalhos (Benchmark → `comparativo.html`, Guia → `guia-editorial.html`) + créditos em texto (Gilsiley Henrique Darú; Claude/Anthropic; GPT/OpenAI). Sumário permanece abaixo (FR-002/003/004/008).
- [x] T005 [US1] Adicionar meta tags Open Graph no `<head>` do template (`og:title`, `og:description`, `og:image`→`assets/capa-social.png`, `twitter:card`) — apenas no index ou em todas as páginas (FR-005).
- [x] T006 [US1] CSS da hero em `publicar/tema/estilo.css`: layout 2 colunas (imagem+texto) que **empilha no mobile**, theme-aware (claro/escuro), botões de CTA (FR-006).

## Phase 4: Polish & Cross-Cutting

- [x] T007 **Revisão developmental** (portão v1.2.0): a hero comunica "livro"? CTA claro? créditos legíveis? não sobrecarrega?
- [x] T008 Build (`node publicar/build.mjs`) verde; verificação visual em Chromium (desktop + ~375px) — screenshot; conferir SC-001..006.
- [x] T009 Registrar edição no `livro/HISTORICO.md` (com agente/modelo — A3).

## Dependencies / Strategy
- MVP = T001–T004 + T006 (a hero visível). T005 (social) e polish depois. T003 bloqueia a exibição dos assets.
