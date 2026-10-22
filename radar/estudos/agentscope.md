# Estudo: AgentScope — triagem de candidato ao corpus

> Pedido do editor, fora da execução agendada. Escrito em `radar/`, conforme a regra dura de escopo.
> Data da leitura: **2026-10-22**. Prosa humanizada antes do commit; citação verbatim, número, data, link
> e ⏳ intocados.

## Resumo para o editor

O AgentScope **passa o teste de inclusão do cap. 01 §4** com folga incomum: os quatro elementos aparecem
não só no README, mas como **pacotes nomeados no código** — `agent/`, `tool/`, `permission/` e, para
gestão de contexto, uma cadeia de `middleware/`. Não há sinal de inflação: razão estrela/fork de **9,1:1**,
Apache-2.0 confirmado por duas fontes independentes, repositório não arquivado, atividade de outubro.

O problema que ele traz **não é se entra, e sim por qual régua**. O repositório contém duas camadas: um
framework e um **Agent Service** com multi-tenancy, UI web, canais de IM, persistência e agendamento. O
cap. 01 §4 decide o Caso 3 — framework que expõe as quatro peças como possibilidade — mandando entrar como
**framework**, avaliado por outra régua. O AgentScope é framework **e** produto implantável no mesmo
endereço, e a regra de que *as notas só comparam dentro da mesma categoria* precisa de uma decisão que não
é minha para tomar.

Recomendação: **entra como candidato**, com arquétipo a decidir pelo editor, e com uma observação que vale
mais que a classificação — ele é o único sistema que eu vi modelar **diretório de trabalho adicional como
tipo do contexto de permissão**, que é exatamente o defeito que o OpenClaw divulgou em 11/set.

## 1. Triagem no repositório (o que o contrato exige antes de qualquer alegação)

| Campo | Valor | Fonte |
|---|---|---|
| **Endereço canônico** | `agentscope-ai/agentscope` | `pyproject.toml`, campos `Homepage` e `Repository` |
| Endereço antigo | `modelscope/agentscope` — serve conteúdo idêntico no `raw` | duas leituras do mesmo arquivo |
| Licença | **Apache-2.0** | `pyproject.toml` (`license = "Apache-2.0"`) **e** página pública |
| Linguagem | Python, `requires-python = ">=3.11"` | `pyproject.toml` |
| Versão no `main` | `2.0.11dev` | `src/agentscope/_version.py` |
| Estrelas × forks | **33,7 mil × 3,7 mil = 9,1:1** | página pública |
| Arquivado | **Não** — nenhum aviso de arquivamento ou somente-leitura | página pública |
| Observadores | 162 | página pública |
| Commits | 787 | página pública |
| Issues / PRs abertos | 360 / **287** | abas da página pública |
| Atividade recente | item de **outubro de 2026** no README (`Agent service supports realtime voice conversations over WebRTC`) | README |
| Publicações | [arXiv:2402.14034](https://arxiv.org/abs/2402.14034) e [arXiv:2508.16279](https://arxiv.org/abs/2508.16279) | seção *Publications* do README |

**Inflação: nenhum sinal.** A razão 9,1:1 está bem acima do limiar de ~5:1 do contrato. Pelo refinamento
que eu propus em 23/set — comparar contra irmão já avaliado em vez de contra um número absoluto —, ela é
melhor que a do `HKUDS/nanobot` (5,6:1) e que a do `HKUDS/OpenHarness` (6,1:1).

**Obituário precoce: descartado.** Não arquivado, com item de release de outubro e dois papers publicados.

**Duas autodescrições, e elas divergem.** O `pyproject.toml` diz *"AgentScope: A Flexible yet Robust
Multi-Agent Platform."*; a descrição da página diz *"Build and run agents you can see, understand and
trust."* A primeira é de plataforma multiagente; a segunda é de observabilidade. Registro a divergência em
vez de escolher — é o mesmo tipo de campo divergente que eu catalogei em 4/out, quando o mesmo defeito
tinha CWE-200 no GHSA e CWE-669 no registro do CVE.

⏳ **787 commits incomodam.** Para um projeto com paper de 2024 e 33,7 mil estrelas, 787 commits sugerem
repositório reiniciado ou reescrito para a linha 2.0 — o que mudaria a leitura de *"endereço antigo serve
conteúdo idêntico"* de renomeação para projeto novo. O `raw` idêntico nos dois endereços é compatível com
as duas hipóteses, e eu não tenho como separá-las sem a API. Fica aberto.

## 2. Teste de inclusão do cap. 01 §4, com a linha que prova cada resposta

O método do capítulo manda procurar a evidência, e não aceitar a prosa. Fiz as duas coisas: cito o README
e confirmo o módulo por requisição ao arquivo.

**1. Loop do agente — sim.** README, verbatim:

> *"[ReAct] Reasoning-acting loop with structured output, realtime interruption & resume, and batched
> (sequential / concurrent) tool acting"*

Código: `src/agentscope/agent/__init__.py` responde 200.

**2. Interface de ferramentas — sim.** README, verbatim:

> *"[Toolkit] Agentic tool management over Python tools, MCP servers, and skills; ships with built-in
> coding tools (shell, file edit, search) and task/plan tools"*

Código: `src/agentscope/tool/__init__.py` responde 200.

**3. Gestão de contexto — sim, e por uma via arquitetural própria.** README, verbatim:

> *"[Context] Automatic compaction, tool-result offload, and context injection (system prompt, RAG,
> memory) via built-in middleware"*

