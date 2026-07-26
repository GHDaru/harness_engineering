# Feature Specification: Apêndice — Estudo sobre processos e metodologias de escrita editorial e acadêmica

**Feature Branch**: `010-estudo-metodologias-escrita`

**Created**: 2026-07-26

**Status**: Draft

**Input**: User description: "Apêndice do livro intitulado 'Estudo sobre processos e metodologias de escrita editorial e acadêmica'. Documentar, com evidência, os processos e metodologias de escrita/editoração — tradicionais/consagrados (escrita científica, revisão por pares, guias de estilo, Backward Design, 4C/ID, Diátaxis, carga cognitiva; artigos + material online) e atuais orientados a IA (escrita assistida por LLM, spec-driven writing, pesquisa aumentada por agentes, verificação de fontes, o próprio ciclo spec-kit). Tornar explícito e fundamentado o método com que este livro é escrito, para leitores e contribuidores."

## Clarifications

### Session 2026-07-26

- Q: Qual a profundidade/escopo do "estudo"? → A: **Survey amplo standalone** — um levantamento abrangente das metodologias (muitas escolas/fontes), com o método deste livro incluído como um caso.
- Q: Postura editorial sobre a assistência de IA na escrita? → A: **Equilibrada e crítica** (ganhos + limitações/riscos: alucinação de fontes, integridade acadêmica, reprodutibilidade).
- Q: Divulgar abertamente que ESTE livro foi co-escrito com um agente de IA? → A: **Sim, divulgar abertamente** (co-autoria com agente de IA sob curadoria/responsabilidade humanas, com o processo descrito).
- Q: Onde o texto vive e como se estrutura? → A: **Anexar ao Guia Editorial** — uma nova seção grande dentro de `livro/GUIA-EDITORIAL.md`, não um arquivo novo em `livro/apendices/`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O leitor entende (e pode confiar) no método do livro (Priority: P1)

Um leitor do livro chega ao apêndice querendo saber *como* um livro sobre engenharia de harness foi, ele próprio, escrito — que processo garante que as afirmações têm evidência, que as fontes são reais, e que a mistura de método tradicional e assistência de IA não comprometeu o rigor. Ao ler, ele reconhece o método explícito do livro (fonte-base = código; pesquisa dupla verificada; framework pedagógico; ciclo spec-driven) e passa a poder *avaliar* o livro pelos seus próprios critérios declarados.

**Why this priority**: É o valor central — um livro que ensina disciplina de engenharia precisa expor a própria disciplina de produção, ou contradiz o que ensina (coerência com a cláusula de expiração e o Princípio I). Entregue sozinho, este story já justifica o apêndice.

**Independent Test**: Dar o apêndice a um leitor que não acompanhou a construção e verificar que ele consegue descrever, sem ajuda, os pilares do método do livro e por que cada um existe.

**Acceptance Scenarios**:

1. **Given** um leitor sem contexto da construção, **When** lê a seção sobre o método do livro, **Then** consegue nomear ao menos quatro práticas (evidência-acima-de-retórica, pesquisa dupla verificada, framework pedagógico combinado, spec-driven) e o porquê de cada uma.
2. **Given** o apêndice publicado, **When** o leitor segue qualquer citação de fonte, **Then** a fonte é real e alcançável (ou marcada explicitamente como não-verificada), coerente com a regra "afirmação exige evidência".

---

### User Story 2 - O contribuidor replica o processo para um novo trecho (Priority: P3)

Um futuro contribuidor quer escrever ou revisar um capítulo/apêndice mantendo o padrão do livro. O apêndice lhe dá o processo como um roteiro repetível: da abertura do tema (pesquisa comercial + científica) à escrita no esqueleto, à verificação de fontes, ao gate de build, ao registro no livro vivo — incluindo quando e como usar assistência de IA sem perder autoria e rigor.

**Why this priority**: Transforma o método de tácito em transferível — é o que permite o livro crescer com mais de uma mão sem degradar. Depende do P1 (o método precisa estar descrito) mas agrega o "como fazer".

**Independent Test**: Um contribuidor recebe apenas o apêndice e consegue listar, em ordem, as etapas para levar um capítulo novo ao padrão do livro, e os critérios de aceite de cada etapa.

**Acceptance Scenarios**:

1. **Given** o apêndice, **When** um contribuidor planeja um novo capítulo, **Then** consegue derivar o fluxo (tema → pesquisa dupla → escrita → verificação → build/gate → datação) e os pontos de decisão.
2. **Given** a seção sobre escrita assistida por IA, **When** o contribuidor decide usar um agente de pesquisa, **Then** encontra as salvaguardas explícitas (verificação cruzada, nada de fonte inventada, autoria e responsabilidade humanas).

---

### User Story 3 - O praticante/pesquisador obtém um panorama comparado (tradicional × IA) (Priority: P2)

Alguém interessado em processos de escrita editorial/acadêmica — independentemente deste livro — lê o estudo como um *survey* comparado: as metodologias consagradas (com suas fontes) de um lado, as abordagens atuais orientadas a IA de outro, com as tensões entre elas (rigor, integridade acadêmica, reprodutibilidade, velocidade) tratadas de forma equilibrada.

**Why this priority**: Elevada a P2 pela clarificação de 2026-07-26 (escopo = "survey amplo standalone") — o panorama comparado abrangente passou a ser entregável primário, ao lado do método do livro, à frente da replicação por contribuidores.

**Independent Test**: Um leitor externo consegue, após a leitura, contrastar ao menos duas metodologias tradicionais e duas orientadas a IA, citando fonte para cada e uma tensão entre os dois mundos.

**Acceptance Scenarios**:

