# 01 — O problema multicritério

> **Estado da arte capturado em 2026-07** · última revisão 2026-07-30 · [histórico](../HISTORICO.md)

## Objetivos de aprendizagem

1. **Definir** os quatro componentes de um problema multicritério — alternativas,
   critérios, desempenhos e pesos — e montar a matriz de decisão de um problema real.
2. **Explicar** a notação usada no livro inteiro: $m$ alternativas, $n$ critérios,
   matriz $X = [x_{ij}]$, direção de cada critério (benefício/custo).
3. **Classificar** um problema segundo a *problemática* de Roy: escolha (α), ordenação
   (γ), classificação (β) — e segundo a natureza das alternativas (discretas × contínuas).
4. **Demonstrar** por que somar desempenhos crus é um erro — o problema das escalas
   incomensuráveis que motiva todo o resto do livro.

## O problema

No capítulo 00 a tabela de apartamentos era só uma tabela. Para aplicar qualquer método,
ela precisa virar um **objeto matemático bem definido** — e cada palavra da definição
esconde uma decisão de modelagem: o que conta como alternativa? O que é um critério bem
formulado? Em que escala se mede "qualidade do bairro"? Errar aqui condena qualquer
cálculo posterior, por mais sofisticado que seja o método.

## Fundamentos

A formulação clássica do problema de decisão multiatributo é sistematizada por Hwang &
Yoon (1981), e a notação deles é a que o livro adota:

- Um conjunto **finito e discreto** de $m$ alternativas $A = \{a_1, \dots, a_m\}$ —
  os apartamentos. (Quando as alternativas são contínuas — "qualquer mistura de
  investimentos" — o campo vizinho é a otimização multiobjetivo/MODM, fora do nosso
  escopo; ver Greco et al., 2016.)
- Um conjunto de $n$ critérios $C = \{c_1, \dots, c_n\}$, cada um com uma **direção**:
  critério de *benefício* (quanto maior, melhor: área) ou de *custo* (quanto menor,
  melhor: preço, deslocamento).
- A **matriz de decisão** $X \in \mathbb{R}^{m \times n}$, onde $x_{ij}$ é o desempenho
  da alternativa $a_i$ no critério $c_j$.
- Um vetor de **pesos** $w = (w_1, \dots, w_n)$, com $w_j \ge 0$ e $\sum_j w_j = 1$,
  expressando a importância relativa dos critérios. (De onde vêm os pesos é o assunto
  do cap. 03 — por ora, assuma-os dados.)

Roy (1996) acrescenta a pergunta que a formulação americana não faz: **qual é a
problemática?** O mesmo modelo serve a perguntas diferentes — **escolher** a melhor
alternativa (problemática α), **ordenar** todas (γ), ou **classificar** cada uma em
categorias como aprovado/reprovado (β). O Decisor implementará as três ao longo do livro.

Critérios bem formulados, ensina Keeney (via Keeney & Raiffa, 1976), medem **objetivos
fundamentais** ("morar bem") por **atributos mensuráveis** ("minutos até o trabalho") —
e devem ser tão completos quanto não-redundantes: critério duplicado é peso contado duas
vezes (voltamos a isso no cap. 02).

(Bibliografia completa e status de validação: [`livro/bibliografia.md`](../bibliografia.md).)

## O método passo a passo

Modelar o caso âncora é preencher quatro definições:

**Passo 1 — alternativas.** $m = 4$: $a_1$ Centro, $a_2$ Jardim, $a_3$ Parque,
$a_4$ Estação.

**Passo 2 — critérios e direções.** $n = 4$:

| $j$ | Critério | Unidade | Direção |
|---|---|---|---|
| 1 | Preço | R$ | custo ↓ |
| 2 | Área | m² | benefício ↑ |
| 3 | Deslocamento | min | custo ↓ |
| 4 | Bairro | escala 1–5 | benefício ↑ |

**Passo 3 — matriz de decisão.**

$$X = \begin{bmatrix} 450000 & 62 & 15 & 4 \\ 380000 & 70 & 35 & 3 \\ 520000 & 85 & 25 & 5 \\ 340000 & 55 & 20 & 2 \end{bmatrix}$$

