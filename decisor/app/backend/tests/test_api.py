"""Rotas do produto: CRUD de decisões + ranking, ponta a ponta em SQLite."""

from fastapi.testclient import TestClient

from decisor.main import app

DECISAO = {
    "titulo": "Escolha de apartamento",
    "problema": {
        "alternativas": ["A1 — Centro", "A2 — Jardim", "A3 — Parque", "A4 — Estação"],
        "criterios": [
            {"nome": "Preço", "direcao": "custo", "unidade": "R$"},
            {"nome": "Área", "direcao": "beneficio", "unidade": "m²"},
            {"nome": "Deslocamento", "direcao": "custo", "unidade": "min"},
            {"nome": "Bairro", "direcao": "beneficio", "unidade": "1–5"},
        ],
        "desempenhos": [
            [450_000, 62, 15, 4],
            [380_000, 70, 35, 3],
            [520_000, 85, 25, 5],
            [340_000, 55, 20, 2],
        ],
        "pesos": [0.35, 0.25, 0.25, 0.15],
    },
}


def test_ciclo_completo_salvar_listar_ranquear():
    with TestClient(app) as client:
        criada = client.post("/api/decisoes", json=DECISAO)
        assert criada.status_code == 201
        decisao_id = criada.json()["id"]

        listadas = client.get("/api/decisoes")
        assert any(d["id"] == decisao_id for d in listadas.json())

        ranking = client.post(f"/api/decisoes/{decisao_id}/ranking?metodo=saw")
        assert ranking.status_code == 200
        corpo = ranking.json()
        assert corpo["ranking"][0]["alternativa"] == "A1 — Centro"
        assert len(corpo["ranking"]) == 4


def test_problema_mal_modelado_e_rejeitado_na_porta():
    quebrada = {
        "titulo": "quebrada",
        "problema": {**DECISAO["problema"], "pesos": [0.7, 0.5, -0.1, -0.1]},
    }
    with TestClient(app) as client:
        resposta = client.post("/api/decisoes", json=quebrada)
        assert resposta.status_code == 422  # pesos negativos: erro de modelagem


def test_metodo_desconhecido_aponta_para_o_catalogo():
    with TestClient(app) as client:
        decisao_id = client.post("/api/decisoes", json=DECISAO).json()["id"]
        resposta = client.post(f"/api/decisoes/{decisao_id}/ranking?metodo=magico")
        assert resposta.status_code == 422
        assert "/api/metodos" in resposta.json()["detail"]


def test_decisao_inexistente_e_404():
    with TestClient(app) as client:
        assert client.post("/api/decisoes/99999/ranking").status_code == 404
