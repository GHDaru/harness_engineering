"""StorePort — persistência de sessões e mensagens.

Duas implementações atrás da mesma porta (hexagonal por necessidade):
  - MemoryStore: dev e testes, sem banco, sem rede.
  - PostgresStore: produção, Neon Postgres (psycopg v3). Cria as tabelas na subida.

Identidade é anônima: `session_id` é um id gerado pelo navegador. Nenhum dado
pessoal é exigido. `delete_session` implementa o direito ao esquecimento (LGPD).

Nota didática: esta é a dor que a etapa 04 (cap. 08, Memória e Estado) formaliza.
O companion, por ser produção, já precisa dela — as etapas ensinam depois.
"""

from __future__ import annotations

import time
from typing import Optional, Protocol

Message = dict


class StorePort(Protocol):
    def ensure_session(self, session_id: str) -> None: ...
    def append(self, session_id: str, role: str, content: str) -> None: ...
    def history(self, session_id: str, limit: int = 100) -> list[Message]: ...
    def count_since(self, session_id: str, since_ts: float) -> int: ...
    def delete_session(self, session_id: str) -> None: ...
    def add_suggestion(self, session_id: str, texto: str, pagina: str) -> None: ...
    def suggestions(self, limit: int = 200) -> list[dict]: ...
    # spec 054 — consentimento, telemetria e objetivo do leitor
    def record_consent(self, session_id: str, versao: str) -> None: ...
    def has_consent(self, session_id: str) -> bool: ...
    def add_nav(self, session_id: str, slug: str) -> None: ...
    def nav_stats(self, limit: int = 500) -> dict: ...
    def set_goal(self, session_id: str, texto: str) -> None: ...
    def get_goal(self, session_id: str) -> Optional[str]: ...


# ----------------------------------------------------------- memória

class MemoryStore:
    def __init__(self) -> None:
        self._msgs: dict[str, list[dict]] = {}
        self._sug: list[dict] = []

    def ensure_session(self, session_id: str) -> None:
        self._msgs.setdefault(session_id, [])

    def append(self, session_id: str, role: str, content: str) -> None:
        self._msgs.setdefault(session_id, []).append(
            {"role": role, "content": content, "ts": time.time()})

    def history(self, session_id: str, limit: int = 100) -> list[Message]:
        return [{"role": m["role"], "content": m["content"]}
                for m in self._msgs.get(session_id, [])[-limit:]]

    def count_since(self, session_id: str, since_ts: float) -> int:
        return sum(1 for m in self._msgs.get(session_id, [])
                   if m["role"] == "user" and m["ts"] >= since_ts)

    def delete_session(self, session_id: str) -> None:
        self._msgs.pop(session_id, None)

    def add_suggestion(self, session_id: str, texto: str, pagina: str) -> None:
        self._sug.append({"session_id": session_id, "texto": texto, "pagina": pagina, "ts": time.time()})

    def suggestions(self, limit: int = 200) -> list[dict]:
        return list(self._sug[-limit:])

    # ---- spec 054 ----
    def record_consent(self, session_id: str, versao: str) -> None:
        self._consents = getattr(self, "_consents", {})
        self._consents[session_id] = {"versao": versao, "ts": time.time()}

    def has_consent(self, session_id: str) -> bool:
        return session_id in getattr(self, "_consents", {})

    def add_nav(self, session_id: str, slug: str) -> None:
        self._nav = getattr(self, "_nav", [])
        self._nav.append({"session_id": session_id, "slug": slug, "ts": time.time()})

    def nav_stats(self, limit: int = 500) -> dict:
        nav = getattr(self, "_nav", [])[-limit:]
        por_slug: dict[str, int] = {}
        for e in nav:
            por_slug[e["slug"]] = por_slug.get(e["slug"], 0) + 1
        return {"total": len(nav), "por_pagina": por_slug,
                "ultimos": [{"slug": e["slug"], "ts": e["ts"]} for e in nav[-20:]]}

    def set_goal(self, session_id: str, texto: str) -> None:
        self._goals = getattr(self, "_goals", {})
        self._goals[session_id] = texto

    def get_goal(self, session_id: str) -> Optional[str]:
        return getattr(self, "_goals", {}).get(session_id)


# ----------------------------------------------------------- postgres (neon)

