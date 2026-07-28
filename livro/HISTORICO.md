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

### Edição 0.18 — 2026-07-27 · Glossário + siglas por extenso
- **Feature spec-kit oficial `023-glossario-siglas`**: nova página **Glossário** (`livro/glossario.md`) com as siglas do livro **por extenso**, explicação curta e **em que capítulos aparecem** (agrupadas por tema). Fiel ao texto (siglas varridas; expansões conferidas na fonte — Princípio I).
- **Siglas "abertas" em todo o livro**: o motor envolve automaticamente cada sigla conhecida em `<abbr title="Por Extenso">` — o leitor vê o significado ao passar o mouse — de forma **não-invasiva** (sem mexer no Markdown-fonte) e **HTML-safe** (não toca em código, `<pre>`, links ou títulos).
- **Política no Guia Editorial**: expandir na 1ª ocorrência; o mapa de siglas vive no motor e é espelhado no Glossário.
- **IA (A3)**: agente **Claude Code (Anthropic)** — implementação; curadoria e aprovação humanas.

### Edição 0.17 — 2026-07-27 · experiência de entrada do livro (índice repaginado)
- **Feature spec-kit oficial `021-experiencia-entrada`**: o sumário deixou de ser uma lista crua e virou uma **entrada de verdade** — mantendo a **sidebar** com o índice completo (navegação sem rolar), o conteúdo principal ganhou: **hero** (capa + título + `vX.Y.0`/DOI + CTAs), card **"Continue lendo/Retomar"** (via `localStorage`, aparece após ler um capítulo), **trilha** em 4 passos (Fundamentos → Funcionalidades → Benchmark → Mão na massa) e os **capítulos em cartões** com *teaser*; benchmark/aparato/sobre como **pills**.
- **Teasers por capítulo** entraram no `sumario.json` (conteúdo reaproveitável). O motor grava o último capítulo lido e popula o "Retomar".
- **Theme-aware** (claro/escuro via `--vars`), **responsivo** (hero empilha, trilha 2 col., cartões 1 col. no mobile) e acessível. O cartão vira a **base do template dos capítulos** (feature futura).
- **IA (A3)**: agente **Claude Code (Anthropic)** — design e implementação; curadoria e aprovação humanas (mockups revisados antes de publicar).

### Edição 0.16 — 2026-07-27 · fix: itálico no markdown do chat-companion
- **Feature spec-kit oficial `022-companion-markdown`**: o widget do companion agora renderiza **itálico** `*x*` (antes vazava como asteriscos). `fmt()` converte `*itálico*` em `<em>` após o negrito, **sem** tocar em `**` nem quebrar identificadores `snake_case`. Escape antes da formatação mantido (segurança).
- **IA (A3)**: agente **Claude Code (Anthropic)** — correção; curadoria humana.

