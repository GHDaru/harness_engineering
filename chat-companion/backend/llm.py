"""LLMPort — a primeira porta do harness-zero, aqui em produção.

Reuso direto do padrão do etapa 01: um Protocol e dois adapters. A novidade
de produção é o **BYOK** (bring your own key): o leitor pode passar a própria
chave numa requisição; ela é usada só naquela chamada e **nunca** persistida
nem logada (cap. 07 — credencial é credencial).
"""

from __future__ import annotations

import os
from typing import Optional, Protocol

import httpx

Message = dict


class LLMPort(Protocol):
    def complete(self, messages: list[Message], tools: list[dict],
                 byok_key: Optional[str] = None) -> Message: ...


class EchoAdapter:
    """Sem rede: prova o fluxo e roda os testes. Nunca pede ferramenta."""

    def complete(self, messages: list[Message], tools: list[dict],
                 byok_key: Optional[str] = None) -> Message:
        ultimo = next((m for m in reversed(messages) if m.get("role") == "user"), None)
        texto = (ultimo or {}).get("content", "")
        return {"role": "assistant",
                "content": f"(echo) recebi: {texto}\n\n"
                           "Configure LLM_ADAPTER=openai + OPENAI_API_KEY para uma resposta real."}


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


def make_llm(adapter: str) -> LLMPort:
    return OpenAICompatAdapter() if adapter == "openai" else EchoAdapter()
