# Feature Specification: Rodada ext-2 do benchmark — QM e Kimi Code

**Feature Branch**: `073-ext2-qm-kimi`

**Created**: 2026-08-02

**Status**: Aprovada pelo editor ("vamos colocar para entrar nas avaliacoes e benchmark" + confirmação dos dois forks)

**Input**: Radar 2026-08-02 (QM confirmado em fonte primária) + leitura crítica da página da Kimi (candidato Kimi Code verificado: MIT, MoonshotAI/kimi-code).

## Objetivo

Segunda promoção Radar→corpus: avaliar **QM (Y Combinator)** e **Kimi Code (Moonshot AI)**
com o instrumento HARNESS_EVAL (12 dimensões 0–3 + 2 suplementares, evidência = caminho de
arquivo em commit congelado) e integrá-los ao livro. Corpus: 18 → **20 sistemas**.

## Commits congelados (leitura nos forks)

| Sistema | Upstream | Fork | Commit | Licença |
|---|---|---|---|---|
| QM | yc-software/qm | GHDaru/qm | `7f2c916` | MIT |
| Kimi Code | MoonshotAI/kimi-code | GHDaru/kimi-code | `e22479a` | MIT |

## Entregas

1. `benchmark/avaliacoes/qm.md` e `benchmark/avaliacoes/kimi-code.md` (rodada ext-2).
2. `benchmark/notas.json` (+2 entradas, `rodada: "ext-2"`, soma validada).
3. `benchmark/comparativo.md` — tabela + leitura da rodada ext-2.
4. Livro: contagem 18→20 e menções (00/01, Apêndice A/apendice-estudo); **delta EN traduzido
   no mesmo ciclo** (regra da 067) com hashes renovados.
5. `radar/AGENTE.md` (20 sistemas) e `radar/RADAR.md` (QM e Kimi Code → promovido spec 073).
6. Corpus do companion regenerado (`build_corpus.py`).
7. HISTORICO: edição 0.67 (nota A3). Merge `--no-ff`, push, CI verde.

## Regras

- Princípio I: nenhuma afirmação sem evidência (caminho de arquivo); medições feitas, não
  presumidas; incerteza marcada.
- Sem identificador de modelo em commits/artefatos.
- QM: dimensão 14 (proatividade) obrigatória — categoria vizinha de agentes pessoais
  (triggers/crons nativos declarados).

## Aceite

- [ ] Duas avaliações completas no formato do template, com paths reais do commit congelado.
- [ ] notas.json validado (sum(dimensões) == total em ambas).
- [ ] Build 4 passos verde (PT+EN, verificadores, selos de sincronia).
- [ ] CI verde na main após o merge.
