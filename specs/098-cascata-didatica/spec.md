# Spec 098 — Cascata didática v4: capítulos 00, 01 e 17

> Branch: `098-cascata-didatica` · aberta em 2026-08-12
> Método: [spec 097](../097-reescrita-didatica/spec.md) · princípios: **III** (pedagogia), **I** (evidência)

## 1. O que esta spec faz

Executa o primeiro lote da cascata definida na spec 097, depois de o editor aprovar o tom do piloto (cap. 02). Três capítulos, PT e EN, na camada didática v4.

A ordem não é a numérica: é a de risco de abandono.

| Capítulo | Por que agora | Estado antes |
|---|---|---|
| **00 Introdução** | primeira página do livro; se o leitor desiste, desiste aqui | 26,7 travessões/1k · sem exemplo trabalhado |
| **01 Fundamentos** | é onde o vocabulário é fixado, e abria com meta-comentário ("este capítulo fixa…") | 20,4 travessões/1k · sem exemplo trabalhado |
| **17 Protocolos** | o **pior do livro** nos dois eixos, e um capítulo sobre protocolos que nunca mostrava um protocolo | 30,0 travessões/1k · frase média 33,2 na medição antiga |

## 2. O que mudou no medidor, e por quê

O portão da 097 reprovou dois dos três capítulos. Nos dois casos o defeito era **do instrumento**, não do texto, e a causa era a mesma: **estrutura medida como se fosse prosa**.

**Falso positivo 1, listas coladas.** `frasesDe()` colapsava `\n+` num espaço antes de dividir por pontuação. Uma lista de seis itens sem ponto final virava uma "frase" de 90 palavras. O cap. 00 reprovou com "2 frases acima de 60" que eram duas listas.

Consequência retroativa: o baseline publicado na edição 0.81 (**26,1** palavras/frase e **51** frases longas) estava inflado. O real é **23,4** e **24**. A contagem de travessões (**22,0**) não muda, porque não depende de fronteira de frase. Corrigido no guia, PT e EN, e registrado no `HISTORICO.md` sem reescrever o registro da 0.81.

**Falso positivo 2, tabela contada como pontuação.** O cap. 17 acusou 12,2 travessões/1k tendo três na prosa. O medidor contava as células `—` de "não se aplica" da matriz de adoção, que é justamente o melhor ativo do capítulo.

**Correção única para os dois:** as métricas passam a considerar **apenas linhas de prosa corrida**. Ficam fora tabela (`|`), citação (`>`), cabeçalho (`#`), HTML e imagem. E cada linha é fronteira de frase, porque item de lista termina no fim da linha mesmo sem ponto.

**Terceira correção, de regra e não de medida:** o gabarito em seção própria passa a ser exigido só de capítulo que **tem** seção de verificação. A introdução não tem, e exigir dela era exigir resposta de pergunta que não existe.

## 3. Critérios de aceitação

Por capítulo, PT e EN:

- [x] abre com cena concreta, não com definição nem com meta-comentário
- [x] pelo menos um exemplo trabalhado com código no corpo
- [x] travessões ≤ 8 por 1.000 palavras de prosa
- [x] frase média ≤ 20 palavras, nenhuma acima de 60
- [x] gabarito em seção própria quando há verificação
- [x] esqueleto v3 preservado e Apêndice A intacto onde existe
- [x] delta traduzido para `livro/en/` com selo i18n de md5-8 real
- [x] `npm run build` verde

Medição final:

| Capítulo | travessões/1k | frase média | frases > 60 | exemplo | gabarito |
|---|---|---|---|---|---|
| 00 | 4,0 | 15,9 | 0 | sim | não se aplica |
| 01 | 1,8 | 17,2 | 0 | sim | sim |
| 02 (piloto) | 0,0 | 13,7 | 0 | sim | sim |
| 17 | 1,8 | 15,9 | 0 | sim | sim |

## 4. O que cada capítulo ganhou de substância

**00** — a cena do conselho perfeito que não conserta nada, e um transcript comentado com a mesma pergunta em dois destinos, modelo puro contra modelo com harness, em que cada linha aponta o capítulo que a explica. Fecha com a observação que a versão antiga não fazia: **ninguém sabia que havia dois problemas**, e o segundo só existe porque o primeiro foi consertado e o teste rodou de novo.

**01** — três engenheiros com três definições incompatíveis no lugar de "este capítulo fixa o vocabulário", e um exemplo trabalhado que **aplica** o teste das quatro peças a três sistemas, com veredito em cada um. A definição deixa de ser enunciada e passa a ser usada. Ganhou também verificação com gabarito, que não existia, e um parágrafo sobre o critério "inspecionável × participável" que o Radar levantou em 10/ago.

**17** — as mensagens na rede, que faltavam a um capítulo sobre protocolos: `tools/list` e `tools/call` do MCP contra `session/prompt` e `session/update` do ACP, lado a lado. Daí sai a leitura nova: o `stopReason` do ACP **é** o rótulo tipado de terminação do cap. 02 exposto na fronteira, e é o `session/update` que explica por que o ACP se espalhou entre harnesses, e não só entre editores.

## 5. Fila restante da 097

Quatorze capítulos: 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15 e 16. Pelo relatório do medidor, os próximos por gravidade são **13 Interfaces** (22,2/1k e 5 frases longas), **11 Verificação** (22,1/1k e 3 longas) e **04 Compactação** (23,4/1k e 3 longas).
