# ADR 0004 — Publicação do livro: MkDocs Material no GitHub Pages

- **Status**: Aceito
- **Data**: 2026-07-30
- **Relacionado**: `mkdocs.yml`; `.github/workflows/pages.yml`; ADR 0001

## Contexto

O livro será publicado no GitHub Pages. O repositório-modelo (harness_engineering) usa um
motor próprio em Node (markdown-it + tema + portões de design + PDF via Playwright) —
poderoso, mas com custo de manutenção que um projeto nascente não deve pagar. Este livro
tem um requisito que o modelo não tinha: **fórmulas matemáticas** em quase todo capítulo.

## Decisão

Publicar com **MkDocs + tema Material**: `mkdocs.yml` na raiz do seed, capítulos servidos
direto de `livro/` (sem cópia), matemática via `pymdownx.arithmatex` + MathJax, busca,
tema claro/escuro. Deploy por GitHub Actions (`pages.yml`) com `mkdocs build --strict`
como portão (link quebrado = build vermelho). O workflow ativa quando o seed virar
repositório próprio (ADR 0001).

## Alternativas avaliadas

- **Herdar o motor Node do harness_engineering** — rejeitado por ora: acoplaria o seed ao
  repositório de origem e exigiria manter build.mjs/verifica-capitulos/pdf.mjs sem os
  portões que os justificam. Fica como evolução possível quando o livro tiver identidade
  visual própria (novo ADR).
- **Jekyll (Pages nativo)** — rejeitado: suporte a matemática e navegação inferiores ao
  Material sem plugins adicionais.
- **Docusaurus/Astro** — rejeitado (YAGNI): build Node + React para servir Markdown.

## Consequências

- `mkdocs build --strict` entra na DoD de toda rodada que toca o livro.
- Callouts pedagógicos do esqueleto v3 usam admonitions do Material; se o projeto quiser
  os componentes visuais do modelo (hero, leitura-exec), será um tema custom em ADR
  futuro.

## Fontes

- MkDocs Material: <https://squidfunk.github.io/mkdocs-material/>
- Arithmatex (MathJax): <https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/>
- Motor do modelo: `publicar/` do harness_engineering (ADR 0006 daquele repositório)