Não existe pacote `context/` no topo; o que existe é `middleware/`, e os seus exports mostram a escolha:
`RAGMiddleware`, `AgenticMemoryMiddleware`, `Mem0Middleware`, `ReMeMiddleware`,
`ReplyBudgetControlMiddleware`, `TracingMiddleware`, `ModelRouterMiddleware`, sobre um `MiddlewareBase`.

**4. Mecanismos de controle — sim, e é a parte mais interessante.** README, verbatim:

> *"[Permission & HITL] Fine-grained control over tools and resources, confirmation, bypass mode"*
>
> *"[Workspace / Sandbox] Isolated tool & code execution — local, Docker, Apple Container, Bubblewrap,
> E2B, OpenSandbox, Daytona, K8s"*

Código: `src/agentscope/permission/__init__.py` exporta, verbatim do arquivo:

> *`PermissionContext`, `AdditionalWorkingDirectory`, `PermissionDecision`, `PermissionEngine`,
> `PermissionRule`, `PermissionMode`, `PermissionBehavior`*

**Veredito do teste: as quatro peças existem.** Pelo critério do capítulo, que separa categoria de
qualidade, isso basta para entrar no estudo.

## 3. O problema de arquétipo, que é o que vale levar ao editor

O cap. 01 §4 resolve o Caso 3 assim: framework que expõe loop, estado e ferramentas como primitivas, sem
rodar nada por conta própria, entra como **framework**, com régua própria, porque comparar permissão de
framework com permissão de produto *"seria comparar potencial com escolha"*.

O AgentScope quebra a dicotomia, porque traz as duas coisas. A seção *Agent Service — All You Need to Build
Your App* promete, verbatim do README: *"Multi-tenancy, multi-session isolation, FastAPI backend,
pre-built Web UI"*; *"Leader–worker orchestration, built-in team tools, task planning"*; *"Connect agents
to IM platforms — Feishu (Lark), Discord, custom channels, message routing"*; *"SQL & NoSQL persistence of
agent state and sessions"*; e *"Scheduled tasks, agent wakeup, background task offloading"*.

Isso não é biblioteca esperando quem decida. São decisões tomadas: há tenant, há sessão isolada, há
backend, há UI. Três leituras possíveis, e a escolha é editorial:

1. **Dois registros no Apêndice A** — `agentscope` como framework e `agentscope-service` como produto —,
   cada um pela sua régua. Custa duplicação e resolve a comparabilidade.
2. **Um registro de arquétipo novo**, algo como *plataforma*, que é como o próprio manifesto se descreve.
   Custa uma categoria a mais no benchmark e reconhece o que o sistema é.
3. **Um registro como framework**, com nota de que a camada de serviço existe e não foi avaliada. Custa
   subestimar, e é a opção que eu escolheria se tivesse de escolher hoje, porque é a única que não afirma
   mais do que eu li.

Minha recomendação é a **3 com prazo**: entrar como framework agora, com a camada de serviço marcada como
não avaliada, e reabrir a questão de arquétipo quando alguém ler o serviço. O que eu **não** faço é decidir
sozinho a taxonomia do estudo.

## 4. Onde o AgentScope toca eixos abertos do Radar

Isto é o que justifica o estudo mesmo que a inclusão seja negada.

**Diretório de trabalho dentro do contexto de permissão.** O export `AdditionalWorkingDirectory` põe o
diretório como **tipo do contexto de permissão**. Em 5/out eu registrei, do lote de advisories do OpenClaw
de 11/set, o título *"Exec approvals could outlive their reviewed working directory"*. O AgentScope modela
no tipo exatamente aquilo cuja ausência produziu o advisory. É o achado mais citável do estudo.

**A decisão de permissão como objeto.** `PermissionDecision` existe como tipo, separado de
`PermissionBehavior` e de `PermissionMode`. O eixo da aprovação como objeto, que em 7, 16 e 17/out ganhou
quatro modos de falha — tomada, forjada, plantada em memória e **inventada pelo intermediário** —, pede
precisamente que a decisão seja um objeto com dono e autenticidade. Aqui ela é um tipo. ⏳ Se carrega
titular e assinatura, não sei: não li o `_decision.py`.

**Verificação de permissão como middleware componível.** O README lista, entre os ganchos, verbatim:
*"Composable hooks across the loop — reply, reasoning, acting, model calling, permission checking, context
compression, system prompt"*. Em 9/out eu registrei que o gancho de guarda do Claude Code falhou aberto de
três formas e formulei que **o portão que você acrescenta é um portão que pode falhar aberto**. Aqui o
portão **é** um gancho, por arquitetura, o que torna a pergunta estrutural em vez de acidental.

