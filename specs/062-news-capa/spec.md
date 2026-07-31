# Spec 062 — Novidades na capa (splash)

**Branch**: `062-news-capa` · **Data**: 2026-07-31 · **Status**: aprovada (pedido direto do editor)

## Contexto

A spec 061 criou o "jornal vivo" — card da última notícia do Radar + linha da edição
corrente — mas o colocou na página de **entrada** (`sumario.html`). O editor aprovou
mantê-lo lá, porém o pedido original era a **capa** (`index.html`, o splash): *"me
referia a capa mesmo com destaque para as novidades"*.

## O que muda

Na tela-capa (splash), entre os CTAs e os créditos:

1. **Destaque maior** — a última notícia relevante do Radar (mesma fonte da 061:
   primeira linha de dados de `radar/RADAR.md` que não seja a `(inicial)`), em card
   âmbar com kicker "🗞 Novidade", data, badge de impacto e link para o Radar.
2. **Destaque menor** — "o que mudou na última versão": versão + título da edição
   corrente de `livro/HISTORICO.md`, em linha discreta com link para o Histórico.

## Requisitos

- **R1** — O splash exibe a última notícia do Radar com destaque visual (card),
  derivada no build de `radar/RADAR.md`. Sem edição manual: capa noticia por construção.
- **R2** — O splash exibe a mudança da edição corrente (versão, data, título) com
  hierarquia visual menor que a notícia, derivada de `livro/HISTORICO.md`.
- **R3** — Parse falho de qualquer fonte ⇒ o bloco correspondente é **omitido**;
  a capa nunca quebra por causa do jornal (mesma postura da 061).
- **R4** — A entrada (`sumario.html`) mantém o bloco da 061 **inalterado** ("ficou,
  pode deixar").
- **R5** — O visual respeita o splash: não compete com o título nem com os CTAs;
  responsivo; sem JS novo (HTML/CSS gerados no build).

## Fora de escopo

- Mudar as fontes de dados ou o formato do RADAR/HISTORICO.
- Feed com mais de 1 notícia (a capa destaca *a* última; o Radar completo é o link).

## Verificação

- Portão `verifica-capitulos.mjs`: `index.html` contém `.splash-news` e
  `.splash-vedicao` quando as fontes parseiam (as fontes atuais parseiam).
- e2e Chromium: capa renderiza a notícia real (texto do RADAR), o badge de impacto,
  a linha da edição com a versão corrente, e os links (Radar e Histórico) corretos;
  entrada segue com `.ent-news` (R4).
