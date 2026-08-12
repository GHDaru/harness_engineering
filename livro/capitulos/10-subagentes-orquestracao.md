# 10. Subagentes e Orquestração

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](../HISTORICO.md)
>
> Camada didática v4 — ver [Guia Editorial §2.1](../GUIA-EDITORIAL.md).
> andaime: lacuna
>
> Esqueleto v3, corpo com o estado da arte; tratamento por repositório no Apêndice A (complementação online).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Explicar** por que o ganho primário de um subagente é isolamento de contexto (lê muito, devolve pouco), não paralelismo;
2. **Comparar** as três filosofias: subagente-como-ferramenta, como-serviço e como-colega;
3. **Avaliar** o gate de custo/benefício de decompor-e-paralelizar (a tensão Anthropic × Cognition) e os modos de falha que justificam guardrails;
4. **Distinguir** delegação local de delegação entre sistemas (A2A (Agent-to-Agent)/ACP (Agent Client Protocol)) e quando cada uma se aplica;
5. **Implementar** a tool `task` com sessão-filha e permissões derivadas no harness-zero (etapa 9).

## A resposta cabia em duas linhas, e a leitura estourou a janela

*"Descubra onde a autenticação é validada neste repositório."*

O agente sai procurando. Abre `auth.py`, segue para `middleware/`, entra em `session.py`, dá uma passada em três testes, volta para o roteador, confere dois decoradores. Cinquenta arquivos depois, ele responde:

> A validação acontece em `middleware/auth.py:41`, no decorador `@requires_auth`.

Duas linhas. Corretas.

Agora olhe o contexto: 80% da janela ocupada. Não pela resposta, que é minúscula, mas pela **leitura** que a produziu, cinquenta arquivos inteiros que ninguém vai reler, e que agora competem por espaço com o trabalho que vem depois.

E o trabalho que vem depois é o que interessa: você queria a resposta para *então* pedir a mudança. Só que a janela já foi.

O problema não é o agente ter lido demais. Era preciso ler para saber. O problema é a leitura ter ficado **no mesmo lugar** que o trabalho seguinte.

## O problema

Um único contexto não segura tarefas grandes: exploração de codebase polui a janela com dumps de arquivos; trabalhos paralelizáveis rodam em série; e um agente generalista faz tudo mediocremente. Subagentes resolvem por **divisão de contexto** (o subagente lê 50 arquivos e devolve só a conclusão), **especialização** (prompts e permissões por papel) e **paralelismo**.

As decisões de projeto:
- **Isolamento**: sessão-filha? Processo separado? Worktree git próprio (para edições paralelas sem conflito)?
- **Permissões**: herda as do pai? Derivadas e restritas? Degradadas por profundidade?
- **Comunicação**: fire-and-forget (retorna um resultado) ou canal contínuo (mailbox, mensagens)?
- **Alcance**: só local, ou delegação a agentes remotos de outros vendors?

## Fundamentos científicos

A literatura de sistemas multi-agente (MAS) tem duas mensagens para quem constrói harness: os padrões que funcionam, e a advertência de que a maioria das falhas é de projeto.

