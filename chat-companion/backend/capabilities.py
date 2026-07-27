"""Registro de capacidades e o gating por capítulo.

Duas modalidades (decisão do autor):
  - "avancado": tudo liberado (o companion completo).
  - "progressivo": só o que o livro já ensinou até o capítulo atual — o
    *fading* do 4C/ID e a carga cognitiva do cap. 04 virando comportamento:
    o companion só oferece o que o leitor já viu.

Cada capacidade declara em que capítulo é liberada e quais tools habilita.
O widget usa `capacidades(chapter, mode)` para mostrar "o que posso fazer agora".
`tools_ativas` e `loop_ativo` decidem o comportamento real do turno.
"""

from __future__ import annotations

from typing import Optional

# chave, rótulo, descrição (voltada ao leitor), capítulo que libera, tools que habilita.
# tools=() significa capacidade conceitual (sem tool nova) ou infra sempre-presente.
REGISTRO = [
    {"chave": "tutor", "rotulo": "Tutor do livro", "libera": 0, "tools": (),
     "descricao": "Explico conceitos e respondo perguntas usando o texto do livro."},
    {"chave": "busca_livro", "rotulo": "Busca no livro", "libera": 0, "tools": (),
     "descricao": "Encontro trechos relevantes no livro para embasar a resposta (com evidência)."},
    {"chave": "loop", "rotulo": "Loop de agente", "libera": 2, "tools": ("hora",),
     "descricao": "Deixo de só conversar: posso executar ferramentas em um loop até resolver."},
    {"chave": "contexto", "rotulo": "Contexto em camadas", "libera": 3, "tools": (),
     "descricao": "Monto o contexto do turno em camadas (regras + capítulo atual + histórico)."},
    {"chave": "compactacao", "rotulo": "Compactação", "libera": 4, "tools": (),
     "descricao": "Resumo conversas longas para caber na janela sem perder o fio."},
    {"chave": "ferramentas", "rotulo": "Ferramentas seguras", "libera": 5, "tools": ("calcular", "buscar_no_livro"),
     "descricao": "Uso ferramentas com schema (cálculo, busca no livro) — só as seguras/sandbox."},
    {"chave": "mcp", "rotulo": "MCP", "libera": 6, "tools": (),
     "descricao": "Conectar servidores MCP (desligado na versão pública por segurança)."},
    {"chave": "permissoes", "rotulo": "Permissões", "libera": 7, "tools": (),
     "descricao": "Só tools sandbox são expostas; nada de shell/arquivo real — a regra do cap. 07."},
    {"chave": "memoria", "rotulo": "Memória entre sessões", "libera": 8, "tools": (),
     "descricao": "Lembro da nossa conversa por uma identidade anônima do seu navegador."},
    {"chave": "planejamento", "rotulo": "Planejamento", "libera": 9, "tools": (),
     "descricao": "Posso planejar antes de agir (plan mode) quando a tarefa pede."},
    {"chave": "subagentes", "rotulo": "Subagentes", "libera": 10, "tools": (),
     "descricao": "Delegar subtarefas a sessões-filhas (em breve na versão pública)."},
    {"chave": "evals", "rotulo": "Verificação", "libera": 11, "tools": (),
     "descricao": "Checo minhas próprias respostas contra critérios (evals)."},
]

MODOS = ("avancado", "progressivo")


def _norm(chapter: Optional[int], mode: str) -> tuple[int, str]:
    ch = 0 if chapter is None else max(0, int(chapter))
    md = mode if mode in MODOS else "progressivo"
    return ch, md


def _ativa(cap: dict, chapter: int, mode: str) -> bool:
    return True if mode == "avancado" else cap["libera"] <= chapter


def capacidades(chapter: Optional[int], mode: str) -> list[dict]:
    """Lista para o widget: cada capacidade com rótulo, descrição e `ativa`."""
    ch, md = _norm(chapter, mode)
    return [{"chave": c["chave"], "rotulo": c["rotulo"], "descricao": c["descricao"],
             "libera_no_capitulo": c["libera"], "ativa": _ativa(c, ch, md)}
            for c in REGISTRO]


def loop_ativo(chapter: Optional[int], mode: str) -> bool:
    ch, md = _norm(chapter, mode)
    return any(c["chave"] == "loop" and _ativa(c, ch, md) for c in REGISTRO)


def tools_ativas(chapter: Optional[int], mode: str) -> set[str]:
    """Nomes de tools habilitadas. Só valem se o loop estiver ativo."""
    ch, md = _norm(chapter, mode)
    if not loop_ativo(ch, md):
        return set()
    ativas: set[str] = set()
    for c in REGISTRO:
        if _ativa(c, ch, md):
            ativas.update(c["tools"])
    return ativas
