# Benchmark de Harnesses — Metodologia

> **Status: exploratório.** Esta seção nasceu de forma amadora e exploratória — leitura assistida de código, uma rodada, três harnesses — e amadurece a cada iteração. As notas são provisórias e comparáveis apenas dentro da mesma rodada metodológica.

## O que avaliamos

Harnesses de agentes de IA de código aberto, avaliados **por dimensão de engenharia de harness** — as 12 funcionalidades que estruturam os capítulos do livro (`livro/capitulos/`). Não avaliamos qualidade de modelo, popularidade ou UX subjetiva: avaliamos o scaffolding, lendo o código.

## Método

1. **Exploração do código-fonte** — cada repositório é vasculhado sistematicamente (agentes de leitura paralelos, um por repo), dimensão por dimensão.
2. **Evidência obrigatória** — toda afirmação exige o caminho do arquivo onde a funcionalidade está implementada. Sem evidência, não pontua. READMEs prometem; código entrega.
3. **Avaliação padronizada** — o instrumento é o [template HARNESS_EVAL](template/HARNESS_EVAL.md): 12 dimensões, perguntas-chave fixas, nota 0–3.
4. **Consolidação** — as avaliações alimentam o [comparativo](comparativo.md) e os capítulos do livro.

## Escala de notas

| Nota | Significado |
|---|---|
| **0 — Ausente** | A dimensão não existe no código. |
| **1 — Básico** | Existe de forma mínima: uma estratégia única, sem configuração, sem casos de borda. |
| **2 — Sólido** | Implementação completa e configurável; cobre os casos principais. |
| **3 — Referência** | Estado da arte entre os avaliados; é o código que você citaria como exemplo da dimensão. |

Regras de calibração:
- "3" é relativo à coorte avaliada, não a um ideal absoluto — pode ser rebaixado quando um harness melhor entra.
- A nota julga o que **está no código na data da avaliação** (versão/commit registrados nos metadados), não o roadmap.
- Empates são esperados e não devem ser desfeitos artificialmente.

## Avaliações desta rodada

| Harness | Avaliação | Total (0–36) |
|---|---|---|
| gemini-cli | [avaliacoes/gemini-cli.md](avaliacoes/gemini-cli.md) | 36 |
| opencode | [avaliacoes/opencode.md](avaliacoes/opencode.md) | 31 |
| OpenHarness | [avaliacoes/openharness.md](avaliacoes/openharness.md) | 29 |

> O total é um resumo grosseiro — a leitura útil é o **perfil** por dimensão (em que o harness é referência, onde é básico) e o arquétipo. Ver o [comparativo](comparativo.md).

## Fila de avaliação

O benchmark se organiza em **categorias** — harnesses só são ranqueados contra pares do mesmo arquétipo (as notas 0–3 continuam comparáveis; a leitura de "referência" é por categoria).

**Categoria: harnesses de código**
- **Lote 2 (confirmado, aguardando forks):** Codex CLI (OpenAI, Rust — hipótese: novo teto em sandboxing), Goose (Block, Rust — hipótese: novo teto em MCP), Aider (Python — arquétipo context-first: repo-map via tree-sitter), OpenHands (Python — hipótese: novo teto em evals).
- **Lote 3 (candidatos):** Cline ou Roo Code (harness dentro do IDE), SWE-agent / mini-swe-agent (arquétipo pesquisa; harness mínimo), Crush (Go/TUI), smolagents (code-as-action).

**Categoria: agentes pessoais self-hosted** (ver [nota de pesquisa](../estudos/2026-07-24-panorama-agentes-pessoais.md))
- Candidatos: **OpenClaw** (Node.js, MIT, ~329k estrelas), **Hermes Agent** (Nous Research, Python — loop de aprendizado auto-evolutivo de skills), **IronClaw** (NEAR AI, Rust — reimplementação security-first) como ângulo de segurança.
- O **ohmo** (OpenHarness, rodada 1) pertence a esta categoria e será relido contra estes pares.
- Possível 13ª dimensão emergente: "Aprendizado / auto-melhoria" (skills escritas pelo próprio agente).

**Categoria: harnesses embutidos** (o harness dentro de um motor de workflow)
- Candidato: **n8n** (nó AI Agent sobre LangChain JS + MCP Client Tool; fair-code/Sustainable Use License — registrar coluna de licença). A pergunta da categoria não é "quanto scaffolding tem", e sim "o que o ambiente dispensa de scaffolding". Primos: Zapier Agents, Make, Dify, Flowise.

**Fora do benchmark — harnesses fechados** (estudo via documentação, no livro, sem notas por falta de evidência de código): Antigravity (Google), Claude Code (Anthropic), Cursor.

**Watchlist** (a observar antes de virar candidato): HoloDesktop (HCompany), Buzz (Dorsey), Omnigent (Databricks), Kilo Code, metaharness (ruvnet).

## Limitações conhecidas

- Leitura de código por agentes de IA pode errar ou desatualizar; achados relevantes devem ser re-verificados no arquivo citado.
- Uma rodada = uma foto; harnesses ativos mudam rápido (registrar versão/commit é obrigatório).
- A escala 0–3 comprime nuances; o texto da avaliação importa mais que o número.
- Ainda não executamos os harnesses em tarefas padronizadas (benchmark *comportamental*) — hoje o método é estático. É a evolução natural da seção.
