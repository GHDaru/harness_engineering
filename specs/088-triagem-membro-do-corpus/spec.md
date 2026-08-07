# Feature Specification: a triagem por repositório vale para membro do corpus, não só para candidato

**Feature Branch**: `088-triagem-membro-do-corpus`

**Created**: 2026-08-07

**Status**: Aprovada pelo editor — *"Sim, pode fazer."*

## Problema

A regra de triagem por API de repositório entrou no contrato na spec 081, redigida para
**candidatos** ao corpus: antes de recomendar um sistema novo, consultar o repositório e checar
licença, cadência e a razão estrela/fork.

A execução de 07/ago encontrou o buraco: a alegação do dia não era sobre candidato, era sobre
**membro** — o `gemini-cli`, nota 36/36 no benchmark. E não era inflação, era o oposto: um
**obituário**. Notícia de que o CLI teria sido encerrado em 18/jun e substituído por um sucessor
fechado, com a cota gratuita caindo de 1.000 para ~20 requisições/dia.

O repositório desmentiu em dois fetches — Apache 2.0, não arquivado, releases semanais, README
documentando o *free tier* vivo em 1.000 req/dia. Mas o texto do contrato **não obrigava** essa
verificação: falava em "candidato ao corpus".

## Correção

A regra passa a cobrir **qualquer alegação sobre um sistema, candidato ou membro**, e nomeia os
**dois** modos de falha em vez de um:

1. **Inflação** — o sistema é menos do que dizem (caso Claw Code, 06/ago).
2. **Obituário precoce** — o sistema é mais do que dizem, está vivo (caso gemini-cli, 07/ago).

Acrescenta também o que verificar num membro estabelecido, que é diferente do que se verifica num
candidato: se está **arquivado** e o que o **README diz hoje** sobre estado, tiers e quotas.

E fixa a lição de método mais cara das duas execuções: **a alegação que confirma um preconceito do
Radar é a que mais exige verificação, não a que menos.** O obituário do gemini-cli encaixava num
padrão real já registrado (opencode perdendo o login Claude Pro/Max, 04/ago) — foi por encaixar
bem que quase passou.

## Fora de escopo

Nada de conteúdo do livro. Isto é contrato do agente; achados continuam sendo insumo para o ciclo
editorial com curadoria humana (ADR 0008).

## Aceite

- [x] A regra fala em "candidato **ou** membro"
- [x] Os dois modos de falha estão nomeados, cada um com o caso concreto que o originou
- [x] A alternativa à API (página pública do repositório) está prevista, porque o escopo de
      repositórios da sessão nem sempre alcança repo externo
- [x] Nenhum arquivo fora de `radar/` e `specs/` tocado
