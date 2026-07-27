# Implementation Plan: Versão e data de atualização na capa

**Branch**: `015-versao-data-capa` · **Date**: 2026-07-27 · **Spec**: [spec.md](./spec.md)

## Summary

Exibir na tela-capa (splash) um selo discreto `vX.Y.0 · atualizado em <data>`. A **versão** é derivada em build-time da última edição de `livro/HISTORICO.md` (fonte única — nunca deriva de um segundo lugar); a **data** vem do último commit (`git log -1`), com fallback para a data do build. Ambos com fallbacks que jamais quebram o build.

## Technical Context

- **Motor**: `publicar/build.mjs`. Adicionar duas funções puras de build-time:
  - `versaoDoLivro()`: lê `livro/HISTORICO.md`, casa a **primeira** ocorrência de `^### Edição (\d+)\.(\d+)` → `v$1.$2.0`; fallback `v0.0.0`.
  - `dataDaUltimaModificacao()`: `execSync("git log -1 --format=%cI")` → formata pt-BR via `Intl.DateTimeFormat("pt-BR", {dateStyle:"long"})`; em erro (sem git / repo raso sem HEAD), usa `new Date()` (data do build).
- **Render**: `paginaSplash()` recebe/usa esses valores num `<p class="splash-versao">`.
- **CSS**: `.splash-versao` — pequeno, opaco reduzido, sobre o fundo escuro (contraste AA).
- **Sem dependências novas** (usa `node:child_process` e `Intl`, nativos).

## Constitution Check

| Princípio | Conformidade |
|---|---|
| I. Evidência acima de retórica | ✓ Versão e data derivam de fontes reais (HISTORICO, git), não digitadas. |
| II. A fonte-base é o código | N/A (elemento de UI factual). |
| III. Método pedagógico | N/A (não é capítulo). |
| IV. Livro vivo (datação) | ✓ **Reforça diretamente** a tese: a entrada do livro agora carimba versão e data de modificação; alinhado ao placar de edições. |
| V. Segurança e credenciais | ✓ Sem segredos; `git log` só lê metadados locais. |
| VI. Neutralidade e acessibilidade | ✓ Selo com contraste adequado; não competitivo. |
| VII. Spec-driven e branch-per-melhoria | ✓ Feature na branch `015-…`, merge ao fim. |
| Política de identidade de modelo | ✓ Nada de identificador interno no HTML. |

**Resultado**: PASS. Sem violações.

## Project Structure

```
publicar/build.mjs            # + versaoDoLivro(), dataDaUltimaModificacao(), uso em paginaSplash()
publicar/tema/estilo.css      # + .splash-versao
livro/HISTORICO.md            # + edição 0.11 (esta feature) -> torna-se a versão exibida (v0.11.0)
specs/015-versao-data-capa/   # spec, checklist, plan, tasks
```

## Design decisions

1. **Fonte única da versão = HISTORICO.md**: evita drift entre "versão exibida" e "edição registrada". Adicionar a edição 0.11 (desta feature) faz o selo mostrar `v0.11.0` automaticamente.
2. **Data pelo git**, não string manual: fiel à última modificação real; no CI (checkout depth 1) `git log -1` do HEAD funciona.
3. **Fallbacks totais**: qualquer falha de git/parse degrada para valores seguros; o build (e o gate) nunca quebra por causa do selo.
4. **Discrição**: uma linha pequena perto dos créditos; não altera a hierarquia visual título → CTA.

## Complexity Tracking

*Sem violações; tabela vazia.*
