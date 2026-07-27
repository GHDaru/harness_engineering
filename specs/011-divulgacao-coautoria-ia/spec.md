# Feature Specification: Divulgação de co-autoria humano+IA na abertura do livro

**Feature Branch**: `011-divulgacao-coautoria-ia`

**Created**: 2026-07-26

**Status**: Draft

**Input**: Achado A1 do parecer `estudos/2026-07-26-achados-metodologia-escrita.md`: levar a divulgação de co-autoria humano+IA para a abertura do livro (cap. 00), não só para o Guia §6.D, seguindo as políticas de autoria (ICMJE/COPE/Nature/Science).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O leitor sabe, logo na abertura, quem escreveu o livro (Priority: P1)

Um leitor que abre o livro encontra, na introdução, uma **nota de autoria** clara: o livro é co-escrito com um agente de IA sob autoria e responsabilidade humanas. Não precisa caçar essa informação no Guia Editorial — ela está onde a confiança se estabelece, na abertura.

**Why this priority**: É o único objetivo da feature e a consequência editorial direta das políticas de autoria (transparência antes do conteúdo). Entregue sozinho, resolve o achado A1.

**Independent Test**: dar o cap. 00 a um leitor sem contexto e verificar que ele identifica a co-autoria humano+IA e quem responde pelo conteúdo.

**Acceptance Scenarios**:

1. **Given** o cap. 00 publicado, **When** o leitor o lê, **Then** encontra uma nota de autoria explícita (co-autoria humano+IA; humano responsável) com ponteiro para o método (Guia §6.D).
2. **Given** a nota, **When** o leitor busca a fundamentação, **Then** ela remete às políticas (ICMJE/COPE/Nature/Science) sem repetir o survey inteiro.

### Edge Cases

- E se o leitor interpretar como "a IA escreveu sozinha"? → a nota afirma explicitamente autoria/curadoria/responsabilidade humanas.
- E se a política de identidade impedir citar o modelo exato? → cita-se o **agente/produto** (Claude Code, Anthropic), não o identificador interno.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O cap. 00 (`livro/00-introducao.md`) DEVE conter uma **nota de autoria** curta e explícita: co-autoria humano+IA (Claude Code/Anthropic) sob **autoria, curadoria e responsabilidade humanas**.
- **FR-002**: A nota DEVE remeter ao método detalhado (Guia §6.D) e às políticas de autoria, **sem** duplicar o survey.
- **FR-003**: A nota DEVE deixar claro que a IA **não** é autora (não pode ser responsável), coerente com ICMJE/COPE/Nature/Science.
- **FR-004**: A construção DEVE passar pelo gate de build (link-check verde) e pela **revisão developmental** (portão novo da constituição v1.2.0).
- **FR-005**: Nenhum identificador interno de modelo nos artefatos (política de identidade) — usar o nome do agente/produto.

### Key Entities

- **Nota de autoria**: bloco na abertura (o quê: co-autoria; quem responde: humano; ponteiro: Guia §6.D + políticas).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um leitor sem contexto identifica, só pelo cap. 00, a co-autoria humano+IA e quem responde pelo conteúdo.
- **SC-002**: A nota tem ponteiro funcional para o Guia §6.D (link interno válido — gate de build verde).
- **SC-003**: Zero identificadores internos de modelo no texto publicado.

## Assumptions

- Placement = uma **seção nova curta no cap. 00** (não uma página de colofão separada, para não inflar o sumário); o Guia §6.D permanece o tratamento detalhado.
- Conteúdo, não código: nenhuma mudança no motor `publicar/`.
