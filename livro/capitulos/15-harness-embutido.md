# 15 — O Harness Embutido: agentes dentro de motores de workflow

## A inversão

Nos capítulos anteriores, o harness contém o trabalho: o loop dirige, as tools agem, o workflow emerge das decisões do modelo. Ferramentas como o **n8n** invertem a relação — **o workflow contém o harness**. Um "nó de agente" é uma etapa dentro de um grafo desenhado por um humano, cercado de gatilhos (webhook, cron, chat), integrações e tratamento de erro que o motor de workflow já fornecia antes de existir IA.

Essa inversão levanta a pergunta que dá sentido à categoria: **quais dimensões do scaffolding são essenciais, e quais são substituíveis pelo ambiente?**

## Anatomia do nó de agente do n8n (evidência: `packages/@n8n/nodes-langchain`)

O n8n implementa o agente como um "cluster node": um nó-raiz **AI Agent** com portas tipadas onde se plugam sub-nós — modelo (`AiLanguageModel`), memória (`AiMemory`), ferramentas (`AiTool`), parser de saída. Três achados de código estruturam o capítulo:

**1. O loop é emprestado — e está sendo devolvido.** A geração V2 delega tudo ao LangChain JS (`AgentExecutor.fromAgentAndTools`, `maxIterations` 10). Mas a V3 mudou o desenho: o LangChain ainda *decide* qual tool chamar (`createToolCallingAgent`), porém a *execução* virou responsabilidade do motor do n8n — as tool calls viram `EngineRequest` devolvidos ao engine, que agenda os nós e reentra no agente com `EngineResponse`. O n8n começou terceirizando o loop e está **reinternalizando** a metade que importa para um motor de workflow: o agendamento da execução.

**2. A ponte `$fromAI` — a ideia mais exportável da categoria.** `create-node-as-tool.ts` transforma **qualquer um dos 400+ nós de integração** marcado `usableAsTool` numa tool do agente: o traversal dos parâmetros coleta expressões `$fromAI('chave', 'descrição', tipo)` — os slots que o LLM deve preencher — e gera o schema Zod automaticamente. Nenhum harness dedicado tem um pool de tools desse tamanho, porque nenhum tem um ecossistema de integrações pré-existente para converter.

**3. A permissão é topologia.** Não há aprovação por chamada dentro do loop: o LLM só pode invocar o que o autor plugou na porta `AiTool` do canvas. É allowlist por construção, decidida visualmente por um humano — complementada por human-in-the-loop real (nós `sendAndWait` pausam a execução de forma durável aguardando aprovação no Slack/Outlook, proibidos dentro de sub-agentes) e um nó Guardrails.

## O que o ambiente dispensa — e o teto da substituição

A avaliação do n8n (29/36, ver `benchmark/avaliacoes/n8n.md`) confirma a tese da categoria com precisão incômoda. As dimensões fracas são exatamente as que o ambiente dispensa:

| Dimensão fraca | Por que o ambiente dispensa |
|---|---|
| Compactação (1) | Execuções acionadas por evento são curtas — o contexto não acumula |
| Planejamento (1) | O plano *é* o grafo do workflow, desenhado pelo humano no canvas |
| Entrega de contexto (2) | O contexto vem mapeado das etapas anteriores via expressões |
| Permissões granulares (2) | A topologia já é a allowlist |

E as fortes são onde o motor tem vantagem estrutural: ferramentas (3 — as integrações), memória (3 — backends de banco plugáveis), interfaces (3 — chat hospedado, webhooks, widget embarcável), MCP (3 — client **e** server: o `McpTrigger` expõe as tools do n8n a clientes MCP externos), subagentes (3 — agente-como-tool e sub-workflows).

Mas a substituição tem teto: **sem compactação nem planejamento, o nó de agente serve automações curtas, não trabalho longo autônomo**. Um agente n8n que precisasse refatorar um repositório por horas colapsaria a janela de contexto sem defesa. As duas camadas não competem — se complementam por duração e autonomia da tarefa: o harness dedicado para trabalho longo e aberto; o embutido para decisões pontuais dentro de processos estruturados.

## Implicações

1. **Para quem constrói harness dedicado**: o `$fromAI` mostra como derivar tools de superfícies existentes sem escrever wrappers; o HITL durável (pausar a execução por dias aguardando aprovação num canal) é superior ao prompt síncrono de aprovação dos CLIs.
2. **Para quem constrói sobre motores de workflow**: as lacunas do n8n (compactação, plan mode) são o roadmap óbvio — e a trajetória V2→V3 sugere que os motores vão absorver cada vez mais o harness, não o contrário.
3. **Para a taxonomia do livro**: "quanto harness é preciso" é função do *ambiente de execução*, não constante universal. A régua do benchmark mede scaffolding presente; esta categoria lembra que scaffolding ausente-por-design não é lacuna — desde que a classe de tarefa seja respeitada.

*Primos a avaliar em rodadas futuras: Zapier Agents, Make, Dify, Flowise.*
