# Contract — Estrutura da seção (o "contrato" desta feature)

> Numa feature de prosa, o contrato não é uma API — é a **estrutura da seção** que será inserida em `livro/GUIA-EDITORIAL.md`. Define as partes obrigatórias e o que cada uma entrega, para que a implementação e a verificação concordem.

## Localização
Nova seção em `livro/GUIA-EDITORIAL.md` (página "Guia Editorial", já publicada), com cabeçalho de atualização de data (livro vivo, Princípio IV).

## Título
`## Estudo: processos e metodologias de escrita editorial e acadêmica (tradicionais e da era-IA)`

## Partes obrigatórias

1. **Abertura / por que este estudo** — o motivo de um livro sobre engenharia expor o próprio método; enquadra o survey e antecipa a divulgação de co-autoria. *(mapeia US1, FR-003)*

2. **Parte A — Metodologias tradicionais** (Diátaxis: *reference*+*explanation*), por família, cada item com fonte e "o que estabelece":
   - estrutura da escrita científica (IMRaD; guias de escrita científica)
   - o processo de escrita como atividade cognitiva (drafting/revisão)
   - craft e estilo (manuais de estilo)
   - craft of research e argumento
   - revisão por pares e fluxo editorial (developmental × copy editing)
   - design instrucional/pedagógico (Backward Design, 4C/ID, Diátaxis, carga cognitiva)
   *(mapeia US3, FR-001, FR-010, SC-003)*

3. **Parte B — Metodologias da era-IA**, por família, cada item com fonte:
   - co-escrita humano-IA
   - spec-driven / structured authoring / docs-as-code
   - pesquisa aumentada por agentes e recuperação (RAG)
   - verificação / proveniência / o problema das citações alucinadas
   - integridade acadêmica e autoria (políticas: LLM não é autor; divulgação)
   *(mapeia US3, FR-002, FR-010, SC-003)*

4. **Parte C — Tensões e síntese (tradicional × IA)** — rigor, integridade, reprodutibilidade, velocidade, homogeneização de estilo; tratamento **equilibrado e crítico**. *(mapeia FR-004, postura da clarificação)*

5. **Parte D — O método deste livro, declarado** — as práticas (fonte-base=código; pesquisa dupla verificada; framework pedagógico combinado; ciclo spec-driven; livro vivo) ligadas aos princípios da constituição, cada uma com sua manifestação no repo; e a **divulgação aberta de co-autoria humano+IA** (Claude Code) sob curadoria e responsabilidade humanas. *(mapeia US1, FR-003, FR-009, SC-001, SC-006)*

6. **Fontes** — ponteiro para a nova subseção de `livro/bibliografia.md`. *(FR-005)*

## Invariantes verificáveis
- Toda metodologia citada tem ≥1 fonte real ou é marcada como lacuna (FR-001/002/005/007).
- ≥5 tradicionais + ≥4 IA, por famílias (FR-010/SC-003).
- A divulgação de co-autoria é explícita (FR-009/SC-006).
- O build publica o Guia Editorial sem links internos quebrados (FR-008/SC-005).
