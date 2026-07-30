"""Acesso a banco — Postgres (Neon) em produção, SQLite local por padrão.

Princípio V (constituição): a connection string vem SÓ de DATABASE_URL (.env
gitignored / variável de ambiente). Princípio VI: sem variável definida, cai em
SQLite local — a trilha roda a custo zero, sem provisionar nada.

Anti-apodrecimento ("Restrições" §4): o resto do app só conhece get_sessao();
trocar Neon por outro Postgres (ou SQLite) não toca motor nem rotas.
"""

import os
from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

URL_PADRAO_LOCAL = "sqlite:///decisor.db"


def _url() -> str:
    url = os.environ.get("DATABASE_URL", URL_PADRAO_LOCAL)
    # Neon fornece URLs "postgres://…"; SQLAlchemy 2 exige o dialeto explícito.
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


def criar_engine(url: str | None = None):
    url = url or _url()
    argumentos = {}
    if url.startswith("sqlite"):
        argumentos["connect_args"] = {"check_same_thread": False}
    return create_engine(url, **argumentos)


engine = criar_engine()


def criar_tabelas(engine_alvo=None) -> None:
    SQLModel.metadata.create_all(engine_alvo or engine)


def get_sessao() -> Iterator[Session]:
    with Session(engine) as sessao:
        yield sessao
