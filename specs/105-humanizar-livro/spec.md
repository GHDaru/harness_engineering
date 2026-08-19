# Spec 105 — Passada humanizer no livro e nos apêndices de conteúdo

> Branch: `105-humanizar-livro` · 2026-08-19 · pedido do editor: *"aplicar a skill humanize em todo o livro e todos os apêndices de conteúdo; históricos e notícias mantenha"*

## 1. O que a medição mostrou antes de eu escrever uma linha

A skill `humanizer` cataloga 33 padrões de escrita de IA. Medindo os detectáveis por varredura nos 18
capítulos (≈55 mil palavras, fora de blocos de código):

| Padrão | Ocorrências |
|---|---|
| §27 autoridade retórica (*"a verdade é que", "no fundo"*) | **0** |
| §28 sinalização (*"vamos explorar", "dito isso"*) | **0** |
| §25 conclusão genérica positiva | **0** |
| §20 artefato de conversa (*"espero que ajude"*) | **0** |
| §21 disclaimer de corte de conhecimento | **0** |
| §7 vocabulário-IA (*crucial, robusto, paisagem*) | 2 (**1 falso positivo**) |
| §4 promocional (*poderoso, elegante, notável*) | 5 (**2 falsos positivos**) |
| **§9 paralelismo negativo** (*"não é X, é Y"*) | **19, em 10 arquivos** |

**A camada didática v4 já tinha feito a maior parte deste trabalho.** As specs 097–102 reescreveram os
18 capítulos com cena narrativa, exemplo trabalhado e orçamento de travessão, e o efeito colateral foi
varrer quase todos os tiques clássicos. O que sobrou é uma passada **cirúrgica**, não uma reescrita — e
dizer isso é parte da entrega, porque o pedido implicava um trabalho maior do que o texto precisa.

## 2. Onde a skill e o livro divergem, e como resolvi

A **§14** manda cortar **todos** os travessões, como restrição dura. O `GUIA-EDITORIAL.md` §2.1 diz o
contrário, por escrito: *"o travessão é pontuação ordinária em pt-BR, e o que se combate aqui é o
empilhamento de apostos numa frase só, não a marca em si"*, e o portão `mede-prosa.mjs` está calibrado
em **≤8 por 1.000 palavras** com essa justificativa registrada na edição 0.81.

A própria skill resolve: *"A sample outranks this skill's style rules, **including the em dash rule in
§14**"*. O livro com seu guia editorial é esse *sample*. Mesma lógica para a **§15** (negrito), que na
v4 é instrumento didático declarado, não ênfase mecânica.

**Aplicadas integralmente**: §1–§13, §16–§33. **Subordinadas à voz do livro**: §14 e §15, mantendo o
limite do portão.

## 3. O padrão que importa, e por que não é eliminação

As 19 ocorrências de *"não é X, é Y"* são a assinatura retórica do livro. Várias são as melhores
frases que ele tem:

> *"Um juiz sem taxa de erro conhecida não é instrumento, é opinião com aparência de número."*
> *"O plan mode não é um modo do agente, é um **modo da política**."*

Nessas o contraste **é** o argumento. A §9 não pede que o contraste desapareça; pede que ele deixe de
sair sempre na mesma fôrma. A passada **reduz densidade e varia a forma** onde há aglomeração — o cap.
09 tem quatro em 3.242 palavras —, e preserva a construção onde ela carrega a tese.

O mesmo critério vale para a §31 (*punchlines* fabricados): uma frase curta para fechar um argumento é
recurso legítimo; três seguidas viram efeito.

## 4. Escopo

**Humanizados** (conteúdo): `00-introducao`, `01-fundamentos`, `14-convergencias`, `capitulos/02`–`17`,
`apendice-supply-chain`, `apendice-harness-um`, `apendice-harness-score`, `apendice-grafo`,
`apendice-uso`, `glossario`, `autor` — e os pares EN correspondentes, com selo i18n regravado.

**Preservados** (o editor pediu): `HISTORICO.md` (histórico), `radar/**` (notícias),
`apendice-estudo.md` (registro do estudo: o que foi lido, em que commit, em que data — é acervo, não
prosa), `benchmark/**` (fichas e comparativo), `GUIA-EDITORIAL.md` (é a régua, não o texto medido).

## 5. O processo, e por que não é script

A edição 0.85 registrou que **transformação roteirizada degrada prosa de um jeito que o portão sintático
não pega** — três rodadas de dano encontradas lendo, nenhuma medindo. Esta spec não repete o erro: cada
alteração é uma substituição exata, decidida na leitura do parágrafo, e nenhuma varredura de expressão
regular reescreve texto.

## 6. Instrução permanente

O pedido inclui tornar isto padrão. Duas escritas:

- **`CLAUDE.md`**: a passada humanizer entra na régua de escrita — todo texto novo de capítulo ou
  apêndice de conteúdo nasce com os padrões aplicados, com as §14/§15 subordinadas ao guia editorial.
- **`radar/AGENTE.md`**: o Radar escreve **notícia**, e notícia o editor mandou preservar. A instrução
  ali é de fronteira: a entrada diária **não** passa pelo humanizer, e o agente aplica a passada
  **depois** de publicar o Radar, quando tocar em conteúdo do livro.

## 7. Critério de parada

| Critério | Como se verifica |
|---|---|
| Zero ocorrências dos padrões §4/§7 que não sejam falso positivo declarado | varredura de conferência |
| §9 sem aglomeração: no máximo 1 por capítulo | varredura de conferência |
| Build verde nos 11 portões | `npm run build` |
| Selos i18n em dia | o próprio portão |
| PT e EN com paridade estrutural | `mede-prosa.mjs` |
| Nenhuma afirmação, número ou citação nova | diff lido por arquivo |