**Passo 4 — a tentação ingênua (e por que ela falha).** Com a matriz na mão, o impulso
é "somar os pontos" de cada linha:

| Alternativa | Soma crua $\sum_j x_{ij}$ |
|---|---|
| A1 — Centro | 450.081 |
| A2 — Jardim | 380.108 |
| A3 — Parque | 520.115 |
| A4 — Estação | 340.077 |

A soma "elege" A3 — mas olhe os números: a soma crua é o **preço com ruído**. Os outros
três critérios, medidos em dezenas, desaparecem diante de um critério medido em centenas
de milhares; e pior, preço é critério de *custo* — a soma premia o apartamento mais
caro. Duas lições que motivam os caps. 03–04: (1) desempenhos em unidades diferentes são
**incomensuráveis** — exigem normalização antes de qualquer agregação; (2) a direção de
cada critério é parte do modelo, não um detalhe. *Este exemplo é reproduzido pelo teste
`test_soma_crua_e_o_preco_com_ruido` da etapa 01 — o absurdo está garantido por CI.*

## Quando usar (e quando não)

A matriz de decisão pressupõe que os desempenhos $x_{ij}$ são conhecidos e pontuais.
Quando há incerteza forte (desempenhos são distribuições), o instrumental é o de análise
de decisão sob risco (MIT OCW IDS.333 é uma boa porta); quando os critérios interagem
(a "qualidade do bairro" muda o valor da "área"?), as premissas de independência dos
métodos aditivos entram em questão (cap. 07). Modelar também é decidir o que **não**
entra: critério que não discrimina as alternativas (todas empatam) só adiciona ruído.

### Leitura executiva

Todo método MCDA — do SAW ao ELECTRE — consome exatamente o mesmo objeto: matriz $X$,
direções e pesos $w$. Quem domina a modelagem troca de método em uma linha de código;
quem a atropela produz rankings sem sentido com qualquer método. **O que levar** hoje:
antes de perguntar "qual método usar?", pergunte "minha matriz está bem definida — cada
critério com unidade, direção e fonte do dado?".

## Mão na massa — decisor-zero, etapa 01

Em [`decisor-zero/etapas/01-matriz/`](../../decisor-zero/etapas/01-matriz/), a matriz
de decisão deixa de ser prosa e vira o coração do código: um módulo puro
(`motor/matriz.py`) com `MatrizDecisao` validando dimensões, direções e pesos — e a API
passa a aceitar **qualquer** problema do usuário, não só o caso âncora. Os testes
reproduzem os números deste capítulo, incluindo o ranking absurdo da soma crua.
Exercício de completar: o validador ainda aceita peso negativo — escreva o teste que
expõe o bug e a correção (part-task practice; gabarito no docstring do teste).

## Verificação

1. Na matriz do caso âncora, o que significaria acrescentar uma coluna "preço do
   condomínio"? E uma coluna "preço por m²"? Qual das duas viola a não-redundância?
   (Dica: objetivo 1 e Keeney & Raiffa.)
2. "Ordenar os 4 apartamentos do melhor ao pior" e "dizer quais apartamentos são
   compráveis" são a mesma problemática? (Dica: objetivo 3 — γ vs β.)
3. Por que a soma crua elegeu exatamente o apartamento mais caro? O que teria acontecido
   se o preço estivesse em milhões de R$? (Dica: objetivo 4 — escala domina agregação.)

---

## Apêndice A — a matriz de decisão nas bibliotecas reais

- **scikit-criteria** modela exatamente o objeto deste capítulo: `mkdm(matrix,
  objectives, weights)` cria um `DecisionMatrix` com direções `MIN`/`MAX` explícitas —
  a validação que implementamos na etapa 01 espelha a dela
  (<https://scikit-criteria.quatrope.org/>).
- **pymcdm** separa matriz, `types` (±1 por critério) e `weights` como três arrays
  NumPy passados a cada método — mesma anatomia, embalagem diferente
  (<https://github.com/kotbaton/pymcdm>).
- **pyDecision** aceita a matriz como lista de listas e a direção como strings
  `'max'/'min'` por critério (<https://github.com/Valdecy/pyDecision>).

Três embalagens, um objeto: a matriz $X$ + direções + pesos deste capítulo.
