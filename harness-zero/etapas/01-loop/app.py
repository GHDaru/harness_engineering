"""harness-zero — Etapa 1: o loop. A diferença entre um chat e um agente.

Na etapa 0, o modelo só falava. Agora ele pode AGIR: damos a ele ferramentas
e — a peça central deste capítulo — o LOOP que executa o que ele pede e
devolve os resultados, repetindo até o modelo decidir parar (ou até o limite
de turnos, porque agentes sem limite são incidentes esperando data).

O loop inteiro tem ~30 linhas (função run_turn). Todo o resto é suporte.
Repare que a porta LLMPort MUDOU de forma em relação à etapa 0: antes
devolvia texto; agora devolve a mensagem completa (que pode conter pedidos
de ferramenta). Fronteiras também evoluem — o custo dessa quebra é a lição.

Os schemas das ferramentas estão escritos À MÃO de propósito: sentir esse
trabalho repetitivo é o que justifica a etapa 2 (derivar schemas de tipos).

Rodar:  uvicorn app:app --reload   →  http://localhost:8000
Nota: esta etapa precisa de um modelo real com tool-calling
      (LLM_ADAPTER=openai). O EchoAdapter continua útil: nunca pede
      ferramentas, então mostra o caminho "só conversa" do loop.
"""

import datetime
import json
import os
from pathlib import Path
from typing import Protocol

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


def _load_dotenv() -> None:
    """Carrega um .env vizinho para os.environ (a chave de API vive só aqui
    ou no ambiente — nunca no código; ver cap. 07). Sem dependência externa."""
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
MAX_TURNS = 8  # o freio de mão: sem isso, um modelo confuso roda para sempre


# ------------------------------------------------------ ferramentas (2)

def get_time() -> str:
    """A ferramenta mais boba possível — e suficiente para ver o loop girar."""
    return datetime.datetime.now().isoformat(timespec="seconds")


def read_file(path: str) -> str:
    """Leitura de arquivo SEM nenhuma proteção. Está errado de propósito:
    o capítulo 07 (permissões) nasce exatamente desta ferida aberta."""
    try:
        return Path(path).read_text()[:4000]
    except OSError as exc:
        return f"erro: {exc}"  # erro volta como TEXTO para o modelo decidir o que fazer


TOOL_IMPLS = {"get_time": lambda args: get_time(),
              "read_file": lambda args: read_file(args["path"])}

# Schemas à mão (dialeto OpenAI tools). Compare o tédio daqui com a etapa 2.
TOOL_SCHEMAS = [
    {"type": "function", "function": {
        "name": "get_time",
        "description": "Retorna a data e hora atuais no formato ISO.",
        "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Lê um arquivo de texto do disco e retorna até 4000 caracteres.",
        "parameters": {"type": "object",
                       "properties": {"path": {"type": "string", "description": "caminho do arquivo"}},
                       "required": ["path"]}}},
]


# ---------------------------------------------------------------- porta

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

def run_turn(history: list[Message], llm: LLMPort, trace: list[str]) -> str:
    """O coração do harness: modelo decide → ferramentas executam →
    resultados voltam → repete. Para quando o modelo responde sem pedir
    ferramenta (o critério de parada universal do cap. 02) ou em MAX_TURNS."""
    for _ in range(MAX_TURNS):
        reply = llm.complete(history, TOOL_SCHEMAS)
        history.append(reply)

        tool_calls = reply.get("tool_calls") or []
        if not tool_calls:                       # sem pedido de ferramenta:
            return reply.get("content") or ""    # o turno acabou.

        for call in tool_calls:
            name = call["function"]["name"]
            args = json.loads(call["function"]["arguments"] or "{}")
            impl = TOOL_IMPLS.get(name)
            result = impl(args) if impl else f"erro: ferramenta desconhecida '{name}'"
            trace.append(f"🔧 {name}({json.dumps(args, ensure_ascii=False)})")
            history.append({"role": "tool", "tool_call_id": call["id"],
                            "content": str(result)})

    return "(interrompido: limite de turnos atingido)"


# ------------------------------------------------------------------ app

app = FastAPI(title="harness-zero · etapa 1")
llm: LLMPort = make_llm()
history: list[Message] = []  # a mesma dor da etapa 0, de propósito (cap. 08)


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(inp: ChatIn) -> dict:
    history.append({"role": "user", "content": inp.message})
    trace: list[str] = []
    reply = run_turn(history, llm, trace)
    return {"reply": reply, "trace": trace}


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse((Path(__file__).parent / "index.html").read_text())
