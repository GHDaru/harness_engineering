"""Chat-companion — o backend (harness-zero ao vivo).

Composition root: escolhe os adapters por ambiente (echo/openai, memória/Neon),
monta as portas e expõe a API que o widget do site consome. Fallbacks seguros:
sem chave -> echo; sem DATABASE_URL -> memória. Sobe em qualquer lugar.
"""

from __future__ import annotations

import hashlib
import re
import secrets
import smtplib
import sys
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


def _system_prompt(chapter: Optional[int], mode: str, achados: list[dict],
                   goal: Optional[str] = None) -> str:
    caps = [c for c in capacidades(chapter, mode) if c["ativa"]]
    lista = ", ".join(c["rotulo"] for c in caps) or "Tutor do livro"
    obj = (f"\n\nObjetivo declarado do leitor: {goal}\n"
           "Conecte as respostas a este objetivo; ao traçar planos de ensino, "
           "sugira a ordem de capítulos e as etapas do harness-zero que melhor o servem, "
           "e sempre aponte o próximo passo concreto.") if goal else ""
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
        f"Capacidades ativas agora: {lista}. {modo_txt}{obj}{ctx}"
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


class ConsentIn(BaseModel):
    session_id: str
    versao: str = "v1"


class TelemetryIn(BaseModel):
    session_id: str
    slug: str


class GoalIn(BaseModel):
    session_id: str
    texto: str


# ---- spec 080 ----

class AssinarIn(BaseModel):
    email: str
    session_id: Optional[str] = None   # sessão anônima de quem pediu (para a fusão)
    lang: str = "pt"


class EntrarIn(BaseModel):
    token: str
    session_id: Optional[str] = None   # sessão anônima do navegador que abriu o link


class ProgressoIn(BaseModel):
    session_id: str
    lang: str = "pt"
    slug: str
    titulo: str = ""


class LeitorIn(BaseModel):
    session_id: str


# ------------------------------------------------------------------ rotas

@app.get("/health")
def health() -> dict:
    """Spec 085: `smtp_vars` lista os NOMES de variáveis de ambiente que começam
    com `SMTP` — nunca os valores. Nasceu de duas rodadas de palpite: o editor
    configurava e redeployava, e o processo continuava sem ver `SMTP_HOST`. Nome
    é o que responde à pergunta que restava — a variável chegou a este serviço?
    veio com typo? veio com espaço no fim? — e nome não é segredo."""
    import os

    return {"ok": True, "llm": config.LLM_ADAPTER,
            "store": "postgres" if config.DATABASE_URL else "memory",
            "email": config.transporte_email(),   # spec 087: resend | smtp | desligado
            "smtp": "configurado" if config.SMTP_HOST else "desligado",
            "smtp_porta": config.SMTP_PORT,   # spec 086: número de porta não é segredo
            "smtp_vars": sorted(repr(k) for k in os.environ if k.upper().startswith("SMTP"))}


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
    """Best-effort, ao contrário do link mágico: a sugestão já está persistida no
    banco, então o e-mail é bônus. Desde a spec 087 usa o mesmo transporte."""
    ok, _ = _enviar_email(
        config.SUGGESTION_EMAIL_TO,
        f"[Engenharia de Harness] Sugestão de leitor ({pagina or 'site'})",
        f"Sugestão recebida pelo companion do livro.\n\n"
        f"Página: {pagina or '-'}\nSessão (anônima): {session_id}\n\n{texto}\n")
    return ok


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


# ---- spec 054: consentimento, telemetria e objetivo ----

@app.post("/consent")
def post_consent(inp: ConsentIn) -> dict:
    """Grava o aceite do disclaimer (sessão anônima + versão do texto).
    Auditável: mudou o texto ⇒ nova versão ⇒ novo aceite."""
    _store.ensure_session(inp.session_id)
    _store.record_consent(inp.session_id, inp.versao[:20])
    return {"ok": True, "versao": inp.versao[:20]}


@app.post("/telemetry")
def post_telemetry(inp: TelemetryIn) -> dict:
    """Navegação anônima (slug×sessão) — só grava com consentimento da sessão.
    Best-effort por design: nunca é obstáculo para o leitor."""
    slug = "".join(c for c in inp.slug.lower() if c.isalnum() or c in "-_.")[:80]
    if not slug or not _store.has_consent(inp.session_id):
        return {"ok": False}
    _store.add_nav(inp.session_id, slug)
    return {"ok": True}


