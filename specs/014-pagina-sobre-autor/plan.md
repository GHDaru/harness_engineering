# Implementation Plan: Página "Sobre o autor"

**Branch**: `014-pagina-sobre-autor` · **Date**: 2026-07-27 · **Spec**: [spec.md](./spec.md)

## Summary

Adicionar uma página de back matter **"Sobre o autor"** ao site do livro: um Markdown-fonte (`livro/autor.md`) com a biografia acadêmica e profissional de Gilsiley Henrique Darú, publicado pelo motor existente como `autor.html`, alcançável pela sidebar/sumário e a partir dos créditos da tela-capa. Sem novo mecanismo de renderização — reaproveita o pipeline de capítulos (entrada no `sumario.json`), mais um pequeno ajuste no `paginaSplash()` para linkar o nome do autor.

## Technical Context

- **Motor**: `publicar/build.mjs` (Node + markdown-it) já renderiza qualquer item de `sumario.json` como página com sidebar + paginação + link-check. Basta um novo item apontando para `livro/autor.md`.
- **Conteúdo**: `livro/autor.md` — Markdown padrão do livro; sem selo "Estado da arte" (não é capítulo datado); fatos das fontes (Lattes 6253911800847523, ORCID 0000-0002-8979-0461, LinkedIn, Journal of Lean Systems art. 1930).
- **Splash**: `paginaSplash()` — envolver "Gilsiley Henrique Darú" num `<a href="autor.html">`.
- **Sem dependências novas**; sem CSS novo obrigatório (usa `.markdown`).

## Constitution Check

*Gate: consultado antes do design. Reavaliar após.*

| Princípio | Conformidade |
|---|---|
| I. Evidência acima de retórica | ✓ Fatos rastreáveis (Lattes/ORCID/LinkedIn/web); artigos no formato bibliográfico; nenhum dado inventado. |
| II. A fonte-base é o código | N/A direto (página institucional, não afirmação sobre harness). Mantém rigor factual. |
| III. Método pedagógico combinado | N/A (back matter, não capítulo v3 — não requer esqueleto de 8 seções). |
| IV. Livro vivo (datação) | Página institucional; sem selo de captura. Edição registrada no `HISTORICO.md` com modelo de IA (A3). |
| V. Segurança e credenciais | ✓ Só e-mail público que o autor divulga; sem segredos. |
| VI. Neutralidade e acessibilidade | ✓ Empresas citadas como trajetória factual, sem juízo; títulos hierárquicos, links descritivos. |
| VII. Spec-driven e branch-per-melhoria | ✓ Esta feature: spec → plan → tasks → implement na branch `014-…`, merge ao fim. |
| Política de identidade de modelo | ✓ Nenhum identificador interno no HTML/commits; créditos com nome de produto. |

**Resultado**: PASS. Nenhuma violação; sem entradas na tabela de complexidade.

## Project Structure

```
livro/autor.md                    # NOVO — conteúdo da biografia
publicar/sumario.json             # + item "Sobre o autor" (parte "Sobre")
publicar/build.mjs                # paginaSplash(): nome do autor -> link autor.html
livro/HISTORICO.md                # + edição 0.10 (página do autor)
specs/014-pagina-sobre-autor/     # spec, checklist, plan, tasks
```

## Design decisions

1. **Reuso do pipeline de capítulos** (não uma página especial como `sumario.html`): entrar no `sumario.json` dá, de graça, sidebar + paginação + link-check. Menor superfície de mudança no motor.
2. **Back matter** numa parte própria "Sobre" ao final do sumário — separa das partes de conteúdo, sinaliza que é institucional.
3. **Dois pontos de entrada**: sidebar/sumário (navegação) e créditos da splash (nome do autor → página).
4. **Tom factual e vendor-agnóstico**: trajetória por empresa/instituição com datas e responsabilidades; sem adjetivação promocional.

## Complexity Tracking

*Sem violações constitucionais; tabela vazia.*
