# Implementation Plan: Sandbox externo no cap. 07

**Branch**: `107-sandbox-externo` (spec) · git `cursor/107-sandbox-externo-7afd` | **Date**: 2026-11-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/107-sandbox-externo/spec.md`

## Summary

Promover, por decisão do editor em 17/11/2026, o padrão de sandbox externo ao cap. 07. A seção explica o padrão, compara com aprovação e com a contenção de sistema operacional já no capítulo, resume o protocolo lido em `PROTOCOL.md` (commit `0681c98`) e registra limites e divergências. Radar, bibliografia, histórico, par EN e selo i18n acompanham. Pull request em rascunho. Sem merge.

## Technical Context

**Language/Version**: Markdown do livro (PT e EN). Sem código de produção.

**Primary Dependencies**: `publicar/` (build, selos, mede-prosa). Corpus do companion regenerado porque `livro/` e `radar/` são fonte.

**Storage**: N/A

**Testing**: `cd publicar && npm run build`. Selo via `node publicar/sela.mjs` nos EN tocados, depois de traduzir.

**Target Platform**: Site estático do livro.

**Project Type**: Capítulo do livro vivo.

**Performance Goals**: N/A

**Constraints**: Sem segredo. Sem identificador interno de modelo. Sem frase copiada das fontes além de citação curta marcada. Sem número que a fonte não tenha. Portão de prosa v4 no capítulo.

**Scale/Scope**: Uma seção no estado da arte, ressalva na Leitura executiva, uma pergunta de verificação, uma entrada de apêndice fora do corpus, bibliografia, histórico, uma linha do Radar.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after the text was written.*

| Princípio | Resultado |
|---|---|
| I. Evidência | Caminhos no Apêndice A do cap. 07 (`PROTOCOL.md`, `COVERAGE.md`, `README.md`, `claude-code/README.md`, `claude-code/claude-shell-prefix.sh`, `codex/README.md`, README da extensão do Pi). Post e protocolo com URL. Commit `0681c98` datado. |
| II. Fonte-base é o código | O corpo sintetiza. O tratamento com path fica no Apêndice A. Onde o post e o código divergem, o capítulo segue o código e diz a divergência. O repositório não entra no corpus. |
| III. Método | Esqueleto v3 preservado. A seção é explicação (Diátaxis), não tutorial. A pergunta 5 testa o objetivo 2, que passou a incluir situar o sandbox externo. Uma ideia nova por parágrafo na seção nova. |
| IV. Livro vivo | Cabeçalho do cap. 07: última revisão 2026-11-17. Captura do panorama permanece 2026-07 (não houve nova rodada do corpus). Edição 0.91 no HISTORICO. Placar relido: sandbox segue 🔴, policy engine segue 🔵, com evidência datada na linha de sandbox. |
| V. Segurança | Nenhum segredo. O texto ensina que a chave fica no proxy e não entra no documento da política. |
| VI. Neutralidade | Sem nota de benchmark. Sem favor a fornecedor. Trilha do harness-zero intocada. Prosa em português, termos técnicos sem tradução. |
| VII. Spec-driven | Spec, plano e tarefas existem em `specs/107-sandbox-externo/`. **Conflito explícito:** a constituição pede branch `107-sandbox-externo` e merge na `main` ao concluir. Esta sessão é obrigada a usar a branch `cursor/107-sandbox-externo-7afd`, e o editor pediu pull request em rascunho, sem merge. O merge fica com o editor, depois da revisão. Não foi feito. |

Sem identificador interno de modelo em commit ou artefato. A linha A3 do HISTORICO usa a assinatura do repositório: "Claude Code (Anthropic)".

## Project Structure

### Documentation (this feature)

```text
specs/107-sandbox-externo/
├── spec.md
├── plan.md
├── research.md
├── tasks.md
└── checklists/requirements.md
```

### Source Code (repository root)

```text
livro/capitulos/07-permissoes-sandbox.md
livro/en/chapters/07-permissions-sandboxing.md
livro/bibliografia.md
livro/en/bibliography.md
livro/glossario.md
livro/en/glossary.md
livro/HISTORICO.md
radar/RADAR.md
```

**Structure Decision**: Edição editorial. Sem `data-model.md` nem `contracts/`: não há entidade de software nova. A pesquisa das divergências está em `research.md`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| Branch git fora do padrão `NNN-nome` | O ambiente desta sessão só aceita `cursor/<nome>-7afd` | Criar `107-sandbox-externo` impediria o pull request que o editor pediu |
| Sem merge na `main` | O editor pediu rascunho e proibiu o merge | O merge é o que publica o site. Publicar antes da revisão do editor contradiz o pedido |
