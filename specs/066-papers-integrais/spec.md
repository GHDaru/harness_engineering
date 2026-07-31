# Spec 066 — Leitura integral dos preprints (arXiv liberado)

**Branch**: `066-papers-integrais` · **Data**: 2026-07-31 · **Status**: aprovada (decisão de rede do editor)

## Contexto

Na spec 065, dois preprints entraram no livro avaliados **pelo abstract**, com a
pendência marcada com honestidade ("texto integral pendente — arXiv inacessível
deste ambiente"). O editor decidiu mudar a política de rede do Environment para
**acesso completo** — registrando que é *"a única exceção até o momento"*, motivada
pela dinâmica do livro vivo (o Radar precisa ler fontes primárias). O curl confirma:
arXiv responde 200 deste container.

## O que muda

1. **Releitura integral** dos dois preprints pelos mesmos agentes (contexto
   preservado; mandato: só deltas + confirmações verbatim com seção/tabela):
   - CompactionRL (arXiv 2607.05378) — números, citações e a limitação do
     train–test mismatch confirmados ou corrigidos;
   - Rethinking the Evaluation of Harness Evolution (arXiv 2607.12227) — autores
     (a lista veio de fonte terciária), números, citações e limitações declaradas.
2. **Promoção das notas**: os adendos dos caps. 04 e 11 e os itens da bibliografia
   perdem a ressalva de pendência (ou são corrigidos, se o texto integral divergir
   do abstract — divergência vira registro no diário, Princípio I).
3. **Diário do Radar**: registra a mudança de política de rede (decisão do editor,
   escopo, motivação) e o resultado da releitura.
4. **HISTORICO**: edição 0.61.

## Requisitos

- **R1**: nenhuma citação permanece no livro sem confirmação verbatim no texto
  integral; números divergentes são corrigidos nos capítulos E no diário.
- **R2**: a ressalva "texto integral pendente" só sai onde a leitura de fato
  aconteceu.
- **R3**: a decisão de rede fica documentada (auditabilidade da exceção).

## Verificação

- e2e Chromium: caps. 04/11 e bibliografia sem a ressalva de pendência; build +
  portões verdes; corpus regenerado; merge --no-ff; CI verde.
