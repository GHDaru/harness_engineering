# Spec 064 — Extensão do corpus: Grok Build e Pi (promoção do Radar)

**Branch**: `064-corpus-ext` · **Data**: 2026-07-31 · **Status**: aprovada ("vamos promover o Grok Build e o Pi com o speckit")

## Contexto

A varredura do Radar de 2026-07-31 encontrou dois candidatos de impacto B que o editor
promoveu no mesmo dia: **Grok Build** (xAI; harness terminal completo aberto sob Apache
2.0 em 2026-07-15) e **Pi** (Earendil/Zechner; o contraponto minimalista — system prompt
<1k tokens, ~4 tools, lazy skills, sem MCP/subagentes/permissões por decisão). O editor
forkou os repositórios (`ghdaru/grok-build`, `ghdaru/pi`) para leitura de código.
É a primeira promoção Radar→corpus e a primeira ampliação desde a rodada 2.

## O que muda

1. **Duas avaliações completas** no protocolo do benchmark (template HARNESS_EVAL,
   12 dimensões 0–3 + 2 suplementares, evidência por caminho de arquivo):
   `benchmark/avaliacoes/grok-build.md` e `benchmark/avaliacoes/pi.md`.
   Rodada nova: **ext-1 (2026-07-31)** — as fotos das rodadas 1/2 não são sobrescritas.
2. **Comparativo e notas**: colunas novas na categoria "harnesses de código" em
   `benchmark/comparativo.md` + entradas em `benchmark/notas.json` (viz do site).
3. **Livro**:
   - cap. 03: caixa de contraste "o harness mínimo" (a filosofia do Pi vs. a tese
     da montagem rica de contexto — com evidência do código);
   - cap. 10: nota sobre subagentes paralelos em git worktrees do Grok Build
     (se confirmado no código);
   - apêndice O estudo: seção "Extensão ext-1" (corpus 16 → 18, como e por quê);
   - grafo: Grok Build e Pi como nós de harness (arestas nascem das menções).
4. **Radar**: os dois itens → `promovido (spec 064)`.
5. **HISTORICO**: edição 0.59 + tabela de rodadas.

## Requisitos

- **R1 — Protocolo íntegro**: mesma régua das rodadas 1/2 (nota exige evidência de
  código com caminho; sem evidência, não pontua). Leitura profunda dos dois clones.
- **R2 — Rodada própria**: rotular tudo como rodada ext-1/2026-07-31; nunca editar
  notas históricas dos outros 16.
- **R3 — O Pi avaliado nos termos dele**: ausências deliberadas são documentadas como
  DECISÃO (com a evidência da filosofia), e a nota reflete a régua comum — o texto
  explica a tensão (é isso que torna o contraste honesto).
- **R4 — Sem quebra do site**: portões verdes; grafo continua ≥40 nós/≥100 arestas;
  viz do benchmark renderiza as colunas novas.
- **R5 — Fontes**: links verificados (anúncios oficiais + código); nada de memória.

## Fora de escopo

- Reavaliar os 16 existentes (janela 2026-10, ADR 0007).
- Traduzir as descobertas em mudanças de tese dos capítulos além da caixa (03) e da
  nota (10) — mudanças maiores esperam a rodada completa.

## Verificação

- As duas avaliações completas (14 dimensões preenchidas, tabela de síntese).
- `npm run build` + portões verdes; e2e: comparativo mostra as colunas novas,
  cap. 03 mostra a caixa, grafo contém os nós grok-build e pi.
- RADAR com status promovido; HISTORICO 0.59; corpus do companion regenerado.
