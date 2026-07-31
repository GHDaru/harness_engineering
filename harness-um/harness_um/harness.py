"""Harness — o agregado que monta tudo (composição, não herança).

`Harness.padrao(raiz)` é o livro inteiro em uma chamada: caixa de
ferramentas presa à raiz (05) + subagente (10) + memória e sessão (08) +
plano (09) + habilidades (12) + MCP opcional (06), contexto montado em
camadas (03), tudo orbitando um LoopDoAgente (02) com política (07),
ganchos (12), verificação (11) e compactação (04). Cada linha do
construtor aponta para um capítulo — é o mapa do livro executável.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .contexto import MontadorDeContexto
from .extensao import GerenciadorDeGanchos, carregar_habilidades
from .ferramentas import CaixaDeFerramentas, caixa_padrao, ferramenta
from .loop import LoopDoAgente, Observador
from .mcp import ClienteMCP
from .memoria import Memoria, Sessao
from .permissoes import Aprovador, Decisao, Politica
from .plano import Plano
from .provedores import Mensagem, Provedor, ProvedorEco
from .subagentes import ferramenta_tarefa


@dataclass
class Harness:
    raiz: Path
    provedor: Provedor
    loop: LoopDoAgente
    montador: MontadorDeContexto
    memoria: Memoria
    plano: Plano
    historico: list[Mensagem] = field(default_factory=list)

    @classmethod
    def padrao(
        cls,
        raiz: str | Path,
        provedor: Provedor | None = None,
        aprovador: Aprovador | None = None,
        urls_mcp: tuple[str, ...] = (),
        observador: Observador | None = None,
    ) -> "Harness":
        raiz = Path(raiz).resolve()
        provedor = provedor or ProvedorEco()
        estado = raiz / ".harness-um"

        memoria = Memoria(estado / "MEMORIA.md")               # cap. 08
        plano = Plano.carregar(estado / "plano.json")          # cap. 09
        sessao = Sessao(estado / "sessoes")                    # cap. 08
        habilidades = carregar_habilidades(raiz / "habilidades")  # cap. 12

        caixa = caixa_padrao(raiz)                             # cap. 05
        caixa.registrar(ferramenta_tarefa(provedor, caixa))    # cap. 10
        for url in urls_mcp:                                   # cap. 06
            for f in ClienteMCP(url).como_ferramentas():
                caixa.registrar(f)

        @ferramenta
        def anotar_memoria(nota: str) -> str:
            """Anota um fato durável em MEMORIA.md (sobrevive à conversa)."""
            return memoria.anotar(nota)

        @ferramenta
        def plano_adicionar(texto: str) -> str:
            """Adiciona um item ao plano persistente."""
            return plano.adicionar(texto)

        @ferramenta
        def plano_marcar(id: int, estado: str) -> str:
            """Marca um item do plano: pendente, em_andamento ou concluido."""
            return plano.marcar(id, estado)

        def _invocar_habilidade(nome: str) -> str:
            for h in habilidades:
                if h.nome == nome:
                    return h.corpo
            return f"habilidade desconhecida: {nome} (disponíveis: {', '.join(h.nome for h in habilidades) or 'nenhuma'})"

        @ferramenta
        def invocar_habilidade(nome: str) -> str:
            """Carrega o corpo completo de uma habilidade (divulgação progressiva)."""
            return _invocar_habilidade(nome)

        for f in (anotar_memoria, plano_adicionar, plano_marcar, invocar_habilidade):
            caixa.registrar(f)

        politica = Politica.padrao_segura()                    # cap. 07
        for nome in ("anotar_memoria", "plano_adicionar", "plano_marcar", "invocar_habilidade"):
            politica.regras[nome] = Decisao.PERMITIR

        montador = MontadorDeContexto()                        # cap. 03
        montador.adicionar("Memória durável (MEMORIA.md)", memoria.ler)
        montador.adicionar("Plano atual", plano.render)
        montador.adicionar(
            "Habilidades disponíveis (use invocar_habilidade)",
            lambda: "\n".join(f"- {h.nome}: {h.descricao}" for h in habilidades),
        )

        loop = LoopDoAgente(                                   # cap. 02
            provedor=provedor,
            caixa=caixa,
            politica=politica,
            aprovador=aprovador or (lambda chamada: False),
            ganchos=GerenciadorDeGanchos(),                    # cap. 12
            sessao=sessao,
            observador=observador or (lambda evento, dados: None),
        )
        return cls(raiz=raiz, provedor=provedor, loop=loop, montador=montador, memoria=memoria, plano=plano)

    def conversar(self, texto: str) -> str:
        """Um turno de conversa: contexto remontado, loop até resposta final."""
        mensagem = {"role": "user", "content": [{"tipo": "texto", "texto": texto}]}
        self.historico.append(mensagem)
        if self.loop.sessao:
            self.loop.sessao.registrar(mensagem)
        return self.loop.executar(self.historico, self.montador.montar())

    @property
    def caixa(self) -> CaixaDeFerramentas:
        return self.loop.caixa
