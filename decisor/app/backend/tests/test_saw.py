"""O worked example do SAW no caso âncora (será a tabela do cap. 04).

Números conferíveis à mão: normalização min-max com inversão nos critérios de
custo, pesos w = (0.35, 0.25, 0.25, 0.15).
"""

import pytest

from decisor.motor.saw import normalizar_minmax, ranquear_saw
from decisor.motor.tipos import Problema

CASO_ANCORA = Problema(
    alternativas=["A1 — Centro", "A2 — Jardim", "A3 — Parque", "A4 — Estação"],
    criterios=[
        {"nome": "Preço", "direcao": "custo", "unidade": "R$"},
        {"nome": "Área", "direcao": "beneficio", "unidade": "m²"},
        {"nome": "Deslocamento", "direcao": "custo", "unidade": "min"},
        {"nome": "Bairro", "direcao": "beneficio", "unidade": "1–5"},
    ],
    desempenhos=[
        [450_000, 62, 15, 4],
        [380_000, 70, 35, 3],
        [520_000, 85, 25, 5],
        [340_000, 55, 20, 2],
    ],
    pesos=[0.35, 0.25, 0.25, 0.15],
)


def test_normalizacao_minmax_inverte_criterios_de_custo():
    normalizada = normalizar_minmax(CASO_ANCORA)
    # Preço (custo): o mais barato (A4, 340k) vira 1; o mais caro (A3, 520k) vira 0.
    assert normalizada[3][0] == pytest.approx(1.0)
    assert normalizada[2][0] == pytest.approx(0.0)
    assert normalizada[0][0] == pytest.approx((520_000 - 450_000) / 180_000)
    # Área (benefício): a maior (A3, 85) vira 1.
    assert normalizada[2][1] == pytest.approx(1.0)


def test_ranking_saw_do_caso_ancora():
    ranking = ranquear_saw(CASO_ANCORA)
    ordem = [linha["alternativa"] for linha in ranking]
    assert ordem == ["A1 — Centro", "A4 — Estação", "A3 — Parque", "A2 — Jardim"]
    escores = {linha["alternativa"]: linha["escore"] for linha in ranking}
    assert escores["A1 — Centro"] == pytest.approx(0.544444, abs=1e-6)
    assert escores["A4 — Estação"] == pytest.approx(0.5375, abs=1e-6)
    assert escores["A3 — Parque"] == pytest.approx(0.525, abs=1e-6)
    assert escores["A2 — Jardim"] == pytest.approx(0.447222, abs=1e-6)


def test_saw_sem_pesos_e_erro_com_ponteiro_para_o_livro():
    sem_pesos = CASO_ANCORA.model_copy(update={"pesos": None})
    with pytest.raises(ValueError, match="cap. 03"):
        ranquear_saw(sem_pesos)


def test_criterio_que_nao_discrimina_vale_zero():
    empatado = Problema(
        alternativas=["X", "Y"],
        criterios=[
            {"nome": "Empate", "direcao": "beneficio"},
            {"nome": "Custo", "direcao": "custo"},
        ],
        desempenhos=[[7, 100], [7, 80]],
        pesos=[0.5, 0.5],
    )
    normalizada = normalizar_minmax(empatado)
    assert normalizada[0][0] == 0.0 and normalizada[1][0] == 0.0
