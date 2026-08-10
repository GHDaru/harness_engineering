#!/usr/bin/env python3
"""Guarda-corpo: identificador interno de modelo não entra em arquivo publicado.

Por que existe (spec 094): o Princípio VI diz que nenhum identificador interno de
modelo aparece em commit, código, comentário ou artefato — o crédito usa o **nome
público do produto** ("Claude Code (Anthropic)", "Claude Opus 5"). Era regra de
prosa, cumprida por atenção. Este hook a torna mecânica.

Como o padrão é montado, e por quê: o hook precisa reconhecer o identificador sem
**conter** um. A solução é montar a expressão a partir de peças — a lista de
famílias (que são nomes públicos, usados no livro) mais a *forma* hifenizada com
dígito. Assim nenhum identificador completo existe literalmente neste arquivo, e
o guarda-corpo não vira a própria violação que persegue.

O que NÃO é bloqueado, de propósito:
  - "Claude Opus 5", "Claude Code", "Claude Fable 5" — nomes públicos, com espaço;
  - `claude-code`, `code.claude.com` — nome de produto e domínio;
  - `claude.ai/code/...` — as URLs de sessão dos rodapés de commit.

Falha do hook não bloqueia (código 0): ver a nota em `guarda-segredo.py`.
"""

import json
import re
import sys

# Nomes públicos de família. Escrevê-los é permitido — o livro os usa. O que a
# constituição proíbe é a FORMA de identificador: família hifenizada + versão.
_FAMILIAS = ("opus", "sonnet", "haiku", "fable")
_FORMA = r"\b(?:[a-z0-9_.]+\.)?claude-(?:" + "|".join(_FAMILIAS) + r")-\d"
IDENTIFICADOR = re.compile(_FORMA, re.IGNORECASE)

# Este hook e a spec que o criou precisam descrever a regra para poder explicá-la.
ISENTOS = re.compile(
    r"(^|/)\.claude/hooks/"
    r"|(^|/)specs/094-medir-o-proprio-harness/"
)


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except Exception:
        return 0

    entrada = evento.get("tool_input") or {}
    caminho = str(entrada.get("file_path") or "")
    if ISENTOS.search(caminho):
        return 0

    texto = " ".join(
        str(entrada.get(campo) or "") for campo in ("content", "new_string")
    )
    achado = IDENTIFICADOR.search(texto or "")
    if not achado:
        return 0

    print(
        "BLOQUEADO: identificador interno de modelo no conteúdo "
        f"(casou com a forma '{achado.group(0)[:12]}…').\n"
        "Princípio VI: em commit, código, comentário ou artefato publicado, use o "
        "NOME PÚBLICO do produto — 'Claude Code (Anthropic)' no crédito A3 do "
        "HISTÓRICO, 'Claude Opus 5' quando a versão importar.\n"
        "Se o texto precisa mesmo citar a forma técnica, ele pertence ao chat, "
        "não a um arquivo do repositório.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
