# Spec 037: harness-zero etapa 07 — MCP client stdio (cap. 06)

- FR-001: servidor MCP de EXEMPLO (servidor_mcp_exemplo.py): JSON-RPC 2.0 por linha no stdio; initialize, tools/list, tools/call; 2 tools didaticas.
- FR-002: ClienteMCP no harness: sobe o servidor como subprocesso, faz o handshake, importa as tools (prefixo mcp_) no ToolPort composto; execucao roteada pelo protocolo.
- FR-003: politica da etapa 06 segue valendo para tools MCP; trace distingue local × MCP; smoke (handshake+list+call) verificado; README (07 ✅).
