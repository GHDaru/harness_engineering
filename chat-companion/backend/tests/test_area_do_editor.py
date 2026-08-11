"""Spec 096 — a área do editor: e-mail provado + senha.

O que estes testes protegem não é uma funcionalidade, é uma **fronteira**. As
asserções que mais importam são as negativas: sem as variáveis nada existe, e a
resposta de "e-mail fora da lista" é indistinguível da de "senha errada" — dizer
qual dos dois falhou diria também qual dos dois está certo.

Sem rede e sem banco: adapter echo + MemoryStore, envio monkeypatched.
"""

import os
import sys
import time

os.environ.setdefault("LLM_ADAPTER", "echo")
os.environ.pop("DATABASE_URL", None)
os.environ["RATE_LIMIT_ASSINAR"] = "50"
os.environ["RATE_LIMIT_MSGS"] = "3"
os.environ["RATE_LIMIT_WINDOW_S"] = "60"
os.environ["RATE_LIMIT_IP_FACTOR"] = "100"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import app as appmod  # noqa: E402

client = TestClient(appmod.app)

EDITOR = "editor@exemplo.com"
SENHA = "uma-senha-longa-de-verdade"


@pytest.fixture
def capturar(monkeypatch):
    enviados = []

    def falso(email, token, lang):
        enviados.append({"email": email, "token": token, "lang": lang})
        return True, ""

    monkeypatch.setattr(appmod, "_enviar_link_magico", falso)
    return enviados


@pytest.fixture(autouse=True)
def limpar_destranques():
    """Cada teste começa com ninguém destrancado — privilégio não vaza entre casos."""
    appmod._admin_ate.clear()
    appmod._hits.clear()
    yield
    appmod._admin_ate.clear()


@pytest.fixture
def configurado(monkeypatch):
    monkeypatch.setattr(appmod.config, "ADMIN_EMAILS", [EDITOR])
    monkeypatch.setattr(appmod.config, "ADMIN_SENHA", SENHA)
    monkeypatch.setattr(appmod.config, "ADMIN_TOKEN", "")


def entrar(capturar, email):
    """Assina e abre o link — devolve a sessão canônica, com o e-mail provado."""
    appmod._hits.clear()
    client.post("/assinar", json={"email": email})
    return client.post("/entrar", json={"token": capturar[-1]["token"]}).json()["session_id"]


def destrancar(sid, senha=SENHA):
    return client.post("/admin/entrar", json={"session_id": sid, "senha": senha})


# ------------------------------------------- sem configuração, nada existe

def test_sem_variaveis_a_area_nao_existe(capturar, monkeypatch):
    """O default é desligado. Nem o e-mail certo destranca sem senha configurada."""
    monkeypatch.setattr(appmod.config, "ADMIN_EMAILS", [])
    monkeypatch.setattr(appmod.config, "ADMIN_SENHA", "")
    sid = entrar(capturar, EDITOR)
    assert destrancar(sid).status_code == 403
    assert client.get("/admin/estado", params={"session_id": sid}).json()["editor"] is False


def test_so_emails_sem_senha_nao_basta(capturar, monkeypatch):
    monkeypatch.setattr(appmod.config, "ADMIN_EMAILS", [EDITOR])
    monkeypatch.setattr(appmod.config, "ADMIN_SENHA", "")
    sid = entrar(capturar, EDITOR)
    assert destrancar(sid, "qualquer").status_code == 403


def test_so_senha_sem_emails_nao_basta(capturar, monkeypatch):
    monkeypatch.setattr(appmod.config, "ADMIN_EMAILS", [])
    monkeypatch.setattr(appmod.config, "ADMIN_SENHA", SENHA)
    sid = entrar(capturar, EDITOR)
    assert destrancar(sid, SENHA).status_code == 403


# ------------------------------------------------------- o caminho feliz

def test_email_provado_mais_senha_destranca(capturar, configurado):
    sid = entrar(capturar, EDITOR)
    r = destrancar(sid)
    assert r.status_code == 200
    assert r.json()["email"] == EDITOR
    assert client.get("/admin/estado", params={"session_id": sid}).json()["editor"] is True


def test_o_email_e_comparado_sem_caso(capturar, configurado, monkeypatch):
    """`/assinar` normaliza para minúsculas; a lista também. Um `ADMIN_EMAILS`
    digitado com maiúscula no painel do Railway não pode trancar o editor fora."""
    monkeypatch.setattr(appmod.config, "ADMIN_EMAILS", [EDITOR])
    sid = entrar(capturar, EDITOR.upper())
    assert destrancar(sid).status_code == 200


# ------------------------------------------------------- as recusas, e o silêncio

def test_senha_errada_nao_destranca(capturar, configurado):
    sid = entrar(capturar, EDITOR)
    assert destrancar(sid, "errada").status_code == 403
    assert client.get("/admin/estado", params={"session_id": sid}).json()["editor"] is False


