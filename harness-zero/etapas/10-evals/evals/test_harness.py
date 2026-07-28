"""Evals do harness-zero — a etapa 10 aplicada a si mesma (cap. 11).

Cada teste verifica um COMPORTAMENTO DO HARNESS, com respostas gravadas
(ReplayAdapter) — nunca o humor de um modelo real. Rode:
    cd etapas/10-evals && python -m pytest evals/ -q
"""

import os
import sys
from pathlib import Path

AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent))
os.environ.setdefault("STORE_ADAPTER", "memoria")  # evals não sujam o sqlite

import app  # noqa: E402
from replay import ReplayAdapter  # noqa: E402
from juiz import julgar  # noqa: E402


def test_politica_nega_paths_sensiveis():
    assert app.decide("read_file", {"path": "/home/x/.env"}) == "negar"
    assert app.decide("read_file", {"path": "~/.ssh/id_rsa"}) == "negar"
    assert app.decide("read_file", {"path": "notas.txt"}) == "permitir"


def test_plan_mode_nega_mutantes():
    assert app.decide("write_file", {"path": "x"}, "planejar") == "negar"
    assert app.decide("write_file", {"path": "x"}, "executar") == "perguntar"


def test_schema_derivado_de_tipos():
    sch = {t["function"]["name"]: t["function"] for t in app.tools.schemas()}
    assert sch["read_file"]["parameters"]["required"] == ["path"]  # max_chars é opcional
    assert sch["read_file"]["parameters"]["properties"]["max_chars"]["type"] == "integer"


def test_compactador_escada_age_no_orcamento():
    msgs = [{"role": "system", "content": "s"}] + [
        {"role": "user", "content": "x" * 300} for _ in range(20)]
    trace = []
    out = app.compactador.compactar(msgs, ReplayAdapter(AQUI / "gravacoes/escreve_arquivo.jsonl"), trace)
    assert len(out) < len(msgs) and any("compactador" in t for t in trace)


def test_replay_write_file_pausa_para_aprovacao():
    """A gravação pede write_file -> o harness DEVE pausar (perguntar), não executar."""
    app.llm = ReplayAdapter(AQUI / "gravacoes/escreve_arquivo.jsonl")
    r = app.chat(app.ChatIn(message="escreva saida_eval.txt"))
    assert r["pendente"] is not None and r["pendente"]["tool"] == "write_file"
    assert not (AQUI.parent / "saida_eval.txt").exists()  # nada foi escrito sem humano
    r2 = app.aprovar(app.DecisaoIn(id=r["pendente"]["id"]))
    assert r2["reply"] == "arquivo escrito."
    assert (AQUI.parent / "saida_eval.txt").exists()
    (AQUI.parent / "saida_eval.txt").unlink()


def test_juiz_degrada_sem_modelo_real():
    veredicto = julgar(app.EchoAdapter(), "o que é um harness?", "é o andaime do agente",
                       ["correção", "concisão"])
    assert "nota" in veredicto  # echo -> nota None com justificativa honesta
