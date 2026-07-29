# 15 — O Harness Embutido: agentes dentro de motores de workflow

> **Estado da arte capturado em 2026-07** · última revisão 2026-07-28 · [histórico e registro de expiração](../HISTORICO.md)
>
> Capítulo derivado da avaliação de motores de workflow no benchmark; evidência por repositório no Apêndice A (complementação online, atualizado a cada rodada do benchmark).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Explicar** a inversão que define a categoria — o workflow contém o harness, e não o contrário — e por que ela levanta a pergunta "quais dimensões do scaffolding são essenciais, e quais são substituíveis pelo ambiente?";
2. **Identificar** quais dimensões do scaffolding o ambiente de workflow dispensa (compactação, planejamento, entrega de contexto, permissões granulares) e **justificar** por que cada uma se torna dispensável;
3. **Analisar** a implementação de um nó de agente real (o AI Agent do n8n, Apêndice A como gabarito) e localizar onde o loop, as tools e as permissões vivem;
4. **Avaliar** quando usar um harness embutido versus um dedicado, em função da duração e da autonomia da tarefa — e reconhecer o teto da substituição;
5. **Aplicar** as ideias exportáveis da categoria a um harness dedicado: derivação de tools a partir de superfícies existentes (padrão `$fromAI`) e human-in-the-loop durável.

## O problema

Nos capítulos anteriores, o harness contém o trabalho: o loop dirige, as tools agem, o workflow emerge das decisões do modelo. Ferramentas como o **n8n** invertem a relação — **o workflow contém o harness**. Um "nó de agente" é uma etapa dentro de um grafo desenhado por um humano, cercado de gatilhos (webhook, cron, chat), integrações e tratamento de erro que o motor de workflow já fornecia antes de existir IA.

Essa inversão levanta a pergunta que dá sentido à categoria: **quais dimensões do scaffolding são essenciais, e quais são substituíveis pelo ambiente?**

## O estado da arte

### O que o ambiente dispensa

A avaliação do representante da categoria (n8n, ver Apêndice A) confirma a tese com precisão incômoda: as dimensões fracas do harness embutido são exatamente as que o ambiente dispensa.

| Dimensão dispensada | Por que o ambiente dispensa |
|---|---|
| Compactação | Execuções acionadas por evento são curtas — o contexto não acumula |
| Planejamento | O plano *é* o grafo do workflow, desenhado pelo humano no canvas |
| Entrega de contexto | O contexto vem mapeado das etapas anteriores via expressões |
| Permissões granulares | A topologia já é a allowlist |

O último ponto merece ênfase: no harness embutido, **a permissão é topologia**. Não há aprovação por chamada dentro do loop — o LLM (Large Language Model) só pode invocar o que o autor plugou no canvas. É allowlist por construção, decidida visualmente por um humano, complementada por human-in-the-loop real: nós que pausam a execução de forma durável aguardando aprovação num canal (Slack/Outlook), em vez do prompt síncrono de aprovação dos CLIs.

E as dimensões fortes são onde o motor tem vantagem estrutural: **ferramentas** (as integrações pré-existentes viram pool de tools), **memória** (backends de banco plugáveis), **interfaces** (chat hospedado, webhooks, widget embarcável), **MCP (Model Context Protocol)** (client *e* server) e **subagentes** (agente-como-tool e sub-workflows). Nenhum harness dedicado tem um pool de tools do tamanho de um ecossistema de integrações convertido — porque nenhum tem um ecossistema pré-existente para converter.

### O loop emprestado — e a trajetória de reinternalização

O harness embutido tipicamente não escreve o próprio loop: ele o toma emprestado de um framework (no caso observado, LangChain JS). Mas a trajetória medida no benchmark aponta numa direção clara: o motor de workflow começa terceirizando o loop e **reinternaliza a metade que importa para um motor de workflow — o agendamento da execução**. O framework continua decidindo *qual* tool chamar; a *execução* da chamada volta a ser responsabilidade do engine, que agenda os nós e reentra no agente. (Detalhe de código no Apêndice A, achado 1.) A implicação: os motores tendem a absorver cada vez mais o harness, não o contrário.

### O teto da substituição

Mas a substituição tem teto: **sem compactação nem planejamento, o nó de agente serve automações curtas, não trabalho longo autônomo**. Um agente embutido que precisasse refatorar um repositório por horas colapsaria a janela de contexto sem defesa. As duas camadas não competem — se complementam por duração e autonomia da tarefa: o harness dedicado para trabalho longo e aberto; o embutido para decisões pontuais dentro de processos estruturados.

### Implicações

1. **Para quem constrói harness dedicado**: o padrão `$fromAI` (Apêndice A, achado 2) mostra como derivar tools de superfícies existentes sem escrever wrappers; o HITL durável (pausar a execução por dias aguardando aprovação num canal) é superior ao prompt síncrono de aprovação dos CLIs.
2. **Para quem constrói sobre motores de workflow**: as lacunas da categoria (compactação, plan mode) são o roadmap óbvio — e a trajetória de reinternalização do loop sugere que os motores vão absorver cada vez mais o harness, não o contrário.
3. **Para a taxonomia do livro**: "quanto harness é preciso" é função do *ambiente de execução*, não constante universal. A régua do benchmark mede scaffolding presente; esta categoria lembra que scaffolding ausente-por-design não é lacuna — desde que a classe de tarefa seja respeitada.

