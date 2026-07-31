"""Permissões (cap. 07) — o harness decide o que o modelo PODE, não o modelo.

Três decisões possíveis por chamada: PERMITIR, PERGUNTAR (aprovação humana),
NEGAR. A política é dado, não código: um dicionário regra→decisão com um
padrão explícito. A pergunta chega ao humano por um `aprovador` injetado —
no REPL é `input()`, no teste é uma função, num servidor seria uma fila.
Negar não derruba o loop: vira um resultado de ferramenta que o modelo lê
("negada pela política") e contorna — a lição de que permissão é conversa,
não exceção.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from .provedores import ChamadaDeFerramenta


class Decisao(Enum):
    PERMITIR = "permitir"
    PERGUNTAR = "perguntar"
    NEGAR = "negar"


Aprovador = Callable[[ChamadaDeFerramenta], bool]


@dataclass
class Politica:
    regras: dict[str, Decisao] = field(default_factory=dict)
    padrao: Decisao = Decisao.PERGUNTAR

    def decidir(self, chamada: ChamadaDeFerramenta) -> Decisao:
        return self.regras.get(chamada.nome, self.padrao)

    @classmethod
    def padrao_segura(cls) -> "Politica":
        """Leitura livre; mutação pergunta. O default que o cap. 07 defende."""
        return cls(
            regras={
                "ler_arquivo": Decisao.PERMITIR,
                "listar_diretorio": Decisao.PERMITIR,
                "tarefa": Decisao.PERMITIR,  # subagente já nasce só-leitura (cap. 10)
                "escrever_arquivo": Decisao.PERGUNTAR,
                "executar_shell": Decisao.PERGUNTAR,
            },
            padrao=Decisao.PERGUNTAR,
        )
