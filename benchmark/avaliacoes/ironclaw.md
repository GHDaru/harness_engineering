# HARNESS_EVAL — IronClaw (NEAR AI)

## Metadados

- **Repositório / versão avaliada:** github.com/nearai/ironclaw · snapshot 2026-07 (fork GHDaru/ironclaw, commit 073ded0)
- **Linguagem / stack:** Rust — **~1.07 milhão de linhas em 63 crates**; PostgreSQL; WASM (wasmtime) + Docker
- **Licença:** MIT
- **Data da avaliação:** 2026-07-24 (rodada 2) · **Categoria:** agentes pessoais self-hosted (foco: segurança)
- **Posicionamento declarado:** "Agent OS focado em privacidade, segurança e extensibilidade" — reimplementação security-first do OpenClaw (FEATURE_PARITY.md de 90 KB rastreia a paridade)
- **Arquétipo observado:** o harness com **arquitetura de autoridade** — o único avaliado onde o loop é *estruturalmente incapaz* de executar efeitos sem mediação
- **Nota da hipótese:** zero-trust/validação/auditoria confirmados; WASM confirmado; **enclaves/TEE não encontrados no código** (o isolamento é WASM + Docker, não hardware)

## Dimensões (resumo com evidência)

### 1. Loop do agente — Nota: 3
Tese explícita da arquitetura (`crates/Architecture.md`): *"The loop is intentionally not the security perimeter."* O loop é um pipeline de estágios selados (input → prompt → model → capability → gate/checkpoint → stop), cada um uma strategy trait privada; o executor retorna um `LoopExit` contendo **apenas referências duráveis** — nunca muta estado; o `LoopExitApplier` valida evidência host-owned antes de aplicar. Estado resumível por checkpoints; máquina de estados Queued→Running→Blocked→Completed com leases/heartbeats; "one active run per canonical thread".

### 2. Entrega de contexto — Nota: 3
Montagem de prompt como decisão de política: `LoopPromptPort` resolve identidade, contexto pessoal (**opt-in por run profile, não por canal**), skills e segurança; conteúdo prompt-injected/pessoal viaja em **"prompt envelopes" com trust class preservada** — metadados seguros, não conteúdo cru.

### 3. Compactação — Nota: 3
`CompactionStrategy` é política pura (retorna Skip ou o limite de compactação; mutação só no host); orçamento de tokens com `preserve_tail_tokens`; **circuit-breaker de efetividade** (compara estimativa pós-compactação contra baseline para detectar compactações inúteis); variante que preserva a tarefa ativa; o host rejeita compactar através de mensagens não-usuário.

### 4. Design de ferramentas — Nota: 3
Tools são **capabilities com descritores tipados** declarando `EffectKind`, credenciais requeridas, política de rede e estimativas de recurso; separação formal entre *visibilidade* (metadado) e *autoridade* (grant) — invocar capability oculta falha fechado; **obligations** (redação, limites) preparadas antes de qualquer efeito.

### 5. MCP — Nota: 3
`ironclaw_mcp` adapta tools MCP a capabilities **sem conceder autoridade ambiente** a servidores (FS/secrets/rede continuam mediados); Streamable HTTP (protocolo 2025-06-18); injeção de credencial mediada (o servidor nunca vê o secret); recursos contabilizados pelo governor.

