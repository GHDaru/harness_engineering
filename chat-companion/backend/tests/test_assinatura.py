"""Spec 080 — e-mail como chave de continuidade (link mágico).

Sem rede e sem banco: adapter echo + MemoryStore, e o envio de e-mail é
monkeypatched. O teste captura o token pelo ponto de envio — nunca pela
resposta HTTP, porque a resposta HTTP NÃO PODE conter o token (é justamente
o que estes testes garantem).
"""

import os
import sys

os.environ.setdefault("LLM_ADAPTER", "echo")
os.environ.pop("DATABASE_URL", None)
os.environ["RATE_LIMIT_ASSINAR"] = "50"
# Os mesmos limites do test_smoke: `config` é lido UMA vez, no primeiro import de
# `app`, e a ordem dos módulos de teste não é garantida. Divergir aqui quebraria
# o outro arquivo dependendo de quem importar primeiro.
os.environ["RATE_LIMIT_MSGS"] = "3"
os.environ["RATE_LIMIT_WINDOW_S"] = "60"
os.environ["RATE_LIMIT_IP_FACTOR"] = "100"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import app as appmod  # noqa: E402

client = TestClient(appmod.app)


@pytest.fixture
def capturar(monkeypatch):
    """Substitui o envio por SMTP e devolve a lista de (email, token, lang)."""
    enviados = []

    def falso(email, token, lang):
        enviados.append({"email": email, "token": token, "lang": lang})
        return True, ""     # spec 084: o envio passou a devolver (ok, motivo)

    monkeypatch.setattr(appmod, "_enviar_link_magico", falso)
    return enviados


def assinar(email, session_id=None, lang="pt"):
    corpo = {"email": email, "lang": lang}
    if session_id:
        corpo["session_id"] = session_id
    return client.post("/assinar", json=corpo)


# ------------------------------------------------------------------ assinar

def test_assinar_envia_link_e_nao_devolve_token(capturar):
    r = assinar("Leitor@Exemplo.COM ")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True and body["enviado"] is True
    # o token não pode aparecer em lugar nenhum da resposta
    assert capturar[0]["token"] not in r.text
    assert set(body) == {"ok", "enviado", "expira_min"}
    # e-mail normalizado (trim + minúsculas)
    assert capturar[0]["email"] == "leitor@exemplo.com"


def test_assinar_email_invalido():
    for ruim in ["", "  ", "sem-arroba", "a@b", "a@b.c d", "x" * 250 + "@e.com"]:
        assert client.post("/assinar", json={"email": ruim}).status_code == 400


def test_assinar_nao_enumera_leitores(capturar):
    primeira = assinar("dup@exemplo.com").json()
    segunda = assinar("dup@exemplo.com").json()   # já cadastrado
    assert primeira == segunda                    # resposta idêntica, byte a byte


def test_assinar_duas_vezes_mantem_a_mesma_sessao_canonica(capturar):
    assinar("estavel@exemplo.com")
    p = client.post("/entrar", json={"token": capturar[-1]["token"]}).json()
    assinar("estavel@exemplo.com")
    s = client.post("/entrar", json={"token": capturar[-1]["token"]}).json()
    assert p["session_id"] == s["session_id"]


def test_rate_limit_por_email(capturar, monkeypatch):
    monkeypatch.setattr(appmod.config, "RATE_LIMIT_ASSINAR", 2)
    appmod._hits.clear()   # a guarda por IP acumulou os assinares dos testes acima
    assert assinar("limite@exemplo.com").status_code == 200
    assert assinar("limite@exemplo.com").status_code == 200
    assert assinar("limite@exemplo.com").status_code == 429


def test_sem_smtp_o_envio_falha_visivelmente(monkeypatch):
    monkeypatch.setattr(appmod.config, "SMTP_HOST", "")
    r = assinar("sem-smtp@exemplo.com")
    assert r.status_code == 200
    assert r.json()["enviado"] is False        # honesto, e sem link na resposta
    assert "http" not in r.text


# ------------------------------------------------------------------ entrar

def test_entrar_adota_sessao_canonica(capturar):
    assinar("entra@exemplo.com")
    r = client.post("/entrar", json={"token": capturar[-1]["token"]})
    assert r.status_code == 200
    d = r.json()
    assert d["email"] == "entra@exemplo.com"
    assert d["session_id"].startswith("leitor-")
    assert client.get("/leitor", params={"session_id": d["session_id"]}).json()["email"] \
        == "entra@exemplo.com"


def test_token_e_de_uso_unico(capturar):
    assinar("unico@exemplo.com")
    tok = capturar[-1]["token"]
    assert client.post("/entrar", json={"token": tok}).status_code == 200
    assert client.post("/entrar", json={"token": tok}).status_code == 400


