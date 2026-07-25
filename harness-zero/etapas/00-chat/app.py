"""harness-zero — Etapa 0: um chat e uma porta.

Nesta etapa ainda NÃO existe harness. Existe um chat que fala com "algo que
completa texto" através de uma única fronteira: a porta LLMPort.

A lição é a fronteira, não o chat: o resto do programa não sabe (nem pode
saber) se do outro lado há um modelo de verdade ou um eco de testes.
Trocar de provedor = trocar um adapter. Essa porta é a defesa do projeto
inteiro contra o envelhecimento das APIs de modelo — e é a primeira decisão
"hexagonal" do livro, tomada porque dói de verdade, não por cerimônia.

Rodar:  uvicorn app:app --reload   →  http://localhost:8000
Config: LLM_ADAPTER=echo|openai · OPENAI_BASE_URL · OPENAI_API_KEY · LLM_MODEL
"""

import os
from pathlib import Path
from typing import Protocol

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


def _load_dotenv() -> None:
    """Carrega um .env vizinho para os.environ, sem dependência externa.
    A chave de API vive SÓ aqui (arquivo gitignored) ou no ambiente — nunca
    no código. É a regra de ouro do cap. 07: credencial não entra no repo."""
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

# ---------------------------------------------------------------- a porta

Message = dict  # {"role": "user"|"assistant"|"system", "content": str}


class LLMPort(Protocol):
    """A fronteira entre o nosso programa e qualquer modelo de linguagem."""

    def complete(self, messages: list[Message]) -> str: ...


# ------------------------------------------------------------- adapters

class EchoAdapter:
    """Sem rede, sem custo: devolve o que recebeu. Serve para estudar o fluxo
    do programa isolado do modelo — e é o dublê natural dos testes."""

    def complete(self, messages: list[Message]) -> str:
        return f"(echo) você disse: {messages[-1]['content']}"


class OpenAICompatAdapter:
    """Fala o dialeto chat/completions, que virou lingua franca: serve para
    OpenAI, Ollama, OpenRouter, vLLM e afins — mude só a OPENAI_BASE_URL."""

    def __init__(self) -> None:
        self.base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "gpt-5.4-mini")

    def complete(self, messages: list[Message]) -> str:
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": messages},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


def make_llm() -> LLMPort:
    if os.environ.get("LLM_ADAPTER", "echo") == "openai":
        return OpenAICompatAdapter()
    return EchoAdapter()


# ------------------------------------------------------------------ app

app = FastAPI(title="harness-zero · etapa 0")
llm: LLMPort = make_llm()

# Etapa 0: a "memória" é uma lista num processo. Isso vai doer — a conversa
# morre com o restart e não há duas sessões. O capítulo 08 resolve; sentir a
# dor primeiro é o método do livro.
history: list[Message] = []


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(inp: ChatIn) -> dict:
    history.append({"role": "user", "content": inp.message})
    reply = llm.complete(history)
    history.append({"role": "assistant", "content": reply})
    return {"reply": reply}


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse((Path(__file__).parent / "index.html").read_text())
