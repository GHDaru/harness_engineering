"""ReplayAdapter — respostas GRAVADAS: o segredo de evals determinísticos.

Testar um harness chamando um modelo de verdade é caro, lento e flakey.
O padrão dos harnesses reais (cap. 11): gravar as respostas uma vez e
REPRODUZI-LAS nos testes. O eval passa a testar o HARNESS — política,
loop, compactação — e não o humor do modelo.
"""

import json
from pathlib import Path


class ReplayAdapter:
    """Um LLMPort que devolve, em ordem, as respostas de um .jsonl gravado."""

    def __init__(self, gravacao: str | Path):
        linhas = Path(gravacao).read_text().strip().splitlines()
        self._respostas = [json.loads(l) for l in linhas]
        self._i = 0

    def complete(self, messages, tools):
        if self._i >= len(self._respostas):
            return {"role": "assistant", "content": "(gravação esgotada)"}
        r = self._respostas[self._i]
        self._i += 1
        return r
