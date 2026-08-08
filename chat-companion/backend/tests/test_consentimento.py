"""Spec 093 — consentimento em camadas (ADR 0010) e progresso visível.

O que estes testes protegem é uma promessa, não um comportamento: a ADR 0009
prometeu "sem informativo", e a ADR 0010 só moveu essa fronteira ao custo de
manter as duas finalidades separadas. Um teste verde aqui é a prova de que
assinar para guardar progresso continua não sendo assinar para receber e-mail.

Sem rede e sem banco: adapter echo + MemoryStore, envio monkeypatched.
"""

import os
import sys

os.environ.setdefault("LLM_ADAPTER", "echo")
os.environ.pop("DATABASE_URL", None)
os.environ["RATE_LIMIT_ASSINAR"] = "50"
# Mesmos limites dos outros arquivos: `config` é lido UMA vez, no primeiro
# import de `app`, e a ordem dos módulos de teste não é garantida.
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
    enviados = []

    def falso(email, token, lang):
        enviados.append({"email": email, "token": token, "lang": lang})
        return True, ""

    monkeypatch.setattr(appmod, "_enviar_link_magico", falso)
    return enviados


def entrar(capturar, email):
    """Assina e consome o link — devolve a sessão canônica do leitor."""
    appmod._hits.clear()
    client.post("/assinar", json={"email": email})
    return client.post("/entrar", json={"token": capturar[-1]["token"]}).json()


# ------------------------------------------------- continuidade (spec 080)

def test_continuidade_e_registrada_no_entrar_e_nao_no_assinar(capturar):
    """A posse do endereço só fica provada quando o link é aberto. Registrar no
    pedido criaria linha em nome de quem apenas teve o e-mail digitado."""
    appmod._hits.clear()
    client.post("/assinar", json={"email": "posse@exemplo.com"})
    assert appmod._store.consentimentos_de("posse@exemplo.com") == {}

    d = client.post("/entrar", json={"token": capturar[-1]["token"]}).json()
    assert d["consentimentos"]["continuidade"]["aceito"] is True
    assert d["consentimentos"]["continuidade"]["versao"] == appmod.VERSAO_CONTINUIDADE


def test_reentrar_nao_consente_de_novo(capturar):
    entrar(capturar, "reentra@exemplo.com")
    entrar(capturar, "reentra@exemplo.com")
    linhas = [c for c in appmod._store._cons
              if c["email"] == "reentra@exemplo.com" and c["finalidade"] == "continuidade"]
    assert len(linhas) == 1


# --------------------------------------------------------- contato (ADR 0010)

def test_assinante_nao_e_migrado_para_contato(capturar):
    """O centro da ADR 0010: quem assinou sob 'sem informativo' NÃO entra na
    lista por efeito da mudança. Silêncio vale não."""
    d = entrar(capturar, "nao-migrado@exemplo.com")
    assert "contato" not in d["consentimentos"]
    assert appmod._store.emails_com_contato() == []


def test_dar_revogar_e_dar_de_novo(capturar):
    sid = entrar(capturar, "vaievem@exemplo.com")["session_id"]

    def por(aceito):
        return client.post("/consentimento",
                           json={"session_id": sid, "finalidade": "contato",
                                 "aceito": aceito})

    assert por(True).json()["aceito"] is True
    estado = client.get("/consentimento", params={"session_id": sid}).json()
    assert estado["consentimentos"]["contato"]["aceito"] is True

    assert por(False).status_code == 200
    estado = client.get("/consentimento", params={"session_id": sid}).json()
    assert estado["consentimentos"]["contato"]["aceito"] is False

    assert por(True).status_code == 200
    assert client.get("/consentimento", params={"session_id": sid}) \
        .json()["consentimentos"]["contato"]["aceito"] is True

    # append-only: as três decisões continuam na base, nenhuma foi sobrescrita
    linhas = [c for c in appmod._store._cons
              if c["email"] == "vaievem@exemplo.com" and c["finalidade"] == "contato"]
    assert [c["aceito"] for c in linhas] == [True, False, True]


