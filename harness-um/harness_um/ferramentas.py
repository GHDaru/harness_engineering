"""Ferramentas (cap. 05) — o vocabulário de ação do agente.

Três lições do capítulo, em código:
1. O esquema NASCE da assinatura da função (`ferramenta(fn)`) — uma fonte de
   verdade só; esquema desatualizado é o bug clássico de tool-use.
2. A descrição É prompt: a primeira linha da docstring vai ao modelo.
3. Toda ferramenta que toca o disco é presa à `raiz` — path traversal não é
   permissão (cap. 07), é invariante da própria ferramenta.
"""

from __future__ import annotations

import inspect
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

_TIPOS = {str: "string", int: "integer", float: "number", bool: "boolean"}


@dataclass
class Ferramenta:
    nome: str
    descricao: str
    esquema: dict
    executar: Callable[..., str]
    muta: bool = False  # mutantes passam por verificação pós-uso (cap. 11)

    def como_esquema(self) -> dict:
        return {"nome": self.nome, "descricao": self.descricao, "esquema": self.esquema}


def ferramenta(fn: Callable | None = None, *, muta: bool = False) -> Ferramenta | Callable:
    """Decora uma função Python e deriva a Ferramenta (esquema pela assinatura)."""

    def montar(f: Callable) -> Ferramenta:
        assinatura = inspect.signature(f)
        propriedades, obrigatorios = {}, []
        for nome, par in assinatura.parameters.items():
            tipo = _TIPOS.get(par.annotation, "string")
            propriedades[nome] = {"type": tipo}
            if par.default is inspect.Parameter.empty:
                obrigatorios.append(nome)
        doc = (f.__doc__ or f.__name__).strip().splitlines()[0]
        return Ferramenta(
            nome=f.__name__,
            descricao=doc,
            esquema={"type": "object", "properties": propriedades, "required": obrigatorios},
            executar=f,
            muta=muta,
        )

    return montar(fn) if fn else montar


@dataclass
class CaixaDeFerramentas:
    ferramentas: dict[str, Ferramenta] = field(default_factory=dict)

    def registrar(self, f: Ferramenta) -> None:
        self.ferramentas[f.nome] = f

    def esquemas(self) -> list[dict]:
        return [f.como_esquema() for f in self.ferramentas.values()]

    def obter(self, nome: str) -> Ferramenta | None:
        return self.ferramentas.get(nome)

    def subconjunto(self, nomes: list[str]) -> "CaixaDeFerramentas":
        """Caixa restrita — é assim que um subagente perde o direito de mutar (cap. 10)."""
        return CaixaDeFerramentas({n: f for n, f in self.ferramentas.items() if n in nomes})

    def executar(self, nome: str, argumentos: dict) -> str:
        f = self.obter(nome)
        if not f:
            return f"erro: ferramenta desconhecida '{nome}'"
        try:
            return str(f.executar(**argumentos))
        except Exception as e:  # o loop nunca morre por causa de uma ferramenta
            return f"erro ao executar {nome}: {e}"


def caixa_padrao(raiz: Path) -> CaixaDeFerramentas:
    """As quatro ferramentas de base, presas à raiz do projeto."""
    raiz = Path(raiz).resolve()

    def _dentro(caminho: str) -> Path:
        alvo = (raiz / caminho).resolve()
        if raiz != alvo and raiz not in alvo.parents:
            raise ValueError(f"caminho fora da raiz do projeto: {caminho}")
        return alvo

    @ferramenta
    def ler_arquivo(caminho: str) -> str:
        """Lê um arquivo de texto relativo à raiz do projeto."""
        return _dentro(caminho).read_text(encoding="utf-8")

    @ferramenta(muta=True)
    def escrever_arquivo(caminho: str, conteudo: str) -> str:
        """Escreve (sobrescreve) um arquivo de texto relativo à raiz do projeto."""
        alvo = _dentro(caminho)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(conteudo, encoding="utf-8")
        return f"escrito: {caminho} ({len(conteudo)} caracteres)"

    @ferramenta
    def listar_diretorio(caminho: str = ".") -> str:
        """Lista os arquivos de um diretório relativo à raiz do projeto."""
        return "\n".join(sorted(p.name + ("/" if p.is_dir() else "") for p in _dentro(caminho).iterdir()))

    @ferramenta(muta=True)
    def executar_shell(comando: str) -> str:
        """Executa um comando de shell na raiz do projeto (timeout de 30s)."""
        r = subprocess.run(comando, shell=True, cwd=raiz, capture_output=True, text=True, timeout=30)
        saida = (r.stdout + r.stderr).strip()
        return saida[:8000] if saida else f"(sem saída; exit {r.returncode})"

    caixa = CaixaDeFerramentas()
    for f in (ler_arquivo, escrever_arquivo, listar_diretorio, executar_shell):
        caixa.registrar(f)
    return caixa