### Leitura executiva

O harness embutido não é um harness dedicado incompleto: é uma categoria em que o ambiente de execução substitui, por construção, metade das dimensões do scaffolding — plano vira grafo, permissão vira topologia, contexto vira expressão mapeada. A substituição vale enquanto a classe de tarefa for respeitada: decisões pontuais dentro de processos estruturados, não trabalho longo autônomo. **O que roubar** hoje: derivação automática de tools a partir de integrações existentes (padrão `$fromAI`) e human-in-the-loop durável em vez de aprovação síncrona.

> **Consulte também**: a coleção viva [Awesome Harness Engineering — Production Infrastructure & Operations](https://github.com/GHDaru/awesome-harness-engineering#production-infrastructure--operations) reúne mais recursos consultáveis desta dimensão, curados por problema.

## Verificação

1. Enuncie a inversão que define a categoria e explique por que ela transforma "dimensões fracas" do benchmark em "dimensões dispensadas pelo ambiente". (Se precisar, releia "O que o ambiente dispensa".)
2. Por que a permissão-como-topologia dispensa aprovação por chamada dentro do loop — e qual mecanismo complementa essa allowlist quando uma decisão humana é realmente necessária no meio da execução?
3. Um time quer usar um nó de agente de motor de workflow para refatorar um repositório por horas. Explique, em termos de compactação e planejamento, por que isso colapsa — e qual seria a divisão correta entre harness embutido e dedicado nessa tarefa.
4. Cite as duas ideias da categoria que valem exportação para um harness dedicado e o que cada uma substitui ou melhora. (Dica: derivação de tools e HITL.)

---

## Apêndice A — n8n (nó AI Agent)

> Evidência por repositório, com paths — material de complementação (versão online), expandido a cada rodada do benchmark. A avaliação completa do n8n (29/36) está em `../../benchmark/avaliacoes/n8n.md`.

### Anatomia do nó de agente (evidência: `packages/@n8n/nodes-langchain`)

O n8n implementa o agente como um "cluster node": um nó-raiz **AI Agent** com portas tipadas onde se plugam sub-nós — modelo (`AiLanguageModel`), memória (`AiMemory`), ferramentas (`AiTool`), parser de saída. Três achados de código estruturam o capítulo:

**1. O loop é emprestado — e está sendo devolvido.** A geração V2 delega tudo ao LangChain JS (`AgentExecutor.fromAgentAndTools`, `maxIterations` 10). Mas a V3 mudou o desenho: o LangChain ainda *decide* qual tool chamar (`createToolCallingAgent`), porém a *execução* virou responsabilidade do motor do n8n — as tool calls viram `EngineRequest` devolvidos ao engine, que agenda os nós e reentra no agente com `EngineResponse`. O n8n começou terceirizando o loop e está **reinternalizando** a metade que importa para um motor de workflow: o agendamento da execução.

**2. A ponte `$fromAI` — a ideia mais exportável da categoria.** `create-node-as-tool.ts` transforma **qualquer um dos 400+ nós de integração** marcado `usableAsTool` numa tool do agente: o traversal dos parâmetros coleta expressões `$fromAI('chave', 'descrição', tipo)` — os slots que o LLM deve preencher — e gera o schema Zod automaticamente. Nenhum harness dedicado tem um pool de tools desse tamanho, porque nenhum tem um ecossistema de integrações pré-existente para converter.

**3. A permissão é topologia.** Não há aprovação por chamada dentro do loop: o LLM só pode invocar o que o autor plugou na porta `AiTool` do canvas. É allowlist por construção, decidida visualmente por um humano — complementada por human-in-the-loop real (nós `sendAndWait` pausam a execução de forma durável aguardando aprovação no Slack/Outlook, proibidos dentro de sub-agentes) e um nó Guardrails.

### O placar (29/36) e o mapa força/fraqueza

As dimensões fracas da avaliação são as que o ambiente dispensa: **compactação (1)** — execuções acionadas por evento são curtas, o contexto não acumula; **planejamento (1)** — o plano é o grafo desenhado no canvas; **entrega de contexto (2)** — o contexto vem mapeado das etapas anteriores via expressões; **permissões granulares (2)** — a topologia já é a allowlist.

E as fortes são onde o motor tem vantagem estrutural: **ferramentas (3)** — as integrações; **memória (3)** — backends de banco plugáveis; **interfaces (3)** — chat hospedado, webhooks, widget embarcável; **MCP (3)** — client **e** server: o `McpTrigger` expõe as tools do n8n a clientes MCP externos; **subagentes (3)** — agente-como-tool e sub-workflows.

*Primos a avaliar em rodadas futuras: Zapier Agents, Make, Dify, Flowise.*
