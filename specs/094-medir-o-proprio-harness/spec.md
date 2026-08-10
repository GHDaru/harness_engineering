# Feature Specification: medir o próprio harness

**Feature Branch**: `094-medir-o-proprio-harness`

**Created**: 2026-08-10

**Status**: **Aprovada pelo editor** — *"Sim e já inclua a correção"*

## A origem

O editor trouxe o [Harness Score](https://paladini.io/harness-score/) e perguntou como poderia entrar
no livro. A avaliação encontrou mais do que uma ferramenta a citar: encontrou **o eixo que falta**
— e, ao rodá-la no nosso repositório, um defeito real.

## O que a ferramenta é (verificado na primária)

[`paladini/harness-score`](https://github.com/paladini/harness-score) — **MIT**, TypeScript,
**164★/12 forks** (13,7:1 ✓), não arquivado, 75 commits. CLI que varre o sistema de arquivos e
devolve **nível L0–L4** e **108 pontos em 6 dimensões, 36 checagens**. O compromisso de projeto:
*"zero LLM calls, zero network access, and the same result every time you run it"* — o resultado é
*"a filesystem fact — a file exists, parses, matches a pattern"*.

**Unidade de análise diferente da nossa.** O benchmark do livro mede **o harness** (12 dimensões,
20 sistemas). O Harness Score mede **o repositório do leitor** — quão preparado ele está para ser
trabalhado por um agente. O livro ensina a ler harnesses e a construir um; nunca deu ao leitor um
instrumento para medir **o próprio lado da equação**.

O mapeamento das dimensões dele contra os nossos capítulos é quase limpo, o que é evidência de que
as nossas não são arbitrárias:

| Harness Score | Pontos | Capítulo |
|---|---|---|
| Context & Guides | 20 | 03 |
| Skills & Commands | 17 | 05, 12 |
| Hooks & Guardrails | 14 | 07 |
| Sensors & Feedback | 20 | 11 |
| CI Feedback | 14 | 11 |
| Hygiene & Safety | 23 | 07 |

E o **determinismo é a tese do cap. 11 encarnada**: o capítulo defende verificador externo e
imutável contra auto-avaliação do modelo; aqui está um medidor de harness que se recusa a usar
modelo para medir harness.

## O que a medição encontrou aqui

Execução em `/workspace/harness_engineering` em 2026-08-10, `harness-score` via `npx`:

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

**O diagnóstico, e ele é honesto.** Temos 81 testes (62 no backend, 19 no harness-um), build de 4
passos com link-check e uma etapa inteira de evals no harness-zero. A checagem `SNS-05 Test files
actually exist` **passou**; `SNS-01 Test runner configured` **falhou**, junto com linter, tipos e
formatador — **−18 pontos**. O scanner vê os arquivos de teste e **não acha ponto de entrada na
raiz**: eles vivem em `chat-companion/backend/tests`, `harness-um/tests` e `publicar/`.

Nós compensamos em **prosa** o que falta em **configuração**: o `CLAUDE.md` e o checklist dizem ao
agente onde rodar cada coisa — e é exatamente por isso que Context deu 20/20.

> **A lição, que é a tese desta spec: prosa perfeita não substitui guarda-corpo executável.**
> O agente lê e obedece. Um hook, um CI ou o próximo colaborador não leem prosa.

E o zero em **Hooks & Guardrails** diz o mesmo pelo outro lado, num repositório que dedica um
capítulo inteiro a permissões: **regras críticas nossas existem só como texto**. O contrato do Radar
manda "escrita somente em `radar/`"; a constituição proíbe segredo em commit e identificador interno
de modelo em artefato. Nada disso é imposto por máquina. São promessas.

## Requisitos

### R1 — O livro ganha o instrumento
- **Cap. 11**: seção nova em "O estado da arte" sobre medir o harness do próprio projeto, com o
  determinismo (sem LLM, sem rede) tratado como decisão de design que o capítulo já defende.
  Leitura executiva atualizada.
- **Cap. 01 §4**: nota da **quinta** definição independente convergente — e a mais operacional
  (harness como o que se pode medir no sistema de arquivos).
- **Apêndice novo `apendice-harness-score.md`** — *"Meça o seu harness"*: o que a ferramenta é,
  o mapa dimensões↔capítulos, como rodar, **o nosso placar antes e depois**, e as ressalvas.
- **Bibliografia**: entrada verificada.

### R2 — A caixa de honestidade
O apêndice publica o **antes (L2 · 59/108)** e o **depois**, com o diagnóstico e a lista do que
deliberadamente **não** foi feito. Um livro que mede a si mesmo e mostra onde perde vale mais que
uma seção teórica.

### R3 — A correção do repositório, com uma regra de honestidade
Fechar o gap **real** — tornar os sensores descobríveis na raiz e converter em guarda-corpo o que
hoje é promessa. **Não caçar pontos.**

> A distinção não é estética. Otimizar para a nota é **gamear o verificador** — o *reward hacking*
> que o cap. 11 descreve, cometido pelos autores do capítulo. Cada item adicionado precisa se
> justificar **sem** o placar: se a única razão for o ponto, não entra, e o apêndice registra a
> recusa.

Itens que se justificam sozinhos:

1. **Ponto de entrada de testes na raiz** — hoje é preciso ler o `CLAUDE.md` para saber que há três
   suítes em três lugares. Um agente que aterrissa na raiz não roda teste nenhum.
2. **Linter e formatador** — dois projetos Python (`chat-companion/backend`, `harness-um`) sem
   padrão declarado; o estilo hoje vive na cabeça de quem revisa.
3. **Hooks de guarda-corpo** — os três que convertem regra escrita em regra imposta:
   - **segredo**: bloquear escrita cujo conteúdo tenha assinatura de credencial;
   - **identificador interno de modelo**: bloquear que entre em qualquer arquivo do repositório;
   - **git destrutivo**: exigir confirmação para `push --force`, `reset --hard` e `clean -fdx`.
4. **Lint no CI** — sensor barato à esquerda, no mesmo workflow que já roda os testes.

### R4 — Nada quebra
O build de 4 passos, os 81 testes e o CI continuam verdes. O lint entra **sem** falhar a
publicação por estilo preexistente: primeiro se declara o padrão, depois se conforma.

## Não faz parte

- Adotar o badge no README como métrica de qualidade — os 108 pontos não são medida exata, e o
  cap. 01 §6 já proíbe agregação numérica espúria (DESMET).
- Tipagem estática estrita no backend: é mudança de porte próprio, e adicioná-la agora seria
  exatamente a caça a pontos que R3 proíbe. Fica registrada como recusa deliberada.
- Adicionar o Harness Score ao corpus do benchmark — não é um harness, é um medidor de harness.

## Ressalvas a publicar junto

- **Viés de raiz**: o scanner subestima monorepo poliglota. Não é defeito fatal — para um agente
  que aterrissa na raiz, o que não é descobrível ali de fato não existe —, mas o limite vai escrito.
- **Discrepância de versão**: o site anuncia npm v1.2.0; o repositório mostra release v1.0.0. ⏳
- O placar publicado leva **data e versão da ferramenta**, como qualquer medida do livro.

## Aceite

- [ ] Cap. 11 com a seção nova e a Leitura executiva atualizada, PT e EN
- [ ] Cap. 01 §4 com a quinta definição convergente, PT e EN
- [ ] Apêndice "Meça o seu harness" nos dois idiomas, no sumário e navegável
- [ ] Bibliografia com a entrada verificada
- [ ] Placar **antes e depois** publicado, com data, versão e o que não foi feito
- [ ] Repositório em **L3 ou superior**, e cada item da correção justificado sem o placar
- [ ] 81 testes verdes, build de 4 passos verde, CI verde
- [ ] Selos i18n regravados com o hash real; corpus regenerado
