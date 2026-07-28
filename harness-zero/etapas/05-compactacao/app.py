"""harness-zero — Etapa 5: compactação. A escada que faz caber na janela.

A etapa 4 deixou as conversas persistirem — e criou o próximo problema:
conversas longas ESTOURAM a janela de contexto do modelo. O capítulo 04
ensina o padrão consolidado nos harnesses reais: uma ESCADA de agressividade,
do barato ao caro, acionada por um orçamento:

    degrau 1 — TRUNCAR   resultados de ferramenta antigos (baratíssimo)
    degrau 2 — PODAR     turnos antigos inteiros (barato, perde detalhe)
    degrau 3 — SUMARIZAR o que foi podado via LLMPort (caro, preserva o fio)

Nasce o **Compactador**: mede o uso (aqui, caracteres como proxy didático de
tokens), aplica o degrau mais barato que resolve, e AVISA no trace ("🗜 ...")
— compactação silenciosa é dívida invisível (cap. 04). O histórico persistido
(etapa 4) fica INTACTO no store; compacta-se só a visão enviada ao modelo —
a distinção registro × janela é a lição central.

Rodar:  uvicorn app:app --reload  →  converse bastante e observe o trace.
Para forçar a escada sem conversar muito: ORCAMENTO_CHARS=800 uvicorn app:app
"""

import datetime
import inspect
import json
import os
import platform
import sqlite3
import typing
import uuid
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


# ------------------------------------------------------------- StorePort

class StorePort(Protocol):
    def append(self, session_id: str, msg: Message) -> None: ...
    def history(self, session_id: str) -> list[Message]: ...
    def sessions(self) -> list[dict]: ...


class MemoriaStore:
    """A etapa 0-3 em forma de adapter: some no restart. Fica como contraste."""

    def __init__(self) -> None:
        self._por_sessao: dict[str, list[Message]] = {}

    def append(self, session_id: str, msg: Message) -> None:
        self._por_sessao.setdefault(session_id, []).append(msg)

    def history(self, session_id: str) -> list[Message]:
        return list(self._por_sessao.get(session_id, []))

    def sessions(self) -> list[dict]:
        return [{"session_id": s, "mensagens": len(m)} for s, m in self._por_sessao.items()]


class SQLiteStore:
    """Persistência real: um arquivo .db ao lado do app. A conversa sobrevive
    ao restart — teste: converse, mate o servidor, suba de novo, continue."""

    def __init__(self, caminho: Path) -> None:
        self._caminho = str(caminho)
        with self._conn() as c:
            c.execute("""CREATE TABLE IF NOT EXISTS mensagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                papel TEXT NOT NULL,
                corpo TEXT NOT NULL,
                criada_em TEXT NOT NULL DEFAULT (datetime('now')))""")

    def _conn(self):
        return sqlite3.connect(self._caminho)

    def append(self, session_id: str, msg: Message) -> None:
        with self._conn() as c:
            c.execute("INSERT INTO mensagens(session_id, papel, corpo) VALUES (?,?,?)",
                      (session_id, msg.get("role", "?"), json.dumps(msg, ensure_ascii=False)))

    def history(self, session_id: str) -> list[Message]:
        with self._conn() as c:
            rows = c.execute("SELECT corpo FROM mensagens WHERE session_id=? ORDER BY id",
                             (session_id,)).fetchall()
        return [json.loads(r[0]) for r in rows]

    def sessions(self) -> list[dict]:
        with self._conn() as c:
            rows = c.execute("""SELECT session_id, count(*), max(criada_em)
                                FROM mensagens GROUP BY session_id ORDER BY 3 DESC""").fetchall()
        return [{"session_id": r[0], "mensagens": r[1], "ultima_em": r[2]} for r in rows]


def make_store() -> StorePort:
    if os.environ.get("STORE_ADAPTER", "sqlite") == "memoria":
        return MemoriaStore()
    return SQLiteStore(AQUI / "sessoes.db")


# ------------------------------------------- MontadorDeContexto (etapa 3)

class MontadorDeContexto:
    def montar(self) -> str:
        regras = (AQUI / "AGENTS.md")
        return "\n\n---\n\n".join([
            "Você é o assistente do harness-zero, a trilha prática do livro "
            "Engenharia de Harness. Você tem ferramentas; use-as quando ajudarem.",
            f"Ambiente: {platform.system()} · Python {platform.python_version()} · "
            f"agora é {datetime.datetime.now().isoformat(timespec='minutes')}.",
            f"Regras do projeto (AGENTS.md — siga-as):\n\n{regras.read_text()}"
            if regras.exists() else "(sem AGENTS.md)",
        ])


contexto = MontadorDeContexto()


# ------------------------------------------------------- ToolPort (etapa 2)

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
        n = sum(1 for m in messages if m["role"] != "system")
        return {"role": "assistant",
                "content": f"(echo) você disse: {messages[-1]['content']} "
                           f"[esta sessão tem {n} mensagens — mate o servidor e volte: elas ficam]"}


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


