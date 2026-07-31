# Apêndice — O estudo: harnesses avaliados

Este apêndice **mostra o trabalho executado**: a lista completa dos harnesses que passaram pelo estudo, com **de onde vieram** (repositório de origem), **a foto exata que foi lida** (fork/commit/snapshot — a materialização da data de corte do método, cap. 01 §6) e o link para a **avaliação completa** de cada um. O instrumento usado em todas as avaliações é o mesmo: o template [`HARNESS_EVAL.md`](../benchmark/template/HARNESS_EVAL.md) (e [`FRAMEWORK_EVAL.md`](../benchmark/template/FRAMEWORK_EVAL.md) para frameworks), aplicado por leitura sistemática de código conforme a [metodologia do benchmark](../benchmark/README.md).

## Como ler esta tabela

- **Origem**: o repositório upstream público.
- **Versão/snapshot**: a versão ou o snapshot lido.
- **Fork/commit (data de corte)**: a foto congelada no fork `GHDaru/*` — é o que garante **reprodutibilidade** (qualquer pessoa pode ler o mesmo commit) e materializa a mitigação de obsolescência do método. Os forks são sincronizados pelo script [`scripts/sync-forks.ps1`](../scripts/sync-forks.ps1).
- **Avaliação**: o documento completo (metadados, notas por dimensão com evidência de código, diagnóstico e "o que roubar").

## Os 16 avaliados

