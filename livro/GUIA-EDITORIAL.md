# Guia Editorial — regras operacionais do livro

> Versão operacional das orientações pedagógicas. O parecer completo (com fundamentação) está em [`estudos/2026-07-25-parecer-editorial-plano-pedagogico.md`](../estudos/2026-07-25-parecer-editorial-plano-pedagogico.md). Este guia é o que se consulta **enquanto escreve**.

## 1. O framework pedagógico em quatro linhas

| Framework | O que dita no livro |
|---|---|
| **Backward Design** | Todo capítulo se projeta de trás para frente: objetivos → evidências (verificação/prática) → só então o conteúdo |
| **4C/ID** | Etapas do harness-zero = tarefas inteiras; capítulos = informação de apoio; boxes no código = just-in-time; katas = treino de parte |
| **Diátaxis** | Quatro tipos de texto, nunca misturados na mesma seção: capítulo=explanation, harness-zero=tutorial, templates/benchmark=reference, "o que roubar"=how-to |
| **Carga Cognitiva** | Worked examples antes de exercício; exercícios são "complete", não "crie do zero"; andaime diminui etapa a etapa; uma ideia nova por vez |

## 2. Esqueleto v3 de capítulo (obrigatório; piloto: cap. 04)

**Regra de edição (v3):** ao abrir cada tema, buscar também **material comercial/industrial** (docs oficiais de vendors, blogs de engenharia, posts de praticantes) além do científico. A fonte-base continua sendo **o código dos repositórios**. O corpo do capítulo recebe **o estado da arte** (o que está mais moderno, sintetizado de todas as rodadas do benchmark + indústria); o tratamento detalhado **por repositório vai para o Apêndice do arquivo** — que fica na versão online como complementação e é atualizado a cada rodada.

1. **Objetivos** — 3–5, verbos de Bloom (explicar, comparar, implementar, avaliar)
2. **O problema** — por que a dimensão existe
3. **Fundamentos científicos** — 2–4 papers *traduzidos para decisões*; ponteiro para `bibliografia.md`
4. **Fontes da indústria** — docs de vendor e posts de engenharia relevantes, com a mesma regra de tradução ("o vendor recomenda X porque Y")
5. **O estado da arte** — o corpo principal: padrões consolidados + o que há de mais moderno, citando repositórios apenas como exemplos nominais (o detalhe fica no apêndice)
6. **Mão na massa** — a etapa correspondente do harness-zero
7. **Síntese + "o que roubar"** — leitura executiva e ideias exportáveis
8. **Verificação** — 2–3 perguntas que testam exatamente os objetivos do item 1
9. **Apêndice A — Como cada repositório trata** — a evidência por harness com paths, expandida a cada rodada do benchmark (material de complementação online)

## 2.1 Livro vivo: datação e histórico (obrigatório)

Este é um **livro vivo** — coerência com a própria tese (a cláusula de expiração: o que descrevemos é temporário). Três regras:

1. **Todo capítulo v3 declara a data de captura no cabeçalho**: `> **Estado da arte capturado em AAAA-MM** · última revisão AAAA-MM-DD · [histórico](../HISTORICO.md)`. Isso diz ao leitor se a seção "Estado da arte" está fresca — o que a data do *evento* (no corpo) não faz.
2. **Distinguir três datas** (ver `HISTORICO.md`): data do evento (no corpo — fato histórico, imutável), data de captura (no cabeçalho — quando fotografamos), rodada do benchmark (nas avaliações — versão da foto de cada repo). Reavaliar = nova rodada, nunca sobrescrever.
3. **Toda edição atualiza `livro/HISTORICO.md`**: o changelog de edições, a tabela de snapshot por capítulo, e — o mais importante — o **registro de expiração** (o placar das previsões: cada cláusula de expiração pontuada 🔵/🟡/🟢/🔴 contra a realidade, com evidência datada). Uma linha que muda de estado é a notícia mais importante de uma nova edição.

Regra de escrita associada: quando uma afirmação for sensível ao tempo ("hoje", "ainda não", "o consenso de 2026"), ela está implicitamente sob a data de captura do cabeçalho — não precisa datar cada frase, mas evite absolutos atemporais ("nunca", "sempre") a menos que sejam do tipo não-expira (fronteira com o mundo).

## 3. Regras de escrita permanentes

- **Evidência por caminho de arquivo** para qualquer afirmação sobre um harness; **status ✓** para qualquer citação científica (skill `academic-research` tem o fluxo).
- Notas 0–3 só comparam dentro da mesma categoria do benchmark.
- Cada componente descrito deve, quando possível, declarar sua **cláusula de expiração**.
- Prosa em português; termos técnicos consagrados (harness, loop, tool, prompt) **sem tradução**.
- Tabelas para fatos enumeráveis; explicação vive na prosa, não nas células.

## 4. Regras do harness-zero (as 4 condições do parecer)

1. **DDD leve** — linguagem ubíqua = glossário do livro; padrão tático só onde paga; DDD aparece como consequência nomeada no código.
2. **Arquitetura por refatoração** — cada porta nasce da dor do capítulo correspondente; nunca estrutura antecipada.
3. **Anti-apodrecimento** — modelo atrás de `LLMPort`; etapas autocontidas e executáveis; erros didáticos deliberados são **comentados como tal** no código.
4. **Chat congelado** — HTML+JS servido pelo backend; só evolui quando uma dimensão exigir superfície nova.

## 5. Ferramentas do repositório

- **spec-kit** (`.specify/` + comandos `/speckit-*`): para features novas do harness-zero ou seções grandes do livro, o fluxo é `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` (com `/speckit-clarify` antes do plano quando o pedido for ambíguo). A constitution do projeto vive em `.specify/memory/`.
- **Skill `academic-research`** (`.claude/skills/`): fluxo de localizar → validar → registrar → integrar referências científicas.
- **`scripts/sync-forks.ps1`**: sincronização local dos forks com upstreams.
