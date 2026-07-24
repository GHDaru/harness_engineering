# 06 — MCP (Model Context Protocol)

## O problema

Nenhum harness consegue embutir tools para todos os sistemas do mundo. O MCP resolve a integração pela via do padrão aberto: servidores expõem tools, resources e prompts num protocolo comum; qualquer harness cliente os consome. Em dois anos, virou a lingua franca — os três harnesses estudados são clientes MCP completos, todos sobre os SDKs oficiais do protocolo.

As decisões que diferenciam as implementações:
- **Transportes**: stdio (processo local), Streamable HTTP e SSE (remoto).
- **Autenticação**: OAuth para servidores remotos — com que fluxos e provedores?
- **Resiliência**: reconexão, servidores indisponíveis, mudança dinâmica da lista de tools.
- **Superfície**: só tools, ou também resources, prompts e roots?

## Como os harnesses estudados implementam

### opencode — a implementação mais completa de protocolo
`packages/opencode/src/mcp/` (~1.000 linhas no `index.ts`, + `catalog.ts`, `oauth-provider.ts`, `auth.ts`). Três transportes — `StdioClientTransport`, `StreamableHTTPClientTransport` e `SSEClientTransport` com **fallback automático HTTP→SSE**. OAuth completo: fluxo de autorização com callback server local, PKCE, comando dedicado `opencode mcp auth`. Cobre a superfície larga do protocolo: notificações `ToolListChanged`, logging, roots, prompts, resources e resource templates. Instruções fornecidas pelo servidor MCP entram no system prompt (`system.ts:mcp()`) — o servidor pode ensinar o modelo a usá-lo.

### gemini-cli — OAuth de nível corporativo
`packages/core/src/tools/mcp-client.ts` + `mcp-client-manager.ts`, com os mesmos três transportes selecionados por config. O diferencial está em `packages/core/src/mcp/`: além do OAuth padrão com callback local e storage de tokens, há provedores **Google auth** e **impersonation de service account** — integração MCP pensada para ambientes corporativos GCP. Tools descobertas viram `DiscoveredMCPTool` com namespacing por servidor; prompts MCP são expostos; gestão via comando `/mcp` e `~/.gemini/settings.json`. Notável: a suíte de evals inclui teste de **prompt injection via MCP** (cap. 11) — o único harness estudado que trata servidor MCP como superfície de ataque testada.

### OpenHarness — cliente pragmático
`src/openharness/mcp/` (`McpClientManager`) sobre o SDK `mcp>=1.0.0`: transportes **stdio** e **Streamable HTTP** (sem SSE), com rastreio de status de conexão, auto-reconnect e degradação graciosa quando um servidor cai (`call_tool`/`read_resource` não derrubam a sessão). Resources são expostos ao modelo como tools próprias (`list_mcp_resources`, `read_mcp_resource`), e há `mcp_auth` para autenticação. Config via `oh mcp` e `--mcp-config`.

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Transportes | stdio + HTTP + SSE (fallback) | stdio + HTTP + SSE | stdio + HTTP |
| OAuth | completo, PKCE, CLI dedicada | completo + Google/SA impersonation | básico (`mcp_auth`) |
| Resources/prompts/roots | todos | resources + prompts | resources |
| Resiliência | reconexão + ToolListChanged | manager por servidor | auto-reconnect + degradação |
| Segurança | instruções no prompt | eval de prompt injection MCP | — |

A adoção universal do MCP — três projetos, três stacks, mesmo protocolo, SDKs oficiais — é o caso mais claro de padronização na disciplina. A fronteira agora é dupla: **autenticação empresarial** (o território que o gemini-cli ocupa) e **segurança** (servidores MCP são código de terceiros injetando texto no contexto do modelo; só um dos três harnesses testa esse vetor). Um ponto em aberto para as próximas rodadas do benchmark: nenhum dos três atua como *servidor* MCP no core — o harness como serviço consumível por outros agentes aparece por outras vias (A2A no gemini-cli, ACP no opencode).
