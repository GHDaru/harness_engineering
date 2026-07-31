"""Provedores — a porta para o modelo (e a camada anticorrupção da linguagem ubíqua).

O domínio inteiro fala português: mensagens carregam blocos `texto`,
`uso_de_ferramenta` e `resultado_de_ferramenta`. A tradução para o dialeto
de cada API (Anthropic Messages, hoje) mora AQUI e só aqui — se amanhã o
provedor mudar, o resto do harness não fica sabendo.

Dois provedores:
- `ProvedorAnthropic` — modelo real via HTTP (`ANTHROPIC_API_KEY` no ambiente;
  segredos nunca em arquivo).
- `ProvedorEco` — determinístico e offline: ecoa texto e obedece diretivas
  `@usar ferramenta {"arg": ...}`, o suficiente para exercitar o loop inteiro
  (tool-use, permissões, verificação) em teste. Todo harness precisa de um
  provedor falso: é o que torna o loop testável (cap. 11).
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Protocol

Mensagem = dict  # {"role": "user"|"assistant", "content": str | list[bloco]}


@dataclass
class ChamadaDeFerramenta:
    id: str
    nome: str
    argumentos: dict


@dataclass
class Resposta:
    texto: str = ""
    chamadas: list[ChamadaDeFerramenta] = field(default_factory=list)
    parada: str = "fim"  # "fim" | "ferramenta"
    uso: dict = field(default_factory=dict)


class Provedor(Protocol):
    def gerar(self, sistema: str, mensagens: list[Mensagem], esquemas: list[dict]) -> Resposta: ...


def _blocos(conteudo) -> list[dict]:
    return conteudo if isinstance(conteudo, list) else [{"tipo": "texto", "texto": str(conteudo)}]


def _json_balanceado(texto: str, inicio: int) -> str | None:
    """Extrai um objeto JSON com chaves balanceadas a partir de `inicio` (respeita strings)."""
    if inicio >= len(texto) or texto[inicio] != "{":
        return None
    nivel, em_string, escapado = 0, False, False
    for i in range(inicio, len(texto)):
        ch = texto[i]
        if em_string:
            em_string, escapado = (True, True) if (ch == "\\" and not escapado) else (ch != '"' or escapado, False)
        elif ch == '"':
            em_string = True
        elif ch == "{":
            nivel += 1
        elif ch == "}":
            nivel -= 1
            if nivel == 0:
                return texto[inicio : i + 1]
    return None


class ProvedorEco:
    """Eco com tool-use: `@usar nome {json}` vira chamada de ferramenta.

    Apenas a PRIMEIRA diretiva vira chamada (o JSON dela pode conter outras,
    destinadas a um subagente — chaves balanceadas, não regex não-guloso).
    """

    DIRETIVA = re.compile(r"@usar\s+([\w\-]+)\s*")

    def gerar(self, sistema, mensagens, esquemas):
        ultima = mensagens[-1]
        blocos = _blocos(ultima["content"])
        resultados = [b for b in blocos if b.get("tipo") == "resultado_de_ferramenta"]
        if resultados:
            resumo = " · ".join(str(r.get("conteudo", ""))[:120] for r in resultados)
            return Resposta(texto=f"eco: recebi {len(resultados)} resultado(s) — {resumo}")
        texto = " ".join(b.get("texto", "") for b in blocos if b.get("tipo") == "texto")
        m = self.DIRETIVA.search(texto)
        if m:
            bruto = _json_balanceado(texto, m.end())
            try:
                argumentos = json.loads(bruto) if bruto else {}
            except json.JSONDecodeError:
                argumentos = {}
            return Resposta(chamadas=[ChamadaDeFerramenta(id="eco_0", nome=m.group(1), argumentos=argumentos)],
                            parada="ferramenta")
        return Resposta(texto=f"eco: {texto.strip()}")


class ProvedorAnthropic:
    """Tradutor domínio ⇄ Anthropic Messages API. Requer ANTHROPIC_API_KEY."""

    URL = "https://api.anthropic.com/v1/messages"

    def __init__(self, modelo: str = "claude-sonnet-4-5", max_tokens: int = 4096):
        self.modelo = modelo
        self.max_tokens = max_tokens

    def _traduzir_ida(self, mensagens: list[Mensagem]) -> list[dict]:
        fora = []
        for m in mensagens:
            blocos_api = []
            for b in _blocos(m["content"]):
                if b["tipo"] == "texto":
                    blocos_api.append({"type": "text", "text": b["texto"]})
                elif b["tipo"] == "uso_de_ferramenta":
                    blocos_api.append({"type": "tool_use", "id": b["id"], "name": b["nome"], "input": b["argumentos"]})
                elif b["tipo"] == "resultado_de_ferramenta":
                    blocos_api.append({"type": "tool_result", "tool_use_id": b["id"], "content": str(b["conteudo"])})
            fora.append({"role": m["role"], "content": blocos_api})
        return fora

    def gerar(self, sistema, mensagens, esquemas):
        import httpx

        chave = os.environ.get("ANTHROPIC_API_KEY", "")
        if not chave:
            raise RuntimeError("ANTHROPIC_API_KEY ausente — use ProvedorEco para rodar offline.")
        corpo = {
            "model": self.modelo,
            "max_tokens": self.max_tokens,
            "system": sistema,
            "messages": self._traduzir_ida(mensagens),
        }
        if esquemas:
            corpo["tools"] = [
                {"name": e["nome"], "description": e["descricao"], "input_schema": e["esquema"]} for e in esquemas
            ]
        r = httpx.post(
            self.URL,
            json=corpo,
            headers={"x-api-key": chave, "anthropic-version": "2023-06-01"},
            timeout=120,
        )
        r.raise_for_status()
        dados = r.json()
        resposta = Resposta(parada="ferramenta" if dados.get("stop_reason") == "tool_use" else "fim",
                            uso=dados.get("usage", {}))
        for b in dados.get("content", []):
            if b["type"] == "text":
                resposta.texto += b["text"]
            elif b["type"] == "tool_use":
                resposta.chamadas.append(ChamadaDeFerramenta(id=b["id"], nome=b["name"], argumentos=b["input"]))
        return resposta
