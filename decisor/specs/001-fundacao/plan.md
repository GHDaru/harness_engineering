# Plan 001 — Fundação

- **Spec**: [spec.md](spec.md) · **Raia**: Plena · **Data**: 2026-07-30

## Constitution Check (constituição v1.0.0)

| Princípio | Conformidade |
|---|---|
| I. Evidência acima de retórica | ✅ Bibliografia com status ✓/? por fonte; worked examples dos caps. 00–01 e do SAW são testes (`test_matriz.py`, `test_saw.py`) |
| II. Método ↔ implementação ↔ fonte | ✅ SAW no produto cita Hwang & Yoon/Fishburn no docstring e reproduz o caso âncora em teste; caps. sem método (00–01) não expõem método |
| III. Método pedagógico | ✅ Esqueleto v3 nos dois capítulos; caso âncora definido no guia editorial e usado em livro, etapas e produto |
| IV. Livro vivo | ✅ Selo de captura nos capítulos; HISTORICO com edição 0.1, snapshot e registro do modelo de IA |
| V. Segurança | ✅ `DATABASE_URL` só por ambiente; `.env` gitignored; `.env.example` sem valores reais |
| VI. Neutralidade e acessibilidade | ✅ Fallback SQLite (custo zero); "nenhum método é o melhor" nos caps. e no README; limitações citadas com fonte |
| VII. Spec-driven e gates | ✅ Esta rodada é a spec 001 em branch própria; ADRs 0001–0004; DoD verificável; gate humano pendente registrado |

**Sem violações.** (Único desvio consciente: o produto v0 expõe SAW antes do cap. 04
existir — mitigado pela regra do Princípio II aplicada ao código, teste e docstring;
o cap. 04 herdará o worked example já testado.)

## Como

1. Herdar o modelo editorial do harness_engineering (constituição, esqueleto v3,
   HISTORICO, spec-kit copiado para `.specify/`) e a operação do Maestro (raias, DoD,
   ADR imutável, CHANGELOG com forcing function, CLAUDE.md=AGENTS.md).
2. Pesquisar fontes MCDA (agente de pesquisa com verificação de URL) → bibliografia
   com curadoria datada → sequência didática dirigida pela dor (ADR 0003).
3. Implementar de dentro para fora: motor puro → etapa didática → produto (casca
   FastAPI + repositório de banco encapsulado em `bd.py`).
4. Publicação MkDocs Material com build estrito como portão (ADR 0004); workflows
   inertes até a extração (ADR 0001).

## Verificação (DoD)

| Check | Comando | Esperado |
|---|---|---|
| Etapa 01 | `cd decisor-zero/etapas/01-matriz && python -m pytest tests/ -q` | `11 passed, 1 skipped` |
| Produto | `cd app/backend && python -m pytest tests/ -q` | `8 passed` |
| Livro | `mkdocs build --strict` | exit 0, sem warnings |
| Segredos | `grep -rE "postgres(ql)?://[^ ]*:[^ ]*@" --include="*.py" --include="*.md" --include="*.example" .` | somente o placeholder do `.env.example` |
