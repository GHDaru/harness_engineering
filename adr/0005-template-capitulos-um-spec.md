# 0005 — Template visual dos capítulos: um spec de motor, verificação por capítulo

- **Status:** Aceito
- **Data:** 2026-07-28
- **Contexto (feature/spec):** `043-template-capitulos`

## Contexto
O autor aprovou a linguagem visual da entrada (spec 021: cartão com badge/título/teaser) como base do template dos capítulos, e pediu "spec-kit por capítulo". O template, porém, é renderizado pelo motor (`pagina()`): uma mudança atinge os 18 capítulos simultaneamente — não há trabalho de conteúdo por capítulo nesta feature.

## Decisão
**Um spec de motor (`043`)** implementa o template (cabeçalho-herói do capítulo com badge/parte/teaser/data/tempo de leitura + paginação em cartões), e a **verificação é por capítulo** (build + screenshots de amostra representativa + checagem automática de todos). Capítulos que precisarem de ajuste individual ganham **specs próprios** depois.

## Alternativas avaliadas
- **A — 18 ciclos spec-kit (um por capítulo)**: fiel à letra do pedido; mas cada ciclo teria o MESMO diff de motor — cerimônia sem conteúdo, ruído no histórico.
- **B — 1 spec de motor + verificação por capítulo (escolhida)**: fiel ao espírito (rigor por capítulo na verificação), sem duplicação.
- **C — Template por conteúdo (editar 18 .md)**: colocaria HTML nos fontes Markdown — viola a separação conteúdo×apresentação do motor.

## Justificativa
O Princípio VII pede um spec por *melhoria*; a melhoria aqui é uma (o template). A granularidade por capítulo entra onde agrega: na verificação. B preserva o histórico limpo e a porta aberta para ajustes individuais com specs próprios.

## Consequências
- Positivas: um diff, todos os capítulos consistentes; verificação rastreável por capítulo.
- Custos: se um capítulo pedir exceção visual, será um spec adicional (aceito).
- Reversibilidade: alta.
