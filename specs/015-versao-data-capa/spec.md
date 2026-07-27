# Feature Specification: Versão e data de atualização na capa

**Feature Branch**: `015-versao-data-capa`

**Created**: 2026-07-27

**Status**: Draft

**Input**: O autor quer que a **tela-capa (splash)** exiba a **versão do livro** (ex.: `v0.11.0`) e a **data da última modificação** ("atualizado em …"). Coerente com a tese do livro vivo (datação/expiração) e com o placar de edições do `HISTORICO.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O leitor vê o quão fresco é o livro (Priority: P1)

Ao abrir a tela-capa, o visitante vê, de forma discreta, a **versão** do livro e **quando foi atualizado pela última vez** — sinal de que é um livro vivo, mantido e datado.

**Why this priority**: É o pedido; reforça a tese central (cláusula de expiração) logo na entrada.

**Independent Test**: abrir `index.html` → ver "v0.11.0 · atualizado em <data>" próximo aos créditos.

**Acceptance Scenarios**:

1. **Given** o site publicado, **When** abro a tela-capa, **Then** vejo a versão (`vX.Y.0`) e a data de última atualização em formato legível em português.
2. **Given** uma nova edição registrada no `HISTORICO.md`, **When** o site é reconstruído, **Then** a versão exibida acompanha automaticamente a última edição (sem edição manual de um segundo lugar).
3. **Given** o build no CI, **When** o site é gerado, **Then** a data reflete a última modificação de conteúdo (data do último commit), não uma data digitada à mão.

### Edge Cases

- Sem git disponível no ambiente de build: a data cai para a data do build (nunca quebra o build).
- `HISTORICO.md` sem uma edição parseável: a versão cai para um padrão seguro (ex.: `v0.0.0`) sem quebrar o build.
- Mobile: a linha de versão/data não estoura a largura; quebra bem.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A tela-capa (`index.html`) DEVE exibir a **versão** do livro no formato `vX.Y.0`, derivada **automaticamente** da última edição declarada em `livro/HISTORICO.md` (fonte única da verdade).
- **FR-002**: A tela-capa DEVE exibir a **data da última modificação** ("atualizado em <data>"), derivada da **data do último commit** no momento do build; sem git, usa a data do build.
- **FR-003**: A data DEVE ser formatada de modo legível em português (ex.: "27 de julho de 2026").
- **FR-004**: A derivação NÃO DEVE quebrar o build em nenhum caso (fallbacks seguros para versão e data).
- **FR-005**: O portão de link-check do build DEVE continuar verde.
- **FR-006**: Sem identificador interno de modelo em qualquer artefato publicado.
- **FR-007**: O elemento DEVE ser discreto e acessível (contraste no fundo escuro da splash), sem competir com título/CTA.

### Key Entities

- **Selo de versão/data**: linha na tela-capa com `vX.Y.0` + "atualizado em <data>".
- **Fonte da versão**: a última entrada `### Edição X.Y` de `livro/HISTORICO.md`.
- **Fonte da data**: data do último commit (`git log -1`), com fallback para data do build.

## Success Criteria *(mandatory)*

- **SC-001**: A tela-capa mostra `vX.Y.0` correspondente à última edição do `HISTORICO.md`.
- **SC-002**: A tela-capa mostra "atualizado em <data>" com a data do último commit.
- **SC-003**: Registrar nova edição no `HISTORICO.md` e reconstruir muda a versão exibida — sem tocar em outro arquivo.
- **SC-004**: Build verde; link-check sem quebras; sem identificador interno de modelo.
- **SC-005**: Em ~375px, a linha de versão/data não estoura horizontalmente.

## Assumptions

- Versão semântica mapeada da edição: `Edição X.Y` → `vX.Y.0` (decisão do autor: "alinhar às edições").
- A data de última modificação = data do último commit de conteúdo (build no CI reflete o merge mais recente).
- Feature toca o motor `publicar/` → ciclo spec-kit (Princípio VII).
