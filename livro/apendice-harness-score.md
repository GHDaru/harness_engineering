# Apêndice — Meça o seu harness

> **Estado da arte capturado em 2026-08** · última revisão 2026-08-10 · [histórico e registro de expiração](HISTORICO.md)

Este livro faz duas coisas com harnesses: **lê** os dos outros (o [Comparativo](../benchmark/comparativo.md), 20 sistemas em 12 dimensões) e **constrói** um do zero (o harness-zero). Falta a terceira, que é a que interessa a quem trabalha: **medir o seu**.

Não o harness que você escreveu — o que você *tem*. Porque quando um agente entra no seu repositório, o harness efetivo não é só o Claude Code ou o Codex que você abriu: é aquilo **mais** o que o seu repositório oferece a ele. As instruções que orientam, os testes que dão sinal, os guarda-corpos que impedem estrago. Dois repositórios com o mesmo modelo e o mesmo CLI produzem resultados diferentes, e a diferença mora aqui.

## O instrumento

O [Harness Score](https://github.com/paladini/harness-score) (Fernando Paladini, **MIT**) varre o repositório e devolve um **nível de maturidade L0–L4** e **108 pontos em 6 dimensões, 36 checagens**. Uma linha:

```bash
npx harness-score
```

O compromisso de projeto é o que o torna citável aqui: *"zero LLM calls, zero network access, and the same result every time you run it"* — cada resultado é *"a filesystem fact — a file exists, parses, matches a pattern"*.

Isso não é detalhe de implementação. É a tese do [cap. 11](capitulos/11-verificacao-evals.md) aplicada ao próprio ato de medir: o capítulo argumenta que verificação que vale é **externa e ancorada**, não auto-relato do modelo. Um medidor de harness que se recusa a usar modelo para medir harness é esse argumento virado ferramenta — e é por isso que o número dele é discutível mas **reprodutível**, que é a única propriedade que uma medida precisa ter para servir de base a uma discussão.

As seis dimensões dele mapeiam quase limpo nos capítulos daqui — o que é, por si só, evidência de que nossas doze dimensões não são arbitrárias:

| Dimensão (pontos) | O que procura | Capítulo |
|---|---|---|
| Context & Guides (20) | `AGENTS.md`, regras com escopo, sem inchaço | [03](capitulos/03-entrega-de-contexto.md) |
| Skills & Commands (17) | skills declaradas, comandos explícitos | [05](capitulos/05-ferramentas.md), [12](capitulos/12-extensibilidade.md) |
| Hooks & Guardrails (14) | hooks de portão e de realimentação | [07](capitulos/07-permissoes-sandbox.md) |
| Sensors & Feedback (20) | testes, linter, tipos, formatador | [11](capitulos/11-verificacao-evals.md) |
| CI Feedback (14) | pipeline, testes e lint no CI, pré-commit | [11](capitulos/11-verificacao-evals.md) |
| Hygiene & Safety (23) | `.gitignore`, ausência de credencial, licença, lockfile | [07](capitulos/07-permissoes-sandbox.md) |

E a definição que o projeto dá de harness é a **quinta** convergência independente com a do [cap. 01](../01-fundamentos.md) que este livro registra — a mais operacional de todas, porque define pelo que se pode verificar no sistema de arquivos: *"A model answers; an agent acts. An agent harness is the runtime that turns one into the other — the model thinks; the harness decides what that thinking is allowed to touch."*

## A escada

| Nível | Nome | O que caracteriza |
|---|---|---|
| **L0** | Unharnessed | partida a frio a cada sessão |
| **L1** | Documented | existe um `AGENTS.md` que orienta o agente |
| **L2** | Guided | regras com escopo e higiene básica |
| **L3** | Sensing | testes, tipos e CI verificam o trabalho |
| **L4** | Self-correcting | hooks fecham o laço |

Os níveis dependem da **forma** do harness, não do total: oitenta pontos de documentação com zero teste dão L1, não L3. É a mesma disciplina da rubrica deste livro — não se compensa ausência de verificação com abundância de prosa.

## O nosso placar, antes e depois

Um livro sobre engenharia de harness que não se mede é um livro que pede confiança. Medimos, e o primeiro resultado foi ruim.

**Antes** — 2026-08-10, `harness-score` via `npx`, no repositório deste livro:

```
Engenharia de Harness · L2 · Guided · 59/108 (55%)
Detectados: claude-code, codex

Context & Guides   ████████████████████ 20/20
Hygiene & Safety   █████████████████░░░ 20/23
Skills & Commands  ██████████░░░░░░░░░░  9/17
CI Feedback        ████████░░░░░░░░░░░░  8/14
Hooks & Guardrails ░░░░░░░░░░░░░░░░░░░░  0/14
Sensors & Feedback ██░░░░░░░░░░░░░░░░░░  2/20
```

**O diagnóstico é o mais interessante do apêndice.** Este repositório tinha, naquele momento, 81 testes automatizados, um build de quatro passos com verificação de links e uma etapa inteira dedicada a evals no harness-zero. A checagem `SNS-05 Test files actually exist` **passou**. A `SNS-01 Test runner configured` **falhou** — junto com linter, tipos e formatador, −18 pontos. O scanner via os arquivos de teste e não achava **ponto de entrada na raiz**: eles viviam em três subdiretórios, e saber disso exigia ler o `CLAUDE.md`.

Ou seja: nós compensávamos em **prosa** o que faltava em **configuração**. E é exatamente por isso que Context deu 20/20 — as instruções eram ótimas.

> **A lição, e ela custou 55%:** prosa perfeita não substitui guarda-corpo executável. O agente lê e obedece. Um hook, um CI ou o próximo colaborador **não leem prosa**.

O zero em Hooks & Guardrails dizia o mesmo pelo outro lado, e doía mais: num repositório que dedica um capítulo inteiro a permissões e sandbox, **nenhuma** das nossas regras críticas era imposta por máquina. "Sem segredo em commit" e "nenhum identificador interno de modelo em artefato" são regras constitucionais deste projeto — e eram cumpridas por atenção humana, o que significa cumpridas até a primeira distração.

**Depois** — mesma ferramenta, mesmo dia, depois da correção descrita abaixo:

```
Engenharia de Harness · L4 · Self-correcting · 87/108 (81%)

Context & Guides   ████████████████████ 20/20   (=)
Sensors & Feedback ████████████████░░░░ 16/20   ↑ de 2
Hooks & Guardrails ████████████████████ 14/14   ↑ de 0
CI Feedback        ████████████████░░░░ 11/14   ↑ de 8
Skills & Commands  ██████████░░░░░░░░░░  9/17   (=)
Hygiene & Safety   ███████████████░░░░░ 17/23   ↓ de 20
```

## O que fizemos — e a regra que seguimos ao fazer

A regra veio antes do trabalho: **cada item precisa se justificar sem olhar o placar**. Otimizar para a nota é gamear o verificador — o *reward hacking* que o cap. 11 descreve em detalhe, cometido pelos autores do capítulo. Se a única razão para adicionar algo fosse o ponto, não entrava.

**Um ponto de entrada.** Um `Makefile` e um `pyproject.toml` na raiz. `make test` roda as três suítes; `make build` faz o site; `make score` mede o harness. Justificativa sem placar: quem chega na raiz não tinha como rodar nada sem antes ler um arquivo de instruções — e um agente que não lê instruções antes de agir é o caso comum, não o excepcional.

**Um padrão de estilo.** Ruff, um só para os dois projetos Python. Justificativa sem placar: o estilo vivia na cabeça de quem revisava.

**Quatro guarda-corpos**, e são eles que sustentam a mudança. Três deles convertem em regra imposta o que era regra escrita:

| Hook | O que impõe | Onde a regra vivia antes |
|---|---|---|
| `guarda-segredo` | escrita com assinatura de credencial é bloqueada | constituição, Princípio IV |
| `guarda-identidade` | identificador interno de modelo não entra em arquivo | constituição, Princípio VI |
| `guarda-git` | `push --force`, `reset --hard`, `clean -fdx` pedem confirmação | em lugar nenhum — era hábito |
| `formata-python` | arquivo `.py` editado passa pelo formatador | nenhum |

Dois detalhes de projeto que valem mais que os hooks em si. O primeiro: **nenhum deles bloqueia quando ele próprio falha** — entrada ilegível, exceção interna, ferramenta ausente, todos saem em silêncio deixando o trabalho seguir. Um guarda-corpo que interrompe o trabalho ao quebrar a si mesmo é desligado na semana seguinte, e aí protege zero. O segundo: `guarda-git` **pergunta** em vez de proibir. Existem motivos legítimos para todas aquelas operações; o objetivo é que sejam deliberadas, não impossíveis. É o raio de alcance do cap. 07 aplicado ao próprio repositório.

E os hooks têm **37 testes**, com os casos que devem *passar* tão explícitos quanto os que devem bloquear — porque um guarda-corpo que atrapalha trabalho legítimo é contornado, e um hook sem teste é uma promessa com sintaxe.

## O que **não** fizemos, e por quê

Esta seção é a que dá valor às duas anteriores. Sem ela, "subimos de L2 para L4" é propaganda.

- **Tipagem estática estrita** (`SNS-03`, 4 pontos). Recusada. Adicionar tipagem estrita a uma base que não foi escrita para ela é uma mudança de porte próprio, com custo real de revisão. Fazê-la agora, no meio de uma spec sobre medição, seria adicioná-la **pelo ponto** — exatamente o que a regra proíbe.
- **Pré-commit** (`CI-04`, 3 pontos). Recusado por ora: os hooks já dão realimentação no momento da edição, e uma segunda camada de mesma função tem custo de manutenção sem sinal novo.
- **Subagentes declarados** (`AGT-01/02`, 5 pontos). Não temos subagentes definidos neste repositório. Declará-los para pontuar seria inventar arquitetura para agradar o instrumento.
- **Configuração de MCP** (`HYG-08`, 3 pontos). Não usamos MCP aqui. Mesma lógica.
- **O badge no README.** O cap. 01 §6 já proíbe agregação numérica espúria (DESMET); 87/108 não é uma medida de qualidade do livro, é um diagnóstico de configuração do repositório. Publicá-lo como selo trairia a régua que aplicamos aos outros.

## A regressão que deixamos acontecer

Higiene **caiu**, de 20/23 para 17/23, e o motivo é o achado mais interessante desta medição inteira.

A checagem `HYG-07` cobra um *lockfile* ao lado do manifesto de dependências. Antes, ela **passava**, e a mensagem do próprio scanner explica por quê: *"No dependency manifest detected (nothing to lock."* Não havia manifesto na raiz, logo não havia o que travar, logo ponto ganho. Depois de acrescentarmos um `pyproject.toml` — que contém **apenas configuração**, nenhuma dependência —, a mensagem virou *"Manifest present but no lockfile"*, e o ponto foi embora.

Poderíamos ter forjado um `requirements.txt` vazio na raiz e recuperado os três pontos. Não fizemos: seria mentir para o instrumento sobre a natureza do arquivo. Ficam duas conclusões, e as duas valem para qualquer escada de maturidade que você venha a usar:

1. **Um ponto ganho por ausência não é um ponto.** Parte do nosso 20/23 inicial em higiene era aprovação vazia — não tínhamos o problema porque não tínhamos a coisa. Toda rubrica que pontua "não se aplica" como acerto infla quem faz menos.
2. **O placar não é monótono sob melhoria honesta.** Tornar o repositório mais legível fez uma checagem passar a falhar. Se a sua meta for o número, você aprende a **não** adicionar o manifesto — e é assim que uma métrica bem-intencionada começa a governar a arquitetura em vez de descrevê-la.

É a lição do cap. 11 sobre sensibilidade do instrumento, encontrada no nosso próprio quintal.

## Ressalvas de uso

- **Viés de raiz.** O scanner subestima monorepo poliglota — o nosso caso, com Python em dois lugares e Node num terceiro. A ressalva tem limite, porém: para um agente que aterrissa na raiz, o que não é descobrível ali **de fato** não existe. Metade do nosso 2/20 inicial era limitação do instrumento; a outra metade era defeito nosso.
- **Discrepância de versão** ⏳: o site anuncia npm v1.2.0; o repositório mostra release v1.0.0. Nossa medição usou a versão publicada no npm em 2026-08-10.
- **O número não é a coisa.** O valor está no **gap nomeado** — `SNS-01`, `HKS-03`, cada um com um remédio específico — e não no total. Trate 87/108 como se trata a nota 31/36 de um harness no Comparativo: um resumo que só significa alguma coisa junto com a evidência que o produziu.

## Como usar isto no seu repositório

1. Rode `npx harness-score` e leia o **primeiro gap**, não o total.
2. Para cada item que pretende corrigir, escreva a justificativa **sem citar o placar**. Se não conseguir, não corrija — você estaria otimizando o instrumento.
3. Comece pelos guarda-corpos, não pela documentação. Documentação é o que a maioria dos repositórios já tem em excesso; o que falta quase sempre é o que roda sozinho.
4. Guarde o placar de partida com data. O valor de uma medida de maturidade está na **série**, não no ponto.
