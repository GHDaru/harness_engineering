# Parecer editorial e plano pedagógico do livro

> Data: 2026-07-25 · Papel: editor pedagógico e de escrita · Escopo: (1) avaliar a proposta "construção de um harness completo com DDD + Hexagonal + chat"; (2) escolher o framework pedagógico e de escrita; (3) planejar os capítulos com objetivos de aprendizagem; (4) mapear a bibliografia científica candidata por capítulo.

---

## Parte 1 — Parecer sobre a proposta (DDD + Hexagonal + chat)

### Veredito: aprovada com condições — e as condições importam mais que a aprovação

**Por que a ideia é boa (e não é enfeite):**

1. **O livro precisa disso.** Hoje ele é analítico — lê código dos outros. Toda a literatura de aprendizagem complexa (4C/ID, construcionismo) diz o mesmo: competência profissional se forma em *tarefas inteiras*, não em análise de partes. Um projeto-fio-condutor transforma o leitor de espectador em construtor, e dá ao livro o terceiro pilar que falta: **teoria (fundamentos) + evidência (benchmark) + prática (construção)**.
2. **Hexagonal não é escolha arbitrária — é o padrão real do domínio.** O benchmark já provou isso sem querer: os melhores harnesses convergiram para portas-e-adaptadores. O `software-agent-sdk` tem tudo como ABC plugável (condenser, analyzer, store); o IronClaw formaliza "ports" no kernel boundary; o opencode separa core/protocol/client; o provedor de modelo é a porta canônica de todos. Ensinar harness *é* ensinar a desenhar essas portas — a arquitetura hexagonal só dá nome ao que o domínio já exige. Item raro: a escolha arquitetural do exemplo didático coincide com a lição do domínio.
3. **O chat como front é a janela de observação certa.** Cada dimensão do harness ganha manifestação visível: streaming (cap. 02), pedido de aprovação inline (cap. 07), indicador de compactação (cap. 04), lista de todos (cap. 09). O chat não é um "front bonitinho" — é o instrumento de medição do leitor.

### As quatro condições (onde a ideia pode afundar o livro)

**Condição 1 — DDD leve, a serviço do domínio; nunca DDD-cerimônia.**
O risco nº 1 é escrever dois livros ao mesmo tempo, ambos mal. DDD completo (aggregates, repositories, factories, bounded contexts, event storming) tem peso conceitual próprio e disputaria a atenção com o assunto real. Recomendação editorial firme:
- Usar o DDD **estratégico** de forma quase invisível: a *linguagem ubíqua* já existe — é o glossário do livro (Turn, Session, Tool, Permission, Compaction, Skill); os *bounded contexts* já existem — são as dimensões dos capítulos.
- Usar padrões **táticos** só onde pagam aluguel: `Session` como aggregate root; `Event` como objeto imutável; `PermissionPolicy` como domínio puro (testável sem LLM). Nada de repository/factory por protocolo.
- Regra de escrita: **DDD aparece como consequência nomeada, não como capítulo teórico.** ("Note que a política de permissão não conhece LLM nem chat — isso é o domínio isolado que o DDD chama de...").

**Condição 2 — Arquitetura por refatoração, não por cerimônia inicial.**
Começar o projeto com a estrutura hexagonal completa viola tudo o que sabemos de carga cognitiva (e contradiz o "start simple" da Anthropic que citamos no cap. 01). O caminho pedagógico correto: a etapa 1 é um loop de ~80 linhas num arquivo só; a porta `LLMPort` nasce na etapa em que trocamos de provedor e dói; o adapter de persistência nasce quando a sessão precisa sobreviver ao restart. **Cada porta nasce de uma dor sentida no capítulo correspondente.** Assim a arquitetura é aprendida como solução, não como liturgia.

**Condição 3 — Defesa contra o apodrecimento do tutorial.**
Código em livro envelhece na velocidade das APIs de modelo. Mitigações obrigatórias: (a) o modelo fica atrás da porta desde a etapa 2 — trocar de provedor é trocar um adapter (a própria arquitetura é a defesa); (b) o projeto vive em repositório próprio com CI que executa cada etapa (uma tag git por capítulo: `etapa-02`, `etapa-03`...); (c) versões pinadas + a "cláusula de expiração" aplicada ao próprio projeto.

