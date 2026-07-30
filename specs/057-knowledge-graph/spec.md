# Spec 057: Knowledge Graph do livro — apêndice interativo, sempre em sincronia

**Feature Branch**: `057-knowledge-graph` · **Criada em**: 2026-07-30

## Conceito

Um grafo de conhecimento **derivado deterministicamente do próprio Markdown** no build: capítulos, harnesses do corpus, conceitos/protocolos e etapas do harness-zero como nós; menções reais no texto como arestas. Como a extração roda **dentro do `npm run build`** (local e no CI a cada push), o grafo é **regenerado automaticamente toda vez que o livro muda** — o requisito de atualização vira propriedade estrutural, não processo.

## Requisitos

- FR-001 (extração): `publicar/grafo.mjs`, chamado pelo `build.mjs`, varre os fontes publicados e emite `docs/assets/grafo.json`:
  - **Nós**: capítulos numerados (do sumário); os 16 sistemas do corpus; conceitos-chave (MCP, A2A, ACP, LSP, RAG, MAST); etapas 00–12 do harness-zero. Cada nó: id, tipo, rótulo, url (página do capítulo / âncora do apêndice do estudo / glossário / GitHub da etapa).
  - **Arestas** (com peso = nº de menções): capítulo→capítulo ("cap. NN" no corpo); capítulo→harness (menção por nome); capítulo→conceito (ocorrência da sigla); capítulo→etapa ("etapa N" na Mão na massa).
  - Determinístico e sem LLM (Princípio I: as arestas são evidência textual verificável).
- FR-002 (visualização): ilha `data-viz="grafo-livro"` em `livro/apendice-grafo.md` — **força dirigida em canvas, JS puro** (`tema/grafo.js`, zero dependências): cores por tipo + legenda com filtro, arrasto de nós, zoom (roda), hover com rótulo, clique → destaca vizinhos + painel com link para a página do nó. Theme-aware.
- FR-003 (página): "Apêndice — Grafo do livro" no Aparato: o que são nós/arestas, como o grafo é derivado (e por que isso garante o sincronismo), guia de leitura (hubs, pontes) e a ilha. No PDF a ilha é omitida (regra existente) com aviso.
- FR-004 (portão): `verifica-capitulos.mjs` confere que `grafo.json` existe, tem os 18 capítulos e contagens sane (≥40 nós, ≥100 arestas) — build falha se a extração regredir.
- FR-005: build/link-check/corpus verdes; e2e Playwright: ilha renderiza N nós, filtro funciona, clique destaca e mostra painel.

## Fora de escopo

- Grafo semântico via LLM (não-determinístico; violaria o sincronismo garantido); edição manual do grafo (é 100% derivado).
