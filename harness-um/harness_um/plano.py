"""Planejamento (cap. 09) — o plano é um ARTEFATO, não um pensamento.

Plano que só existe dentro da janela evapora com ela. Aqui ele é uma
estrutura persistida (JSON) e renderizada no contexto a cada turno: o
modelo relê o próprio plano, marca progresso por ferramenta, e o humano
pode abrir o arquivo e discordar. Três estados por item — pendente,
em andamento, concluído — porque mais que isso vira burocracia.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

ESTADOS = ("pendente", "em_andamento", "concluido")
_MARCAS = {"pendente": "[ ]", "em_andamento": "[~]", "concluido": "[x]"}


@dataclass
class Plano:
    caminho: Path | None = None
    itens: list[dict] = field(default_factory=list)

    def adicionar(self, texto: str) -> str:
        self.itens.append({"id": len(self.itens) + 1, "texto": texto, "estado": "pendente"})
        self._salvar()
        return f"item {len(self.itens)} adicionado ao plano"

    def marcar(self, id: int, estado: str) -> str:
        if estado not in ESTADOS:
            return f"erro: estado deve ser um de {ESTADOS}"
        for item in self.itens:
            if item["id"] == id:
                item["estado"] = estado
                self._salvar()
                return f"item {id} → {estado}"
        return f"erro: item {id} não existe"

    def render(self) -> str:
        return "\n".join(f"{_MARCAS[i['estado']]} {i['id']}. {i['texto']}" for i in self.itens)

    def _salvar(self) -> None:
        if self.caminho:
            p = Path(self.caminho)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(self.itens, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def carregar(cls, caminho: Path) -> "Plano":
        p = Path(caminho)
        itens = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
        return cls(caminho=p, itens=itens)
