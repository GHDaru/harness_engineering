"""Configuração do chat-companion, lida só de variáveis de ambiente.

Regra do cap. 07 aplicada ao próprio projeto: nenhuma credencial no código.
A chave do projeto (NVIDIA NIM) e a DATABASE_URL (Neon) vivem só no ambiente.
Defaults são seguros: sem chave -> adapter echo; sem banco -> store em memória.
"""

import os
from pathlib import Path


def _load_dotenv() -> None:
    """Carrega um .env vizinho para os.environ (sem dependência externa).
    Procura a partir deste arquivo subindo os diretórios. `.env` é gitignored."""
    for parent in (Path(__file__).parent, *Path(__file__).parents):
        env = parent / ".env"
        if env.exists():
            for line in env.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ.setdefault(key.strip(), val.strip())
            return


_load_dotenv()


def _bool(name: str, default: bool) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def _int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


# --- LLM ---
LLM_ADAPTER = os.environ.get("LLM_ADAPTER", "echo")            # "echo" | "openai"
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://integrate.api.nvidia.com/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")          # chave do PROJETO (nunca commitada)
LLM_MODEL = os.environ.get("LLM_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")

# --- Persistência (Neon) ---
DATABASE_URL = os.environ.get("DATABASE_URL", "")             # vazio -> MemoryStore

# --- Rede / origens ---
# Origens que podem chamar o backend. Default cobre o site publicado + dev local.
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "ALLOWED_ORIGINS",
        "https://ghdaru.github.io,http://localhost:8000,http://127.0.0.1:8000,http://localhost:5173",
    ).split(",")
    if o.strip()
]

# --- Limites ---
RATE_LIMIT_MSGS = _int("RATE_LIMIT_MSGS", 20)                  # msgs por janela, por sessão/IP
RATE_LIMIT_WINDOW_S = _int("RATE_LIMIT_WINDOW_S", 300)         # janela em segundos
ALLOW_BYOK = _bool("ALLOW_BYOK", True)                         # leitor pode usar a própria chave

# --- Livro (fonte do tutor) ---
# Raiz do repositório, para o índice de busca no texto do livro. Robusto a
# contextos isolados (ex.: Railway com Root Directory = chat-companion/backend,
# onde só esta pasta é copiada): procura subindo até achar `livro/`; se não
# achar (deploy isolado), o `corpus.json` empacotado cobre a busca no livro.
def _find_repo_root() -> Path:
    override = os.environ.get("REPO_ROOT")
    if override:
        return Path(override)
    aqui = Path(__file__).resolve()
    for parent in aqui.parents:
        if (parent / "livro").is_dir():
            return parent
    return aqui.parent  # fallback seguro (sem IndexError); corpus.json cobre o livro


REPO_ROOT = _find_repo_root()
# Corpus do livro empacotado (gerado por build_corpus.py) — usado quando o
# repositório completo não está no container.
CORPUS_PATH = Path(__file__).resolve().parent / "corpus.json"

# --- Sugestões dos leitores (E05) ---
SUGGESTION_EMAIL_TO = os.environ.get("SUGGESTION_EMAIL_TO", "ghdaru@gmail.com")
SMTP_HOST = os.environ.get("SMTP_HOST", "")           # vazio -> não envia email (só persiste)
SMTP_PORT = _int("SMTP_PORT", 587)
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")       # vazio -> /suggestions desabilitado
