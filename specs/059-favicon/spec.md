# Spec 059: Favicon

**Feature Branch**: `059-favicon` · **Criada em**: 2026-07-30

- FR-001: favicon na identidade do livro (a metáfora da capa: **núcleo âmbar = modelo, anel segmentado = harness**, fundo azul-escuro do splash), legível a 16px.
- FR-002: `favicon.svg` (fonte, nítido em qualquer escala) + `favicon-32.png` (fallback) + `apple-touch-icon.png` 180px (iOS), gerados a partir do SVG; `<link rel>` nos dois templates (páginas e splash) via `build.mjs`.
- FR-003: build/portão verdes; conferência visual em 16/32/180px.
