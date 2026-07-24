# HARNESS_EVAL — Hermes Agent (Nous Research)

## Metadados

- **Repositório / versão avaliada:** github.com/NousResearch/hermes-agent · snapshot 2026-07 (fork GHDaru/hermes-agent, commit 55ef425)
- **Linguagem / stack:** Python (codebase grande: `conversation_loop.py` ~6.5k linhas, `cli.py` ~16.6k, 69 skills empacotadas)
- **Licença:** MIT
- **Data da avaliação:** 2026-07-24 (rodada 2) · **Categoria:** agentes pessoais self-hosted
- **Posicionamento declarado:** agente pessoal self-hosted com loop de aprendizado embutido ("the only agent with a built-in learning loop")
- **Arquétipo observado:** o agente que aprende — o loop auto-evolutivo de skills é o pilar arquitetural, e se confirma integralmente no código

## Dimensões (resumo com evidência)

### 1. Loop do agente — Nota: 3
`agent/conversation_loop.py` com fases separadas (turn_context/tool_executor/turn_finalizer); `iteration_budget`; streaming de output de tools; **interrupt-and-redirect** (`/steer` drenado pré-API e pós-tool); recuperação de respostas vazias com nudges sintéticos; reparo de alternância de papéis; sanitização de tool-calls corrompidos. Loop maduro e defensivo.

### 2. Entrega de contexto — Nota: 3
System prompt em **três camadas explícitas para maximizar prefix-cache**: `stable` (identidade `SOUL.md` + guidance + índice de skills), `context` (`AGENTS.md`/`.cursorrules` do projeto) e `volatile` (memória, `USER.md`, timestamp). Persona migrável do OpenClaw.

### 3. Compactação — Nota: 3
`ContextEngine` plugável (`should_compact`/`compress`/`prune`) + `trajectory_compressor.py` (~1.6k linhas); sumarização de tool-responses antigas via modelo auxiliar barato (default Gemini Flash, até 50 requisições concorrentes); `/compress` manual, `/usage` e `/insights`.

### 4. Design de ferramentas — Nota: 3
~40+ tools em **toolsets componíveis** (`toolsets.py`) com posturas dinâmicas (coding/acp/api-server) selecionando subconjuntos; `execute_code` (Python chamando tools via RPC — colapsa pipelines em turnos de custo-zero-contexto); browser completo, mídia, Home Assistant, Spotify; `schema_sanitizer` normalizando schemas por provider.

### 5. MCP — Nota: 3
**Cliente E servidor**: cliente com stdio/StreamableHTTP/SSE, OAuth, timeouts por servidor, **sampling** (servidor pode requisitar completions) e paralelismo opt-in por servidor; `mcp_serve.py` expõe o Hermes a outros hosts MCP.

### 6. Permissões e sandboxing — Nota: 3
Aprovação de comandos perigosos com detecção + allowlist (`tools/approval.py`), callbacks por-thread; **seis backends de terminal com isolamento** (local, Docker, SSH, Singularity, **Modal**, **Daytona** — sandboxes cloud); subagentes com `_subagent_auto_deny` como default seguro; `path_security.py` anti-traversal; egress isolation documentado.

### 7. Memória e estado — Nota: 3
Multicamada: `MEMORY.md` (notas do agente) + `USER.md` (perfil do usuário) editados por tool única com **nudges periódicos** (a cada 10 turnos); provedores externos plugáveis (**Honcho**, mem0, supermemory); e **`session_search`** — índice FTS5 sobre o SQLite de sessões com três modos (discovery/BM25, recall janelado, sumarização por LLM) para recall cross-session.

### 8. Planejamento — Nota: 2
Tool `todo` + orçamento de iterações + sistema Kanban para coordenação multi-agente com specs. Sem planner formal separado do loop.

### 9. Subagentes / orquestração — Nota: 3
`delegate_task` spawna `AIAgent` filhos com contexto isolado e aprovação não-interativa segura; **Kanban dispatcher** no gateway spawna workers com handoffs estruturados, bloqueio para input humano e heartbeat em operações longas.

### 10. Verificação / evals — Nota: 3
32 subdiretórios de teste; **verify-on-stop nudge** (o agente é forçado a verificar antes de parar, com `verification_evidence.py` rastreando evidência); `batch_runner.py` (trajetórias em lote) e `mini_swe_runner.py` (avaliação estilo SWE-bench) — orientação a pesquisa.

