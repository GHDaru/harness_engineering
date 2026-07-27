# Parecer — achados acionáveis do estudo de metodologias de escrita (Guia §6)

> **Registro, não regra.** Documento de decisão rastreável (gênero `estudos/`). Os itens abaixo só se tornam **oficiais/vinculantes** quando viram regra na constituição (`.specify/memory/constitution.md`) e/ou no `GUIA-EDITORIAL.md`, via ciclo spec-kit (Princípio VII) — emendas à constituição podem ir direto ao main, mas registradas no `HISTORICO.md`. Data: 2026-07-26. Fonte: Guia Editorial §6 + `specs/010-estudo-metodologias-escrita/research.md`.

## Reforços (o survey confirmou práticas já vigentes — não exigem mudança)

- **Verificação de fontes é controle obrigatório, não zelo.** Walters & Wilder (55% de citações fabricadas no GPT-3.5; 18% no GPT-4) e Liu et al. (só 51,5% das afirmações de busca generativa suportadas) dão a base empírica do Princípio I e da "pesquisa dupla verificada por busca cruzada". Manter o marcador `⏳` e a proibição de fonte inventada.
- **Esqueleto v3 = convenção decantada legítima.** Sollaci & Pereira (IMRaD "imposto por decantação") e Gopen & Swan (o sentido nasce da posição estrutural) validam o v3 e dão alavanca de revisão (topic/stress positions).

## Ações propostas (mudam a próxima edição — pendentes de ratificação)

| # | Achado (fonte) | Mudança proposta | Casa oficial |
|---|---|---|---|
| **A1** | Autoria: LLM não pode ser autor; uso deve ser divulgado (ICMJE/COPE/Nature/Science) | **Divulgar a co-autoria humano+IA na abertura do livro** (cap. 00 e/ou colofão), não só no Guia §6.D | Conteúdo (cap. 00) → **spec-kit feature** |
| **A2** | "Escrever é reescrever"; revisão = re-ver o sentido (Sommers; Flower & Hayes) | Adicionar um **passo explícito de revisão *developmental*** (reestruturar), distinto do copyedit, ao fluxo de produção | Regra → **Guia §6.E** + possível **gate na constituição** |
| **A3** | Reprodutibilidade / não-determinismo de LLM (Thinking Machines) | **Registrar a versão do modelo** (e a sessão) nas entradas de edição | Regra de datação → **constituição (IV)** + **HISTORICO** |

## Vigilâncias (não são regra, são cuidado editorial recorrente)

- **Persuasão latente** (Jakesch): a opinião do modelo pode vazar como tese do livro → o humano possui o argumento (Toulmin); reforça a neutralidade (Princípio VI).
- **Homogeneização / cognitive debt** (2402.01536; Kosmyna): usar IA para pesquisar/estruturar, não para gerar prosa final sem revisão; preservar a voz.

## Encaminhamento sugerido

1. **A3** (logar versão do modelo) e **A2** (gate de revisão) são regras de método/governança → **emenda de constituição v1.2.0** (direto ao main + HISTORICO) + ajuste no Guia.
2. **A1** (divulgação na abertura) é conteúdo do livro → **feature spec-kit** própria (`/speckit-specify …`).
3. As vigilâncias entram como uma nota no Guia §6.C (já parcialmente lá), sem virar gate.
