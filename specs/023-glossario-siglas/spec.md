# Feature Specification: Glossário + siglas por extenso

**Feature Branch**: `023-glossario-siglas` · **Created**: 2026-07-27

**Input**: O livro precisa de um **glossário**, e **toda sigla** deve estar "aberta" (por extenso). O glossário explica a sigla e o **contexto** em que ela aparece.

## Requisitos
- **FR-001**: DEVE existir uma página **Glossário** (`livro/glossario.md` → `glossario.html`), no aparato/sidebar, listando cada sigla: **por extenso**, explicação curta e **onde aparece** (capítulos).
- **FR-002**: O conteúdo DEVE ser **fiel ao livro** (siglas obtidas por varredura real; expansões conferidas no texto — Princípio I). Ex.: MCP = Model Context Protocol; ACP = Agent Client Protocol (Zed); A2A = Agent-to-Agent; LSP = Language Server Protocol; MAST = Multi-Agent System Failure Taxonomy.
- **FR-003**: Toda ocorrência de uma sigla conhecida DEVE ficar "aberta" ao leitor: o motor envolve a sigla em `<abbr title="Por Extenso">` (tooltip ao passar o mouse), **sem** alterar o texto-fonte e **sem** tocar em código/`<pre>`/links/títulos.
- **FR-004**: O **Guia Editorial** DEVE registrar a política ("expandir na 1ª ocorrência / abbr no motor").
- **FR-005**: Build **verde** (link-check); sem identificador interno de modelo; `<abbr>` estilizado de forma discreta e acessível.

## Sucesso
- SC-001: página Glossário no sidebar, com siglas + extenso + explicação + capítulos.
- SC-002: num capítulo, passar o mouse numa sigla mostra o por extenso; blocos de código intactos.
- SC-003: build verde; sem identificador interno de modelo.

## Assumptions
- Auto-`<abbr>` cobre "toda vez aberta" de forma não-invasiva; a expansão inline manual na 1ª ocorrência pode entrar numa rodada de auditoria depois.
- Feature toca `livro/` + `publicar/` → ciclo spec-kit; merge após aprovação (screenshots).
