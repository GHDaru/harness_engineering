"""Testes rodam contra SQLite temporário — nunca contra o banco real.

DATABASE_URL é definida ANTES de importar decisor.bd (o engine nasce no import).
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

_tmp = tempfile.mkdtemp(prefix="decisor-teste-")
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp}/teste.db"
