# Tasks: Página "Sobre o autor"

**Feature**: `014-pagina-sobre-autor` · **Plan**: [plan.md](./plan.md)

## Fase 1 — Conteúdo

- [x] **T101** Escrever `livro/autor.md`: resumo de abertura; Formação acadêmica; Atuação profissional (indústria); Docência (professor universitário + coordenação de curso); Produção acadêmica (artigos, anais, orientações); Perfis e contato. Fatos das fontes (Lattes/ORCID/LinkedIn/web); artigos no formato bibliográfico. (FR-002, FR-005, FR-008)

## Fase 2 — Integração no motor

- [x] **T201** Adicionar item "Sobre o autor" (`livro/autor.md`) ao `publicar/sumario.json`, em nova parte "Sobre" ao final. (FR-001, FR-003)
- [x] **T202** Ajustar `paginaSplash()` em `publicar/build.mjs`: nome "Gilsiley Henrique Darú" nos créditos vira `<a href="autor.html">`. (FR-004)

## Fase 3 — Verificação

- [x] **T301** `node build.mjs`: build verde, `autor.html` gerada, link-check sem quebras (`autor.html` no conjunto válido — automático via `sumario.json`). (FR-006, SC-004)
- [x] **T302** Screenshot desktop+mobile de `autor.html` e da splash (nome linkado); conferir seções, links de perfil, contraste. (SC-001, SC-002, SC-003)
- [x] **T303** Revisão de conteúdo: nenhuma afirmação sem lastro; zero identificador interno de modelo no HTML. (SC-005, SC-006)

## Fase 4 — Registro e merge

- [x] **T401** `livro/HISTORICO.md`: edição 0.10 (página do autor) + modelo de IA usado (A3). (Princípio IV)
- [x] **T402** Commit na branch `014-…`, merge para `main` (`--no-ff`), push → dispara o deploy (republica o site, inclusive a splash em `/`). (Princípio VII)
