# 09 — Planejamento

## O problema

Modelos tendem a agir precipitadamente: editam antes de entender, "resolvem" antes de mapear o problema. Os artefatos de planejamento forçam uma fase de leitura e desenho antes da fase de escrita — e dão ao humano um ponto de aprovação barato (revisar um plano custa menos que revisar um diff).

Três instrumentos distintos, frequentemente confundidos:
1. **Plan mode** — um *estado* do harness em que escrever é proibido; o agente só pesquisa e propõe.
2. **Todo list** — memória de trabalho da tarefa em andamento: o que falta, o que está feito.
3. **Decomposição** — quebrar trabalho grande em subtarefas rastreáveis, possivelmente com dependências.

## A convergência: plan mode = modo de permissão

A descoberta mais interessante da primeira rodada do benchmark: os três harnesses implementam plan mode **como um caso especial do sistema de permissões** (cap. 07), não como um subsistema próprio. Entrar em plan mode = trocar para um ruleset que nega escritas. Sair = restaurar. É elegante: reutiliza um mecanismo que já existe e ganha de graça a garantia de que o "modo de planejar" é *imposto*, não sugerido ao modelo.

## Como os harnesses estudados implementam

### opencode — plan como agente
O plan mode é um **agente built-in `plan`** com ruleset read-only (nega edições, pede confirmação para bash) — planejar é trocar de agente, não só de modo. A tool `plan_exit` (`tool/plan.ts`) fecha o ciclo: pergunta ao usuário se aprova, **escreve o plano em arquivo** e faz a transição para o agente `build` implementar. Prompts dedicados (`prompt/plan-mode.txt`, `plan-reminder-anthropic.txt` — inclusive lembretes específicos por família de modelo). Todos por sessão via tool `todowrite` (`session/todo.ts`).

### gemini-cli — plan com gatekeeping e decomposição opcional
`ApprovalMode.PLAN` (`policy/types.ts`) com tools `enter-plan-mode`/`exit-plan-mode`: estado read-only em que o prompt lista explicitamente as tools disponíveis (`planModeToolsList`), e `getApprovedPlanPath()` **gatekeepa a execução** — só se implementa plano aprovado. Todos via `WriteTodosTool`. E o instrumento que os outros não têm: o **tracker** opcional (`trackerTools.ts` + `trackerService.ts`) — tarefas com dependências (`tracker_add_dependency`) e visualização em grafo (`tracker_visualize`), decomposição de verdade para trabalho grande. Plan mode tem eval comportamental própria (`evals/plan_mode.eval.ts`).

### OpenHarness — a versão mínima e correta
`EnterPlanModeTool` simplesmente seta `settings.permission.mode = PLAN` (que bloqueia todas as escritas); `ExitPlanModeTool` restaura — a implementação mais direta da equivalência plan-mode-é-permissão. Todos em arquivo `TODO.md` via `TodoWriteTool` (persistente e legível, menos estruturado que os equivalentes em memória). Uma skill bundled `plan` orienta o desenho do plano, e a decomposição pesada aparece no subsistema autopilot (fila de `RepoTaskCard` com journal).

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Plan mode | agente `plan` dedicado | `ApprovalMode.PLAN` | modo de permissão |
| Artefato de plano | arquivo escrito ao sair | plano aprovado gatekeepa execução | skill orientadora |
| Todo list | por sessão (estruturada) | `write-todos` | arquivo `TODO.md` |
| Decomposição c/ dependências | — | tracker (grafo) | autopilot (fila de cards) |
| Transição plan→build | pergunta + troca de agente | aprovação de plano | troca de modo |

O padrão maduro combina três garantias: read-only **imposto** (não pedido), plano como **artefato persistido** (não só texto na conversa), e **aprovação explícita** antes de executar. O gemini-cli é o único que fecha as três; o opencode fecha duas com a elegância extra de planejar com um agente (que pode ter até modelo diferente); o OpenHarness prova que o essencial cabe em duas tools e um enum. A fronteira aberta é a decomposição com dependências — só o tracker do gemini-cli a tem como instrumento nativo, e ainda atrás de feature flag.
