# Engenharia de Harness — O Livro

> Um livro aberto, em português, sobre a disciplina de construir o *scaffolding* que envolve agentes de IA — escrito a partir do estudo sistemático de harnesses de código aberto reais.

## O que é este repositório

Este é o repositório oficial de escrita do projeto. Todos os estudos, análises de código, avaliações e comparativos são reportados aqui, e o conjunto forma um livro sobre **engenharia de harness**: a disciplina de projetar entrega de contexto, interfaces de ferramentas, artefatos de planejamento, loops de verificação, sistemas de memória e sandboxes que determinam se um agente de IA tem sucesso ou falha em tarefas reais.

O método do livro é empírico: em vez de teorizar no abstrato, lemos o código-fonte de harnesses reais (opencode, gemini-cli, OpenHarness, e outros por vir) e extraímos os padrões, as convergências e as divergências de implementação.

## Estrutura

### O Livro (`livro/`)

| Parte | Conteúdo |
|---|---|
| [00 — Introdução](livro/00-introducao.md) | O que é um harness, por que a disciplina existe, método do livro |
| [01 — Fundamentos](livro/01-fundamentos.md) | Definições, teoria, artigos canônicos, taxonomia por problema |
| **Capítulos por funcionalidade** | |
| [02 — Loop do Agente](livro/capitulos/02-loop-do-agente.md) | O ciclo prompt → decisão → ferramenta → resultado |
| [03 — Entrega de Contexto](livro/capitulos/03-entrega-de-contexto.md) | System prompts, arquivos de regras, montagem hierárquica |
| [04 — Compactação](livro/capitulos/04-compactacao.md) | Gestão da janela de contexto: prune, sumarização, truncamento |
| [05 — Design de Ferramentas](livro/capitulos/05-ferramentas.md) | Tools built-in, schemas, seleção por modelo |
| [06 — MCP](livro/capitulos/06-mcp.md) | Model Context Protocol: transportes, OAuth, descoberta |
| [07 — Permissões e Sandboxing](livro/capitulos/07-permissoes-sandbox.md) | Modos de aprovação, policy engines, sandbox de SO |
| [08 — Memória e Estado](livro/capitulos/08-memoria-estado.md) | Sessões, persistência, memória de longo prazo, checkpointing |
| [09 — Planejamento](livro/capitulos/09-planejamento.md) | Plan mode, todo lists, decomposição de tarefas |
| [10 — Subagentes e Orquestração](livro/capitulos/10-subagentes-orquestracao.md) | Delegação, isolamento, times, protocolos (A2A) |
| [11 — Verificação e Evals](livro/capitulos/11-verificacao-evals.md) | Testes do harness, evals comportamentais, LSP em runtime |
| [12 — Extensibilidade](livro/capitulos/12-extensibilidade.md) | Hooks, plugins, skills, provedores de modelo |
| [13 — Interfaces](livro/capitulos/13-interfaces.md) | TUI, headless, IDE, CI, chat |
| [14 — Convergências e Tendências](livro/14-convergencias.md) | O que a indústria já padronizou e a "cláusula de expiração" |
| [15 — O Harness Embutido](livro/capitulos/15-harness-embutido.md) | Agentes dentro de motores de workflow (n8n): o harness invertido |
| [16 — Aprendizado e Auto-melhoria](livro/capitulos/16-aprendizado-auto-evolutivo.md) | O harness que se escreve: dois designs nível 3 (Hermes autônomo × gemini-cli inbox) |
| [17 — A Camada de Protocolos](livro/capitulos/17-protocolos.md) | MCP, A2A, ACP, agentskills.io, AGENTS.md — com matriz de adoção medida no código |
| [Bibliografia](livro/bibliografia.md) | Referências científicas por capítulo, com status de validação |
| [Histórico](livro/HISTORICO.md) | Livro vivo: edições datadas, snapshot por capítulo e o **registro de expiração** (placar das previsões) |

### A Construção (`harness-zero/`)

Trilha prática do livro: um harness completo construído do zero, uma etapa por capítulo (Python + FastAPI + chat mínimo), com arquitetura hexagonal **por refatoração** e DDD leve. Método pedagógico: Backward Design + 4C/ID + Diátaxis + Carga Cognitiva (ver [parecer editorial](estudos/2026-07-25-parecer-editorial-plano-pedagogico.md)). Etapas 0 (chat + porta LLM) e 1 (o loop) prontas e testadas — [mapa completo](harness-zero/README.md).

### O Benchmark (`benchmark/`)

Seção empírica do livro: avaliação padronizada de harnesses de código aberto, por dimensão, com escala 0–3 e exigência de evidência no código-fonte.

