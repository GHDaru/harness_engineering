# Feature Specification: Landing / hero de capa no site

**Feature Branch**: `012-landing-capa`

**Created**: 2026-07-26

**Status**: Draft

**Input**: Publicar a imagem de capa gerada (`Engenharia de Harness.png`, 1024×1536) como uma **hero de abertura no `index.html`** do site, acima do sumário, com título, subtítulo, chamada para leitura e os créditos; incluir preview social (og:image). Renomear o arquivo para um nome sem espaços.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O visitante chega a uma capa, não a uma lista (Priority: P1)

Quem abre o site vê primeiro a **capa do livro** (a arte) com título, subtítulo e um convite claro para começar a ler — e logo abaixo continua o sumário atual. A primeira impressão é de um livro, não de um índice cru.

**Why this priority**: É o objetivo da feature — dar uma porta de entrada visual ao livro. Entregue sozinho, resolve o pedido.

**Independent Test**: abrir `index.html` e verificar que a capa aparece no topo, com CTA para o cap. 00, e o sumário logo abaixo.

**Acceptance Scenarios**:

1. **Given** a home publicada, **When** o visitante a abre, **Then** vê a hero com a imagem de capa, título, subtítulo e um botão "Começar a ler" (→ cap. 00), além de atalhos (Benchmark, Guia).
2. **Given** um link do site compartilhado numa rede social/chat, **When** o preview é gerado, **Then** aparece uma imagem de preview (og:image) e título/descrição corretos.

### Edge Cases

- Tela estreita (mobile): a hero empilha (imagem acima, texto abaixo) sem quebrar o layout.
- Sem a imagem (falha de asset): a hero degrada para título+subtítulo em texto, sem área quebrada.
- Acessibilidade: a imagem tem `alt` descritivo; os créditos são texto real (não embutidos só na imagem).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O arquivo de capa DEVE ser renomeado para um nome **sem espaços** (`publicar/tema/capa.png`) e versionado.
- **FR-002**: O `index.html` gerado DEVE exibir, no topo, uma **hero** com a imagem de capa + título + subtítulo + **CTA "Começar a ler"** (→ `00-introducao.html`) + atalhos (Benchmark, Guia).
- **FR-003**: O sumário atual DEVE permanecer **abaixo** da hero (navegação preservada).
- **FR-004**: A imagem DEVE ter **`alt` descritivo**; os créditos (Gilsiley Henrique Darú — edição/direção/orquestração; Claude/Anthropic — pesquisa/texto; GPT/OpenAI — imagem) DEVEM aparecer como **texto** (acessibilidade + coerência com a divulgação de co-autoria do cap. 00).
- **FR-005**: A página DEVE ter meta tags de **preview social** (`og:title`, `og:description`, `og:image`) apontando para uma imagem social **1200×630**.
- **FR-006**: A hero DEVE ser **responsiva** (empilha no mobile) e respeitar o tema claro/escuro do site.
- **FR-007**: O motor `publicar/build.mjs` DEVE **copiar os assets de capa** para `docs/assets/`; o gate de build (link-check) DEVE continuar verde.
- **FR-008**: Nenhum identificador interno de modelo nos artefatos (política de identidade) — os créditos usam nomes de produto (Claude/Anthropic, GPT/OpenAI).

### Key Entities

- **Capa (asset)**: imagem 1024×1536 (`capa.png`) + derivado social 1200×630 (`capa-social.png`).
- **Hero**: bloco de abertura do index (imagem + título + subtítulo + CTAs + créditos).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Ao abrir a home, a capa é o primeiro elemento visível, com CTA funcional para o cap. 00.
- **SC-002**: O sumário permanece acessível abaixo da hero (nenhum item perdido).
- **SC-003**: O `<head>` contém `og:title`/`og:description`/`og:image` válidos (imagem social 1200×630 servida).
- **SC-004**: Em viewport ~375px de largura, a hero não estoura horizontalmente (empilha).
- **SC-005**: Gate de build verde; a imagem e a social existem em `docs/assets/`.
- **SC-006**: Zero identificadores internos de modelo no HTML publicado.

## Assumptions

- Opção **A** (hero no `index.html`), recomendada e não contestada — não uma página `capa.html` separada.
- A social 1200×630 é gerada a partir da capa (fit em fundo escuro) via Chromium/Playwright (sem PIL/sharp no ambiente).
- Feature toca o motor `publicar/` → ciclo spec-kit (Princípio VII).
