# publicar/ — o motor do livro

App próprio (não framework) que gera o site navegável do livro a partir do
**Markdown** em `livro/`. Coerente com a tese do livro (portas-e-adaptadores):
a fonte é única; a publicação é um adapter sobre ela.

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

## Roadmap (spec 001)

- **P1 (feito)** — site navegável a partir do Markdown.
- **P2** — visualizações React como *islands* (`data-viz`): comparativo do
  benchmark, registro de expiração, radar de notas.
- **P3** — PDF via LaTeX do mesmo Markdown.
- **P4** — CI (publica a cada push) + portão de qualidade (link quebrado falha
  o build) + apêndice do livro que documenta esta infraestrutura.