# ---------------------------------------------------------- Compactador

ORCAMENTO_CHARS = int(os.environ.get("ORCAMENTO_CHARS", "6000"))


class Compactador:
    """A escada do cap. 04. Opera sobre a VISÃO (lista enviada ao modelo),
    nunca sobre o registro persistido. Cada degrau reporta o que fez."""

    def _uso(self, msgs: list[Message]) -> int:
        return sum(len(json.dumps(m, ensure_ascii=False)) for m in msgs)

    def _truncar_tools(self, msgs: list[Message]) -> int:
        n = 0
        for m in msgs[:-6]:  # preserva o final da conversa
            if m.get("role") == "tool" and len(m.get("content", "")) > 200:
                m["content"] = m["content"][:200] + " …[truncado pelo compactador]"
                n += 1
        return n

    def _podar(self, msgs: list[Message]) -> list[Message]:
        # mantém system + os 8 últimos; o que sai vai para o degrau 3
        return msgs[:1] + msgs[-8:] if len(msgs) > 9 else msgs

    def compactar(self, msgs: list[Message], llm: "LLMPort", trace: list[str]) -> list[Message]:
        if self._uso(msgs) <= ORCAMENTO_CHARS:
            return msgs
        # degrau 1 — truncar tool-results antigos
        n = self._truncar_tools(msgs)
        if n:
            trace.append(f"🗜 compactador: degrau 1 — {n} resultado(s) de tool truncado(s)")
        if self._uso(msgs) <= ORCAMENTO_CHARS:
            return msgs
        # degrau 2 — podar turnos antigos (guardando-os para o resumo)
        podados = msgs[1:-8] if len(msgs) > 9 else []
        msgs = self._podar(msgs)
        trace.append(f"🗜 compactador: degrau 2 — {len(podados)} mensagem(ns) podada(s)")
        if not podados or self._uso(msgs) <= ORCAMENTO_CHARS * 1.2:
            return msgs
        # degrau 3 — sumarizar o podado via LLMPort (caro; preserva o fio)
        texto = "\n".join(f"{m.get('role')}: {str(m.get('content'))[:300]}" for m in podados)
        resumo = llm.complete([{"role": "user", "content":
            "Resuma em até 5 linhas os fatos e decisões desta conversa "
            "(será a memória do agente):\n\n" + texto}], [])
        msgs.insert(1, {"role": "system",
                        "content": "Resumo da conversa anterior (compactada): "
                                   + (resumo.get("content") or "")[:800]})
        trace.append("🗜 compactador: degrau 3 — resumo gerado e injetado")
        return msgs


compactador = Compactador()


# ------------------------------------------------------------- O LOOP
# Igual à etapa 3, mas quem guarda mensagens agora é o StorePort.

def run_turn(session_id: str, store: StorePort, llm: LLMPort, port, trace: list[str]) -> str:
    mensagens = [{"role": "system", "content": contexto.montar()}] + store.history(session_id)
    mensagens = compactador.compactar(mensagens, llm, trace)  # a escada age na VISÃO
    for _ in range(MAX_TURNS):
        reply = llm.complete(mensagens, port.schemas())
        mensagens.append(reply)
        store.append(session_id, reply)

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
            store.append(session_id, msg)

    return "(interrompido: limite de turnos atingido)"


# ------------------------------------------------------------------ app

app = FastAPI(title="harness-zero · etapa 5")
llm: LLMPort = make_llm()
store: StorePort = make_store()


class ChatIn(BaseModel):
    message: str
    session_id: str | None = None  # sem id -> o servidor cria um (e devolve)


@app.post("/chat")
def chat(inp: ChatIn) -> dict:
    session_id = inp.session_id or uuid.uuid4().hex[:12]
    store.append(session_id, {"role": "user", "content": inp.message})
    trace: list[str] = []
    reply = run_turn(session_id, store, llm, tools, trace)
    return {"reply": reply, "trace": trace, "session_id": session_id}


@app.get("/contexto_uso")
def contexto_uso(session_id: str) -> dict:
    """Janela de observação: uso atual da janela × orçamento (antes de compactar)."""
    msgs = [{"role": "system", "content": contexto.montar()}] + store.history(session_id)
    return {"session_id": session_id, "chars": compactador._uso(msgs),
            "orcamento": ORCAMENTO_CHARS, "mensagens": len(msgs)}


@app.get("/sessions")
def listar_sessions() -> dict:
    """Janela de observação: as conversas que o store conhece (o /resume)."""
    return {"sessions": store.sessions()}


@app.get("/history")
def ver_history(session_id: str) -> dict:
    return {"session_id": session_id, "messages": store.history(session_id)}


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse((Path(__file__).parent / "index.html").read_text())
