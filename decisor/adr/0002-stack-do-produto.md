# ADR 0002 — Stack do produto: FastAPI + Neon/Postgres + frontend estático v0

- **Status**: Aceito
- **Data**: 2026-07-30
- **Relacionado**: constituição ("Restrições da construção"); spec 001

## Contexto

O pedido de origem fixa backend FastAPI e banco Neon (Postgres serverless), e deixa o
frontend em aberto. O projeto tem dois consumidores de stack com necessidades opostas:
as **etapas didáticas** (carga cognitiva mínima, zero build, custo zero) e o **produto**
(evoluirá para comparação multi-método, contas de usuário, deploy).

## Decisão

1. **Backend**: Python 3.11+ / FastAPI / SQLModel; motor MCDA em módulos **puros**
   (`decisor/motor/`) sem I/O — a API é casca (hexagonal por refatoração).
2. **Banco**: Postgres no **Neon** via `DATABASE_URL` (driver `psycopg`), com
   **fallback SQLite** quando a variável não existe — a trilha roda a custo zero
   (Princípio VI) e os testes nunca tocam banco real. Acesso encapsulado em
   `decisor/bd.py` (Restrição 4, anti-apodrecimento).
3. **Frontend das etapas** (`decisor-zero/`): HTML+JS sem build, para sempre.
4. **Frontend do produto**: **estático v0** (uma página servida pelo FastAPI). Quando a
   UI exigir estado complexo (comparação multi-método, cap. 11+), migrar para
   **React + Vite + TypeScript** em `app/frontend/` — gatilho registrado no placar de
   expiração do `livro/HISTORICO.md`.

## Alternativas avaliadas

- **React desde já** — rejeitado (YAGNI, Maestro Princípio VII): v0 tem um formulário e
  uma tabela; um build de frontend agora só adiciona atrito.
- **HTMX/Jinja** — rejeitado: criaria uma terceira tecnologia entre o v0 e o destino
  React, sem eliminar a migração.
- **ORM completo (SQLAlchemy puro + Alembic) no v0** — adiado para o cap. 13 (spec de
  raia infra, com gates de reversibilidade para migrações).

## Consequências

- O produto expõe métodos MCDA um a um, apenas quando o capítulo correspondente existe
  com teste (Princípio II) — o SAW entra no v0 como adiantamento do cap. 04, já testado.
- Migração de frontend e migrações de banco serão specs próprias (raia plena/infra).

## Fontes

- Neon — connection strings e sslmode: <https://neon.tech/docs/connect/connect-from-any-app>
- scikit-criteria como referência de API de motor: <https://scikit-criteria.quatrope.org/>
