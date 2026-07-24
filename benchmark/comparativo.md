# Comparativo Consolidado — Rodada 1

> Três harnesses avaliados por leitura sistemática de código, 12 dimensões, escala 0–3 (ver [metodologia](README.md)). Data: 2026-07-24. Notas comparáveis apenas dentro desta rodada.

## Tabela de notas

| # | Dimensão | opencode | gemini-cli | OpenHarness |
|---|---|:---:|:---:|:---:|
| 1 | Loop do agente | 3 | 3 | 2 |
| 2 | Entrega de contexto | 3 | 3 | 2 |
| 3 | Compactação | 3 | 3 | 3 |
| 4 | Ferramentas | 2 | 3 | 3 |
| 5 | MCP | 3 | 3 | 2 |
| 6 | Permissões/sandbox | 2 | 3 | 2 |
| 7 | Memória/estado | 3 | 3 | 3 |
| 8 | Planejamento | 2 | 3 | 2 |
| 9 | Subagentes | 2 | 3 | 3 |
| 10 | Verificação/evals | 2 | 3 | 2 |
| 11 | Extensibilidade | 3 | 3 | 3 |
| 12 | Interfaces | 3 | 3 | 2 |
| | **Total (0–36)** | **31** | **36** | **29** |

## Leitura executiva

**gemini-cli** lidera a rodada sem dimensão fraca. Suas vantagens estruturais estão em *controle* (policy engine com parsing de shell + sandbox de SO + trusted folders) e *verificação* (quatro suítes, juiz LLM, baselines nightly) — as duas dimensões mais caras de construir e mais raras no mercado. Nota metodológica: um 36/36 na primeira rodada também mede a régua, não só o harness — espera-se que notas caiam quando entrarem concorrentes fortes por dimensão (Codex CLI em sandbox, Aider em contexto).

**opencode** (31) é o segundo colocado com um perfil claro: referência em *arquitetura de contexto e estado* (Context Epochs, SQLite com eventos replayáveis) e *neutralidade de provedor* (~26 loaders + models.dev). Sua lacuna consequente é uma só: contenção — política de permissões elegante, mas sem sandbox de SO no core.

**OpenHarness** (29) tem o perfil mais irregular — e é o mais valioso por unidade de código para quem quer *aprender*: o port fiel da compactação do Claude Code, a defesa de paths sensíveis indesligável, e a aposta mais ambiciosa da coorte em multi-agente (Swarm: times, mailbox, worktrees). Paga o preço da juventude (v0.1.9) nas dimensões de robustez.

## Campeões por dimensão

| Dimensão | Referência da rodada | Por quê |
|---|---|---|
| Loop | empate opencode/gemini-cli | durabilidade (opencode) vs. next-speaker + anti-loop (gemini) |
| Contexto | empate opencode/gemini-cli | Context Epochs vs. hierarquia com @imports |
| Compactação | empate triplo | convergência total — o padrão está consolidado |
| Ferramentas | gemini-cli / OpenHarness | declarativas por família vs. maior arsenal |
| MCP | opencode | superfície de protocolo mais completa |
| Permissões/sandbox | **gemini-cli** | o único com política + contenção obrigatórias |
| Memória/estado | três campeões parciais | sessão (opencode), workspace (gemini), longo prazo (OpenHarness) |
| Planejamento | **gemini-cli** | read-only imposto + plano persistido + aprovação gatekeeper |
| Subagentes | gemini-cli / OpenHarness | serviço com A2A vs. times com mailbox |
| Verificação | **gemini-cli** | comportamento sob regressão contínua |
| Extensibilidade | empate triplo | profundidade (opencode), empacotamento (gemini), interoperabilidade (OH) |
| Interfaces | opencode / gemini-cli | superfície de produto vs. plataforma (SDK/A2A) |

## O harness ideal (exercício de síntese)

Se pudéssemos montar um harness com o melhor de cada avaliado: o **contexto e estado** do opencode (epochs, eventos replayáveis, prompts por modelo), a **contenção e verificação** do gemini-cli (policy engine, sandbox, evals, checkpoint git), o **multi-agente e a interoperabilidade** do OpenHarness (swarm, formatos portáveis de skill/plugin), e três detalhes baratos: paths sensíveis indesligáveis (OH), paralelismo read-only (OH), truncamento que move para arquivo em vez de descartar (opencode).

## Próxima rodada

Aguardando forks: **Codex CLI** (hipótese: novo teto em permissões/sandbox), **Goose** (hipótese: novo teto em MCP), **Aider** (hipótese: caminho alternativo em contexto — repo-map estático vs. exploração por agente), **OpenHands** (hipótese: novo teto em evals acadêmicos/event-stream). Cada hipótese está registrada aqui para ser confrontada com o código — é assim que o benchmark deixa de ser amador: prevendo antes de medir.
