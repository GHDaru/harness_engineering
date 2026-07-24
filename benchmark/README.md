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

## Avaliações realizadas

**Categoria código** (rodadas 1–2):

| Harness | Avaliação | Total (0–36) |
|---|---|---|
| gemini-cli | [avaliacoes/gemini-cli.md](avaliacoes/gemini-cli.md) | 36 |
| Codex CLI | [avaliacoes/codex-cli.md](avaliacoes/codex-cli.md) | 35 |
| Goose | [avaliacoes/goose.md](avaliacoes/goose.md) | 34 |
| opencode | [avaliacoes/opencode.md](avaliacoes/opencode.md) | 31 |
| OpenHarness | [avaliacoes/openharness.md](avaliacoes/openharness.md) | 29 |
| Aider | [avaliacoes/aider.md](avaliacoes/aider.md) | 28 |
| OpenHands (Canvas)* | [avaliacoes/openhands.md](avaliacoes/openhands.md) | 27* |

**Categoria agentes pessoais** (rodada 2; + dims suplementares 13/14):

| Harness | Avaliação | Total (0–36) | Aprendizado | Proatividade |
|---|---|---|---|---|
| OpenClaw | [avaliacoes/openclaw.md](avaliacoes/openclaw.md) | 36 | 1 | 3 |
| Hermes Agent | [avaliacoes/hermes-agent.md](avaliacoes/hermes-agent.md) | 35 | **3** | 2 |
| IronClaw | [avaliacoes/ironclaw.md](avaliacoes/ironclaw.md) | 34 | 2 | 3 |

**Categoria harnesses embutidos** (rodada 2):

| Harness | Avaliação | Total (0–36) |
|---|---|---|
| n8n (nó AI Agent) | [avaliacoes/n8n.md](avaliacoes/n8n.md) | 29 (não comparável aos dedicados) |

\* OpenHands: mede só o control-plane — o núcleo migrou para `software-agent-sdk` (na fila).

> O total é um resumo grosseiro — a leitura útil é o **perfil** por dimensão (em que o harness é referência, onde é básico) e o arquétipo. Ver o [comparativo](comparativo.md).

## Fila de avaliação

O benchmark se organiza em **categorias** — harnesses só são ranqueados contra pares do mesmo arquétipo (as notas 0–3 continuam comparáveis; a leitura de "referência" é por categoria).

**Categoria: harnesses de código**
- ✅ Rodada 2 concluída: Codex CLI (hipótese de sandboxing **confirmada**), Goose (MCP-nativo **confirmado**), Aider (context-first **confirmado**), OpenHands (hipótese de evals **refutada para o repo** — núcleo migrou para SDK).
- **Próximos:** `OpenHands/software-agent-sdk` (o núcleo que faltou), Cline ou Roo Code (IDE), SWE-agent / mini-swe-agent (harness mínimo), Crush (Go/TUI), smolagents (code-as-action).

**Categoria: agentes pessoais self-hosted** (ver [nota de pesquisa](../estudos/2026-07-24-panorama-agentes-pessoais.md))
- ✅ Rodada 2 concluída: OpenClaw (36), Hermes (35 + aprendizado 3), IronClaw (34 + novo paradigma de segurança).
- A **dimensão 13 (Aprendizado)** foi promovida a suplementar do template pela evidência do Hermes; a **14 (Proatividade)** é obrigatória nesta categoria.
- ✅ **Retro dim. 13 na rodada 1 concluída** (2026-07-24): gemini-cli **3** (Auto Memory + skill extraction com inbox humana — segundo design nível 3), OpenHarness 1 (auto-fatos com staleness), opencode 0. Ver capítulo 16.
- **Próximo:** avaliação dedicada do ohmo (em andamento).

**Categoria: harnesses embutidos**
- ✅ n8n avaliado (29/36; tese da categoria confirmada — as dimensões fracas são as que o ambiente dispensa). Primos candidatos: Zapier Agents, Make, Dify, Flowise.

**Categoria: frameworks de harness** (ver [nota de pesquisa](../estudos/2026-07-24-panorama-frameworks.md); template adaptado pronto: [FRAMEWORK_EVAL](template/FRAMEWORK_EVAL.md))
- **Lote frameworks-1 (aguardando forks):** LangGraph (`langchain-ai/langgraph`), OpenAI Agents SDK (`openai/openai-agents-python`), Claude Agent SDK (`anthropics/claude-agent-sdk-python`), CrewAI (`crewAIInc/crewAI`).
- **Lote frameworks-2:** Microsoft Agent Framework, Pydantic AI, Mastra, smolagents.

**Camada de protocolos** (MCP, A2A, ACP, agentskills.io, AGENTS.md): não recebe notas 0–3 — é avaliada por **adoção medida** (matriz no [capítulo 17](../livro/capitulos/17-protocolos.md), extraída das avaliações deste benchmark) e saúde de governança. A matriz é atualizada a cada rodada.

**Fora do benchmark — harnesses fechados** (estudo via documentação, no livro, sem notas por falta de evidência de código): Antigravity (Google), Claude Code (Anthropic), Cursor.

**Watchlist**: HoloDesktop (HCompany), Buzz (Dorsey), Omnigent (Databricks), Kilo Code, metaharness (ruvnet).

## Limitações conhecidas

- Leitura de código por agentes de IA pode errar ou desatualizar; achados relevantes devem ser re-verificados no arquivo citado.
- Uma rodada = uma foto; harnesses ativos mudam rápido (registrar versão/commit é obrigatório).
- A escala 0–3 comprime nuances; o texto da avaliação importa mais que o número.
- Ainda não executamos os harnesses em tarefas padronizadas (benchmark *comportamental*) — hoje o método é estático. É a evolução natural da seção.
