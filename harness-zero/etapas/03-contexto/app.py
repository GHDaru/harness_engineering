"""harness-zero — Etapa 3: entrega de contexto. O prompt montado em camadas.

Nas etapas 0–2, o modelo recebia só o histórico cru — nenhuma identidade,
nenhuma regra, nenhum conhecimento do ambiente. Faça o teste na etapa 2:
pergunte "quais são as regras deste projeto?" e veja o modelo inventar.

O capítulo 03 ensina a cura: o que o modelo enxerga é uma DECISÃO DE
ENGENHARIA, não um acidente. Todo harness real monta o system prompt em
CAMADAS, cada uma com uma fonte e um dono diferentes:

    1. identidade      — quem o agente é (fixa, do harness)
    2. ambiente        — onde ele está (derivada da máquina, a cada turno)
    3. regras do projeto — o AGENTS.md (do usuário; editável sem tocar código)
    4. a conversa      — o histórico (das etapas anteriores)

Nasce o **MontadorDeContexto**: remonta as camadas A CADA TURNO (o ambiente
muda; o AGENTS.md pode ter sido editado entre uma mensagem e outra — teste!).
A janela de observação é o endpoint /contexto: veja exatamente o que o
modelo enxergaria agora. Loop e ToolPort: intactos das etapas 1–2.

Rodar:  uvicorn app:app --reload   →  http://localhost:8000
"""

import datetime
import inspect
import json
import os
import platform
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
AQUI = Path(__file__).parent


# ------------------------------------------------- MontadorDeContexto (novo)

class MontadorDeContexto:
    """Monta o system prompt em camadas nomeadas. Cada camada tem uma fonte:
    fixa (identidade), derivada (ambiente) ou do usuário (AGENTS.md).
    Remontado a cada turno — contexto é fresco, nunca cacheado por preguiça."""

    def camada_identidade(self) -> str:
        return ("Você é o assistente do harness-zero, a trilha prática do livro "
                "Engenharia de Harness. Você tem ferramentas; use-as quando ajudarem.")

    def camada_ambiente(self) -> str:
        return (f"Ambiente: {platform.system()} · Python {platform.python_version()} · "
                f"diretório {Path.cwd()} · agora é {datetime.datetime.now().isoformat(timespec='minutes')}.")

    def camada_regras_do_projeto(self) -> str:
        """A camada do USUÁRIO: o AGENTS.md ao lado do app. Edite-o com o chat
        aberto e mande outra mensagem — o comportamento muda sem redeploy."""
        arq = AQUI / "AGENTS.md"
        if not arq.exists():
            return "(sem AGENTS.md neste projeto — o agente segue só as camadas acima)"
        return f"Regras do projeto (AGENTS.md — siga-as):\n\n{arq.read_text()}"

    def montar(self) -> str:
        return "\n\n---\n\n".join([
            self.camada_identidade(),
            self.camada_ambiente(),
            self.camada_regras_do_projeto(),
        ])


contexto = MontadorDeContexto()


# ------------------------------------------------------------- ToolPort
# (idêntico à etapa 2 — schemas derivados de tipos)

_MAPA_TIPOS = {str: "string", int: "integer", float: "number", bool: "boolean"}


def _schema_da_funcao(fn) -> dict:
    sig = inspect.signature(fn)
    hints = typing.get_type_hints(fn)
    props, required = {}, []
    for nome, par in sig.parameters.items():
        props[nome] = {"type": _MAPA_TIPOS.get(hints.get(nome, str), "string")}
        if par.default is inspect.Parameter.empty:
            required.append(nome)
    return {"type": "function", "function": {
        "name": fn.__name__, "description": inspect.getdoc(fn) or fn.__name__,
        "parameters": {"type": "object", "properties": props, "required": required}}}


class RegistroDeTools:
    def __init__(self) -> None:
        self._fns: dict[str, typing.Callable] = {}

    def tool(self, fn):
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
        except Exception as exc:
            return f"erro: {exc}"


tools = RegistroDeTools()


@tools.tool
def get_time() -> str:
    """Retorna a data e hora atuais no formato ISO."""
    return datetime.datetime.now().isoformat(timespec="seconds")


@tools.tool
def read_file(path: str, max_chars: int = 4000) -> str:
    """Lê um arquivo de texto do disco e retorna até max_chars caracteres.
    (Ainda sem proteção — cap. 07.)"""
    return Path(path).read_text()[:max_chars]


# ---------------------------------------------------------------- LLMPort

class LLMPort(Protocol):
    def complete(self, messages: list[Message], tools: list[dict]) -> Message: ...


class EchoAdapter:
    def complete(self, messages: list[Message], tools: list[dict]) -> Message:
        # o echo mostra o tamanho do contexto — repare no efeito das camadas
        sistema = next((m for m in messages if m["role"] == "system"), None)
        n = len(sistema["content"]) if sistema else 0
        return {"role": "assistant",
                "content": f"(echo) você disse: {messages[-1]['content']} "
                           f"[system prompt atual: {n} caracteres — veja /contexto]"}


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
# Mudança de UMA linha em relação à etapa 2: o system prompt entra na frente.
# O histórico guarda só a conversa; o sistema é remontado fresco a cada turno.

def run_turn(history: list[Message], llm: LLMPort, port, trace: list[str]) -> str:
    mensagens = [{"role": "system", "content": contexto.montar()}] + history
    for _ in range(MAX_TURNS):
        reply = llm.complete(mensagens, port.schemas())
        mensagens.append(reply)
        history.append(reply)

        tool_calls = reply.get("tool_calls") or []
        if not tool_calls:
            return reply.get("content") or ""

        for call in tool_calls:
            nome = call["function"]["name"]
            args = json.loads(call["function"]["arguments"] or "{}")
            resultado = port.executar(nome, args)
            trace.append(f"🔧 {nome}({json.dumps(args, ensure_ascii=False)})")
            msg = {"role": "tool", "tool_call_id": call["id"], "content": resultado}
            mensagens.append(msg)
            history.append(msg)

    return "(interrompido: limite de turnos atingido)"


# ------------------------------------------------------------------ app

app = FastAPI(title="harness-zero · etapa 3")
llm: LLMPort = make_llm()
history: list[Message] = []


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(inp: ChatIn) -> dict:
    history.append({"role": "user", "content": inp.message})
    trace: list[str] = []
    reply = run_turn(history, llm, tools, trace)
    return {"reply": reply, "trace": trace}


@app.get("/contexto")
def ver_contexto() -> dict:
    """Janela de observação da etapa: o system prompt que o modelo enxergaria
    AGORA, camada por camada. Edite o AGENTS.md e recarregue."""
    return {"camadas": {
        "identidade": contexto.camada_identidade(),
        "ambiente": contexto.camada_ambiente(),
        "regras_do_projeto": contexto.camada_regras_do_projeto(),
    }, "montado": contexto.montar()}


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse((Path(__file__).parent / "index.html").read_text())
