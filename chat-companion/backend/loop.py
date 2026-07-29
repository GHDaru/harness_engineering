"""O loop de tool-calling — o coração do harness, do etapa 01 do harness-zero.

Diferença de produção: recebe apenas as tools **habilitadas pelo gating**
(`permitidas`), e a chave BYOK opcional. Quando não há tools ativas (modo
progressivo antes do cap. 02), o loop degrada para uma única resposta — o
companion é, ali, só um tutor que conversa (a lição do cap. 02).
"""

from __future__ import annotations

import json
from typing import Iterator, Optional

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


def _executar_calls(chamadas: list, history: list[Message], tools: Tools,
                    permitidas: set[str], trace: list[str]) -> Iterator[dict]:
    for call in chamadas:
        nome = call["function"]["name"]
        try:
            args = json.loads(call["function"].get("arguments") or "{}")
        except json.JSONDecodeError:
            args = {}
        resultado = tools.executar(nome, args, permitidas)
        registro = f"🔧 {nome}({json.dumps(args, ensure_ascii=False)})"
        trace.append(registro)
        yield {"trace": registro}
        history.append({"role": "tool", "tool_call_id": call.get("id", ""),
                        "content": str(resultado)})


def run_turn_stream(history: list[Message], llm: LLMPort, tools: Tools,
                    permitidas: set[str], trace: list[str],
                    byok_key: Optional[str] = None) -> Iterator[dict]:
    """Versão streaming (spec 047): gera {"delta"}/{"trace"} conforme acontecem
    e, por último, {"reply": texto_completo}. Mesmo contrato do run_turn:
    MAX_TURNS de freio, tools do gating, trace preenchido."""
    schemas = tools.schemas_para(permitidas)
    partes: list[str] = []
    for _ in range(MAX_TURNS):
        reply: Message = {}
        for ev in llm.stream(history, schemas, byok_key=byok_key):
            if "delta" in ev:
                partes.append(ev["delta"])
                yield {"delta": ev["delta"]}
            elif "message" in ev:
                reply = ev["message"]
        history.append(reply)

        chamadas = reply.get("tool_calls") or []
        if not chamadas:
            yield {"reply": "".join(partes) or (reply.get("content") or "")}
            return
        yield from _executar_calls(chamadas, history, tools, permitidas, trace)

    yield {"reply": "".join(partes) + "\n(interrompido: limite de turnos atingido)"}