### 11. Extensibilidade — Nota: 3
`ProviderProfile` subclassável: **Nous Portal** (300+ modelos sob uma assinatura, OAuth), OpenRouter, endpoint próprio; sistema de plugins (20 diretórios, registry de toolsets, hooks de sessão); adaptadores Anthropic/Bedrock/Codex/ACP.

### 12. Interfaces — Nota: 3
TUI completa; **gateway multi-canal de processo único**: Telegram, Discord, Slack, WhatsApp, Signal, Email, iMessage, QQ, WeChat, Yuanbao — com continuidade cross-plataforma; voz (transcrição + TTS multi-provider); ACP para editores; servidor API OpenAI-compatível.

### 13. Aprendizado / auto-melhoria — Nota: 3 ⭐⭐ (a dimensão que este harness cria; hipótese confirmada em detalhe)
O loop fechado completo, no código:
1. **Gatilho autônomo**: a cada ~10 iterações de tool-calling (`skill_nudge_interval`, `turn_finalizer.py:634`), dispara `_spawn_background_review(review_skills=True)`; gatilho manual via `/learn`.
2. **Decisão**: um **fork isolado do agente** em thread daemon (`background_review.py`) reprocessa a conversa com o prompt curatorial `_SKILL_REVIEW_PROMPT` — instruído a ser ativo ("um passe que não faz nada é aprendizado perdido"), com ordem de preferência (atualizar skill carregada → atualizar umbrella → adicionar arquivo de suporte → só então criar skill nova), sinais (correção de estilo do usuário é sinal first-class) e **anti-padrões explícitos** (não capturar falhas de ambiente, claims negativos sobre tools, one-offs). Nomes obrigatoriamente class-level.
3. **Isolamento**: o fork tem whitelist de tools restrita a `memory`+`skills`, `skip_memory`, persistência desligada — para não contaminar a sessão real; herda o system prompt cacheado do pai (prefix-cache, ~26% de redução de custo).
4. **Escrita**: `skill_manage` salva `SKILL.md` compatível com **agentskills.io** em `~/.hermes/skills/<categoria>/<nome>/` (+ `references/`, `templates/`, `scripts/`), com standards hardline (descrição ≤60 chars porque o índice trunca em 60).
5. **Reencontro**: índice compacto de skills **sempre presente no system prompt** (cache LRU + snapshot em disco); carga integral sob demanda via `skill_view`; slash commands `/<skill>`; Skills Hub com quarantine/scan para skills de terceiros.
6. **Manutenção**: `curator.py` roda periodicamente quando idle — pin/archive/consolidate, prune por inatividade (archive aos 90 dias, **nunca deleta**), consolidação por LLM opt-in.

### 14. Proatividade / agendamento (suplementar, categoria) — Nota: 2
Cron scheduler com entrega a qualquer plataforma; Kanban watchers; sem heartbeat contextual do nível do OpenClaw.

## Síntese

| Dimensões 1–12 | **Total: 35/36** + Aprendizado 3 ⭐ | 
|---|---|

- **Perfil/arquétipo:** o primeiro harness avaliado onde a auto-melhoria é arquitetura, não feature — o ciclo captura→curadoria→skill→índice→reuso→manutenção está fechado e protegido contra degeneração (anti-padrões, isolamento do fork, curador).
- **Pontos mais fortes:** o learning loop; memória multicamada (MEMORY/USER + Honcho + FTS5); prompt em camadas cache-aware.
- **Pontos mais fracos:** planejamento leve; heartbeat proativo simples comparado ao OpenClaw.
- **Recurso distintivo:** o prompt curatorial de skills — engenharia de *o que não aprender* tão cuidadosa quanto a de o que aprender.
- **"O que roubar":** o fork isolado com whitelist para meta-tarefas; verify-on-stop nudge; descrição de skill ≤60 chars por design do índice.
- **Cláusula de expiração (invertida):** o learning loop não é prótese de limitação — é o mecanismo pelo qual as *outras* próteses expiram por harness (cada skill aprendida é scaffolding que o par modelo+harness escreveu para si). É a primeira evidência de harness que se auto-expande em vez de esperar o modelo melhorar.