**`bypass mode` declarado no README.** O sistema de permissão anuncia modo de desvio como recurso. Não é
defeito — produtos do corpus têm equivalente —, e é dado para a coluna de postura que eu venho propondo.

**Rastro como middleware.** `TracingMiddleware` está na mesma cadeia componível que o resto. Em 27/set o
paper de adulteração de rastro recomendou que o registro passe por *"an independent interception mechanism
outside of the agent's control"*. Um rastro que é middleware da composição que o agente configura está, por
construção, dentro do alcance dela. ⏳ **Não afirmo defeito**: não li como o `TracingMiddleware` é montado
nem quem pode removê-lo. Registro a pergunta, que é a certa a fazer.

**Orçamento de resposta como middleware.** `ReplyBudgetControlMiddleware` é critério de parada como peça de
primeira classe. O eixo que o APPA nomeou em 2/out como encalhe por monotonia, e que apareceu como laço de
autenticação sem cabeça em 3/out, tem aqui um lugar arquitetural para morar.

**Bubblewrap entre os oito backends de sandbox.** A mesma primitiva cuja integridade o Codex passou a
medir em 0.163.0 — e que, pelo PR #51843 que eu li hoje, mede **sem bloquear**. Um candidato que oferece
oito backends de isolamento herda a pergunta de integridade em oito formas.

**A2A e hub de MCP e skills.** O README registra suporte a A2A por `A2AAgent` em setembro de 2026, e um
*"MCP & Skill Hub"* que navega hubs de terceiros, verbatim: *"Browse hubs (GitHub MCP Registry, ClawHub),
install into your library, add to a workspace"*. Para o cap. 17 é implementação nova de protocolo; para o
cap. 12 é superfície de supply chain, porque instalar de hub de terceiro na própria biblioteca é
exatamente a cadeia que o *Scanning the Harness* mediu em 27/set.

**Interrupção e retomada no loop.** O README promete *"realtime interruption & resume"*. Em 17/out eu
registrei que uma chamada interrompida no meio da verificação de permissão do Claude Code era relatada ao
modelo **como recusada pelo usuário**. Interromper e retomar durante a decisão é a superfície exata do
defeito, e aqui é recurso anunciado.

**Multi-tenancy com sessão isolada.** Em 7/out, dois advisories do n8n mostraram aprovação pendente
sequestrada entre usuários e aprovação forjada por desvio de HMAC, num serviço de agentes multi-tenant. O
Agent Service do AgentScope tem a mesma forma de superfície.

## 5. Descartes e ⏳

| Alegação | Motivo |
|---|---|
| Que `modelscope/agentscope` tenha sido renomeado para `agentscope-ai/agentscope` | ⏳ **Compatível, não provado.** O manifesto nomeia o segundo; o `raw` serve igual nos dois; os 787 commits admitem a hipótese de repositório novo |
| Linguagem e data do último commit pela página | **Não visíveis** na leitura: a seção de linguagens veio sem dados e não havia data de commit. Linguagem afirmada pelo `requires-python` do manifesto |
| Número de releases e tag mais recente | **Não visíveis** na página lida |
| Que 360 issues e 287 PRs sejam todos abertos | **Caveat registrado**: são os números das abas, que não diziam explicitamente *open* |
| Mecanismo do `bypass mode` | ⏳ **Não lido.** Afirmado pelo README, código não aberto |
| Conteúdo de `_decision.py`, `_engine.py` e `_rule.py` | ⏳ **Não lidos.** Sei os nomes exportados, não o comportamento |
| Como o `TracingMiddleware` é montado e quem pode removê-lo | ⏳ **Não lido.** A pergunta fica registrada sem veredito |
| Os dois papers do AgentScope | ⏳ **Não lidos.** Só os identificadores, da seção *Publications* |
| Camada **Agent Service** | **Não avaliada.** É a razão da recomendação com prazo na seção 3 |
| Comparação de nota com os quatro frameworks do corpus | **Não feita, e não deve ser feita** sem o `FRAMEWORK_EVAL.md` aplicado por leitura de código |

## 6. O que eu faria em seguida, se o editor aprovar a entrada

1. Aplicar o `benchmark/template/FRAMEWORK_EVAL.md` por leitura de código, começando por
   `permission/_engine.py` e `permission/_rule.py`, que é onde o cap. 07 tem mais a ganhar.
2. Ler os dois papers, porque o de 2024 antecede quase todo o corpus e pode mudar a seção de linhagem do
   cap. 01 §3.
3. Decidir o arquétipo, que é decisão do editor, e registrar a **linha** e o **canal** na ficha, pelas
   lições de 20 e 22/out.
4. Fixar a foto: fork e commit, como as quinze fichas existentes fazem, porque sem isso a avaliação não
   tem data de corte.
