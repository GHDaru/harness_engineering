"""Índice leve de busca no texto do livro — sem dependências, sem rede.

O tutor responde do livro (Princípio I: evidência). Este módulo carrega os
Markdown de `livro/` (+ o comparativo do benchmark), quebra em blocos por
cabeçalho/parágrafo e pontua por sobreposição de termos. Não é um vetor de
embeddings — é um BM25- zero honesto, suficiente para ancorar respostas e
citar de onde vieram. Quando uma etapa futura pedir RAG real, troca-se aqui.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Optional

_STOP = set("de da do das dos a o e que em para com sem por no na nos nas um uma os as "
            "se ao à é são como mais ou seu sua the of to and in is a an".split())


def _norm(txt: str) -> list[str]:
    txt = unicodedata.normalize("NFD", txt.lower())
    txt = "".join(c for c in txt if unicodedata.category(c) != "Mn")
    return [t for t in re.findall(r"[a-z0-9]+", txt) if t not in _STOP and len(t) > 2]


class BookIndex:
    def __init__(self, repo_root: Path, corpus_path: Optional[Path] = None) -> None:
        """Carrega do `corpus.json` empacotado se existir (caso do container
        isolado); senão varre `livro/` ao vivo (dev / repo completo)."""
        self.blocos: list[dict] = []
        if corpus_path and Path(corpus_path).exists():
            self._carregar_corpus(Path(corpus_path))
        elif (Path(repo_root) / "livro").is_dir():
            self._carregar(repo_root)

    def _carregar_corpus(self, path: Path) -> None:
        try:
            dados = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        for b in dados:
            self.blocos.append({"fonte": b["fonte"], "titulo": b["titulo"], "texto": b["texto"],
                                "termos": _norm(b["titulo"] + " " + b["texto"])})

    def exportar(self, path: Path) -> int:
        """Grava o corpus (sem os termos — recomputados no load) para empacotar."""
        dados = [{"fonte": b["fonte"], "titulo": b["titulo"], "texto": b["texto"]}
                 for b in self.blocos]
        Path(path).write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        return len(dados)

    def _carregar(self, repo_root: Path) -> None:
        fontes = sorted(f for f in (repo_root / "livro").rglob("*.md")
                        if "en" not in f.relative_to(repo_root / "livro").parts[:1])
        comp = repo_root / "benchmark" / "comparativo.md"
        if comp.exists():
            fontes.append(comp)
        for f in fontes:
            try:
                texto = f.read_text(encoding="utf-8")
            except OSError:
                continue
            rel = f.relative_to(repo_root).as_posix()
            titulo_atual = f.stem
            buffer: list[str] = []

            def flush():
                if buffer:
                    corpo = " ".join(buffer).strip()
                    if len(corpo) > 40:
                        self.blocos.append(
                            {"fonte": rel, "titulo": titulo_atual, "texto": corpo,
                             "termos": _norm(titulo_atual + " " + corpo)})

            for linha in texto.splitlines():
                if linha.startswith("#"):
                    flush()
                    buffer = []
                    titulo_atual = linha.lstrip("#").strip()
                elif linha.strip():
                    buffer.append(linha.strip())
                else:
                    flush()
                    buffer = []
            flush()

    def buscar(self, query: str, k: int = 4) -> list[dict]:
        termos = set(_norm(query))
        if not termos:
            return []
        pontuados = []
        for b in self.blocos:
            score = sum(1 for t in b["termos"] if t in termos)
            if score:
                pontuados.append((score, b))
        pontuados.sort(key=lambda x: x[0], reverse=True)
        return [{"fonte": b["fonte"], "titulo": b["titulo"],
                 "trecho": b["texto"][:600]} for _, b in pontuados[:k]]
