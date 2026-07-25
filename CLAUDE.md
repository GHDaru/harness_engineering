# CLAUDE.md — instruções para agentes neste repositório

Este repositório é o livro vivo **Engenharia de Harness** (teoria + benchmark + construção prática `harness-zero`).

## Regra primária

**Todo trabalho neste repositório DEVE seguir as diretrizes do projeto, que estão na constituição: [`.specify/memory/constitution.md`](.specify/memory/constitution.md).** Em caso de conflito entre um pedido pontual e a constituição, a constituição prevalece — ou o conflito é explicitado ao usuário antes de agir.

Resumo do que a constituição exige (leia-a por inteiro antes de contribuir):

1. **Evidência acima de retórica** — afirmação sobre harness exige caminho de arquivo; citação científica exige status ✓; fonte da indústria exige URL verificável.
2. **A fonte-base é o código** — o livro nasce da leitura do código; ciência e indústria contextualizam. Tratamento por repositório vai para o Apêndice A; o corpo recebe o estado da arte.
3. **Método pedagógico combinado** — Backward Design + 4C/ID + Diátaxis + Carga Cognitiva. Esqueleto v3 de capítulo obrigatório. Detalhe operacional em `livro/GUIA-EDITORIAL.md`.
4. **Livro vivo** — datar a captura no cabeçalho do capítulo; atualizar `livro/HISTORICO.md` (incluindo o registro de expiração) sempre que o estado da arte mudar.
5. **Segurança** — nenhum segredo em arquivo/commit/texto; credenciais só em `.env` gitignored.
6. **Neutralidade e acessibilidade** — vendor-agnóstico; trilha prática a custo zero; português com termos técnicos sem tradução.
7. **Spec-driven e branch-per-melhoria (NÃO-NEGOCIÁVEL)** — toda melhoria (inclusive pedagógica/editorial) passa por spec-kit (`spec → plan → tasks → implement`) em sua própria branch `NNN-nome`. Exceção: emendas à constituição e correções triviais (typo/link) podem ir direto ao main.

## Mapa do repositório

- `livro/` — o livro. `GUIA-EDITORIAL.md` (como escrever), `HISTORICO.md` (edições + expiração), `bibliografia.md`, `capitulos/`.
- `benchmark/` — avaliações por dimensão (`README.md` = metodologia; `template/` = HARNESS_EVAL e FRAMEWORK_EVAL; `avaliacoes/`; `comparativo.md`).
- `harness-zero/` — a construção prática (Python + FastAPI), uma etapa por capítulo. Regras da construção: seção "Restrições" da constituição.
- `estudos/` — notas de pesquisa (parecer editorial, panoramas).
- `.specify/` — spec-kit (constituição + comandos `/speckit-*`). `.claude/skills/` — skill `academic-research`.
- `scripts/sync-forks.ps1` — sincronização local dos forks estudados.

## Ferramentas

- **spec-kit** para trabalho estruturado: `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement`. Planos respeitam a constituição.
- **skill `academic-research`** para referências científicas (localizar → validar → registrar → integrar).
- Forks dos harnesses estudados vivem fora deste repo; a fonte-base é lida deles.
