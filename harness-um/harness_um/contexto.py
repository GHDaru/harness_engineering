"""Contexto (cap. 03) — o system prompt é MONTADO, nunca escrito à mão.

A montagem em camadas nomeadas é a feature: identidade fixa embaixo,
estado vivo (memória, plano, habilidades) por cima, cada camada com
cabeçalho próprio. Quem lê o prompt final enxerga de onde veio cada
parágrafo — o mesmo princípio dos "Bastidores" do companion do livro:
contexto injetado tem que ser auditável.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

Camada = tuple[str, Callable[[], str]]  # (título, produtor — avaliado a cada turno)

IDENTIDADE = (
    "Você é um agente do harness-um, a implementação de referência do livro "
    "Engenharia de Harness. Use as ferramentas quando precisar agir; responda "
    "em texto quando souber. Seja direto e honesto sobre o que fez e o que falhou."
)


@dataclass
class MontadorDeContexto:
    camadas: list[Camada] = field(default_factory=list)

    def adicionar(self, titulo: str, produtor: Callable[[], str]) -> None:
        self.camadas.append((titulo, produtor))

    def montar(self) -> str:
        partes = [IDENTIDADE]
        for titulo, produtor in self.camadas:
            corpo = (produtor() or "").strip()
            if corpo:
                partes.append(f"## {titulo}\n{corpo}")
        return "\n\n".join(partes)
