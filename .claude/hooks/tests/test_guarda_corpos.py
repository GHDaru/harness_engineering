"""Testes dos guarda-corpos do repositório (spec 094).

Um hook sem teste é uma promessa com sintaxe. Estes casos existem para que o
guarda-corpo continue guardando depois que ninguém lembrar por que ele existe —
e, principalmente, para que os casos que ele deve DEIXAR PASSAR sejam tão
explícitos quanto os que ele deve bloquear: um guarda-corpo que atrapalha o
trabalho legítimo é desligado, e aí protege zero.

Contrato do PreToolUse: código 2 bloqueia (o stderr volta ao modelo); código 0
deixa passar. `guarda-git` usa a terceira via — JSON com `permissionDecision:
"ask"` — para pedir confirmação humana em vez de proibir.
"""

import json
import subprocess
from pathlib import Path

import pytest

HOOKS = Path(__file__).resolve().parent.parent


def roda(hook: str, evento: dict) -> tuple[int, str, str]:
    p = subprocess.run(
        ["python3", str(HOOKS / hook)],
        input=json.dumps(evento), capture_output=True, text=True, timeout=30,
    )
    return p.returncode, p.stdout, p.stderr


def escrita(caminho: str, conteudo: str) -> dict:
    return {"tool_name": "Write", "tool_input": {"file_path": caminho, "content": conteudo}}


def edicao(caminho: str, novo: str) -> dict:
    return {"tool_name": "Edit", "tool_input": {"file_path": caminho, "new_string": novo}}


def bash(comando: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": comando}}


# ------------------------------------------------------------ guarda-segredo
# As "credenciais" abaixo são montadas por concatenação e repetição justamente
# para que este arquivo não contenha nada que se pareça com uma chave de verdade.

@pytest.mark.parametrize("conteudo,nome", [
    ("K = \"re_" + "A" * 24 + "\"", "Resend"),
    ("ghp_" + "b" * 36, "GitHub"),
    ("AKIA" + "C" * 16, "AWS"),
    ("postgresql://u:sup3rsecreta@host/db", "URL de banco com senha"),
    ("-----BEGIN RSA PRIVATE KEY-----", "chave privada"),
    ("sk-ant-" + "d" * 24, "Anthropic"),
    ("xoxb-" + "e" * 24, "Slack"),
])
def test_segredo_e_bloqueado(conteudo, nome):
    rc, _, err = roda("guarda-segredo.py", escrita("chat-companion/backend/config.py", conteudo))
    assert rc == 2, f"{nome} passou"
    assert "BLOQUEADO" in err


@pytest.mark.parametrize("caminho,conteudo", [
    (".env", "RESEND_API_KEY=re_" + "A" * 24),                       # é o lugar dele, e é gitignored
    ("livro/capitulos/07-permissoes-sandbox.md", "Nunca comite uma chave."),
    ("docs.md", "sk-EXEMPLO-NAO-E-UMA-CHAVE"),                        # exemplo didático
    ("README.md", "postgresql://localhost/harness"),                  # sem senha
])
def test_conteudo_legitimo_passa(caminho, conteudo):
    rc, _, _ = roda("guarda-segredo.py", escrita(caminho, conteudo))
    assert rc == 0


# --------------------------------------------------------- guarda-identidade

@pytest.mark.parametrize("texto", [
    "rodou em claude-" + "opus" + "-5",
    "us.anthropic.claude-" + "sonnet" + "-5-v1",
    "modelo: claude-" + "haiku" + "-4",
])
def test_identificador_interno_e_bloqueado(texto):
    rc, _, err = roda("guarda-identidade.py", escrita("livro/HISTORICO.md", texto))
    assert rc == 2
    assert "Princípio VI" in err


@pytest.mark.parametrize("texto", [
    "IA (A3): Claude Code (Anthropic)",          # o crédito que a constituição MANDA usar
    "Claude Opus 5 com janela de 1M",            # nome público, com espaço
    "o claude-code corrigiu oito furos",         # nome de produto
    "https://claude.ai/code/session_01Tc",       # rodapé de commit
    "code.claude.com/docs/en/changelog",         # domínio citado no Radar
])
def test_nome_publico_passa(texto):
    rc, _, _ = roda("guarda-identidade.py", escrita("radar/RADAR.md", texto))
    assert rc == 0


# --------------------------------------------------------------- guarda-git

@pytest.mark.parametrize("comando", [
    "git push --force origin main",
    "git push -f",
    "git reset --hard origin/main",
    "git clean -fdx",
    "git branch -D 093-progresso",
    "rm -rf build",
])
def test_git_destrutivo_pede_confirmacao(comando):
    rc, out, _ = roda("guarda-git.py", bash(comando))
    assert rc == 0
    assert json.loads(out)["hookSpecificOutput"]["permissionDecision"] == "ask"


@pytest.mark.parametrize("comando", [
    "git push -u origin main",                        # o push do contrato
    "git push --force-with-lease origin 094-medir",   # force COM trava: legítimo
    "git status",
    "git commit -m 'x'",
    "rm -rf /tmp/claude-0/scratch",                   # temporário
])
def test_git_legitimo_passa(comando):
    rc, out, _ = roda("guarda-git.py", bash(comando))
    assert rc == 0
    assert "ask" not in out


# ------------------------------------------------------------- robustez geral

@pytest.mark.parametrize("hook", [
    "guarda-segredo.py", "guarda-identidade.py", "guarda-git.py", "formata-python.py",
])
def test_entrada_invalida_nunca_bloqueia(hook):
    """Guarda-corpo que quebra o trabalho ao quebrar a si mesmo é pior que a
    ausência dele. Entrada ilegível => sai 0 e sai de cena."""
    p = subprocess.run(["python3", str(HOOKS / hook)], input="isto nao e json",
                       capture_output=True, text=True, timeout=30)
    assert p.returncode == 0


@pytest.mark.parametrize("hook", ["guarda-segredo.py", "guarda-identidade.py"])
def test_evento_sem_conteudo_passa(hook):
    rc, _, _ = roda(hook, {"tool_name": "Read", "tool_input": {"file_path": "x.md"}})
    assert rc == 0


def test_formatador_ignora_arquivo_nao_python():
    rc, _, _ = roda("formata-python.py", escrita("livro/HISTORICO.md", "# titulo"))
    assert rc == 0
