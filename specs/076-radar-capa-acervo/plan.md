# Plano — spec 076

| Arquivo | Mudança |
|---|---|
| `publicar/jornal.mjs` | `gerarJornal()` passa a devolver **lista de páginas** (capa + uma por mês) em vez de uma string. Novos: `lerEdicoes`, `lerMesa` (parser da tabela do RADAR.md), `resumo()` (corte seguro que não parte link), `montarCapa`, `montarAcervo`. |
| `publicar/build.mjs` | Escreve todas as páginas devolvidas; coleta `paginasRadar` e as inclui no portão de links internos (inclusive como origem). |
| `publicar/tema/estilo.css` | Blocos novos: `.jr-placar`, `.jr-mesa`, `.jr-filtros/.jr-chip`, `.jr-dia`, `.jr-acervo-*`, `.jr-arq-*`; responsivo em 640px. |

Verificação: build 4 passos; Chromium/Playwright sobre o `docs/` servido — filtro clicado
(todos → A → todos), contagem dos chips, zero erro de JS; checagem programática de resíduo de
markdown na mesa; conferência de que as caixas de transparência não se repetem na capa.

Sem delta EN: o Radar é PT-only por decisão da spec 067.
