"""Chat-companion — o backend (harness-zero ao vivo).

Composition root: escolhe os adapters por ambiente (echo/openai, memória/Neon),
monta as portas e expõe a API que o widget do site consome. Fallbacks seguros:
sem chave -> echo; sem DATABASE_URL -> memória. Sobe em qualquer lugar.
"""

from __future__ import annotations

import hashlib
import hmac
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


# ---- spec 093 ----

class ConsentimentoIn(BaseModel):
    session_id: str
    finalidade: str = "contato"
    aceito: bool = False


class DescadastroIn(BaseModel):
    e: str          # sha256 do e-mail, como vem no link de um clique


# ---- spec 096 ----

class AdminEntrarIn(BaseModel):
    session_id: str
    senha: str


# Versão faz parte do registro: mudou o texto, muda a versão, e o aceite velho
# deixa de valer para o texto novo — é o que torna o consentimento auditável em
# vez de declarado. Definidas aqui, acima de todas as rotas, porque `/entrar`
# (spec 080) grava `continuidade` e as rotas da spec 093 gravam `contato`.
VERSAO_CONTINUIDADE = "continuidade-2026-08"
VERSAO_CONTATO = "contato-2026-08"
FINALIDADES = {"continuidade": VERSAO_CONTINUIDADE, "contato": VERSAO_CONTATO}


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
            "site": config.SITE_URL,              # spec 091: base do link magico
            "origens": config.ALLOWED_ORIGINS,    # spec 092: CORS deixa de ser invisivel
            "email": config.transporte_email(),   # spec 087: resend | smtp | desligado
            "admin": config.admin_estado(),        # spec 096: estado, nunca valor
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
def get_telemetry(token: str = "", session_id: str = "") -> dict:
    _exige_admin(token, session_id)
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

    # spec 093: o consentimento de continuidade é registrado AQUI, não no
    # `/assinar` — é neste ponto que a posse do endereço fica provada. Gravar no
    # pedido criaria linha em nome de quem só teve o e-mail digitado por outra
    # pessoa. Só a primeira vez: reentrar não é consentir de novo.
    estado = _store.consentimentos_de(email)
    if not estado.get("continuidade", {}).get("aceito"):
        _store.registrar_consentimento(email, "continuidade", VERSAO_CONTINUIDADE, True)
        estado = _store.consentimentos_de(email)

    return {"ok": True, "email": email, "session_id": canonico,
            "progresso": _store.get_progresso(canonico),
            "consentimentos": estado, "versoes": FINALIDADES}


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


# ---- spec 093: consentimento em camadas (ADR 0010) e progresso visível ----
#
# Duas finalidades, nunca embutidas uma na outra:
#   `continuidade` — o e-mail como chave de progresso (spec 080). Registrada no
#                    `/entrar`, porque é ali que a posse do endereço fica provada;
#                    gravar no `/assinar` criaria linha em nome de quem só teve o
#                    e-mail digitado por um terceiro.
#   `contato`      — avisar sobre livros novos. Perguntada DEPOIS, à parte, e
#                    desmarcada por padrão. Silêncio vale não.
#
# Versão faz parte do registro: mudou o texto, muda a versão, e o aceite velho
# deixa de valer para o texto novo. É o mesmo princípio do consentimento da
# spec 054, agora com histórico — cada "dei" e cada "revoguei" é uma linha.

@app.post("/consentimento")
def post_consentimento(inp: ConsentimentoIn) -> dict:
    """Só `contato` se dá e se revoga por aqui. `continuidade` não é opcional
    para quem assinou (é o que faz a assinatura existir) e sai pelo `/apagar`,
    não por uma caixa — oferecer um botão que não desliga nada seria teatro."""
    if inp.finalidade != "contato":
        raise HTTPException(status_code=400, detail="finalidade não editável")
    email = _store.leitor_por_sessao(inp.session_id)
    if not email:
        raise HTTPException(status_code=403, detail="sessão sem leitor")
    _store.registrar_consentimento(email, "contato", VERSAO_CONTATO, bool(inp.aceito))
    return {"ok": True, "finalidade": "contato", "aceito": bool(inp.aceito),
            "versao": VERSAO_CONTATO}


@app.get("/consentimento")
def get_consentimento(session_id: str) -> dict:
    """Estado atual por finalidade. Sessão anônima devolve vazio — sem erro:
    quem ainda não assinou não tem o que consentir, e a tela precisa saber
    disso sem tratar 'anônimo' como falha."""
    email = _store.leitor_por_sessao(session_id)
    if not email:
        return {"email": None, "consentimentos": {}, "versoes": FINALIDADES}
    return {"email": email, "consentimentos": _store.consentimentos_de(email),
            "versoes": FINALIDADES}


