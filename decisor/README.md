# Decisor — decisão multicritério: o livro vivo e a aplicação

Aprenda a decidir com métodos quantitativos (MCDA — *Multi-Criteria Decision Analysis*)
**lendo, calculando à mão e implementando** — e use o que aprendeu numa aplicação real.

## As três frentes

| Frente | O que é | Comece por |
|---|---|---|
| **O livro** (`livro/`) | 14 capítulos com fontes seminais verificadas, um caso âncora único e fórmulas que fecham | [`livro/SUMARIO.md`](livro/SUMARIO.md) |
| **decisor-zero** (`decisor-zero/`) | Uma etapa executável por capítulo; o diff entre etapas é a lição | [`decisor-zero/README.md`](decisor-zero/README.md) |
| **Decisor** (`app/`) | O produto: FastAPI + Postgres (Neon) + web | [`app/README.md`](app/README.md) |

## Rodar em 60 segundos (custo zero)

```bash
pip install -r decisor-zero/requirements.txt
cd decisor-zero/etapas/01-matriz
uvicorn app:app --reload        # http://localhost:8000
pytest                          # os números do capítulo 01, verificados
```

O livro é publicado com MkDocs Material (`mkdocs build --strict`; deploy no GitHub
Pages via `.github/workflows/pages.yml` — ver ADR 0001 sobre a ativação).

## Governança (leia antes de contribuir)

- **[Constituição](.specify/memory/constitution.md)** — os 7 princípios; prevalece sobre tudo.
- **[CLAUDE.md](CLAUDE.md) / [AGENTS.md](AGENTS.md)** — orientações para agentes de IA.
- **[ADRs](adr/README.md)** — decisões com alternativas e consequências.
- **Ciclos** em `specs/NNN-nome/` (spec → plan → tasks → qa-report), metodologia
  herdada do [Maestro](https://github.com/ghdaru/maestro); modelo editorial herdado do
  [Engenharia de Harness](https://github.com/ghdaru/harness_engineering).

Nenhum método é "o melhor"; nenhuma fórmula sem fonte; nenhum método sem teste que
reproduza um exemplo da literatura. Se um capítulo discordar do código, o código (e o
teste) ganham — e a prosa é corrigida.
