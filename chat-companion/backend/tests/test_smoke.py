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