| Harness | Categoria | Origem | Versão/snapshot | Fork/commit lido | Avaliado em | Análise |
|---|---|---|---|---|---|---|
| **Aider** | harnesses de código | [github.com/Aider-AI/aider](https://github.com/Aider-AI/aider) | snapshot 2026-07 | fork GHDaru/aider, commit 5dc9490 | 2026-07-24 (rodada 2) | [avaliação](../benchmark/avaliacoes/aider.md) |
| **Codex CLI (OpenAI)** | harnesses de código | [github.com/openai/codex](https://github.com/openai/codex) | snapshot 2026-07 | fork GHDaru/codex, commit 000d254 | 2026-07-24 (rodada 2) | [avaliação](../benchmark/avaliacoes/codex-cli.md) |
| **gemini-cli** | harnesses de código | [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | snapshot 2026-07 (main) | — | 2026-07-24 (rodada 1, exploratória) | [avaliação](../benchmark/avaliacoes/gemini-cli.md) |
| **Goose (Block / AAIF)** | harnesses de código | [github.com/block/goose](https://github.com/block/goose) | v1.44.0 | fork GHDaru/goose, commit 0038bc7 | 2026-07-24 (rodada 2) | [avaliação](../benchmark/avaliacoes/goose.md) |
| **opencode** | harnesses de código | [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode) | v1.18.4 (V2 em transição, documentada em `CONTEXT.md`) | — | 2026-07-24 (rodada 1, exploratória) | [avaliação](../benchmark/avaliacoes/opencode.md) |
| **OpenHands (Agent Canvas)** | harnesses de código | [github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) | snapshot 2026-07 | fork GHDaru/OpenHands, commit 6b04532 | 2026-07-24 (rodada 2) | [avaliação](../benchmark/avaliacoes/openhands.md) |
| **OpenHarness** | harnesses de código | [github.com/HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) | v0.1.9 | — | 2026-07-24 (rodada 1, exploratória) | [avaliação](../benchmark/avaliacoes/openharness.md) |
| **Hermes Agent (Nous Research)** | agentes pessoais self-hosted | [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | snapshot 2026-07 | fork GHDaru/hermes-agent, commit 55ef425 | 2026-07-24 (rodada 2) | [avaliação](../benchmark/avaliacoes/hermes-agent.md) |
| **IronClaw (NEAR AI)** | agentes pessoais self-hosted | [github.com/nearai/ironclaw](https://github.com/nearai/ironclaw) | snapshot 2026-07 | fork GHDaru/ironclaw, commit 073ded0 | 2026-07-24 (rodada 2) | [avaliação](../benchmark/avaliacoes/ironclaw.md) |
| **ohmo (OpenHarness)** | agentes pessoais self-hosted | [github.com/HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) (diretório `ohmo/`) | v0.1.9 — avaliação dedicada, complementar à do OpenHarness (rodada 1) | — | 2026-07 | [avaliação](../benchmark/avaliacoes/ohmo.md) |
| **OpenClaw** | agentes pessoais self-hosted | [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) | snapshot 2026-07 | fork GHDaru/openclaw, commit 1e15b18b | 2026-07-24 (rodada 2) | [avaliação](../benchmark/avaliacoes/openclaw.md) |
| **n8n (nó AI Agent)** | harnesses embutidos | [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n) | snapshot 2026-07; pacote avaliado: `packages/@n8n/nodes-langchain` v2.32.0 (135 nós de IA) | fork GHDaru/n8n, commit 55e92cc2 | 2026-07-24 (rodada 2) | [avaliação](../benchmark/avaliacoes/n8n.md) |
| **CrewAI** | frameworks | [github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | v1.15.6 — monorepo com 6 pacotes (`crewai`, `crewai-core`, `crewai-tools` ~79 tools, `cli`, `crewai-files`, `devtools`) | fork GHDaru, commit b3aaaab | 2026-07 | [avaliação](../benchmark/avaliacoes/crewai.md) |
| **LangGraph** | frameworks | [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | langgraph 1.2.9 — monorepo: core (~28k LOC), prebuilt, checkpoint (+postgres/sqlite/conformance), cli, sdk-py; **~63k LOC de testes (2,3× o código)** | fork GHDaru, commit 1e1ca88 | 2026-07 | [avaliação](../benchmark/avaliacoes/langgraph.md) |
| **OpenAI Agents SDK** | frameworks | [github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python) | v0.18.3 | fork GHDaru, commit 5976333 | 2026-07 | [avaliação](../benchmark/avaliacoes/openai-agents-sdk.md) |
| **Software Agent SDK (OpenHands)** | frameworks | [github.com/OpenHands/software-agent-sdk](https://github.com/OpenHands/software-agent-sdk) | v1.37.1 | fork GHDaru, commit 99342c4 | 2026-07 | [avaliação](../benchmark/avaliacoes/software-agent-sdk.md) |

## Extensão ext-1 (2026-07-31): a primeira promoção Radar→corpus

O corpus cresceu de 16 para **18** pelo caminho que o próprio livro institucionalizou: o [Radar diário](https://github.com/GHDaru/harness_engineering/blob/main/radar/RADAR.md) encontrou os candidatos (varredura de 2026-07-31), o editor aprovou a promoção, os repositórios foram forkados para leitura congelada e o mesmo instrumento (`HARNESS_EVAL.md`) foi aplicado — rodada **ext-1**, sem tocar as fotos das rodadas 1/2. Ambos passam o teste de inclusão do cap. 01 §4 (código aberto + harness de propósito geral + adoção/representatividade): o Grok Build pela abertura de um harness comercial completo; o Pi como **caso deliberadamente atípico** (a lógica de replicação de Yin pedia um contraponto minimalista, e faltava um no corpus).

| Harness | Categoria | Origem | Versão/snapshot | Fork/commit lido | Avaliado em | Análise |
|---|---|---|---|---|---|---|
| **Grok Build (xAI)** | harnesses de código | [github.com/xai-org/grok-build](https://github.com/xai-org/grok-build) | snapshot 2026-07 (aberto em 2026-07-15, Apache 2.0) | fork GHDaru/grok-build, commit dd04f39 | 2026-07-31 (rodada ext-1) | [avaliação](../benchmark/avaliacoes/grok-build.md) |
| **Pi (Earendil Labs)** | harnesses de código | [github.com/badlogic/pi-mono](https://github.com/badlogic/pi-mono) | snapshot 2026-07-31 | fork GHDaru/pi, commit 7846534 | 2026-07-31 (rodada ext-1) | [avaliação](../benchmark/avaliacoes/pi.md) |

## Diagnóstico consolidado

Os **resultados por dimensão** (notas 0–3, com evidência) e o diagnóstico comparativo estão no [Comparativo dos Harnesses](../benchmark/comparativo.md) — incluindo o heatmap interativo. Cada avaliação individual traz, além das notas: o **arquétipo observado** do harness, os pontos fortes com caminhos de arquivo, e a seção **"o que roubar"** (padrões que merecem ser levados para outros harnesses).

> **Nota de método** (cap. 01 §6): a seleção seguiu lógica de replicação (Yin) — casos representativos *e* deliberadamente atípicos; a unidade de análise é o código-fonte; as notas seguem a grade fixa do template (feature analysis, DESMET). O placar de expiração das previsões está no [Histórico](HISTORICO.md).

---

> **Consulte também**: implementações de referência além das avaliadas aqui estão catalogadas em [Awesome Harness Engineering — Reference Implementations](https://github.com/GHDaru/awesome-harness-engineering#reference-implementations).
