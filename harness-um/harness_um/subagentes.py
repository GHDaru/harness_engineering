"""Subagentes (cap. 10) — dividir para conquistar, com isolamento.

A tool `tarefa(descricao)` cria um loop-FILHO: mesmo provedor, mesmo loop,
mas contexto ZERADO (só a descrição), caixa restrita a leitura e política
que nega o resto sem perguntar — filho não muta o mundo nem incomoda o
humano. As duas fronteiras são a lição do capítulo: na ida vai só a
descrição; na volta vem só o resultado final. É isso que mantém o contexto
do pai limpo — o motivo de existir subagente.
"""

from __future__ import annotations

from .ferramentas import CaixaDeFerramentas, Ferramenta
from .loop import LoopDoAgente
from .permissoes import Decisao, Politica
from .provedores import Provedor

SO_LEITURA = ("ler_arquivo", "listar_diretorio")

SISTEMA_FILHO = (
    "Você é um subagente do harness-um com uma única tarefa, descrita na "
    "mensagem do usuário. Você só tem ferramentas de leitura. Ao terminar, "
    "responda com o resultado final — apenas ele voltará ao agente-pai."
)


def ferramenta_tarefa(provedor: Provedor, caixa_do_pai: CaixaDeFerramentas, max_turnos: int = 6) -> Ferramenta:
    def tarefa(descricao: str) -> str:
        filho = LoopDoAgente(
            provedor=provedor,
            caixa=caixa_do_pai.subconjunto(list(SO_LEITURA)),
            politica=Politica(regras={n: Decisao.PERMITIR for n in SO_LEITURA}, padrao=Decisao.NEGAR),
            max_turnos=max_turnos,
        )
        historico = [{"role": "user", "content": [{"tipo": "texto", "texto": descricao}]}]
        return filho.executar(historico, SISTEMA_FILHO)

    return Ferramenta(
        nome="tarefa",
        descricao="Delega uma tarefa de investigação a um subagente com contexto limpo e ferramentas só de leitura; devolve apenas o resultado final.",
        esquema={"type": "object", "properties": {"descricao": {"type": "string"}}, "required": ["descricao"]},
        executar=tarefa,
    )
