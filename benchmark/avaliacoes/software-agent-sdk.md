# HARNESS+FRAMEWORK_EVAL — OpenHands Software Agent SDK

> Avaliação dupla: este repositório é ao mesmo tempo **o núcleo de harness que faltava** na avaliação do OpenHands/Canvas (rodada 2) e um **framework** para construir agentes. Os dois placares abaixo.

## Metadados

- **Repositório / versão avaliada:** github.com/OpenHands/software-agent-sdk · v1.37.1 (fork GHDaru, commit 99342c4)
- **Linguagem / stack:** Python — 4 pacotes (sdk 66k LOC, tools 16k, agent-server 24k, workspace) contra **207k LOC de testes** (538 arquivos)
- **Licença:** MIT · **Data:** 2026-07-24 (rodada frameworks-1)
- **Posicionamento:** o motor do OpenHands CLI e Cloud, extraído como SDK (paper arXiv 2511.03690; SWE-bench 77.6 anunciado)

## Parte 1 — Dimensões de harness (completando o OpenHands)

### H1. Loop do agente — 3
A extração foi real, não cosmética: o antigo `AgentController` virou duas peças com contrato explícito — `LocalConversation.run()` (política: parar, confirmar, desistir; stuck detector; orçamento em USD; máquina de estados com `WAITING_FOR_CONFIRMATION`) e `Agent.step()` (mecânica stateless: view → mensagens → LLM → dispatch). O event-stream virou **event log append-only** (um evento = um arquivo JSON) com `View` derivada; erros de LLM são controle de fluxo (context-window exceeded → `CondensationRequest`), hooks `Stop` podem **vetar** o término, e há execução paralela de tool calls.

### H2. Compactação / condenser — 3 ⭐ (possivelmente o melhor subsistema de compactação medido)
`LLMSummarizingCondenser`: esquecimento por **tombstones** sobre o log append-only (auditabilidade completa — nada é mutado); disparo por três razões (REQUEST/TOKENS/EVENTS) com distinção **hard/soft** — o gatilho soft desiste se a condensação violaria o pareamento tool_use/tool_result e tenta no próximo step; o hard cai em `hard_context_reset`. Prompt estruturado preservando IDs exatos de tarefa e estado de código; **invariantes de view como código testável** (`view/properties/`: tool_call_matching, batch_atomicity...) validadas contra LLMs reais. Condensers componíveis em pipeline.

### H3. Tools built-in — 3
Terminal com backends plugáveis (tmux/subprocess/windows, pane pool, sessão persistente), file editor, browser (browser-use), grep/glob, apply_patch, task tracker, delegação — mais builtins do agente (think, finish, invoke_skill, **switch_llm** em conversa viva). Presets por modelo (default/gpt5/gemini/planning): o "harness pronto" em uma linha.

### H4. Evals — 2
O harness SWE-bench **continua fora**: roda por dispatch de CI no repo `OpenHands/evaluation` (o 77.6 é reprodutível pela equipe, não por você). Localmente há o que é bom mas não é benchmark: testes de integração com LLMs reais em três classes (conclusão de tarefa bloqueando release; conformidade comportamental com LLM-judge; stress do condenser) + compliance de API de histórico.

### H5. Segurança / confirmação — 3
Dois eixos ortogonais: **análise de risco** (LLM analyzer + `defense_in_depth/` determinístico com parser AST de shell via tree-sitter detectando composições perigosas como fetch-to-exec, + ensemble) e **política de confirmação** (`AlwaysConfirm`/`NeverConfirm`/`ConfirmRisky` por limiar). A conversa *retorna* ao chamador em `WAITING_FOR_CONFIRMATION` (não bloqueia em `input()`) — utilizável em CLI, web e API. Mascaramento de segredos nos eventos.

**Leitura combinada OpenHands:** Canvas (27/36, rodada 2) + este SDK fecham o quadro — loop 3, compactação 3, tools 3, segurança 3; a única dimensão em que o projeto completo segue abaixo do teto é evals reproduzíveis por terceiros (2).

## Parte 2 — Eixos de framework

