# Comparativo Consolidado — Rodadas 1, 2, ext-1, ext-2 e ext-4

> 16 harnesses avaliados por leitura sistemática de código, 12 dimensões (0–3) + 2 suplementares. Rodada 1: 2026-07-24 (opencode, gemini-cli, OpenHarness). Rodada 2: 2026-07-24 (Codex CLI, Goose, Aider, OpenHands, OpenClaw, Hermes, IronClaw, n8n). Rodada **ext-1**: 2026-07-31 (**Grok Build**, **Pi**). Rodada **ext-2**: 2026-08-02 (**Kimi Code**, **QM** — este inaugurando a categoria *agentes organizacionais*). Rodada **ext-3**: 2026-08-02 (**Traycer** — avaliado e **não incluído**). Rodada **ext-4**: 2026-08-06 (**Prime Agent**). Ver [metodologia](README.md).

<div data-viz="benchmark-codigo"></div>

## Categoria: harnesses de código

| # | Dimensão | opencode | gemini-cli | OpenHarness | **Codex CLI** | **Goose** | **Aider** | **OpenHands*** | **Grok Build** | **Pi** | **Kimi Code** | **Prime Agent** |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Loop | 3 | 3 | 2 | 3 | 3 | 2 | 2 | 3 | 3 | 3 | 3 |
| 2 | Contexto | 3 | 3 | 2 | 3 | 3 | **3** | 3 | 3 | 3 | 3 | 3 |
| 3 | Compactação | 3 | 3 | 3 | 3 | 3 | 2 | 2 | 3 | **3⭐** | 3 | 3 |
| 4 | Ferramentas | 2 | 3 | 3 | 3 | 3 | 3 | 2 | 3 | 3 | 3 | 3 |
| 5 | MCP | 3 | 3 | 2 | 3 | 3 | **0** | 3 | 3 | **0** | 2 | 2 |
| 6 | Permissões/sandbox | 2 | 3 | 2 | **3⭐** | 2 | 2 | 3 | **3⭐** | 1 | 2 | **1** |
| 7 | Memória/estado | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 2 | 3 |
| 8 | Planejamento | 2 | 3 | 2 | 2 | 2 | 2 | 1 | 3 | 1 | 3 | 2 |
| 9 | Subagentes | 2 | 3 | 3 | 3 | 3 | 2 | 2 | **3⭐** | 1 | 3 | **3⭐** |
| 10 | Verificação/evals | 2 | 3 | 2 | 3 | 3 | 3 | 0* | 2 | 3 | 2 | 2 |
| 11 | Extensibilidade | 3 | 3 | 3 | 3 | 3 | 3 | 3 | **3⭐** | **3⭐** | 3 | 3 |
| 12 | Interfaces | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | **3⭐** | 3 |
| | **Total** | **31** | **36** | **29** | **35** | **34** | **28** | **27*** | **35** | **26** | **32** | **31** |
| 13 | **Aprendizado** (supl.) | — | 3 | — | — | — | — | — | — | 2 | 1 | **3⭐** |

\* OpenHands: o repo avaliado é o control-plane (Agent Canvas); o núcleo (loop, condenser, evals SWE-bench) migrou para `software-agent-sdk` — o total subestima o projeto completo. O SDK entra na fila.

**Leitura da rodada ext-1 (2026-07-31):**
1. **Os extremos do espectro chegaram juntos.** O Grok Build (35) empata com o Codex CLI cobrindo tudo com profundidade industrial — inclusive lendo os artefatos dos concorrentes (AGENTS/CLAUDE/Cursor/`.mcp.json`) e portando as tools do codex e do opencode. O Pi (26) pontua 3 em **tudo que aceita** e 0–1 em tudo que recusa por manifesto — o perfil serrilhado não é imaturidade, é tese ("adapt pi to your workflows, not the other way around"), e cada exclusão existe como extensão de exemplo testada.
2. **A dimensão 6 continua separando produto de projeto** — e o Grok Build sobe a régua: autorização de shell por **AST** (tree-sitter-bash), fecho do bypass `mv secret x && cat x`, sandbox kernel-enforced fail-closed. O Pi é o contraexemplo deliberado (1): terceiriza o boundary ao SO e argumenta que sandbox in-process é teatro.
3. **Evals comportamentais seguem sendo o gap mais comum** — o Grok Build tem 26k testes de mecanismo e zero de competência (nota 10 = 2); o Pi, na contramão, é o único da rodada com bancada de A/B de configurações de harness (`evalHarnessTable`) e artefatos de eval no formato nativo de sessão.

