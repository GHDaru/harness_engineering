# Spec 097 — Reescrita didática: capítulos que um humano lê

> Branch: `097-reescrita-didatica` · aberta em 2026-08-11
> Princípios em jogo: **III** (método pedagógico), **I** (evidência), **IV** (livro vivo)

## 1. O problema

Os capítulos passaram no esqueleto v3 — 16 de 18 têm objetivos, mão na massa, verificação e selo de captura. A estrutura está certa. **A prosa não é de ensino, é de dossiê.**

O capítulo 05 é o caso limpo. Uma frase do corpo:

> "Os harnesses convergem num núcleo de ~10 tools (ler/escrever/editar arquivo, glob, grep, shell, web fetch/search, todo, delegar) — o kit mínimo de um agente de código. E ninguém escreve JSON Schema à mão: a fonte de verdade é o sistema de tipos (Pydantic no OpenHarness/Hermes, Effect Schema no opencode, classes declarativas no gemini-cli, dataclasses genéricas no software-agent-sdk)."

Duas frases, sete nomes próprios, quatro conceitos novos, zero exemplo. Isso é excelente **material de consulta** e péssimo **material de leitura**. O leitor que já sabe confirma; o leitor que veio aprender desliza.

### 1.1 Medição (não impressão)

Corpo dos 18 capítulos, Apêndice A excluído — 31.623 palavras:

| Métrica | Medido | Alvo didático | Por quê |
|---|---|---|---|
| Travessões por 1.000 palavras | **22,0** | ≤ 8 | Um a cada 45 palavras. O travessão empilha aposto sobre aposto: é o mecanismo pelo qual sete ideias entram numa frase |
| Amplitude entre capítulos | 15,3 – 30,0 | — | **Uniformidade é o achado.** Um tique estilístico do autor varia por assunto e por humor; este não varia. É assinatura de gerador, não de voz |
| Comprimento médio de frase | 26,1 palavras | 17–20, com variância alta | Prosa didática alterna: frase longa que constrói, frase curta que crava |
| Frases acima de 60 palavras | 51 no livro | ≤ 10 | Nenhuma delas sobrevive à leitura em voz alta |
| Exemplos trabalhados no corpo | **0** | ≥ 1 por capítulo | 4C/ID e Sweller pedem *worked example antes do exercício*. O guia editorial já manda; o texto não cumpre |

A última linha é a mais séria: o `GUIA-EDITORIAL.md` §1 prescreve "worked examples antes de exercício" e "uma ideia nova por vez". **O livro descreve um método pedagógico que não aplica a si mesmo** — exatamente a falha que ele acusa nos outros (Princípio I: prosa não é sensor).

### 1.2 O que não está errado

A densidade não é defeito de pesquisa; é defeito de **destino**. Tudo o que está no corpo é verdadeiro, verificado e tem path. O problema é que material de referência foi servido como material de explicação — os dois tipos que o Diátaxis (já adotado no guia) manda **nunca** misturar na mesma seção.

Logo: nada se joga fora. Move-se.

## 2. O método — camada didática v4

O v4 **não substitui** o esqueleto v3: acrescenta uma camada de escrita sobre ele. Estrutura permanece; prosa muda.

### 2.1 As sete regras de reescrita

1. **Uma porta de entrada narrativa.** O capítulo abre com uma cena concreta — uma falha, uma decisão, um número que não fecha — antes de qualquer definição. O leitor precisa de um motivo para ler o parágrafo 2.
2. **Um exemplo trabalhado por capítulo.** Código ou diálogo real, resolvido *na frente do leitor*, com o raciocínio visível. Vem **antes** do exercício, nunca depois.
3. **Conceito antes de nome.** `to_llm_content`, `defer_loading`, V4A: o leitor recebe a ideia primeiro e o rótulo depois, na mesma frase ("...um campo que decide o que volta ao modelo — no software-agent-sdk chama-se `to_llm_content`").
4. **Uma ideia nova por parágrafo.** Se o parágrafo apresenta dois conceitos inéditos, ele é dois parágrafos.
5. **Nomes de repositório saem do corpo.** O corpo cita repositório apenas quando o exemplo *é* aquele repositório. A varredura "quem faz o quê" é Apêndice A — que já existe e é para isso.
6. **Verificação sem gabarito na mesma linha.** As respostas descem para o fim do capítulo. Recuperação só treina quando há esforço de recuperação.
7. **Travessão com orçamento.** ≤ 8 por 1.000 palavras. Cada corte força uma escolha: virar frase, virar parêntese, ou a ideia sair. Quase sempre a terceira é a certa.

