"""harness-um — a implementação de referência do livro Engenharia de Harness.

O harness-zero ensina a CONSTRUIR (uma feature por etapa, do zero); o
harness-um é o destino: um harness completo, pequeno e legível, com as
features dos capítulos 02–13 reunidas num único sistema coeso.

A decisão central é a LINGUAGEM UBÍQUA: o código fala a língua do livro.
`Harness`, `Turno`, `Ferramenta`, `Politica`, `Memoria`, `Plano`,
`Subagente`, `Verificador`, `Gancho`, `Habilidade`, `Compactador`,
`Provedor` — ler o código é reler o sumário. A tradução para o dialeto de
cada API de modelo acontece só na borda (provedores.py), nunca no domínio.
"""

from .harness import Harness
from .provedores import ProvedorAnthropic, ProvedorEco, Resposta
from .ferramentas import Ferramenta, CaixaDeFerramentas, ferramenta
from .permissoes import Decisao, Politica

__all__ = [
    "Harness",
    "ProvedorAnthropic",
    "ProvedorEco",
    "Resposta",
    "Ferramenta",
    "CaixaDeFerramentas",
    "ferramenta",
    "Decisao",
    "Politica",
]

__version__ = "0.1.0"
