# Spec 065 — Promoção do Radar: papers de julho + conferência A2A

**Branch**: `065-papers-a2a` · **Data**: 2026-07-31 · **Status**: aprovada ("vamos promover as análises dos papers e a conferência")

## Contexto

Restavam dois itens da varredura de 2026-07-31 no Radar: (1) três papers de julho
avaliados só pela busca (⏳ PDFs não lidos) — *Rethinking the Evaluation of Harness
Evolution for Agents* (2607.12227), *CompactionRL* (2607.05378) e o survey *Agent
Systems with Harness Engineering* (RUCAIBox); (2) a conferência de que o adendo do
cap. 17 cobre o status v1.0 do A2A. O editor promoveu ambos.

## O que muda

1. **Leitura dirigida real** dos três papers (agentes de leitura com WebFetch,
   relatório com metadados verificados e trechos citáveis) — o ⏳ sai.
2. **Bibliografia**: os papers que sobreviverem à leitura entram como itens
   verificados (Princípio I), com nota opinativa.
3. **Capítulos**: nota no cap. 11 (o que o paper de harness-evolution diz sobre
   avaliar harness — valida/refina o método do nosso benchmark?); nota no cap. 04
   (CompactionRL como terceira via: compactação **aprendida no treino**, além de
   "harness compacta" e "API compacta"); referência ao survey onde couber (cap. 01
   ou bibliografia — a disciplina do livro agora tem survey acadêmico).
4. **Cap. 17**: adendo enriquecido com o resultado da conferência A2A (v1.0 já
   coberto; acrescentar v1.0.1/mecanismo de extensões e arquitetura em camadas,
   com fonte primária).
5. **Radar**: papers → `promovido (spec 065)`; A2A → `conferido (spec 065)`.
6. **HISTORICO**: edição 0.60.

## Requisitos

- **R1 — Sem fabricação**: toda afirmação incorporada vem do texto realmente lido
  nesta execução; o que não se confirmar é registrado como divergência no diário
  do Radar (a busca pode ter exagerado).
- **R2 — Notas cirúrgicas**: adendos datados nos capítulos, sem reescrever teses —
  mudanças maiores esperam a janela 2026-10 (ADR 0007).
- **R3 — Leituras executivas**: se algum paper invalidar uma síntese, tratar como
  gatilho extraordinário (registrar impacto A no RADAR e parar — ADR 0008 não se
  aplica aqui, mas a curadoria é a mesma).

## Verificação

- Bibliografia sem ⏳ nos itens novos; build + portões verdes; e2e Chromium
  (notas nos caps. 04/11/17 renderizadas; bibliografia com os itens).
- RADAR atualizado; HISTORICO 0.60; corpus regenerado; merge --no-ff; CI verde.
