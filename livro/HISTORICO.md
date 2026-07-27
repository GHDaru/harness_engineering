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
| 06 MCP | 2026-07 | ✓ | 2026-07-26 |
| 07 Permissões/Segurança | 2026-07 | ✓ | 2026-07-25 |
| 08 Memória e Estado | 2026-07 | ✓ | 2026-07-26 |
| 09 Planejamento | 2026-07 | ✓ | 2026-07-26 |
| 10 Subagentes/Orquestração | 2026-07 | ✓ | 2026-07-26 |
| 11 Verificação/Evals | 2026-07 | ✓ | 2026-07-26 |
| 12 Extensibilidade | 2026-07 | ✓ | 2026-07-26 |
| 13 Interfaces | 2026-07 | ✓ | 2026-07-26 |
| 00–01, 14–17 | — (pré-v3) | pendente | — |

## Edições

### Edição 0.8 — 2026-07-27 · capa e landing (hero) no site
- **Feature spec-kit oficial `012-landing-capa`**: a home (`index.html`) ganhou uma **hero de capa** com a imagem gerada (`capa.png`, 1024×1536), título, subtítulo, CTAs ("Começar a ler", Benchmark, Guia) e **créditos como texto** (Gilsiley Henrique Darú — edição/direção/orquestração; Claude/Anthropic — pesquisa/texto; GPT/OpenAI — imagem); o sumário permanece abaixo. Responsiva (empilha e vem antes da navegação no mobile), theme-aware, com `alt` descritivo.
- **Preview social**: meta tags Open Graph + `capa-social.png` (1200×630, gerada via Chromium) para previews de link.
- **Motor**: `build.mjs` copia os assets de capa e injeta as meta OG; sem quebra do gate de link-check.
- **IA (A3)**: agente **Claude Code (Anthropic)** — pesquisa/texto e implementação; imagem de capa por **GPT (OpenAI)**; curadoria e responsabilidade humanas.

### Edição 0.7 — 2026-07-26 · emenda de constituição v1.2.0 (achados do Guia §6)
- **Governança (emenda direta, exceção do Princípio VII, registrada aqui):** constituição **v1.1.0 → v1.2.0** incorporando dois achados do estudo de metodologias (parecer `estudos/2026-07-26-achados-metodologia-escrita.md`):
  - **A2 — revisão developmental** vira portão de qualidade: antes do copyedit, um passo de re-ver estrutura e sentido ("escrever é reescrever"; Sommers/Flower-Hayes). Refletido no Guia §6.E (fluxo) e na seção de portões de qualidade.
  - **A3 — registro do modelo de IA** na datação (Princípio IV): toda edição registra o agente/modelo de IA e a sessão usados (reprodutibilidade).
- **A1 concluído** (feature spec-kit oficial `011-divulgacao-coautoria-ia`): nota de autoria adicionada à abertura (cap. 00, "Nota de autoria e método"), divulgando a co-autoria humano+IA sob responsabilidade humana, com ponteiro para o Guia §6. Os três achados ratificáveis (A1/A2/A3) do estudo estão agora incorporados.
- **IA (aplicação de A3):** agente **Claude Code (Anthropic)** sob curadoria/responsabilidade humanas; sessão registrada nos trailers de commit. *(O identificador interno do modelo é omitido dos artefatos por política de identidade da ferramenta; o autor humano pode anotá-lo à parte se desejar.)*

### Edição 0.6 — 2026-07-26 · estudo de metodologias de escrita (ciclo spec-kit oficial)
- **Primeira feature pelo ciclo oficial do Spec Kit** (spec 010, branch `010-estudo-metodologias-escrita`): `/speckit-specify` → `/speckit-clarify` → `/speckit-plan` (com Constitution Check) → `/speckit-tasks` → `/speckit-analyze` → `/speckit-implement`, usando os scripts `.specify/` e os templates oficiais e seus gates — em contraste com as edições anteriores, que seguiram o *método* spec-driven mas escritas à mão.
- **Nova seção 6 do `GUIA-EDITORIAL.md`**: um *survey* das metodologias de escrita editorial e acadêmica — tradicionais (IMRaD, processo cognitivo, craft/estilo, argumento, peer review, design instrucional) e da era-IA (co-escrita, spec-driven, RAG/verificação, integridade/autoria, críticas) — com o **método deste livro declarado** e a **divulgação aberta de co-autoria humano+IA** (Claude Code sob responsabilidade humana), seguindo as políticas ICMJE/COPE/Nature/Science.
- **Bibliografia**: nova seção "Guia — Metodologias de escrita" com as fontes verificadas por busca cruzada.

