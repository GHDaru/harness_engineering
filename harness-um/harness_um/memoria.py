"""Memória e estado (cap. 08) — o que sobrevive ao fim da janela.

Dois mecanismos, deliberadamente distintos:
- `Memoria`: um arquivo `MEMORIA.md` legível por humanos, injetado no
  contexto a cada turno. O agente anota; a pessoa edita. Memória boa é a
  que o dono consegue auditar com `cat`.
- `Sessao`: o histórico integral em JSONL, uma linha por mensagem —
  append-only, barato, e a base para retomar conversas (o mesmo desenho
  das sessões do harness-zero, etapa 4).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .provedores import Mensagem


@dataclass
class Memoria:
    caminho: Path

    def ler(self) -> str:
        try:
            return Path(self.caminho).read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            return ""

    def anotar(self, nota: str) -> str:
        p = Path(self.caminho)
        p.parent.mkdir(parents=True, exist_ok=True)
        existente = self.ler()
        cabecalho = existente if existente else "# MEMORIA\n"
        p.write_text(cabecalho.rstrip() + f"\n- {nota.strip()}\n", encoding="utf-8")
        return f"anotado na memória: {nota.strip()}"


@dataclass
class Sessao:
    diretorio: Path
    nome: str = "sessao"

    @property
    def arquivo(self) -> Path:
        return Path(self.diretorio) / f"{self.nome}.jsonl"

    def registrar(self, mensagem: Mensagem) -> None:
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)
        linha = {"quando": datetime.now(timezone.utc).isoformat(), **mensagem}
        with self.arquivo.open("a", encoding="utf-8") as f:
            f.write(json.dumps(linha, ensure_ascii=False) + "\n")

    def carregar(self) -> list[Mensagem]:
        if not self.arquivo.exists():
            return []
        historico = []
        for linha in self.arquivo.read_text(encoding="utf-8").splitlines():
            if linha.strip():
                d = json.loads(linha)
                d.pop("quando", None)
                historico.append(d)
        return historico
