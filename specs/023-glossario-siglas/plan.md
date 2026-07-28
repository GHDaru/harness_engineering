# Plan: Glossário + siglas
**Branch**: `023-glossario-siglas`
## Constitution Check — PASS
I (evidência): siglas/expansões da fonte. IV: edição no HISTORICO. VI: abbr acessível. VII: branch→merge. Sem identificador interno de modelo.
## Arquivos
- `livro/glossario.md` — a página do glossário (sigla · por extenso · explicação · capítulos).
- `publicar/sumario.json` — Glossário no Aparato.
- `publicar/build.mjs` — mapa `SIGLAS` + `abrirSiglas(html)` (envolve em `<abbr>` fora de code/pre/a/hN), aplicado aos capítulos (menos a própria página do glossário).
- `publicar/tema/estilo.css` — `abbr[title]` discreto/acessível.
- `livro/GUIA-EDITORIAL.md` — política de siglas.
## Design
- Fonte única do mapa no build; a página do glossário mirroreia (pequena duplicação, comentada).
- Auto-abbr é HTML-safe (tokeniza por tags, respeita regiões protegidas).
