"""Persistência v0: a decisão inteira (problema + metadados) em uma tabela.

Deliberadamente simples — o problema é guardado como JSON validado pelo motor
(Problema) antes de entrar. O modelo relacional completo (alternativas e
critérios como linhas, histórico de rankings) é assunto do cap. 13 e virá por
spec própria; registrar em ADR se o v0 apodrecer antes disso.
"""

from datetime import datetime, timezone

from sqlmodel import Column, Field, JSON, SQLModel


class Decisao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    problema: dict = Field(sa_column=Column(JSON, nullable=False))
    criada_em: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
