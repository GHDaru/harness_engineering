"""MCP (cap. 06) — ferramentas dos outros, no MESMO vocabulário de ação.

Cliente mínimo no desenho da spec 2026-07-28 (nota de época: escrita em
2026-07-31): núcleo STATELESS — nenhum `initialize`, nenhum session id;
cada requisição é um POST JSON-RPC autocontido com o método espelhado no
header `Mcp-Method`. Ferramentas remotas viram `Ferramenta` comuns na
caixa: o loop não sabe (nem deve saber) o que é local e o que é MCP — a
tese do capítulo.

O `transporte` é injetável: nos testes, uma função; em produção, HTTP via
httpx. Igual ao provedor: a borda é trocável, o domínio não muda.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

from .ferramentas import Ferramenta

Transporte = Callable[[str, dict, dict], dict]  # (url, corpo, headers) -> resposta json


def transporte_http(url: str, corpo: dict, headers: dict) -> dict:
    import httpx

    r = httpx.post(url, json=corpo, headers=headers, timeout=60)
    r.raise_for_status()
    return r.json()


@dataclass
class ClienteMCP:
    url: str
    transporte: Transporte = transporte_http

    def _chamar(self, metodo: str, params: dict | None = None) -> dict:
        corpo = {"jsonrpc": "2.0", "id": 1, "method": metodo, "params": params or {}}
        headers = {"Mcp-Method": metodo, "Content-Type": "application/json"}
        resposta = self.transporte(self.url, corpo, headers)
        if "error" in resposta:
            raise RuntimeError(f"MCP {metodo}: {resposta['error']}")
        return resposta.get("result", {})

    def listar_ferramentas(self) -> list[dict]:
        return self._chamar("tools/list").get("tools", [])

    def executar(self, nome: str, argumentos: dict) -> str:
        resultado = self._chamar("tools/call", {"name": nome, "arguments": argumentos})
        blocos = resultado.get("content", [])
        textos = [b.get("text", "") for b in blocos if b.get("type") == "text"]
        return "\n".join(textos) or json.dumps(resultado, ensure_ascii=False)

    def como_ferramentas(self) -> list[Ferramenta]:
        """Cada tool remota vira uma Ferramenta comum (prefixo mcp_ no nome)."""
        ferramentas = []
        for t in self.listar_ferramentas():
            nome_remoto = t["name"]

            def executar(_nome=nome_remoto, **argumentos):
                return self.executar(_nome, argumentos)

            ferramentas.append(
                Ferramenta(
                    nome=f"mcp_{nome_remoto}",
                    descricao=t.get("description", nome_remoto),
                    esquema=t.get("inputSchema", {"type": "object", "properties": {}}),
                    executar=executar,
                    muta=True,  # remoto = desconhecido: trata como mutante (cap. 07)
                )
            )
        return ferramentas
