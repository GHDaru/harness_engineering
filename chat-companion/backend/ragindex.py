"""Índice leve de busca no texto do livro — sem dependências, sem rede.

O tutor responde do livro (Princípio I: evidência). Este módulo carrega os
Markdown do projeto, quebra em blocos por cabeçalho/parágrafo e pontua por
sobreposição de termos. Não é um vetor de embeddings — é um BM25- zero
honesto, suficiente para ancorar respostas e citar de onde vieram. Quando uma
etapa futura pedir RAG real, troca-se aqui.

**Escopo (spec 077)**: até a edição 0.69 o índice cobria só `livro/` e o
comparativo — então perguntas sobre um sistema avaliado ("o que vocês acharam
do Grok Build?") ou sobre uma apuração do Radar caíam no vazio, porque a
avaliação individual e o diário não estavam indexados. Agora entram também as
**avaliações do benchmark** (a evidência por caminho de arquivo de cada
sistema) e o **Radar** (mesa de edição + diários), que é onde vive o que ainda
não virou capítulo. O livro segue sendo a fonte canônica; estes são registros
operacionais, e o campo `fonte` de cada bloco permite ao tutor dizer de onde
tirou — inclusive avisando que veio do Radar, não do livro.
"""

from __future__ import annotations

import json
import math
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
        # Benchmark: o comparativo (placar) + as avaliações individuais, que são
        # onde mora a evidência por caminho de arquivo de cada sistema.
        for extra in ("comparativo.md", "README.md"):
            p = repo_root / "benchmark" / extra
            if p.exists():
                fontes.append(p)
        fontes.extend(sorted((repo_root / "benchmark" / "avaliacoes").glob("*.md")))
        # Radar: a mesa priorizada e os diários — o que foi apurado e ainda não
        # virou capítulo. Sem isso o tutor não sabe responder sobre um achado
        # recente, mesmo ele estando publicado no site.
        for extra in ("RADAR.md", "AGENTE.md"):
            p = repo_root / "radar" / extra
            if p.exists():
                fontes.append(p)
        fontes.extend(sorted((repo_root / "radar" / "diario").glob("*.md"), reverse=True))
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
                crua = linha.strip()
                if linha.startswith("#"):
                    flush()
                    buffer = []
                    titulo_atual = linha.lstrip("#").strip()
                # Linha de tabela vira bloco próprio (spec 077): markdown não põe
                # linha em branco entre linhas de tabela, então a mesa inteira do
                # RADAR virava UM bloco — que casava com qualquer pergunta e, pior,
                # era truncado em 600 chars antes de chegar ao modelo, cortando
                # justamente a linha procurada. Cada item é autocontido; que seja
                # um bloco.
                elif crua.startswith("|") and crua.endswith("|"):
                    if set(crua) <= set("|-: "):   # separador da tabela
                        continue
                    flush()
                    buffer = [crua.strip("|")]
                    flush()
                    buffer = []
                elif crua:
                    buffer.append(crua)
                else:
                    flush()
                    buffer = []
            flush()

    def buscar(self, query: str, k: int = 4) -> list[dict]:
        """Pontuação (spec 077): **termos distintos** da pergunta encontrados no
        bloco, com penalidade suave de tamanho.

        Antes contava-se cada *ocorrência* de termo, sem normalizar por tamanho:
        um bloco longo que repetisse uma palavra comum vencia um bloco curto e
        exato. Cobrir mais termos da pergunta é o que indica relevância; o
        divisor logarítmico impede que o bloco gigante ganhe por volume.
        """
        termos = set(_norm(query))
        if not termos:
            return []
        pontuados = []
        for b in self.blocos:
            conjunto = b.get("set")
            if conjunto is None:
                conjunto = b["set"] = set(b["termos"])
            comuns = termos & conjunto
            if not comuns:
                continue
            score = len(comuns) / (1 + math.log(1 + len(b["termos"]) / 80))
            pontuados.append((score, b))
        pontuados.sort(key=lambda x: x[0], reverse=True)
        return [{"fonte": b["fonte"], "titulo": b["titulo"],
                 "trecho": b["texto"][:600]} for _, b in pontuados[:k]]
