# Orientações do projeto — Decisor (livro vivo + app de decisão multicritério)

## Regra central

- **Antes de qualquer trabalho, leia [`.specify/memory/constitution.md`](.specify/memory/constitution.md)**
  (a lei do projeto: 7 princípios + restrições da construção). Prevalece sobre qualquer
  outra prática; em conflito com um pedido pontual, explicite o conflito antes de agir.
- O projeto tem três corpos que evoluem juntos: **livro** (`livro/`), **construção
  prática** (`decisor-zero/`, uma etapa por capítulo) e **produto** (`app/`, FastAPI +
  Neon + frontend). Capítulo sem etapa testada não é publicado (Princípios I–II).

## Fluxo de desenvolvimento (spec-driven, herdado do Maestro)

- **Toda melhoria** — capítulo novo, etapa, feature do app, rodada de revisão — segue
  `spec → plan (Constitution Check) → tasks → implement → DoD → revisão em contexto
  fresco → gate humano → merge`, registrada em `specs/NNN-nome/` na sua própria branch.
- **Raias**: leve (typo/link/bug com teste que o reproduz — o PR é o artefato) ·
  plena (capítulo/etapa/feature — spec completa) · infra (banco/deploy/migração —
  sempre plena + backup, dry-run e rollback). Na dúvida, é plena.
- Templates e scripts do spec-kit em `.specify/`; use
  `bash .specify/scripts/bash/create-new-feature.sh "<nome>"` para abrir uma feature.
- **Prove, não declare**: nenhum "pronto" sem o output de `pytest` (decisor-zero e app)
  e do build do livro. Bug corrigido exige o teste que o reproduzia falhando antes.

## Regras que os agentes mais violam (não viole)

- **Fórmula sem fonte não entra** (`livro/bibliografia.md`, status ✓); **método sem
  exemplo numérico reproduzido em teste não entra** (o worked example é fixture).
- **Nenhum segredo em arquivo/commit** — connection string do Neon só via `DATABASE_URL`
  em `.env` gitignored; `.env.example` sempre sem valores reais.
- Capítulos seguem o **esqueleto v3** de `livro/GUIA-EDITORIAL.md` e declaram data de
  captura no cabeçalho; toda edição atualiza `livro/HISTORICO.md` (incl. modelo de IA).
- Nenhum método é apresentado como "o melhor"; limitações com fonte (Princípio VI).
- Decisão relevante → ADR em `adr/` (imutável); mudança de escopo → volta à spec.

## Onde está o quê

- Constituição → `.specify/memory/constitution.md`
- Como escrever capítulos (esqueleto v3, caso âncora) → `livro/GUIA-EDITORIAL.md`
- Sequência didática (sumário) → `livro/SUMARIO.md` · Fontes → `livro/bibliografia.md`
- Edições, datação e modelo de IA → `livro/HISTORICO.md`
- Etapas executáveis → `decisor-zero/etapas/NN-tema/` (uma por capítulo, autocontida)
- Produto → `app/backend/` (FastAPI + motor MCDA + Neon) · frontend conforme ADR 0002
- Decisões → `adr/` · Ciclos → `specs/NNN-nome/` · Publicação (GitHub Pages) → `mkdocs.yml`
