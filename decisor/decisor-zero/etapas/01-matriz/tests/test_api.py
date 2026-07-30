"""A casca FastAPI da etapa 01: validação e soma crua via API."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

PROBLEMA = {
    "alternativas": ["X", "Y"],
    "criterios": [
        {"nome": "Custo", "direcao": "custo", "unidade": "R$"},
        {"nome": "Qualidade", "direcao": "beneficio"},
    ],
    "desempenhos": [[100, 3], [80, 5]],
}


def test_matriz_valida_retorna_dimensoes():
    resposta = client.post("/api/matriz", json=PROBLEMA)
    assert resposta.status_code == 200
    assert resposta.json() == {"valida": True, "m_alternativas": 2, "n_criterios": 2}


def test_erro_de_modelagem_vira_422_legivel():
    quebrado = {**PROBLEMA, "desempenhos": [[100, 3], [80]]}
    resposta = client.post("/api/matriz", json=quebrado)
    assert resposta.status_code == 422
    assert "linha 1" in resposta.json()["detail"]


def test_soma_crua_avisa_que_nao_e_para_decidir():
    resposta = client.post("/api/matriz/soma-crua", json=PROBLEMA)
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert "NÃO use para decidir" in corpo["aviso"]
    assert corpo["ranking"][0] == "X"  # maior soma crua = mais caro: o absurdo


def test_caso_ancora_continua_igual_ao_livro():
    corpo = client.get("/api/caso-ancora").json()
    assert corpo["desempenhos"][2] == [520_000, 85, 25, 5]  # A3 — Parque
