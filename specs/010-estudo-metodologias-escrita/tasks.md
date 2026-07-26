# Tasks: Estudo sobre processos e metodologias de escrita editorial e acadêmica

**Feature**: `010-estudo-metodologias-escrita` | **Input**: spec.md, plan.md, research.md, data-model.md, contracts/outline.md, quickstart.md

**Tests**: não solicitados (feature de documentação; o "teste" é o gate de build/link-check + revisão editorial). Nenhuma tarefa de teste automatizado gerada.

**Organização**: por user story (US1=P1, US3=P2, US2=P3), cada fase um incremento entregável.

---

## Phase 1: Setup

- [ ] T001 Criar a subseção de fontes "Cap. Guia — Metodologias de escrita" em `livro/bibliografia.md` (cabeçalho + nota de escopo), pronta para receber as referências tradicionais e de IA do `research.md`.

## Phase 2: Foundational (bloqueia as user stories)

- [ ] T002 Inserir em `livro/GUIA-EDITORIAL.md` o esqueleto da nova seção `## Estudo: processos e metodologias de escrita editorial e acadêmica (tradicionais e da era-IA)` com as 6 partes da `contracts/outline.md` como subtítulos vazios + linha de atualização de data (livro vivo).
- [ ] T003 Escrever a Parte 1 (Abertura / por que este estudo) em `livro/GUIA-EDITORIAL.md`, enquadrando o survey e antecipando a divulgação de co-autoria.

## Phase 3: User Story 1 — O leitor entende (e confia) no método do livro (P1) 🎯 MVP

**Goal**: o leitor nomeia ≥4 práticas do método do livro e reconhece a co-autoria humano+IA.
**Independent test**: dar só a Parte D a um leitor sem contexto e verificar SC-001/SC-006.

- [ ] T004 [US1] Escrever a **Parte D — O método deste livro, declarado** em `livro/GUIA-EDITORIAL.md`: as práticas (fonte-base=código; pesquisa dupla verificada; framework pedagógico combinado; ciclo spec-driven; livro vivo) ligadas aos princípios I–VII, cada uma com sua manifestação real no repo (`specs/`, `HISTORICO.md`, commits).
- [ ] T005 [US1] Acrescentar à Parte D a **divulgação aberta de co-autoria humano+IA** (Claude Code) sob curadoria e responsabilidade humanas (FR-009/SC-006), citando as políticas de autoria (ICMJE/COPE/Nature/Science) do `research.md`.

**Checkpoint**: US1 entregue — o método do livro está explícito e a autoria divulgada.

## Phase 4: User Story 3 — Panorama comparado tradicional × IA (P2)

**Goal**: survey amplo com ≥5 metodologias tradicionais e ≥4 de IA, por famílias, com fontes.
**Independent test**: SC-003 (contagem por família) + SC-002 (fontes reais/marcadas).

- [ ] T006 [P] [US3] Escrever a **Parte A — Metodologias tradicionais** em `livro/GUIA-EDITORIAL.md` (6 famílias do `research.md`: estrutura científica/IMRaD; processo cognitivo; craft/estilo; craft of research/argumento; peer review/editoração; design instrucional), cada item com "o que estabelece" + fonte.
- [ ] T007 [P] [US3] Escrever a **Parte B — Metodologias da era-IA** em `livro/GUIA-EDITORIAL.md` (6 famílias: co-escrita; spec-driven/structured authoring; pesquisa aumentada por agentes; verificação/proveniência; integridade/autoria; críticas), cada item com fonte.
- [ ] T008 [US3] Escrever a **Parte C — Tensões e síntese (tradicional × IA)** em `livro/GUIA-EDITORIAL.md`: rigor, integridade, reprodutibilidade, velocidade, homogeneização — tratamento equilibrado/crítico usando as fontes de cautela (Walters & Wilder, Liu, Jakesch, homogenização, cognitive debt).
- [ ] T009 [US3] Registrar as fontes de A e B na subseção de `livro/bibliografia.md` (T001), com status ✓/⏳ conforme o `research.md`.

**Checkpoint**: US1 + US3 entregues — método do livro + survey comparado completos.

## Phase 5: User Story 2 — O contribuidor replica o processo (P3)

**Goal**: um contribuidor deriva o fluxo de produção de um capítulo a partir do texto.
**Independent test**: SC-004 (derivar etapas + critérios de aceite).

- [ ] T010 [US2] Acrescentar à Parte D (ou como Parte E curta) em `livro/GUIA-EDITORIAL.md` o **fluxo repetível** para um novo capítulo/seção: tema → pesquisa dupla verificada → escrita (esqueleto/Diátaxis) → verificação de fontes → gate de build → datação; com as salvaguardas de uso de IA (verificação cruzada, nada de fonte inventada, autoria humana).

**Checkpoint**: as três user stories entregues.

## Phase 6: Polish & Cross-Cutting

- [ ] T011 Registrar a edição no `livro/HISTORICO.md` (nova entrada; livro vivo — Princípio IV) mencionando a seção nova do Guia Editorial.
- [ ] T012 Rodar o gate: `cd publicar && node build.mjs` — link-check verde; a seção aparece no `guia-editorial.html`. Corrigir qualquer link quebrado (FR-008/SC-005).
- [ ] T013 Verificação final contra a `quickstart.md` (SC-001..SC-006) e revisão de coerência (Diátaxis: não misturar tipos; termos técnicos sem tradução).

---

## Dependencies

- Setup (T001) → Foundational (T002–T003) → user stories.
- **US1 (T004–T005)** é o MVP; independe de US3/US2.
- **US3 (T006–T009)**: T006 e T007 são paralelizáveis [P] (partes distintas do texto); T008 depende de T006+T007; T009 registra as fontes usadas.
- **US2 (T010)** reusa o método já descrito na Parte D (depende de T004).
- Polish (T011–T013) por último.

## Parallel opportunities

- T006 [P] e T007 [P] podem ser escritas em paralelo (Parte A × Parte B, seções distintas do mesmo arquivo — coordenar a inserção).

## Implementation strategy

MVP = **US1** (Parte D + divulgação de autoria): já entrega o valor central (o leitor entende e confia no método). Incrementos: + US3 (survey comparado) → + US2 (fluxo para contribuidores) → Polish (HISTORICO + build + verificação).
