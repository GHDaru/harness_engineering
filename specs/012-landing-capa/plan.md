# Implementation Plan: Landing / hero de capa no site

**Branch**: `012-landing-capa` | **Date**: 2026-07-26 | **Spec**: [spec.md](./spec.md)

## Summary

Renomear a capa para `publicar/tema/capa.png`, gerar a social 1200×630 (`capa-social.png`) via Chromium/Playwright, e adicionar uma **hero** ao topo do `index.html` (imagem + título + subtítulo + CTAs + créditos) mantendo o sumário abaixo. Ajustar `build.mjs` para copiar os assets de capa e injetar meta tags Open Graph; CSS responsivo e theme-aware.

## Technical Context

**Language/Version**: Node (motor `publicar/`, markdown-it) + HTML/CSS. **Primary Dependencies**: markdown-it, esbuild (já presentes); Chromium/Playwright (global) para gerar a social. **Storage**: assets PNG versionados. **Testing**: gate de link-check do build + verificação visual (Playwright screenshot) + checagem responsiva. **Target Platform**: site GitHub Pages. **Project Type**: site estático (motor próprio). **Scale/Scope**: um bloco hero + 2 assets + meta tags.

## Constitution Check

*GATE: Must pass before Phase 0. Re-check after Phase 1.* (Constituição **v1.2.0**.)

| Princípio | Status | Nota |
|---|---|---|
| I. Evidência | ✅ (n/a) | Feature de UI; sem afirmações que exijam fonte. |
| II. Fonte-base é código | ✅ (n/a) | Não é dimensão de harness. |
| III. Método pedagógico | ✅ | UI de abertura; Diátaxis não se aplica a chrome de navegação. |
| IV. Livro vivo | ✅ | Registro no HISTORICO (edição) com agente/modelo. |
| V. Segurança | ✅ | Sem segredos; **sem identificador interno de modelo** (FR-008). |
| VI. Neutralidade/acessibilidade | ✅ **(central)** | `alt` descritivo, créditos como texto, responsivo, theme-aware — a feature *serve* este princípio. |
| VII. Spec-driven | ✅ | Ciclo oficial na branch `012`; toca o motor `publicar/`. |
| Portão — revisão developmental (v1.2.0) | ✅ (a aplicar) | Revisar copy/layout da hero antes de publicar. |

**Gate: PASS** — sem violações.

## Project Structure

Fonte alterada: `publicar/build.mjs` (copiar assets de capa + `<head>` OG + hero no index), `publicar/tema/estilo.css` (CSS da hero), `publicar/tema/capa.png` (renomeado), `publicar/tema/capa-social.png` (novo). Registro: `livro/HISTORICO.md`.

**Structure Decision**: hero renderizada no template do `index.html` dentro do `build.mjs` (onde a capa/sumário já é montada); assets copiados como estilo.css/app.js já são. Sem página nova no sumário.

## Phase 0 / Phase 1
- **Phase 0**: sem pesquisa (decisões de UI conhecidas). Sem `NEEDS CLARIFICATION`.
- **Phase 1**: contrato = a estrutura da hero (spec §Key Entities + FRs). Re-check pós-design: **PASS**.

## Complexity Tracking
> Sem violações — vazio.
