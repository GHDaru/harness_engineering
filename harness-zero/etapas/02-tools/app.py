"""harness-zero — Etapa 2: ToolPort. Schemas derivados de tipos.

Na etapa 1, os schemas das ferramentas foram escritos À MÃO — e você sentiu o
tédio: cada tool exigia um bloco JSON repetitivo, fácil de desatualizar quando
a assinatura muda. Este é o problema que o capítulo 05 resolve, e a solução é
a mesma que os harnesses reais adotaram (schema derivado de tipos: FastMCP,
OpenAI Agents SDK `function_tool`, Goose `#[tool]`...):

    a FONTE DA VERDADE da ferramenta é a própria função —
    assinatura tipada + docstring. O schema é DERIVADO, nunca duplicado.

Nasce aqui a segunda porta do harness: o **ToolPort** — o registro que conhece
as ferramentas, produz os schemas para o modelo e executa as chamadas. O loop
da etapa 1 continua o mesmo; ele só passa a perguntar ao ToolPort em vez de
carregar listas soltas. (DDD leve: "ferramenta" agora é um conceito nomeado
do domínio, não um par de dicionários.)

Rodar:  uvicorn app:app --reload   →  http://localhost:8000
Como na etapa 1: EchoAdapter para estudar o fluxo; modelo real para tool-calling.
"""

import datetime
import inspect
import json
import os
import typing
from pathlib import Path
from typing import Protocol

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


def _load_dotenv() -> None:
    for parent in (Path(__file__).parent, *Path(__file__).parents):
        env = parent / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ.setdefault(key.strip(), val.strip())
            return


_load_dotenv()

Message = dict
MAX_TURNS = 8


# ------------------------------------------------------------- ToolPort
# A porta: o que o resto do harness precisa saber sobre "ferramentas".

class ToolPort(Protocol):
    def schemas(self) -> list[dict]: ...
    def executar(self, nome: str, args: dict) -> str: ...


# O adapter concreto: um registro que DERIVA o schema da assinatura tipada.
# Compare com a etapa 1: lá, cada tool tinha um bloco JSON copiado à mão.

_MAPA_TIPOS = {str: "string", int: "integer", float: "number", bool: "boolean"}


def _schema_da_funcao(fn) -> dict:
    """Deriva o JSON Schema (dialeto OpenAI tools) de uma função tipada.
    Docstring vira description; parâmetros tipados viram properties;
    parâmetros sem default viram required. Uma fonte da verdade."""
    sig = inspect.signature(fn)
    hints = typing.get_type_hints(fn)
    props, required = {}, []
    for nome, par in sig.parameters.items():
        tipo = _MAPA_TIPOS.get(hints.get(nome, str), "string")
        props[nome] = {"type": tipo}
        if par.default is inspect.Parameter.empty:
            required.append(nome)
    return {"type": "function", "function": {
        "name": fn.__name__,
        "description": inspect.getdoc(fn) or fn.__name__,
        "parameters": {"type": "object", "properties": props, "required": required}}}


class RegistroDeTools:
    """O adapter do ToolPort: decore uma função tipada e ela vira ferramenta."""

    def __init__(self) -> None:
        self._fns: dict[str, typing.Callable] = {}

    def tool(self, fn):
        """Decorator: registra a função como ferramenta do harness."""
        self._fns[fn.__name__] = fn
        return fn

    def schemas(self) -> list[dict]:
        return [_schema_da_funcao(f) for f in self._fns.values()]

    def executar(self, nome: str, args: dict) -> str:
        fn = self._fns.get(nome)
        if fn is None:
            return f"erro: ferramenta desconhecida '{nome}'"
        try:
            return str(fn(**args))
        except Exception as exc:  # erro volta como texto — o modelo decide o que fazer
            return f"erro: {exc}"


tools = RegistroDeTools()


# --------------------------------------------------- as ferramentas (tipadas)
# Repare: NENHUM schema à mão. A assinatura + docstring são a fonte da verdade.

@tools.tool
def get_time() -> str:
    """Retorna a data e hora atuais no formato ISO."""
    return datetime.datetime.now().isoformat(timespec="seconds")


@tools.tool
def somar(a: float, b: float) -> float:
    """Soma dois números e retorna o resultado."""
    return a + b


@tools.tool
def read_file(path: str, max_chars: int = 4000) -> str:
    """Lê um arquivo de texto do disco e retorna até max_chars caracteres.
    (Ainda sem proteção — a ferida continua aberta de propósito até o cap. 07.)"""
    return Path(path).read_text()[:max_chars]


# ---------------------------------------------------------------- LLMPort

class LLMPort(Protocol):
    def complete(self, messages: list[Message], tools: list[dict]) -> Message: ...


class EchoAdapter:
    def complete(self, messages: list[Message], tools: list[dict]) -> Message:
        return {"role": "assistant", "content": f"(echo) você disse: {messages[-1]['content']}"}


class OpenAICompatAdapter:
    def __init__(self) -> None:
        self.base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "gpt-5.4-mini")

    def complete(self, messages: list[Message], tools: list[dict]) -> Message:
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": messages, "tools": tools},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]


def make_llm() -> LLMPort:
    if os.environ.get("LLM_ADAPTER", "echo") == "openai":
        return OpenAICompatAdapter()
    return EchoAdapter()


# ------------------------------------------------------------- O LOOP
# Idêntico ao da etapa 1 — só que agora pergunta ao ToolPort.
# É assim que uma porta paga o aluguel: o loop não mudou quando as tools mudaram.

def run_turn(history: list[Message], llm: LLMPort, port: ToolPort, trace: list[str]) -> str:
    for _ in range(MAX_TURNS):
        reply = llm.complete(history, port.schemas())
        history.append(reply)

        tool_calls = reply.get("tool_calls") or []
        if not tool_calls:
            return reply.get("content") or ""

        for call in tool_calls:
            nome = call["function"]["name"]
            args = json.loads(call["function"]["arguments"] or "{}")
            resultado = port.executar(nome, args)
            trace.append(f"🔧 {nome}({json.dumps(args, ensure_ascii=False)})")
            history.append({"role": "tool", "tool_call_id": call["id"],
                            "content": resultado})

    return "(interrompido: limite de turnos atingido)"


# ------------------------------------------------------------------ app

app = FastAPI(title="harness-zero · etapa 2")
llm: LLMPort = make_llm()
history: list[Message] = []  # a mesma dor de estado das etapas 0-1 (cap. 08 resolve)


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(inp: ChatIn) -> dict:
    history.append({"role": "user", "content": inp.message})
    trace: list[str] = []
    reply = run_turn(history, llm, tools, trace)
    return {"reply": reply, "trace": trace}


@app.get("/tools")
def listar_tools() -> dict:
    """Janela de observação da etapa: veja os schemas DERIVADOS das assinaturas."""
    return {"tools": tools.schemas()}


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse((Path(__file__).parent / "index.html").read_text())