### 6. Permissões e sandboxing — Nota: 3 ⭐⭐ (a dimensão central; o novo teto da categoria)
Defense-in-depth em nove camadas, todas host-owned e fail-closed:
(a) **autorização de invocação exata** (`ironclaw_authorization`) — Allow só com autoridade correspondente à capability *e* seus efeitos; (b) **aprovações como leases exatos-por-invocação com fingerprint** (não allowlists amplos), com hard floor de efeitos never-auto-approve; (c) **trust class inforjável por tipo** (`ironclaw_trust`: variantes privilegiadas só construíveis dentro do crate, `#[serde(skip_deserializing)]` impede forjar trust via wire); (d) **WASM sandbox** (wasmtime: fuel 100M instruções, memória 16 MB, rate limit por tool, 4 host functions apenas, egress HTTP negado por default); (e) **process sandbox Docker per-tenant** com regra documentada de bug real (#6170): FS virtual não contém subprocesso — spawns multi-user obrigatoriamente via `TenantSandboxProcessPort`; sem sandbox verificado, a capability shell é **ocultada e rejeitada**, nunca degradada silenciosamente; (f) **secrets zero-exposure** (AES-256-GCM + HKDF por secret; injeção na borda de egress; broker reescreve headers na saída); (g) **rede mediada anti-SSRF** (allowlist revalidada a cada redirect, bloqueio de IPs privados/loopback); (h) **camada safety** (leak detector Aho-Corasick+regex bidirecional, detecção de command injection, redação); (i) **auditoria** com redação re-aplicada antes de qualquer log/evento. E o enforcement é *mecânico*: testes de fronteira de dependência (`ironclaw_architecture`) provam que o loop não alcança os efeitos.

### 7. Memória e estado — Nota: 3
Busca híbrida full-text + vetorial com Reciprocal Rank Fusion; identity files; e o detalhe raro: **prompt-write safety** (`memory/safety.rs`) — documentos protegidos (system prompt, identidade, perfil) têm fronteira de escrita uniforme com política versionada e auditoria, protegendo contra prompt injection que corrompe a identidade do agente.

### 8. Planejamento — Nota: 2
Sem decomposição de tarefas de primeira classe; o "planner" do loop é composição de strategies. Forte em planejamento *temporal* (ver dim. 14).

### 9. Subagentes / orquestração — Nota: 2
Design elegante (subagentes como child-runs no mesmo pipeline, com gates/checkpoints unificados e teste E2E) — **mas `spawn_subagent` está deny-filtrado em todos os profiles de produção** (`TEMP(disable-spawn-subagents)`). A nota reflete a capacidade disponível, não o design (que seria 3).

### 10. Verificação / evals — Nota: 3
~415 arquivos de teste; fuzzing; **testes de isolamento cross-tenant/agent/project/thread como cidadãos de primeira classe** (`reborn_*_scope_isolation_parity.rs`); parity tests de trace gravado contra o OpenClaw; testes de arquitetura mecanizados; regra que exige testes de denial/redaction/escape para qualquer mudança de sandbox.

### 11. Extensibilidade — Nota: 3
**Formato de skill compatível com OpenClaw/Claude** (`SKILL.md` com frontmatter); skills v2 com snippets de código executáveis, métricas de uso/confiança e **extração automática de skills** (`learning.rs`); extensões via WASM/MCP/first-party sem restart; providers configuráveis (NEAR AI, Gemini OAuth etc.).

### 12. Interfaces — Nota: 3
CLI/REPL completo, WebUI (SSE+WS com OIDC, rate limit, origin check), Slack, Telegram, webhooks — todos entrando pelos **mesmos contratos de turn** (ProductAdapter); a WebUI é proibida de bypassar as fronteiras de auth.

### 13. Aprendizado / auto-melhoria (suplementar) — Nota: 2
Extração automática de skills (`ironclaw_skills/learning.rs`) com métricas de uso/confiança e versionamento — presente e estruturado, menos central e curado que no Hermes.

### 14. Proatividade / agendamento (suplementar, categoria) — Nota: 3
Routines Engine (`ironclaw_triggers`, 17.5k linhas): tarefas cron, reativas a eventos e webhooks; heartbeat de monitoramento.

## Síntese

| Dimensões 1–12 | **Total: 34/36** (planejamento e subagentes-desabilitados) |
|---|---|

- **Perfil/arquétipo:** o kernel de segurança da categoria — enquanto os outros *aplicam política sobre* o loop, o IronClaw torna o loop incapaz de agir sem o kernel. É a diferença entre guarda na porta e porta que não existe.
- **Pontos mais fortes:** as nove camadas da dimensão 6; trust class inforjável por sistema de tipos; testes de isolamento cross-tenant como rotina.
- **Pontos mais fracos:** subagentes desabilitados em produção; sem decomposição de tarefas; hipótese de TEE/enclaves não confirmada (marketing externo vs. código).
- **Recurso dististivo:** a arquitetura de 4 camadas não-pares (Products / Userland loops / Kernel boundary / Substrates) com enforcement mecânico por testes de dependência.
- **"O que roubar":** trust class por sistema de tipos; prompt-write safety para documentos de identidade; circuit-breaker de efetividade de compactação; fail-closed que oculta a capability em vez de degradar.
- **Cláusula de expiração:** quase nada aqui expira — é tudo fronteira com o mundo. A exceção é o deny-filter de subagentes (prótese temporária de imaturidade do próprio sistema, não do modelo).