def test_token_expirado_e_recusado(capturar, monkeypatch):
    monkeypatch.setattr(appmod.config, "MAGIC_LINK_TTL_MIN", 0)
    assinar("expira@exemplo.com")
    assert client.post("/entrar", json={"token": capturar[-1]["token"]}).status_code == 400


def test_token_inexistente_e_recusado():
    assert client.post("/entrar", json={"token": "nao-existe"}).status_code == 400


def test_o_banco_guarda_so_o_hash_do_token(capturar):
    assinar("hash@exemplo.com")
    tok = capturar[-1]["token"]
    guardados = list(appmod._store._links.keys())
    assert tok not in guardados
    assert appmod._hash_token(tok) in guardados


# ------------------------------------------------------------------ fusão

def test_entrar_funde_a_conversa_anterior_a_assinatura(capturar):
    anon = "anon-conversou"
    client.post("/chat", json={"session_id": anon, "message": "o que é um harness?"})
    assinar("funde@exemplo.com", session_id=anon)
    canonico = client.post("/entrar", json={"token": capturar[-1]["token"],
                                            "session_id": anon}).json()["session_id"]

    msgs = client.get("/history", params={"session_id": canonico}).json()["messages"]
    assert any("harness" in m["content"] for m in msgs)
    # a sessão anônima deixou de existir
    assert client.get("/history", params={"session_id": anon}).json()["messages"] == []


def test_fusao_leva_o_objetivo_declarado(capturar):
    anon = "anon-objetivo"
    client.post("/objetivo", json={"session_id": anon, "texto": "migrar meu time para agentes"})
    assinar("obj@exemplo.com", session_id=anon)
    canonico = client.post("/entrar", json={"token": capturar[-1]["token"]}).json()["session_id"]
    assert client.get("/objetivo", params={"session_id": canonico}).json()["objetivo"] \
        == "migrar meu time para agentes"


def test_fusao_nao_engole_a_sessao_de_outro_leitor(capturar):
    assinar("vitima@exemplo.com")
    alvo = client.post("/entrar", json={"token": capturar[-1]["token"]}).json()["session_id"]
    client.post("/chat", json={"session_id": alvo, "message": "conversa privada"})

    assinar("atacante@exemplo.com")
    meu = client.post("/entrar", json={"token": capturar[-1]["token"],
                                       "session_id": alvo}).json()["session_id"]
    assert meu != alvo
    assert client.get("/history", params={"session_id": meu}).json()["messages"] == []
    assert client.get("/history", params={"session_id": alvo}).json()["messages"] != []


# ------------------------------------------------------------------ progresso

def test_progresso_atravessa_navegadores(capturar):
    assinar("progresso@exemplo.com")
    sid = client.post("/entrar", json={"token": capturar[-1]["token"]}).json()["session_id"]

    client.post("/progresso", json={"session_id": sid, "lang": "pt",
                                    "slug": "08-memoria", "titulo": "Memória e estado"})
    client.post("/progresso", json={"session_id": sid, "lang": "en",
                                    "slug": "08-memory", "titulo": "Memory and state"})

    itens = {i["lang"]: i for i in client.get("/progresso", params={"session_id": sid}).json()["itens"]}
    assert itens["pt"]["slug"] == "08-memoria"
    assert itens["en"]["titulo"] == "Memory and state"

    # o último lido substitui o anterior no mesmo idioma
    client.post("/progresso", json={"session_id": sid, "lang": "pt", "slug": "09-planejamento"})
    itens = {i["lang"]: i for i in client.get("/progresso", params={"session_id": sid}).json()["itens"]}
    assert itens["pt"]["slug"] == "09-planejamento" and len(itens) == 2


def test_progresso_rejeita_slug_vazio():
    assert client.post("/progresso", json={"session_id": "s", "slug": "///"}).status_code == 400


# ------------------------------------------------------------------ esquecimento

def test_apagar_leitor_remove_tudo(capturar):
    assinar("apaga@exemplo.com")
    sid = client.post("/entrar", json={"token": capturar[-1]["token"]}).json()["session_id"]
    client.post("/chat", json={"session_id": sid, "message": "oi"})
    client.post("/progresso", json={"session_id": sid, "slug": "01-loop"})

    assert client.request("DELETE", "/leitor", json={"session_id": sid}).json()["apagado"] is True
    assert client.get("/leitor", params={"session_id": sid}).json()["email"] is None
    assert client.get("/history", params={"session_id": sid}).json()["messages"] == []
    assert client.get("/progresso", params={"session_id": sid}).json()["itens"] == []
    # e o e-mail volta a ser assinável do zero
    assert assinar("apaga@exemplo.com").status_code == 200


