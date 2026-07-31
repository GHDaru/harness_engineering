"""Interface (cap. 13) — o REPL: a menor interface honesta para um agente.

`python -m harness_um` abre a conversa. O humano é o aprovador: toda
chamada PERGUNTAR aparece com nome e argumentos ANTES de executar — a
transparência do cap. 07 na prática. Comandos: /plano /memoria /contexto
/sair. Com `ANTHROPIC_API_KEY` no ambiente usa o modelo real; sem ela,
avisa e usa o ProvedorEco (didático: o loop funciona igual).

Uso único (bom para pipes e testes): python -m harness_um "sua mensagem"
"""

from __future__ import annotations

import argparse
import os
import sys

from .harness import Harness
from .provedores import ProvedorAnthropic, ProvedorEco


def _aprovador_terminal(chamada) -> bool:
    resposta = input(f"  ⚙ aprovar {chamada.nome}({chamada.argumentos})? [s/N] ")
    return resposta.strip().lower() in ("s", "sim", "y", "yes")


def principal() -> int:
    parser = argparse.ArgumentParser(prog="harness_um", description="harness-um — a referência do livro, executável.")
    parser.add_argument("mensagem", nargs="?", help="modo de uso único: responde e sai")
    parser.add_argument("--raiz", default=".", help="raiz do projeto (default: diretório atual)")
    parser.add_argument("--eco", action="store_true", help="força o ProvedorEco (offline)")
    parser.add_argument("--modelo", default="claude-sonnet-4-5", help="modelo Anthropic (com ANTHROPIC_API_KEY)")
    args = parser.parse_args()

    if not args.eco and os.environ.get("ANTHROPIC_API_KEY"):
        provedor = ProvedorAnthropic(modelo=args.modelo)
    else:
        if not args.eco:
            print("(sem ANTHROPIC_API_KEY — usando ProvedorEco; diretivas: @usar ferramenta {\"arg\": ...})")
        provedor = ProvedorEco()

    aprovador = _aprovador_terminal if sys.stdin.isatty() else (lambda chamada: False)
    h = Harness.padrao(args.raiz, provedor=provedor, aprovador=aprovador)

    if args.mensagem:
        print(h.conversar(args.mensagem))
        return 0

    print("harness-um · /plano /memoria /contexto /sair")
    while True:
        try:
            linha = input("\nvocê › ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not linha:
            continue
        if linha == "/sair":
            return 0
        if linha == "/plano":
            print(h.plano.render() or "(plano vazio)")
            continue
        if linha == "/memoria":
            print(h.memoria.ler() or "(memória vazia)")
            continue
        if linha == "/contexto":
            print(h.montador.montar())
            continue
        print("\nagente › " + h.conversar(linha))


if __name__ == "__main__":
    raise SystemExit(principal())
