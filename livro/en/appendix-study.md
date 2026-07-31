<!-- i18n fonte:livro/apendice-estudo.md edicao:0.61 hash:bfa30c3b -->
# Appendix — The study: the harnesses evaluated

This appendix **shows the work**: the full list of harnesses that went through the study, with **where they came from** (upstream repository), **the exact snapshot that was read** (fork/commit/snapshot — the materialization of the method's cutoff date, ch. 01 §6) and the link to the **complete evaluation** of each one. The instrument used in every evaluation is the same: the [`HARNESS_EVAL.md`](https://github.com/GHDaru/harness_engineering/blob/main/benchmark/template/HARNESS_EVAL.md) template (and [`FRAMEWORK_EVAL.md`](https://github.com/GHDaru/harness_engineering/blob/main/benchmark/template/FRAMEWORK_EVAL.md) for frameworks), applied through systematic code reading following the [benchmark methodology](https://github.com/GHDaru/harness_engineering/blob/main/benchmark/README.md) (in Portuguese).

## How to read this table

- **Origin**: the public upstream repository.
- **Version/snapshot**: the version or snapshot that was read.
- **Fork/commit (cutoff date)**: the picture frozen in the `GHDaru/*` fork — this is what guarantees **reproducibility** (anyone can read the same commit) and materializes the method's obsolescence mitigation. The forks are synchronized by the [`scripts/sync-forks.ps1`](https://github.com/GHDaru/harness_engineering/blob/main/scripts/sync-forks.ps1) script.
- **Evaluation**: the complete document (metadata, per-dimension scores with code evidence, diagnosis and "what to steal").

## The 16 evaluated

| Harness | Category | Origin | Version/snapshot | Fork/commit read | Evaluated on | Analysis |
|---|---|---|---|---|---|---|
| **Aider** | coding harnesses | [github.com/Aider-AI/aider](https://github.com/Aider-AI/aider) | snapshot 2026-07 | fork GHDaru/aider, commit 5dc9490 | 2026-07-24 (round 2) | [evaluation](../../benchmark/avaliacoes/aider.html) |
| **Codex CLI (OpenAI)** | coding harnesses | [github.com/openai/codex](https://github.com/openai/codex) | snapshot 2026-07 | fork GHDaru/codex, commit 000d254 | 2026-07-24 (round 2) | [evaluation](../../benchmark/avaliacoes/codex-cli.html) |
| **gemini-cli** | coding harnesses | [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | snapshot 2026-07 (main) | — | 2026-07-24 (round 1, exploratory) | [evaluation](../../benchmark/avaliacoes/gemini-cli.html) |
| **Goose (Block / AAIF)** | coding harnesses | [github.com/block/goose](https://github.com/block/goose) | v1.44.0 | fork GHDaru/goose, commit 0038bc7 | 2026-07-24 (round 2) | [evaluation](../../benchmark/avaliacoes/goose.html) |
| **opencode** | coding harnesses | [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode) | v1.18.4 (V2 in transition, documented in `CONTEXT.md`) | — | 2026-07-24 (round 1, exploratory) | [evaluation](../../benchmark/avaliacoes/opencode.html) |
| **OpenHands (Agent Canvas)** | coding harnesses | [github.com/All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands) | snapshot 2026-07 | fork GHDaru/OpenHands, commit 6b04532 | 2026-07-24 (round 2) | [evaluation](../../benchmark/avaliacoes/openhands.html) |
| **OpenHarness** | coding harnesses | [github.com/HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) | v0.1.9 | — | 2026-07-24 (round 1, exploratory) | [evaluation](../../benchmark/avaliacoes/openharness.html) |
| **Hermes Agent (Nous Research)** | self-hosted personal agents | [github.com/NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | snapshot 2026-07 | fork GHDaru/hermes-agent, commit 55ef425 | 2026-07-24 (round 2) | [evaluation](../../benchmark/avaliacoes/hermes-agent.html) |
| **IronClaw (NEAR AI)** | self-hosted personal agents | [github.com/nearai/ironclaw](https://github.com/nearai/ironclaw) | snapshot 2026-07 | fork GHDaru/ironclaw, commit 073ded0 | 2026-07-24 (round 2) | [evaluation](../../benchmark/avaliacoes/ironclaw.html) |
| **ohmo (OpenHarness)** | self-hosted personal agents | [github.com/HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) (`ohmo/` directory) | v0.1.9 — dedicated evaluation, complementary to OpenHarness's (round 1) | — | 2026-07 | [evaluation](../../benchmark/avaliacoes/ohmo.html) |
| **OpenClaw** | self-hosted personal agents | [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) | snapshot 2026-07 | fork GHDaru/openclaw, commit 1e15b18b | 2026-07-24 (round 2) | [evaluation](../../benchmark/avaliacoes/openclaw.html) |
| **n8n (AI Agent node)** | embedded harnesses | [github.com/n8n-io/n8n](https://github.com/n8n-io/n8n) | snapshot 2026-07; package evaluated: `packages/@n8n/nodes-langchain` v2.32.0 (135 AI nodes) | fork GHDaru/n8n, commit 55e92cc2 | 2026-07-24 (round 2) | [evaluation](../../benchmark/avaliacoes/n8n.html) |
| **CrewAI** | frameworks | [github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) | v1.15.6 — monorepo with 6 packages (`crewai`, `crewai-core`, `crewai-tools` ~79 tools, `cli`, `crewai-files`, `devtools`) | fork GHDaru, commit b3aaaab | 2026-07 | [evaluation](../../benchmark/avaliacoes/crewai.html) |
| **LangGraph** | frameworks | [github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | langgraph 1.2.9 — monorepo: core (~28k LOC), prebuilt, checkpoint (+postgres/sqlite/conformance), cli, sdk-py; **~63k LOC of tests (2.3× the code)** | fork GHDaru, commit 1e1ca88 | 2026-07 | [evaluation](../../benchmark/avaliacoes/langgraph.html) |
| **OpenAI Agents SDK** | frameworks | [github.com/openai/openai-agents-python](https://github.com/openai/openai-agents-python) | v0.18.3 | fork GHDaru, commit 5976333 | 2026-07 | [evaluation](../../benchmark/avaliacoes/openai-agents-sdk.html) |
| **Software Agent SDK (OpenHands)** | frameworks | [github.com/OpenHands/software-agent-sdk](https://github.com/OpenHands/software-agent-sdk) | v1.37.1 | fork GHDaru, commit 99342c4 | 2026-07 | [evaluation](../../benchmark/avaliacoes/software-agent-sdk.html) |

## Extension ext-1 (2026-07-31): the first Radar→corpus promotion

The corpus grew from 16 to **18** through the very path the book itself institutionalized: the [daily Radar](https://github.com/GHDaru/harness_engineering/blob/main/radar/RADAR.md) (in Portuguese) found the candidates (2026-07-31 sweep), the editor approved the promotion, the repositories were forked for frozen reading, and the same instrument (`HARNESS_EVAL.md`) was applied — round **ext-1**, without touching the round 1/2 snapshots. Both pass the inclusion test of ch. 01 §4 (open source + general-purpose harness + adoption/representativeness): Grok Build for the opening of a complete commercial harness; Pi as a **deliberately atypical case** (Yin's replication logic called for a minimalist counterpoint, and the corpus was missing one).

| Harness | Category | Origin | Version/snapshot | Fork/commit read | Evaluated on | Analysis |
|---|---|---|---|---|---|---|
| **Grok Build (xAI)** | coding harnesses | [github.com/xai-org/grok-build](https://github.com/xai-org/grok-build) | snapshot 2026-07 (opened on 2026-07-15, Apache 2.0) | fork GHDaru/grok-build, commit dd04f39 | 2026-07-31 (round ext-1) | [evaluation](../../benchmark/avaliacoes/grok-build.html) |
| **Pi (Earendil Labs)** | coding harnesses | [github.com/badlogic/pi-mono](https://github.com/badlogic/pi-mono) | snapshot 2026-07-31 | fork GHDaru/pi, commit 7846534 | 2026-07-31 (round ext-1) | [evaluation](../../benchmark/avaliacoes/pi.html) |

## Consolidated diagnosis

The **per-dimension results** (scores 0–3, with evidence) and the comparative diagnosis live in the [Harness Comparison](comparative.html) — including the interactive heatmap. Beyond the scores, each individual evaluation brings: the harness's **observed archetype**, its strengths with file paths, and the **"what to steal"** section (patterns worth carrying over to other harnesses).

> **Method note** (ch. 01 §6): selection followed replication logic (Yin) — representative *and* deliberately atypical cases; the unit of analysis is the source code; the scores follow the template's fixed grid (feature analysis, DESMET). The expiration scoreboard for the predictions is in the [History](../historico.html) (in Portuguese).

---

> **See also**: reference implementations beyond the ones evaluated here are catalogued in [Awesome Harness Engineering — Reference Implementations](https://github.com/GHDaru/awesome-harness-engineering#reference-implementations).
