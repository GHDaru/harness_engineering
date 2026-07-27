# Implementation Plan: Tela-capa full-screen (splash)

**Branch**: `013-splash-capa-cheia` | **Date**: 2026-07-27 | **Spec**: [spec.md](./spec.md)

## Summary
`index.html` vira uma **splash** full-screen (capa grande + título + CTA "Entrar no livro"), sem sidebar; o índice atual migra para **`sumario.html`** (com sidebar). Ajustar `build.mjs` (template splash + geração de `sumario.html` + marca→sumario + paginação + gate inclui sumario) e CSS.

## Technical Context
Node (motor `publicar/`) + HTML/CSS. Sem deps novas. Testing: link-check + verificação visual (Playwright). Target: GitHub Pages. Project Type: site estático. Scope: 1 template novo + 1 página + CSS.

## Constitution Check (v1.2.0)
| Princípio | Status |
|---|---|
| I/II | ✅ n/a (UI) |
| III | ✅ chrome de navegação (não é capítulo) |
| IV | ✅ registro no HISTORICO (agente/modelo) |
| V | ✅ sem segredos; sem ID interno de modelo |
| VI | ✅ **central**: responsivo, `alt`, contraste, créditos em texto |
| VII | ✅ ciclo oficial na branch 013 |
| Revisão developmental (v1.2.0) | ✅ a aplicar antes de publicar |

**Gate: PASS.**

## Structure Decision
Splash gerada por um template próprio (`paginaSplash`) no `build.mjs`; `sumario.html` pela `pagina()` existente. Gate de link-check passa a reconhecer `sumario.html`.

## Phase 0/1
Sem pesquisa; contrato = estrutura da splash (spec). Re-check pós-design: PASS.
