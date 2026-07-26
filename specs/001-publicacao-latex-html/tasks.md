# Tasks — Publicação (feature 001)

## P1 — Site navegável (MVP)  ← esta fase
- [x] T101 — `publicar/package.json` + instalar markdown-it (motor em Node)
- [x] T102 — `publicar/sumario.json`: manifesto ordenado (partes, 00–17, apêndices)
- [x] T103 — `publicar/build.mjs`: ler manifesto → markdown-it → template → `docs/`
- [x] T104 — tema `publicar/tema/estilo.css`: sidebar, claro/escuro, código, callouts, responsivo
- [x] T105 — navegação anterior/próximo + reescrita de links `.md → .html`
- [x] T106 — data de captura extraída e exibida no capítulo
- [x] T107 — gerar `docs/` a partir do Markdown atual e verificar build sem erro
- [x] T108 — `docs/.nojekyll` + nota de configuração do GitHub Pages (main/docs)

## P2 — Visualizações React (islands)
- [x] T201 — componente: comparativo do benchmark (tabela sortável, notas por dimensão/categoria) → `publicar/viz/BenchmarkTabela.jsx`
- [x] T202 — componente: registro de expiração (placar 🔵🟡🟢🔴 com filtro por estado) → `publicar/viz/Expiracao.jsx`
- [x] T203 — heatmap de notas por harness (células coloridas por nota 0–3, integradas à tabela sortável de T201)
- [x] T204 — bundle (esbuild, IIFE) e montagem como islands `<div data-viz>` nas páginas geradas; dados canônicos em `benchmark/notas.json`

## P3 — PDF via LaTeX
- [ ] T301 — passo de geração PDF (pandoc + template LaTeX) atrás do comando de build
- [ ] T302 — capa, TOC, numeração, bibliografia, código; hifenização PT-BR (babel/polyglossia)
- [ ] T303 — provisionar texlive na infra (apêndice) e no CI

## P4 — CI + apêndice de infra
- [x] T401 — GitHub Actions: build + publish `docs/` a cada push no main
- [x] T402 — portão de qualidade: link interno quebrado / capítulo que não compila falha o build
- [ ] T403 — `livro/apendices/infra.md`: apêndice que documenta o pipeline (o "harness de publicação")
- [ ] T404 — `HISTORICO.md`: registrar a edição; `make book`/script único documentado

> Legenda: [x] feito · [ ] pendente. Fase corrente: **P1** (MVP do site navegável).
