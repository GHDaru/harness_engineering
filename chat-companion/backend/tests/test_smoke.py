"""Smoke tests do companion — sem rede, sem banco (adapter echo + memória).

Cobrem o fluxo (chat, histórico, capacidades), o gating progressivo e o
rate limit. Rodar:  cd chat-companion/backend && python -m pytest
"""

import os
import sys

os.environ.setdefault("LLM_ADAPTER", "echo")   # sem rede
os.environ.pop("DATABASE_URL", None)           # força MemoryStore
os.environ["RATE_LIMIT_MSGS"] = "3"
os.environ["RATE_LIMIT_WINDOW_S"] = "60"
os.environ["RATE_LIMIT_IP_FACTOR"] = "100"  # guarda por IP fora do caminho nos testes

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  # noqa: E402

import capabilities  # noqa: E402
import app as appmod  # noqa: E402

client = TestClient(appmod.app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["store"] == "memory"


def test_chat_and_history():
    sid = "s-chat"
    r = client.post("/chat", json={"session_id": sid, "message": "olá", "chapter": 1,
                                   "mode": "progressivo"})
    assert r.status_code == 200
    body = r.json()
    assert "echo" in body["reply"]
    assert any(c["chave"] == "tutor" for c in body["capabilities_ativas"])
    h = client.get("/history", params={"session_id": sid}).json()["messages"]
    assert h[0]["role"] == "user" and h[-1]["role"] == "assistant"


def test_gating_progressive_hides_future_tools():
    # cap. 1 progressivo: loop ainda não liberado (libera no cap. 2) -> sem tools
    assert capabilities.tools_ativas(1, "progressivo") == set()
    # cap. 2 progressivo: loop + 'hora'
    assert "hora" in capabilities.tools_ativas(2, "progressivo")
    # 'calcular' só no cap. 5
    assert "calcular" not in capabilities.tools_ativas(2, "progressivo")
    assert "calcular" in capabilities.tools_ativas(5, "progressivo")
    # avançado libera tudo mesmo no cap. 0
    assert {"hora", "calcular", "buscar_no_livro"} <= capabilities.tools_ativas(0, "avancado")


def test_capabilities_endpoint():
    r = client.get("/capabilities", params={"chapter": 0, "mode": "progressivo"})
    j = r.json()
    assert j["loop_ativo"] is False
    ativos = {c["chave"] for c in j["capabilities"] if c["ativa"]}
    assert "tutor" in ativos and "loop" not in ativos


def test_rate_limit_429():
    sid = "s-rate"
    for _ in range(3):
        assert client.post("/chat", json={"session_id": sid, "message": "hi"}).status_code == 200
    # 4ª na janela estoura
    assert client.post("/chat", json={"session_id": sid, "message": "hi"}).status_code == 429


def test_byok_bypasses_rate_limit():
    sid = "s-byok"
    for _ in range(3):
        client.post("/chat", json={"session_id": sid, "message": "hi"})
    r = client.post("/chat", json={"session_id": sid, "message": "hi", "byok_key": "nvapi-x"})
    # BYOK isenta do limite do projeto; echo ignora a chave, mas não deve dar 429
    assert r.status_code == 200


def test_delete_session():
    sid = "s-del"
    client.post("/chat", json={"session_id": sid, "message": "oi"})
    client.delete(f"/session/{sid}")
    assert client.get("/history", params={"session_id": sid}).json()["messages"] == []


def test_suggestion_persists_and_lists():
    sid = "s-sug"
    r = client.post("/suggestion", json={"session_id": sid, "texto": "ótimo livro, cap 5 podia ter mais exemplos", "pagina": "05-ferramentas.html"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True and body["email_enviado"] is False  # sem SMTP no teste
    # sem ADMIN_TOKEN -> 403
    assert client.get("/suggestions", params={"token": "x"}).status_code == 403


def test_suggestion_empty_400():
    assert client.post("/suggestion", json={"session_id": "s", "texto": "  "}).status_code == 400


def test_chat_stream_echo():
    """spec 047: o stream emite deltas e um done com a resposta completa,
    idêntica à que fica persistida no histórico."""
    import json
    sid = "t-stream"
    with client.stream("POST", "/chat/stream",
                       json={"session_id": sid, "message": "olá streaming"}) as r:
        assert r.status_code == 200
        assert r.headers["content-type"].startswith("text/event-stream")
        eventos = []
        for linha in r.iter_lines():
            if linha.startswith("data: "):
                eventos.append(json.loads(linha[6:]))
    deltas = [e["delta"] for e in eventos if "delta" in e]
    done = [e for e in eventos if e.get("done")]
    assert len(deltas) > 1, "deveria vir em mais de um pedaço"
    assert len(done) == 1
    assert "".join(deltas) == done[0]["reply"]
    hist = client.get("/history", params={"session_id": sid}).json()["messages"]
    assert hist[-1]["role"] == "assistant" and hist[-1]["content"] == done[0]["reply"]


def test_rate_limit_sobrevive_a_restart():
    """spec 049: o 429 por sessão vem do STORE (mensagens persistidas), não do
    deque em memória — limpar o deque (simulando deploy) não zera o limite."""
    sid = "t-rl-persistente"
    for i in range(3):  # RATE_LIMIT_MSGS = 3 nos testes
        r = client.post("/chat", json={"session_id": sid, "message": f"m{i}"})
        assert r.status_code == 200
    appmod._hits.clear()  # "restart" da instância
    r = client.post("/chat", json={"session_id": sid, "message": "m-extra"})
    assert r.status_code == 429


def test_debug_bastidores():
    """spec 053: /chat e o done do stream expõem o bloco debug (transparência)."""
    import json
    r = client.post("/chat", json={"session_id": "t-debug", "message": "o que é loop?"})
    d = r.json()["debug"]
    assert d["tokens_estimados"] > 0 and d["janela_tokens"] > 0
    assert d["historico_msgs"] >= 1 and isinstance(d["trechos"], list)
    assert "Tutor do livro" in d["capacidades_ativas"]

    with client.stream("POST", "/chat/stream",
                       json={"session_id": "t-debug2", "message": "e compactação?"}) as r:
        eventos = [json.loads(l[6:]) for l in r.iter_lines() if l.startswith("data: ")]
    done = [e for e in eventos if e.get("done")][0]
    assert done["debug"]["tokens_estimados"] > 0
