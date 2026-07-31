"""Extensibilidade (cap. 12) — o harness cresce sem ser reescrito.

Dois mecanismos que a coorte inteira convergiu a ter:
- `Gancho` (hook): código do DONO rodando em pontos fixos do loop
  (`antes_ferramenta`, `depois_ferramenta`, `antes_turno`). Um gancho pode
  VETAR uma chamada devolvendo uma string — o veto vira resultado de
  ferramenta que o modelo lê. Determinístico por construção: gancho é
  política em código, não prompt.
- `Habilidade` (skill): conhecimento em arquivos `habilidades/<nome>/SKILL.md`
  — a primeira linha é a descrição (vai ao contexto sempre); o corpo inteiro
  só entra quando a habilidade é invocada. Divulgação progressiva, o padrão
  do cap. 12.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

# Recebe (evento, dados); devolve None ou uma string de veto (só antes_ferramenta).
FnGancho = Callable[[str, dict], str | None]


@dataclass
class Gancho:
    evento: str  # "antes_turno" | "antes_ferramenta" | "depois_ferramenta"
    fn: FnGancho


@dataclass
class GerenciadorDeGanchos:
    ganchos: list[Gancho] = field(default_factory=list)

    def registrar(self, evento: str, fn: FnGancho) -> None:
        self.ganchos.append(Gancho(evento, fn))

    def emitir(self, evento: str, dados: dict) -> str | None:
        for g in self.ganchos:
            if g.evento != evento:
                continue
            veto = g.fn(evento, dados)
            if veto and evento == "antes_ferramenta":
                return str(veto)
        return None


@dataclass
class Habilidade:
    nome: str
    descricao: str
    corpo: str


def carregar_habilidades(diretorio: Path) -> list[Habilidade]:
    habilidades = []
    base = Path(diretorio)
    if base.is_dir():
        for skill in sorted(base.glob("*/SKILL.md")):
            linhas = skill.read_text(encoding="utf-8").strip().splitlines()
            if linhas:
                habilidades.append(
                    Habilidade(nome=skill.parent.name, descricao=linhas[0].lstrip("# ").strip(),
                               corpo="\n".join(linhas))
                )
    return habilidades
