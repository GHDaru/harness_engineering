# HARNESS_EVAL — ohmo (OpenHarness)

## Metadados

- **Repositório / versão avaliada:** github.com/HKUDS/OpenHarness (diretório `ohmo/`) · v0.1.9 — avaliação dedicada, complementar à do OpenHarness (rodada 1)
- **Linguagem / stack:** Python; app empacotado sobre o engine do OpenHarness (workspace `~/.ohmo/`, gateway multi-canal, memória e backend de sessão próprios)
- **Licença:** MIT · **Data:** 2026-07-24 (retro/rodada 2.5)
- **Categoria:** agentes pessoais self-hosted
- **Arquétipo observado:** o app-sobre-harness — prova de que a fronteira app/engine do OpenHarness foi desenhada (implementa `SessionBackend`, `MemoryCommandBackend` e extra roots como plugins de primeira classe, sem tocar no core)

## Dimensões (nota · origem: próprio/herdado)

### 1. Loop — 3 · herdado + orquestração própria
O loop é o `QueryEngine` do OpenHarness; o que é próprio é o **pool multi-sessão** (`ohmo/gateway/runtime.py`: um `RuntimeBundle` por `session_key`, recriado quando o cwd muda) e a **interrupção real por mensagem nova** (`bridge.py`: cada mensagem é uma asyncio.Task; nova mensagem da mesma sessão cancela a anterior) — poucos concorrentes cancelam corretamente.

### 2. Entrega de contexto — 3 · próprio
`ohmo/prompts.py`: base do OpenHarness → soul.md → identity.md → user.md → BOOTSTRAP.md → workspace → memória, em seções ordenadas. Decisão rigorosa: `include_project_memory=False` em todos os call sites — o agente pessoal **não** carrega CLAUDE.md de projeto (testado). Fraqueza menor: BOOTSTRAP.md nunca é removido automaticamente.

### 3. Compactação — 3 · herdado + UX própria
Herda o sistema sério do OpenHarness (context collapse, retry de prompt-too-long, session memory); o próprio é a tradução de `CompactProgressEvent` em **mensagens humanas bilíngues (pt/en/zh) no canal de chat**, com 4 testes dedicados.

### 4. Ferramentas — 3 · herdado + 1 própria
Herda as ~40 do registry default, sem restrição por canal. Própria: `ohmo_create_feishu_group` — **registrada apenas no turno vindo de `/group`** (rejeição fora do contexto testada), um padrão de tool-scoping por origem que vale documentar.

### 5. MCP — 3 · herdado
Completo via `McpClientManager`; contagem de servidores no estado e resumo exposto ao gateway. Lacuna: sem config MCP própria (`~/.ohmo/mcp.json` não existe) e sem isolamento de MCP por canal/remetente.

### 6. Permissões e sandboxing — 2 ⚠️ · misto — o gap decisivo
**A metade certa existe**: allowlist de contatos **deny-by-default** (lista vazia = nega tudo, logado), políticas de grupo com 4 modos (default `managed_or_mention`), **isolamento de sessão por remetente** (pessoas no mesmo grupo não compartilham a memória do agente — testado exaustivamente), bloqueio de comandos administrativos remotos com opt-in nominal, e os paths sensíveis não-burláveis do OpenHarness. **A metade que falta**: `permission_mode` e `sandbox_enabled` do `gateway.json` são **código morto** (nunca lidos); sem `permission_prompt` no gateway, o modo default **nega duro** toda tool mutante — empurrando o usuário para `full_auto` global (um penhasco, não um dial); sem sandbox por canal/remetente; sem marcação de conteúdo de terceiros como não-confiável; **zero testes de permissão no escopo ohmo**. Conserto de maior alavancagem identificado: rotear `permission_prompt` de volta pelo canal (aprovação assíncrona por reply) e ligar `sandbox_enabled` ao Docker sandbox existente.