def test_leitor_comum_com_a_senha_certa_nao_destranca(capturar, configurado):
    """A senha sozinha não basta: é preciso ser um dos e-mails provados."""
    sid = entrar(capturar, "leitor-comum@exemplo.com")
    assert destrancar(sid, SENHA).status_code == 403


def test_sessao_anonima_nao_destranca(configurado):
    assert destrancar("anon-sem-leitor", SENHA).status_code == 403


def test_email_errado_e_senha_errada_sao_indistinguiveis(capturar, configurado):
    """A asserção central da spec: quem tenta não descobre QUAL metade acertou."""
    editor = entrar(capturar, EDITOR)
    outro = entrar(capturar, "outro@exemplo.com")

    a = destrancar(editor, "senha-errada")     # e-mail certo, senha errada
    b = destrancar(outro, SENHA)               # e-mail errado, senha certa
    c = destrancar(outro, "senha-errada")      # os dois errados

    assert a.status_code == b.status_code == c.status_code == 403
    assert a.json() == b.json() == c.json()


def test_rate_limit_nas_tentativas(capturar, configurado, monkeypatch):
    monkeypatch.setattr(appmod.config, "RATE_LIMIT_ADMIN", 3)
    sid = entrar(capturar, EDITOR)
    appmod._hits.clear()
    for _ in range(3):
        assert destrancar(sid, "errada").status_code == 403
    assert destrancar(sid, SENHA).status_code == 429   # nem a senha certa passa


# ------------------------------------------------------------- expiração

def test_o_destranque_expira(capturar, configurado, monkeypatch):
    monkeypatch.setattr(appmod.config, "ADMIN_SESSAO_MIN", 30)
    sid = entrar(capturar, EDITOR)
    destrancar(sid)
    assert client.get("/admin/estado", params={"session_id": sid}).json()["editor"] is True

    appmod._admin_ate[sid] = time.time() - 1     # como se meia hora tivesse passado
    assert client.get("/admin/estado", params={"session_id": sid}).json()["editor"] is False
    assert sid not in appmod._admin_ate          # expirado sai do mapa, não vira lixo


# --------------------------------------------------- as duas portas do cômodo

@pytest.mark.parametrize("rota", ["/leitores", "/suggestions", "/telemetry"])
def test_rota_admin_aceita_sessao_destrancada(capturar, configurado, rota):
    sid = entrar(capturar, EDITOR)
    assert client.get(rota).status_code == 403
    destrancar(sid)
    assert client.get(rota, params={"session_id": sid}).status_code == 200


@pytest.mark.parametrize("rota", ["/leitores", "/suggestions", "/telemetry"])
def test_rota_admin_aceita_token_de_script(monkeypatch, rota):
    """A porta de script continua funcionando, sem sessão nenhuma."""
    monkeypatch.setattr(appmod.config, "ADMIN_TOKEN", "token-do-editor")
    assert client.get(rota, params={"token": "token-do-editor"}).status_code == 200
    assert client.get(rota, params={"token": "chute"}).status_code == 403


@pytest.mark.parametrize("rota", ["/leitores", "/suggestions", "/telemetry"])
def test_sessao_de_outro_leitor_nao_abre(capturar, configurado, rota):
    editor = entrar(capturar, EDITOR)
    destrancar(editor)
    outro = entrar(capturar, "curioso@exemplo.com")
    assert client.get(rota, params={"session_id": outro}).status_code == 403


def test_token_vazio_nao_e_chave_mestra(monkeypatch):
    """Com `ADMIN_TOKEN` vazio, `?token=` vazio não pode virar autorização — é o
    modo de falha clássico de comparação de string com o default."""
    monkeypatch.setattr(appmod.config, "ADMIN_TOKEN", "")
    assert client.get("/leitores", params={"token": ""}).status_code == 403
    assert client.get("/leitores").status_code == 403


# ------------------------------------------------------------------ /health

def test_health_declara_o_estado_e_nunca_o_valor(monkeypatch):
    monkeypatch.setattr(appmod.config, "ADMIN_EMAILS", [EDITOR])
    monkeypatch.setattr(appmod.config, "ADMIN_SENHA", SENHA)
    monkeypatch.setattr(appmod.config, "ADMIN_TOKEN", "token-do-editor")
    r = client.get("/health")
    assert r.json()["admin"] == {"token": True, "emails": 1, "senha": True}
    # nenhum dos três valores pode aparecer na resposta
    assert SENHA not in r.text
    assert EDITOR not in r.text
    assert "token-do-editor" not in r.text


def test_health_com_admin_desligado(monkeypatch):
    monkeypatch.setattr(appmod.config, "ADMIN_EMAILS", [])
    monkeypatch.setattr(appmod.config, "ADMIN_SENHA", "")
    monkeypatch.setattr(appmod.config, "ADMIN_TOKEN", "")
    assert client.get("/health").json()["admin"] == {"token": False, "emails": 0, "senha": False}