**Condição 4 — Escopo do chat congelado.**
Um arquivo HTML+JS (ou equivalente mínimo) servido pelo próprio backend. Sem framework de front, sem build step. O chat evolui *só* quando uma dimensão do harness precisar de superfície nova. Qualquer sofisticação de front é escopo roubado do assunto do livro.

**Decisões que recomendo (para o autor ratificar):** stack Python + FastAPI (coerente com OpenHarness/software-agent-sdk, os dois códigos-referência mais legíveis do benchmark; público BR); nome do projeto: **"Arreio"** (harness em português — memorável e temático); repositório separado `GHDaru/arreio` referenciado pelo livro.

---

## Parte 2 — Framework pedagógico e de escrita

Nenhum framework isolado cobre um livro técnico com trilha prática; a combinação certa é conhecida e complementar:

### 2.1 Backward Design (Wiggins & McTighe) — o "para quê" de cada capítulo
Todo capítulo passa a declarar, nesta ordem de projeto: (1) **resultados desejados** (objetivos de aprendizagem, verbos da taxonomia de Bloom); (2) **evidências de compreensão** (o que o leitor consegue fazer/explicar ao final — os exercícios e o passo da construção); (3) só então o conteúdo. Escrevemos o capítulo de trás para frente.

### 2.2 4C/ID (van Merriënboer) — a espinha da trilha prática
O modelo de referência para *aprendizagem complexa* (habilidades com alta interatividade de elementos — exatamente engenharia de harness). Os quatro componentes mapeiam 1:1 no nosso material:
- **Learning tasks** (tarefas inteiras, do simples ao complexo) = as etapas da construção do Arreio — cada uma é um harness *funcionando*, progressivamente mais completo;
- **Supportive information** (teoria que apoia o raciocínio) = o corpo dos capítulos 02–17;
- **Just-in-time information** (procedimento no momento do uso) = boxes e comentários no código da construção;
- **Part-task practice** (treino de rotina isolada) = katas por capítulo ("escreva a função de prune"; "derive o JSON Schema de um dataclass").
Fundamento: [Blueprints for complex learning: The 4C/ID-model](https://link.springer.com/article/10.1007/BF02504993) e o livro *Ten Steps to Complex Learning* (3ª ed., 2018).

### 2.3 Diátaxis — a disciplina dos tipos de texto
O livro já tem os quatro quadrantes do Diátaxis sem saber; a regra editorial é **não misturá-los na mesma seção**:
- *Explanation* = capítulos 02–17 (o problema, os padrões, a evidência);
- *Tutorial* = a construção do Arreio (trilha guiada, garantia de sucesso);
- *Reference* = templates (HARNESS_EVAL, FRAMEWORK_EVAL) e as tabelas do benchmark;
- *How-to* = as seções "o que roubar" (receitas pontuais para quem já constrói).

### 2.4 Teoria da Carga Cognitiva (Sweller) — as regras de escrita do código didático
- **Worked examples primeiro**: código completo e comentado antes de pedir modificação;
- **Completion problems**: exercícios são "complete este adapter", não "escreva do zero";
- **Fading**: o andaime didático diminui etapa a etapa (na etapa 1 mostramos tudo; na 10, especificamos e o leitor implementa);
- Uma ideia nova por vez: nunca introduzir conceito de harness + padrão DDD + sintaxe nova no mesmo trecho.
Fundamento: [Cognitive Architecture and Instructional Design: 20 Years Later](https://link.springer.com/article/10.1007/s10648-019-09465-5) (Sweller, van Merriënboer & Paas, 2019).

### 2.5 O esqueleto padrão de capítulo (v2)
Cada capítulo de dimensão passa a ter oito seções fixas:
1. **Objetivos** (3–5, verbos de Bloom: *explicar* a escada de compactação; *comparar* prune × sumarização; *implementar* truncamento com preservação de bordas)
2. **O problema** (já existe)
3. **Fundamentos científicos** (novo — 2–4 papers com o que a pesquisa estabeleceu)
4. **Padrões de implementação** (já existe)
5. **Evidência do benchmark** (já existe)
6. **Mão na massa — Arreio etapa N** (novo — a tarefa inteira do 4C/ID)
7. **Síntese + "o que roubar"** (já existe)
8. **Verificação** (novo — 2–3 perguntas/exercícios que testam os objetivos do item 1)

---

## Parte 3 — Plano por capítulo: objetivo central + etapa da construção

| Cap. | Objetivo de aprendizagem central (Bloom) | Etapa do Arreio |
|---|---|---|
| 00–01 | *Definir* harness e *justificar* cada componente pela limitação que compensa | Etapa 0: chat burro + `LLMPort` (echo → modelo real) |
| 02 Loop | *Implementar* o ciclo prompt→tool→resultado com critérios de parada | Etapa 1: loop de tool-calling em ~80 linhas, streaming no chat |
| 05 Tools | *Derivar* schemas de tipos e *avaliar* trade-offs de arsenal | Etapa 2: `ToolPort` + 3 tools (read/write/shell) com schema automático |
| 03 Contexto | *Compor* system prompt em camadas cache-aware | Etapa 3: montador de contexto + `ARREIO.md` do projeto |
| 08 Memória | *Projetar* persistência de sessão com retomada | Etapa 4: adapter SQLite; `/resume` no chat |
| 04 Compactação | *Aplicar* a escada truncar→prune→sumarizar | Etapa 5: compactação com indicador visual no chat |
| 07 Permissões | *Isolar* política como domínio puro e *criticar* política sem contenção | Etapa 6: `PermissionPolicy` + aprovação inline no chat + paths sensíveis fixos |
| 06 MCP | *Integrar* um servidor MCP externo via adapter | Etapa 7: adapter MCP client (stdio) |
| 09 Planejamento | *Impor* plan mode via permissões | Etapa 8: modo plan no chat (toggle) |
| 10 Subagentes | *Delegar* com contexto e permissões isolados | Etapa 9: tool `task` com sessão-filha |
| 11 Verificação | *Construir* eval mínima com juiz e respostas gravadas | Etapa 10: suíte de evals do próprio Arreio |
| 12 Extensibilidade | *Expor* hooks nos pontos do ciclo de vida | Etapa 11: hooks pre/post tool |
| 13 Interfaces | *Separar* núcleo de superfície | (retrospectiva: o chat foi um adapter o tempo todo) |
| 16 Aprendizado | *Fechar* um ciclo mínimo de skill learning com anti-padrões | Etapa 12 (avançada): skills que o Arreio escreve |
| 14/15/17 | *Analisar* convergências, embutidos e protocolos | sem etapa (capítulos analíticos) |

*(Ordem das etapas ≠ ordem dos capítulos em dois pontos — tools antes de contexto — porque a construção exige; o livro sinaliza os desvios.)*

---

## Parte 4 — Bibliografia científica candidata por capítulo

> **Status: candidata — nenhuma referência entra no livro sem validação** (ler o abstract, confirmar aderência e URL viva, no padrão verify_urls do referencial). ⭐ = âncora provável do capítulo. IDs de arXiv confirmados por busca em 2026-07-25; itens marcados (m) vêm de memória e exigem verificação redobrada.

**Transversal / Fundamentos (01):**
- ⭐ *From Question Answering to Task Completion: A Survey on Agent System and Harness Design* — [arXiv 2606.20683](https://arxiv.org/pdf/2606.20683) — o survey exatamente no nosso recorte; candidato a espinha teórica do cap. 01.
- *A Review of Prominent Paradigms for LLM-Based Agents* (CoLing 2025) — [aclanthology](https://aclanthology.org/2025.coling-main.652.pdf)
- *LLM Agent: A Survey on Methodology, Applications and Challenges* — [repo](https://github.com/luo-junyu/Awesome-Agent-Papers)

**Cap. 02 (Loop):** ReAct (m, arXiv 2210.03629); *LLM-based Agentic Reasoning Frameworks: A Survey* — [2508.17692](https://arxiv.org/pdf/2508.17692); *RL-based Agentic Search Survey* — [2510.16724](https://arxiv.org/pdf/2510.16724)

**Cap. 03 (Contexto):** ⭐ *A Survey of Context Engineering for LLMs* — [2507.13334](https://arxiv.org/abs/2507.13334); *Less Context, Better Agents* — [2606.10209](https://arxiv.org/abs/2606.10209); *Lost in the Middle* (m, 2307.03172)

**Cap. 04 (Compactação):** *ContextBudget* — [2604.01664](https://arxiv.org/pdf/2604.01664); *The Missing Memory Hierarchy: Demand Paging for LLM Context Windows* — [2603.09023](https://arxiv.org/pdf/2603.09023); MemGPT (m, 2310.08560)

**Cap. 05 (Tools):** *Evolution of Tool Use in LLM Agents* — [2603.22862](https://arxiv.org/pdf/2603.22862); *Tool Learning survey* — [repo quchangle1](https://github.com/quchangle1/LLM-Tool-Survey); Gorilla/ToolLLM (m)

**Cap. 06 (MCP):** spec MCP; análises de segurança de MCP (a localizar — lacuna de busca)

**Cap. 07 (Permissões/segurança):** ⭐ *Security Threats and Defenses in LLM-Based AI Agents: Layered Attack Surface* — [2604.23338](https://arxiv.org/pdf/2604.23338); *A Survey on Agentic Security* — [2510.06445](https://arxiv.org/pdf/2510.06445); *Safety of Computer-Using Agents* — [2505.10924](https://arxiv.org/pdf/2505.10924); prompt injection Greshake et al. (m)

**Cap. 08 (Memória):** ⭐ *Survey on Memory Mechanism of LLM-based Agents* — [2404.13501](https://arxiv.org/abs/2404.13501); *From Storage to Experience* — [2605.06716](https://arxiv.org/abs/2605.06716); *From Human Memory to AI Memory* — [2504.15965](https://arxiv.org/pdf/2504.15965); *Governing Evolving Memory (SSGM)* — [2603.11768](https://arxiv.org/pdf/2603.11768)

**Cap. 09 (Planejamento):** *Understanding the Planning of LLM Agents* (m, 2402.02716); *PLANET: benchmarks de planejamento* — [2504.14773](https://arxiv.org/pdf/2504.14773); *Task-Decoupled Planning* — [2601.07577](https://arxiv.org/pdf/2601.07577)

**Cap. 10 (Multi-agente):** survey multi-agente (m, 2412.17481); *MultiAgentBench* (m); *D3MAS* — [2510.10585](https://arxiv.org/pdf/2510.10585)

**Cap. 11 (Evals):** ⭐ *Survey on Evaluation of LLM-based Agents* — [2503.16416](https://arxiv.org/abs/2503.16416); SWE-bench (m, 2310.06770); *2025 AI Agent Index* — [2602.17753](https://arxiv.org/abs/2602.17753)

**Cap. 16 (Aprendizado):** ⭐ *A Survey of Self-Evolving Agents* — [2507.21046](https://arxiv.org/abs/2507.21046); *Comprehensive Survey of Self-Evolving AI Agents* (m, 2508.07407); Voyager (m, 2305.16291); *Adaptation of Agentic AI: Post-Training, Memory, and Skills* — [2512.16301](https://arxiv.org/pdf/2512.16301)

**Caps. 12/13/15/17:** dimensões com literatura acadêmica rarefeita (extensibilidade, interfaces, embutidos, protocolos) — a lacuna é em si um achado a registrar no livro; cobrir com specs, papers industriais e o survey-âncora transversal.

---

## Próximos passos propostos (ordem)

1. **Ratificação do autor**: stack (Python+FastAPI?), nome (Arreio?), repositório separado.
2. **Sprint de validação bibliográfica**: verificar cada candidata (abstract + URL), promover ⭐ a definitivas, preencher as lacunas (MCP security; multi-agente atual) — vira `livro/bibliografia.md`.
3. **Retrofit piloto em 1 capítulo** (sugiro o 04, Compactação — o mais maduro): aplicar o esqueleto v2 completo (objetivos, fundamentos científicos, verificação) e calibrar o formato antes de replicar aos demais.
4. **Etapa 0–1 do Arreio** (repo próprio, chat + loop mínimo) para validar a viabilidade da trilha prática.
