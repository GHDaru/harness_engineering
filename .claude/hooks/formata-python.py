#!/usr/bin/env python3
"""Sensor de realimentação: arquivo Python editado passa pelo formatador.

Por que existe (spec 094): é o mais modesto dos quatro hooks e o mais fiel ao
cap. 11 — realimentar sinal real no mesmo turno, em vez de esperar a revisão.
Ruído de formatação em diff **esconde erro de verdade** de quem revisa; corrigir
na hora custa milissegundos e devolve o diff à sua função.

Best-effort de propósito: sem Ruff instalado, ele se cala e sai com 0. Um hook
de conveniência que quebra o trabalho quando a ferramenta falta é um hook que
será desligado — e aí a conveniência vira zero.
"""

import json
import shutil
import subprocess
import sys


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except Exception:
        return 0

    caminho = str((evento.get("tool_input") or {}).get("file_path") or "")
    if not caminho.endswith(".py"):
        return 0
    if not shutil.which("ruff"):
        return 0

    try:
        subprocess.run(
            ["ruff", "format", "--quiet", caminho],
            check=False, capture_output=True, timeout=20,
        )
    except Exception:
        pass  # formatação é conveniência; nunca é motivo para atrapalhar o turno

    return 0


if __name__ == "__main__":
    sys.exit(main())