@app.post("/descadastrar")
def post_descadastrar(inp: DescadastroIn) -> dict:
    """Descadastro de um clique (R4): o link de toda mensagem de contato traz o
    sha256 do e-mail, e sair não pede login, formulário nem motivo. O hash entra
    por comparação contra a lista de contato ativa — não há como partir do hash
    para o e-mail, e quem já saiu não aparece, então o endpoint não vira oráculo
    de 'este endereço está cadastrado?'. Resposta idempotente de propósito: sair
    duas vezes diz a mesma coisa."""
    alvo = (inp.e or "").strip().lower()
    if len(alvo) != 64 or not all(c in "0123456789abcdef" for c in alvo):
        raise HTTPException(status_code=400, detail="parâmetro inválido")
    for r in _store.emails_com_contato():
        if _hash_token(r["email"]) == alvo:
            _store.registrar_consentimento(r["email"], "contato", VERSAO_CONTATO, False)
            break
    return {"ok": True}


@app.get("/progresso/detalhe")
def get_progresso_detalhe(session_id: str) -> dict:
    """Quanto o leitor andou. Sem tabela nova: `nav_events` já registra slug ×
    sessão e já segue o leitor na fusão da spec 080. Quem sabe quais slugs são
    capítulo é o site, que tem o sumário — o backend devolve os visitados e não
    finge conhecer a estrutura do livro."""
    return {"session_id": session_id,
            "visitados": _store.capitulos_lidos(session_id),
            "itens": _store.get_progresso(session_id)}


# ---- spec 096: a área do editor ----
#
# Duas portas para o mesmo cômodo, e elas provam coisas diferentes:
#
#   `token=`  — porta de SCRIPT. Senha compartilhada na barra de endereço; serve
#               a `curl` e automação, e é a que já existia.
#   sessão    — porta de PESSOA. O e-mail foi provado pelo link mágico (spec 080)
#               e está em ADMIN_EMAILS, e a senha re-provou intenção agora.
#
# O destranque vive em MEMÓRIA. Reiniciou o serviço, destranca de novo: persistir
# concessão de privilégio é dívida que ninguém revisa, e o custo de redigitar uma
# senha a cada deploy é justamente o que mantém o privilégio curto.
_admin_ate: dict[str, float] = {}


def _sessao_e_editora(session_id: str) -> bool:
    ate = _admin_ate.get((session_id or "").strip())
    if not ate:
        return False
    if ate < time.time():
        _admin_ate.pop(session_id, None)   # expirou: some do mapa, não fica lixo
        return False
    return True


def _exige_admin(token: str = "", session_id: str = "") -> None:
    """403 sem dizer QUAL porta falhou. Distinguir 'token errado' de 'sessão não
    destrancada' entrega metade da porta a quem está tentando."""
    if config.ADMIN_TOKEN and token and hmac.compare_digest(token, config.ADMIN_TOKEN):
        return
    if _sessao_e_editora(session_id):
        return
    raise HTTPException(status_code=403, detail="token inválido")


@app.post("/admin/entrar")
def post_admin_entrar(inp: AdminEntrarIn, request: Request) -> dict:
    """Destranca a área do editor para esta sessão.

    A resposta é IDÊNTICA para e-mail fora da lista e para senha errada — dizer
    qual dos dois falhou diria também qual dos dois está certo."""
    sid = (inp.session_id or "").strip()
    ip = request.client.host if request.client else "?"
    if not _rate_ok(f"admin:{sid}", limite=config.RATE_LIMIT_ADMIN) or \
       not _rate_ok(f"admin-ip:{ip}", limite=config.RATE_LIMIT_ADMIN):
        raise HTTPException(status_code=429, detail="tentativas demais; espere um pouco")

    # Sem as duas variáveis a área não existe — e responde igual a senha errada,
    # para que a ausência de configuração não seja detectável de fora.
    if not config.ADMIN_EMAILS or not config.ADMIN_SENHA:
        raise HTTPException(status_code=403, detail="não autorizado")

    email = (_store.leitor_por_sessao(sid) or "").lower()
    senha_ok = hmac.compare_digest(inp.senha or "", config.ADMIN_SENHA)
    # As duas checagens SEMPRE rodam, e o `and` só decide no fim: sair mais cedo
    # quando o e-mail não confere transformaria o tempo de resposta em oráculo.
    if not (email in config.ADMIN_EMAILS and senha_ok):
        raise HTTPException(status_code=403, detail="não autorizado")

    ate = time.time() + config.ADMIN_SESSAO_MIN * 60
    _admin_ate[sid] = ate
    return {"ok": True, "email": email, "minutos": config.ADMIN_SESSAO_MIN}


@app.get("/admin/estado")
def get_admin_estado(session_id: str = "") -> dict:
    """O painel pergunta isto para saber se desenha a área. Não revela se a
    área EXISTE no servidor — só se esta sessão está destrancada."""
    return {"editor": _sessao_e_editora(session_id),
            "minutos": config.ADMIN_SESSAO_MIN}


@app.get("/leitores")
def get_leitores(token: str = "", session_id: str = "") -> dict:
    """Lista de contato para o editor. Nasce DESLIGADA: sem `ADMIN_TOKEN` no
    ambiente nenhum token confere, como em `/suggestions` e na telemetria de
    administração. Traz só quem tem contato ativo — quem revogou some daqui sem
    perder a continuidade."""
    _exige_admin(token, session_id)
    leitores = _store.emails_com_contato()
    return {"total": len(leitores), "leitores": leitores}


@app.get("/suggestions")
def get_suggestions(token: str = "", session_id: str = "") -> dict:
    _exige_admin(token, session_id)
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
