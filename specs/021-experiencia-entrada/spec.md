# Feature Specification: Experiência de entrada do livro (índice repaginado)

**Feature Branch**: `021-experiencia-entrada` · **Created**: 2026-07-27

**Input**: A entrada do livro (sumário) era uma lista crua. O autor aprovou uma **síntese** de UX: **sidebar** com a lista completa (navegação sem rolar) + conteúdo principal com **hero** (capa, título, versão/DOI, CTAs) + card **"Continue lendo/Retomar"** + **trilha** em 4 passos + **capítulos em cartões** com teaser. Mesmo padrão visual servirá de base para as páginas de capítulo (feature futura). Aprovado nos temas claro e escuro.

## User Scenarios

### US1 — O leitor entra e tem direção + beleza (P1)
Ao abrir o sumário, o leitor vê um hero convidativo, pode **começar do início**, **retomar de onde parou** (se já leu), enxerga a **trilha** da obra e escolhe capítulos em **cartões** com um teaser. A **sidebar** continua com o índice completo para pular a qualquer ponto.

**Acceptance**:
1. Abrir o sumário → hero (capa+título+`vX.Y.0`/DOI+CTAs), trilha (4), cartões por parte, sidebar completa.
2. Se há leitura anterior (localStorage), o card **"Retomar"** aparece com o último capítulo e leva a ele; sem histórico, fica oculto.
3. Cada cartão leva ao capítulo; badge com o número, título e teaser.
4. Tema claro e escuro consistentes (herdando `--vars`).

### Edge Cases
- Sem `localStorage`/sem histórico: retomar oculto, sem quebrar.
- Mobile: sidebar recolhe/empilha; cartões viram 1–2 colunas; sem overflow.
- Aparato (benchmark, bibliografia, histórico, guia, autor): como **pills** compactas (não cartões grandes).

## Requirements

- **FR-001**: A página **sumário** DEVE renderizar: hero + retomar (condicional) + trilha (4 passos) + grids de cartões (Abertura, Funcionalidade) + pills (Benchmark/Aparato/Sobre), mantendo a **sidebar** com o índice completo.
- **FR-002**: Cada cartão de capítulo DEVE ter **número (badge)**, **título** e **teaser** (de `sumario.json`), e linkar o capítulo.
- **FR-003**: O card **Retomar** DEVE usar `localStorage` (último capítulo lido, gravado ao abrir cada capítulo) e ocultar-se sem histórico.
- **FR-004**: A trilha DEVE ter 4 passos (Fundamentos → Funcionalidades → Benchmark → Mão na massa) linkando alvos reais.
- **FR-005**: DEVE ser **theme-aware** (claro/escuro via `--vars`), **responsivo** e **acessível** (contraste, foco, `alt`).
- **FR-006**: O gate de link-check DEVE seguir **verde**; sem identificador interno de modelo.
- **FR-007**: O padrão de cartão/estilo DEVE ser reaproveitável nas páginas de capítulo (feature futura).

## Success Criteria
- **SC-001**: Sumário exibe hero+trilha+cartões+pills; sidebar completa; nada quebrado.
- **SC-002**: Retomar aparece após ler um capítulo e leva a ele; oculto sem histórico.
- **SC-003**: Claro e escuro OK; mobile sem overflow (~375px).
- **SC-004**: Build verde; zero identificador interno de modelo.

## Assumptions
- Só a **entrada** (sumário) nesta feature; o **template de capítulo** e o **glossário** são features seguintes.
- Teasers curtos por capítulo entram no `sumario.json` (conteúdo reaproveitável).
- Feature toca `publicar/` → ciclo spec-kit; merge após aprovação (screenshots) publica.
