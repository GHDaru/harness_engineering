# Feature Specification: Publicação do livro em LaTeX/PDF e HTML navegável

**Feature Branch**: `001-publicacao-latex-html`
**Created**: 2026-07-25
**Status**: Draft (aguarda `/speckit-clarify` → `/speckit-plan`)
**Input**: "Livro em LaTeX; criar HTML para navegação online em formato pedagógico; infra ok, com apêndice explicando a infra do livro."

## Contexto e restrição de fonte

O livro hoje é **Markdown** (`livro/**/*.md`, 21 arquivos). Reescrever à mão em LaTeX seria custoso e frágil (dois formatos a manter em sincronia — viola o anti-apodrecimento da constituição). A abordagem proposta é **fonte única em Markdown → geração automática de LaTeX/PDF e HTML**. Isto preserva o fluxo de escrita atual e entrega os dois artefatos pedidos.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Leitor navega o livro online (Priority: P1)
Um leitor acessa uma URL pública e lê o livro num site com **navegação pedagógica**: sumário lateral, busca, próximo/anterior por capítulo, capítulos e apêndices separados, código com realce, e os "boxes" (objetivos, verificação, mão na massa) visualmente distintos. Cada capítulo mostra sua **data de captura** (livro vivo).
**Why P1**: é o pedido central de acessibilidade (constituição VI) e o formato de maior alcance.
**Teste independente**: gerar o site a partir do Markdown atual e navegar do cap. 02 ao 07, seguir um link do sumário, usar a busca.

### User Story 2 — Leitor/autor gera o PDF via LaTeX (Priority: P2)
O mesmo conteúdo produz um **PDF profissional** via LaTeX (capa, sumário, numeração, referências, código formatado) — o formato de leitura offline/impressão e de arquivo "de registro" de cada edição.
**Why P2**: o pedido explícito de LaTeX; complementa o HTML.
**Teste independente**: compilar o PDF a partir do Markdown atual e conferir sumário, um capítulo com código e a bibliografia.

### User Story 3 — O livro explica a própria infraestrutura (Priority: P3)
Um **apêndice do livro** documenta a infra de publicação (fonte única, toolchain, build, hospedagem) — on-theme: um livro sobre harnesses que explica o próprio "harness de publicação".
**Why P3**: pedido explícito; reforça a coerência (o processo do livro como exemplo).
**Teste independente**: o apêndice existe, descreve o pipeline real e é gerado junto com o resto.

### Edge cases
- Links relativos entre `.md` (ex.: `../HISTORICO.md`) devem funcionar tanto no HTML quanto no repositório GitHub.
- Os **Apêndices A** por capítulo (evidência por repositório) devem render corretamente e caber na navegação sem poluir o fluxo principal.
- Mermaid/diagramas (se houver) e tabelas largas do benchmark precisam scroll/quebra adequada no PDF e no HTML.
- Caracteres em português e blocos de código com `$`/`\` não podem quebrar o LaTeX.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: Fonte única em Markdown; nenhum conteúdo duplicado em `.tex` mantido à mão.
- **FR-002**: Gerar um **site HTML** navegável (sumário, busca, navegação por capítulo) a partir de `livro/`.
- **FR-003**: Gerar um **PDF via LaTeX** com o mesmo conteúdo (capa, TOC, numeração, bibliografia, código).
- **FR-004**: Mapear os elementos pedagógicos (objetivos, verificação, mão na massa, "o que roubar", apêndice) para **callouts/estilos distintos** no HTML e no PDF.
- **FR-005**: Preservar e exibir a **data de captura** de cada capítulo (livro vivo).
- **FR-006**: Um **comando único** reproduz o build local (ex.: `make book` ou script), documentado.
- **FR-007**: Publicar o HTML numa **URL pública** por CI (a cada push no main).
- **FR-008**: Um apêndice do livro descreve a infraestrutura de publicação.
- **FR-009**: O build **falha o CI** se um capítulo não compilar ou se um link interno quebrar (portão de qualidade).

### Decisões a resolver em `/speckit-clarify` (marcadas para o plano)
- **[NEEDS CLARIFICATION] Toolchain**: proposta **Quarto** (single-source → HTML book + PDF via LaTeX, callouts, cross-refs, busca — feito para livros técnicos). Alternativa: Pandoc + template LaTeX próprio + mdBook para HTML (mais controle, mais peça). *Recomendação: Quarto.*
- **[NEEDS CLARIFICATION] Hospedagem**: proposta **GitHub Pages** (estático, sem servidor, grátis, CI simples). Alternativas: Cloudflare Pages, Netlify. *Recomendação: GitHub Pages* — mas o autor abriu espaço para "subir infra"; se quiser algo além de estático (ex.: busca server-side, analytics, versões navegáveis por edição), reavaliar aqui.
- **[NEEDS CLARIFICATION] LaTeX customizado**: usar o template PDF padrão do Quarto ou um `.tex` de classe/estilo próprio (capa e tipografia do livro)? *Recomendação: começar no padrão, evoluir o template numa melhoria futura.*
- **[NEEDS CLARIFICATION] Idioma do build**: garantir hifenização/tipografia PT-BR (babel/polyglossia no LaTeX; lang no HTML).

## Success Criteria *(mandatory)*
- **SC-001**: A partir do Markdown atual, um comando produz **PDF e site HTML** sem edição manual de conteúdo.
- **SC-002**: O site está numa URL pública e navegável (sumário + busca + capítulo-a-capítulo).
- **SC-003**: Os elementos pedagógicos aparecem visualmente distintos nos dois formatos.
- **SC-004**: O CI regenera e publica a cada push no main; quebra de capítulo/link falha o build.
- **SC-005**: O apêndice de infraestrutura existe e descreve o pipeline real.
- **SC-006**: Nenhuma fonte `.tex` de conteúdo mantida à mão (fonte única preservada).

## Fora de escopo (desta melhoria)
- Template LaTeX de tipografia autoral avançada (capa artística, fontes compradas) — melhoria futura.
- Versionamento navegável por edição no site (só a edição corrente é publicada agora; o `HISTORICO.md` registra as demais).
- Tradução do livro para outros idiomas.

## Conformidade com a constituição
- **I/II** (evidência/código): o pipeline não altera conteúdo; só transforma. Preserva paths e citações.
- **III** (pedagógico): os callouts materializam os tipos de texto do Diátaxis no HTML/PDF.
- **IV** (livro vivo): a data de captura é exibida; cada edição pode arquivar seu PDF.
- **VII** (spec-driven): esta é a primeira melhoria sob o novo regime — spec nesta branch, `plan`/`tasks`/`implement` a seguir.