@app.get("/telemetry/publico")
def get_telemetry_publico() -> dict:
    """Projeção pública do uso do livro (spec 055): SÓ agregados por página —
    sem sessões, sem timestamps, sem token. Alimenta o Apêndice — Uso do livro."""
    stats = _store.nav_stats()
    por = stats.get("por_pagina", {})
    return {"total": stats.get("total", 0), "paginas_distintas": len(por), "por_pagina": por}


@app.get("/telemetry")
def get_telemetry(token: str = "") -> dict:
    if not config.ADMIN_TOKEN or token != config.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="token inválido")
    return _store.nav_stats()


@app.post("/objetivo")
def post_objetivo(inp: GoalIn) -> dict:
    texto = inp.texto.strip()[:300]
    if not texto:
        raise HTTPException(status_code=400, detail="objetivo vazio")
    _store.ensure_session(inp.session_id)
    _store.set_goal(inp.session_id, texto)
    return {"ok": True, "objetivo": texto}


@app.get("/objetivo")
def get_objetivo(session_id: str) -> dict:
    return {"session_id": session_id, "objetivo": _store.get_goal(session_id)}


# ---- spec 080: e-mail como chave de continuidade (link mágico) ----
#
# Não é login: sem senha, sem sessão autenticada, sem área restrita. O e-mail
# aponta para um `session_id` canônico; adotar esse id é o que faz histórico,
# objetivo, consentimento e progresso atravessarem dispositivos.

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _normalizar_email(bruto: str) -> str:
    email = (bruto or "").strip().lower()
    if len(email) > 254 or not _EMAIL_RE.match(email):
        raise HTTPException(status_code=400, detail="e-mail inválido")
    return email


def _link_magico(token: str, lang: str) -> str:
    base = config.SITE_URL.rstrip("/") + "/"
    pagina = "en/entrar.html" if lang == "en" else "entrar.html"
    return f"{base}{pagina}?t={token}"


def _enviar_por_resend(para: str, assunto: str, corpo: str) -> tuple[bool, str]:
    """Envio por API HTTP (spec 087). A chave vai no header e NUNCA em log,
    resposta ou artefato — mesmo tratamento da chave do LLM."""
    import httpx

    try:
        r = httpx.post(
            config.RESEND_URL,
            headers={"Authorization": f"Bearer {config.RESEND_API_KEY}",
                     "content-type": "application/json"},
            json={"from": config.EMAIL_FROM, "to": [para],
                  "subject": assunto, "text": corpo},
            timeout=20,
        )
        if r.status_code < 300:
            return True, ""
        # O corpo do erro pode citar domínio e remetente: vai para o log do
        # operador, nunca para o cliente.
        classe = ("auth" if r.status_code in (401, 403)
                  else "destinatario" if r.status_code in (400, 422)
                  else "limite" if r.status_code == 429
                  else "api")
        print(f"[email] resend recusou ({classe}) HTTP {r.status_code}: {r.text[:300]}",
              file=sys.stderr, flush=True)
        return False, classe
    except Exception as exc:
        classe = _classe_da_falha(exc)
        print(f"[email] resend falhou ({classe}): {type(exc).__name__}: {exc}",
              file=sys.stderr, flush=True)
        return False, classe


def _enviar_email(para: str, assunto: str, corpo: str) -> tuple[bool, str]:
    """Porta única de saída de e-mail. O transporte é detalhe de ambiente;
    quem chama só quer saber se foi e, se não foi, por quê."""
    transporte = config.transporte_email()
    if transporte == "desligado":
        return False, "desligado"
    if transporte == "resend":
        return _enviar_por_resend(para, assunto, corpo)
    try:
        msg = EmailMessage()
        msg["Subject"] = assunto
        msg["From"] = config.SMTP_USER or "companion@harness"
        msg["To"] = para
        msg.set_content(corpo)
        with _abrir_smtp() as smtp:
            if config.SMTP_USER:
                smtp.login(config.SMTP_USER, config.SMTP_PASS)
            smtp.send_message(msg)
        return True, ""
    except Exception as exc:
        classe = _classe_da_falha(exc)
        print(f"[email] smtp falhou ({classe}): {type(exc).__name__}: {exc}",
              file=sys.stderr, flush=True)
        return False, classe


def _abrir_smtp():
    """Spec 086: a porta decide o protocolo, e errar isso parece falha de rede.

    465 é TLS **implícito** — o servidor espera o handshake imediatamente, então
    um `SMTP` em texto claro seguido de `starttls()` fica pendurado até estourar
    o timeout e chega aqui como `conexao`, indistinguível de porta bloqueada.
    587 é STARTTLS: conecta em claro e negocia depois."""
    if config.SMTP_PORT == 465:
        return smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, timeout=20)
    smtp = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=20)
    smtp.starttls()
    return smtp


