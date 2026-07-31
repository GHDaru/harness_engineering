# RADAR — roadmap de auto-atualização do livro vivo

> Mantido por um agente agendado (1×/dia) sob o contrato de [`AGENTE.md`](AGENTE.md).
> Itens daqui **não entram no livro automaticamente**: promover = abrir feature spec-kit com curadoria humana (ADR 0008).

## ⚠ Leituras executivas possivelmente invalidadas

- ~~Cap. 06 (MCP)~~ **tratada na spec 060 (edição 0.55)** — a spec **2026-07-28** removeu o handshake `initialize` e o `Mcp-Session-Id` (núcleo stateless), **depreciou Sampling/Roots/Logging e o transporte HTTP+SSE**, e substituiu elicitation/sampling por MRTR. A Leitura executiva atual celebra exatamente o que foi depreciado. → promover a spec de revisão (impacto A; ver diário 2026-07-31).

## Itens

| Data | Item (com link) | Capítulo | Impacto | Ação sugerida | Status |
|---|---|---|---|---|---|
| 2026-07-31 | [Grok Build (xAI) open source, Apache 2.0](https://x.ai/news/grok-build-open-source) — harness completo com subagentes paralelos em git worktrees, AGENTS.md, skills/hooks/MCP | 01 §4, 10, Apêndice A | **B** | teste de inclusão no corpus na rodada 2026-10; nota worktrees no cap. 10 | novo |
| 2026-07-31 | [Pi (Earendil/Ronacher)](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent) — harness minimalista: system prompt <1k tokens, 4 tools, lazy skills, sem MCP/subagentes | 03, 12, 01 §4 | **B** | candidato ao corpus; caixa de contraste "o harness mínimo" no cap. 03 | novo |
| 2026-07-31 | Papers jul/2026: [Harness Evolution eval](https://arxiv.org/html/2607.12227) · [CompactionRL](https://arxiv.org/html/2607.05378v1) · [survey Harness Engineering (RUCAIBox)](https://github.com/RUCAIBox/awesome-agent-harness) ⏳ PDFs não lidos | 04, 11, bibliografia | **B/C** | leitura dirigida na janela 2026-10; survey candidata à bibliografia | novo |
| 2026-07-31 | Evolução do corpus: [Claude Code](https://code.claude.com/docs/en/whats-new) (/fork, Opus 5 1M) · [Codex](https://releasebot.io/updates/openai/codex) (plugins interop) · [gemini-cli v0.53](https://geminicli.com/docs/changelogs/latest/) (caretakers, eval coverage) | 11, 14, 16, Apêndice A | **C** | refresh do Apêndice A na rodada 2026-10; sinal de convergência (plugins) no 14 | novo |
| 2026-07-31 | [A2A v1.0 estável (Linux Foundation)](https://a2a-protocol.org/latest/specification/), v1.0.1 com extensões | 17 | **C** | conferir se o adendo 2026-07-31 do cap. 17 já cobre o v1.0 | avaliando |
| 2026-07-31 | [MCP spec 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/) — núcleo stateless, MRTR, extensões, cache ttlMs, depreciações (Sampling/Roots/Logging/SSE/DCR) | 06 (A), 17 (B), etapa 07 (B), 03/04 (C) | **A** | revisar cap. 06 (lifecycle/Leitura executiva), nota no 17 e na etapa 07 | promovido (spec 060) |
| 2026-07-29 | *(inicial)* Radar criado; primeira varredura na próxima execução agendada | — | — | — | novo |
