# Comparativo Consolidado — Rodadas 1 e 2

> 11 harnesses avaliados por leitura sistemática de código, 12 dimensões (0–3) + 2 suplementares. Rodada 1: 2026-07-24 (opencode, gemini-cli, OpenHarness). Rodada 2: 2026-07-24 (Codex CLI, Goose, Aider, OpenHands, OpenClaw, Hermes, IronClaw, n8n). Ver [metodologia](README.md).

## Categoria: harnesses de código

| # | Dimensão | opencode | gemini-cli | OpenHarness | **Codex CLI** | **Goose** | **Aider** | **OpenHands*** |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | Loop | 3 | 3 | 2 | 3 | 3 | 2 | 2 |
| 2 | Contexto | 3 | 3 | 2 | 3 | 3 | **3** | 3 |
| 3 | Compactação | 3 | 3 | 3 | 3 | 3 | 2 | 2 |
| 4 | Ferramentas | 2 | 3 | 3 | 3 | 3 | 3 | 2 |
| 5 | MCP | 3 | 3 | 2 | 3 | 3 | **0** | 3 |
| 6 | Permissões/sandbox | 2 | 3 | 2 | **3⭐** | 2 | 2 | 3 |
| 7 | Memória/estado | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 8 | Planejamento | 2 | 3 | 2 | 2 | 2 | 2 | 1 |
| 9 | Subagentes | 2 | 3 | 3 | 3 | 3 | 2 | 2 |
| 10 | Verificação/evals | 2 | 3 | 2 | 3 | 3 | 3 | 0* |
| 11 | Extensibilidade | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 12 | Interfaces | 3 | 3 | 2 | 3 | 3 | 3 | 3 |
| | **Total** | **31** | **36** | **29** | **35** | **34** | **28** | **27*** |

\* OpenHands: o repo avaliado é o control-plane (Agent Canvas); o núcleo (loop, condenser, evals SWE-bench) migrou para `software-agent-sdk` — o total subestima o projeto completo. O SDK entra na fila.

## Categoria: agentes pessoais self-hosted

| # | Dimensão | **OpenClaw** | **Hermes** | **IronClaw** | (ohmo/OpenHarness¹) |
|---|---|:---:|:---:|:---:|:---:|
| 1–5 | Loop/Contexto/Compact./Tools/MCP | 3,3,3,3,3 | 3,3,3,3,3 | 3,3,3,3,3 | — |
| 6 | Permissões/sandbox | 3 | 3 | **3⭐⭐** | — |
| 7 | Memória/estado | 3 | 3 | 3 | — |
| 8 | Planejamento | 3 | 2 | 2 | — |
| 9 | Subagentes | 3 | 3 | 2² | — |
| 10 | Verificação/evals | 3 | 3 | 3 | — |
| 11 | Extensibilidade | 3 | 3 | 3 | — |
| 12 | Interfaces | 3 | 3 | 3 | — |
| | **Total (1–12)** | **36** | **35** | **34** | — |
| 13 | **Aprendizado** (supl.) | 1 | **3⭐⭐** | 2 | — |
| 14 | **Proatividade** (supl.) | 3 | 2 | 3 | — |

¹ o ohmo foi avaliado dentro do OpenHarness (rodada 1) antes da categoria existir; reavaliação dedicada pendente. ² design nota-3, mas `spawn_subagent` está desabilitado em produção.

## Categoria: harnesses embutidos

| n8n (nó AI Agent) | Total 1–12: **29/36** | Fortes: tools 3 (`$fromAI`→Zod sobre 400+ integrações), MCP 3 (client+server), memória 3, subagentes 3, interfaces 3 · Fracas **por design do ambiente**: compactação 1, planejamento 1, contexto 2, permissões 2 (estrutural/topológica) |
|---|---|---|

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
