"""StorePort — persistência de sessões e mensagens.

Duas implementações atrás da mesma porta (hexagonal por necessidade):
  - MemoryStore: dev e testes, sem banco, sem rede.
  - PostgresStore: produção, Neon Postgres (psycopg v3). Cria as tabelas na subida.

Identidade é anônima por padrão: `session_id` é um id gerado pelo navegador e
nenhum dado pessoal é exigido. A spec 080 acrescenta uma continuidade OPCIONAL —
o leitor que quiser atravessar dispositivos informa um e-mail e recebe um link
mágico; o e-mail apenas aponta para um `session_id` canônico, não vira login.
`delete_session` e `apagar_leitor` implementam o direito ao esquecimento (LGPD).

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
    # spec 080 — e-mail como chave de continuidade (link mágico)
    def criar_leitor(self, email: str, session_id: str) -> str: ...
    def leitor_por_email(self, email: str) -> Optional[str]: ...
    def leitor_por_sessao(self, session_id: str) -> Optional[str]: ...
    def apagar_leitor(self, session_id: str) -> bool: ...
    def salvar_link(self, token_hash: str, email: str, expira_ts: float,
                    origem_sid: str = "") -> None: ...
    def consumir_link(self, token_hash: str, agora_ts: float) -> Optional[dict]: ...
    def set_progresso(self, session_id: str, lang: str, slug: str, titulo: str) -> None: ...
    def get_progresso(self, session_id: str) -> list[dict]: ...
    def merge_session(self, origem: str, destino: str) -> None: ...
    # spec 093 — consentimento em camadas (ADR 0010) e progresso visível
    def registrar_consentimento(self, email: str, finalidade: str, versao: str,
                                aceito: bool) -> None: ...
    def consentimentos_de(self, email: str) -> dict: ...
    def emails_com_contato(self) -> list[dict]: ...
    def capitulos_lidos(self, session_id: str) -> list[str]: ...


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

    # ---- spec 080 ----
    def criar_leitor(self, email: str, session_id: str) -> str:
        self._leitores = getattr(self, "_leitores", {})   # email -> session_id
        if email in self._leitores:
            return self._leitores[email]
        self.ensure_session(session_id)
        self._leitores[email] = session_id
        return session_id

    def leitor_por_email(self, email: str) -> Optional[str]:
        return getattr(self, "_leitores", {}).get(email)

    def leitor_por_sessao(self, session_id: str) -> Optional[str]:
        for mail, sid in getattr(self, "_leitores", {}).items():
            if sid == session_id:
                return mail
        return None

    def apagar_leitor(self, session_id: str) -> bool:
        email = self.leitor_por_sessao(session_id)
        if email is None:
            return False
        self._leitores.pop(email, None)
        self._links = {h: v for h, v in getattr(self, "_links", {}).items()
                       if v["email"] != email}
        getattr(self, "_prog", {}).pop(session_id, None)
        # spec 093: append-only vale para a operação normal — dar e revogar são
        # linhas novas. O esquecimento é outro direito e ganha dele: guardar a
        # prova do consentimento de quem pediu para sumir seria guardar o e-mail
        # que ele mandou apagar. Sem dado tratado, não há consentimento a provar.
        self._cons = [c for c in getattr(self, "_cons", []) if c["email"] != email]
        self.delete_session(session_id)
        return True

    def salvar_link(self, token_hash: str, email: str, expira_ts: float,
                    origem_sid: str = "") -> None:
        self._links = getattr(self, "_links", {})
        self._links[token_hash] = {"email": email, "expira": expira_ts,
                                   "origem": origem_sid, "usado": False}

    def consumir_link(self, token_hash: str, agora_ts: float) -> Optional[dict]:
        link = getattr(self, "_links", {}).get(token_hash)
        if not link or link["usado"] or link["expira"] < agora_ts:
            return None
        link["usado"] = True
        return {"email": link["email"], "origem": link["origem"]}

    def set_progresso(self, session_id: str, lang: str, slug: str, titulo: str) -> None:
        self._prog = getattr(self, "_prog", {})
        self._prog.setdefault(session_id, {})[lang] = {
            "lang": lang, "slug": slug, "titulo": titulo, "ts": time.time()}

    def get_progresso(self, session_id: str) -> list[dict]:
        return list(getattr(self, "_prog", {}).get(session_id, {}).values())

    # ---- spec 093 ----
    # Append-only: consentir e revogar são AMBOS linhas novas. Um booleano diria
    # o estado e perderia a história — e é a história (quando, e a que texto) que
    # a LGPD pede como prova. O estado atual é a última linha por finalidade.
    def registrar_consentimento(self, email: str, finalidade: str, versao: str,
                                aceito: bool) -> None:
        self._cons = getattr(self, "_cons", [])
        self._cons.append({"email": email, "finalidade": finalidade, "versao": versao,
                           "aceito": aceito, "ts": time.time()})

    def consentimentos_de(self, email: str) -> dict:
        estado: dict = {}
        for c in getattr(self, "_cons", []):
            if c["email"] == email:
                estado[c["finalidade"]] = {"aceito": c["aceito"], "versao": c["versao"],
                                           "ts": c["ts"]}
        return estado

    def emails_com_contato(self) -> list[dict]:
        saida = []
        for email in {c["email"] for c in getattr(self, "_cons", [])}:
            c = self.consentimentos_de(email).get("contato")
            if c and c["aceito"]:
                saida.append({"email": email, "versao": c["versao"], "desde": c["ts"]})
        return sorted(saida, key=lambda x: x["email"])

    def capitulos_lidos(self, session_id: str) -> list[str]:
        """Slugs distintos visitados. Sem tabela nova: `nav_events` já registra
        slug × sessão e já segue o leitor na fusão da spec 080. Quem filtra por
        'é capítulo?' é o site, que conhece o sumário."""
        vistos = {e["slug"] for e in getattr(self, "_nav", [])
                  if e["session_id"] == session_id}
        return sorted(vistos)

    def merge_session(self, origem: str, destino: str) -> None:
        if origem == destino:
            return
        self.ensure_session(destino)
        msgs = self._msgs.pop(origem, [])
        if msgs:
            self._msgs[destino] = sorted(self._msgs.get(destino, []) + msgs,
                                         key=lambda m: m["ts"])
        goals = getattr(self, "_goals", {})
        if origem in goals:
            goals.setdefault(destino, goals[origem])
            goals.pop(origem, None)
        consents = getattr(self, "_consents", {})
        if origem in consents:
            consents.setdefault(destino, consents[origem])
            consents.pop(origem, None)
        for e in getattr(self, "_nav", []):
            if e["session_id"] == origem:
                e["session_id"] = destino
        prog = getattr(self, "_prog", {})
        for lang, item in prog.pop(origem, {}).items():
            atual = prog.get(destino, {}).get(lang)
            if not atual or atual["ts"] < item["ts"]:
                prog.setdefault(destino, {})[lang] = item


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
                -- spec 080: o e-mail é só um ponteiro para a sessão canônica.
                -- Nenhuma senha, nenhum hash de senha, nenhum dado além do e-mail.
                CREATE TABLE IF NOT EXISTS readers (
                    email TEXT PRIMARY KEY,
                    session_id TEXT UNIQUE NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                -- O token NUNCA é guardado em claro: só o SHA-256. Uso único.
                CREATE TABLE IF NOT EXISTS magic_links (
                    token_hash TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    origem_sid TEXT NOT NULL DEFAULT '',
                    expira_em TIMESTAMPTZ NOT NULL,
                    usado_em TIMESTAMPTZ,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                CREATE INDEX IF NOT EXISTS idx_links_email ON magic_links(email);
                -- spec 093 / ADR 0010: append-only. Consentir e revogar são ambos
                -- linhas; o estado é a última por (email, finalidade). Não há
                -- UPDATE aqui de propósito -- apagar a história seria apagar a prova.
                CREATE TABLE IF NOT EXISTS consentimentos (
                    id BIGSERIAL PRIMARY KEY,
                    email TEXT NOT NULL,
                    finalidade TEXT NOT NULL,
                    versao TEXT NOT NULL,
                    aceito BOOLEAN NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                CREATE INDEX IF NOT EXISTS idx_cons_email ON consentimentos(email, finalidade, id);
                CREATE TABLE IF NOT EXISTS progress (
                    session_id TEXT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
                    lang TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    titulo TEXT NOT NULL DEFAULT '',
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    PRIMARY KEY (session_id, lang)
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

    # ---- spec 080 ----
    def criar_leitor(self, email: str, session_id: str) -> str:
        """Idempotente: e-mail já cadastrado devolve a sessão canônica existente.
        Esse retorno é o que garante que assinar duas vezes não perde o histórico."""
        self.ensure_session(session_id)
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO readers(email, session_id) VALUES (%s, %s) "
                        "ON CONFLICT (email) DO NOTHING", (email, session_id))
            conn.commit()
            cur.execute("SELECT session_id FROM readers WHERE email = %s", (email,))
            existente = cur.fetchone()[0]
        if existente != session_id:  # já havia leitor: a sessão recém-criada é lixo
            self.delete_session(session_id)
        return existente

    def leitor_por_email(self, email: str) -> Optional[str]:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT session_id FROM readers WHERE email = %s", (email,))
            row = cur.fetchone()
        return row[0] if row else None

    def leitor_por_sessao(self, session_id: str) -> Optional[str]:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT email FROM readers WHERE session_id = %s", (session_id,))
            row = cur.fetchone()
        return row[0] if row else None

    def apagar_leitor(self, session_id: str) -> bool:
        email = self.leitor_por_sessao(session_id)
        if email is None:
            return False
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM magic_links WHERE email = %s", (email,))
            # spec 093: o esquecimento ganha do append-only — ver MemoryStore.
            cur.execute("DELETE FROM consentimentos WHERE email = %s", (email,))
            cur.execute("DELETE FROM readers WHERE email = %s", (email,))
            # sessions ON DELETE CASCADE leva messages, consents, nav, goals e progress
            cur.execute("DELETE FROM sessions WHERE session_id = %s", (session_id,))
            conn.commit()
        return True

    def salvar_link(self, token_hash: str, email: str, expira_ts: float,
                    origem_sid: str = "") -> None:
        from datetime import datetime, timezone
        expira = datetime.fromtimestamp(expira_ts, tz=timezone.utc)
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO magic_links(token_hash, email, origem_sid, expira_em) "
                        "VALUES (%s, %s, %s, %s) ON CONFLICT (token_hash) DO NOTHING",
                        (token_hash, email, origem_sid, expira))
            conn.commit()

    def consumir_link(self, token_hash: str, agora_ts: float) -> Optional[dict]:
        """Marca como usado e devolve o e-mail — numa única sentença condicional,
        para que dois cliques simultâneos no mesmo link não passem os dois."""
        from datetime import datetime, timezone
        agora = datetime.fromtimestamp(agora_ts, tz=timezone.utc)
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("UPDATE magic_links SET usado_em = %s "
                        "WHERE token_hash = %s AND usado_em IS NULL AND expira_em >= %s "
                        "RETURNING email, origem_sid", (agora, token_hash, agora))
            row = cur.fetchone()
            conn.commit()
        return {"email": row[0], "origem": row[1]} if row else None

    def set_progresso(self, session_id: str, lang: str, slug: str, titulo: str) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO progress(session_id, lang, slug, titulo) "
                        "VALUES (%s, %s, %s, %s) ON CONFLICT (session_id, lang) DO UPDATE "
                        "SET slug = EXCLUDED.slug, titulo = EXCLUDED.titulo, updated_at = now()",
                        (session_id, lang, slug, titulo))
            conn.commit()

    def get_progresso(self, session_id: str) -> list[dict]:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT lang, slug, titulo, updated_at FROM progress "
                        "WHERE session_id = %s", (session_id,))
            rows = cur.fetchall()
        return [{"lang": r[0], "slug": r[1], "titulo": r[2], "ts": r[3].timestamp()}
                for r in rows]

    # ---- spec 093 ----
    def registrar_consentimento(self, email: str, finalidade: str, versao: str,
                                aceito: bool) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO consentimentos(email, finalidade, versao, aceito) "
                        "VALUES (%s, %s, %s, %s)", (email, finalidade, versao, aceito))
            conn.commit()

    def consentimentos_de(self, email: str) -> dict:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT ON (finalidade) finalidade, aceito, versao, created_at "
                "FROM consentimentos WHERE email = %s "
                "ORDER BY finalidade, id DESC", (email,))
            rows = cur.fetchall()
        return {r[0]: {"aceito": r[1], "versao": r[2], "ts": r[3].timestamp()} for r in rows}

    def emails_com_contato(self) -> list[dict]:
        """Só quem tem contato ATIVO — a última linha da finalidade diz sim."""
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT email, versao, created_at FROM ("
                "  SELECT DISTINCT ON (email) email, aceito, versao, created_at"
                "  FROM consentimentos WHERE finalidade = 'contato'"
                "  ORDER BY email, id DESC"
                ") u WHERE aceito ORDER BY email")
            rows = cur.fetchall()
        return [{"email": r[0], "versao": r[1], "desde": r[2].timestamp()} for r in rows]

    def capitulos_lidos(self, session_id: str) -> list[str]:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT DISTINCT slug FROM nav_events WHERE session_id = %s "
                        "ORDER BY slug", (session_id,))
            return [r[0] for r in cur.fetchall()]

    def merge_session(self, origem: str, destino: str) -> None:
        """Funde a sessão anônima na canônica. Quem assina depois de já ter
        conversado não perde a conversa — foi o que motivou a fusão existir."""
        if origem == destino:
            return
        self.ensure_session(destino)
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute("UPDATE messages SET session_id = %s WHERE session_id = %s",
                        (destino, origem))
            cur.execute("UPDATE nav_events SET session_id = %s WHERE session_id = %s",
                        (destino, origem))
            # goals/consents/progress têm PK por sessão: só migram se o destino não tiver
            cur.execute("INSERT INTO goals(session_id, texto) "
                        "SELECT %s, texto FROM goals WHERE session_id = %s "
                        "ON CONFLICT (session_id) DO NOTHING", (destino, origem))
            cur.execute("INSERT INTO consents(session_id, versao) "
                        "SELECT %s, versao FROM consents WHERE session_id = %s "
                        "ON CONFLICT (session_id) DO NOTHING", (destino, origem))
            cur.execute("INSERT INTO progress(session_id, lang, slug, titulo, updated_at) "
                        "SELECT %s, lang, slug, titulo, updated_at FROM progress "
                        "WHERE session_id = %s "
                        "ON CONFLICT (session_id, lang) DO UPDATE "
                        "SET slug = EXCLUDED.slug, titulo = EXCLUDED.titulo, "
                        "    updated_at = EXCLUDED.updated_at "
                        "WHERE progress.updated_at < EXCLUDED.updated_at", (destino, origem))
            cur.execute("DELETE FROM sessions WHERE session_id = %s", (origem,))
            conn.commit()


def make_store(database_url: str) -> StorePort:
    return PostgresStore(database_url) if database_url else MemoryStore()
