# 00 — Introdução: por que sua intuição não escala

> **Estado da arte capturado em 2026-07** · última revisão 2026-07-30 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

1. **Reconhecer** quando uma decisão é um problema multicritério — e por que "pesar de
   cabeça" produz respostas diferentes a cada dia.
2. **Explicar** a diferença entre decidir (escolher) e apoiar a decisão (estruturar,
   comparar, expor trade-offs) — a distinção *decision making* vs *decision aiding* de
   Bernard Roy.
3. **Descrever** o que este livro constrói: um método de estudo (ler → calcular à mão →
   implementar) e uma aplicação real (o **Decisor**) que nasce capítulo a capítulo.

## O problema

Você precisa escolher um apartamento. Quatro candidatos sobreviveram às visitas:

| Alternativa | Preço (R$) ↓ | Área (m²) ↑ | Deslocamento (min) ↓ | Bairro (1–5) ↑ |
|---|---|---|---|---|
| A1 — Centro | 450.000 | 62 | 15 | 4 |
| A2 — Jardim | 380.000 | 70 | 35 | 3 |
| A3 — Parque | 520.000 | 85 | 25 | 5 |
| A4 — Estação | 340.000 | 55 | 20 | 2 |

Nenhum vence em tudo. O mais barato (A4) tem o pior bairro; o melhor apartamento (A3) é
o mais caro; o mais perto do trabalho (A1) não é nem o maior nem o mais barato. Toda
escolha aqui é um **trade-off**: ganhar em um critério custa perder em outro.

O que a maioria de nós faz? "Pesa de cabeça". E a psicologia da decisão documenta há
décadas o que acontece: ancoramos no último número que vimos, damos peso desproporcional
ao critério mais fácil de comparar, mudamos de opinião conforme a ordem em que as opções
são apresentadas. A intuição funciona para escolher o almoço; ela não escala para
decisões com muitos critérios em conflito, muitas alternativas, ou muitas pessoas
opinando.

**Decisão multicritério** (MCDA — *Multi-Criteria Decision Analysis*) é o campo da
pesquisa operacional que estuda como estruturar e apoiar essas decisões com métodos
quantitativos: explicitar critérios, medir alternativas, revelar pesos e agregar tudo em
uma recomendação — *auditável e reproduzível*. Não para decidir por você, mas para que
você entenda **por que** prefere o que prefere, e possa defender a escolha.

## Fundamentos

Duas ideias fundadoras atravessam o livro inteiro:

- **Apoio à decisão, não decisão automática.** Roy (1996) chama o campo de *aide à la
  décision*: o analista constrói um modelo **com** o decisor, e o modelo devolve clareza
  — não uma sentença. Nenhum método deste livro "dá a resposta certa"; cada um torna
  visível um jeito diferente de pensar o trade-off.
- **Preferências são construídas, não descobertas.** Keeney & Raiffa (1976) mostram que
  pesos e funções de valor não existem prontos na cabeça do decisor; são *elicitados* por
  procedimentos explícitos. Métodos diferem exatamente em **como** elicitam e **como**
  agregam — e é por isso que podem discordar entre si (cap. 11).

(Bibliografia completa e status de validação: [`livro/bibliografia.md`](../bibliografia.md).)

## Quando usar (e quando não)

MCDA vale o custo quando a decisão tem critérios em conflito **e** consequências que
justificam método: escolher fornecedor, priorizar projetos, localizar uma planta,
selecionar tecnologia, alocar orçamento público. Não vale para decisões triviais,
reversíveis e de baixo impacto — o custo de modelar supera o ganho.

### Leitura executiva

Este é um livro para aprender **fazendo três vezes**: cada método é (1) lido com sua
fonte seminal, (2) calculado à mão sobre o mesmo caso âncora — a tabela de apartamentos
acima — e (3) implementado em Python numa etapa executável do `decisor-zero/`, cujos
testes reproduzem o exemplo do capítulo. Ao final da trilha, as etapas convergem no
**Decisor**: uma aplicação web (FastAPI + Postgres/Neon) em que qualquer pessoa monta
sua decisão e compara o veredito de vários métodos lado a lado. **O que levar** hoje:
método multicritério não substitui julgamento — ele o torna explícito, auditável e
discutível.

## Mão na massa — decisor-zero, etapa 00

Abra [`decisor-zero/etapas/00-esqueleto/`](../../decisor-zero/etapas/00-esqueleto/):
uma API FastAPI mínima com uma página web que apresenta o caso âncora. Ainda não há
nenhum método — só o chassi sobre o qual as próximas 13 etapas vão crescer. Rode
`uvicorn app:app --reload`, abra `http://localhost:8000` e confira que a tabela que você
viu neste capítulo é a mesma que a API serve em `/api/caso-ancora`.

## Verificação

1. Na tabela de apartamentos, existe alguma alternativa que seja melhor que outra em
   *todos* os critérios? O que isso implicaria se existisse? (Dica: se A1 fosse melhor
   que A2 em tudo, A2 poderia ser descartada sem nenhum método — cap. 02.)
2. Qual a diferença entre um método que *decide por você* e um método que *apoia sua
   decisão*? (Dica: objetivo 2.)
3. Por que dois métodos legítimos podem recomendar apartamentos diferentes para a mesma
   tabela? (Dica: elicitação e agregação — objetivo 3 e cap. 11.)

---

## Apêndice A — o ecossistema de ferramentas MCDA

Panorama do que existe pronto (e que este livro usa como referência de validação):

- **pymcdm** (<https://github.com/kotbaton/pymcdm>) — biblioteca Python MIT com dezenas
  de métodos, normalizações e técnicas de pesos; usaremos para validação cruzada dos
  nossos resultados a partir do cap. 04.
- **pyDecision** (<https://github.com/Valdecy/pyDecision>) — ~70 métodos com notebooks
  de exemplo por método.
- **scikit-criteria** (<https://scikit-criteria.quatrope.org/>) — API estilo
  scikit-learn (`DecisionMatrix`, pipelines); referência de arquitetura para o `app/`.
- **International Society on MCDM** (<https://www.mcdmsociety.org/>) — sociedade
  científica do campo, com banco de software e material histórico.