**Leitura da rodada ext-2 (2026-08-02):**
1. **O segundo vendor verticalizado confirma o padrão — e a divergência.** O Kimi Code (32) repete o movimento do Grok Build (modelo próprio → harness próprio, aberto), mas com aposta oposta: onde o xAI foi a plataforma máxima em Rust com sandbox kernel-enforced, a Moonshot foi de **autonomia estruturada** — goal mode com máquina de estados e budgets (turns/tokens/tempo), swarm de até 128 subagentes, cron exposto ao modelo — sobre enforcement fraco (sem sandbox de SO; bash autorizado por glob de string no engine em produção, com o parser AST pronto mas só no v2 experimental). O detalhe que nenhum outro tem: **co-design harness↔API** — a API do Kimi ganhou a capability `dynamically_loaded_tools` para servir a *progressive tool disclosure* do harness, com degradação documentada para outros provedores. O vendor mudou o modelo para servir o harness.
2. **Polinização cruzada dentro do corpus virou rotina**: a TUI do Kimi Code é um fork vendorizado da `pi-tui` (agradecimento no README); o QM traz Pi, OpenCode, Codex e Claude Code como *motores* plugáveis. O corpus deixou de ser uma lista de concorrentes e virou uma cadeia de suprimentos.
3. **Evals comportamentais seguem sendo o divisor** também na ext-2: o Kimi Code tem 1.137 arquivos de teste de mecanismo e zero evals de competência; o QM, na contramão, roda **E2E multiplayer contra Slack real com juiz LLM** — a implementação mais completa da dimensão 10 fora do gemini-cli.

**Leitura da rodada ext-4 (2026-08-06):**
1. **O anúncio e o código discordam — e o código venceu.** O lançamento afirma que *"fixed tool-calling schemas and context compaction force the model to work around its own scaffolding"*. Na leitura, a compactação **não foi eliminada nem enfraquecida**: as 1.398 linhas de `core/compaction/` herdadas do Pi continuam lá, com corte seguro, split turns e recuperação reativa de overflow — e ainda **melhoradas** (instruções customizadas, recálculo de `tokensBefore`). O que mudou é a **subordinação**: `compact.run()`/`compact.status()` viraram chamáveis pelo agente, com handler que **agenda em vez de executar** (executar abortaria a célula que pediu), rodando mesmo com auto-compaction desligada, sob 12 testes. A Leitura executiva do cap. 04 **não cai — ganha ressalva**: compactação deixou de ser evento involuntário do harness e virou um de vários mecanismos contra o crescimento de contexto, além de virar gatilho de destilação (`autoRefine.compact: true` por padrão).
2. **O Pi virou substrato do corpus.** O Prime Agent é o **Pi por baixo** — mesmos quatro pacotes (`pi-agent-core`, `pi-ai`, `pi-coding-agent`, `pi-tui`), LICENSE com dupla titularidade (Mario Zechner + Prime Intellect). É o **quinto** consumidor do Pi no mapa da cadeia de suprimentos, e o mais radical: colapsou o *tool set* inteiro num **único tool `ipython`** e construiu por cima o REPL como superfície de programa. A ironia fecha o argumento do cap. 12: o sistema de **menor nota do corpus** (Pi, 26) — que recusa metade das dimensões por manifesto — foi a base escolhida por um laboratório de fronteira. A extensibilidade do Pi recebeu sua validação empírica mais forte.
3. **A dimensão 13 tem um novo teto — e a 10 um novo piso.** O *Continual Harness* dá ao agente **CRUD do próprio estado** (prompt, memória, skill, spec de subagente) com escopo local/global, review gate a cada 25 turnos e rollback por snapshot: supera o Hermes e vira a referência da dimensão 13. Mas a **assimetria tese↔medição é gritante**: o repositório **não contém nenhum eval** — o `packages/evals` do Pi *desapareceu no fork* —, o `expectedOutcome` que o próprio `/refine` emite não é validado por nada, e a alegação de 95,5% no ARC-AGI-3 não tem artefato reprodutível no código. Um harness que se auto-modifica sem bancada de medição é a combinação mais arriscada que o benchmark já registrou.
4. **Regressões herdadas para baixo.** Além dos evals, o **Project Trust do Pi foi removido** (grep por `trust` em `src/` → nada) e o tool único é execução de Python arbitrário, com filhos herdando cwd e permissões — daí o **1** na dimensão 6, abaixo do já baixo piso do Pi.

