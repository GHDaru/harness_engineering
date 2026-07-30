# Changelog

Todas as mudanças notáveis do **Decisor** são registradas aqui. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versionamento semântico.

> Forcing function (herdada do Maestro): toda PR adiciona uma entrada em
> **[Unreleased]** — a CI (`.github/workflows/ci.yml`, job `changelog`) falha se o
> `CHANGELOG.md` não for alterado. Bypass: label `skip-changelog`.

## [Unreleased]

### Added

- **Fundação do projeto (spec 001)**: constituição v1.0.0 (linhagem Engenharia de
  Harness + Maestro), [CLAUDE.md](CLAUDE.md)/[AGENTS.md](AGENTS.md) para agentes,
  spec-kit (`.specify/`), ADRs 0001–0004.
- **Livro**: guia editorial (esqueleto v3 + caso âncora), sumário com a sequência
  didática (14 capítulos), bibliografia com 30+ fontes e status de verificação,
  capítulos [00](livro/capitulos/00-introducao.md) e
  [01](livro/capitulos/01-problema-multicriterio.md), publicação MkDocs Material
  (`mkdocs build --strict` verde).
- **decisor-zero**: etapas `00-esqueleto` e `01-matriz` (motor puro `MatrizDecisao` +
  API + página), 11 testes reproduzindo os números do cap. 01 (+1 exercício do leitor).
- **app (produto v0)**: backend FastAPI + motor SAW puro (com fonte no docstring) +
  persistência Neon/Postgres com fallback SQLite + frontend estático; 8 testes.

### Follow-up

- Extração do seed para repositório próprio e ativação do GitHub Pages (ADR 0001).
- Promover fontes "?" da bibliografia a ✓ antes de citá-las em capítulos novos.
- Cap. 02 (estruturação + dominância) — próxima rodada natural.