def test_revogar_contato_preserva_continuidade(capturar):
    """Misturar as finalidades puniria quem só não quer receber novidade."""
    d = entrar(capturar, "so-nao-quero@exemplo.com")
    sid = d["session_id"]
    client.post("/consentimento", json={"session_id": sid, "aceito": True})
    client.post("/consentimento", json={"session_id": sid, "aceito": False})

    estado = client.get("/consentimento", params={"session_id": sid}).json()
    assert estado["consentimentos"]["continuidade"]["aceito"] is True
    assert estado["consentimentos"]["contato"]["aceito"] is False
    # e a continuidade continua funcionando de fato
    assert client.get("/leitor", params={"session_id": sid}).json()["email"] \
        == "so-nao-quero@exemplo.com"


def test_consentimento_desmarcado_e_o_default_do_corpo():
    """Um POST sem `aceito` registra NÃO. O default do contrato acompanha o
    default da caixa — se divergissem, um cliente desatento consentiria por
    omissão, que é exatamente o que a ADR rejeitou."""
    assert appmod.ConsentimentoIn(session_id="x").aceito is False


def test_continuidade_nao_e_editavel_por_esta_rota(capturar):
    sid = entrar(capturar, "trava@exemplo.com")["session_id"]
    r = client.post("/consentimento", json={"session_id": sid,
                                            "finalidade": "continuidade", "aceito": False})
    assert r.status_code == 400
    assert appmod._store.consentimentos_de("trava@exemplo.com")["continuidade"]["aceito"] is True


def test_sessao_anonima_nao_consente_e_nao_quebra_a_tela():
    """POST recusa (não há a quem atribuir); GET devolve vazio sem erro, porque
    a tela precisa distinguir 'anônimo' de 'falhou'."""
    assert client.post("/consentimento", json={"session_id": "anon-093"}).status_code == 403
    r = client.get("/consentimento", params={"session_id": "anon-093"})
    assert r.status_code == 200
    assert r.json()["email"] is None and r.json()["consentimentos"] == {}


# ------------------------------------------------------- descadastro (R4)

def test_descadastro_de_um_clique(capturar):
    d = entrar(capturar, "sai@exemplo.com")
    client.post("/consentimento", json={"session_id": d["session_id"], "aceito": True})
    assert "sai@exemplo.com" in [r["email"] for r in appmod._store.emails_com_contato()]

    h = appmod._hash_token("sai@exemplo.com")
    assert client.post("/descadastrar", json={"e": h}).json() == {"ok": True}
    assert "sai@exemplo.com" not in [r["email"] for r in appmod._store.emails_com_contato()]
    # continuidade intacta
    assert client.get("/leitor", params={"session_id": d["session_id"]}).json()["email"] \
        == "sai@exemplo.com"


def test_descadastro_e_idempotente_e_nao_enumera(capturar):
    """Sair duas vezes diz a mesma coisa, e um hash desconhecido também — senão
    a rota viraria oráculo de 'este endereço está cadastrado?'."""
    d = entrar(capturar, "duas-vezes@exemplo.com")
    client.post("/consentimento", json={"session_id": d["session_id"], "aceito": True})
    h = appmod._hash_token("duas-vezes@exemplo.com")
    primeira = client.post("/descadastrar", json={"e": h})
    segunda = client.post("/descadastrar", json={"e": h})
    desconhecido = client.post("/descadastrar", json={"e": appmod._hash_token("nunca@x.com")})
    assert primeira.json() == segunda.json() == desconhecido.json()
    assert primeira.status_code == segunda.status_code == desconhecido.status_code == 200


def test_descadastro_recusa_parametro_que_nao_e_hash():
    for ruim in ["", "abc", "z" * 64, "  "]:
        assert client.post("/descadastrar", json={"e": ruim}).status_code == 400


# ------------------------------------------------------- exportação (R3)

