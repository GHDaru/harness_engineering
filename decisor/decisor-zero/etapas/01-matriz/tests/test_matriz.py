"""Os números do capítulo 01, verificados (Princípio I: worked example = teste)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from motor.matriz import Criterio, ErroDeModelagem, MatrizDecisao


def caso_ancora(pesos=None) -> MatrizDecisao:
    return MatrizDecisao(
        alternativas=["A1 — Centro", "A2 — Jardim", "A3 — Parque", "A4 — Estação"],
        criterios=[
            Criterio("Preço", "custo", "R$"),
            Criterio("Área", "beneficio", "m²"),
            Criterio("Deslocamento", "custo", "min"),
            Criterio("Bairro", "beneficio", "1–5"),
        ],
        desempenhos=[
            [450_000, 62, 15, 4],
            [380_000, 70, 35, 3],
            [520_000, 85, 25, 5],
            [340_000, 55, 20, 2],
        ],
        pesos=pesos,
    )


def test_caso_ancora_e_um_problema_4x4_valido():
    matriz = caso_ancora()
    assert len(matriz.alternativas) == 4
    assert len(matriz.criterios) == 4


def test_soma_crua_reproduz_a_tabela_do_capitulo():
    # Passo 4 do cap. 01: 450.081 / 380.108 / 520.115 / 340.077
    escores = caso_ancora().soma_crua()
    assert escores == {
        "A1 — Centro": 450_081,
        "A2 — Jardim": 380_108,
        "A3 — Parque": 520_115,
        "A4 — Estação": 340_077,
    }


def test_soma_crua_e_o_preco_com_ruido():
    """A lição do cap. 01: o ranking da soma crua é o ranking do preço.

    A soma "elege" A3, o apartamento mais CARO — prova de que agregar escalas
    incomensuráveis premia o critério de maior magnitude, ignorando direção.
    """
    matriz = caso_ancora()
    ranking = matriz.ranking_por(matriz.soma_crua())
    ranking_do_preco = ["A3 — Parque", "A1 — Centro", "A2 — Jardim", "A4 — Estação"]
    assert ranking == ranking_do_preco


def test_direcao_invalida_e_erro_de_modelagem():
    with pytest.raises(ErroDeModelagem, match="direção"):
        Criterio("Preço", "menor-melhor")


def test_linha_com_desempenhos_faltando_e_erro():
    with pytest.raises(ErroDeModelagem, match="linha 1"):
        MatrizDecisao(
            alternativas=["A1", "A2"],
            criterios=[Criterio("Preço", "custo"), Criterio("Área", "beneficio")],
            desempenhos=[[1, 2], [1]],
        )


def test_pesos_que_nao_somam_um_sao_erro():
    with pytest.raises(ErroDeModelagem, match="somar 1"):
        caso_ancora(pesos=[0.5, 0.5, 0.5, 0.5])


def test_pesos_validos_passam():
    assert caso_ancora(pesos=[0.35, 0.25, 0.25, 0.15]).pesos is not None


@pytest.mark.skip(reason="exercício do leitor — cap. 01, Mão na massa")
def test_peso_negativo_e_erro_de_modelagem():
    """Complete-me: a definição exige w_j >= 0, mas o validador não checa.

    Gabarito: em MatrizDecisao.__post_init__, dentro do bloco de pesos,
    levante ErroDeModelagem se any(w < 0 for w in self.pesos); aqui, remova o
    skip e afirme pytest.raises(ErroDeModelagem) para pesos=[0.7, 0.5, -0.1, -0.1]
    (que somam 1 — o caso que escapa da checagem de soma).
    """
