"""Chat-companion — o backend (harness-zero ao vivo).

Composition root: escolhe os adapters por ambiente (echo/openai, memória/Neon),
monta as portas e expõe a API que o widget do site consome. Fallbacks seguros:
sem chave -> echo; sem DATABASE_URL -> memória. Sobe em qualquer lugar.
"""

from __future__ import annotations

import smtplib
import time
from collections import defaultdict, deque
from email.message import EmailMessage
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import config
from capabilities import MODOS, capacidades, loop_ativo, tools_ativas
from llm import make_llm
from loop import run_turn, run_turn_stream
from ragindex import BookIndex
from store import make_store
from tools import Tools

app = FastAPI(title="chat-companion · Engenharia de Harness")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# --- portas (montadas uma vez) ---
_llm = make_llm(config.LLM_ADAPTER)
_store = make_store(config.DATABASE_URL)
_index = BookIndex(config.REPO_ROOT, config.CORPUS_PATH)
_tools = Tools(_index)

# --- rate limit (spec 049) ---
# Fonte da verdade POR SESSÃO: o store (count_since sobre mensagens `user`
# persistidas) — sobrevive a deploys e vale entre instâncias. O deque em
# memória fica como guarda secundária POR IP (multi-sessão de um mesmo IP)
# e como limitador das sugestões: best-effort, zera no restart, e está ok.
_hits: dict[str, deque] = defaultdict(deque)


def _rate_ok(chave: str, limite: int | None = None) -> bool:
    agora = time.time()
    janela = _hits[chave]
    while janela and janela[0] < agora - config.RATE_LIMIT_WINDOW_S:
        janela.popleft()
    if len(janela) >= (limite if limite is not None else config.RATE_LIMIT_MSGS):
        return False
    janela.append(agora)
    return True


def _rate_ok_chat(session_id: str, ip: str) -> bool:
    persistidas = _store.count_since(session_id, time.time() - config.RATE_LIMIT_WINDOW_S)
    if persistidas >= config.RATE_LIMIT_MSGS:
        return False
    return _rate_ok(f"ip:{ip}", limite=config.RATE_LIMIT_MSGS * config.RATE_LIMIT_IP_FACTOR)


def _system_prompt(chapter: Optional[int], mode: str, achados: list[dict]) -> str:
    caps = [c for c in capacidades(chapter, mode) if c["ativa"]]
    lista = ", ".join(c["rotulo"] for c in caps) or "Tutor do livro"
    ctx = ("\n\nTrechos do livro relevantes (use como evidência e cite a fonte entre colchetes):\n"
           + "\n".join(f"- [{a['fonte']} · {a['titulo']}] {a['trecho']}" for a in achados)
           ) if achados else ""
    modo_txt = ("Modo AVANÇADO: todas as capacidades disponíveis."
                if mode == "avancado" else
                f"Modo PROGRESSIVO: só o que o livro ensinou até o capítulo {chapter or 0}. "
                "Se pedirem algo de um capítulo à frente, explique que aquela capacidade "
                "ainda não foi liberada e de qual capítulo ela vem.")
    return (
        "Você é o companion do livro vivo 'Engenharia de Harness', em português. "
        "Ajuda o leitor a entender o scaffolding que envolve agentes de IA. "
        "Seja preciso e conciso; ancore afirmações no texto do livro; sem inventar fontes. "
        f"Capacidades ativas agora: {lista}. {modo_txt}{ctx}"
    )


# ------------------------------------------------------------------ modelos

class ChatIn(BaseModel):
    session_id: str
    message: str
    chapter: Optional[int] = None
    mode: str = "progressivo"
    byok_key: Optional[str] = None


class SessionIn(BaseModel):
    session_id: str


class SuggestionIn(BaseModel):
    session_id: str
    texto: str
    pagina: Optional[str] = None


# ------------------------------------------------------------------ rotas

@app.get("/health")
def health() -> dict:
    return {"ok": True, "llm": config.LLM_ADAPTER,
            "store": "postgres" if config.DATABASE_URL else "memory"}


@app.get("/capabilities")
def get_capabilities(chapter: Optional[int] = None, mode: str = "progressivo") -> dict:
    if mode not in MODOS:
        mode = "progressivo"
    return {"chapter": chapter, "mode": mode,
            "loop_ativo": loop_ativo(chapter, mode),
            "capabilities": capacidades(chapter, mode)}


@app.post("/session")
def post_session(inp: SessionIn) -> dict:
    _store.ensure_session(inp.session_id)
    return {"session_id": inp.session_id, "ok": True}


@app.get("/history")
def get_history(session_id: str) -> dict:
    return {"session_id": session_id, "messages": _store.history(session_id)}


@app.delete("/session/{session_id}")
def delete_session(session_id: str) -> dict:
    _store.delete_session(session_id)
    return {"session_id": session_id, "deleted": True}


