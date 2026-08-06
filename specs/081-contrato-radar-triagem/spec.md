# Feature Specification: O contrato do Radar aprende com três dias de campo

**Feature Branch**: `081-contrato-radar-triagem`

**Created**: 2026-08-06

**Status**: Aprovada pelo editor ("Pode mudar")

## Origem

Sugestões registradas pelo próprio agente do Radar em duas execuções seguidas — ele detectou os
padrões mas **não podia mudar o contrato** (regra dura: escrita só em `radar/`, e `AGENTE.md` é
o processo). O editor aprovou.

## Os dois padrões observados em campo

1. **Agregador com data errada — três execuções seguidas.** 04/ago: o episódio Anthropic×terceiros
   (opencode) foi apresentado como notícia de agosto, sendo de **janeiro–março**. 05/ago: o GA do
   Microsoft Agent Framework (abr) confundido com o GA do Harness (jul). 06/ago: press release
   pago vendendo um repositório como framework de produção. Em todos, o **fato existia** — o que
   estava errado era a **datação** ou o **enquadramento** da fonte secundária.
2. **Métrica de repositório como isca.** O `ultraworkers/claw-code` aparecia com 194.982 estrelas
   — mais que o opencode, o maior do corpus — e teria entrado como candidato prioritário. A API
   do GitHub mostrou **109.281 forks para essas estrelas** (razão 1,8:1, quando projetos reais
   ficam em 10:1 ou mais) e a descrição do próprio repositório dizendo *"agent-managed museum
   exhibit… developed and maintained with no human intervention"*.

## Mudanças no contrato (`radar/AGENTE.md`)

Três regras duras novas, todas com custo baixo de execução:

- **Agregador é pista, nunca fonte** — ranking, newsletter, rastreador de release, blog de resumo
  e wire de press release servem para *encontrar*; afirmar exige primária (repositório, blog
  oficial, spec, paper, press release da própria organização). Sem primária: ⏳ dizendo qual
  fonte falta.
- **A data merece verificação separada do fato** — confirmar *quando* aconteceu, não só *o quê*.
- **Candidato ao corpus passa pela API do repositório** antes de qualquer recomendação: licença,
  linguagem, criação, último push e **estrelas × forks**; razão abaixo de ~5:1 exige ⏳ e
  desconfiança explícita; e ler a descrição que o repositório dá de si mesmo.

Mais um ponteiro no passo 2 (Busca): "a busca encontra; quem afirma é a fonte primária".

## Fora de escopo

- Automatizar a triagem (um script que consulte a API e calcule a razão). O contrato descreve o
  procedimento; a ferramenta pode vir depois se a checagem manual incomodar.

## Aceite

- [x] `AGENTE.md` com as três regras e o ponteiro no passo de busca
- [x] O caso concreto citado no contrato (é o que faz a regra ser lembrada)
- [ ] CI verde na main
