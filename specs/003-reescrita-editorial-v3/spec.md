# Spec 003 — Reescrita editorial dos capítulos ao esqueleto v3

> Iniciativa de escrita, sob o Princípio VII (spec-driven, branch-per-melhoria). Fonte-base continua sendo o código dos repositórios (Princípio II); método pedagógico combinado (Princípio III); livro vivo com datação (Princípio IV).

## Problema

Cinco capítulos já estão no **esqueleto v3** (02, 03, 04, 05, 07): corpo com o estado da arte sintetizado, fundamentos científicos e fontes da indústria traduzidos em decisões, mão-na-massa do harness-zero, verificação alinhada aos objetivos, e o tratamento por-repositório movido para o **Apêndice A** (complementação online, expandida a cada rodada).

Os demais capítulos de funcionalidade ainda estão em formato pré-v3 (curto, sem objetivos de Bloom, sem seção de indústria, sem Apêndice A, sem selo de datação). Precisam ser trazidos ao mesmo padrão para que o livro seja consistente e pedagogicamente sólido.

## Escopo

Trazer ao esqueleto v3 (na ordem de prioridade), cada capítulo em seu próprio commit rastreável nesta branch:

1. **06 — MCP** (preenche o buraco entre 05 e 07; bibliografia registrada como lacuna a cobrir)
2. **08 — Memória e Estado**
3. **09 — Planejamento**
4. **10 — Subagentes e Orquestração**
5. **11 — Verificação e Evals**
6. **12 — Extensibilidade**
7. **13 — Interfaces**

Fora de escopo nesta iteração: capítulos analíticos (14, 15, 16, 17) e de abertura (00, 01), que seguem estrutura própria; serão tratados em spec posterior.

## Critérios de aceitação (por capítulo)

- [ ] Cabeçalho com **selo de captura** (`> **Estado da arte capturado em AAAA-MM** · última revisão AAAA-MM-DD · [histórico...]`).
- [ ] **Objetivos de aprendizagem** (3–5, verbos de Bloom) mapeados 1:1 à seção **Verificação**.
- [ ] **Fundamentos científicos** — papers reais traduzidos em decisões, com ponteiro para `bibliografia.md`; lacunas acadêmicas registradas honestamente.
- [ ] **Fontes da indústria** — docs de vendor e posts de engenharia reais, com a regra de tradução ("o vendor recomenda X porque Y").
- [ ] **O estado da arte** no corpo — padrões consolidados + o que há de mais moderno; repositórios citados só como exemplos nominais.
- [ ] **Mão na massa** — a etapa correspondente do harness-zero.
- [ ] **Síntese + "o que roubar"**.
- [ ] **Apêndice A** — evidência por repositório com paths, incluindo as rodadas 2/frameworks quando aplicável.
- [ ] `bibliografia.md` atualizada; build do site sem erros (portão de link-check verde).
- [ ] Nenhuma URL inventada; fontes não confirmadas marcadas como tal.

## Não-objetivos

- Não alterar as notas do benchmark (a menos que uma releitura de código justifique — aí vira rodada, não reescrita).
- Não mudar o motor de publicação (isso é o spec 001).
