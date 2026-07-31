# RADAR — roadmap de auto-atualização do livro vivo

> Mantido por um agente agendado (1×/dia) sob o contrato de [`AGENTE.md`](AGENTE.md).
> Itens daqui **não entram no livro automaticamente**: promover = abrir feature spec-kit com curadoria humana (ADR 0008).

## ⚠ Leituras executivas possivelmente invalidadas

- **Cap. 06 (MCP)** — a spec **2026-07-28** removeu o handshake `initialize` e o `Mcp-Session-Id` (núcleo stateless), **depreciou Sampling/Roots/Logging e o transporte HTTP+SSE**, e substituiu elicitation/sampling por MRTR. A Leitura executiva atual celebra exatamente o que foi depreciado. → promover a spec de revisão (impacto A; ver diário 2026-07-31).

## Itens

| Data | Item (com link) | Capítulo | Impacto | Ação sugerida | Status |
|---|---|---|---|---|---|
| 2026-07-31 | [MCP spec 2026-07-28](https://blog.modelcontextprotocol.io/posts/2026-07-28/) — núcleo stateless, MRTR, extensões, cache ttlMs, depreciações (Sampling/Roots/Logging/SSE/DCR) | 06 (A), 17 (B), etapa 07 (B), 03/04 (C) | **A** | revisar cap. 06 (lifecycle/Leitura executiva), nota no 17 e na etapa 07 | novo |
| 2026-07-29 | *(inicial)* Radar criado; primeira varredura na próxima execução agendada | — | — | — | novo |
