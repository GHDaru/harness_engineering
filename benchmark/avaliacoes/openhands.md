# HARNESS_EVAL — OpenHands (Agent Canvas)

## Metadados

- **Repositório / versão avaliada:** github.com/All-Hands-AI/OpenHands · snapshot 2026-07 (fork GHDaru/OpenHands, commit 6b04532)
- **Linguagem / stack:** Python (app-server) + React (frontend) + enterprise/SaaS
- **Licença:** MIT
- **Data da avaliação:** 2026-07-24 (rodada 2) · **Categoria:** harnesses de código
- **⚠️ Achado metodológico central:** este repositório **não é mais o monólito clássico** OpenHands/OpenDevin. O núcleo do agente (loop, tools, condenser, evals) **migrou para `OpenHands/software-agent-sdk`** (dependências pinadas `openhands-sdk==1.36.0` etc.); os diretórios clássicos (`agenthub/`, `controller/`, `runtime/`, `evaluation/`) não existem mais aqui. O que este repo contém é o **Agent Canvas**: control-plane, orquestração, persistência, sandboxing, integrações e UI. As notas avaliam **o que está presente neste repo** — avaliar o OpenHands "completo" exigiria também o SDK (candidato para rodada futura).

## Dimensões (resumo com evidência)

### 1. Loop do agente — Nota: 2 (núcleo no SDK)
A hipótese do event-stream confirma-se conceitualmente: `openhands/app_server/event/` persiste cada `Event` como JSON por conversa com paginação, filtros e export de trajetória — mas o loop ação/observação roda no `openhands-agent-server` (SDK). Este repo consome eventos, não os gera.

### 2. Entrega de contexto — Nota: 3
Sistema de skills/microagents multi-escopo raro: `skill_loader.build_org_configs` carrega skills automaticamente de repositórios convencionais **`owner/.openhands` e `owner/.agents`**, varrendo a conta do usuário **e todas as suas organizações** em múltiplos provedores Git (GitHub/GitLab/Azure), com dedup e limites de fan-out. Skills com `KeywordTrigger` e `TaskTrigger` (slash commands), formato agentskills, marketplace com auto-load, hooks via `.openhands/hooks.json`.

### 3. Compactação — Nota: 2 (motor no SDK)
O *condenser* é config de primeira classe (tela dedicada na UI, default organizacional, validação via SDK) — mas o algoritmo vive no SDK.

### 4. Design de ferramentas — Nota: 2
Toolset de execução vem do `openhands-tools` (SDK). O repo define tools próprias **como servidor MCP** (`create_pr`, `create_mr` e variantes Bitbucket/Azure) via FastMCP com schemas declarativos.

### 5. MCP — Nota: 3
Bidirecional: **client** (config MCP por agente com tratamento sofisticado de segredos — redação/restauração em round-trips GET/PUT) e **server** (o app-server É um FastMCP expondo tools de PR aos sandboxes, mais um **proxy MCP para Tavily** que dá busca sem expor a API key). Perfis de agente referenciam subconjuntos de servidores.

### 6. Permissões e sandboxing — Nota: 3
`app_server/sandbox/` (14 arquivos): backends Docker/remoto/processo atrás de abstração; containers por conversa com estratégias de agrupamento (`SandboxGroupingStrategy`), portas para Agent Server/VSCode, autenticação por `SESSION_API_KEY`, segredos criptografados, acesso user-scoped. Isolamento por sessão como fundação do produto — a herança acadêmica (executar código não-confiável de benchmarks) virou arquitetura.

### 7. Memória e estado — Nota: 3
Event store multi-backend (**filesystem, S3, Google Cloud**) com eventos endereçáveis, paginação e export ordenado de trajetória; metadados de conversa em SQL; live-status e tarefas de início persistidas (retomada/auditoria).

### 8. Planejamento — Nota: 1
Aba planner na UI e ganchos; sem subsistema de decomposição de primeira classe neste repo.

### 9. Subagentes / orquestração — Nota: 2
Primitivas do SDK (`openhands.sdk.subagent`) + **AgentProfiles** por organização (cada perfil = LLM profile + servidores MCP), incluindo perfis **ACP** — o Canvas orquestra **Claude Code, Codex e Gemini** como agentes. A tese multi-backend é central; a delegação fina roda no SDK.

### 10. Verificação / evals — Nota: 0 (neste repo)
Hipótese refutada *para este repositório*: o diretório `evaluation/` clássico (harness SWE-bench pelo qual o OpenHands é historicamente referência) migrou para o SDK. Aqui há 115 arquivos de testes unitários do app-server, mas zero evals de agente.

### 11. Extensibilidade — Nota: 3
Marketplaces de skills/plugins (instance/org/personal); LLM profiles + agent profiles; camada de integrações Git plugável (GitHub, GitLab, Bitbucket, Azure DevOps, Forgejo, Jira); agentes de terceiros via ACP; backends de sandbox/event-store trocáveis por injeção de dependências; litellm.

### 12. Interfaces — Nota: 3
Web UI React completa (~40 rotas: conversas, settings, admin, billing, orgs); CLI `agent-canvas`; headless/REST via Agent Server; **resolvers GitHub/GitLab/Jira/Slack** (webhooks e automações); enterprise/SaaS completo (Keycloak, Stripe, multi-tenant); deploy Docker/k8s.

### 13. Aprendizado / auto-melhoria (suplementar) — Nota: 0
Carrega skills de repositórios; não as escreve.

## Síntese

| Dimensões 1–12 | **Total: 27/36** — com asterisco: mede o Canvas, não o OpenHands completo |
|---|---|

- **Perfil/arquétipo:** o harness que virou **plataforma de harnesses** — control-plane multi-tenant que orquestra agentes próprios e de terceiros (via ACP), com o núcleo extraído para SDK reutilizável. É o mesmo movimento do Codex (App Server) e do opencode (V2) levado ao extremo.
- **Pontos mais fortes:** skills organizacionais auto-descobertas (`owner/.openhands` em todas as orgs do usuário); sandbox por conversa multi-backend; event store plugável.
- **Pontos mais fracos:** o repo isolado perde as dimensões-núcleo (loop, evals) — a nota 0 em verificação é artefato da migração, não descaso histórico.
- **Recurso distintivo:** convenção de repositório organizacional de skills — contexto de time versionado em git e carregado automaticamente para todos os membros.
- **"O que roubar":** o repo `.openhands`/`.agents` por organização; proxy MCP para APIs pagas (busca sem expor chave); perfis de agente org-wide.
- **Lição metodológica para o benchmark:** avaliar por repositório tem limites — quando um projeto se decompõe em SDK + control-plane, a unidade de avaliação precisa acompanhar. Registrar `software-agent-sdk` na fila.
