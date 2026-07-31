# Plano — Spec 064 (extensão do corpus: Grok Build e Pi)

## Método

1. **Leitura** (2 agentes de exploração em paralelo, um por clone): varredura das 14
   dimensões do HARNESS_EVAL com caminhos de arquivo como evidência. Clones:
   `/workspace/grok-build` (Rust) e `/workspace/pi` (TS, monorepo).
2. **Julgamento** (editor-agente, no contexto principal): notas 0–3 por dimensão a
   partir da evidência reportada, calibradas contra as avaliações existentes
   (gemini-cli=36 é a régua do teto; Aider=28 mostra como um projeto forte pontua
   baixo em dimensões que rejeita — precedente direto para o Pi).
3. **Escrita**: avaliações → comparativo/notas.json → livro (cap. 03 caixa, cap. 10
   nota, apêndice do estudo) → grafo.mjs → RADAR → HISTORICO.

## Mudanças por arquivo

- `benchmark/avaliacoes/grok-build.md`, `benchmark/avaliacoes/pi.md` — novas, no template.
- `benchmark/comparativo.md` — cabeçalho (11→13 avaliados; rodada ext-1), colunas novas
  na tabela de código, leitura da rodada ext-1 (2–3 bullets).
- `benchmark/notas.json` — 2 entradas em `categorias.codigo.harnesses` + nota da rodada.
- `livro/capitulos/03-contexto.md` — caixa "O contraponto: o harness mínimo (Pi)".
- `livro/capitulos/10-subagentes-orquestracao.md` — nota worktrees (Grok Build), se
  confirmada no código.
- `livro/apendice-estudo.md` — seção "Extensão ext-1 (2026-07-31)": teste de inclusão,
  processo Radar→promoção, corpus 16→18.
- `publicar/grafo.mjs` — 2 entradas em HARNESSES (regex \bGrok Build\b / \bPi\b — cuidado:
  "Pi" de 2 letras colide com palavras; usar regex com fronteira estrita e caso exato).
- `radar/RADAR.md` — status → promovido (spec 064).
- `livro/HISTORICO.md` — edição 0.59 + rodada ext-1 na tabela de rodadas (se houver).

## Riscos

- **Regex do Pi no grafo**: `\bPi\b` casa "Pi" em contextos errados (π, "Pi" em inglês).
  Mitigação: casar só "Pi" com maiúscula isolada e revisar contagens; se ruído, usar
  `(?:o\s|harness\s)?Pi\b` restrito aos capítulos que o citam de fato.
- **Rust denso do grok-build**: leitura por agente pode perder profundidade em
  permissões/sandbox — pedir caminhos e conferir os módulos citados por amostragem.
- **Tamanho da sessão**: agentes de exploração devolvem só o relatório (contexto limpo).

## Verificação

- Portões + build + e2e Chromium (comparativo com colunas novas; caixa no 03; nós no grafo).
- Corpus do companion regenerado; merge --no-ff; CI verde.