1. **Given** o apêndice, **When** o leitor procura o contraste, **Then** encontra metodologias dos dois períodos com fontes reais e uma discussão honesta de limitações/riscos da assistência de IA (incl. integridade acadêmica).

### Edge Cases

- E se uma metodologia relevante **não tiver fonte verificável** (só material de opinião online)? → o apêndice a inclui marcando o status da evidência, nunca a apresentando como consolidada.
- E se uma prática de IA de hoje **expirar** (mudar de dono, ser absorvida pela plataforma)? → o apêndice é datado (livro vivo) e a afirmação fica atrelada à data de captura.
- E se o leitor interpretar o apêndice como endosso de "IA escreve sozinha"? → o texto deve deixar explícito que autoria, julgamento e responsabilidade permanecem humanos.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O apêndice DEVE cobrir metodologias **tradicionais** de escrita científica e editorial, cada uma com ao menos uma fonte real (artigo, livro canônico ou material online) e uma frase sobre *o que ela estabelece* — nunca só o nome.
- **FR-002**: O apêndice DEVE cobrir metodologias/processos **atuais orientados a IA** (escrita assistida por LLM, spec-driven writing, pesquisa aumentada por agentes, verificação de fontes), cada um com fonte real e a mesma regra de tradução.
- **FR-003**: O apêndice DEVE tornar **explícito o método deste livro** — fonte-base = código; pesquisa dupla (indústria + científica) verificada; framework pedagógico combinado (Backward Design + 4C/ID + Diátaxis + carga cognitiva); ciclo spec-driven; livro vivo/datação — ligando cada prática aos princípios da constituição.
- **FR-004**: O apêndice DEVE **contrastar** os dois mundos (tradicional × IA), incluindo uma discussão honesta de riscos/limitações da assistência de IA (integridade acadêmica, alucinação de fontes, reprodutibilidade).
- **FR-005**: Toda afirmação com fonte DEVE seguir a regra do livro: **nenhuma referência inventada**; itens não confirmados marcados explicitamente como tais (coerência com o Princípio I).
- **FR-006**: O estudo DEVE ser incorporado como **uma nova seção grande dentro de `livro/GUIA-EDITORIAL.md`** (já publicado no site como "Guia Editorial"), legível de forma autônoma (survey standalone), com selo/atualização de data (livro vivo) — **não** um arquivo novo em `livro/apendices/`.
- **FR-007**: O estudo DEVE registrar honestamente **lacunas** — onde uma prática carece de literatura consolidada, isso é dito, não preenchido com fonte fraca.
- **FR-008**: A construção DEVE passar pelo **gate de qualidade** do projeto (build sem links internos quebrados) antes de ser considerada pronta.
- **FR-009**: O estudo DEVE **divulgar abertamente** que este livro foi co-escrito com um agente de IA (Claude Code) sob **autoria, curadoria e responsabilidade humanas**, descrevendo o processo real (pesquisa dupla por agentes, verificação cruzada, ciclo spec-driven) — transparência como valor acadêmico.
- **FR-010**: O estudo DEVE ter **abrangência de survey** — cobrir múltiplas escolas/famílias de metodologia (tradicionais e de IA), não apenas as usadas por este livro, organizando-as de forma comparável.

### Key Entities

- **Metodologia**: uma prática de escrita/editoração (nome; período — tradicional ou era-IA; o que estabelece; fonte com status de evidência; quando se aplica).
- **Fonte**: referência que sustenta uma metodologia (título; autor/veículo; URL/DOI; status ✓ validada / ⏳ pendente).
- **Prática do livro**: uma decisão de processo deste livro ligada a um princípio da constituição e a uma metodologia (tradicional e/ou de IA).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Um leitor sem contexto consegue, após ler o apêndice, **nomear ≥4 práticas** do método do livro e o porquê de cada uma (verificável por leitura/entrevista informal).
- **SC-002**: **100% das fontes citadas** no apêndice são reais e alcançáveis ou explicitamente marcadas como não-verificadas — zero referências inventadas.
- **SC-003**: O estudo contrasta, com abrangência de survey, **≥5 metodologias tradicionais e ≥4 orientadas a IA**, organizadas por famílias/escolas, cada uma com fonte.
- **SC-004**: Um contribuidor consegue **derivar o fluxo de produção** de um capítulo (etapas + critérios de aceite) usando só o estudo.
- **SC-005**: O site publica o "Guia Editorial" (com a nova seção) **sem links internos quebrados** (gate de build verde) e a seção aparece na navegação.
- **SC-006**: O estudo declara **explicitamente** a co-autoria humano+IA e o processo, de forma que um leitor identifique quem é responsável pelo conteúdo (verificável por leitura).

## Assumptions

- O estudo é uma **nova seção do `livro/GUIA-EDITORIAL.md`** (Markdown, já publicado como "Guia Editorial"), não um arquivo novo em `apendices/` nem código — o "sistema" aqui é o livro e seu processo editorial. (Ajustado pela clarificação de 2026-07-26.)
- "Estudo" = **survey amplo standalone** (cobre múltiplas escolas/famílias com fontes), não uma nota curta nem só o método do livro; mesmo assim registra lacunas em vez de forçar fontes fracas. (Ajustado pela clarificação de 2026-07-26.)
- O tratamento da assistência de IA é **equilibrado e crítico** (inclui limitações/integridade/reprodutibilidade), refletindo os valores do projeto; não é um manifesto pró-IA.
- A profundidade científica reusa e estende a `bibliografia.md` existente e a skill `academic-research` do projeto.
- Público-alvo: leitores do livro e contribuidores; secundariamente, praticantes de escrita editorial/acadêmica.