### Edição 0.15 — 2026-07-27 · DOI emitido e fixado
- **Feature spec-kit oficial `019-doi-badge-site`**: o **DOI** da obra foi emitido pelo Zenodo — **[10.5281/zenodo.21632412](https://doi.org/10.5281/zenodo.21632412)** — e fixado: **badge** no README, **link do DOI** na tela-capa (junto ao selo de versão) e seção **"Como citar"** na página do autor.
- Com isso, a obra passa a ser **citável academicamente** com identificador persistente, versionado por edição — a cláusula de expiração agora tem um DOI.
- **IA (A3)**: agente **Claude Code (Anthropic)** — fixação do DOI; curadoria humana.

### Edição 0.14 — 2026-07-27 · preparação de DOI e citação (Zenodo/DataCite)
- **Feature spec-kit oficial `018-doi-citacao-zenodo`**: repositório preparado para receber um **DOI** via **Zenodo** (DataCite) — modelo de **concept DOI** (obra viva) + **DOI por versão** (cada edição), espelhando a cláusula de expiração.
- **Licenciamento duplo**: `LICENSE` = **CC BY 4.0** (conteúdo) e `LICENSE-CODE` = **MIT** (código), com nota no README dizendo o que cada uma cobre.
- **Metadados de citação**: `CITATION.cff` (o GitHub passa a mostrar "Cite this repository") e `.zenodo.json` (autor **Gilsiley Henrique Darú** + ORCID `0000-0002-8979-0461`, tipo = livro, licença, keywords, idioma, links para o site). A **co-autoria de IA** é declarada na descrição, **não** como creator (ICMJE/COPE, Guia §6).
- **README**: seções "Como citar" (com espaço para o badge do DOI) e "Licença".
- **Pendente (follow-up)**: o autor liga o Zenodo ao repo e publica um *release* → o DOI é emitido; então o **número/badge** é fixado no README e na capa/colofão do site.
- **IA (A3)**: agente **Claude Code (Anthropic)** — preparação dos metadados; curadoria humana.

### Edição 0.13 — 2026-07-27 · chat-companion: widget no site
- **Feature spec-kit oficial `017-widget-chat-companion`**: o **widget** do companion — um chat flutuante (launcher que abre/minimiza) presente em **todas as páginas, inclusive a capa**. JS/CSS puro injetado pelo motor `publicar/` (progressive enhancement; sem JS a página segue inteira).
- **Cabeçalho de capacidades por capítulo**: o painel mostra "o que posso fazer agora (até o cap. N)" com as capacidades **ativas** (verdes) e as **bloqueadas** (🔒), conforme o capítulo da página e o modo (avançado × progressivo). O capítulo é derivado no build a partir do título; o mapa de capacidades é espelhado no build para render instantâneo — o **backend continua impondo** o gating no `/chat`.
- **Conversa e memória**: fala com o backend (016) em `POST /chat`; identidade **anônima por navegador** (`localStorage`), com histórico via `GET /history`. Degradação graciosa se o backend cair (aviso amigável; a página nunca trava).
- **Acessível e responsivo**: `aria-label`, foco ao abrir, teclado (Enter envia, Esc fecha), contraste; painel quase full no mobile; legível sobre a capa escura; theme-aware.
- **Backend no ar**: publicado no Railway (`harnessengineering-production.up.railway.app`) com Postgres (Neon) e NVIDIA NIM; `/health` = `openai`+`postgres`; `/chat` já cita o livro.
- **IA (A3)**: agente **Claude Code (Anthropic)** — implementação; curadoria humana.

### Edição 0.12 — 2026-07-27 · chat-companion: backend (harness-zero ao vivo)
- **Feature spec-kit oficial `016-chat-companion-backend`**: nasce o **backend do chat-companion** em `chat-companion/backend/` — um serviço FastAPI que **é o harness-zero rodando em produção** (reusa `LLMPort` e o loop de tool-calling do etapa 01). Atende o futuro widget do site.
- **Portas (hexagonal por necessidade)**: `LLMPort` (echo / OpenAI-compatible → NVIDIA NIM, com **BYOK** por requisição), `StorePort` (`MemoryStore` para dev / `PostgresStore` para **Neon**, com criação de tabelas na subida) e `ToolPort` (tools **seguras/sandbox**: hora, cálculo aritmético seguro, busca no texto do livro).
- **Gating de capacidades por capítulo** (`capabilities.py`): modo **avançado** (tudo) × **progressivo** (só o que o livro ensinou até o capítulo atual) — o *fading* do 4C/ID virando comportamento. `GET /capabilities` é a fonte que o widget exibe ("o que posso fazer agora").
- **Endpoints**: `/health`, `/capabilities`, `/session`, `/chat`, `/history`, `DELETE /session/{id}` (LGPD). **Identidade anônima** por navegador; **rate limit** por sessão/IP (BYOK isenta); **CORS** restrito.
- **Segurança (cap. 07 aplicado a si)**: nenhum segredo no repo; chave só em env; `.env` gitignored; tools sandbox; BYOK nunca persistida. Suíte de smoke (echo + memória) verde, **sem rede e sem banco**.
- **Deploy**: artefatos (`Procfile`, `railway.json`, `runtime.txt`, `requirements.txt`, `.env.example`) e **README com passo-a-passo Neon + Railway**. O deploy do Railway é manual do autor; o Pages não hospeda o backend.
- **Tensão intencional documentada**: o companion (produção) roda à frente das etapas didáticas — `StorePort`/`ToolPort` que as etapas 02/04 formalizarão depois. Registrado no plano, não é violação.
- **IA (A3)**: agente **Claude Code (Anthropic)** — arquitetura, código e testes; curadoria humana.

### Edição 0.11 — 2026-07-27 · versão e data de atualização na tela-capa
- **Feature spec-kit oficial `015-versao-data-capa`**: a tela-capa (splash) passa a exibir um selo discreto **`vX.Y.0 · atualizado em <data>`**. A **versão** é derivada automaticamente da **última edição deste histórico** (fonte única — `### Edição X.Y` → `vX.Y.0`), de modo que o placar de edições e a versão exibida nunca divergem. A **data** vem do **último commit** no momento do build (`git log -1`), fiel à última modificação de conteúdo; sem git, cai para a data do build. Fallbacks totais: o selo jamais quebra o build nem o gate de link-check.
- **Coerência com a tese**: carimbar versão + data de atualização logo na entrada materializa a cláusula de expiração (livro vivo) na própria porta do site.
- **IA (A3)**: agente **Claude Code (Anthropic)** — implementação; curadoria humana.

### Edição 0.10 — 2026-07-27 · página "Sobre o autor"
- **Feature spec-kit oficial `014-pagina-sobre-autor`**: nova página de *back matter* **"Sobre o autor"** (`livro/autor.md` → `autor.html`), com a biografia acadêmica e profissional de **Gilsiley Henrique Darú** — formação (doutorado UFPR em andamento, mestrados USP e UFPR, especializações), atuação profissional (Neogrid: Head de Dados & IA e trajetória no laboratório de inovação; WEG, Malwee, Datasul), docência (professor universitário na UDESC e outras; coordenação de curso de Engenharia de Produção na FAMEG; pós-graduação em IA & Deep Learning) e produção acadêmica (artigos, anais, orientações), com perfis verificáveis.
- **Navegação**: item entra no `sumario.json` (parte "Sobre"), aparecendo na sidebar e no sumário, com paginação padrão; o nome do autor nos **créditos da tela-capa** vira link para a página.
- **Fontes**: Currículo Lattes (`6253911800847523`), ORCID (`0000-0002-8979-0461`), perfil profissional público (LinkedIn) e busca web verificável (Journal of Lean Systems, art. 1930). Fatos rastreáveis, sem dados inventados (Princípio I); empresas/instituições citadas como trajetória, sem endosso (Princípio VI).
- **IA (A3)**: agente **Claude Code (Anthropic)** — pesquisa das fontes, redação e implementação; curadoria e responsabilidade humanas.

### Edição 0.9 — 2026-07-27 · tela-capa full-screen (splash)
- **Feature spec-kit oficial `013-splash-capa-cheia`**: `index.html` virou uma **tela-capa full-screen** (capa grande + título + subtítulo + créditos + CTA "Entrar no livro"), sem sidebar; o índice migrou para **`sumario.html`** (com a navegação). A marca das páginas internas aponta para o sumário e há link discreto para a capa; paginação Sumário↔capítulos. Responsiva, `alt` descritivo, gate de link-check verde.
- **IA (A3)**: agente **Claude Code (Anthropic)** — implementação; imagem por **GPT (OpenAI)**; curadoria humana.

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
