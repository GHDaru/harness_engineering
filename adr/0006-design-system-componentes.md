# 0006 — Design system: entregáveis da metodologia como componentes de tela

- **Status:** Aceito (catálogo em aprovação com o autor)
- **Data:** 2026-07-28
- **Contexto (feature/spec):** `043-template-capitulos`

## Contexto
Ao desenhar o template visual dos capítulos, o autor observou que cada capítulo tem um conjunto de **entregáveis definidos pela metodologia** (esqueleto v3: objetivos, problema, fundamentos, fontes, estado da arte, leitura executiva, mão na massa, verificação, apêndice A; mais datação, figuras, siglas, citações). A pergunta de arquitetura: o template é um bloco monolítico de CSS, ou uma **composição de componentes** onde cada entregável vira um objeto de tela nomeado — com um local canônico de definição e um registro do racional?

## Decisão
**Decompor em componentes**: cada entregável da metodologia ↔ um componente de tela nomeado (C01–C12 + infraestrutura N01–N05), catalogado em **`publicar/DESIGN-SISTEMA.md`** (o local da definição: origem metodológica, anatomia, gatilho no motor, classes, variantes, status). A página do capítulo é uma **composição** declarada ("regras de composição"). O motor reconhece os entregáveis por **convenção de conteúdo** (títulos de seção, blockquote de data, `sumario.json`) — os `.md` nunca carregam HTML de apresentação. Decisões visuais com alternativas relevantes passam por **gate humano** (mockups) e viram ADR.

## Alternativas avaliadas
- **A — Template monolítico (CSS da página como um bloco)**: mais rápido de fazer uma vez. Contras: sem rastreabilidade entregável→tela; mudanças pontuais viram arqueologia de CSS; sem lugar para dizer "por quê".
- **B — HTML de apresentação nos capítulos (.md)**: controle fino por página. Contras: viola a separação conteúdo×apresentação; 18 arquivos para cada mudança; conteúdo poluído — rejeitada de pronto.
- **C — Adotar um framework de docs (Docusaurus/VitePress) com theme components**: componentes ganhos "de graça". Contras: abandona o motor próprio (que é parte da tese do livro — app próprio, não framework), migração cara, perde os componentes já feitos (callouts, viz, abbr, companion).
- **D — Design system próprio, leve, sobre o motor existente (escolhida)**: cataloga o que JÁ existe (callouts, selo, figura, viz, abbr, cita) + os novos (C01 cabeçalho, C08 leitura executiva, N02 paginação em cartões), com governança (spec-kit + gate humano + ADR).

## Justificativa
D preserva o motor-tese, dá nome e endereço a cada objeto de tela (manutenção e conversa de design ficam precisas: "ajustar o C01" em vez de "aquele header"), amarra a tela à metodologia (rastreabilidade pedagógica — cada componente cita o entregável que materializa) e cria o processo de evolução (catálogo + gate + ADR). O custo é manter um documento a mais — pequeno, e ele é o próprio artefato de governança que faltava.

## Consequências
- Positivas: vocabulário compartilhado autor↔agente; visual muda no motor sem tocar conteúdo; auditável (status por componente); o livro pratica o que ensina (contrato estável + composição — a mesma lição das portas do harness-zero).
- Custos: disciplina de atualizar o catálogo a cada componente novo; ADRs adicionais para decisões visuais.
- Reversibilidade: alta (o catálogo é documentação; o CSS continua no mesmo lugar).
