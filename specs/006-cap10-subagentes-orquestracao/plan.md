# Plano — Cap. 10 (Subagentes e Orquestração)

## Fonte-base (código, reunida)
- Rodada 1: opencode (tool `task` → sessão-filha, permissões derivadas, depth 1), gemini-cli (`invoke_agent` + registry, contratos de terminação, **A2A** client+server), OpenHarness (**Swarm**: times persistentes, mailbox, worktree git por membro, permission_sync).
- Rodada 2: Codex (`multi_agents_v2` spawn/send/interrupt, ~100 perfis TOML, **agent-graph-store** persistido, hooks SubagentStart/Stop); OpenClaw (`sessions_spawn` push-based, nesting 1–5, política de tools **degradada por profundidade**, **ACP** para harnesses externos); Hermes (`delegate_task` + **Kanban dispatcher** com handoffs); Goose (`summon`, **SubRecipes** hierárquicos, extensão `orchestrator` lead/worker); Aider (split architect→editor, depth 1); IronClaw (child-runs elegantes mas **`spawn_subagent` deny-filtrado em prod**); n8n (agente-como-tool inline, ToolWorkflow); OpenHands (SDK subagent + AgentProfiles + perfis **ACP** orquestrando Claude Code/Codex/Gemini); ohmo (Agent/Task/Team/SendMessage herdados).

## Pesquisa (em andamento → verificar)
- Científico: AutoGen, MetaGPT (SOPs), CAMEL, ChatDev, surveys de MAS, estudos de falha (MAST / "Why Do Multi-Agent LLM Systems Fail?").
- Indústria: Claude Code subagents; multi-agent research system (Anthropic) × "Don't Build Multi-Agents" (Cognition); frameworks (Agents SDK/Swarm, CrewAI, LangGraph supervisor, AutoGen, ADK); A2A/ACP.

## Tradução em decisões (corpo)
1. **Três filosofias** (ferramenta/serviço/colega) — a moldura da rodada 1 persiste.
2. **Isolamento de contexto é o ganho primário** — o subagente lê muito e devolve pouco; worktree git isola edições paralelas (Beyond Entangled Planning, cap. 09, dá o fundamento: contexto escopado).
3. **A tensão central** — Anthropic (orchestrator-worker, +90% em pesquisa a ~15× tokens) × Cognition (não paralelize; planejar = coerência de contexto). Decompor-e-paralelizar é gate de custo/benefício.
4. **Falha de MAS** — a literatura de failure modes justifica os guardrails (depth, terminação, permissões degradadas); IronClaw deny-filtrar em prod é a expressão extrema.
5. **A virada A2A/ACP** — orquestrar harnesses de vendors diferentes como subagentes (gemini-cli A2A, OpenClaw/OpenHands ACP) — liga ao cap. 17.

## Passos
1. Escrever `10-subagentes-orquestracao.md` v3. 2. Atualizar `bibliografia.md`. 3. Build. 4. Commit na branch 003.
