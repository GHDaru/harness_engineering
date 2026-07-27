# Tasks: DOI e citação (Zenodo)

**Feature**: `018-doi-citacao-zenodo` · **Plan**: [plan.md](./plan.md)

## Fase 1 — Licenças
- [x] **T101** `LICENSE`: CC BY 4.0 (conteúdo) — aviso canônico + URLs oficiais + escopo. (FR-001)
- [x] **T102** `LICENSE-CODE`: MIT (código), titular Gilsiley Henrique Darú. (FR-001)

## Fase 2 — Metadados
- [x] **T201** `CITATION.cff`: autor+ORCID, título, versão, data, url/repo, licença, resumo, keywords. (FR-002)
- [x] **T202** `.zenodo.json`: creators (nome+ORCID), upload_type=publication/book, access_right=open, license=cc-by-4.0, keywords, idioma por, related_identifiers (site), **descrição com nota de co-autoria de IA**. (FR-003, FR-004)

## Fase 3 — README e registro
- [x] **T301** `README.md`: seções "Como citar" e "Licença" (o que cada licença cobre; espaço para o badge do DOI). (FR-005)
- [x] **T302** `livro/HISTORICO.md`: edição 0.14 (preparação de DOI/citação) + modelo de IA (A3).

## Fase 4 — Verificação e merge
- [x] **T401** `CITATION.cff` e `.zenodo.json` válidos (YAML/JSON parseiam); sem segredo; sem identificador interno de modelo. (FR-006, SC-004)
- [x] **T402** Commit na branch `018-…`, merge para `main` (`--no-ff`), push. (Princípio VII)