- **A falha é de design, não do modelo**: [MAST, "Why Do Multi-Agent LLM (Large Language Model) Systems Fail?", arXiv 2503.13657](https://arxiv.org/abs/2503.13657) deriva empiricamente 14 modos de falha em três categorias (especificação/papéis · desalinhamento inter-agente · verificação de tarefa). Conclui que a maioria vem do *sistema*, não dos pesos. Decisão: invista em specs de papel explícitos, checagens de alinhamento e um estágio de verificação dedicado, não num modelo maior.
- **Papéis e SOPs contra alucinação em cascata**: [MetaGPT, arXiv 2308.00352](https://arxiv.org/abs/2308.00352) codifica *Standardized Operating Procedures* e papéis de linha de montagem (PM, arquiteto, engenheiro, QA) com artefatos intermediários estruturados, porque encadear LLMs ingenuamente propaga alucinação. Saídas escopadas por papel deixam o agente seguinte verificar o anterior. E [CAMEL, arXiv 2303.17760](https://arxiv.org/abs/2303.17760) mostra que o role-play **deriva** (troca de papel, repetição, término precoce), a estabilidade de papel precisa ser *imposta*, não assumida.
- **Topologia programável e recrutamento dinâmico**: [AutoGen, arXiv 2308.08155](https://arxiv.org/abs/2308.08155) separa os agentes da topologia de conversa (troque o padrão de orquestração sem reescrever agentes). [AgentVerse, arXiv 2308.10848](https://arxiv.org/abs/2308.10848) monta o grupo por tarefa e monitora comportamento emergente negativo. [ChatDev, arXiv 2307.07924](https://arxiv.org/abs/2307.07924) decompõe o pipeline em diálogos de duas partes por fase. Ponteiro de taxonomia: o [survey de MAS, arXiv 2402.01680](https://arxiv.org/abs/2402.01680).
- **O ceticismo saudável**: o debate multi-agente é uma primitiva de verificação ([Du et al., arXiv 2305.14325](https://arxiv.org/abs/2305.14325)), mas [Should We Be Going MAD?, arXiv 2311.17371](https://arxiv.org/abs/2311.17371) e [Stop Overvaluing Multi-Agent Debate, arXiv 2502.08788](https://arxiv.org/abs/2502.08788) mostram que ele nem sempre bate self-consistency/CoT a compute igual. Decisão: **sempre compare o harness multi-agente com um baseline single-agent compute-matched** antes de aceitar a complexidade.

(Bibliografia completa e ponteiros: `livro/bibliografia.md`.)

## Fontes da indústria

- **Subagente = instância isolada com toolset restrito**: [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents): cada subagente é uma instância *fresca e isolada* lançada pela tool `Task`, com janela de contexto própria e toolset por tipo de agente. Os [subagents do Agent SDK](https://platform.claude.com/docs/en/agent-sdk/subagents) são declarados como config (nome, tools, modelo, prompt), dá para fixar modelos baratos (Haiku para Explore read-only) por papel e impor least-privilege por tipo. Decisão: um subagente de busca queima tokens explorando sem poluir o contexto do orquestrador, devolvendo só um resumo compacto.
- **Orchestrator-worker. O preço**: o [multi-agent research system da Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system): um *lead* planeja, grava o plano em memória e spawna subagentes paralelos, cada um com contexto isolado e um **contrato explícito** (objetivo, formato de saída, tools, fronteiras). O ganho de largura vem a **~15× os tokens** de um chat único (e, segundo o post, tokens explicam ~80% da variância de desempenho), só paga em tarefas de alto valor e muita amplitude. O [guia de quando usar multi-agente](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them) dá os três casos: poluição de contexto, subtarefas genuinamente paralelas, especialização que afia a seleção de tools. *(anthropic.com 403 pelo proxy; números por espelhos independentes.)*
- **O contra-argumento**: [Don't Build Multi-Agents (Cognition)](https://cognition.com/blog/dont-build-multi-agents): prefira um agente **single-thread com compressão de contexto**. Quando o trabalho se abre em paralelo, cada subagente age sobre uma visão parcial e toma decisões implícitas conflitantes (o exemplo do Flappy Bird: um constrói fundo estilo Mario, outro um pássaro incompatível), um "telefone sem fio" que cria a etapa de reconciliação que a própria arquitetura gerou. Dois princípios: *compartilhe o traço completo com todo agente* e *ações carregam decisões implícitas, evite as conflitantes*. Para tarefas longas, adicione um modelo de compressão em vez de dividir a thread. *(cognition.com 403; confirmado por HN/GitHub.)*
- **Os frameworks materializam os padrões**: [Agents SDK (OpenAI)](https://openai.github.io/openai-agents-python/multi_agent/) distingue **handoffs** (transfere controle a um especialista) de **agents-as-tools** (um manager chama sub-agentes como funções, mantendo a thread). O [Swarm](https://github.com/openai/swarm) foi a origem educacional do handoff. [CrewAI](https://docs.crewai.com/en/concepts/processes) escolhe entre **sequential** e **hierarchical** (`manager_llm` delega e valida). O [LangGraph](https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems) modela um **supervisor** roteando entre workers com estado persistente. O [Magentic-One (AutoGen)](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html) mantém um **ledger de progresso** e replaneja na falha; o [ADK do Google](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) mistura coordinator/dispatcher com primitivas `Sequential/Parallel/Loop`. Decisão: escolha a forma de coordenação (handoff × tool × supervisor × ledger) pelo que precisa reter, thread, controle ou recuperação.
- **Delegação entre sistemas: A2A (e ACP convergindo nele)**: quando os subagentes vivem em vendors diferentes, a delegação vira protocolo: o [A2A](https://a2a-protocol.org/latest/specification/) usa **Agent Cards** (JSON anunciando identidade, skills, endpoint, auth) para descoberta e **Tasks** com ciclo de vida como unidade de trabalho delegado, sobre HTTP+JSON-RPC (Remote Procedure Call)+SSE (Server-Sent Events). É a generalização cross-org do handoff da tool `Task`. O [ACP (IBM/BeeAI)](https://agentcommunicationprotocol.dev/introduction/welcome) era a alternativa REST-nativa, mas [fundiu-se no A2A sob a Linux Foundation em ago/2025](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/). Decisão: para trabalho novo, padronize no A2A (liga ao cap. 17).
- **Consulte também**: a coleção viva [Awesome Harness Engineering: Task Runners & Orchestration](https://github.com/GHDaru/awesome-harness-engineering#task-runners--orchestration) reúne mais recursos consultáveis desta dimensão (padrões, artigos e implementações), curados por problema.

## Na prática: a sessão-filha, e o que atravessa a fronteira

Um subagente é uma sessão nova com contexto limpo. O que faz dele uma ferramenta útil não é o paralelismo: é o que **não** atravessa a fronteira.

```python
@tools.tool
def task(descricao: str) -> str:
    """Delega uma subtarefa a uma sessão-filha com contexto limpo.
    Devolve APENAS o resultado final, o trabalho intermediário não volta."""
    filha = Sessao(
        mensagens=[Message("user", descricao)],   # ← só isto vai na ida
        tools=so_leitura(TOOLS_DO_PAI),           # ← interseção, nunca expansão
        max_turnos=20,
        orcamento_usd=pai.orcamento_restante() * 0.3,
    )
    fim = rodar_turno(filha)
    return fim.texto                              # ← só isto volta
```

Três decisões estão nessas dez linhas, e nenhuma é sobre velocidade.

**Na ida vai só a descrição.** A filha não herda o histórico do pai. Isso a torna mais burra sobre o contexto e imune ao ruído dele, e é o ponto: os cinquenta arquivos da cena vão para a janela **dela**, que será descartada.

**Na volta vem só o resultado.** É a assimetria que resolve o problema da abertura. O pai gasta duas linhas de contexto por uma tarefa que consumiu oitenta por cento de uma janela inteira.

**As tools são interseção, nunca expansão.** `so_leitura(TOOLS_DO_PAI)` significa que a filha nunca pode fazer o que o pai não podia, e por padrão nem escreve. Um subagente que pudesse escalar privilégio seria uma porta dos fundos na política do cap. 07, e "delegar" viraria o jeito de contornar a regra.

O orçamento também desce, e desce **fracionado**:

```python
orcamento_usd=pai.orcamento_restante() * 0.3
```

Sem isso, dez subagentes com o teto do pai gastam dez vezes o teto do pai. O orçamento propagado é o que impede a delegação de virar multiplicação.

E o caso em que delegar **piora**, que é o que a maioria dos textos omite:

```python
# RUIM: a subtarefa precisa negociar decisões de volta
task("refatore o módulo de pagamentos como você achar melhor")

# LACUNA (etapa 9): escreva o guarda que recusa delegar quando a descrição
# não converge para um fato. Dica: exigir critério de conclusão verificável.
def delegavel(descricao: str) -> bool:
    ...
```

A filha vai decidir sozinha, sem o contexto das conversas anteriores, e voltar com duas linhas descrevendo escolhas que você teria vetado. A assimetria que economiza contexto é a mesma que **impede negociação**: quando a tarefa exige idas e vindas de julgamento, o canal estreito deixa de ser vantagem e vira cegueira.

A regra prática que sai daí: delegue o que **converge para um fato**: encontrar, medir, listar, resumir. Não delegue o que **converge para uma decisão**.

## O estado da arte

### 1. Três filosofias, ferramenta, serviço, colega

A moldura da primeira rodada persiste e ganhou reforço da rodada 2. **Subagente-como-ferramenta**: pontual, contido, com guardrails (opencode `task` → sessão-filha, depth 1; Aider split architect→editor, depth 1). **Subagente-como-serviço**: registry, contratos de terminação, alcance remoto (gemini-cli `invoke_agent` + A2A; Codex `multi_agents_v2` com **grafo de agentes persistido** e ~100 perfis; Goose `orchestrator` lead/worker). **Subagente-como-colega**: equipes persistentes com comunicação contínua (OpenHarness Swarm com mailbox + worktree git por membro; Hermes com **Kanban dispatcher** e handoffs estruturados).

### 2. O ganho primário é isolamento de contexto, não paralelismo

O que os três harnesses da rodada 1 já mostravam, a indústria consolidou: o subagente vale porque **lê muito e devolve pouco**. É por isso que o Claude Code o modela como instância *fresca* e isolada, e por que o worktree git (OpenHarness) importa, ele isola *edições* paralelas, não só leituras. Isso é o mesmo princípio do "contexto escopado por subtarefa" do cap. 09 (Beyond Entangled Planning): o subagente é o veículo de escopo de contexto.

### 3. A tensão central: paralelizar custa, e a maioria das falhas é de design

O eixo de decisão da dimensão é a tensão Anthropic × Cognition. Orchestrator-worker compra largura (+~90% em pesquisa) a **~15× tokens**; o single-thread evita o "telefone sem fio" mas serializa. O MAST fecha o argumento com dados: a maioria das falhas de MAS é de *especificação e coordenação*, não do modelo, o que explica por que todo harness sério cerca subagentes de **guardrails**: profundidade limitada (opencode/Aider depth 1. OpenClaw 1–5), contratos de terminação (gemini-cli GOAL/MAX_TURNS/TIMEOUT), permissões **degradadas por profundidade** (OpenClaw: subagente nunca ganha `message`/`gateway`/`cron`), e a expressão extrema, o **IronClaw deny-filtra `spawn_subagent` em todos os profiles de produção** (o design suporta, a política proíbe até haver confiança). A regra de projeto: decompor-e-paralelizar é um gate de custo/benefício, com baseline single-agent como controle.

### 4. A virada: orquestrar harnesses de outros vendors

A fronteira que a rodada 2 tornou concreta: o subagente pode ser *outro harness*. O OpenClaw orquestra Claude Code, Gemini CLI, opencode e Codex como subagentes via runtime **ACP**. O OpenHands (Canvas) orquestra Claude Code, Codex e Gemini via perfis **ACP**; o gemini-cli é cliente **e servidor A2A**. Com o ACP-IBM (Agent Communication Protocol) convergindo no A2A sob a Linux Foundation, o *agent card* vira o contrato universal de delegação entre sistemas. A orquestração deixou de ser interna ao harness e virou interoperabilidade (cap. 17).

> **Adendo da rodada ext-1 (2026-07-31): o isolamento de *workspace* virou infraestrutura.** O corpus isolava o **contexto** do subagente; o [Grok Build](../../benchmark/avaliacoes/grok-build.md) (xAI, aberto em 2026-07-15) fecha a outra metade, o **filesystem**. Cada `spawn_subagent` com isolamento ativo recebe uma **git worktree própria** criada por uma crate dedicada (`xai-fast-worktree`: CoW paralelo, snapshots BTRFS O(1), overlayfs, metadata com auto-GC), com merge de volta como operação de protocolo (`x.ai/git/worktree/apply`) e fallback gracioso para o workspace compartilhado. A lição não é "usar worktrees" (vários harnesses têm); é o investimento em torná-las **baratas o bastante para o agente usar sem pensar**, subagentes paralelos que editam deixam de brigar pelo working tree. Confirmado no código (`agent/subagent/handle_request.rs`), não só no anúncio.

### Leitura executiva

O que está mais moderno: subagente como isolamento de contexto com contrato explícito. A escolha de coordenação (handoff × tool × supervisor × ledger). Guardrails motivados por modos de falha reais (MAST); a delegação cross-vendor via A2A; e (desde a rodada ext-1) o isolamento de workspace por worktree barata (Grok Build). **O que roubar:** dê a cada subagente um contrato (objetivo/formato/tools/fronteiras) e contexto isolado. Limite profundidade e degrade permissões por profundidade. Compare sempre com um single-agent compute-matched; se subagentes editam em paralelo, isole o filesystem (worktree), não só o contexto; e, se orquestrar entre sistemas, fale A2A.

## Mão na massa, harness-zero, etapa 9

A etapa 9 (`harness-zero/etapas/09-subagentes/`) adiciona uma tool `task` que lança um **subagente em sessão-filha**: contexto próprio, **permissões derivadas e restritas** da sessão-pai. **profundidade máxima 1** (subagente não spawna subagente), os guardrails que o MAST justifica, na sua forma mínima. O subagente recebe um contrato (objetivo + formato de saída), roda seu próprio loop e devolve só o resumo ao pai. Exercício de completude: você adiciona a degradação de permissões por profundidade e um contrato de terminação configurável (objetivo + timeout por subagente).

## Verificação

1. Seu orquestrador precisa entender 40 arquivos para decidir um refactor, mas você não quer 40 dumps no contexto principal. Como um subagente resolve, e qual é o ganho real?
2. Um colega propõe rodar 5 subagentes em paralelo para acelerar. Cite o principal risco (com um nome da literatura/indústria) e o gate que você aplica antes de aceitar.
3. Você quer que seu harness delegue uma subtarefa a um agente de outro vendor. Que mecanismo usa e qual é o "contrato"?
---

## Apêndice A — Como cada repositório trata subagentes e orquestração

> Evidência por harness, com paths — complementação online, expandida a cada rodada.

### opencode (rodada 1) — delegação contida
Tool `task` (`tool/task.ts`) → subagente em **sessão-filha** (`parentID`), **permissões derivadas e restritas** (`agent/subagent-permissions.ts`), depth 1. Agentes em markdown com modo `primary|subagent|all`; built-in `build`/`plan`/`general`/`compaction`. Modo background experimental (`BackgroundJob`) com `task_id` para **retomar a sessão de subagente**.

### gemini-cli (rodada 1) — do subagente local ao remoto
`invoke_agent` sobre `AgentRegistry` (`packages/core/src/agents/registry.ts`); built-in codebase-investigator, generalist, cli-help, browser, skill-extraction, cada um com `ModelConfig`. Terminação explícita (`AgentTerminateMode`: GOAL/MAX_TURNS/TIMEOUT). Exclusividade: **A2A** client+server (`@a2a-js/sdk`, agent cards). Evals de delegação próprias.

### OpenHarness (rodada 1) — times, não subagentes
Swarm (`src/openharness/swarm/`, 11 módulos): `AgentTool` em três backends (subprocesso, remoto, teammate in-process); `TeamRegistry`; **mailbox** (comunicação contínua); **worktrees git** (`worktree.py`) para edições paralelas; `permission_sync.py`. Tools `team_create/delete`, `send_message`.

### Codex CLI (rodada 2) — grafo de agentes persistido
Duas gerações de API (`multi_agents_v2`: spawn, send_message, followup, interrupt, wait); ~100 perfis de subagentes em TOML; **`agent-graph-store`** (grafo persistido), identidade de agente, comunicação inter-agente, hooks SubagentStart/Stop; `ThreadManager` coordenando threads paralelas.

### OpenClaw (rodada 2) — spawn push-based e ACP externo
`sessions_spawn` cria subagentes isolados com **conclusão push-based** (`sessions_yield` como espera sem polling); nesting 1–5; política de tools **degradada por profundidade** (subagentes nunca ganham `message`/`gateway`/`cron`). Runtime **ACP** orquestra Claude Code, Gemini CLI, opencode e Codex como subagentes; Swarm via Code Mode.

### Hermes (rodada 2) — Kanban dispatcher
`delegate_task` spawna `AIAgent` filhos com contexto isolado e aprovação não-interativa segura; **Kanban dispatcher** no gateway spawna workers com handoffs estruturados, bloqueio para input humano e heartbeat em operações longas.

### Goose (rodada 2) — SubRecipes e orchestrator
`summon` delega a subagentes (Agent filho com recipe própria, eventos streamados); **SubRecipes** com composição hierárquica e execução paralela/sequencial; extensão `orchestrator` (lead/worker: list/start/send/interrupt/stop).

### Aider (rodada 2) — architect→editor
Split `architect_coder.py`: um modelo raciocinador produz o plano; após confirmação, um segundo coder (com `editor_model`/`editor_edit_format` próprios) executa. Orquestração de dois papéis com modelos distintos, profundidade fixa 1.

### IronClaw (rodada 2) — design elegante, política restritiva
Subagentes como child-runs no mesmo pipeline, com gates/checkpoints unificados e teste E2E — **mas `spawn_subagent` está deny-filtrado em todos os profiles de produção** (`TEMP(disable-spawn-subagents)`). A nota reflete a capacidade disponível, não o design (que seria 3). O caso extremo de "guardrail vence capacidade".

### OpenHands / ohmo (rodada 2)
OpenHands: primitivas do SDK (`openhands.sdk.subagent`) + **AgentProfiles** por organização, incluindo perfis **ACP** — o Canvas orquestra Claude Code, Codex e Gemini. ohmo: Agent/Task/Team/SendMessage herdados; assimetria observada (`/tasks run` bloqueado remotamente, tools equivalentes disponíveis ao modelo).

### Grok Build (rodada ext-1) — worktrees como infraestrutura ⭐
`agent/subagent/handle_request.rs`: `spawn_subagent` com `capability_mode` **intersectado** com o toolset do tipo (`intersect_capability_modes`), profundidade máx. 1, `resume_from`, contratos de I/O entre personas; isolamento por `WorktreeBuilder…worktree_kind(WorktreeKind::Subagent)` sobre `xai-fast-worktree` (CoW + BTRFS O(1) + auto-GC), merge via `x.ai/git/worktree/apply`; agentes de plugin proibidos de declarar `mcpServers`/hooks/`bypassPermissions`.

### Pi (rodada ext-1) — a recusa documentada
Sem subagentes no core, por manifesto ("There's many ways to do this; spawn pi instances via tmux, or build your own"); o exemplo primeiro-classe `examples/extensions/subagent/` spawna **processos `pi` completos** (isolamento real de contexto) com 4 personas e 3 workflows — a feature existe como prova de que a superfície de extensão basta.

### n8n (rodada 2) — agente como tool de agente
**AI Agent Tool** (`AgentTool.node.ts` v3): um agente completo como tool de outro — o V3 roda o loop do sub-agente inline (`resolveSubAgentRequest`), com proibição de HITL aninhado; **ToolWorkflow** (sub-workflows como tools). Orquestração hierárquica visual.

### Frameworks (rodada frameworks)
Agents SDK: handoffs × agents-as-tools; CrewAI: sequential × hierarchical (`manager_llm`); LangGraph: supervisor + workers como nós com estado; AutoGen/Magentic-One: orchestrator com ledger e replanejamento; Google ADK: coordinator/dispatcher + `Sequential/Parallel/Loop`. Os frameworks expõem como API de primeira classe o que os harnesses de código implementam à mão.

---

## Respostas da verificação

**1.** O subagente resolve porque a fronteira é **assimétrica**: na ida atravessa só a descrição da tarefa, e na volta só o resultado. Os quarenta arquivos entram na janela da filha, que é descartada quando ela termina, e o pai recebe o parágrafo que interessa. O ganho não é de velocidade, é de **orçamento de contexto**: você troca uma leitura de dezenas de milhares de tokens por algumas centenas, e o pai continua com espaço para fazer o trabalho que motivou a pergunta. É a mesma ideia do `dado` × `para_o_modelo` do cap. 05, subida um nível: o que volta é o destilado, e o bruto morre onde foi lido.

**2.** O principal risco é a **falta de contexto compartilhado**: cinco subagentes trabalhando em paralelo tomam decisões incompatíveis entre si, porque cada um só enxerga a própria descrição, e o resultado é um conjunto de partes que não fecham. A literatura de sistemas multiagente descreve isso como o problema de **coordenação**, e a versão prática é conhecida: dois subagentes renomeiam a mesma função de dois jeitos, ou um assume um contrato que o outro mudou.

O portão que se aplica antes de paralelizar é a **independência do resultado**: só paralelize subtarefas cujo resultado não depende do resultado das outras. Encontrar cinco coisas em paralelo é seguro; **decidir** cinco coisas em paralelo não é. E, quando há escrita envolvida, some-se o isolamento de arquivos — worktree ou diretório próprio —, porque paralelismo sobre o mesmo working tree produz conflito antes de produzir resposta.

**3.** O mecanismo é o protocolo **agente-para-agente** do cap. 17, e o contrato tem duas partes. A primeira é a **descoberta**: o agente remoto publica um descritor dizendo quem é, o que faz e como autenticar, e é isso que permite delegar sem acoplamento a um fornecedor. A segunda é o **ciclo de vida da tarefa**: o pedido vira uma tarefa com estado, com andamento reportado e resultado final tipado, porque delegação entre organizações não pode depender de uma conexão aberta.

A ressalva que o benchmark obriga a fazer: essa fronteira é a que **menos** tem uso medido no corpus. O padrão existe, a governança é sólida, e a adoção nos harnesses de produto ainda é rara — enquanto a delegação *dentro* de casa, por sessão-filha ou por protocolo de composição, é o que aparece no código.
