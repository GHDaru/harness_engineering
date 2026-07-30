# ADR 0003 — Sequência didática: fundamentos → compensatórios → outranking → robustez

- **Status**: Aceito
- **Data**: 2026-07-30
- **Relacionado**: `livro/SUMARIO.md`; `livro/GUIA-EDITORIAL.md`; spec 001

## Contexto

Um livro de MCDA pode ser organizado por método (catálogo), por escola (americana ×
europeia) ou por problema. O público-alvo aprende **lendo e construindo**: cada capítulo
precisa terminar em código executável, e conceitos devem aparecer exatamente quando a
etapa anterior criou a dor que eles resolvem (4C/ID + carga cognitiva).

## Decisão

Sequência em 4 partes (14 capítulos), dirigida pela dor:

1. **Fundamentos (00–03)** — modelagem antes de método: matriz de decisão, a falha da
   soma crua (motiva normalização), estruturação de critérios (Keeney), dominância
   (o que dá para decidir *sem* método), normalização e pesos.
2. **Compensatórios (04–07)** — do mais simples ao mais fundamentado: SAW/SMART → AHP
   (elicitação par a par + consistência) → TOPSIS (geometria) → MAUT/MAVT + Even Swaps
   (a fundação axiomática, apresentada por último porque é a mais abstrata).
3. **Outranking (08–09)** — PROMETHEE antes de ELECTRE (fluxos são mais palatáveis que
   concordância/discordância/veto); a pergunta-chave "quando NÃO compensar".
4. **Robustez, grupo e produto (10–13)** — VIKOR/BWM, sensibilidade e rank reversal
   (só faz sentido depois de conhecer ≥3 métodos que discordam), decisão em grupo, e a
   virada protótipo→produto (persistência Neon, deploy).

Um único **caso âncora** (apartamento) atravessa tudo; cada método novo é aplicado a ele
primeiro, permitindo comparação direta entre métodos no cap. 11.

## Alternativas avaliadas

- **Catálogo de métodos (um por capítulo, sem ordem interna)** — rejeitado: é o formato
  dos surveys (Greco et al.), ótimo para consulta, ruim para aprender.
- **Escola europeia primeiro** — rejeitado: outranking exige maturidade sobre limites da
  compensação, que só se adquire usando métodos compensatórios.
- **AHP primeiro (popularidade)** — rejeitado: começar por elicitação par a par esconde
  a anatomia comum (matriz + pesos + agregação) que o SAW expõe com clareza.

## Consequências

- O produto (`app/`) ganha métodos na ordem do livro; o cap. 11 destrava a feature mais
  valiosa do Decisor (comparação multi-método lado a lado).
- A Parte I inteira roda sem nenhum "método famoso" — é deliberado: modelagem é onde
  decisões reais mais erram.

## Fontes

- Belton & Stewart (2002) — integração das escolas: <https://link.springer.com/book/10.1007/978-1-4615-1495-4>
- Ishizaka & Nemery (2013) — modelo "método → exemplo → software" (DOI 10.1002/9781118644898)
- Wątróbski et al. (2018) — seleção de método: <https://arxiv.org/abs/1810.11078>
- van Merriënboer & Kirschner — 4C/ID (base pedagógica herdada do guia editorial do
  Engenharia de Harness)
