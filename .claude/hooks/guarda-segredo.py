#!/usr/bin/env python3
"""Guarda-corpo: nenhuma credencial entra em arquivo deste repositório.

Por que existe (spec 094): o Princípio IV da constituição diz "nada de segredo em
arquivo ou commit". Até 2026-08-10 isso era uma frase — cumprida por disciplina,
verificada por revisão humana, e portanto sujeita à primeira distração. A medição
do Harness Score deu zero em "Hooks & Guardrails" num repositório que dedica um
capítulo inteiro a permissões, e o diagnóstico era esse: a regra existia só como
prosa.

Um hook não é mais inteligente que a revisão humana. É mais **chato** — e a
disciplina do cap. 07 é justamente essa: o controle que vale é o que não depende
de alguém lembrar.

Contrato de saída (PreToolUse): código 2 bloqueia a ferramenta e devolve o stderr
ao modelo; 0 deixa passar. Falha do próprio hook NÃO bloqueia (código 0): um
guarda-corpo que quebra o trabalho ao quebrar a si mesmo é pior que a ausência
dele — vira o `--full-auto` que o Codex removeu.
"""

import json
import re
import sys

# Assinaturas de credencial, não heurísticas de "parece segredo". Cada uma é um
# formato publicado por quem o emite; falso positivo aqui custa uma edição, falso
# negativo custa uma chave viva num repositório público.
ASSINATURAS = [
    (r"\bre_[A-Za-z0-9]{20,}", "chave da API do Resend"),
    (r"\bsk-[A-Za-z0-9]{20,}", "chave de API no formato OpenAI"),
    (r"\bsk-ant-[A-Za-z0-9_-]{20,}", "chave de API da Anthropic"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}", "token do GitHub"),
    (r"\bAKIA[0-9A-Z]{16}\b", "chave de acesso da AWS"),
    (r"\bnvapi-[A-Za-z0-9_-]{20,}", "chave da NVIDIA NIM"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "chave privada"),
    (r"postgres(?:ql)?://[^\s:@/]+:[^\s@/]{6,}@", "URL de banco com senha"),
    (r"\bxox[baprs]-[A-Za-z0-9-]{20,}", "token do Slack"),
]

# `.env` é gitignored e existe para guardar exatamente isto; os arquivos desta
# spec CITAM as assinaturas para poder explicá-las.
ISENTOS = re.compile(
    r"(^|/)\.env(\.|$)"
    r"|(^|/)\.claude/hooks/"
    r"|(^|/)specs/094-medir-o-proprio-harness/"
)


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except Exception:
        return 0  # sem entrada legível, não é hora de bloquear ninguém

    entrada = evento.get("tool_input") or {}
    caminho = str(entrada.get("file_path") or "")
    if ISENTOS.search(caminho):
        return 0

    # Write manda `content`; Edit manda `new_string`. Só o que vai ENTRAR importa.
    texto = " ".join(
        str(entrada.get(campo) or "") for campo in ("content", "new_string")
    )
    if not texto:
        return 0

    for padrao, nome in ASSINATURAS:
        if re.search(padrao, texto):
            print(
                f"BLOQUEADO: o conteúdo tem assinatura de {nome}.\n"
                f"Princípio IV da constituição: credencial vive só em variável de "
                f"ambiente (Railway) ou em `.env`, que é gitignored.\n"
                f"Se for exemplo didático, use um valor obviamente falso "
                f"(ex.: 'sk-EXEMPLO-NAO-E-UMA-CHAVE').",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