def _classe_da_falha(exc: BaseException) -> str:
    """Classe GROSSEIRA da falha de envio (spec 084). Nunca a mensagem do
    servidor: ela pode conter endereço, host interno ou pista de credencial."""
    import socket
    import ssl

    # A ORDEM importa: em Python 3 `smtplib.SMTPException` herda de `OSError`,
    # então um `isinstance(exc, OSError)` no topo engoliria todas as específicas.
    if isinstance(exc, smtplib.SMTPAuthenticationError):
        return "auth"
    if isinstance(exc, (smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused)):
        return "destinatario"
    if isinstance(exc, (smtplib.SMTPNotSupportedError, ssl.SSLError)):
        return "tls"
    if isinstance(exc, (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected,
                        socket.timeout, socket.gaierror, ConnectionError)):
        return "conexao"
    if isinstance(exc, smtplib.SMTPException):
        return "smtp"
    if isinstance(exc, OSError):
        return "conexao"
    return "outro"


def _enviar_link_magico(email: str, token: str, lang: str) -> tuple[bool, str]:
    """Diferente da sugestão, aqui o envio NÃO é best-effort: se falhar, o leitor
    precisa saber — ficou sem o link e não há outro caminho.

    Spec 084: falhar em silêncio era pior que falhar. Spec 087: o transporte
    saiu do SMTP (bloqueado no PaaS) e virou detalhe de `_enviar_email`. O token
    continua fora de log, de resposta e de artefato."""
    if config.transporte_email() == "desligado":
        return False, "desligado"
    link = _link_magico(token, lang)
    en = lang == "en"
    assunto = ("[Harness Engineering] Your reading link" if en
               else "[Engenharia de Harness] Seu link de leitura")
    corpo = (f"Open this link to pick your reading up where you left off:\n\n{link}\n\n"
             f"It works once and expires in {config.MAGIC_LINK_TTL_MIN} minutes.\n"
             "If you did not ask for it, ignore this message — nothing was created "
             "under your name and you will not receive anything else.\n"
             if en else
             f"Abra este link para retomar sua leitura de onde parou:\n\n{link}\n\n"
             f"Ele vale uma vez e expira em {config.MAGIC_LINK_TTL_MIN} minutos.\n"
             "Se não foi você que pediu, ignore esta mensagem — nada foi criado em "
             "seu nome e você não receberá mais nada.\n")
    return _enviar_email(email, assunto, corpo)


@app.post("/assinar")
def post_assinar(inp: AssinarIn, request: Request) -> dict:
    """Envia o link mágico. A resposta é IDÊNTICA para e-mail novo e já cadastrado
    — quem tem a caixa de entrada descobre; quem só tem o formulário, não."""
    email = _normalizar_email(inp.email)
    ip = request.client.host if request.client else "?"
    if not _rate_ok(f"assin:{email}", limite=config.RATE_LIMIT_ASSINAR) or \
       not _rate_ok(f"assin-ip:{ip}", limite=config.RATE_LIMIT_ASSINAR):
        raise HTTPException(status_code=429, detail="muitos pedidos; tente mais tarde.")

    if not _store.leitor_por_email(email):
        # Sessão canônica com entropia do SERVIDOR — não derivada do e-mail e não
        # gerada pelo navegador: este id passa a valer como credencial de fato.
        _store.criar_leitor(email, "leitor-" + secrets.token_urlsafe(24))

    token = secrets.token_urlsafe(32)
    _store.salvar_link(_hash_token(token), email,
                       time.time() + config.MAGIC_LINK_TTL_MIN * 60,
                       (inp.session_id or "").strip())
    enviado, motivo = _enviar_link_magico(email, token, "en" if inp.lang == "en" else "pt")
    resp = {"ok": True, "enviado": enviado, "expira_min": config.MAGIC_LINK_TTL_MIN}
    if not enviado:
        resp["motivo"] = motivo
    return resp


