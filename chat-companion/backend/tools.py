"""ToolPort — o registro de tools SEGURAS do companion.

Regra do cap. 07 aplicada à superfície pública: nada de shell, nada de leitura
arbitrária de disco, nada de rede de saída. Só tools sandbox, com efeito
limitado e previsível. Cada tool tem um schema (dialeto OpenAI) e está amarrada
a uma capacidade em `capabilities.py` — o gating decide quais entram no loop.

Nota didática: derivar schema de tipos é a lição da etapa 02 (cap. 05); aqui os
schemas ainda são à mão, de propósito — a mesma dor que justifica aquela etapa.
"""

from __future__ import annotations

import ast
import datetime
import operator
from typing import Callable

from ragindex import BookIndex


# ------------------------------------------------------ implementações seguras

def _hora(_args: dict) -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


# Avaliador aritmético seguro: só números e + - * / ** ( ) unário. Sem nomes,
# sem chamadas, sem atributos — não é eval() do Python (que seria uma ferida).
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _eval_no(no: ast.AST) -> float:
    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
        return no.value
    if isinstance(no, ast.BinOp) and type(no.op) in _OPS:
        return _OPS[type(no.op)](_eval_no(no.left), _eval_no(no.right))
    if isinstance(no, ast.UnaryOp) and type(no.op) in _OPS:
        return _OPS[type(no.op)](_eval_no(no.operand))
    raise ValueError("expressão não permitida")


def _calcular(args: dict) -> str:
    expr = str(args.get("expressao", ""))
    try:
        return str(_eval_no(ast.parse(expr, mode="eval").body))
    except Exception as exc:  # erro volta como texto para o modelo decidir
        return f"erro: {exc}"


class Tools:
    """Fecha as tools sobre o índice do livro (dependência injetada)."""

    def __init__(self, index: BookIndex) -> None:
        self._index = index
        self.impls: dict[str, Callable[[dict], str]] = {
            "hora": _hora,
            "calcular": _calcular,
            "buscar_no_livro": self._buscar_no_livro,
        }

    def _buscar_no_livro(self, args: dict) -> str:
        achados = self._index.buscar(str(args.get("consulta", "")), k=4)
        if not achados:
            return "nada encontrado no livro para essa consulta."
        return "\n\n".join(f"[{a['fonte']} · {a['titulo']}] {a['trecho']}" for a in achados)

    def schemas_para(self, nomes: set[str]) -> list[dict]:
        """Só os schemas das tools ativas (gating)."""
        todos = {
            "hora": {"type": "function", "function": {
                "name": "hora",
                "description": "Retorna a data e hora atuais (ISO).",
                "parameters": {"type": "object", "properties": {}, "required": []}}},
            "calcular": {"type": "function", "function": {
                "name": "calcular",
                "description": "Avalia uma expressão aritmética segura (+ - * / ** %).",
                "parameters": {"type": "object",
                               "properties": {"expressao": {"type": "string",
                                              "description": "ex.: (2+3)*4"}},
                               "required": ["expressao"]}}},
            "buscar_no_livro": {"type": "function", "function": {
                "name": "buscar_no_livro",
                "description": "Busca trechos relevantes no texto do livro.",
                "parameters": {"type": "object",
                               "properties": {"consulta": {"type": "string",
                                              "description": "o que procurar no livro"}},
                               "required": ["consulta"]}}},
        }
        return [todos[n] for n in nomes if n in todos]

    def executar(self, nome: str, args: dict, permitidas: set[str]) -> str:
        if nome not in permitidas:                       # gating também na execução
            return f"erro: ferramenta '{nome}' não está habilitada neste capítulo."
        impl = self.impls.get(nome)
        return impl(args) if impl else f"erro: ferramenta desconhecida '{nome}'"
