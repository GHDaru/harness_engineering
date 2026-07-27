"""O loop de tool-calling — o coração do harness, do etapa 01 do harness-zero.

Diferença de produção: recebe apenas as tools **habilitadas pelo gating**
(`permitidas`), e a chave BYOK opcional. Quando não há tools ativas (modo
progressivo antes do cap. 02), o loop degrada para uma única resposta — o
companion é, ali, só um tutor que conversa (a lição do cap. 02).
"""

from __future__ import annotations

import json
from typing import Optional

from llm import LLMPort, Message
from tools import Tools

MAX_TURNS = 6  # freio de mão: agente sem limite é incidente esperando data (cap. 02)


def run_turn(history: list[Message], llm: LLMPort, tools: Tools,
             permitidas: set[str], trace: list[str],
             byok_key: Optional[str] = None) -> str:
    schemas = tools.schemas_para(permitidas)
    for _ in range(MAX_TURNS):
        reply = llm.complete(history, schemas, byok_key=byok_key)
        history.append(reply)

        chamadas = reply.get("tool_calls") or []
        if not chamadas:
            return reply.get("content") or ""

        for call in chamadas:
            nome = call["function"]["name"]
            try:
                args = json.loads(call["function"].get("arguments") or "{}")
            except json.JSONDecodeError:
                args = {}
            resultado = tools.executar(nome, args, permitidas)
            trace.append(f"🔧 {nome}({json.dumps(args, ensure_ascii=False)})")
            history.append({"role": "tool", "tool_call_id": call.get("id", ""),
                            "content": str(resultado)})

    return "(interrompido: limite de turnos atingido)"
