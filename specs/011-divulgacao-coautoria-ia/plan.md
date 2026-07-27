# Implementation Plan: Divulgação de co-autoria humano+IA na abertura

**Branch**: `011-divulgacao-coautoria-ia` | **Date**: 2026-07-26 | **Spec**: [spec.md](./spec.md)

## Summary

Adicionar uma **nota de autoria** curta ao cap. 00 (`livro/00-introducao.md`), logo após a seção "O método", divulgando a co-autoria humano+IA sob responsabilidade humana, com ponteiro para o Guia §6.D e as políticas de autoria. Sem código; reusa as fontes já verificadas do §6 (nenhuma pesquisa nova).

## Technical Context

**Language/Version**: Português + Markdown. **Primary Dependencies**: motor `publicar/` (sem mudança). **Storage**: N/A. **Testing**: gate de link-check + revisão developmental (constituição v1.2.0). **Target Platform**: site GitHub Pages. **Project Type**: documentação (uma seção de capítulo). **Scale/Scope**: uma seção curta.

## Constitution Check

*GATE: Must pass before Phase 0. Re-check after Phase 1.* (Constituição **v1.2.0**.)

| Princípio | Status | Nota |
|---|---|---|
| I. Evidência | ✅ | A nota remete a fontes reais já verificadas (§6); nenhuma nova afirmação sem base. |
| II. Fonte-base é código | ✅ (n/a) | Meta-nota editorial; não é dimensão de harness. |
| III. Método pedagógico | ✅ | Texto de *explanation* na abertura; não exige esqueleto v3 (capítulo de abertura). |
| IV. Livro vivo | ✅ | Registro no HISTORICO com agente/modelo (A3 já vigente). |
| V. Segurança | ✅ | Sem segredos; **sem identificador interno de modelo** (FR-005). |
| VI. Neutralidade/acessibilidade | ✅ | Prosa PT; nomeia o agente/produto, não favorece marca. |
| VII. Spec-driven | ✅ | Esta feature roda o ciclo oficial na branch `011`. |
| **Portão novo — revisão developmental (v1.2.0)** | ✅ (a aplicar) | A implementação inclui o passo de revisão antes de publicar. |

**Gate: PASS** — sem violações.

## Project Structure

Fonte alterada: `livro/00-introducao.md` (nova seção) + `livro/HISTORICO.md` (registro). Artefatos em `specs/011-divulgacao-coautoria-ia/`.

**Structure Decision**: seção nova no cap. 00 (decisão nas Assumptions da spec); sem página de colofão (não inflar o sumário); sem mudança no motor.

## Phase 0 / Phase 1
- **Phase 0 (research)**: nenhuma pesquisa nova — reusa as fontes verificadas do Guia §6 (ICMJE/COPE/Nature/Science). Sem `NEEDS CLARIFICATION`.
- **Phase 1 (design)**: sem data-model/contracts (prosa curta; o "contrato" é a spec). Re-check pós-design: **PASS**.

## Complexity Tracking
> Sem violações — vazio.