## Categoria: agentes organizacionais *(nova na ext-2)*

| # | Dimensão | **QM** |
|---|---|:---:|
| 1 | Loop | 3 |
| 2 | Contexto | **3⭐** |
| 3 | Compactação | 3 |
| 4 | Ferramentas | 3 |
| 5 | MCP | 1 |
| 6 | Permissões/sandbox | 3 |
| 7 | Memória/estado | 3 |
| 8 | Planejamento | 1 |
| 9 | Subagentes | 2 |
| 10 | Verificação/evals | **3⭐** |
| 11 | Extensibilidade | 3 |
| 12 | Interfaces | 3 |
| | **Total (1–12)** | **31** |
| 13 | **Aprendizado** (supl.) | 2 |
| 14 | **Proatividade** (supl.) | **3⭐** |

O QM (Y Combinator) inaugura a categoria: o primeiro harness do corpus em que a unidade de design é a **organização**, não a sessão de um usuário — escopos (pessoa/time/sala/org), contexto filtrado por *entitlement* de toda a audiência presente (`context-filter.ts`), consentimento de destinatário para entregas autônomas e auditoria como primitivas do core. O loop do agente é uma **dependência trocável** (Pi, OpenCode, Codex ou Claude Code por configuração), com a sessão portável entre motores via "fita" re-semeável. É a tese da commoditização do loop escrita em `package.json` — e a razão de a categoria ser nova: nas dimensões clássicas ele pontua como um harness maduro (31/36), mas o que o define não cabe nelas.

## Categoria: agentes pessoais self-hosted

| # | Dimensão | **OpenClaw** | **Hermes** | **IronClaw** | **ohmo¹** |
|---|---|:---:|:---:|:---:|:---:|
| 1–5 | Loop/Contexto/Compact./Tools/MCP | 3,3,3,3,3 | 3,3,3,3,3 | 3,3,3,3,3 | 3,3,3,3,3 |
| 6 | Permissões/sandbox | 3 | 3 | **3⭐⭐** | 2 |
| 7 | Memória/estado | 3 | 3 | 3 | 3 |
| 8 | Planejamento | 3 | 2 | 2 | 2 |
| 9 | Subagentes | 3 | 3 | 2² | 3 |
| 10 | Verificação/evals | 3 | 3 | 3 | 3 |
| 11 | Extensibilidade | 3 | 3 | 3 | 3 |
| 12 | Interfaces | 3 | 3 | 3 | 3 |
| | **Total (1–12)** | **36** | **35** | **34** | **34** |
| 13 | **Aprendizado** (supl.) | 1 | **3⭐⭐** | 2 | 2 |
| 14 | **Proatividade** (supl.) | 3 | 2 | 3 | 3 |

¹ avaliação dedicada (2026-07-24) do app pessoal do OpenHarness — gap concentrado na dim. 6 (config de permissão/sandbox do gateway é código morto; sem dial entre nega-tudo e full_auto). ² design nota-3, mas `spawn_subagent` está desabilitado em produção.

## Categoria: harnesses embutidos

| n8n (nó AI Agent) | Total 1–12: **29/36** | Fortes: tools 3 (`$fromAI`→Zod sobre 400+ integrações), MCP 3 (client+server), memória 3, subagentes 3, interfaces 3 · Fracas **por design do ambiente**: compactação 1, planejamento 1, contexto 2, permissões 2 (estrutural/topológica) |
|---|---|---|

## Categoria: frameworks de harness (rodada frameworks-1, template FRAMEWORK_EVAL)

