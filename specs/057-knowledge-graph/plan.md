# Plan — 057

1. `publicar/grafo.mjs` (módulo puro, exporta `gerarGrafo(itens, RAIZ)`): listas fixas de harnesses (16, com variantes de nome) e conceitos (6); parse dos .md publicados; arestas por regex com peso; retorna {nos, arestas, geradoEm(versão)}. `build.mjs` importa, grava `docs/assets/grafo.json` (após as páginas, antes do portão embutido).
2. `tema/grafo.js`: carrega grafo.json (fetch relativo — mesmo host, sem CORS); simulação própria (repulsão O(n²) para ~55 nós, molas nas arestas, gravidade ao centro, ~300 iterações com esfriamento + interativo); canvas com devicePixelRatio; interações (drag/zoom/hover/click/filtros); painel lateral simples em DOM.
3. `livro/apendice-grafo.md` + entrada no sumario.json (Aparato, após "Uso do livro").
4. Portão: checagens do grafo.json no verifica-capitulos.mjs.
5. e2e + screenshot; HISTORICO 0.52; corpus; merge --no-ff; push.
