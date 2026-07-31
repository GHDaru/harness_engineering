"""O loop do agente (cap. 02) — o coração de todo harness.

O ciclo canônico: montar contexto → chamar o modelo → executar ferramentas
→ devolver resultados → repetir, sob um ORÇAMENTO de turnos. Tudo que os
outros módulos oferecem se encontra aqui, cada um no seu ponto do ciclo:
compactação antes de gerar, política e ganchos antes de executar,
verificação depois de mutar, sessão registrando cada passo. O loop em si
cabe numa tela — a complexidade de um harness não está no loop, está no
que ele orquestra (a tese do capítulo).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .compactacao import Compactador
from .extensao import GerenciadorDeGanchos
from .ferramentas import CaixaDeFerramentas
from .memoria import Sessao
from .permissoes import Aprovador, Decisao, Politica
from .provedores import ChamadaDeFerramenta, Mensagem, Provedor
from .verificacao import Verificador

Observador = Callable[[str, dict], None]  # eventos: turno, chamada, resultado, fim


@dataclass
class LoopDoAgente:
    provedor: Provedor
    caixa: CaixaDeFerramentas
    politica: Politica = field(default_factory=Politica.padrao_segura)
    aprovador: Aprovador = lambda chamada: False  # sem humano, PERGUNTAR nega
    ganchos: GerenciadorDeGanchos = field(default_factory=GerenciadorDeGanchos)
    verificador: Verificador = field(default_factory=Verificador)
    compactador: Compactador = field(default_factory=Compactador)
    sessao: Sessao | None = None
    max_turnos: int = 12
    observador: Observador = lambda evento, dados: None

    def executar(self, historico: list[Mensagem], sistema: str) -> str:
        for turno in range(1, self.max_turnos + 1):
            self.ganchos.emitir("antes_turno", {"turno": turno})
            if self.compactador.precisa(historico):
                historico[:] = self.compactador.compactar(historico)
                self.observador("compactacao", {"mensagens": len(historico)})
            resposta = self.provedor.gerar(sistema, historico, self.caixa.esquemas())
            self.observador("turno", {"n": turno, "parada": resposta.parada, "uso": resposta.uso})

            blocos = []
            if resposta.texto:
                blocos.append({"tipo": "texto", "texto": resposta.texto})
            for c in resposta.chamadas:
                blocos.append({"tipo": "uso_de_ferramenta", "id": c.id, "nome": c.nome, "argumentos": c.argumentos})
            self._registrar(historico, {"role": "assistant", "content": blocos})

            if not resposta.chamadas:
                self.observador("fim", {"turnos": turno})
                return resposta.texto

            resultados = []
            for c in resposta.chamadas:
                resultado = self._executar_chamada(c)
                self.observador("resultado", {"nome": c.nome, "resultado": resultado[:200]})
                resultados.append({"tipo": "resultado_de_ferramenta", "id": c.id, "conteudo": resultado})
            self._registrar(historico, {"role": "user", "content": resultados})

        return "(orçamento de turnos esgotado — o loop parou antes do modelo)"

    def _executar_chamada(self, c: ChamadaDeFerramenta) -> str:
        decisao = self.politica.decidir(c)
        self.observador("chamada", {"nome": c.nome, "argumentos": c.argumentos, "decisao": decisao.value})
        if decisao is Decisao.NEGAR:
            return f"chamada a {c.nome} negada pela política"
        if decisao is Decisao.PERGUNTAR and not self.aprovador(c):
            return f"chamada a {c.nome} negada pelo humano"
        veto = self.ganchos.emitir("antes_ferramenta", {"nome": c.nome, "argumentos": c.argumentos})
        if veto:
            return f"chamada a {c.nome} vetada por gancho: {veto}"
        resultado = self.caixa.executar(c.nome, c.argumentos)
        self.ganchos.emitir("depois_ferramenta", {"nome": c.nome, "resultado": resultado})
        f = self.caixa.obter(c.nome)
        if f and f.muta:
            problemas = self.verificador.verificar(c, resultado)
            if problemas:
                resultado += "\n⚠ verificação: " + "; ".join(problemas)
        return resultado

    def _registrar(self, historico: list[Mensagem], mensagem: Mensagem) -> None:
        historico.append(mensagem)
        if self.sessao:
            self.sessao.registrar(mensagem)