| Eixo | **LangGraph** | **OpenAI Agents SDK** | **CrewAI** | **software-agent-sdk** |
|---|:---:|:---:|:---:|:---:|
| A1 Loop/orquestração | 3 | 3 | 3 | 3 |
| A2 Estado/durabilidade | **3⭐⭐** | 3 | 3 | 3 |
| A3 Tools/schemas | 2 | 3 | 3 | 3 |
| A4 Multi-agente | 2 | 3 | 3 | 3 |
| A5 Human-in-the-loop | 3 | **3⭐** | 3 | 3 |
| A6 Streaming/eventos | 3 | 3 | 3 | 3 |
| **Total A (0–18)** | **16** | **18** | **18** | **18** |
| D1 Observabilidade | 2 | 2 | 2 | 2 |
| D2 Testes/evals | 3 | 3 | 3 | 3 |
| D3 Ergonomia | 2 | 3 | 3 | 3 |
| D4 Ecossistema | 3 | 3 | 3 | 3 |
| **Total D (0–12)** | **10** | **11** | **11** | **11** |

**Leitura da rodada frameworks-1:**
1. **As primitivas viraram commodity** (A quase todo 3) — a diferenciação real está nos eixos B (fronteiras) e C (protocolos), que são descritivos: LangGraph impõe BSP e deixa contexto/permissões totalmente abertos; Agents SDK impõe o vocabulário Responses; CrewAI impõe a ontologia papel/tarefa; o SDK da OpenHands impõe o modelo de eventos inteiro.
2. **Nenhum framework tem observabilidade aberta first-class** (D1=2 em todos): cada um gravita para sua plataforma (LangSmith, OpenAI, AMP, Laminar) — o espaço do "OTel de agentes" segue vago.
3. **Protocolos separam os campos**: CrewAI (MCP obrigatório + **A2A client/server** + skills + AGENTS.md auto-gerado) e software-agent-sdk (MCP OAuth + **ACP** + agentskills) são os poliglotas; o Agents SDK fala só MCP; **LangGraph fala zero** — protocolos são feature do servidor pago.
4. **A previsão dos "dois movimentos" confirmou-se no código**: o software-agent-sdk é o harness-virando-framework mais avançado (tudo virou ABC plugável, e seu `ACPAgent` orquestra Claude Code/Gemini/Codex como motores); o LangGraph faz o movimento oposto — **esvaziando-se** da camada de agente (create_react_agent deprecado rumo ao pacote langchain) para ser só runtime durável.
5. **Compactação continua sendo a linha divisória harness/framework**: só o software-agent-sdk a entrega pronta (condenser com tombstones — o melhor medido no benchmark inteiro); LangGraph/Agents SDK/CrewAI deixam a janela de contexto por conta do usuário (Agents SDK tem apenas uma session de compactação; CrewAI nada).

## Leitura executiva da rodada 2

**As hipóteses registradas na rodada 1 foram confrontadas — 3 confirmadas, 1 surpresa:**

1. ✅ **Codex CLI = novo teto em contenção** (35/36): Seatbelt + bubblewrap/seccomp + Landlock + execpolicy Starlark + network-proxy — três camadas independentes. O gemini-cli deixa de ser o único "3 de referência" na dimensão 6.
2. ✅ **Goose = MCP-nativo confirmado** (34/36): até as tools internas são servidores MCP reais servidos in-process. O empate técnico Codex/Goose/gemini-cli no topo da categoria código indica que a fronteira de produto está convergindo.
3. ✅ **Aider = o caminho alternativo em contexto** (28/36): repo-map (tree-sitter + PageRank) é referência em entrega de contexto sem loop de agente — e o primeiro **0** do benchmark (MCP) mostra o custo da filosofia.
4. ⚠️ **OpenHands = surpresa metodológica** (27/36*): o repo virou control-plane; o núcleo está num SDK externo. Lição: a unidade de avaliação precisa acompanhar a decomposição dos projetos.

**A categoria agentes pessoais estreou com nível inesperadamente alto**: OpenClaw (36) é o "gemini-cli da categoria"; Hermes (35) traz a única implementação fechada de **aprendizado auto-evolutivo** (dimensão 13 promovida a suplementar do template por causa dele); IronClaw (34) redefine o teto conceitual de segurança — o loop estruturalmente incapaz de agir sem o kernel (trust class inforjável por tipos, aprovações como leases por invocação, WASM fail-closed) — algo que **nenhum harness de código avaliado tem**.