### 7. Memória e estado — 3 · próprio
`ohmo/memory.py`: memória pessoal em `~/.ohmo/memory/` com o schema do OpenHarness, mas **file-lock exclusivo, escrita atômica, dedupe por assinatura** (reescreve em vez de duplicar) e **soft-delete** — mais robusto que o típico "append ao markdown" da categoria. Sessões próprias (`OhmoSessionBackend`) com resume por `session_key` — a conversa do Telegram continua de onde parou.

### 8. Planejamento — 2 · herdado sem adaptação
Plan mode/todos existem mas assumem TUI: não há superfície de aprovação de plano num canal de chat, nem persistência de plano no workspace.

### 9. Subagentes — 3 · herdado
Agent/Task/Team/SendMessage tools ativos. Assimetria observada: `/tasks run` é bloqueado remotamente, mas as tools equivalentes seguem disponíveis ao modelo. O `/group` é um caso real: vira prompt de tarefa que o modelo resolve chamando a tool uma vez (loop completo testado).

### 10. Verificação — 3 · próprio
**96 testes adversariais** em `tests/test_ohmo/` (75 só no gateway): sessão não restaura mensagens de outro remetente, `/config show` não vaza segredos, histórico de `/group` sanitizado antes de virar contexto, tail de tool_use pendente descartado no refresh. Lacuna: nenhum teste de permissão/sandbox — exatamente a dimensão fraca.

### 11. Extensibilidade — 3 · próprio
`~/.ohmo/skills` e `~/.ohmo/plugins` como raízes extras coexistindo com as do projeto; plugins carregam tools, slash commands e servidores MCP; skills viram comandos no canal; `channel_configs` arbitrário por canal.

### 12. Interfaces — 3 · próprio
Wizard para **Telegram, Slack, Discord, Feishu** (+6 canais acessíveis via config: WhatsApp, Matrix, DingTalk, QQ, MoChat, e-mail); bridge com streaming de progresso, anexos baixados e imagens inline (com retry textual); TUI React, backend-only e `ohmo --print`; serviço com PID/log/heartbeat e restart auto-notificado no chat.

### 13. Aprendizado (suplementar) — 2 · herdado, bem conectado
O **autodream** do OpenHarness plugado ao workspace pessoal: consolida sessões em memória durável com lock, backup e diff. Limite: auto-edição de soul/identity/user é só convenção de prompt, sem mecanismo.

### 14. Proatividade (suplementar) — 3 · herdado com hooks próprios
Ciclo proativo genuinamente fechado: cron scheduler constrói `ohmo --print <msg>` e o resultado vira **DM no Feishu** (`ohmo/gateway/notify.py`, código próprio) — o agente fala com você sem ser perguntado. O modelo pode agendar via tools de cron. Ressalvas: scheduler é daemon separado; notify só implementado para Feishu.

## Síntese

| Dimensões 1–12 | **Total: 34/36** · Aprendizado 2 · Proatividade 3 |
|---|---|

- **Posição na categoria:** 3º (OpenClaw 36 · Hermes 35 · **ohmo 34** · IronClaw 34) — entrada de topo, e o gap está concentrado numa única dimensão decisiva.
- **Pontos mais fortes:** isolamento de sessão por remetente; memória com rigor de formato; 96 testes adversariais; interrupção por mensagem nova.
- **Ponto mais fraco:** o modelo de confiança "parou no meio do caminho" — ótimo no *quem entra* (pairing/allowlist), incompleto no *o que pode fazer depois de entrar* (sem dial entre nega-tudo e full_auto; config de sandbox morta).
- **Recurso distintivo:** `/group` — o agente cria um grupo Feishu dedicado com binding de repo/cwd: um "espaço de trabalho social" sem equivalente no OpenClaw/Hermes.
- **"O que roubar":** tool registrada só no turno de origem correta (`/group`); interrupção-por-nova-mensagem; progresso de compactação traduzido para o chat.
- **Conserto de maior alavancagem (para o upstream):** rotear aprovação de permissão pelo próprio canal (reply assíncrono) e ligar os campos mortos do `gateway.json` — os dois juntos levariam a dimensão 6 a 3 e o total a 36.
