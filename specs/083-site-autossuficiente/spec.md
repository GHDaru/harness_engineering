# Feature Specification: Site autossuficiente — o conteúdo não depende mais do repositório

**Feature Branch**: `083-site-autossuficiente`

**Created**: 2026-08-06

**Status**: Aprovada pelo editor ("O repositório do livro vai ficar privado, e todo acesso é via site, logo corrija")

## Problema

A verificação da rodada ext-4 encontrou um link quebrado (`benchmark/avaliacoes/*.html` → 404 no
site). A investigação mostrou que o defeito era muito maior que o sintoma, e que a decisão de
**tornar o repositório privado** o transformava de incômodo em bloqueio:

- **74 links** do site apontavam para o repositório — 41 em `benchmark/`, 12 em `radar/`, 9 em
  `adr/`, e 7 para código/estudos.
- Em **PT** eles eram reescritos para URLs do GitHub (funcionavam enquanto o repo fosse público).
- Em **EN** apontavam para `../../benchmark/avaliacoes/*.html`, páginas que **nunca existiram** —
  e o portão de links não pegava, porque ele ignora hrefs com `../` (que cruzam idioma por design).

Com o repositório privado, **as 21 avaliações do benchmark — o ativo central do estudo — ficariam
inacessíveis a qualquer leitor**.

## Correção

O motor passa a publicar como páginas do site tudo o que é **conteúdo** e vivia só no repositório:

| Grupo | Páginas | Slug |
|---|---:|---|
| Avaliações do benchmark | 21 | `avaliacao-<nome>.html` |
| Metodologia + templates do benchmark | 3 | `benchmark-metodologia.html`, `benchmark-template-*.html` |
| Radar: mesa e contrato do agente | 2 | `radar-mesa.html`, `radar-contrato.html` |
| ADRs | 9 | `adr-<nnnn>-<nome>.html` |
| Estudos de apoio | 6 | `estudo-<data>-<nome>.html` |
| | **41** | |

Detalhes que a implementação exigiu:

- **Prefixo de grupo no slug**, para não colidir com o que o sumário já publica — `radar/RADAR.md`
  viraria `radar`, que é o jornal; `benchmark/README.md` viraria `readme`.
- O **mapa de páginas extras é construído nas duas passadas** de idioma. Na primeira tentativa ele
  só existia no PT, e os links EN continuavam indo ao GitHub — as páginas são geradas só no PT
  (registros operacionais, decisão da 067), mas o EN precisa **linká-las** com `../`.
- `jornal.mjs` tinha os links do Radar **em código** (`${GH}radar/RADAR.md`) — trocados pelas páginas.
- O portão de links internos passa a validar as páginas novas, como origem e como destino.

Resultado: **74 → 7 links** para o repositório.

## O que ficou de fora (decisão do editor)

Os 7 restantes apontam para **código e infraestrutura**, não conteúdo: `scripts/sync-forks.ps1`,
`publicar/DESIGN-SISTEMA.md`, `harness-um/README.md`, `chat-companion/backend/EMAIL.md`,
`docs/config.md`. Com o repositório privado, viram becos sem saída para o leitor. Três caminhos
possíveis, todos fora do escopo desta spec: publicá-los também, manter um espelho público só do
código, ou reescrever as menções para não prometerem um link.

## Aceite

- [x] 41 páginas geradas; build 4 passos verde nas duas línguas
- [x] Caminho do leitor verificado em navegador: apêndice do estudo → avaliação do Prime Agent
- [x] Link EN → página PT resolve (200), com o `../` correto
- [x] Portão de links valida as páginas novas
- [ ] CI verde na main
