# Plano — Cap. 09 (Planejamento)

## Fonte-base (código, reunida)
- Rodada 1: opencode (agente `plan` + `plan_exit` escreve arquivo), gemini-cli (`ApprovalMode.PLAN` + `getApprovedPlanPath` gatekeepa + **tracker** com dependências/grafo), OpenHarness (`EnterPlanModeTool` = enum de permissão; `TODO.md`).
- Rodada 2: OpenClaw ⭐ (quatro camadas: `update_plan` tático + **Goals** durável + **Task Flow** + standing orders); Codex (`update_plan` checklist na TUI); Goose (recipes + todo); Aider (`/ask`,`/architect`,`/context`; split architect→editor); Hermes (todo + Kanban); n8n (Plan-and-Execute **depreciado**, convergiu para Tools Agent/ReAct implícito); IronClaw (sem decomposição de 1ª classe; forte em planejamento temporal); OpenHands (planner tab, nota 1); ohmo (herdado, assume TUI).

## Pesquisa (em andamento → verificar)
- Científico: confirmar survey 2402.02716, PLANET 2504.14773, Beyond Entangled 2601.07577; + ReAct, Plan-and-Solve, Tree of Thoughts, decomposição hierárquica.
- Indústria: plan mode (Claude Code), todo/TodoWrite, the think tool, spec-driven (GitHub Spec Kit, Kiro).

## Tradução em decisões (corpo)
1. **Read-only imposto, não pedido** — plan mode como caso do sistema de permissões (a descoberta da rodada 1 persiste).
2. **ReAct vs plan-then-execute** — o sinal do n8n (Plan-and-Execute depreciado) instancia o achado científico: intercalar razão+ação vence plan-then-execute quando o ambiente é imprevisível; o plano explícito volta para trabalho longo/humano-no-loop.
3. **Tático × durável** — a contribuição do OpenClaw (Goals/Task Flow) preenche a lacuna dos harnesses de código: plano da tarefa (efêmero) × objetivo da sessão (durável).
4. **Decomposição com dependências** — a fronteira aberta (tracker do gemini-cli; Task Flow do OpenClaw).
5. **Dado do livro vivo**: planejamento é a dimensão mais fraca em todas as rodadas — registrar (liga ao registro de expiração "plan mode imposto", 🔵 aberta).

## Passos
1. Escrever `09-planejamento.md` v3. 2. Atualizar `bibliografia.md`. 3. Build (link-check verde). 4. Commit na branch 003.