### A1–A6 (18/18)
- **A1 Loop como primitiva — 3:** `Conversation(agent, workspace)` + `run()` traz de graça stuck detection, orçamento, métricas, visualizer; e a factory é a primitiva mais forte: trocar `workspace=` roda o **mesmo código** local, em Docker, apptainer ou cloud (`RemoteConversation` com API idêntica). Acima: **Critic/refinamento iterativo**, goal-completion loop e hooks com os 6 eventos do Claude Code (formato de config compatível).
- **A2 Estado/durabilidade — 3:** event-sourcing com retomada por diretório de persistência, `verify()` na retomada, fork de conversa, **compat de estado persistido testada em CI** e benchmarks próprios de latência/replay.
- **A3 Tools/schemas — 3:** contrato Action/Observation/Executor com o detalhe de design mais forte da camada: `Observation.to_llm_content` separa **o que volta ao contexto do modelo** do dado estruturado. Toolsets (um create → várias tools com executor comum), anotações MCP-style, e **ClientToolSpec** (tool executa na máquina do cliente com agente remoto).
- **A4 Multi-agente — 3:** subagentes declarativos em markdown com cadeia de precedência documentada (programático > projeto > usuário > plugin > builtin), builtins prontos (code_explorer, web_researcher...), delegação **paralela** via dict, endpoint REST.
- **A5 HITL — 3:** política + analisador plugáveis, estado explícito, rejeição auditada no log, `send_message()`/`pause()` durante o run.
- **A6 Streaming/eventos — 3:** união discriminada pydantic (serialização polimórfica de graça), ~19 tipos de evento, `visualize()` como parte do contrato do evento, canais separados para eventos e deltas de token, WebSocket/webhooks no server.

### B. Fronteiras — 2
**Impõe muito**: pydantic v2 + união discriminada em toda extensão, o modelo de eventos inteiro, o ciclo de vida de `Conversation` — não é biblioteca que se usa aos pedaços. **Abre muito**: `AgentBase` é substituível de verdade (o `ACPAgent` de 4.154 linhas troca o motor inteiro por Claude Code/Gemini CLI/Codex via ACP), system prompt com escape hatch, condenser/critic/analyzer/policy/store plugáveis. **Lock-in:** litellm como dependência dura (100+ provedores, mas acoplamento total), Chat Completions + Responses, function calling emulado para modelos sem tool calling.

### C. Protocolos — 3
| MCP client | MCP server | A2A | ACP | SKILL.md | AGENTS.md |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✅ fastmcp, 3 transportes, **OAuth completo**, hot-reload de tools | ❌ (só gateway OpenAI-compatible) | ❌ | ✅ **cliente extenso** — usa Claude Code/Gemini/Codex como motor | ✅ conforme spec agentskills.io + marketplace | ✅ convenção `.agents/`+`.openhands/` |

### D. Produção — 11/12
- **D1 Observabilidade — 2:** `@observe` nos pontos quentes com backend OTel genérico ou Laminar; no-op silencioso sem env; redação de segredos. Sem exporter first-class agnóstico documentado no repo.
- **D2 Testes — 3:** 538 arquivos/207k linhas (3,1× o código), stress tests, política anti-mock, e CI de *produto*: **api-breakage**, compat de estado persistido, deprecation-check, exemplos executados de verdade.
- **D3 Ergonomia — 3:** hello world em 29 linhas; preset em 1; 56 exemplos numerados verificados em CI (com checagem de documentação e duplicação).
- **D4 Ecossistema — 3:** sandboxes Docker/Apptainer/Cloud, VSCode server embutido, gateway OpenAI-compatible, plugins de GitHub, binários PyInstaller.

## Síntese

- **Placares:** Harness H **14/15** · Framework A **18/18** · D **11/12**
- **Perfil:** a resposta mais completa à pergunta do capítulo de frameworks — aqui **tudo é framework, exceto o eval**: cada peça de harness (condenser, confirmação, stuck detector, tools) virou ABC plugável, e o mesmo código roda do laptop à cloud trocando um parâmetro.
- **O que roubar:** tombstones + invariantes de view testáveis (compactação); `to_llm_content` separando dado de contexto; a factory local/remoto com API única; CI de api-breakage e de compat de estado persistido.
- **Teste decisivo:** difícil *sem* ele: um agente de código com condensação correta sob APIs reais e confirmação por risco, portável de local para Kubernetes sem mudar código. Difícil *com* ele: qualquer coisa fora do modelo de eventos pydantic — a superfície conceitual imposta é grande.
- **Nota metodológica:** confirma a previsão da nota de frameworks — harnesses estão virando SDKs; este é o caso mais avançado, e o `ACPAgent` fecha o ciclo: o framework que orquestra os harnesses concorrentes como motores intercambiáveis.
