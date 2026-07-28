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

## Fluxo de trabalho (spec-kit) — uma branch por spec

Operacionaliza o Princípio VII. **Toda melhoria** — capítulo novo, **rodada de auditoria/revisão**, etapa do `harness-zero`, feature de infra, ajuste editorial — segue este ciclo, cada uma na **sua própria branch**. Não se edita direto na `main`.

1. **specify** — `bash .specify/scripts/bash/create-new-feature.sh "<nome>"` cria `specs/NNN-nome/` (e o nº da feature); então `git checkout -b NNN-nome`. Escreva `spec.md` (o QUÊ/PORQUÊ) a partir de `.specify/templates/spec-template.md`.
2. **checklist / clarify** — valide a qualidade do spec (`checklists/requirements.md`); use *clarify* quando houver ambiguidade real de escopo.
3. **plan** — `plan.md` com o **Constitution Check** (portão): conformidade com os 7 princípios, sem segredo, sem identificador interno de modelo.
4. **tasks** — `tasks.md` com tarefas verificáveis.
5. **implement** — implemente e **verifique**: build verde, link-check, testes e screenshots (quando houver UI).
6. **registrar** — atualize `livro/HISTORICO.md` (nova edição + modelo de IA usado) quando a mudança afeta o livro.
7. **merge** — ao concluir e verificar, **merge para a `main`** (`git merge --no-ff NNN-nome`) e push. **O merge na `main` é o que publica** (deploy do Pages nos paths `livro/`, `publicar/`, `benchmark/`); por isso, acumule o trabalho na branch e faça **um** merge por lote.

As skills `/speckit-*` (em `.claude/skills/`) automatizam esses passos; quando não estiverem disponíveis como comando, rode os scripts de `.specify/scripts/bash/` diretamente — o resultado é o mesmo (branch por spec).

**Exceções (Princípio VII):** emendas à constituição e a **este** documento de governança, e correções triviais (typo, link quebrado), podem ir direto à `main`, sempre com commit descritivo.

**Decisões (ADR):** toda decisão relevante (com alternativas e consequências) vira um registro em `adr/` (ver `adr/README.md`): contexto → decisão → alternativas avaliadas → justificativa → consequências. Registra o *porquê*, além do *o quê* (specs/HISTORICO).

## Mapa do repositório

- `livro/` — o livro. `GUIA-EDITORIAL.md` (como escrever), `HISTORICO.md` (edições + expiração), `bibliografia.md`, `capitulos/`.
- `benchmark/` — avaliações por dimensão (`README.md` = metodologia; `template/` = HARNESS_EVAL e FRAMEWORK_EVAL; `avaliacoes/`; `comparativo.md`).
- `harness-zero/` — a construção prática (Python + FastAPI), uma etapa por capítulo. Regras da construção: seção "Restrições" da constituição.
- `estudos/` — notas de pesquisa (parecer editorial, panoramas).
- `adr/` — Architecture Decision Records (decisões + alternativas + justificativa).
- `.specify/` — spec-kit: constituição (`memory/`), scripts (`scripts/bash/`), templates (`templates/`). `.claude/skills/` — skills `/speckit-*` (o ciclo spec-kit) e `academic-research`.
- `scripts/sync-forks.ps1` — sincronização local dos forks estudados.

## Ferramentas

- **spec-kit** para trabalho estruturado: `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement`. Planos respeitam a constituição.
- **skill `academic-research`** para referências científicas (localizar → validar → registrar → integrar).
- Forks dos harnesses estudados vivem fora deste repo; a fonte-base é lida deles.
