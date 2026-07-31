"""Verificação (cap. 11) — o harness não confia; confere.

Depois de TODA ferramenta que muta o mundo, os verificadores rodam e o
veredito volta AO MODELO no mesmo resultado de ferramenta — o agente lê a
própria falha e corrige no turno seguinte. É o portão de qualidade do
livro em miniatura: automático, barato e impossível de esquecer, porque
mora no loop, não na disciplina de quem usa.
"""

from __future__ import annotations

import py_compile
import tempfile
from dataclasses import dataclass, field
from typing import Callable

from .provedores import ChamadaDeFerramenta

# Recebe a chamada já executada; devolve None (ok) ou a descrição do problema.
Checagem = Callable[[ChamadaDeFerramenta, str], str | None]


def python_compila(chamada: ChamadaDeFerramenta, resultado: str) -> str | None:
    """Se escreveu um .py, ele precisa ao menos compilar."""
    caminho = str(chamada.argumentos.get("caminho", ""))
    conteudo = chamada.argumentos.get("conteudo")
    if chamada.nome != "escrever_arquivo" or not caminho.endswith(".py") or conteudo is None:
        return None
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(str(conteudo))
        nome = tmp.name
    try:
        py_compile.compile(nome, doraise=True)
        return None
    except py_compile.PyCompileError as e:
        return f"o Python escrito não compila: {e.msg.strip().splitlines()[-1]}"


@dataclass
class Verificador:
    checagens: list[Checagem] = field(default_factory=lambda: [python_compila])

    def verificar(self, chamada: ChamadaDeFerramenta, resultado: str) -> list[str]:
        problemas = []
        for checagem in self.checagens:
            try:
                p = checagem(chamada, resultado)
            except Exception as e:  # verificador quebrado não pode derrubar o loop
                p = f"checagem {getattr(checagem, '__name__', '?')} falhou: {e}"
            if p:
                problemas.append(p)
        return problemas
