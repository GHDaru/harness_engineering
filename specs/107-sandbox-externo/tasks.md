# Tasks: Sandbox externo no cap. 07

**Input**: `specs/107-sandbox-externo/`

**Prerequisites**: spec.md, plan.md, research.md

## Phase 1: Spec

- [x] T001 Escrever `specs/107-sandbox-externo/spec.md` com a decisão do editor em 17/11/2026
- [x] T002 Escrever `plan.md` com Constitution Check, inclusive o conflito de branch e de merge
- [x] T003 Escrever `research.md` com o que post e código concordam e as divergências

## Phase 2: Capítulo (US1, US3)

- [x] T004 Acrescentar a seção 4 em `livro/capitulos/07-permissoes-sandbox.md`, a ressalva na Leitura executiva, a pergunta 5 e a entrada de apêndice com paths
- [x] T005 Atualizar objetivo 2, fontes da indústria, cabeçalho de revisão e respostas
- [x] T006 Traduzir o delta em `livro/en/chapters/07-permissions-sandboxing.md`
- [x] T007 Passada humanizer por leitura do parágrafo novo (sem varredura)

## Phase 3: Rastro (US2)

- [x] T008 Linha `promovido (spec 107)` em `radar/RADAR.md` e nota na seção de Leituras executivas
- [x] T009 Links em `livro/bibliografia.md` e `livro/en/bibliography.md`
- [x] T010 Edição 0.91 e placar em `livro/HISTORICO.md`
- [x] T011 Menção do cap. 07 no verbete MCP de `livro/glossario.md` e `livro/en/glossary.md`

## Phase 4: Verificação

- [x] T012 Regravar selos i18n com `node publicar/sela.mjs` nos EN traduzidos
- [x] T013 `cd publicar && npm run build` verde (prosa do cap. 07: 3,5 travessões/1k, 15,0 palavras/frase, 0 frases longas)
- [x] T014 Regenerar `chat-companion/backend/corpus.json` e conferir que "sandbox externo" é encontrável (`fonte`: o cap. 07)
- [x] T015 Abrir pull request em rascunho. Não mergear. PR: https://github.com/GHDaru/harness_engineering/pull/1
