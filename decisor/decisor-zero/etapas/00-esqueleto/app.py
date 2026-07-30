"""Etapa 00 — o esqueleto.

Capítulo correspondente: livro/capitulos/00-introducao.md.

Aqui ainda não existe nenhum método multicritério — de propósito. Esta etapa é o
chassi sobre o qual as próximas 13 vão crescer: uma API FastAPI que serve o caso
âncora (a escolha de apartamento que atravessa o livro inteiro) e uma página HTML
sem build que o exibe. A dor que fica no ar: a tabela mostra o conflito entre
critérios, mas nada aqui ajuda a resolvê-lo. A etapa 01 começa a resolver dando
à tabela uma definição matemática precisa (a matriz de decisão).

Como rodar:
    uvicorn app:app --reload
    # http://localhost:8000
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="decisor-zero — etapa 00")

# O caso âncora (livro/SUMARIO.md). Direção: "custo" = quanto menor, melhor;
# "beneficio" = quanto maior, melhor.
CASO_ANCORA = {
    "titulo": "Escolha de apartamento",
    "criterios": [
        {"nome": "Preço", "unidade": "R$", "direcao": "custo"},
        {"nome": "Área", "unidade": "m²", "direcao": "beneficio"},
        {"nome": "Deslocamento", "unidade": "min", "direcao": "custo"},
        {"nome": "Bairro", "unidade": "1–5", "direcao": "beneficio"},
    ],
    "alternativas": [
        {"nome": "A1 — Centro", "desempenhos": [450_000, 62, 15, 4]},
        {"nome": "A2 — Jardim", "desempenhos": [380_000, 70, 35, 3]},
        {"nome": "A3 — Parque", "desempenhos": [520_000, 85, 25, 5]},
        {"nome": "A4 — Estação", "desempenhos": [340_000, 55, 20, 2]},
    ],
}


@app.get("/api/caso-ancora")
def caso_ancora() -> dict:
    """A mesma tabela do capítulo 00 — a API e o livro nunca divergem."""
    return CASO_ANCORA


@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return (Path(__file__).parent / "index.html").read_text(encoding="utf-8")
