# Spec 055: Apêndice vivo — Uso do livro (resumo da telemetria)

**Feature Branch**: `055-apendice-uso-vivo` · **Criada em**: 2026-07-29

## Conceito

O livro que ensina verificação e observabilidade (caps. 11/13) passa a **expor a própria telemetria**: uma página do aparato mostra, ao vivo, como o livro é usado — páginas mais lidas, total de visitas — alimentada pelos dados da spec 054. É o "livro vivo" fechando o ciclo: o leitor vê o mesmo painel que orienta a cadência de revisão (ADR 0007).

## Requisitos

- FR-001 (backend): novo `GET /telemetry/publico` — **agregado e anônimo por construção**: `{total, por_pagina: {slug: visitas}, paginas_distintas}`. Sem sessões, sem timestamps individuais, sem token (é público porque não há nada pessoal). O `GET /telemetry` (admin) permanece com os detalhes.
- FR-002 (página): `livro/apendice-uso.md` — "Apêndice — Uso do livro (vivo)", no Aparato do sumário, com: o que é medido e por quê (só navegação, só com consentimento — spec 054); o modelo de privacidade (anônimo, agregado, LGPD/esquecimento); **a ilha viva** `<div data-viz="uso-livro">` (mesma convenção C10); e como o dado alimenta a cadência (ADR 0007).
- FR-003 (ilha): `tema/uso.js` (JS puro, sem React) preenche a ilha no navegador: total de visitas, páginas distintas e o **top de páginas em barras** (slug → título legível; barra proporcional; theme-aware). Backend indisponível → mensagem honesta ("dados vivos indisponíveis agora"). No PDF a ilha some (regra `[data-viz]` já existente) — o texto avisa que os números são da versão online.
- FR-004: build (uso.js copiado e carregado como viz.js), link-check, portão por capítulo e corpus verdes; teste backend do endpoint público; e2e da ilha com backend local semeado.

## Privacidade

O endpoint público expõe estritamente contagens agregadas por página — nada identifica sessão ou pessoa; é o mesmo princípio do placar de expiração. Auditável no código (`nav_stats` → projeção pública sem `ultimos`).