class PostgresStore:
    """Persistência real. Import de psycopg é tardio para o app subir mesmo
    sem a lib instalada (o MemoryStore cobre dev/testes)."""

    def __init__(self, database_url: str) -> None:
        import psycopg  # noqa: F401  (falha cedo e claro se ausente em produção)

        self._psycopg = psycopg
        # Neon exige SSL; normaliza a URL se vier sem sslmode.
        if "sslmode=" not in database_url:
            database_url += ("&" if "?" in database_url else "?") + "sslmode=require"
        self._dsn = database_url
        self._init_schema()

    def _conn(self):
        return self._psycopg.connect(self._dsn)

    def _init_schema(self) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                CREATE TABLE IF NOT EXISTS messages (
                    id BIGSERIAL PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id, id);
                CREATE TABLE IF NOT EXISTS suggestions (
                    id BIGSERIAL PRIMARY KEY,
                    session_id TEXT,
                    texto TEXT NOT NULL,
                    pagina TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                CREATE TABLE IF NOT EXISTS consents (
                    session_id TEXT PRIMARY KEY REFERENCES sessions(session_id) ON DELETE CASCADE,
                    versao TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                CREATE TABLE IF NOT EXISTS nav_events (
                    id BIGSERIAL PRIMARY KEY,
                    session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                    slug TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                CREATE INDEX IF NOT EXISTS idx_nav_slug ON nav_events(slug);
                CREATE TABLE IF NOT EXISTS goals (
                    session_id TEXT PRIMARY KEY REFERENCES sessions(session_id) ON DELETE CASCADE,
                    texto TEXT NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
            """)
            conn.commit()

    def ensure_session(self, session_id: str) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO sessions(session_id) VALUES (%s) ON CONFLICT DO NOTHING",
                (session_id,))
            conn.commit()

    def append(self, session_id: str, role: str, content: str) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO messages(session_id, role, content) VALUES (%s, %s, %s)",
                (session_id, role, content))
            conn.commit()

    def history(self, session_id: str, limit: int = 100) -> list[Message]:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT role, content FROM messages WHERE session_id = %s "
                "ORDER BY id DESC LIMIT %s", (session_id, limit))
            rows = cur.fetchall()
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

    def count_since(self, session_id: str, since_ts: float) -> int:
        from datetime import datetime, timezone
        since = datetime.fromtimestamp(since_ts, tz=timezone.utc)
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT count(*) FROM messages WHERE session_id = %s AND role = 'user' "
                "AND created_at >= %s", (session_id, since))
            return int(cur.fetchone()[0])

    def delete_session(self, session_id: str) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM sessions WHERE session_id = %s", (session_id,))
            conn.commit()

    def add_suggestion(self, session_id: str, texto: str, pagina: str) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO suggestions(session_id, texto, pagina) VALUES (%s, %s, %s)",
                        (session_id, texto, pagina))
            conn.commit()

    def suggestions(self, limit: int = 200) -> list[dict]:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT session_id, texto, pagina, created_at FROM suggestions ORDER BY id DESC LIMIT %s", (limit,))
            rows = cur.fetchall()
        return [{"session_id": r[0], "texto": r[1], "pagina": r[2], "created_at": str(r[3])} for r in rows]

    # ---- spec 054 ----
    def record_consent(self, session_id: str, versao: str) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO consents(session_id, versao) VALUES (%s, %s) "
                        "ON CONFLICT (session_id) DO UPDATE SET versao = EXCLUDED.versao, created_at = now()",
                        (session_id, versao))
            conn.commit()

    def has_consent(self, session_id: str) -> bool:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1 FROM consents WHERE session_id = %s", (session_id,))
            return cur.fetchone() is not None

    def add_nav(self, session_id: str, slug: str) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO nav_events(session_id, slug) VALUES (%s, %s)", (session_id, slug))
            conn.commit()

    def nav_stats(self, limit: int = 500) -> dict:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT slug, count(*) FROM nav_events GROUP BY slug ORDER BY count(*) DESC LIMIT 100")
            por = {r[0]: int(r[1]) for r in cur.fetchall()}
            cur.execute("SELECT slug, created_at FROM nav_events ORDER BY id DESC LIMIT 20")
            ult = [{"slug": r[0], "ts": str(r[1])} for r in cur.fetchall()]
            cur.execute("SELECT count(*) FROM nav_events")
            total = int(cur.fetchone()[0])
        return {"total": total, "por_pagina": por, "ultimos": ult}

    def set_goal(self, session_id: str, texto: str) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO goals(session_id, texto) VALUES (%s, %s) "
                        "ON CONFLICT (session_id) DO UPDATE SET texto = EXCLUDED.texto, updated_at = now()",
                        (session_id, texto))
            conn.commit()

    def get_goal(self, session_id: str) -> Optional[str]:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT texto FROM goals WHERE session_id = %s", (session_id,))
            row = cur.fetchone()
        return row[0] if row else None


def make_store(database_url: str) -> StorePort:
    return PostgresStore(database_url) if database_url else MemoryStore()
