# Histórico — este é um livro vivo

> A engenharia de harness muda em meses. Este livro assume isso: cada capítulo declara **quando** seu estado da arte foi capturado, e este arquivo registra o que mudou entre edições. É a materialização da tese central do livro — a **cláusula de expiração** (cap. 01, 14): todo componente de harness é temporário; um livro sobre isso precisa ser datado, ou contradiz o que ensina.

## Como ler as datas do livro

- **Data do evento** (no corpo dos capítulos): quando algo aconteceu no mundo — "AGENTS.md doado à Linux Foundation (dez/2025)". É fato histórico, não muda.
- **Data de captura / "estado da arte em"** (no cabeçalho de cada capítulo): quando *nós* fotografamos o panorama. É o que diz ao leitor se a seção "Estado da arte" está fresca. Uma seção capturada em 2026-07 lida em 2028 deve ser confrontada com este histórico.
- **Rodada do benchmark** (nas avaliações): a versão da foto de cada repositório (`rodada 1`, `rodada 2`, `frameworks-1`), com data. Reavaliar = nova rodada, nunca sobrescrever silenciosamente.

## Tabela de snapshot por capítulo

| Capítulo | Estado da arte capturado em | Fontes da indústria | Última revisão |
|---|---|---|---|
| 02 Loop | 2026-07 | ✓ | 2026-07-25 |
| 03 Contexto | 2026-07 | ✓ | 2026-07-25 |
| 04 Compactação | 2026-07 | ✓ | 2026-07-25 |
| 05 Ferramentas | 2026-07 | ✓ | 2026-07-25 |
| 07 Permissões/Segurança | 2026-07 | ✓ | 2026-07-25 |
| 06, 08–17 | — (pré-v3) | pendente | — |

## Edições

### Edição 0.4 — 2026-07-25 · publicação (feature 001, em andamento)
- **Primeira melhoria sob o Princípio VII** (spec-driven, branch `001-publicacao-latex-html`): spec → plan → tasks → implement.
- **Motor do livro próprio** (`publicar/`, Node): gera o site HTML navegável a partir do Markdown (`docs/`), com sidebar, navegação anterior/próximo, tema claro/escuro, selo de data de captura (livro vivo) e callouts pedagógicos. Fonte permanece Markdown; publicação é um adapter (portas-e-adaptadores). P1 concluída; P2 (viz React), P3 (PDF/LaTeX), P4 (CI + apêndice de infra) pendentes.

### Edição 0.3 — 2026-07-25 · "livro vivo"
- Introduzido o sistema de datação (este arquivo, cabeçalhos de captura nos capítulos, o registro de expiração abaixo).
- Fase de edição v3 iniciada: capítulos 02, 03, 04, 05, 07 reescritos com "Fontes da indústria" + "Estado da arte" + "Apêndice A por repositório".
- harness-zero: endpoint gratuito NVIDIA NIM documentado.
- **Governança formalizada**: constituição do projeto preenchida (`.specify/memory/constitution.md`, v1.0.0) com os 6 princípios centrais — incluindo o framework pedagógico (princípio III) — e `CLAUDE.md` na raiz tornando-a a autoridade que todo trabalho deve seguir.

### Edição 0.2 — 2026-07-25 · fundação pedagógica e camadas novas
- Parecer editorial, framework pedagógico (Backward Design + 4C/ID + Diátaxis + Carga Cognitiva), Guia Editorial.
- Capítulos novos: 15 (harness embutido), 16 (aprendizado auto-evolutivo), 17 (protocolos).
- harness-zero iniciado (etapas 0–1); bibliografia científica; spec-kit e skill academic-research.

### Edição 0.1 — 2026-07-24 · fundação
- Introdução, fundamentos, 12 capítulos de dimensão, capítulo de convergências.
- Benchmark: rodada 1 (opencode, gemini-cli, OpenHarness), rodada 2 (Codex, Goose, Aider, OpenHands, OpenClaw, Hermes, IronClaw, n8n), rodada frameworks-1 (LangGraph, Agents SDK, CrewAI, software-agent-sdk); ohmo; retro dim-13.

---

## Registro de expiração (o placar das previsões)

> A parte mais viva do livro. Cada componente de harness que descrevemos existe porque o modelo ainda não faz aquilo sozinho — e prevemos *quando* deixaria de ser necessário. Aqui pontuamos essas previsões contra a realidade, com data. É a única seção que **espera-se** que envelheça: quando uma linha vira "cumprida", o livro registrou a própria disciplina se dissolvendo em tempo real.

**Estados:** 🔵 aberta (prótese ainda necessária) · 🟡 em movimento (sinais de expiração) · 🟢 cumprida (o modelo/plataforma absorveu) · 🔴 refutada (a previsão estava errada; o componente é mais permanente do que pensávamos)

<div data-viz="expiracao"></div>

| Componente | Existe porque… | Previmos que expira quando… | Estado | Evidência datada |
|---|---|---|---|---|
| Compactação (cap. 04) | janelas são finitas e caras | contexto longo ficar barato e confiável | 🟡 em movimento | A compactação **mudou de dono** antes de expirar: Anthropic lançou compaction na API (beta `compact-2026-01-12`) e o Codex fez compactação remota v2 (2026). Não desapareceu — migrou do harness para a plataforma. |
| Prompt por família de modelo (cap. 03) | modelos respondem diferente a instruções | instruction-following convergir | 🔵 aberta | Ainda divergente; Codex chegou a tornar o prompt server-driven por modelo (2026) — reforço, não expiração. |
| Plan mode imposto (cap. 09) | modelos agem precipitadamente | modelos planejarem sob risco espontaneamente | 🔵 aberta | Planejamento seguiu como a dimensão mais fraca da indústria em todas as rodadas (2026-07). |
| Policy engine / aprovações (cap. 07) | modelos não são confiáveis com ações destrutivas | confiabilidade calibrada e verificável | 🔵 aberta | Consenso 2026: injection tratada como não-resolvível; esforço migrou para blast radius, não para confiar no modelo. |
| Aprendizado auto-evolutivo (cap. 16) | — (cláusula invertida) | nunca — o harness *escreve* scaffolding em vez de esperar o modelo | 🔵 aberta | Hermes e gemini-cli fecharam o ciclo (2026-07); é auto-expansão, não expiração. |
| Sandbox / contenção (cap. 07) | é sobre o mundo, não sobre o modelo | nunca (fronteira, não prótese) | 🔴 não-expira | Confirmado nas 3 rodadas; contenção é o scaffolding que resta quando o modelo melhora. |
| Protocolos (MCP/A2A/ACP/AGENTS.md — cap. 17) | interoperabilidade entre sistemas | nunca (fronteira com o mundo) | 🔴 não-expira | AGENTS.md sob Linux Foundation; MCP em 10/11 harnesses (2026-07). |

*Regra de manutenção: a cada rodada do benchmark e a cada edição, revisar esta tabela — promover 🔵→🟡→🟢 com a evidência datada que justifica. Uma linha que muda de estado é a notícia mais importante que uma nova edição pode trazer.*
