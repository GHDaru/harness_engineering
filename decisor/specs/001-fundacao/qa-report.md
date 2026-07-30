# QA Report 001 — Fundação

- **Data**: 2026-07-30 · **Raia**: Plena · **Veredito**: ✅ CONFORME (pendente só o gate humano)

## Checks da DoD ("prove, não declare")

| Check | Comando | Esperado | Resultado |
|---|---|---|---|
| Etapa 01 | `cd decisor-zero/etapas/01-matriz && python -m pytest tests/ -q` | 11 passed, 1 skipped | ✅ `11 passed, 1 skipped, 1 warning in 0.34s` |
| Etapa 00 (smoke) | TestClient: `/api/caso-ancora` + `/` | dados do caso âncora servidos | ✅ `etapa 00 smoke ok` |
| Produto | `cd app/backend && python -m pytest tests/ -q` | 8 passed | ✅ `8 passed, 1 warning in 0.70s` |
| Livro | `mkdocs build --strict` | exit 0 sem warnings | ✅ `Documentation built in 0.41 seconds`, exit 0 |
| Segredos | `grep -rE "postgres(ql)?://…:…@"` no seed | só o placeholder comentado do `.env.example` | ✅ 1 ocorrência, é o placeholder |

Nota: o `1 skipped` é deliberado — exercício do leitor do cap. 01 (part-task practice),
com gabarito no docstring do teste.

## Cobertura dos requisitos

| FR | Evidência |
|---|---|
| FR1 | `CLAUDE.md` = `AGENTS.md` (cópia byte a byte); `.specify/memory/constitution.md` v1.0.0 |
| FR2 | `livro/SUMARIO.md` (14 caps., 4 partes, mapa capítulo↔etapa); ADR 0003 |
| FR3 | `livro/bibliografia.md` — 30+ fontes, status ✓/?, notas de curadoria datadas |
| FR4 | `livro/capitulos/00-*.md` e `01-*.md` no esqueleto v3, selo de captura 2026-07 |
| FR5 | `decisor-zero/etapas/00-esqueleto/`, `01-matriz/` — pytest acima |
| FR6 | `app/backend/decisor/` (motor puro, tipos, bd com fallback, rotas) — pytest acima |
| FR7 | `mkdocs.yml` + `livro/index.md`; `.github/workflows/{pages,ci}.yml` (inertes até a extração — ADR 0001) |
| FR8 | `adr/0001..0004`, `livro/HISTORICO.md` (edição 0.1 + IA registrada), `CHANGELOG.md` |

## Estado da fase

Fundação completa e verificada. Próxima rodada natural: spec 002 (cap. 02 —
estruturação e dominância + etapa `02-dominancia`).

## Pendência de gate

A promoção depende de aprovação humana indelegável (Maestro §8): revisão do Steward
desta rodada e decisão sobre a extração do seed para repositório próprio (ADR 0001).
