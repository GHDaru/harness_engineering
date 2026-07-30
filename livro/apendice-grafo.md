# Apêndice — Grafo do livro (vivo)

> **Estado da arte capturado em 2026-07** · última revisão 2026-07-30 · [histórico e registro de expiração](HISTORICO.md)

Todo livro técnico é um grafo disfarçado de sequência: capítulos que se citam, sistemas que aparecem em várias dimensões, conceitos que costuram tudo. Esta página torna o grafo explícito — e **interativo**.

## Como este grafo é construído (e por que ele nunca desatualiza)

Os nós e as arestas **não são editados à mão nem gerados por um modelo**: são extraídos **deterministicamente do próprio Markdown** a cada build do site, pelo motor de publicação (`publicar/grafo.mjs`). Uma aresta capítulo→harness existe porque aquele capítulo *menciona* aquele sistema no texto — com o peso igual ao número de menções (Princípio I: cada aresta é evidência textual verificável). Como o build roda a **cada mudança publicada do livro**, o grafo acompanha o conteúdo por construção — atualizá-lo não é um processo, é uma propriedade.

- **Nós** (4 tipos): os 18 **capítulos**; os 16 **sistemas do corpus** do estudo; **conceitos**-chave (MCP, A2A, ACP, LSP, RAG, MAST); as 13 **etapas do harness-zero**.
- **Arestas**: capítulo→capítulo (referências cruzadas "cap. NN"), capítulo→sistema (menções), capítulo→conceito (ocorrências), capítulo→etapa (a trilha Mão na massa).

## O grafo interativo

<div data-viz="grafo-livro"></div>

*(A visualização existe apenas na versão online — no PDF esta ilha é omitida por definição.)*

## Guia de leitura

- **Hubs**: os nós maiores concentram conexões — espere ver o cap. 02 (Loop) e sistemas avaliados em todas as dimensões como centros gravitacionais.
- **Pontes**: conceitos como MCP conectam grupos que de outro modo ficariam distantes (o cap. 06 ao cap. 17, o corpus aos protocolos) — é a costura do livro visível.
- **A trilha prática**: filtre por "harness-zero" para ver como as etapas amarram os capítulos teóricos à construção (Backward Design em forma de grafo).
- **Clique em qualquer nó** para isolar a vizinhança e navegar direto para a página correspondente.