def _enviar_email_sugestao(texto: str, pagina: str, session_id: str) -> bool:
    """Envia a sugestão por email se SMTP estiver configurado. Nunca levanta:
    a sugestão já está persistida; email é best-effort."""
    if not config.SMTP_HOST:
        return False
    try:
        msg = EmailMessage()
        msg["Subject"] = f"[Engenharia de Harness] Sugestão de leitor ({pagina or 'site'})"
        msg["From"] = config.SMTP_USER or "companion@harness"
        msg["To"] = config.SUGGESTION_EMAIL_TO
        msg.set_content(f"Sugestão recebida pelo companion do livro.\n\n"
                        f"Página: {pagina or '-'}\nSessão (anônima): {session_id}\n\n{texto}\n")
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=20) as smtp:
            smtp.starttls()
            if config.SMTP_USER:
                smtp.login(config.SMTP_USER, config.SMTP_PASS)
            smtp.send_message(msg)
        return True
    except Exception:
        return False


@app.post("/suggestion")
def post_suggestion(inp: SuggestionIn, request: Request) -> dict:
    texto = inp.texto.strip()
    if not texto:
        raise HTTPException(status_code=400, detail="sugestão vazia")
    if len(texto) > 4000:
        raise HTTPException(status_code=400, detail="sugestão longa demais (máx. 4000)")
    ip = request.client.host if request.client else "?"
    if not _rate_ok(f"sug:{inp.session_id}:{ip}"):
        raise HTTPException(status_code=429, detail="muitas sugestões; tente mais tarde.")
    _store.ensure_session(inp.session_id)
    _store.add_suggestion(inp.session_id, texto, inp.pagina or "")  # persiste SEMPRE
    email_ok = _enviar_email_sugestao(texto, inp.pagina or "", inp.session_id)
    return {"ok": True, "email_enviado": email_ok}


@app.get("/suggestions")
def get_suggestions(token: str = "") -> dict:
    if not config.ADMIN_TOKEN or token != config.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="token inválido")
    return {"suggestions": _store.suggestions()}


def _preparar_chat(inp: ChatIn, request: Request) -> tuple[str, str, list, set]:
    """Validações, rate-limit, persistência do turno do usuário e montagem do
    histórico — comum ao /chat e ao /chat/stream (spec 047)."""
    if not inp.message.strip():
        raise HTTPException(status_code=400, detail="mensagem vazia")
    mode = inp.mode if inp.mode in MODOS else "progressivo"

    byok = (inp.byok_key or "").strip() if config.ALLOW_BYOK else ""
    if not byok:  # BYOK isenta do limite do projeto
        ip = request.client.host if request.client else "?"
        if not _rate_ok_chat(inp.session_id, ip):
            raise HTTPException(status_code=429,
                                detail="limite de mensagens atingido; tente mais tarde "
                                       "ou use sua própria chave (BYOK).")

    _store.ensure_session(inp.session_id)
    _store.append(inp.session_id, "user", inp.message)

    achados = _index.buscar(inp.message, k=3)  # busca no livro é baseline (sempre)
    history = [{"role": "system", "content": _system_prompt(inp.chapter, mode, achados)}]
    history += _store.history(inp.session_id, limit=40)
    return mode, byok, history, tools_ativas(inp.chapter, mode)


@app.post("/chat")
def chat(inp: ChatIn, request: Request) -> dict:
    mode, byok, history, permitidas = _preparar_chat(inp, request)
    trace: list[str] = []
    try:
        reply = run_turn(history, _llm, _tools, permitidas, trace, byok_key=byok or None)
    except Exception as exc:  # nunca vaza stack para o cliente
        raise HTTPException(status_code=502, detail=f"falha ao consultar o modelo: {exc}")

    _store.append(inp.session_id, "assistant", reply)
    return {"reply": reply, "trace": trace, "mode": mode, "chapter": inp.chapter,
            "capabilities_ativas": [c for c in capacidades(inp.chapter, mode) if c["ativa"]]}


@app.post("/chat/stream")
def chat_stream(inp: ChatIn, request: Request) -> StreamingResponse:
    """Mesmo contrato do /chat, em text/event-stream (spec 047): eventos JSON
    {delta} / {trace} / {done} / {erro}. A resposta do assistente é persistida
    ao final do stream."""
    import json as _json

    mode, byok, history, permitidas = _preparar_chat(inp, request)
    trace: list[str] = []

    def sse(ev: dict) -> str:
        return "data: " + _json.dumps(ev, ensure_ascii=False) + "\n\n"

    def gerar():
        reply = ""
        try:
            for ev in run_turn_stream(history, _llm, _tools, permitidas, trace,
                                      byok_key=byok or None):
                if "reply" in ev:
                    reply = ev["reply"]
                else:
                    yield sse(ev)
        except Exception as exc:  # nunca vaza stack para o cliente
            yield sse({"erro": f"falha ao consultar o modelo: {exc}"})
            return
        _store.append(inp.session_id, "assistant", reply)
        yield sse({"done": True, "reply": reply, "mode": mode, "chapter": inp.chapter,
                   "capabilities_ativas": [c for c in capacidades(inp.chapter, mode) if c["ativa"]]})

    return StreamingResponse(gerar(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
