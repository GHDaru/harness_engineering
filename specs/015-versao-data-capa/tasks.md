# Tasks: Versão e data de atualização na capa

**Feature**: `015-versao-data-capa` · **Plan**: [plan.md](./plan.md)

## Fase 1 — Motor

- [x] **T101** Em `publicar/build.mjs`, adicionar `versaoDoLivro()`: parseia a 1ª `### Edição X.Y` de `livro/HISTORICO.md` → `vX.Y.0`; fallback `v0.0.0`. (FR-001, FR-004)
- [x] **T102** Adicionar `dataDaUltimaModificacao()`: `git log -1 --format=%cI` → data pt-BR (`dateStyle:"long"`); fallback data do build. (FR-002, FR-003, FR-004)
- [x] **T103** Usar ambos em `paginaSplash()` num `<p class="splash-versao">vX.Y.0 · atualizado em <data></p>`. (FR-001, FR-002, FR-007)

## Fase 2 — Estilo

- [x] **T201** `.splash-versao` em `publicar/tema/estilo.css`: discreto, contraste AA no fundo escuro, sem estourar no mobile. (FR-007, SC-005)

## Fase 3 — Registro

- [x] **T301** `livro/HISTORICO.md`: edição 0.11 (selo de versão/data na capa) + modelo de IA (A3). Isso define a versão exibida como `v0.11.0`. (Princípio IV, SC-001)

## Fase 4 — Verificação e merge

- [x] **T401** `node build.mjs`: build verde; `index.html` mostra `v0.11.0 · atualizado em <data>`; link-check sem quebras. (FR-005, SC-001, SC-002)
- [x] **T402** Screenshot desktop+mobile da splash com o selo; conferir contraste e não-overflow; zero identificador interno de modelo. (SC-004, SC-005)
- [x] **T403** Commit na branch `015-…`, merge para `main` (`--no-ff`), push → deploy. (Princípio VII)
