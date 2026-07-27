# Feature Specification: Página "Sobre o autor"

**Feature Branch**: `014-pagina-sobre-autor`

**Created**: 2026-07-27

**Status**: Draft

**Input**: O autor quer uma **página sobre o autor** no site do livro — uma apresentação (biografia acadêmica e profissional) de Gilsiley Henrique Darú, o editor/direcionador/orquestrador humano da obra. Fontes fornecidas: currículo Lattes (PDF), LinkedIn e busca na web (artigos publicados, atuação como professor universitário e coordenador de curso).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O leitor conhece quem dirige o livro (Priority: P1)

Ao navegar pelo livro, o leitor pode abrir uma página **"Sobre o autor"** e encontrar quem é Gilsiley Henrique Darú: formação (doutorado em andamento, mestrados, graduações), atuação profissional (cientista de dados / liderança em dados e IA na indústria de supply chain), trajetória docente (professor universitário e coordenador de curso de engenharia de produção) e produção acadêmica (artigos e orientações), com links verificáveis (Lattes, ORCID, LinkedIn).

**Why this priority**: É o pedido — dar rosto e credibilidade ao livro. Entregue sozinho, resolve a solicitação.

**Independent Test**: abrir `autor.html` → ver a biografia estruturada (formação, atuação, docência, produção) com links externos que funcionam.

**Acceptance Scenarios**:

1. **Given** o site publicado, **When** abro "Sobre o autor" pela sidebar, **Then** vejo a biografia com seções claras (quem é, formação, atuação, docência, produção acadêmica) e um resumo de abertura.
2. **Given** a tela-capa (splash), **When** clico no nome **"Gilsiley Henrique Darú"** nos créditos, **Then** chego à página "Sobre o autor".
3. **Given** a página do autor, **When** clico nos links de perfil (Lattes, ORCID, LinkedIn), **Then** abrem os perfis externos corretos em contexto verificável.

### Edge Cases

- Sem dados de um item (ex.: artigo sem DOI): registra o que há (veículo, ano) sem inventar identificador — Princípio I.
- Fotografia do autor é opcional; a página degrada bem sem imagem.
- Acessibilidade: títulos hierárquicos, links com texto descritivo, contraste do tema.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: DEVE existir uma página **"Sobre o autor"** (`autor.html`), gerada de um Markdown-fonte (`livro/autor.md`), com a sidebar e a navegação padrão do livro.
- **FR-002**: A página DEVE conter, no mínimo: (a) resumo de abertura; (b) **Formação acadêmica**; (c) **Atuação profissional** (indústria); (d) **Docência** (professor universitário e coordenação de curso); (e) **Produção acadêmica** (artigos, trabalho em anais, orientações); (f) **Perfis e contato** (Lattes, ORCID, LinkedIn).
- **FR-003**: A página DEVE ser alcançável pela navegação — entrar no `sumario.json` (aparecendo na sidebar e no sumário) — e receber paginação prev/next coerente.
- **FR-004**: A **tela-capa (splash)** DEVE transformar o nome do autor nos créditos em **link** para `autor.html`.
- **FR-005**: Toda afirmação factual DEVE ser rastreável às fontes (Lattes/ORCID/web); nenhum dado inventado (Princípio I). Artigos citados no formato bibliográfico do projeto.
- **FR-006**: O portão de link-check do build DEVE continuar **verde** (a nova página incluída no conjunto de páginas válidas; links internos resolvidos).
- **FR-007**: Sem identificador interno de modelo em qualquer artefato publicado (política de identidade).
- **FR-008**: A página DEVE ser coerente com o tom do livro (português, vendor-agnóstica quanto a empresas onde atua — fatos, não propaganda).

### Key Entities

- **Página do autor (`autor.md` → `autor.html`)**: back matter do livro com a biografia estruturada e links de perfil.
- **Créditos da splash**: ponto de entrada adicional para a página do autor.

## Success Criteria *(mandatory)*

- **SC-001**: A partir da sidebar/sumário, o leitor abre "Sobre o autor" e encontra as seis seções (resumo, formação, atuação, docência, produção, perfis).
- **SC-002**: O nome do autor na splash leva a `autor.html`.
- **SC-003**: Os links de perfil (Lattes `6253911800847523`, ORCID `0000-0002-8979-0461`, LinkedIn) estão presentes e corretos.
- **SC-004**: Gate de build verde; `autor.html` gerada; link-check sem quebras.
- **SC-005**: Zero identificadores internos de modelo no HTML.
- **SC-006**: Nenhuma afirmação sem lastro nas fontes (revisão de conteúdo).

## Assumptions

- A página é **back matter** (parte "Sobre" no fim do sumário), não um capítulo numerado.
- Fatos vêm do Lattes/ORCID/CV + busca web verificável; empresas e instituições são citadas como trajetória, sem juízo de valor.
- Feature toca o motor `publicar/` e o conteúdo `livro/` → ciclo spec-kit (Princípio VII).
