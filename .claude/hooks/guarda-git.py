#!/usr/bin/env python3
"""Guarda-corpo: operação de git que reescreve história pede confirmação.

Por que existe (spec 094): esta regra não estava nem em prosa. Era hábito. O
repositório publica um livro vivo cuja história de edições **é** parte do
material — o `HISTORICO.md`, o Radar diário, o registro de expiração. Um
`reset --hard` no lugar errado não perde código, perde o registro de como o livro
pensou.

A escolha é `ask`, não `deny`: existem motivos legítimos para todas estas
operações, e um guarda-corpo que proíbe o legítimo é contornado no dia seguinte.
O cap. 07 chama isso de calibrar o raio de alcance — o objetivo é que a operação
seja **deliberada**, não impossível.

Contrato de saída (PreToolUse, JSON em stdout): `permissionDecision: "ask"`
manda o harness perguntar ao humano. Sem JSON e com código 0, passa direto.
"""

import json
import re
import sys

# Cada padrão é uma operação que reescreve ou descarta trabalho já feito.
PERIGOSOS = [
    (r"\bgit\s+push\b[^|;&]*\s--force(?!-with-lease)\b", "push --force sem --force-with-lease"),
    (r"\bgit\s+push\b[^|;&]*\s-f\b", "push -f"),
    (r"\bgit\s+reset\s+--hard\b", "reset --hard"),
    (r"\bgit\s+clean\b[^|;&]*-[a-z]*f[a-z]*d", "clean -fd"),
    (r"\bgit\s+branch\s+-D\b", "branch -D"),
    (r"\bgit\s+rebase\b[^|;&]*\s-i\b", "rebase interativo"),
    (r"\brm\s+-rf?\s+(?!/tmp)(?!\./?docs\b)/?\w", "rm -rf fora de /tmp e docs/"),
]


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except Exception:
        return 0

    comando = str((evento.get("tool_input") or {}).get("command") or "")
    if not comando:
        return 0

    for padrao, nome in PERIGOSOS:
        if re.search(padrao, comando):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        f"`{nome}` reescreve ou descarta trabalho já feito. Neste "
                        f"repositório a história de edições é parte do material "
                        f"publicado (HISTORICO, Radar, registro de expiração). "
                        f"Confirme se é mesmo isso."
                    ),
                }
            }))
            return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
