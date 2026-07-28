"""Um servidor MCP MÍNIMO — para o leitor ver o protocolo por dentro.

MCP (Model Context Protocol) no transporte stdio: JSON-RPC 2.0, uma mensagem
por linha. Este servidor implementa o essencial do handshake e expõe duas
ferramentas bobas. É o "lado de lá" que o cap. 06 descreve: qualquer harness
cliente consegue usá-las sem saber quem as implementou — esse é o ponto.

Rode-o à mão para sentir o protocolo:
    python servidor_mcp_exemplo.py
    {"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
    {"jsonrpc":"2.0","id":2,"method":"tools/list"}
    {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"contar_palavras","arguments":{"texto":"um dois tres"}}}
"""

import json
import sys

TOOLS = [
    {"name": "contar_palavras",
     "description": "Conta as palavras de um texto.",
     "inputSchema": {"type": "object", "properties": {"texto": {"type": "string"}},
                     "required": ["texto"]}},
    {"name": "inverter_texto",
     "description": "Inverte um texto (último caractere vira o primeiro).",
     "inputSchema": {"type": "object", "properties": {"texto": {"type": "string"}},
                     "required": ["texto"]}},
]


def executar(nome: str, args: dict) -> str:
    if nome == "contar_palavras":
        return str(len(str(args.get("texto", "")).split()))
    if nome == "inverter_texto":
        return str(args.get("texto", ""))[::-1]
    return f"erro: tool desconhecida '{nome}'"


def responder(msg_id, resultado) -> None:
    print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": resultado}), flush=True)


for linha in sys.stdin:
    linha = linha.strip()
    if not linha:
        continue
    req = json.loads(linha)
    metodo, mid = req.get("method"), req.get("id")
    if metodo == "initialize":
        responder(mid, {"protocolVersion": "2025-06-18",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "servidor-exemplo-harness-zero", "version": "0.1"}})
    elif metodo == "notifications/initialized":
        pass  # notificação: sem resposta
    elif metodo == "tools/list":
        responder(mid, {"tools": TOOLS})
    elif metodo == "tools/call":
        p = req.get("params", {})
        texto = executar(p.get("name", ""), p.get("arguments", {}))
        responder(mid, {"content": [{"type": "text", "text": texto}], "isError": False})
    elif mid is not None:
        print(json.dumps({"jsonrpc": "2.0", "id": mid,
                          "error": {"code": -32601, "message": f"método não suportado: {metodo}"}}), flush=True)
