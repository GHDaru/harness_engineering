"""LLMPort — a primeira porta do harness-zero, aqui em produção.

Reuso direto do padrão do etapa 01: um Protocol e dois adapters. A novidade
de produção é o **BYOK** (bring your own key): o leitor pode passar a própria
chave numa requisição; ela é usada só naquela chamada e **nunca** persistida
nem logada (cap. 07 — credencial é credencial).
"""

from __future__ import annotations

import json
import os
from typing import Iterator, Optional, Protocol

import httpx

Message = dict


class LLMPort(Protocol):
    def complete(self, messages: list[Message], tools: list[dict],
                 byok_key: Optional[str] = None) -> Message: ...

    def stream(self, messages: list[Message], tools: list[dict],
               byok_key: Optional[str] = None) -> Iterator[dict]:
        """Gera eventos {"delta": str} (texto incremental) e, por último,
        {"message": Message} — a mensagem completa (com tool_calls, se houver)."""
        ...


class EchoAdapter:
    """Sem rede: prova o fluxo e roda os testes. Nunca pede ferramenta."""

    def complete(self, messages: list[Message], tools: list[dict],
                 byok_key: Optional[str] = None) -> Message:
        ultimo = next((m for m in reversed(messages) if m.get("role") == "user"), None)
        texto = (ultimo or {}).get("content", "")
        return {"role": "assistant",
                "content": f"(echo) recebi: {texto}\n\n"
                           "Configure LLM_ADAPTER=openai + OPENAI_API_KEY para uma resposta real."}

    def stream(self, messages: list[Message], tools: list[dict],
               byok_key: Optional[str] = None) -> Iterator[dict]:
        msg = self.complete(messages, tools, byok_key)
        # em pedaços de poucas palavras: prova o fluxo incremental sem rede
        palavras = msg["content"].split(" ")
        for i in range(0, len(palavras), 3):
            yield {"delta": " ".join(palavras[i:i + 3]) + (" " if i + 3 < len(palavras) else "")}
        yield {"message": msg}


class OpenAICompatAdapter:
    """Qualquer endpoint OpenAI-compatible (NVIDIA NIM por padrão)."""

    def __init__(self) -> None:
        self.base_url = os.environ.get("OPENAI_BASE_URL", "https://integrate.api.nvidia.com/v1")
        self.project_key = os.environ.get("OPENAI_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")

    def complete(self, messages: list[Message], tools: list[dict],
                 byok_key: Optional[str] = None) -> Message:
        # BYOK tem prioridade e é efêmera (só esta chamada); senão, a chave do projeto.
        key = (byok_key or self.project_key or "").strip()
        payload: dict = {"model": self.model, "messages": messages}
        if tools:
            payload["tools"] = tools
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]

    def stream(self, messages: list[Message], tools: list[dict],
               byok_key: Optional[str] = None) -> Iterator[dict]:
        """SSE do endpoint OpenAI-compatible: emite deltas de conteúdo na hora;
        deltas de tool_calls são agregados por índice e só saem na mensagem final."""
        key = (byok_key or self.project_key or "").strip()
        payload: dict = {"model": self.model, "messages": messages, "stream": True}
        if tools:
            payload["tools"] = tools
        conteudo: list[str] = []
        calls: dict[int, dict] = {}
        with httpx.stream("POST", f"{self.base_url}/chat/completions",
                          headers={"Authorization": f"Bearer {key}"},
                          json=payload, timeout=120) as r:
            r.raise_for_status()
            for linha in r.iter_lines():
                if not linha.startswith("data: "):
                    continue
                dado = linha[6:].strip()
                if dado == "[DONE]":
                    break
                try:
                    delta = json.loads(dado)["choices"][0].get("delta") or {}
                except (json.JSONDecodeError, LookupError):
                    continue
                if delta.get("content"):
                    conteudo.append(delta["content"])
                    yield {"delta": delta["content"]}
                for tc in delta.get("tool_calls") or []:
                    i = tc.get("index", 0)
                    alvo = calls.setdefault(i, {"id": "", "type": "function",
                                                "function": {"name": "", "arguments": ""}})
                    if tc.get("id"):
                        alvo["id"] = tc["id"]
                    fn = tc.get("function") or {}
                    if fn.get("name"):
                        alvo["function"]["name"] += fn["name"]
                    if fn.get("arguments"):
                        alvo["function"]["arguments"] += fn["arguments"]
        msg: Message = {"role": "assistant", "content": "".join(conteudo) or None}
        if calls:
            msg["tool_calls"] = [calls[i] for i in sorted(calls)]
        yield {"message": msg}


def make_llm(adapter: str) -> LLMPort:
    return OpenAICompatAdapter() if adapter == "openai" else EchoAdapter()
