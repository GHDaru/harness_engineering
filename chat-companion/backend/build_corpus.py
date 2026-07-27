"""Gera o corpus.json do livro para empacotar com o backend.

Necessário porque o deploy (Railway com Root Directory isolado) copia só a
pasta do backend — o texto de `livro/` não vai junto. Este script varre o
repositório completo (em dev/CI) e grava um `corpus.json` self-contained que
o backend carrega no container.

Rodar (com o repositório completo presente):
    cd chat-companion/backend && python build_corpus.py

Regere sempre que o livro mudar (idealmente no CI, antes do deploy).
"""

from pathlib import Path

import config
from ragindex import BookIndex

# corpus_path=None força a varredura ao vivo de livro/ (não lê um corpus antigo).
idx = BookIndex(config.REPO_ROOT, corpus_path=None)
destino = Path(__file__).resolve().parent / "corpus.json"
n = idx.exportar(destino)
print(f"corpus.json gerado: {n} blocos de {config.REPO_ROOT}/livro -> {destino}")
