# Tasks: DOI no site e README

**Feature**: `019-doi-badge-site` · **Plan**: [plan.md](./plan.md)

- [x] **T101** README: substituir o marcador `BADGE-DOI` pelo badge real do Zenodo. (FR-001)
- [x] **T102** `build.mjs` `paginaSplash()`: link do DOI junto ao selo de versão. (FR-002)
- [x] **T103** `estilo.css`: `.splash-doi` (link discreto sobre o fundo escuro). (FR-002)
- [x] **T104** `livro/autor.md`: seção "Como citar" com a referência formatada + DOI. (FR-003)
- [x] **T105** `livro/HISTORICO.md`: edição 0.15 (DOI fixado) + modelo de IA (A3).
- [x] **T201** `node build.mjs` verde; capa mostra o DOI; link-check ok; sem identificador interno de modelo. (FR-004, SC-*)
- [x] **T202** Commit na branch `019-…`, merge para `main` (`--no-ff`), push → deploy. (Princípio VII)
