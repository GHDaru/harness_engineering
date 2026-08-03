# Feature Specification: Rodada ext-3 (Traycer) + Apêndice da cadeia de suprimentos

**Feature Branch**: `074-ext3-traycer-supply`

**Created**: 2026-08-02

**Status**: Aprovada pelo editor ("1. [fork] … vale uma abertura de um apendice mostrando o supply chain das aplicacoes")

**Input**: Indicação do editor (repo com contexto comercial) + tese da rodada ext-2 (corpus como cadeia de suprimentos).

## Objetivo

1. **Avaliar o Traycer** (Traycer AI) com o instrumento HARNESS_EVAL — rodada **ext-3** — com
   veredito explícito do **teste de inclusão** (cap. 01 §4): harness completo no código aberto
   ou casca de orquestração com cérebro SaaS? A avaliação vale nos dois casos (o livro
   documenta recusas com evidência).
2. **Novo apêndice do livro**: "A cadeia de suprimentos dos harnesses" — o mapa de quem
   consome quem dentro do corpus (deps de package.json, forks vendorizados, spawn de CLIs,
   protocolos, leitura de artefatos alheios), com evidência por caminho de arquivo, leitura
   editorial (concorrentes → fornecedores) e o ângulo de segurança (supply chain como
   superfície de risco herdada).

## Commit congelado

| Sistema | Upstream | Fork | Commit | Licença |
|---|---|---|---|---|
| Traycer | traycerai/traycer | GHDaru/traycer | `65fc3d7` | MIT |

## Entregas

1. `benchmark/avaliacoes/traycer.md` (rodada ext-3, com veredito de inclusão).
2. `livro/apendice-supply-chain.md` + espelho EN + entradas nos dois sumários.
3. Se o Traycer passar: notas.json/comparativo/00/01/apendice-estudo (corpus → 21) + radar.
   Se não passar: registro da recusa com evidência no apêndice do estudo + radar (descartado).
4. Delta EN completo com selos; corpus do companion regenerado; HISTORICO 0.68; CI verde.

## Aceite

- [ ] Avaliação com veredito explícito e evidência por path.
- [ ] Apêndice novo renderizado em PT e EN, navegável pelos sumários, links internos OK.
- [ ] Build 4 passos verde; CI verde na main.
