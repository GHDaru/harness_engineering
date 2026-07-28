"""harness-zero — Etapa 6: permissões. Poder com contenção.

Desde a etapa 1 carregamos uma FERIDA ABERTA de propósito: `read_file` lê
QUALQUER arquivo — inclusive o seu `.env` com a chave da API (teste na etapa
5: "leia o arquivo .env"). E se existisse um `write_file`, o modelo poderia
escrever onde quisesse. O capítulo 07 fecha a ferida com a regra de ouro:
o agente propõe; a POLÍTICA decide; o humano arbitra o meio-termo.

Nasce a **PermissionPolicy** — e repare no desenho (DDD de verdade):
é DOMÍNIO PURO. Uma função sem I/O, sem framework, sem estado:

    decide(tool, args)  ->  "permitir" | "perguntar" | "negar"

  · paths sensíveis (.env, .ssh, chaves…)  ->  NEGAR, sempre (fixo no código,
    como nos harnesses reais — gemini-cli, Claude Code: não é configurável)
  · write_file                             ->  PERGUNTAR (aprovação humana)
  · o resto                                ->  permitir

"Perguntar" exige uma mecânica nova: o turno PAUSA — a chamada pendente é
guardada com um id, o usuário vê [aprovar]/[negar] no chat, e o loop RETOMA
do ponto exato. É o approval flow de todo harness interativo real.
Negação não é exceção: volta como TEXTO para o modelo (ele explica e segue).

Rodar:  uvicorn app:app --reload  →  peça "leia o .env" (negado) e
"escreva um arquivo notas.txt" (aprovação inline).
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
    """Lê um arquivo de texto do disco e retorna até max_chars caracteres."""
    return Path(path).read_text()[:max_chars]


@tools.tool
def write_file(path: str, conteudo: str) -> str:
    """Escreve conteúdo num arquivo de texto (cria ou sobrescreve)."""
    destino = Path(path)
    destino.write_text(conteudo)
    return f"escrito: {destino} ({len(conteudo)} chars)"


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


# ------------------------------------------------- PermissionPolicy (cap. 07)
# DOMÍNIO PURO: sem I/O, sem estado, testável com uma linha. A lista de paths
# sensíveis é FIXA no código de propósito — segurança que o usuário pode
# desligar não é segurança (a regra dos harnesses reais).

PATHS_SENSIVEIS = (".env", ".ssh", "id_rsa", "credentials", "secrets", ".aws", "token")


def decide(tool: str, args: dict) -> str:
    """permitir | perguntar | negar — a política inteira numa função pura."""
    alvo = str(args.get("path", "")).lower()
    if any(p in alvo for p in PATHS_SENSIVEIS):
        return "negar"
    if tool == "write_file":
        return "perguntar"
    return "permitir"


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

def run_turn(session_id: str, store: StorePort, llm: LLMPort, port, trace: list[str],
             mensagens: list[Message] | None = None) -> dict:
    """Agora o turno pode terminar de DOIS jeitos: resposta final, ou PAUSA
    aguardando aprovação (retorna a pendência). `mensagens` != None = retomada."""
    if mensagens is None:
        mensagens = [{"role": "system", "content": contexto.montar()}] + store.history(session_id)
        mensagens = compactador.compactar(mensagens, llm, trace)
    for _ in range(MAX_TURNS):
        reply = llm.complete(mensagens, port.schemas())
        mensagens.append(reply)
        store.append(session_id, reply)

        tool_calls = reply.get("tool_calls") or []
        if not tool_calls:
            return {"reply": reply.get("content") or "", "pendente": None}

        for i, call in enumerate(tool_calls):
            nome = call["function"]["name"]
            args = json.loads(call["function"]["arguments"] or "{}")
            veredicto = decide(nome, args)                      # <- a política
            if veredicto == "negar":
                trace.append(f"🛡 política: NEGADO {nome}({args.get('path','')})")
                resultado = ("erro: acesso negado pela política de permissões "
                             "(path sensível). Explique ao usuário e siga sem esse dado.")
            elif veredicto == "perguntar":
                pid = uuid.uuid4().hex[:8]
                trace.append(f"🛡 política: aguardando aprovação humana para {nome}")
                PENDENTES[pid] = {"session_id": session_id, "mensagens": mensagens,
                                  "calls_restantes": tool_calls[i:], "trace": trace}
                return {"reply": None, "pendente": {
                    "id": pid, "tool": nome, "args": args,
                    "aviso": f"O agente quer executar {nome}({json.dumps(args, ensure_ascii=False)[:120]}). Aprovar?"}}
            else:
                resultado = port.executar(nome, args)
                trace.append(f"🔧 {nome}({json.dumps(args, ensure_ascii=False)})")
            msg = {"role": "tool", "tool_call_id": call["id"], "content": resultado}
            mensagens.append(msg)
            store.append(session_id, msg)

    return {"reply": "(interrompido: limite de turnos atingido)", "pendente": None}


def retomar(pid: str, aprovado: bool) -> dict:
    """Retoma o loop pausado: executa (ou nega) a chamada pendente e continua."""
    p = PENDENTES.pop(pid, None)
    if p is None:
        return {"reply": "(pendência não encontrada ou já resolvida)", "pendente": None, "trace": []}
    mensagens, trace = p["mensagens"], p["trace"]
    for j, call in enumerate(p["calls_restantes"]):
        nome = call["function"]["name"]
        args = json.loads(call["function"]["arguments"] or "{}")
        if j == 0:
            if aprovado:
                resultado = tools.executar(nome, args)
                trace.append(f"✅ humano aprovou: {nome}")
            else:
                resultado = "o humano NEGOU esta ação. Não tente de novo; explique e siga."
                trace.append(f"⛔ humano negou: {nome}")
        else:
            resultado = tools.executar(nome, args) if decide(nome, args) == "permitir" \
                else "erro: bloqueado pela política"
        msg = {"role": "tool", "tool_call_id": call["id"], "content": resultado}
        mensagens.append(msg)
        store.append(p["session_id"], msg)
    r = run_turn(p["session_id"], store, llm, tools, trace, mensagens=mensagens)
    r["trace"] = trace
    return r


# ------------------------------------------------------------------ app

app = FastAPI(title="harness-zero · etapa 6")
llm: LLMPort = make_llm()
store: StorePort = make_store()
PENDENTES: dict[str, dict] = {}  # pausas aguardando o humano (memória: didático)


class ChatIn(BaseModel):
    message: str
    session_id: str | None = None  # sem id -> o servidor cria um (e devolve)


@app.post("/chat")
def chat(inp: ChatIn) -> dict:
    session_id = inp.session_id or uuid.uuid4().hex[:12]
    store.append(session_id, {"role": "user", "content": inp.message})
    trace: list[str] = []
    r = run_turn(session_id, store, llm, tools, trace)
    return {"reply": r["reply"], "pendente": r["pendente"], "trace": trace, "session_id": session_id}


class DecisaoIn(BaseModel):
    id: str


@app.post("/aprovar")
def aprovar(inp: DecisaoIn) -> dict:
    return retomar(inp.id, aprovado=True)


@app.post("/negar")
def negar(inp: DecisaoIn) -> dict:
    return retomar(inp.id, aprovado=False)


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
