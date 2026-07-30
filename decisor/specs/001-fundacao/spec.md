# Spec 001 — Fundação: livro vivo + aplicação de decisão multicritério

- **Status**: Aprovada (defaults) · **Raia**: Plena · **Data**: 2026-07-30
- **Origem**: pedido do Steward — "montar um livro vivo e uma aplicação para usuários
  tomarem decisão baseada em métodos quantitativos, seguindo as teorias multicritério;
  tomar como base o livro harness engineering; seguir a metodologia do maestro; backend
  FastAPI, banco Neon, livro no GitHub Pages; escrever CLAUDE.md e AGENTS.md para IA".

## O quê e por quê

Fundar o projeto **Decisor**: a governança escrita para IA (CLAUDE.md/AGENTS.md +
constituição), a sequência didática completa do livro, os dois primeiros capítulos com
suas etapas executáveis, o esqueleto do produto e a infraestrutura de publicação —
tudo autocontido e extraível para repositório próprio.

Dor real observada (não especulação):

- Decisões multicritério são tomadas "de cabeça" sem método; não há material em
  português que ensine MCDA **construindo** a ferramenta junto.
- Projetos guiados por IA sem constituição/spec degradam rápido (evidência: a própria
  existência do Maestro e do modelo do harness_engineering).

## Requisitos funcionais

- **FR1** — Governança para IA: `CLAUDE.md` e `AGENTS.md` (idênticos) + constituição
  própria com linhagem declarada (harness_engineering + Maestro).
- **FR2** — Sequência didática: `livro/SUMARIO.md` com 14 capítulos em 4 partes, cada
  capítulo mapeado a uma etapa do `decisor-zero`; racional em ADR.
- **FR3** — Fontes: `livro/bibliografia.md` com fontes seminais por método e status de
  verificação ✓/?; curadoria datada.
- **FR4** — Capítulos 00 e 01 no esqueleto v3, com caso âncora e worked examples
  reproduzidos por testes (Princípio I).
- **FR5** — `decisor-zero/` etapas 00 e 01 autocontidas (FastAPI + HTML sem build) com
  `pytest` verde.
- **FR6** — Produto v0 em `app/backend`: CRUD de decisões + ranking SAW; motor puro;
  Neon via `DATABASE_URL` com fallback SQLite; nenhum segredo em arquivo.
- **FR7** — Publicação: `mkdocs.yml` (Material + MathJax) com build estrito verde;
  workflows de Pages e CI prontos para o repositório próprio.
- **FR8** — Registro: ADRs 0001–0004, `HISTORICO.md` (edição 0.1 + modelo de IA),
  `CHANGELOG.md` com forcing function documentada.

## Fora de escopo (YAGNI)

- Capítulos 02–13 e seus métodos (uma rodada por capítulo, dali em diante).
- Frontend React, autenticação, deploy do backend, migrações Alembic (cap. 13 / specs
  próprias, raia infra).
- Criação do repositório próprio (ação externa — gate humano; ADR 0001).

## Critérios de aceite (DoD)

- [x] `pytest` verde em `decisor-zero/etapas/01-matriz` (worked examples do cap. 01)
- [x] `pytest` verde em `app/backend` (motor SAW + API ponta a ponta)
- [x] `mkdocs build --strict` verde
- [x] Nenhum segredo em arquivo (`.env.example` sem valores; `.gitignore` cobre `.env`)
- [x] ADRs 0001–0004 registrados; HISTORICO e CHANGELOG atualizados
- [ ] Gate humano: revisão do Steward e decisão sobre extração (ADR 0001)

## Clarify (resolvido — defaults, 2026-07-30)

- *Onde o projeto nasce?* → seed autocontido em `decisor/` na branch designada do
  harness_engineering (ADR 0001; alternativas registradas lá).
- *Qual frontend?* → estático v0, React+Vite quando a UI exigir (ADR 0002).
- *Qual publicador?* → MkDocs Material, pela matemática e custo de manutenção (ADR 0004).
- *Que método entra no produto v0?* → SAW, como adiantamento testado do cap. 04
  (Princípio II respeitado: fonte no docstring + worked example em teste).
