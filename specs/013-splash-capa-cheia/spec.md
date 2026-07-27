# Feature Specification: Tela-capa full-screen como entrada do site

**Feature Branch**: `013-splash-capa-cheia`

**Created**: 2026-07-27

**Status**: Draft

**Input**: A hero de capa (spec 012) ficou pequena como thumbnail. O autor quer que o site **abra numa tela-capa cheia** (estilo do card social: capa grande + título grande, fundo escuro) e só depois o leitor entre no índice/sumário e navegue.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O livro abre numa capa cheia e o leitor "entra" (Priority: P1)

Ao abrir o site, o visitante vê uma **tela-capa full-screen** — a arte da capa grande, título, subtítulo e créditos, num fundo escuro elegante — com um botão claro para **entrar no livro**. Ao clicar, chega ao sumário/índice e navega normalmente.

**Why this priority**: É o objetivo — uma entrada com presença de "livro", não uma lista. Entregue sozinho, resolve o pedido.

**Independent Test**: abrir `index.html` → ver a capa ocupando a tela, com CTA "Entrar no livro"; clicar → chegar ao sumário com a navegação.

**Acceptance Scenarios**:

1. **Given** o site publicado, **When** abro a home, **Then** vejo a tela-capa cheia (capa grande + título + subtítulo + créditos + CTA "Entrar no livro"), sem a lista de capítulos competindo.
2. **Given** a tela-capa, **When** clico em "Entrar no livro", **Then** vou ao **sumário** (`sumario.html`) com a sidebar e a lista completa.
3. **Given** qualquer página interna, **When** clico no título do livro (marca), **Then** volto ao **sumário** (não à splash), e há um link discreto para a **capa**.

### Edge Cases

- Mobile: a tela-capa empilha (capa em cima, texto/CTA embaixo) sem overflow.
- Sem a imagem: degrada para título+subtítulo+CTA em texto.
- Acessibilidade: `alt` descritivo; créditos como texto; contraste adequado no fundo escuro.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `index.html` DEVE ser uma **tela-capa full-screen** (min. 100svh) SEM a sidebar: capa grande + título + subtítulo + créditos + CTA **"Entrar no livro" → `sumario.html`** (+ atalhos Benchmark/Guia).
- **FR-002**: DEVE existir uma nova página **`sumario.html`** com o índice atual (sidebar + lista de partes/capítulos) — o conteúdo que hoje está no index.
- **FR-003**: A **marca** (título do livro na sidebar) DEVE apontar para `sumario.html`; DEVE haver um link discreto para a **capa** (`index.html`).
- **FR-004**: A paginação interna DEVE tratar `sumario.html` como o "início" (o 1º capítulo tem o Sumário como anterior; o Sumário tem o 1º capítulo como próximo).
- **FR-005**: A tela-capa DEVE ser **responsiva** (empilha no mobile) e a capa DEVE aparecer **grande** (ex.: até ~78svh de altura no desktop).
- **FR-006**: O portão de link-check do build DEVE continuar verde — `sumario.html` incluída no conjunto de páginas válidas.
- **FR-007**: Sem identificador interno de modelo (política de identidade); créditos com nomes de produto.
- **FR-008**: As meta Open Graph (capa-social) DEVEM permanecer em todas as páginas (preview de link).

### Key Entities

- **Splash (index)**: tela de entrada full-screen (capa + título + CTA); sem sidebar.
- **Sumário (`sumario.html`)**: índice navegável (sidebar + lista), destino do "Entrar".

## Success Criteria *(mandatory)*

- **SC-001**: Ao abrir a home, a capa ocupa a tela (a lista de capítulos não aparece antes do fold no desktop).
- **SC-002**: O CTA "Entrar no livro" leva ao `sumario.html`, de onde toda a navegação funciona.
- **SC-003**: A marca nas páginas internas leva ao `sumario.html`; existe link para a capa.
- **SC-004**: Em ~375px de largura, a tela-capa não estoura horizontalmente.
- **SC-005**: Gate de build verde; `sumario.html` e `index.html` gerados; assets de capa presentes.
- **SC-006**: Zero identificadores internos de modelo no HTML.

## Assumptions

- Duas páginas (splash `index` → `sumario`), decisão do autor ("abrir na capa, depois navegar pelo índice").
- Splash com fundo escuro fixo (a arte é escura); demais páginas seguem theme-aware.
- Feature toca o motor `publicar/` → ciclo spec-kit (Princípio VII).
