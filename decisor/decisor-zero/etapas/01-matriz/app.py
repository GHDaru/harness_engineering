"""Etapa 01 — a matriz de decisão vira código.

Capítulo correspondente: livro/capitulos/01-problema-multicriterio.md.

A dor deixada pela etapa 00: a tabela do caso âncora era um dicionário solto —
nada impedia uma alternativa com 3 desempenhos para 4 critérios, uma direção
digitada errada, pesos somando 1,2. Nesta etapa nasce o conceito central do
livro: a MatrizDecisao (motor/matriz.py), um objeto puro e validado que TODO
método dos próximos capítulos vai consumir. A API deixa de servir só o caso
âncora e passa a aceitar qualquer problema do usuário (POST /api/matriz), além
de expor a "soma crua" — a agregação ingênua cujo absurdo motiva os caps. 03–04.

Como rodar:
    uvicorn app:app --reload      # http://localhost:8000
    pytest                        # os números do capítulo, verificados
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from motor.matriz import Criterio, ErroDeModelagem, MatrizDecisao

app = FastAPI(title="decisor-zero — etapa 01")


def caso_ancora() -> MatrizDecisao:
    """O caso âncora do livro (SUMARIO.md) como MatrizDecisao."""
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
    )


class CriterioIn(BaseModel):
    nome: str
    direcao: str
    unidade: str = ""


class MatrizIn(BaseModel):
    alternativas: list[str]
    criterios: list[CriterioIn]
    desempenhos: list[list[float]]
    pesos: list[float] | None = None


def _montar(entrada: MatrizIn) -> MatrizDecisao:
    try:
        return MatrizDecisao(
            alternativas=entrada.alternativas,
            criterios=[Criterio(c.nome, c.direcao, c.unidade) for c in entrada.criterios],
            desempenhos=entrada.desempenhos,
            pesos=entrada.pesos,
        )
    except ErroDeModelagem as erro:
        # O erro de modelagem é lição, não stack trace: vai legível para o usuário.
        raise HTTPException(status_code=422, detail=str(erro)) from erro


@app.post("/api/matriz")
def validar_matriz(entrada: MatrizIn) -> dict:
    """Valida um problema multicritério qualquer segundo a definição do cap. 01."""
    matriz = _montar(entrada)
    return {
        "valida": True,
        "m_alternativas": len(matriz.alternativas),
        "n_criterios": len(matriz.criterios),
    }


@app.post("/api/matriz/soma-crua")
def soma_crua(entrada: MatrizIn) -> dict:
    """A agregação ingênua — exposta de propósito para o leitor ver o absurdo."""
    matriz = _montar(entrada)
    escores = matriz.soma_crua()
    return {
        "aviso": "soma de escalas incomensuráveis — NÃO use para decidir (cap. 01)",
        "escores": escores,
        "ranking": matriz.ranking_por(escores),
    }


@app.get("/api/caso-ancora")
def api_caso_ancora() -> dict:
    matriz = caso_ancora()
    return {
        "titulo": "Escolha de apartamento",
        "alternativas": matriz.alternativas,
        "criterios": [vars(c) for c in matriz.criterios],
        "desempenhos": matriz.desempenhos,
    }


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return (Path(__file__).parent / "index.html").read_text(encoding="utf-8")
