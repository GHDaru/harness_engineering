# Tasks: Divulgação de co-autoria humano+IA na abertura

**Feature**: `011-divulgacao-coautoria-ia` · Tests: n/a (doc; gate = build + revisão developmental).

## Phase 1: User Story 1 — nota de autoria no cap. 00 (P1) 🎯 MVP

- [x] T001 [US1] Adicionar a seção `## Nota de autoria e método` em `livro/00-introducao.md` (após "O método: ler código, não marketing"): co-autoria humano+IA (Claude Code/Anthropic) sob autoria/curadoria/responsabilidade humanas; IA **não** é autora; ponteiro para Guia §6.D e às políticas (ICMJE/COPE/Nature/Science). Sem identificador interno de modelo. (FR-001..003, FR-005)

## Phase 2: Polish & Cross-Cutting

- [x] T002 **Revisão developmental** (portão v1.2.0): re-ver a nota — clara? afirma responsabilidade humana? não soa como "IA escreveu sozinha"? ponteiro correto? (FR-004)
- [x] T003 Gate de build: `cd publicar && node build.mjs` verde; a seção aparece em `00-introducao.html` com link interno válido para o Guia (SC-002/SC-003).
- [x] T004 Registrar no `HISTORICO.md` (edição 0.7 já existe; anexar A1 concluído) e verificar SC-001..003.

## Dependencies / Strategy
- MVP = T001 (a nota). T002–T004 são polish. Feature de uma story.