@app.post("/entrar")
def post_entrar(inp: EntrarIn) -> dict:
    """Consome o link (uso único) e devolve a sessão canônica do leitor. Funde
    as sessões anônimas envolvidas: a de quem pediu o link e a de quem o abriu —
    por construção, a mesma pessoa. Quem conversou antes de assinar não perde
    a conversa."""
    dados = _store.consumir_link(_hash_token((inp.token or "").strip()), time.time())
    if not dados:
        raise HTTPException(status_code=400, detail="link inválido, expirado ou já usado")

    email = dados["email"]
    canonico = _store.leitor_por_email(email)
    if not canonico:  # leitor apagado entre o pedido e o clique
        canonico = _store.criar_leitor(email, "leitor-" + secrets.token_urlsafe(24))

    for anonima in {(dados.get("origem") or "").strip(), (inp.session_id or "").strip()}:
        if anonima and anonima != canonico and not _store.leitor_por_sessao(anonima):
            _store.merge_session(anonima, canonico)

    return {"ok": True, "email": email, "session_id": canonico,
            "progresso": _store.get_progresso(canonico)}


@app.get("/leitor")
def get_leitor(session_id: str) -> dict:
    return {"session_id": session_id, "email": _store.leitor_por_sessao(session_id)}


@app.delete("/leitor")
def delete_leitor(inp: LeitorIn) -> dict:
    """Direito ao esquecimento (Princípio V): apaga leitor, sessão, mensagens,
    progresso e links pendentes. Sessão sem leitor devolve `apagado: false`."""
    return {"apagado": _store.apagar_leitor(inp.session_id)}


@app.post("/progresso")
def post_progresso(inp: ProgressoIn) -> dict:
    slug = "".join(c for c in inp.slug.lower() if c.isalnum() or c in "-_.")[:80]
    if not slug:
        raise HTTPException(status_code=400, detail="slug inválido")
    _store.ensure_session(inp.session_id)
    _store.set_progresso(inp.session_id, "en" if inp.lang == "en" else "pt",
                         slug, inp.titulo.strip()[:200])
    return {"ok": True}


@app.get("/progresso")
def get_progresso(session_id: str) -> dict:
    return {"session_id": session_id, "itens": _store.get_progresso(session_id)}


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
    goal = _store.get_goal(inp.session_id)  # objetivo do leitor como camada (spec 054)
    history = [{"role": "system", "content": _system_prompt(inp.chapter, mode, achados, goal)}]
    history += _store.history(inp.session_id, limit=40)
    return mode, byok, history, tools_ativas(inp.chapter, mode), achados


def _debug(achados: list, history: list, trace: list, chapter, mode: str, session_id: str = "") -> dict:
    """Bloco de transparência dos Bastidores (spec 053): o que foi injetado e
    quanto custa — dados que o backend já computava e descartava. Tokens são
    ESTIMADOS (~chars/4); o widget exibe sempre com '~'."""
    chars = sum(len(str(m.get("content") or "")) for m in history)
    return {
        "trechos": [{"fonte": a.get("fonte", ""), "titulo": a.get("titulo", ""),
                     "preview": str(a.get("trecho", ""))[:90]} for a in achados],
        "historico_msgs": max(0, len(history) - 1),  # sem contar o system
        "prompt_chars": chars,
        "tokens_estimados": chars // 4,
        "janela_tokens": config.CONTEXT_WINDOW_TOKENS,
        "tools_executadas": len(trace),
        "modo": mode,
        "capacidades_ativas": [c["rotulo"] for c in capacidades(chapter, mode) if c["ativa"]],
        "objetivo": _store.get_goal(session_id) if session_id else None,
    }


@app.post("/chat")
def chat(inp: ChatIn, request: Request) -> dict:
    mode, byok, history, permitidas, achados = _preparar_chat(inp, request)
    trace: list[str] = []
    try:
        reply = run_turn(history, _llm, _tools, permitidas, trace, byok_key=byok or None)
    except Exception as exc:  # nunca vaza stack para o cliente
        raise HTTPException(status_code=502, detail=f"falha ao consultar o modelo: {exc}")

    _store.append(inp.session_id, "assistant", reply)
    return {"reply": reply, "trace": trace, "mode": mode, "chapter": inp.chapter,
            "capabilities_ativas": [c for c in capacidades(inp.chapter, mode) if c["ativa"]],
            "debug": _debug(achados, history, trace, inp.chapter, mode, inp.session_id)}


@app.post("/chat/stream")
def chat_stream(inp: ChatIn, request: Request) -> StreamingResponse:
    """Mesmo contrato do /chat, em text/event-stream (spec 047): eventos JSON
    {delta} / {trace} / {done} / {erro}. A resposta do assistente é persistida
    ao final do stream."""
    import json as _json

    mode, byok, history, permitidas, achados = _preparar_chat(inp, request)
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
                   "capabilities_ativas": [c for c in capacidades(inp.chapter, mode) if c["ativa"]],
                   "debug": _debug(achados, history, trace, inp.chapter, mode, inp.session_id)})

    return StreamingResponse(gerar(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