def test_leitores_nasce_desligado(monkeypatch):
    """Sem `ADMIN_TOKEN` no ambiente nenhum token confere — nem o vazio."""
    monkeypatch.setattr(appmod.config, "ADMIN_TOKEN", "")
    assert client.get("/leitores").status_code == 403
    assert client.get("/leitores", params={"token": ""}).status_code == 403
    assert client.get("/leitores", params={"token": "chute"}).status_code == 403


def test_leitores_traz_so_contato_ativo(capturar, monkeypatch):
    monkeypatch.setattr(appmod.config, "ADMIN_TOKEN", "token-do-editor")

    quer = entrar(capturar, "quer@exemplo.com")["session_id"]
    client.post("/consentimento", json={"session_id": quer, "aceito": True})

    entrar(capturar, "calado@exemplo.com")                 # nunca respondeu

    saiu = entrar(capturar, "saiu@exemplo.com")["session_id"]
    client.post("/consentimento", json={"session_id": saiu, "aceito": True})
    client.post("/consentimento", json={"session_id": saiu, "aceito": False})

    lista = client.get("/leitores", params={"token": "token-do-editor"}).json()
    emails = [r["email"] for r in lista["leitores"]]
    assert "quer@exemplo.com" in emails
    assert "calado@exemplo.com" not in emails
    assert "saiu@exemplo.com" not in emails
    assert lista["total"] == len(lista["leitores"])
    assert lista["leitores"][0]["versao"] == appmod.VERSAO_CONTATO


# --------------------------------------------------- progresso visível (R1)

def test_progresso_detalhe_lista_os_slugs_visitados(capturar):
    """Sem tabela nova: sai de `nav_events`, que já existe e já segue o leitor
    na fusão da spec 080."""
    sid = entrar(capturar, "andou@exemplo.com")["session_id"]
    client.post("/consent", json={"session_id": sid, "versao": "v1"})
    for slug in ["01-loop", "02-contexto", "01-loop"]:
        client.post("/telemetry", json={"session_id": sid, "slug": slug})

    d = client.get("/progresso/detalhe", params={"session_id": sid}).json()
    assert d["visitados"] == ["01-loop", "02-contexto"]     # distintos e ordenados


def test_progresso_detalhe_de_sessao_vazia_nao_e_erro():
    d = client.get("/progresso/detalhe", params={"session_id": "anon-vazio"})
    assert d.status_code == 200
    assert d.json()["visitados"] == [] and d.json()["itens"] == []


def test_a_leitura_anonima_tambem_conta(capturar):
    """A fusão da spec 080 leva o `nav_events` da sessão anônima. Quem leu antes
    de assinar não chega com a barra zerada — seria a pior primeira impressão
    possível para uma tela cujo assunto é justamente não perder progresso."""
    anon = "anon-leu-antes"
    client.post("/consent", json={"session_id": anon, "versao": "v1"})
    client.post("/telemetry", json={"session_id": anon, "slug": "03-ferramentas"})

    appmod._hits.clear()
    client.post("/assinar", json={"email": "leu-antes@exemplo.com", "session_id": anon})
    sid = client.post("/entrar", json={"token": capturar[-1]["token"],
                                       "session_id": anon}).json()["session_id"]
    assert client.get("/progresso/detalhe", params={"session_id": sid}) \
        .json()["visitados"] == ["03-ferramentas"]


# ------------------------------------------------------------ esquecimento

def test_apagar_leitor_leva_os_consentimentos(capturar):
    """Append-only é regra da operação normal; o esquecimento ganha dele. Guardar
    a prova do consentimento de quem pediu para sumir seria guardar o e-mail que
    ele mandou apagar."""
    d = entrar(capturar, "esquece@exemplo.com")
    client.post("/consentimento", json={"session_id": d["session_id"], "aceito": True})

    client.request("DELETE", "/leitor", json={"session_id": d["session_id"]})
    assert appmod._store.consentimentos_de("esquece@exemplo.com") == {}
    assert "esquece@exemplo.com" not in [r["email"] for r in appmod._store.emails_com_contato()]