### 2.2 O que a camada acrescenta a cada capítulo

Entre "O problema" e "Fundamentos científicos":

- **Abertura** (2–4 parágrafos) — a cena. Sem citação, sem lista.

Dentro de "O estado da arte":

- **Exemplo trabalhado** — uma seção `### Na prática` com código comentado e o porquê de cada escolha.

No fim:

- **Respostas da verificação** — seção final, depois do Apêndice A, com o gabarito comentado.

Seções de "Fontes da indústria" viram **prosa de síntese** com as fontes em nota, ou descem para o Apêndice A quando forem inventário.

### 2.3 Avaliação — o que o repositório acadêmico entra fazendo

`ghdaru/academic-research-skills` (fork; upstream `Imbad0202/academic-research-skills`) entra como **régua**, não como autor. Dois artefatos são aplicáveis diretamente:

- `academic-paper/references/writing_quality_check.md` — travessões, *throat-clearing*, comprimento uniforme de parágrafo, "compulsão da regra de três", *burstiness*. Escrito para inglês acadêmico; **as regras de padrão valem, os limites numéricos são recalibrados para prosa didática em português** (o travessão é pontuação normal em pt-BR; o que se combate é o empilhamento de apostos, não o sinal).
- `academic-paper-reviewer` modo `guided` — revisão socrática questão a questão, o formato certo para texto que ensina.

O que **não** se aplica: IMRaD, APA, PRISMA e os portões de integridade de pesquisa. Este livro não é um paper; usar o revisor de manuscrito inteiro mediria a coisa errada.

## 3. Escopo

**Entra:** os 18 capítulos do corpo (`livro/00`, `livro/01`, `livro/capitulos/02–17`, `livro/14`), na ordem de leitura.

**Não entra nesta spec:** apêndices, glossário, bibliografia, `harness-um`. A tradução do delta para `livro/en/` acompanha cada capítulo reescrito, conforme a regra permanente.

**Piloto:** capítulo 02 (Loop do agente) — é o coração conceitual e o primeiro capítulo em que o leitor decide se continua.

## 4. Critérios de aceitação

Por capítulo reescrito:

- [ ] Abre com cena concreta, não com definição
- [ ] Tem ≥ 1 exemplo trabalhado com código no corpo
- [ ] Travessões ≤ 8 por 1.000 palavras (medido pelo script)
- [ ] Frase média ≤ 20 palavras; nenhuma frase acima de 60
- [ ] Nenhum conceito nomeado antes de explicado
- [ ] Gabarito da verificação fora da pergunta
- [ ] Esqueleto v3 intacto (objetivos, mão na massa, verificação, selo)
- [ ] Apêndice A preservado — nada de evidência se perde
- [ ] Delta traduzido para `livro/en/` + selo i18n com md5-8 real
- [ ] `node publicar/build.mjs` verde

Do conjunto:

- [ ] Script `publicar/mede-prosa.mjs` roda no build e reporta as métricas por capítulo
- [ ] `GUIA-EDITORIAL.md` ganha a §2.2 com a camada v4
- [ ] `HISTORICO.md` registra a edição com nota A3

## 5. Riscos

| Risco | Mitigação |
|---|---|
| Perder evidência ao "arejar" o texto | Nada é apagado: o que sai do corpo desce para o Apêndice A, sempre num commit que mostra as duas pontas |
| Capítulos incharem e o livro virar outro livro | Alvo de +40% no corpo, não +150%. O ganho vem de *mover*, não só de acrescentar |
| A régua de prosa em inglês distorcer o português | Limites recalibrados e declarados nesta spec; o script mede o que decidimos, não o que o checklist estrangeiro decidiu |
| Reescrever tudo e só depois descobrir que o tom não agradou | Piloto de um capítulo, revisão do editor, e só então a cascata |

## 6. Registro

O capítulo 05 fica como **antes/depois** documentado: é o exemplo que a §1 usa para diagnosticar, e serve de par comparativo quando for reescrito.