### Edição 0.5 — 2026-07-26 · visualizações React + unificação editorial v3
- **P2 concluída** (spec 001, branch `002-visualizacoes-react`): ilhas de visualização React no motor do livro — heatmap sortável do benchmark e registro de expiração com filtro, como *islands* (progressive enhancement; sem JS, ficam as tabelas Markdown). Fonte canônica em `benchmark/notas.json`.
- **Sete capítulos de funcionalidade trazidos ao esqueleto v3** (specs 003–009, um ciclo spec-kit por capítulo, branch `003-reescrita-editorial-v3`): 06 MCP, 08 Memória e Estado, 09 Planejamento, 10 Subagentes/Orquestração, 11 Verificação/Evals, 12 Extensibilidade, 13 Interfaces. Cada um ganhou objetivos de Bloom, **fundamentos científicos** (papers reais verificados por busca cruzada), **fontes da indústria** (docs de vendor/blogs), estado da arte no corpo, mão na massa, verificação e **Apêndice A** com as rodadas 2/frameworks.
- **Lacunas de bibliografia preenchidas/registradas**: o cap. 06 (MCP) saiu de "lacuna" para literatura de segurança consolidada (SoK, MCPTox, auditorias); os caps. 12 (extensibilidade) e 13 (interfaces) — sem canon *agent-specific* — foram ancorados em SE clássica e HCI, respectivamente, com a lacuna registrada honestamente (Princípio I).
- **Atualizações datadas (livro vivo)**: refutada a previsão de que "nenhum harness atua como *servidor* MCP no core" (rodada 2: Codex/Hermes/OpenClaw/OpenHands/n8n são cliente **e** servidor); o n8n **depreciou** seu Plan-and-Execute Agent (planejamento explícito recuando para trabalho longo); a verificação virou **adversarial** (reward hacking — o agente joga contra o verificador); e os formatos de extensão (SKILL.md/AGENTS.md) convergindo num padrão portável (o "MCP da extensibilidade").

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
| Plan mode imposto (cap. 09) | modelos agem precipitadamente | modelos planejarem sob risco espontaneamente | 🔵 aberta | Planejamento seguiu como a dimensão mais fraca da indústria em todas as rodadas (2026-07); o n8n **depreciou** seu Plan-and-Execute Agent — o plano explícito recuou para trabalho longo/humano-no-loop, não expirou. |
| Policy engine / aprovações (cap. 07) | modelos não são confiáveis com ações destrutivas | confiabilidade calibrada e verificável | 🔵 aberta | Consenso 2026: injection tratada como não-resolvível; esforço migrou para blast radius, não para confiar no modelo. |
| Verificação externa (cap. 11) | a auto-correção intrínseca não basta (o modelo não se conserta sozinho) | modelos verificarem o próprio trabalho de forma confiável | 🔵 aberta | Reforçada, não expirando: "LLMs Cannot Self-Correct Reasoning Yet" (2310.01798) e o *reward hacking* (o agente apaga asserts/patcha o pytest) empurraram a indústria para verificador **externo e imutável** (testes held-out, verify-on-stop) — 2026-07. |
| Aprendizado auto-evolutivo (cap. 16) | — (cláusula invertida) | nunca — o harness *escreve* scaffolding em vez de esperar o modelo | 🔵 aberta | Hermes e gemini-cli fecharam o ciclo (2026-07); é auto-expansão, não expiração. |
| Sandbox / contenção (cap. 07) | é sobre o mundo, não sobre o modelo | nunca (fronteira, não prótese) | 🔴 não-expira | Confirmado nas 3 rodadas; contenção é o scaffolding que resta quando o modelo melhora. |
| Protocolos (MCP/A2A/ACP/AGENTS.md — cap. 17) | interoperabilidade entre sistemas | nunca (fronteira com o mundo) | 🔴 não-expira | MCP, goose e AGENTS.md doados à **Agentic AI Foundation / Linux Foundation** (dez/2025); MCP em 10/11 harnesses e o ACP fundido no A2A sob a LF (ago/2025) — a fronteira se institucionaliza, não desaparece (2026-07). |

*Regra de manutenção: a cada rodada do benchmark e a cada edição, revisar esta tabela — promover 🔵→🟡→🟢 com a evidência datada que justifica. Uma linha que muda de estado é a notícia mais importante que uma nova edição pode trazer.*
