"""Compactação (cap. 04) — a janela é finita; a conversa, não.

Estratégia de referência: quando a estimativa de tokens do histórico passa
do limite, as mensagens antigas viram UM resumo estrutural (o que se pediu,
que ferramentas rodaram, o que veio) e a CAUDA recente fica intacta — o
modelo perde a prosa velha, nunca o presente. A estimativa `caracteres/4`
é crua de propósito: compactação precisa ser barata, senão ela mesma vira
o custo (a lição do capítulo).
"""

from __future__ import annotations

from dataclasses import dataclass

from .provedores import Mensagem


def estimar_tokens(mensagens: list[Mensagem]) -> int:
    return sum(len(str(m.get("content", ""))) for m in mensagens) // 4


@dataclass
class Compactador:
    limite_tokens: int = 24000
    cauda: int = 6  # mensagens recentes preservadas na íntegra

    def precisa(self, mensagens: list[Mensagem]) -> bool:
        return estimar_tokens(mensagens) > self.limite_tokens

    def compactar(self, mensagens: list[Mensagem]) -> list[Mensagem]:
        if len(mensagens) <= self.cauda:
            return mensagens
        # O corte cai numa mensagem do assistente: o resumo (user) + cauda
        # continuam alternando papéis e nenhum resultado de ferramenta fica
        # órfão do seu uso_de_ferramenta — exigências da API real.
        corte = len(mensagens) - self.cauda
        while corte < len(mensagens) and mensagens[corte]["role"] != "assistant":
            corte += 1
        if corte >= len(mensagens):
            return mensagens
        antigas, recentes = mensagens[:corte], mensagens[corte:]
        pedidos, ferramentas = [], []
        for m in antigas:
            blocos = m["content"] if isinstance(m["content"], list) else [{"tipo": "texto", "texto": str(m["content"])}]
            for b in blocos:
                if m["role"] == "user" and b.get("tipo") == "texto" and b.get("texto"):
                    pedidos.append(b["texto"][:100])
                if b.get("tipo") == "uso_de_ferramenta":
                    ferramentas.append(b["nome"])
        resumo = (
            f"[resumo de {len(antigas)} mensagens compactadas]\n"
            f"Pedidos: {'; '.join(pedidos[-5:]) or '—'}\n"
            f"Ferramentas usadas: {', '.join(ferramentas) or '—'}"
        )
        return [{"role": "user", "content": [{"tipo": "texto", "texto": resumo}]}] + recentes
