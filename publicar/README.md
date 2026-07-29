# publicar/ — o motor do livro

App próprio (não framework) que gera o site navegável do livro a partir do
**Markdown** em `livro/`. Coerente com a tese do livro (portas-e-adaptadores):
a fonte é única; a publicação é um adapter sobre ela.

**Site publicado:** https://ghdaru.github.io/harness_engineering/ — deploy
automático a cada push no `main` que toque `livro/` ou `publicar/`.

## Uso

```bash
cd publicar
npm install        # markdown-it (biblioteca de parsing; o motor é nosso)
npm run build      # gera ../docs/ (site estático, servido pelo GitHub Pages)
```

Abra `../docs/index.html` no navegador.

## Como funciona

- `sumario.json` — ordem canônica do livro (partes, capítulos, apêndices).
- `build.mjs` — lê o manifesto, converte cada `.md` (markdown-it + âncoras),
  extrai o selo de data de captura (livro vivo), marca os callouts pedagógicos
  (objetivos/verificação/mão na massa/o que roubar/apêndice), reescreve links
  internos `.md → .html`, e monta cada página no template (sidebar + navegação
  anterior/próximo + tema claro/escuro).
- `tema/` — `estilo.css` (tema, callouts, responsivo) e `app.js` (alternância
  de tema, dependency-free).
- Saída em `../docs/` (GitHub Pages serve de `main/docs`; `.nojekyll` incluído).

## Estado do motor (atualizado na spec 052)

Tudo do roadmap original (spec 001) está entregue — P1 site, P2 ilhas React,
P3 PDF (via Chromium, não LaTeX: `pdf.mjs`, livro completo + por capítulo),
P4 CI com portões (link-check + `verifica-capitulos.mjs`). Além dele:
design system de componentes (`DESIGN-SISTEMA.md`, ADR 0006), downloads
PDF/Markdown, siglas automáticas, citações ligadas à bibliografia.
O backlog corrente vive nas specs (`specs/`) e no histórico do livro.
