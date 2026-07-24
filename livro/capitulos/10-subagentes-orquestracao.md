# 10 — Subagentes e Orquestração

## O problema

Um único contexto não segura tarefas grandes: exploração de codebase polui a janela com dumps de arquivos; trabalhos paralelizáveis rodam em série; e um agente generalista faz tudo mediocremente. Subagentes resolvem por **divisão de contexto** (o subagente lê 50 arquivos e devolve só a conclusão), **especialização** (prompts e permissões por papel) e **paralelismo**.

As decisões de projeto:
- **Isolamento**: o subagente roda em sessão-filha? Processo separado? Worktree git próprio (para edições paralelas sem conflito)?
- **Permissões**: herda as do pai? Derivadas e restritas?
- **Comunicação**: fire-and-forget (retorna um resultado) ou canal contínuo (mailbox, mensagens)?
- **Alcance**: só local, ou delegação a agentes remotos?

## Como os harnesses estudados implementam

### opencode — delegação contida e disciplinada
Tool `task` (`tool/task.ts`) lança um subagente numa **sessão-filha** (`parentID` na hierarquia de sessões), com **permissões derivadas e restritas** (`agent/subagent-permissions.ts`) e limite de profundidade (`subagent_depth`, default 1 — subagente não spawna subagente). Agentes definíveis em markdown com modo `primary|subagent|all`; built-in: `build`, `plan`, `general`, `compaction`. Modo background experimental: roda assíncrono, notifica ao terminar (`BackgroundJob`), e o `task_id` permite **retomar a mesma sessão de subagente** com contexto intacto. Filosofia: subagente como ferramenta pontual, com guardrails.

### gemini-cli — do subagente local ao agente remoto
Tool unificada `invoke_agent` sobre um `AgentRegistry` (`packages/core/src/agents/registry.ts`) que descobre e valida `AgentDefinition`s — built-in: **codebase-investigator, generalist, cli-help, browser agent, skill-extraction** — cada um com seu `ModelConfig` e política própria. Limites de terminação explícitos (`AgentTerminateMode`: GOAL/MAX_TURNS/TIMEOUT; defaults 30 turnos / 10 min). A exclusividade: **delegação remota via protocolo A2A** (`@a2a-js/sdk`, agent cards, autenticação plugável) — e o pacote `a2a-server` expõe o próprio gemini-cli como agente remoto para outros. Delegação tem evals comportamentais próprias (`subagents.eval.ts`, `generalist_delegation.eval.ts`).

### OpenHarness — times, não subagentes
O subsistema **Swarm** (`src/openharness/swarm/`, 11 módulos) modela algo qualitativamente diferente: **equipes persistentes**. `AgentTool` spawna agentes em três backends (subprocesso headless, remoto, teammate in-process); `TeamRegistry` mantém times e membros; **mailbox** (`mailbox.py`) dá comunicação contínua inter-agente (não só resultado final); `team_lifecycle.py` gerencia o ciclo de vida; **worktrees git** (`worktree.py`) isolam edições paralelas; `permission_sync.py` sincroniza permissões entre membros. Tools de primeira classe: `team_create/delete`, `send_message`, e gestão de tasks em background (`tasks/manager.py`).

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Mecanismo | tool `task` → sessão-filha | `invoke_agent` → registry | swarm: times + backends |
| Isolamento | sessão + permissões derivadas | processo/sessão por invocação | subprocesso + **worktree git** |
| Comunicação | resultado (+ retomada por id) | resultado | **mailbox contínua** |
| Especialização | agentes markdown | 5 built-in c/ modelo próprio | subagent_type + definitions |
| Remoto | — | **A2A client + server** | backend remoto |
| Guardrails | profundidade 1, permissões restritas | turnos/tempo/objetivo | sync de permissões |

Três filosofias: **subagente-como-ferramenta** (opencode — pontual, contido), **subagente-como-serviço** (gemini-cli — registry, contratos de terminação, alcance remoto) e **subagente-como-colega** (OpenHarness — times persistentes com caixa postal). A aposta do OpenHarness é a mais especulativa e a mais interessante: se modelos ficarem bons em coordenação, a mailbox e o worktree por membro são a infraestrutura certa; se não, é complexidade à frente do tempo. O A2A do gemini-cli aponta a outra direção óbvia: orquestração *entre* harnesses de fornecedores diferentes, com o agent card como contrato.