def test_apagar_sessao_sem_leitor_devolve_false():
    r = client.request("DELETE", "/leitor", json={"session_id": "anon-qualquer"})
    assert r.json()["apagado"] is False


# ------------------------------------------------- spec 084: falha diagnosticável

import smtplib  # noqa: E402
import socket   # noqa: E402
import ssl      # noqa: E402


def test_classe_da_falha_por_excecao():
    """A ordem do mapa importa: `SMTPException` herda de `OSError` em Python 3,
    então um teste de `OSError` no topo classificaria tudo como 'conexao'."""
    casos = [
        (smtplib.SMTPAuthenticationError(535, b"bad"), "auth"),
        (smtplib.SMTPRecipientsRefused({}), "destinatario"),
        (smtplib.SMTPSenderRefused(550, b"no", "de@x.com"), "destinatario"),
        (smtplib.SMTPNotSupportedError("sem STARTTLS"), "tls"),
        (ssl.SSLError("handshake"), "tls"),
        (smtplib.SMTPConnectError(421, b"busy"), "conexao"),
        (smtplib.SMTPServerDisconnected("caiu"), "conexao"),
        (socket.timeout("estourou"), "conexao"),
        (socket.gaierror("dns"), "conexao"),
        (ConnectionRefusedError("porta fechada"), "conexao"),
        (smtplib.SMTPDataError(554, b"rejeitado"), "smtp"),
        (OSError("io"), "conexao"),
        (ValueError("nada a ver"), "outro"),
    ]
    for exc, esperado in casos:
        assert appmod._classe_da_falha(exc) == esperado, (type(exc).__name__, esperado)


def _falhar_com(monkeypatch, exc):
    """Faz o smtplib.SMTP levantar `exc` já na construção."""
    monkeypatch.setattr(appmod.config, "SMTP_HOST", "smtp.exemplo.com")

    def explode(*a, **k):
        raise exc

    monkeypatch.setattr(appmod.smtplib, "SMTP", explode)


def test_assinar_nomeia_a_falha(monkeypatch):
    _falhar_com(monkeypatch, smtplib.SMTPAuthenticationError(535, b"bad credentials"))
    r = assinar("motivo-auth@exemplo.com")
    assert r.status_code == 200
    assert r.json() == {"ok": True, "enviado": False, "expira_min": 30, "motivo": "auth"}


def test_assinar_sem_smtp_diz_desligado(monkeypatch):
    monkeypatch.setattr(appmod.config, "SMTP_HOST", "")
    assert assinar("motivo-desligado@exemplo.com").json()["motivo"] == "desligado"


def test_envio_bem_sucedido_nao_traz_motivo(capturar):
    assert "motivo" not in assinar("sem-motivo@exemplo.com").json()


def test_a_falha_nao_vaza_token_nem_mensagem_do_servidor(monkeypatch, capsys):
    """O detalhe vai para o log do operador; ao cliente, só a classe. A mensagem
    do servidor SMTP pode conter endereço interno ou pista de credencial."""
    _falhar_com(monkeypatch, smtplib.SMTPAuthenticationError(535, b"senha-de-app-invalida"))
    r = assinar("vazamento@exemplo.com")
    assert "senha-de-app-invalida" not in r.text
    assert "smtp.exemplo.com" not in r.text
    erro = capsys.readouterr().err
    assert "[assinar] falha no envio (auth)" in erro   # o operador vê
    assert "https://" not in erro                       # o link mágico, não


def test_health_declara_o_estado_do_smtp(monkeypatch):
    monkeypatch.setattr(appmod.config, "SMTP_HOST", "smtp.exemplo.com")
    assert client.get("/health").json()["smtp"] == "configurado"
    monkeypatch.setattr(appmod.config, "SMTP_HOST", "")
    assert client.get("/health").json()["smtp"] == "desligado"


def test_health_lista_nomes_smtp_mas_nunca_valores(monkeypatch):
    """spec 085: o nome responde 'a variável chegou a este processo?'. O valor
    não pode sair por rota nenhuma — é a senha de app."""
    monkeypatch.setenv("SMTP_HOST", "smtp.exemplo.com")
    monkeypatch.setenv("SMTP_PASS", "senha-secreta-de-app")
    monkeypatch.setenv("SMTP_HOST_COM_ESPACO ", "x")   # o caso que o repr() revela
    r = client.get("/health")
    nomes = r.json()["smtp_vars"]
    assert "'SMTP_HOST'" in nomes
    assert "'SMTP_HOST_COM_ESPACO '" in nomes          # o espaço fica visível
    assert "senha-secreta-de-app" not in r.text
    assert "smtp.exemplo.com" not in r.text
