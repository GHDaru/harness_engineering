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
5. **implement** — implemente e **verifique** percorrendo o [**checklist de verificação**](.specify/memory/checklist-verificacao.md): build verde (4 passos), tradução do delta com selo real, corpus do companion regenerado, nenhum link novo para o repositório (privado), verificação em navegador quando houver UI.
6. **registrar** — atualize `livro/HISTORICO.md` (nova edição + modelo de IA usado) quando a mudança afeta o livro.
7. **merge** — ao concluir e verificar, **merge para a `main`** (`git merge --no-ff NNN-nome`) e push. **O merge na `main` é o que publica** (deploy do Pages nos paths `livro/`, `publicar/`, `benchmark/`); por isso, acumule o trabalho na branch e faça **um** merge por lote.

As skills `/speckit-*` (em `.claude/skills/`) automatizam esses passos; quando não estiverem disponíveis como comando, rode os scripts de `.specify/scripts/bash/` diretamente — o resultado é o mesmo (branch por spec).

**Exceções (Princípio VII):** emendas à constituição e a **este** documento de governança, e correções triviais (typo, link quebrado), podem ir direto à `main`, sempre com commit descritivo.

**Decisões (ADR):** toda decisão relevante (com alternativas e consequências) vira um registro em `adr/` (ver `adr/README.md`): contexto → decisão → alternativas avaliadas → justificativa → consequências. Registra o *porquê*, além do *o quê* (specs/HISTORICO).

## Passada humanizer (obrigatória em conteúdo do livro)

Todo texto novo ou reescrito de **capítulo ou apêndice de conteúdo** passa pela skill `humanizer`
antes de ir para a `main`. A régua e a decisão de escopo estão na spec 105.

- **Aplicadas integralmente**: §1–§13 e §16–§33 (paralelismo negativo, aforismo, *punchline*
  fabricado, autoridade retórica, sinalização, vocabulário-IA, promocional, hedging, conclusão
  genérica, artefato de conversa).
- **Subordinadas à voz do livro**: §14 (travessão) e §15 (negrito). A skill manda cortar todo
  travessão; o `GUIA-EDITORIAL.md` §2.1 diz que em pt-BR ele é pontuação ordinária e o portão
  `mede-prosa.mjs` o limita a **≤8 por 1.000 palavras**. A própria skill dá a precedência:
  *"a sample outranks this skill's style rules, including the em dash rule in §14"* — e o livro com o
  guia é esse *sample*. O mesmo vale para o negrito, que na camada v4 é instrumento didático declarado.
- **Fora do escopo, por decisão do editor**: `livro/HISTORICO.md` (histórico),
  `livro/apendice-estudo.md` (acervo do estudo), `benchmark/**`, o próprio `GUIA-EDITORIAL.md` e as
  **entradas de Radar já publicadas** (acervo).
- **Dentro do escopo desde 2026-08-20, por decisão do editor**: a **entrada diária do Radar**, aplicada
  antes do commit, e **só na prosa de ligação**. Citação verbatim, alvo de link, número, data,
  identificador, o marcador ⏳ e nome próprio ficam intactos. Contrato em `radar/AGENTE.md`.

**Nunca por varredura.** A edição 0.85 registrou que transformação roteirizada degrada prosa de um
jeito que o portão sintático não pega: três rodadas de dano, todas encontradas lendo, nenhuma medindo.
Cada alteração é uma substituição exata decidida na leitura do parágrafo.

E o critério que evita o zelo excessivo: o contraste que **carrega a tese** de um capítulo fica. O que
a §9 combate é a fôrma repetida, não o contraste — no máximo uma ocorrência por capítulo.

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