**O harness embutido confirmou a tese da categoria**: as dimensões fracas do n8n são exatamente as que o motor de workflow dispensa (execuções curtas → sem compactação; o plano é o grafo desenhado; permissão é topologia). E a V3 revelou movimento inverso ao esperado: o n8n está *reinternalizando* o loop de execução do LangChain para o próprio engine.

## Campeões por dimensão (geral, rodadas 1+2)

| Dimensão | Referência atual | Menção |
|---|---|---|
| Loop | IronClaw (loop ≠ perímetro de segurança) | opencode (durabilidade), gemini-cli (next-speaker) |
| Contexto | Aider (repo-map) e opencode (epochs) | Codex (server-driven por modelo), Hermes (3 camadas cache-aware) |
| Compactação | Codex (remota v2) e Goose (3 técnicas) | IronClaw (circuit-breaker de efetividade) |
| Ferramentas | Goose (MCP-uniforme) e IronClaw (capabilities tipadas) | n8n (`$fromAI`), Aider (edit formats por eval) |
| MCP | Codex e OpenClaw (client+server completos) | Goose (in-process) |
| **Permissões/sandbox** | **IronClaw** (kernel de autoridade) | Codex (3 camadas de SO), OpenClaw (pairing) |
| Memória | Hermes (multicamada + FTS5) | gemini-cli (git checkpoint), OpenClaw (Dreaming) |
| Planejamento | gemini-cli e OpenClaw (goals/task flow) | — dimensão mais fraca da indústria inteira |
| Subagentes | OpenClaw (push-based + ACP de terceiros) | Codex (graph store), OpenHarness (swarm) |
| Verificação | gemini-cli (4 suítes) e IronClaw (isolamento cross-tenant) | Aider (benchmark guiando design), Goose (leaderboard) |
| Extensibilidade | empate amplo — virou commodity | OpenClaw (ClawHub c/ scan), Goose (providers JSON) |
| Interfaces | OpenClaw (23 canais + voz + apps) | Codex (1 core → CLI/IDE/desktop/cloud) |
| **Aprendizado (13)** | **Hermes** (autônomo) e **gemini-cli** (inbox humana) — dois designs nível 3 | IronClaw (extração automática) |
| **Proatividade (14)** | OpenClaw (heartbeat c/ contexto leve) | IronClaw (routines engine) |

## Achados transversais da rodada 2

1. **Planejamento é a dimensão mais fraca da indústria**: nenhum harness novo atingiu 3; a média geral da dimensão 8 é a menor do benchmark. Todo mundo tem todo-list; quase ninguém tem plan→approve→execute imposto.
2. **MCP client+server virou o padrão dos maduros**: Codex, OpenClaw, Hermes, OpenHands, n8n e IronClaw expõem-se como servidores — na rodada 1, nenhum dos três fazia isso no core. O harness como *serviço consumível* consolidou em meses.
3. **ACP emergiu como protocolo de orquestração de harnesses**: OpenClaw, OpenHands e Goose orquestram/integram outros harnesses (Claude Code, Codex, Gemini CLI, opencode) via ACP — a predição do cap. 14 sobre "agente-como-serviço" se confirmou por outra via.
4. **A cláusula de expiração ganhou um caso invertido**: o learning loop do Hermes não espera o modelo melhorar — o par modelo+harness escreve o próprio scaffolding (skills). Auto-expansão em vez de expiração.
5. **Segurança tem agora dois paradigmas distintos**: contenção por SO (Codex — o processo não consegue) e arquitetura de autoridade (IronClaw — o loop não alcança). São complementares, e nenhum harness combina os dois ainda.

## Próximos passos registrados

- **Reavaliações retroativas**: dimensão 13 nos harnesses da rodada 1 (o `skill-extraction-agent` do gemini-cli é candidato a 2); ohmo como entrada dedicada na categoria pessoal.
- **Fila**: `OpenHands/software-agent-sdk` (o núcleo que faltou), frameworks (LangGraph, CrewAI, Agents SDK — template adaptado), Cline/Roo (IDE), mini-swe-agent (harness mínimo), Crush, smolagents.
- **Evolução metodológica**: do estático ao comportamental — rodar os harnesses em tarefas padronizadas (o Harbor do Goose e o Benchmark Pack do OpenClaw são modelos a estudar).
