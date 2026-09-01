# 0009 — Portão de slop bilíngue, sem a regra do travessão em nenhum dos dois idiomas

- **Status:** Aceito
- **Data:** 2026-08-13
- **Contexto (feature/spec):** `069-portao-de-slop`

## Contexto

Os capítulos deste livro nascem com apoio de IA — o `HISTORICO` registra o modelo de cada
edição. O Princípio I exige **evidência acima de retórica**, e o registro em que um texto
gerado costuma cair ("esta arquitetura desempenha um papel crucial no cenário em evolução
dos harnesses") é exatamente o oposto disso: retórica sem caminho de arquivo.

O `verifica-capitulos.mjs` mede estrutura — esqueleto v3, datação, downloads, sincronia
PT↔EN — e não olha a prosa. Nenhum portão olhava.

O portão vem do livro *Teoria das Restrições* (mesmo autor, ADR 0006 de lá), onde a decisão
central já havia sido tomada: **não medir travessão**, porque a regra §14 do guia de origem
("Signs of AI writing", Wikipédia) nasceu do inglês, e em português o travessão é pontuação
(aposto, intercalação, fala), não ornamento.

Aqui a questão volta com um dado novo: **este livro tem edição em inglês**, e naquele idioma
a regra se aplicaria de verdade.

## A medição

| | arquivos | palavras | travessões | por mil palavras |
|---|---|---|---|---|
| PT | 27 | 56.321 | 2.744 | 48,7 |
| EN | 27 | 48.131 | 1.265 | 26,3 |

A tradução já derrubou 46% da densidade: o tradutor converteu boa parte dos apostos em
vírgula e ponto. O que restou no EN **herda a pontuação do original** — é tradução de aposto
português, não hábito de composição em inglês.

## Decisão

**O portão não mede travessão em nenhum dos dois idiomas.** Todo o resto da lista vale nos
dois: 16 padrões em português e 16 em inglês, cada um com sua amostra-canário.

## Alternativas avaliadas

- **A — Aplicar §14 só ao EN.** Prós: coerente com a origem da regra, que é inglesa. Contras:
  1.265 achados de uma vez, todos em texto que o tradutor produziu fielmente a partir de
  pontuação portuguesa correta. Puniria a tradução por ser fiel, e um portão que acusa 1.265
  vezes no primeiro dia ensina a pessoa a ignorar a saída inteira — inclusive os achados
  reais dos outros 32 padrões.
- **B — Aplicar §14 aos dois.** Contras: os de A, mais 2.744 no PT, contra a gramática.
- **C — Teto por arquivo.** Contras: o número é arbitrário e pune o capítulo que usa aposto
  de forma correta e frequente. Troca uma questão de estilo por aritmética, que é o tipo de
  portão que se contorna sem pensar.
- **D — Não medir, e registrar por quê.** Escolhida.

## Justificativa

D vence porque preserva a única propriedade que faz um portão de estilo valer alguma coisa:
**zero achado no texto limpo**. Um achado futuro só significa algo se hoje não houver ruído.

A e B sacrificam essa propriedade por uma regra cuja premissa — "o em dash aqui é tique de
IA" — não se sustenta neste corpus: no PT ela contraria a gramática, e no EN o número que
sobra é resíduo de tradução, não escolha de composição.

O mesmo critério eliminou duas outras regras, ambas medidas antes de descartadas: §16
(listas com rótulo em negrito, descartada no repositório de origem por acusar notação
legítima) e parte de §18 — o `HISTORICO` fica fora da checagem de emoji porque é changelog e
usa ícone como índice visual (🏷 release, 📈 métrica, 🔑 chave, 🏁 marco: 11 pictogramas
avulsos, todos lá dentro e em nenhum outro arquivo).

Ainda em §18, a regra usa `\p{Emoji_Presentation}` e não `\p{Extended_Pictographic}`: o
segundo casa `↔`, que aparece 36 vezes no livro como relação bidirecional em texto técnico
("cliente ↔ servidor"), além de `→`, `✓` e `⚠`. Seta não é decoração.

## Consequências

- **Positivas:** o portão passa limpo nos dois idiomas hoje, então qualquer achado futuro é
  sinal. Cada padrão carrega um canário que o autoteste roda a cada build — e o canário é
  testado também dobrado em duas linhas, porque Markdown quebra parágrafo onde quiser e a
  primeira versão deixava passar todo slop que caísse na dobra. Custo por capítulo novo: zero.
- **Negativas / custos aceitos:** fica um tell de IA sem cobertura automática nos dois
  idiomas. Se o hábito do travessão vier do agente e não do autor, só a revisão editorial
  humana percebe. A decisão se apoia em gramática e em densidade de tradução, não numa
  amostra independente da escrita do autor.
- **Reversibilidade:** alta. Acrescentar a contagem é uma entrada na tabela `PADROES`. Quem
  fizer isso terá de argumentar contra o cabeçalho do `verifica-slop.mjs`, que é onde a
  justificativa mora. **Gatilho para reabrir:** um capítulo composto direto em inglês (não
  traduzido) — aí a premissa desta decisão deixa de valer para o EN.
