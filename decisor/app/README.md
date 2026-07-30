# Decisor — o produto

Aplicação web de apoio à decisão multicritério. Backend FastAPI, banco Postgres
([Neon](https://neon.tech)) com fallback SQLite, frontend estático v0 (ADR 0002).

## Rodar localmente (sem banco — custo zero)

```bash
cd app/backend
pip install -r requirements.txt
uvicorn decisor.main:app --reload    # http://localhost:8000 (usa decisor.db local)
pytest                               # 8 testes: motor SAW + API ponta a ponta
```

## Conectar ao Neon (produção)

1. Crie um projeto no [Neon](https://neon.tech) (free tier) e copie a connection string.
2. `cp .env.example .env` e preencha `DATABASE_URL` (o `.env` é gitignored —
   **nunca** commite a string; Princípio V da constituição).
3. Exporte antes de subir: `export $(grep -v '^#' .env | xargs)` (ou use seu gerenciador
   de processos). URLs `postgres://…` do Neon são aceitas e adaptadas para `psycopg`.

## API v0

| Rota | O quê |
|---|---|
| `POST /api/decisoes` | Salva um problema multicritério validado (matriz, direções, pesos) |
| `GET /api/decisoes` · `GET /api/decisoes/{id}` | Lista/recupera decisões |
| `GET /api/metodos` | Catálogo de métodos disponíveis (v0: SAW) |
| `POST /api/decisoes/{id}/ranking?metodo=saw` | Ranking pelo método escolhido |

O motor de cálculo (`decisor/motor/`) é puro — sem I/O — e cada método cita sua fonte
no docstring; novos métodos entram apenas quando o capítulo correspondente do livro
existe com teste (Princípio II). Próximos: os das Partes II–III do
[sumário](../livro/SUMARIO.md).
