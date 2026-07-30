"""Decisor — API do produto (v0).

Backend FastAPI; banco Postgres (Neon) via DATABASE_URL com fallback SQLite
(ver bd.py); motor MCDA puro em decisor/motor/. Método disponível no v0: SAW.
Os próximos entram um a um conforme os capítulos do livro ficam prontos
(constituição, Princípio II: nenhum método sem capítulo + teste).

Como rodar:
    cd app/backend
    uvicorn decisor.main:app --reload    # http://localhost:8000
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlmodel import Session, select

from decisor.bd import criar_tabelas, get_sessao
from decisor.modelos import Decisao
from decisor.motor.saw import ranquear_saw
from decisor.motor.tipos import Problema

METODOS = {"saw": ranquear_saw}


@asynccontextmanager
async def ciclo_de_vida(_: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(title="Decisor", version="0.1.0", lifespan=ciclo_de_vida)


class DecisaoIn(BaseModel):
    titulo: str
    problema: Problema


class DecisaoOut(BaseModel):
    id: int
    titulo: str
    problema: Problema


@app.post("/api/decisoes", response_model=DecisaoOut, status_code=201)
def criar_decisao(entrada: DecisaoIn, sessao: Session = Depends(get_sessao)):
    registro = Decisao(titulo=entrada.titulo, problema=entrada.problema.model_dump())
    sessao.add(registro)
    sessao.commit()
    sessao.refresh(registro)
    return DecisaoOut(id=registro.id, titulo=registro.titulo, problema=entrada.problema)


@app.get("/api/decisoes", response_model=list[DecisaoOut])
def listar_decisoes(sessao: Session = Depends(get_sessao)):
    registros = sessao.exec(select(Decisao)).all()
    return [
        DecisaoOut(id=r.id, titulo=r.titulo, problema=Problema(**r.problema))
        for r in registros
    ]


@app.get("/api/decisoes/{decisao_id}", response_model=DecisaoOut)
def obter_decisao(decisao_id: int, sessao: Session = Depends(get_sessao)):
    registro = sessao.get(Decisao, decisao_id)
    if registro is None:
        raise HTTPException(404, "decisão não encontrada")
    return DecisaoOut(
        id=registro.id, titulo=registro.titulo, problema=Problema(**registro.problema)
    )


@app.get("/api/metodos")
def listar_metodos() -> dict:
    return {
        "metodos": [
            {
                "id": "saw",
                "nome": "SAW — Simple Additive Weighting",
                "capitulo": "04",
                "exige_pesos": True,
            }
        ]
    }


@app.post("/api/decisoes/{decisao_id}/ranking")
def ranquear(
    decisao_id: int, metodo: str = "saw", sessao: Session = Depends(get_sessao)
) -> dict:
    registro = sessao.get(Decisao, decisao_id)
    if registro is None:
        raise HTTPException(404, "decisão não encontrada")
    if metodo not in METODOS:
        raise HTTPException(422, f"método {metodo!r} indisponível (ver /api/metodos)")
    problema = Problema(**registro.problema)
    try:
        ranking = METODOS[metodo](problema)
    except ValueError as erro:
        raise HTTPException(422, str(erro)) from erro
    return {"decisao": registro.titulo, "metodo": metodo, "ranking": ranking}


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return (Path(__file__).resolve().parents[1] / "static" / "index.html").read_text(
        encoding="utf-8"
    )