- [Metodologia](benchmark/README.md) — escala, regras de evidência, categorias, fila
- [Template de avaliação](benchmark/template/HARNESS_EVAL.md) — 12 dimensões + 2 suplementares
- [Comparativo consolidado](benchmark/comparativo.md) — tabelas por categoria, campeões por dimensão, achados transversais
- Avaliações — **código**: [gemini-cli](benchmark/avaliacoes/gemini-cli.md) (36) · [Codex CLI](benchmark/avaliacoes/codex-cli.md) (35) · [Goose](benchmark/avaliacoes/goose.md) (34) · [opencode](benchmark/avaliacoes/opencode.md) (31) · [OpenHarness](benchmark/avaliacoes/openharness.md) (29) · [Aider](benchmark/avaliacoes/aider.md) (28) · [OpenHands](benchmark/avaliacoes/openhands.md) (27*) — **agentes pessoais**: [OpenClaw](benchmark/avaliacoes/openclaw.md) (36) · [Hermes](benchmark/avaliacoes/hermes-agent.md) (35) · [IronClaw](benchmark/avaliacoes/ironclaw.md) (34) — **embutidos**: [n8n](benchmark/avaliacoes/n8n.md) (29)

> **Status**: exploratório, rodada 2 concluída (11 harnesses, 3 categorias). Notas provisórias, por leitura assistida de código com evidência por arquivo.

## Harnesses estudados até agora

| Harness | Stack | Categoria / arquétipo |
|---|---|---|
| [gemini-cli](https://github.com/google-gemini/gemini-cli) | TypeScript | Código — controle e verificação |
| [Codex CLI](https://github.com/openai/codex) | Rust (97 crates) | Código — contenção de SO em 3 camadas |
| [Goose](https://github.com/block/goose) | Rust | Código — MCP-nativo |
| [opencode](https://github.com/anomalyco/opencode) | TypeScript + Effect-TS | Código — arquitetura de contexto/estado |
| [OpenHarness](https://github.com/HKUDS/OpenHarness) | Python | Código — port didático + swarm |
| [Aider](https://github.com/Aider-AI/aider) | Python | Código — context-first (repo-map) |
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) | Python + React | Código — control-plane multi-harness |
| [OpenClaw](https://github.com/openclaw/openclaw) | Node.js/TS | Pessoal — plataforma completa (23 canais) |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Python | Pessoal — aprendizado auto-evolutivo |
| [IronClaw](https://github.com/nearai/ironclaw) | Rust (63 crates) | Pessoal — kernel de autoridade zero-trust |
| [n8n](https://github.com/n8n-io/n8n) (nó AI Agent) | TypeScript/LangChain | Embutido — o harness invertido |

Referencial teórico: [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) (~426 recursos curados, taxonomia por problema).

## Ferramentas (`scripts/`)

- [`sync-forks.ps1`](scripts/sync-forks.ps1) — script PowerShell para rodar **localmente** e manter todos os forks do projeto sincronizados com seus upstreams (clona se faltar, `fetch upstream` + merge fast-forward-only + push para o fork). Uso: `.\scripts\sync-forks.ps1` (opções: `-BaseDir`, `-Only repo1,repo2`, `-NoPush`). O merge é ff-only de propósito: commits locais divergentes geram aviso, nunca sobrescrita.

## Como contribuir

O livro cresce por estudo: cada novo harness avaliado alimenta os capítulos com novos padrões de implementação. Avaliações seguem o [template](benchmark/template/HARNESS_EVAL.md) — afirmações sobre um harness exigem evidência (caminho de arquivo no código-fonte).

## Como citar

Esta obra é um **livro vivo**: cada edição é datada e versionada. O registro de DOI (via [Zenodo](https://zenodo.org)/DataCite) segue o mesmo modelo — um **concept DOI** para a obra como um todo (sempre a versão mais recente) e um **DOI de versão** para cada edição.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21632412.svg)](https://doi.org/10.5281/zenodo.21632412)

Cite assim (o GitHub também mostra um botão **"Cite this repository"** a partir do [`CITATION.cff`](CITATION.cff)):

> Darú, Gilsiley Henrique. *Engenharia de Harness — Um livro vivo sobre o scaffolding que envolve agentes de IA*. 2026. https://doi.org/10.5281/zenodo.21632412

Autoria e método: obra co-produzida por humano e IA, sob responsabilidade e curadoria humanas; o autor (creator) é Gilsiley Henrique Darú ([ORCID 0000-0002-8979-0461](https://orcid.org/0000-0002-8979-0461)) e a assistência de IA é declarada abertamente (Guia Editorial §6), sem figurar como autora (ICMJE/COPE).

## Licença

Licenciamento **duplo**, por natureza da obra:

- **Conteúdo** (texto do livro, figuras, material editorial em `livro/`, `benchmark/`, `estudos/` e páginas do site): **[CC BY 4.0](LICENSE)** — reuso livre, inclusive comercial, com atribuição.
- **Código** (software em `harness-zero/`, `publicar/`, `chat-companion/`): **[MIT](LICENSE-CODE)**.
