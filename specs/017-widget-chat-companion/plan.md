# Implementation Plan: Widget do chat-companion

**Branch**: `017-widget-chat-companion` · **Date**: 2026-07-27 · **Spec**: [spec.md](./spec.md)

## Summary

Um widget de chat flutuante em JS/CSS puro (sem framework), injetado pelo motor `publicar/` em **todas** as páginas geradas (inclusive a splash). Launcher que abre/minimiza um painel; cabeçalho de **capacidades por capítulo**; conversa com o backend 016 no Railway; identidade anônima em `localStorage`; modos avançado × progressivo. Degrada com elegância se o backend cair.

## Technical Context

- **Assets novos**: `publicar/tema/companion.js` + `publicar/tema/companion.css`, copiados para `docs/assets/` pelo build (como `app.js`/`estilo.css`).
- **Injeção por página**: `build.mjs` insere, em `pagina()` e `paginaSplash()`, um `<script>window.COMPANION = {backend, chapter, mode padrão, capabilities[]}</script>` + `<link>`/`<script>` do widget. `chapter` é derivado do título do item (ex.: "02 — …" → 2; capa/aparato → 0). `capabilities[]` é um espelho leve do registro do backend (chave/rótulo/descrição/libera) para render instantâneo e offline-safe.
- **Config de URL**: `publicar/sumario.json` ganha `"companion_backend"`; o build injeta. Fonte única, fácil de trocar.
- **Fonte da verdade do gating**: o **backend** (016) impõe no `/chat`. O mapa no front é só para **exibição** (o que mostrar como ativo/bloqueado) e é offline-safe.
- **Endpoints usados**: `POST /chat`, `GET /history`, `POST /session` (o `/capabilities` é opcional — o mapa embutido já cobre a exibição).

## Constitution Check

| Princípio | Conformidade |
|---|---|
| I. Evidência | ✓ As respostas do tutor (backend) citam o livro; o widget só apresenta. |
| III. Método pedagógico | ✓ O cabeçalho de capacidades por capítulo torna o *fading* visível ao leitor. |
| IV. Livro vivo | ✓ Edição registrada com modelo de IA (A3). |
| V. Segurança | ✓ Nenhum segredo no front; só a URL pública do backend; a chave vive no Railway; gating imposto no servidor. |
| VI. Neutralidade e acessibilidade | ✓ a11y (aria-label, foco, teclado, contraste), responsivo, theme-aware. |
| VII. Spec-driven | ✓ Branch `017-…`, merge ao fim. |
| Identidade de modelo | ✓ Sem identificador interno em nenhum artefato. |

**Resultado**: PASS.

## Project Structure

```
publicar/tema/companion.js     # NOVO — o widget (launcher + painel + chamadas)
publicar/tema/companion.css    # NOVO — estilos (theme-aware, responsivo, sobre a capa)
publicar/build.mjs             # injeta config por página + copia os assets; deriva chapter; espelha capabilities
publicar/sumario.json          # + "companion_backend"
livro/HISTORICO.md             # + edição 0.13 (widget)
specs/017-widget-chat-companion/
```

## Design decisions

1. **JS puro injetado no build** (não React/ilha): o widget é global e leve; segue o app.js existente. Progressive enhancement — sem JS, a página segue inteira.
2. **Mapa de capacidades espelhado no build** para render instantâneo e offline-safe; backend continua o **enforcer** do gating. Pequena duplicação de rótulos, comentada.
3. **`chapter` por página** derivado do título no build — o widget sabe onde o leitor está sem heurística no cliente.
4. **Degradação graciosa**: falha de rede → aviso no painel; cabeçalho de capacidades ainda aparece; a página nunca trava.
5. **Anônimo por navegador**: `session_id` em `localStorage` (fallback memória de aba); nada de login.

## Complexity Tracking

*Sem violações; tabela vazia.*
