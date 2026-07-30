# Histórico — este é um livro vivo

> Princípio IV da constituição (`.specify/memory/constitution.md`): o que este livro
> descreve tem data; toda edição fica registrada aqui, com o modelo de IA usado.

## Como ler as datas do livro

- **Data do evento** — quando algo aconteceu no mundo (ex.: publicação de um paper);
  vive no corpo do texto e não muda.
- **Data de captura** — o "estado da arte capturado em AAAA-MM" no cabeçalho de cada
  capítulo: quando as fontes, bibliotecas e links foram verificados pela última vez.
- **Rodada** — o ciclo spec-kit (`specs/NNN-*`) que produziu ou revisou o conteúdo.

## Tabela de snapshot por capítulo

| Capítulo | Estado da arte capturado em | Etapa testada | Última revisão |
|---|---|---|---|
| 00 Introdução | 2026-07 | ✓ (etapa 00) | 2026-07-30 |
| 01 O problema multicritério | 2026-07 | ✓ (etapa 01) | 2026-07-30 |

## Edições

### Edição 0.1 — 2026-07-30 · fundação do projeto (spec 001)

- Nasce o projeto **Decisor**: constituição própria (v1.0.0, linhagem Engenharia de
  Harness + Maestro), `CLAUDE.md`/`AGENTS.md` para agentes, guia editorial com esqueleto
  v3 e caso âncora, sumário com a sequência didática completa (14 capítulos, Parte I–IV).
- Capítulos 00 e 01 escritos no esqueleto v3; bibliografia inicial com 30+ fontes e
  status de verificação (✓/?) — curadoria registrada em `bibliografia.md`.
- `decisor-zero/` etapas 00 (esqueleto FastAPI) e 01 (matriz de decisão como código),
  com os worked examples dos capítulos reproduzidos em testes.
- `app/` (o produto Decisor): backend FastAPI + motor SAW puro + repositório com
  Postgres (Neon) e fallback SQLite; frontend estático v0. Decisões em ADR 0001–0004.
- **Verificação**: `pytest` verde nas etapas e no app; build do livro verde
  (ver `specs/001-fundacao/qa-report.md`).
- **IA**: agente **Claude Code (Anthropic)**; curadoria humana pendente de gate de merge.

## Registro de expiração (o placar das previsões)

| Componente | Existe porque… | Previmos que expira quando… | Estado | Evidência datada |
|---|---|---|---|---|
| Fallback SQLite no `app/` | a trilha deve rodar a custo zero e offline (Princípio VI) | o cap. 13 tornar o provisionamento Neon parte da trilha | 🔵 aberta | — |
| Frontend estático v0 | zero build = carga cognitiva mínima nas etapas | a UI do produto exigir estado complexo (comparação multi-método, cap. 11+) → migração conforme ADR 0002 | 🔵 aberta | — |
| Status "?" na bibliografia | editores bloqueiam verificação por robô | cada fonte "?" for promovida a ✓ antes de ser citada em capítulo novo | 🔵 aberta | — |

Legenda: 🔵 aberta · 🟡 em movimento · 🟢 cumprida · 🔴 refutada/não-expira.
Regra de manutenção: revisar este placar a cada edição.
