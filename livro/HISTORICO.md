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
| 14 Convergências | 2026-07 | — | 2026-07-28 |
| 15 Harness Embutido | 2026-07 | — | 2026-07-28 |
| 16 Auto-melhoria | 2026-07 | — | 2026-07-28 |
| 17 Protocolos | 2026-07 | — | 2026-07-28 |
| 00 Introdução · 01 Fundamentos | 2026-07 | ✓ (01) | 2026-07-28 |

## Edições

### Correção 2026-08-05 · o tutor não conhecia o próprio Radar (spec 077)
- **Defeito relatado pelo editor**: perguntas ao companion sobre um sistema avaliado ("o que acharam do Grok Build?") ou sobre uma apuração do Radar não encontravam nada.
- **Três causas independentes**, todas encontradas no diagnóstico: (1) **escopo** — o índice cobria só `livro/` e o comparativo; as **20 avaliações individuais** e o **Radar inteiro** estavam de fora; (2) **blocos** — markdown não separa linhas de tabela com linha em branco, então a mesa inteira do RADAR virava **um único bloco**, que casava com qualquer pergunta e era truncado em 600 caracteres antes de chegar ao modelo, cortando justamente a linha procurada; (3) **pontuação** — o score contava cada *ocorrência* de termo sem normalizar por tamanho, então bloco longo vencia bloco curto e exato.
- **Correções**: escopo ampliado (corpus de **738 → 1.406 blocos**), cada linha de tabela virou bloco próprio, e o score passou a contar **termos distintos** da pergunta com divisor logarítmico de tamanho. Verificado por consulta ao vivo: "Grok Build" agora traz a avaliação; "Microsoft Agent Harness" traz o diário do dia; "opencode × Anthropic" traz os dois diários da apuração.
- **Frescor**: o Radar muda todo dia e seu agente só escreve em `radar/` — o CI passou a regenerar e commitar o `corpus.json`, senão o tutor responderia sempre com um dia de atraso.
- **IA (A3)**: agente **Claude Code (Anthropic)**; diagnóstico, correção e verificação. Correção (Princípio VII) com decisão humana explícita.

### Edição 0.69 — 2026-08-05 · o jornal ganha capa e acervo (spec 076)
- **Feature spec-kit oficial `076-radar-capa-acervo`**, com o editor no papel de aprovador de uma proposta de UX. O [Radar-jornal](https://ghdaru.github.io/harness_engineering/radar.html) tinha prazo de validade medido: com uma página só, a fita de abas viraria parede de datas em ~3 semanas e o HTML passaria de **3 MB em um ano**. Agora são duas camadas: **capa** com as 7 edições mais recentes (tamanho constante para sempre) e **acervo mensal** (`radar-AAAA-MM.html`), com o crescimento virando horizontal — nenhuma página passa de ~250 KB, em qualquer horizonte.
- **A capa deixou de ser só cronologia.** Ganhou o **placar da semana** (edições, achados, quantos A/B, quantos promovidos) e a **mesa de edição** — os itens abertos de impacto A/B do `RADAR.md`, que é o dado mais acionável do Radar e não aparecia no site. O diagnóstico que originou a mudança: ninguém pergunta "o que aconteceu em 12 de agosto?"; pergunta "o que mudou no livro?" e "o que espera decisão?".
- **Detalhes de acabamento que a inspeção visual pegou** (e que valem como padrão do projeto): o filtro por impacto mostra **contagem no chip** e desabilita o vazio — filtro que zera a página sem aviso é beco sem saída; e o resumo da mesa corta no travessão sem **partir link de markdown** (o primeiro corte vazava um `[` na tela).
- O contrato do agente do Radar **não mudou**: ele segue escrevendo um arquivo por dia, sem saber que existe acervo.
- **IA (A3)**: agente **Claude Code (Anthropic)** como UX/UI e implementador; decisões do editor (7 dias na capa, só A/B na mesa) e aprovação humana da proposta antes da implementação.

### Correção 2026-08-03 · a capa noticiava o dia anterior (spec 075)
- **Defeito relatado pelo editor**: com o Radar do dia publicado e o jornal correto, o card de novidades da capa (e da entrada) ainda mostrava 02/08.
- **Causa raiz**: `noticiaDoRadar()` (em `publicar/build.mjs`) devolvia a **primeira linha válida** da tabela de `radar/RADAR.md`, presumindo que o arquivo estivesse sempre em ordem cronológica reversa. Na varredura de 03/08 as linhas novas entraram abaixo de uma linha de 02/08 (a do Traycer, spec 074) — a ordem física deixou de refletir a cronologia e a capa passou a noticiar um item mais antigo (e **descartado**).
- **Correção**: a notícia passa a ser escolhida por **dado** — data mais recente, desempate por impacto (A > B > C) e depois pela ordem do arquivo. Como higiene, a tabela do RADAR.md foi reordenada por data (nenhuma linha alterada). Verificado com tabela deliberadamente fora de ordem (escolhe 08-03/A ignorando a 08-02 no topo) e no site construído: capa e entrada, PT e EN, em 2026-08-03.
- **Lição registrada**: arquivo mantido por agente agendado não garante ordenação — o motor não deve inferir semântica da posição física. Mesma família do defeito de `tx` (0.64): premissa silenciosa que só falha em produção.
- **IA (A3)**: agente **Claude Code (Anthropic)**; enquadrada como correção (Princípio VII) com decisão humana explícita.

### Edição 0.68 — 2026-08-02 · a cadeia de suprimentos vira apêndice — e o teste de inclusão recusa pela primeira vez (spec 074)
- **Novo [Apêndice — A cadeia de suprimentos](apendice-supply-chain.md)** (PT+EN, nos sumários): o mapa de quem consome quem dentro do corpus, com evidência por elo — QM remendando o Pi com patch de segurança próprio (`package.json:58`), Kimi Code com a TUI do Pi vendorizada, software-agent-sdk orquestrando Codex/gemini-cli via ACP, Grok Build retomando sessões de Claude/Codex/Cursor, e três leituras editoriais (a pergunta "de quem é feito?", a sessão como interface de integração, o enforcement que não viaja pela cadeia).
- **Rodada ext-3**: o **[Traycer](../benchmark/avaliacoes/traycer.md)** (indicação do editor, fork GHDaru/traycer @ `65fc3d7`, MIT) foi avaliado com o instrumento completo e é a **primeira recusa documentada do teste de inclusão** (18/36): ~513 mil linhas abertas de clientes/CLI/protocolo, mas o Host que executa as quatro peças é binário fechado + nuvem obrigatória. A leitura rendeu o mapa dos 18 harnesses que ele orquestra — evidência central do apêndice novo. Corpus permanece em 20.
- **Delta traduzido no mesmo ciclo**: apêndice novo em EN, apêndice do estudo (seção ext-3) espelhado, selos renovados; sumários PT/EN em paridade posicional (29 itens).
- **IA (A3)**: agente **Claude Code (Anthropic)** — avaliador sobre o clone congelado com veredito de inclusão fundamentado; curadoria humana (indicação e aprovação do editor).

### Edição 0.67 — 2026-08-02 · rodada ext-2: o corpus vai a vinte — e ganha uma quinta categoria (spec 073)
- **Feature spec-kit oficial `073-ext2-qm-kimi`**: segunda promoção Radar→corpus. **[Kimi Code](../benchmark/avaliacoes/kimi-code.md) (Moonshot AI, 32/36)** — segundo vendor de modelo verticalizando no harness, com co-design harness↔API (a API do Kimi ganhou capability para servir a *progressive tool disclosure* do harness) e autonomia estruturada (goal mode com budgets, swarm de 128 subagentes) sobre enforcement fraco. **[QM](../benchmark/avaliacoes/qm.md) (Y Combinator, 31/36)** — não coube na taxonomia e **inaugurou a categoria "agentes organizacionais"**: escopos, contexto filtrado por entitlement da audiência, consentimento de destinatário e auditoria como primitivas; o loop do agente é motor trocável (Pi, OpenCode, Codex, Claude Code) com a sessão portável via "fita".
- Leituras congeladas: fork GHDaru/kimi-code commit `e22479a`; fork GHDaru/qm commit `7f2c916`. Notas no [comparativo](../benchmark/comparativo.md) (leitura da rodada ext-2: polinização cruzada no corpus — a TUI do Kimi Code é fork da do Pi; o QM traz 4 membros do corpus como dependências) e em `notas.json`.
- Livro: caps. 00/01 (vinte sistemas, cinco arquétipos), Apêndice do estudo (seção ext-2), radar (contrato a 20; QM e Kimi Code promovidos). **Delta traduzido no mesmo ciclo** (00/01/apêndice do estudo/comparativo EN, selos renovados).
- **IA (A3)**: agente **Claude Code (Anthropic)** — dois avaliadores em paralelo sobre os clones congelados; curadoria humana (aprovação do editor e revisão das notas).

### Edição 0.66 — 2026-08-02 · o jornal atualiza sozinho (spec 072)
- **Feature spec-kit oficial `072-radar-publica-site`** (infraestrutura, 1 linha): `radar/**` entrou nos paths do workflow de publicação — o commit diário do agente do Radar agora reconstrói o site, e o [Radar-jornal](https://ghdaru.github.io/harness_engineering/radar.html) publica a edição do dia sem esperar o próximo push editorial. Fecha o ciclo da spec 071: apuração agendada → jornal no ar, sem toque humano.
- **Origem**: nota de manutenção da execução agendada de 2026-08-02 — o agente do Radar detectou a lacuna mas não pôde corrigi-la (regra dura: escrita só em `radar/`), registrou e o editor promoveu ("promova"). O contrato funcionando como projetado.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.65 — 2026-08-01 · o Radar vira jornal (spec 071)
- **Feature spec-kit oficial `071-radar-jornal`**: o diário do Radar agora é diagramado como **site de notícias** em [`radar.html`](https://ghdaru.github.io/harness_engineering/radar.html) — masthead com o contrato editorial, abas por edição, **manchete** (achado de maior impacto do dia), cards com badge A/B/C e **chips de fontes por domínio** (estilo jornalístico: toda afirmação com fonte clicável), e caixas de transparência ("como esta edição foi apurada", "da redação: o que ficou de fora — e por quê", "leituras executivas em risco"). Parser tolerante: diário fora do formato vira matéria corrida — o jornal nunca quebra. Os links "ver o Radar completo" da capa e da entrada (PT/EN) apontam para o jornal.
- **IA (A3)**: agente **Claude Code (Anthropic)** como UX/UI e implementador; validação do editor sobre o site real (hoje + 1 dia).

### Edição 0.64 — 2026-08-01 · companion 100% bilíngue (spec 070)
- **Feature spec-kit oficial `070-companion-en`**: fechada a limitação declarada na 067 — **todas** as strings visíveis do widget (paleta, tour, Bastidores, sugestão, BYOK, plano de ensino, tooltips, erros, até o separador decimal dos tokens) passam por `tx(pt, en)`: 120 chamadas, PT byte-idêntico, sem sombreamento de `tx` (a lição do fix de 01/08 virou guarda-corpo do ciclo).
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.63 — 2026-08-01 · revisão de nivelamento: a porta de entrada alargada (spec 069)
- **Feature spec-kit oficial `069-nivelamento`** (origem: parecer editorial simulado para busca de editora): os caps. 00–02 ganharam **chão sem perder teto** — ponte "por que o ChatGPT responde mas não resolve" e seção **"Como ler este livro — três portas de entrada"** (00); a imagem-âncora do "profissional no primeiro dia" + as quatro peças numa tarefa real + preâmbulo leigo da metodologia (01); **um turno completo em câmera lenta** (7 passos) antes do vocabulário técnico (02). Glosas de "janela de contexto" e "tool call" no primeiro uso. Nada removido: as adições são pontes.
- De brinde, a revisão pegou uma desatualização real: os caps. 00/01 ainda diziam **dezesseis** sistemas — corrigido para **dezoito** com Grok Build e Pi nas listas.
- **Delta traduzido no mesmo ciclo** (regra da 067): os 3 capítulos EN espelhados, hashes renovados, selos de sincronia verdes.
- **IA (A3)**: agente **Claude Code (Anthropic)** atuando como editor-revisor; curadoria humana.

### Correção 2026-08-01 · o banner de consentimento nunca aparecia
- **Defeito de uma linha, efeito silencioso**: em `publicar/tema/companion.js`, dentro de `montarBanner()`, uma variável local `var tx` sombreava a função `tx(pt, en)` do escopo do módulo. Como `var` é içado para o topo da função, na linha seguinte `tx` já era um elemento DOM, e a chamada `tx("Entendi e aceito", …)` lançava `TypeError` — em **PT e EN**, no carregamento de toda página.
- **Consequência**: `montarBanner()` abortava e, com ele, a `telemetria()` chamada logo depois no mesmo bootstrap. Ou seja, (1) **nenhum leitor novo viu o banner de consentimento** e (2) **nenhum evento de navegação foi registrado** por quem não consentisse pelo painel do chat. **Os números do [Apêndice — Uso do livro](apendice-uso.md) subcontam** o período anterior a esta correção; leia-os com essa ressalva.
- **Por que passou despercebido**: o cartão de consentimento *dentro* do painel do chat usa a função `tx` correta e seguia funcionando — o caminho testado à mão estava íntegro; o quebrado era o que aparece sozinho, sem clique.
- **Verificação** (Chromium/Playwright sobre o `docs/` construído, antes e depois): antes, `['tx is not a function']` e banner ausente nas duas edições; depois, nenhum erro e banner presente. Build verde: 18 capítulos + aparato em PT e EN.
- **Origem do achado**: o motor foi portado para outro livro vivo, e o mesmo defeito apareceu lá — reuso como forma de teste.
- **IA (A3)**: agente **Claude Code (Anthropic)**; diagnóstico, correção e verificação. Enquadrada como correção trivial (exceção do Princípio VII), com decisão humana explícita.

### Edição 0.62 — 2026-07-31 · o livro fala inglês (spec 067)
- **Feature spec-kit oficial `067-livro-en`**: o livro vira **multiidioma** — rodada inglês, em [`/en/`](https://ghdaru.github.io/harness_engineering/en/) espelhado com slugs ingleses. **27 páginas traduzidas** (18 capítulos + benchmark + aparato) por 6 agentes em paralelo sob contrato de tradução (glossário fixo, seções canônicas, estrutura 1:1 verificada, citações em inglês verbatim).
- **PT permanece a fonte canônica; a tradução é artefato derivado com selo de sincronia**: cada fonte EN declara `fonte+edição+hash` do original; o build compara com o PT atual e mostra "in sync" ou o aviso âmbar de tradução atrasada — dívida de tradução é sempre visível, e o portão de qualidade falha se o selo mentir. Regra permanente: toda spec que edite `livro/` inclui o passo "traduzir o delta".
- **UX**: seletor PT·EN (pill textual, sem bandeiras) em todas as páginas, levando à MESMA página no outro idioma; preferência gravada; capa PT com navegador em inglês ganha convite discreto (nunca redirect); `hreflang` correto. Ficam em PT com aviso: Histórico, Radar e o conteúdo do card de news (registros operacionais).
- **Paridade**: PDFs e Markdown completos EN (`harness-engineering.pdf/.md`) no mesmo CI; grafo interativo com rótulos/URLs ingleses; superfície principal do companion em EN (demais strings do widget: limitação conhecida). RAG segue só no PT canônico.
- **IA (A3)**: agente **Claude Code (Anthropic)** (motor i18n + 6 tradutores-agentes); decisões de UX e curadoria humanas.
- 🏷 **Release congelada** (spec 068): [GitHub v0.62.0](https://github.com/GHDaru/harness_engineering/releases/tag/v0.62.0) · **DOI desta versão: [10.5281/zenodo.21724433](https://doi.org/10.5281/zenodo.21724433)** (o DOI-conceito 10.5281/zenodo.21632412 segue resolvendo para a versão mais recente). Mecanismo permanente: release = commitar `releases/vX.Y.Z.md` na main (o CI cria tag e Release; o Zenodo cunha o DOI).

### Edição 0.61 — 2026-07-31 · leitura integral verificada: as citações agora são do texto (spec 066)
- **Feature spec-kit oficial `066-papers-integrais`**: o editor liberou o arXiv na política de rede do Environment (acesso completo — registrado no diário do Radar como **a única exceção até o momento**, pela dinâmica do livro vivo) e os dois preprints da edição 0.60 foram **relidos na íntegra** pelos mesmos agentes, com mandato de deltas verbatim.
- **Cap. 11 corrigido**: duas frases que circulavam como citação do paper da AI2 eram **paráfrases de agregadores** — substituídas pelo verbatim real (§4.3 e §5.2), com os números das Tabelas 1–3 (evolução de harness piora o GPT-5.4 sem testes unitários; held-out +0,6). Lição de método no diário: paráfrase de agregador vira "citação" em um dia de circulação.
- **Cap. 04 corrigido e ampliado**: ganho do GLM-4.7-Flash era +5,5/+6,8 (não "+3,1"); nuance de baseline explicitada; e o achado pró-harness da Tabela 1 — **trocar só o sumarizador move +6,5 pontos** ("compaction is a performance-critical decision process") — devolve à tese do capítulo o que a "terceira via" parecia tirar.
- **Bibliografia**: os dois itens perdem a ressalva "texto integral pendente"; autores/afiliações completados (Tsinghua/Z.AI; AI2/UW/indep.).
- **IA (A3)**: agente **Claude Code (Anthropic)**; decisão de rede e curadoria humanas.

### Edição 0.60 — 2026-07-31 · os papers do Radar entram no livro + conferência A2A (spec 065)
- **Feature spec-kit oficial `065-papers-a2a`**: promoção dos dois itens restantes da varredura de 2026-07-31. Três agentes de leitura; **arXiv bloqueado no ambiente** (registrado no diário do Radar) ⇒ dois papers avaliados pelo abstract com marcação explícita; o survey **lido na íntegra** (62 pp.).
- **Cap. 04** ganha o adendo "a terceira via": [CompactionRL](https://arxiv.org/abs/2607.05378) — compactação **aprendida no treino** (RL com sumarização no loop, recompensa de tarefa, +7,0 Pass@1 SWE-bench Verified) e a limitação reveladora: ganhos não transferem sem compactação ⇒ acoplamento modelo↔harness — o argumento mais forte até agora para a compactação nativa de provedor.
- **Cap. 11** ganha o adendo "três regras": [Rethinking the Evaluation of Harness Evolution](https://arxiv.org/abs/2607.12227) (AI2/UW) — evolução automática de harness não supera test-time scaling sob orçamento equiparado; regras (orçamento equiparado, held-out, benchmark sensível a design) adotadas como dever de casa do próprio benchmark do livro (validade convergente).
- **Bibliografia**: 3 itens novos — incluindo o survey **Agent Systems with Harness Engineering** (RUC, maio/2026, OpenReview — a busca o datara de julho; corrigido no diário), com nota de rigor (sem limitações declaradas, sem metodologia de survey, n=3 sistemas) e o mapeamento taxonomia-a-taxonomia (converge no scaffold; diverge em permissões/extensibilidade/interfaces — fortes aqui, futuras lá; treinamento agêntico — forte lá, ausente aqui).
- **Cap. 17**: conferência do A2A concluída — v1.0 já estava coberto; adendo enriquecido (3 camadas, v1.0.1 com **mecanismo formal de extensões**, fonte primária) e a simetria editorial: MCP e A2A chegaram no mesmo trimestre a "extensões formais em vez de features no núcleo".
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.59 — 2026-07-31 · o corpus cresce: Grok Build e Pi (rodada ext-1, spec 064)
- **Feature spec-kit oficial `064-corpus-ext`**: primeira **promoção Radar→corpus** — o Radar achou (varredura de 2026-07-31), o editor aprovou e forkou, dois agentes de leitura varreram os clones congelados e o instrumento padrão (HARNESS_EVAL) foi aplicado. Corpus: 16 → **18**; rodada **ext-1**, sem tocar as fotos das rodadas 1/2.
- **[Grok Build (xAI)](../benchmark/avaliacoes/grok-build.md): 35/36** — plataforma máxima; ⭐ em permissões (autorização de shell por **AST** tree-sitter + sandbox kernel-enforced fail-closed), subagentes (**worktrees CoW/BTRFS confirmadas no código**) e extensibilidade (compat poliglota: lê artefatos de Claude/Cursor e porta tools do codex/opencode). Distintivo: workflows Rhai com **replay determinístico**. Gap: zero evals comportamentais.
- **[Pi (Earendil)](../benchmark/avaliacoes/pi.md): 26/36** — o contraponto minimalista que faltava (caso deliberadamente atípico, lógica de replicação de Yin): 3 em tudo que aceita (compactação ⭐ — a mais completa do corpus; extensibilidade ⭐ com 28 eventos), 0–1 no que recusa por manifesto (MCP/permissões/plan/subagentes) — cada recusa provada por extensão de exemplo testada. A alegação "system prompt <1k tokens" foi **medida**: ~460 tokens na base, mas os AGENTS.md concatenam sem orçamento (~6× o slogan no próprio repo do Pi).
- Livro: caixa "**o contraponto: o harness mínimo**" no cap. 03 + entrada no Apêndice A; adendo "worktrees como infraestrutura" no cap. 10 + entradas no Apêndice A; seção ext-1 no apêndice do estudo; comparativo e `notas.json` com as colunas novas; grafo com os nós grok-build e pi.
- **IA (A3)**: agente **Claude Code (Anthropic)** (leitura de código por subagentes; notas julgadas contra a régua das rodadas 1/2); curadoria e aprovação humanas.

### Edição 0.58 — 2026-07-31 · harness-um: o livro inteiro, executável (spec 063)
- **Feature spec-kit oficial `063-harness-um`**: nasce a **implementação de referência** do livro — [`harness-um/`](../harness-um/README.md), um pacote Python com as features dos capítulos 02–13 num sistema coeso: loop com orçamento (02), contexto em camadas (03), compactação (04), ferramentas com esquema pela assinatura (05), cliente MCP stateless pós-2026-07-28 (06), política permitir/perguntar/negar (07), MEMORIA.md + sessões JSONL (08), plano-artefato (09), subagente só-leitura com contexto limpo (10), verificação pós-mutação (11), ganchos vetáveis + habilidades SKILL.md (12) e REPL (13). **Linguagem ubíqua em português** (o código fala a língua do livro; a borda `provedores.py` é a camada anticorrupção). 19 testes offline via `ProvedorEco`, rodando no CI a cada push.
- **Nome**: "harness-um" (progressão do harness-zero) — decisão do editor após o alerta de colisão: "OpenHarness" já é um sistema do corpus (HKUDS). O apêndice registra a escolha.
- Novo [apêndice](apendice-harness-um.md) com a **figura oficial** (núcleo "1" âmbar + anel de 12 segmentos = capítulos 02–13), a tabela da linguagem ubíqua e o "como baixar e rodar".
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria e decisões de nome/hospedagem humanas.

### Edição 0.57 — 2026-07-31 · o jornal chega à capa: novidades no splash (spec 062)
- **Feature spec-kit oficial `062-news-capa`**: correção de alvo da 061 — o pedido era a **capa** (`index.html`). O splash agora exibe, entre os CTAs e os créditos: (1) **destaque** — card âmbar `splash-news` com a última notícia do Radar (data, badge de impacto, link "ver o Radar completo"); (2) **menos destaque** — linha `splash-vedicao` "📖 Nesta edição". Mesmas fontes e mesma postura da 061 (parse falho ⇒ bloco omitido); o bloco da entrada permanece como aprovado. Portão novo: fonte parseia ⇒ a capa noticia.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.56 — 2026-07-31 · news na entrada: a última do Radar + a edição corrente (spec 061)
- **Feature spec-kit oficial `061-news-entrada`**: a entrada do livro ganhou uma faixa de **jornal vivo**, derivada no build sem curadoria extra: (1) **destaque** — card âmbar com a notícia mais recente e relevante do [Radar](../radar/RADAR.md) (data, impacto, item com link e "ver o Radar completo"); (2) **menos destaque** — a linha "📖 Nesta edição (vX.Y.0 · data): título — Histórico", parseada da última entrada deste arquivo. **Auto-atualização estrutural**: o agente diário escreve no RADAR ⇒ a capa muda no build seguinte; edição nova aqui ⇒ idem. Parse falhou ⇒ bloco omitido (a entrada nunca quebra).
- Verificação: e2e 4/4 (conteúdo real do MCP 2026-07-28, impacto A, versão e link do Histórico) + screenshot.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.55 — 2026-07-31 · MCP 2026-07-28: o primeiro gatilho extraordinário exercido (spec 060)
- **Feature spec-kit oficial `060-mcp-2026-07-28`**, promovida do **Radar** (diário 2026-07-31, impacto A) — o fluxo do ADR 0007/0008 funcionando de ponta a ponta: aviso → pesquisa com fontes oficiais → registro no radar → spec → revisão.
- **Cap. 06**: nova seção "§6 A guinada stateless — a spec 2026-07-28" (fim do handshake `initialize` e do `Mcp-Session-Id`; MRTR no lugar de sampling/elicitation; extensões formais; cache `ttlMs` como contrato; primeira política de depreciação — 12 meses — cobrindo Sampling/Roots/Logging/HTTP+SSE/DCR→CIMD); **Leitura executiva reescrita** (o que a coorte roda × o que se escreve hoje); "o que roubar" corrigido (fallback SSE agora é depreciado); fonte oficial adicionada; revisão 2026-07-31.
- **Cap. 17**: adendo — a guinada stateless + política de depreciação como sinal de protocolo em fase de infraestrutura. **Etapa 07 do harness-zero**: nota de época na docstring (o handshake ensinado é o protocolo 2025-06). **Cap. 04**: `ttlMs` como o protocolo absorvendo cache. **Glossário/motor**: MRTR, CIMD e DCR. **Bibliografia**: release verificada por fetch direto.
- **IA (A3)**: agente **Claude Code (Anthropic)**; gatilho reportado pelo editor humano; fontes verificadas nesta sessão.

### Edição 0.54 — 2026-07-31 · favicon (spec 059)
- **Feature spec-kit `059-favicon`**: o site ganhou favicon na identidade do livro — **núcleo âmbar (o modelo) envolto pelo anel segmentado (o harness)**, a mesma metáfora da capa e do diagrama do cap. 00. `favicon.svg` (nítido em qualquer escala) + PNG 32px + apple-touch-icon 180px, nos dois templates (páginas e splash). Conferido visualmente em 16/32/180px nos dois fundos.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.53 — 2026-07-30 · contador de visitas no rodapé (spec 058)
- **Feature spec-kit oficial `058-contador-visitas`**: o clássico contador de visitas, do jeito honesto — o rodapé de todas as páginas ganha o chip `📈 N visitas registradas`, alimentado pelo **agregado público da telemetria consentida** (`/telemetry/publico`, spec 055), com cache por sessão de leitura (1 requisição/10 min) e **link para o Apêndice — Uso do livro** (o contador como porta de entrada da página de transparência). Sem número na capa e sem "você é a visita #N" — visitantes sem consentimento não contam, então não existe ordinal verdadeiro a atribuir. Backend fora do ar ⇒ o chip simplesmente não aparece.
- Verificação: e2e 6/6 (chip com total e link; cache na 2ª página sem novo fetch; ausência silenciosa sem backend).
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.52 — 2026-07-30 · Knowledge Graph do livro: apêndice interativo, sempre em sincronia (spec 057)
- **Feature spec-kit oficial `057-knowledge-graph`** (ciclo specify→plan→tasks→implement): novo aparato [Apêndice — Grafo do livro](apendice-grafo.md), com o mapa de conexões do livro **interativo** (força dirigida em canvas, JS puro, zero dependências): 4 tipos de nó (18 capítulos · 16 sistemas do corpus · 6 conceitos · 13 etapas do harness-zero) e arestas com peso = menções reais no texto. Interações: arrasto, zoom, hover, clique (isola a vizinhança + painel com link para a página), filtros por tipo.
- **O sincronismo é estrutural, não processo**: a extração (`publicar/grafo.mjs`) é **determinística, sem LLM**, e roda dentro do `npm run build` — toda mudança publicada do livro regenera o grafo (52 nós / 324 arestas nesta edição). O portão de qualidade agora falha o build se o grafo regredir (18 capítulos, ≥40 nós, ≥100 arestas). Cada aresta é evidência textual verificável (Princípio I aplicado a visualização).
- Verificação: e2e Playwright 7/7 (dados, filtros, clique/painel/link) + screenshots nos 2 temas; build/portão/corpus verdes.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.51 — 2026-07-29 · radar diário: o livro vigia o próprio ecossistema (spec 056)
- **Feature spec-kit oficial `056-radar-diario`** ([ADR 0008](../adr/0008-radar-diario-automatizado.md)): uma **sessão-agente agendada (1×/dia)** busca novidades do ecossistema (releases do corpus, protocolos, papers, ferramentas candidatas), avalia impacto por capítulo/Leitura executiva e mantém o **roadmap de auto-atualização** em [`radar/RADAR.md`](../radar/RADAR.md), com o bruto diário auditável em `radar/diario/`. O contrato do agente é versionado em [`radar/AGENTE.md`](../radar/AGENTE.md) — **escrita somente em `radar/`**; promover item a mudança no livro continua exigindo spec-kit com curadoria humana (a fronteira de autonomia dos caps. 07/16 aplicada ao próprio projeto). O radar é a fila de entrada do gatilho extraordinário do ADR 0007.
- **IA (A3)**: agente **Claude Code (Anthropic)**; decisão registrada em ADR com alternativas.

### Edição 0.50 — 2026-07-29 · Apêndice — Uso do livro (vivo) (spec 055)
- **Feature spec-kit oficial `055-apendice-uso-vivo`** (ciclo specify→plan→tasks→implement): o livro passa a **expor a própria telemetria** — novo aparato [Apêndice — Uso do livro](apendice-uso.md), com uma **ilha viva** (`data-viz="uso-livro"`, JS puro) que consome o novo `GET /telemetry/publico`: projeção **estritamente agregada** (total, páginas distintas, contagens por página — sem sessões, sem timestamps, por isso pública). A página explica o que é medido e o que não é (consentimento da spec 054, sessões anônimas, direito ao esquecimento) e conecta o painel à cadência do livro vivo (ADR 0007): atenção dos leitores orienta a prioridade de revisão. No PDF a ilha é omitida (regra existente), com aviso no texto.
- Verificação: suíte do backend 14/14 (teste do agregado público sem campos sensíveis); e2e com backend semeado (KPIs, barras, títulos legíveis, nota de privacidade) e fallback honesto sem backend; build/portão/corpus verdes.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.49 — 2026-07-29 · experiência educacional: consentimento, onboarding, telemetria e plano de ensino (spec 054)
- **Feature spec-kit oficial `054-experiencia-educacional`** (ciclo specify→plan→tasks→implement):
  - **Consentimento com aceite gravado**: banner em todas as páginas (e cartão no chat, que fica bloqueado até o aceite) avisa que as conversas alimentam o **aprimoramento vivo do livro** e que **dados pessoais não devem ser compartilhados**; o aceite é versionado e gravado no navegador **e** no backend (tabela `consents`, sessão anônima, `ON DELETE CASCADE` — LGPD preservada).
  - **Onboarding**: tour de 5 passos com spotlight (navegação, cabeçalho/downloads, companion, Bastidores, `/plano`), oferecido após o aceite, 1× por navegador, revisitável com **`/tour`**; passos sem alvo na página são pulados.
  - **Telemetria de navegação**: só após o aceite (verificado também no servidor), cada página envia `{sessão anônima, slug}` via sendBeacon → tabela `nav_events`; resumo por página em `GET /telemetry` (ADMIN_TOKEN) — insumo de quais capítulos merecem a próxima revisão. Sem IP/UA persistidos.
  - **Objetivo + plano de ensino**: **`/plano <objetivo>`** grava o objetivo do leitor (tabela `goals`) e pede ao tutor um plano pelos capítulos e etapas do harness-zero; com objetivo gravado, **toda conversa** ganha a camada "Objetivo declarado do leitor" no system prompt (o cap. 03 em ação) e os Bastidores o exibem.
- Verificação: suíte do backend 13/13; e2e Playwright com **14 checagens verdes** (aceite bloqueia/libera, tour navega e não repete, beacon grava só pós-consent, objetivo chega ao prompt e aos Bastidores). Três bugs reais pegos pelo e2e e corrigidos (bootstrap duplo, `[hidden]` × flex, banner sobrepondo o cartão de aceite).
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.48 — 2026-07-29 · chat repaginado: dock, paleta de comandos, tooltips e Bastidores (spec 053)
- **Feature spec-kit oficial `053-chat-ux`** (ciclo completo specify→plan→tasks→implement; gate humano com 3 padrões de tela aprovados): o companion ganhou uma repaginação de usabilidade em quatro frentes:
  - **Layout**: painel flutuante ampliado (480px×78vh) + **modo ancorado** (sidebar direita que empurra o conteúdo — leitura e conversa lado a lado) + **maximizar** (640px); estado persiste entre páginas; mobile vira tela cheia.
  - **Entrada**: textarea de 3 linhas com auto-crescimento, linha de dicas e botão **Enviar** rotulado.
  - **Explicabilidade**: chips de capacidade com **tooltip** (descrição + "libera no cap. X", dados do `/capabilities`); **paleta de `/`** com os cinco comandos descritos, filtro por prefixo e navegação por teclado.
  - **Bastidores** (o livro se demonstrando): barra de status com `~tokens · chamadas · trechos` e painel com Janela de contexto (barra de ocupação), **o que foi injetado no turno** (trechos RAG com fonte), Memória da sessão, e aba **Documentos** (downloads do capítulo + fontes citadas). Backend expõe o bloco `debug` (aditivo) no `/chat` e no stream — tokens sempre estimados (~chars/4), honestamente marcados.
- Verificação: suíte do backend 12/12 (teste novo do `debug`); e2e Playwright com 18 checagens verdes (estados persistem, paleta, tooltip, bastidores com dados reais, regressão de stream/sugestão/BYOK).
- **IA (A3)**: agente **Claude Code (Anthropic)**; padrões de tela aprovados pelo editor.

### Edição 0.47 — 2026-07-29 · cadência do livro vivo declarada (spec 052)
- **Feature spec-kit oficial `052-cadencia-livro-vivo`** ([ADR 0007](../adr/0007-cadencia-livro-vivo.md)): o livro agora tem **política explícita de revisão** — janela **trimestral** (próxima: **2026-10**; re-sync dos 16 forks, diff por dimensão, Apêndices A + placar) e **gatilho extraordinário**: qualquer evento que invalide uma "Leitura executiva" dispara revisão pontual do capítulo, sem esperar a janela. A Leitura executiva (C08) vira o contrato observável de frescor. Guia Editorial ganhou a seção operacional; `publicar/README` atualizado ao estado real do motor; branches mergeadas podadas.
- **IA (A3)**: agente **Claude Code (Anthropic)**; política decidida em ADR com alternativas.

### Edição 0.46 — 2026-07-29 · auditoria editorial rodada 2: 27 correções (spec 051)
- **Feature spec-kit oficial `051-auditoria-rodada2`**: 4 auditores (subagentes) leram o livro inteiro em paralelo; 27 achados confirmados e corrigidos. O mais grave: o **cap. 02 estava truncado no meio do Apêndice A desde a reescrita v3** (entrada do IronClaw cortada; Aider, OpenHands, ohmo, n8n e frameworks ausentes) — reconstruído a partir da evidência do benchmark. Demais: cap. 01 §5 realinhado ao corpus real (quatro arquétipos), caps. 15–17 na estrutura do cap. 00, exercícios dos caps. 05/06/07/09/12 realinhados ao harness-zero real, `StorePort` nos caps. 08/13, ACP-IBM desambiguado (cap. 10), contagens do cap. 17 e do glossário corrigidas, e uma dúzia de consertos de português/consistência. Detalhe completo na spec.
- **IA (A3)**: agente **Claude Code (Anthropic)**; achados verificados um a um contra o fonte antes de corrigir.

### Edição 0.45 — 2026-07-29 · bibliografia 100% verificada (spec 050)
- **Feature spec-kit oficial `050-bibliografia-verificacao`** (Princípio I — evidência acima de retórica): os **16 itens ⏳** da Bibliografia foram verificados por **busca web independente nesta sessão** e promovidos a ✓ com dados completos (autores, veículo, páginas, ISBN/DOI). Duas correções encontradas e registradas: o arXiv 2509.18661 é o ***Agentic* AutoSurvey** (Liu et al.), não o AutoSurvey original; e o ISBN 9780226595146 do *Developmental Editing* (Norton) é da **1ª ed. 2009** (a 2ª ed. 2023 tem ISBN 9780226793634). A URL da entrada de Peer Review (Baldwin, CMU ETHOS) foi corrigida. **A fila de pendências da Bibliografia está zerada.**
- **IA (A3)**: agente **Claude Code (Anthropic)**; verificação por busca cruzada com fontes independentes.

### Edição 0.44 — 2026-07-29 · rate-limit persistente (spec 049)
- **Feature spec-kit oficial `049-rate-limit-persistente`**: o limite de mensagens **por sessão** agora deriva do **store** (`count_since` sobre as mensagens persistidas — porta que existia desde a spec 016 nos dois adapters): **sobrevive a deploys do Railway e vale entre instâncias**, sem tabela nova. O deque em memória virou guarda secundária **por IP** (`RATE_LIMIT_MSGS × RATE_LIMIT_IP_FACTOR`, default 3×) contra abuso multi-sessão, e segue limitando sugestões. BYOK continua isento. Trade-off registrado: `delete_session` (LGPD) zera a contagem — privacidade > contabilidade; a guarda por IP cobre o atalho.
- Verificação: teste novo simula restart (deque limpo) e o 429 por sessão continua vindo do store; suíte 11/11.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.43 — 2026-07-29 · BYOK no widget (spec 048)
- **Feature spec-kit oficial `048-byok-widget`**: o leitor pode usar a **própria chave de API** no companion — comando **`/chave`** abre um campo `password` discreto (mesmo padrão sob-demanda da sugestão); a chave fica **só no localStorage do navegador**, mascarada (`…últimos 4`), vai como `byok_key` no `/chat` e `/chat/stream` (o backend já a tratava como efêmera e isenta do rate-limit — specs 016/017), e some com `/chave limpar` ou um clique no selo 🔑 do cabeçalho. A mensagem de limite (429) agora ensina o comando.
- Verificação e2e (uvicorn echo + Chromium): payload com/sem `byok_key` conferido na rede; a chave nunca aparece em texto claro na conversa.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.42 — 2026-07-29 · companion com streaming SSE (spec 047)
- **Feature spec-kit oficial `047-companion-sse`**: as respostas do tutor agora chegam **em streaming** — novo `POST /chat/stream` (`text/event-stream`, eventos `{delta}`/`{trace}`/`{done}`/`{erro}`), `stream()` nos dois adapters de LLM (SSE OpenAI-compatible com agregação de tool_calls por índice; Echo em pedaços, testável sem rede) e `run_turn_stream()` no loop (mesmo freio `MAX_TURNS`, mesmo trace). O widget consome via `fetch`+`ReadableStream`, renderiza incrementalmente (markdown aplicado ao final) e **cai no `/chat` clássico** em falha de transporte — falha do modelo no meio do stream não refaz a chamada (evita duplicar o turno persistido).
- Verificação: suíte do backend 10/10 (novo teste do stream com Echo: deltas + done ≡ histórico persistido); ponta a ponta real com uvicorn local + widget no Chromium (render incremental e markdown final conferidos).
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.41 — 2026-07-29 · a obra ligada ao Awesome Harness Engineering (spec 046)
- **Feature spec-kit oficial `046-awesome-list-obra`** (criada pelo script `.specify/create-new-feature.sh`): a coleção viva **[Awesome Harness Engineering](https://github.com/GHDaru/awesome-harness-engineering)** (curada pelo autor, organizada por problema — a mesma taxonomia do livro) agora é referenciada em toda a obra:
  - **"Consulte também"** ao fim das Fontes da indústria dos caps. 02–13 e 17, apontando para a **seção específica** da lista (Agent Loop, Context Delivery, Tool Design, Skills & MCP, Permissions, Memory, Planning, Orchestration, Verification, DX, Human-in-the-Loop…);
  - caps. 14/15/16 (sem seção de fontes): nota antes da Verificação (Foundations, Production Infrastructure, Skills & MCP);
  - cap. 00 (Os harnesses do estudo), cap. 01 §5 e Apêndice do estudo (→ Reference Implementations);
  - **Bibliografia**: nova seção "Coleções vivas" com a entrada da lista.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.40 — 2026-07-29 · download do livro: PDF e Markdown, completo e por capítulo (spec 045)
- **Feature spec-kit oficial `045-downloads`**:
  - **Livro completo**: a entrada ganhou os botões **⬇ PDF** (`pdf/engenharia-de-harness.pdf`, capa + rodapé paginado) e **⬇ Markdown** (`md/engenharia-de-harness.md`, concatenação na ordem do sumário com cabeçalho de versão/DOI — útil inclusive para alimentar LLMs).
  - **Por capítulo**: o cabeçalho de cada capítulo (C01) ganhou os chips **⬇ md** (fonte exata) e **⬇ pdf** (avulso com título, datação e rodapé paginado) — 18 PDFs gerados no CI.
  - **Correção**: o PDF completo tinha perdido os títulos de capítulo após a spec 043 (o `h1` saiu do `<article>`); o gerador agora injeta o título do sumário + linha de datação do cabeçalho. O painel Leitura executiva (C08) também ganhou estilo de impressão.
  - **CI**: o workflow instala Chromium (Playwright) e gera os PDFs após o build; o portão por capítulo confere links e artefatos de download.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.39 — 2026-07-29 · correções do editor: contagem de arquétipos + sugestão sob demanda + Gmail
- **Feature spec-kit oficial `044-correcoes-cap00-sugestoes`**:
  - **Cap. 00**: a contagem agora bate com a lista — "**quatro** arquétipos" (código, agentes pessoais self-hosted, embutidos, frameworks). A taxonomia própria do cap. 01 §5 (três, com 3 itens) permanece.
  - **Companion — sugestão sob demanda**: o formulário "enviar ao autor" **não aparece mais por default** (corrigido inclusive um bug de CSS que o deixava sempre visível) e o botão 💡 permanente saiu do cabeçalho. Ele abre quando o leitor pede no chat: comando **`/sugerir`** ou intenção explícita ("quero enviar uma sugestão ao autor"); a solicitação é resolvida no widget, sem passar pelo tutor. As boas-vindas mencionam o comando.
  - **Email via Gmail**: [`chat-companion/backend/EMAIL.md`](../chat-companion/backend/EMAIL.md) documenta a configuração (senha de app do Google + variáveis `SMTP_*` no Railway; remetente = conta do autor, destinatário = `SUGGESTION_EMAIL_TO`). Nenhuma credencial no repositório.
- **IA (A3)**: agente **Claude Code (Anthropic)**; revisão editorial humana.

### Edição 0.38 — 2026-07-28 · design system dos capítulos: C01 + C08 + N02 (spec 043)
- **Feature spec-kit oficial `043-template-capitulos`** ([ADR 0005](../adr/0005-template-capitulos-um-spec.md) e [ADR 0006](../adr/0006-design-system-componentes.md)): o catálogo de componentes ([`publicar/DESIGN-SISTEMA.md`](../publicar/DESIGN-SISTEMA.md)) ganhou os três componentes que faltavam, todos aprovados em **gate humano** (página-espécime + 3 modelos por componente):
  - **C01 CabeçalhoDeCapítulo — variante B "faixa editorial"**: kicker da parte, título, teaser, número em marca d'água, datação absorvida (C02) e **tempo de leitura estimado**; o `h1` e o blockquote de datação do Markdown saem do corpo (sem duplicação). Só páginas de capítulo numeradas; o aparato mantém o selo clássico.
  - **C08 LeituraExecutiva — V1 "painel âmbar"**: a seção `### Leitura executiva` (16 capítulos) vira painel destacado com rótulo em versalete; âncora preservada.
  - **N02 PaginaçãoEmCartões — V2 "cartões com badge"**: anterior/próximo na linguagem dos cartões da entrada (badge numerado = "clique para ir a um capítulo").
- **Portão novo por capítulo** ([ADR 0005](../adr/0005-template-capitulos-um-spec.md)): `publicar/verifica-capitulos.mjs` confere os 18 capítulos (badge correto, `h1` único, datação absorvida, C08 aplicado) e as 7 páginas de aparato — falha encerra com erro.
- **IA (A3)**: agente **Claude Code (Anthropic)**; direção de arte e aprovações (B/V1/V2) humanas.

### Edição 0.37 — 2026-07-28 · harness-zero: etapa 12 — skills (cap. 16) — TRILHA COMPLETA
- **Feature spec-kit oficial `042-harness-zero-etapa12`**: o harness que **aprende — com freio**. `salvar_skill(nome, quando_usar, conteudo)` captura procedimentos como skills, mas a skill **nunca entra em vigor sozinha**: vai para `skills/pendentes/` (**auto-aprovação = prompt injection persistente**, o anti-padrão central do cap. 16); o humano **aprova** (`POST /skills/aprovar`) ou rejeita. Aprovada, entra como **camada nova do MontadorDeContexto** (etapa 03 pagando dividendos) — **só nome + quando usar** no prompt; o conteúdo completo vem sob demanda via `ler_skill` (**progressive disclosure**, cap. 04). Smoke com asserções: pendente fora do contexto; aprovada dentro (índice apenas); conteúdo via tool.
- **🏁 Com esta etapa, a trilha prática fecha o mapa completo: etapas 00–12** — loop, tools (schemas derivados), contexto em camadas, sessões, compactação, permissões+aprovação, MCP, plan mode, subagentes, evals (replay+juiz), hooks e skills. As doze dimensões do livro, construídas do zero, cada etapa autocontida e verificada.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.36 — 2026-07-28 · harness-zero: etapa 11 — hooks (cap. 12)
- **Feature spec-kit oficial `041-harness-zero-etapa11`**: extensibilidade sem tocar no loop. **Hooks** em duas fronteiras estáveis da execução de ferramentas — `pre_tool` (pode **bloquear** ou **ajustar args**) e `post_tool` (pode **transformar o resultado**) — envolvendo `registro.executar` em todos os caminhos (loop, aprovação, subagente). Dois hooks de exemplo com dor real: **auditoria** (cada chamada vira linha estruturada em `auditoria.jsonl`; janela `GET /auditoria`) e **redator** (mascara padrões de segredo — `nvapi-…`, `password=` — antes de o resultado chegar ao modelo; defesa em profundidade somada à política da etapa 06). Smoke: redação, bloqueio e log verificados.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.35 — 2026-07-28 · harness-zero: etapa 10 — evals do harness (cap. 11)
- **Feature spec-kit oficial `040-harness-zero-etapa10`**: o harness aplicado a si mesmo. Suíte `evals/` com **`ReplayAdapter`** — **respostas gravadas** em `.jsonl` reproduzidas em ordem: o eval testa o **harness** (política, plan mode, escada de compactação, derivação de schema, **pausa de aprovação**: a gravação pede `write_file` e nada é escrito sem o humano), nunca o humor do modelo. **`juiz.py`** — LLM-as-judge atrás do mesmo `LLMPort` (nota+justificativa por critérios; com echo degrada honestamente, com chave real julga). 6/6 verdes.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.34 — 2026-07-28 · harness-zero: etapa 09 — subagentes (cap. 10)
- **Feature spec-kit oficial `039-harness-zero-etapa09`**: a tool **`task(descricao)`** delega a um **subagente com sessão-filha** (`task-…`): system prompt focado **só na descrição** (zero contexto do pai), **mesmo loop** com turnos limitados, ferramentas **restritas a leitura** (filha não muta o mundo; a política da etapa 06 segue por cima) — e **só o resultado final volta** ao pai como tool result. As duas fronteiras (ida: só a descrição; volta: só o resultado) são a lição do capítulo: é o que mantém o contexto do pai limpo. Filhas persistidas e visíveis em `/sessions` (a etapa 04 pagando dividendos). Smoke com asserções nas fronteiras.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.33 — 2026-07-28 · harness-zero: etapa 08 — plan mode (cap. 09)
- **Feature spec-kit oficial `038-harness-zero-etapa08`**: plan mode **imposto, não pedido**. Um **modo por sessão** (`executar`/`planejar`, `POST /modo`); em `planejar`, a **política da etapa 06 nega toda ferramenta mutante** — a mudança é **uma linha** no `decide()` (a lição: quem garante o comportamento é o mecanismo de permissões, não a boa vontade do modelo). Nova tool `propor_plano` grava o artefato **PLAN.md** revisável (`GET /plano`); aprovar o plano = trocar o modo para executar. O turno em modo planejar recebe o aviso injetado. Smoke: negação com motivo em planejar; executar volta a perguntar.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.32 — 2026-07-28 · harness-zero: etapa 07 — MCP client (cap. 06)
- **Feature spec-kit oficial `037-harness-zero-etapa07`**: o harness aprende a **plugar ferramentas dos outros**. A etapa traz um **servidor MCP de exemplo** (~60 linhas, JSON-RPC 2.0 por linha no stdio — para o leitor ver o protocolo por dentro) e o **ClienteMCP** no harness: `initialize` → `tools/list` → `tools/call`, com as tools importadas de **prefixo `mcp_`** num **RegistroComposto** (locais + MCP atrás da mesma interface — o loop não sabe de onde a ferramenta vem). A **política da etapa 06 vale para as tools MCP** (servidor externo é input não-confiável); trace distingue 🔧 local × 🔌 MCP; degradação graciosa se o servidor cair. Smoke: handshake + list + call verificados.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.31 — 2026-07-28 · harness-zero: etapa 06 — permissões (cap. 07)
- **Feature spec-kit oficial `036-harness-zero-etapa06`**: fecha a **ferida aberta desde a etapa 1** (`read_file` lia qualquer arquivo, inclusive `.env`). Nasce a **PermissionPolicy** como **domínio puro** — `decide(tool, args) → permitir | perguntar | negar`, uma função sem I/O — com **paths sensíveis fixos no código** (segurança que o usuário pode desligar não é segurança) e `write_file` exigindo **aprovação humana inline**: o turno **pausa** (pendência com id), o chat mostra [aprovar]/[negar], e o loop **retoma do ponto exato**. Negação vira **texto para o modelo** (ele explica e segue). Evolução justificada do chat congelado (a aprovação exige superfície). Smoke: política pura + pausa/aprovação/retomada verificadas.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.30 — 2026-07-28 · harness-zero: etapa 05 — compactação (cap. 04)
- **Feature spec-kit oficial `035-harness-zero-etapa05`**: a **etapa 05** (`harness-zero/etapas/05-compactacao/`) implementa a **escada de agressividade** do cap. 04: degrau 1 **trunca** resultados de ferramenta antigos, degrau 2 **poda** turnos antigos, degrau 3 **sumariza** o podado via `LLMPort` e injeta o resumo — acionada por **orçamento** de contexto (chars como proxy didático de tokens; `ORCAMENTO_CHARS` para experimentar). Lições materializadas: a escada age na **visão** enviada ao modelo, nunca no **registro** persistido (etapa 4 intacta), e **compactação avisa** (indicador 🗜 no trace — silenciosa é dívida invisível). Janela `GET /contexto_uso`. Smoke verificado (degraus 2 e 3 disparando).
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.29 — 2026-07-28 · harness-zero: etapa 04 — sessões (cap. 08)
- **Feature spec-kit oficial `034-harness-zero-etapa04`**: a **etapa 04** (`harness-zero/etapas/04-sessoes/`) paga a dívida carregada de propósito desde a etapa 0: o histórico sai da variável global. Nasce o **StorePort** (terceira porta) com dois adapters — `MemoriaStore` (o contraste didático) e **`SQLiteStore`** (persistência real: converse, mate o servidor, volte — a conversa fica). Conceito de **sessão** (`session_id` + `/sessions` + `/history` = o *resume* dos harnesses reais); **1ª evolução justificada do chat congelado** (a dimensão exigiu superfície: id no navegador + retomada do histórico). O companion roda a mesma arquitetura em produção (mesmo StorePort, adapter Postgres). Smoke verificado.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.28 — 2026-07-28 · harness-zero: etapa 03 — contexto em camadas (cap. 03)
- **Feature spec-kit oficial `033-harness-zero-etapa03`**: a **etapa 03** (`harness-zero/etapas/03-contexto/`) introduz o **MontadorDeContexto** — o system prompt montado em **camadas nomeadas** (identidade fixa → ambiente derivado → **regras do projeto via `AGENTS.md`**), **remontado a cada turno** (edite o AGENTS.md com o chat aberto e veja o comportamento mudar sem redeploy — o artefato-padrão do cap. 01 §9 em ação). Loop e ToolPort intactos (mudança de uma linha no loop); janela de observação `GET /contexto` mostra as camadas e o prompt final; o EchoAdapter passou a exibir o tamanho do system prompt. Etapa autocontida, roda sem rede.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.27 — 2026-07-28 · harness-zero: etapa 02 — ToolPort (cap. 05)
- **Feature spec-kit oficial `032-harness-zero-etapa02`**: retomada a trilha prática. A **etapa 02** (`harness-zero/etapas/02-tools/`) introduz o **ToolPort** — a segunda porta do harness: ferramentas são **funções Python tipadas** registradas por decorator (`@tools.tool`); o **JSON Schema é derivado** da assinatura + docstring (`inspect`/`typing`), curando o tédio dos schemas à mão da etapa 1 (a mesma solução dos harnesses reais: FastMCP, `function_tool`, `#[tool]`). O loop não mudou — é assim que uma porta paga o aluguel. Endpoint `/tools` como janela de observação; parâmetros com default viram opcionais no schema (verificado). Etapa autocontida; roda com echo (sem rede).
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.26 — 2026-07-28 · companion: corpus atualizado + apagar conversa
- **Feature spec-kit oficial `031-companion-atualizacoes`**: o **`corpus.json`** do companion foi **regenerado** (618 blocos) — o tutor volta a citar o livro **atual** (Fundamentos novo, Glossário, Apêndice do estudo, caps 14–17 revisados). Prática registrada: regenerar o corpus a cada mudança relevante do livro (roadmap R2; automação via CI fica como evolução).
- **Widget**: novo botão **🗑 Apagar a conversa** (CO2 do roadmap) — confirma, chama `DELETE /session/{id}` (LGPD) e reinicia o chat localmente.
- **IA (A3)**: agente **Claude Code (Anthropic)**; curadoria humana.

### Edição 0.25 — 2026-07-28 · formato editorial v3 nos caps 00, 14–17 + siglas inline (auditoria)
- **Feature spec-kit oficial `030-formato-editorial`** (O005 da auditoria): os capítulos **pré-v3** foram trazidos ao formato editorial do livro (padrão do cap. 04): **14 — Convergências**, **15 — Harness Embutido**, **16 — Aprendizado e Auto-melhoria** e **17 — Protocolos** ganharam cabeçalho de data, objetivos de aprendizagem (Bloom), "O problema", estado da arte reorganizado com leitura executiva, verificação e Apêndice A (material por-repositório preservado, com link às avaliações). **Conteúdo preservado; nenhuma fonte inventada** (capítulos sem papers não ganharam seção de fundamentos — pendência honesta).
- **Cap. 00 (Introdução)**: cabeçalho de data + seção **"Os harnesses do estudo"** (O004): a **lista completa dos 16 sistemas** por arquétipo, com ponteiro ao Apêndice — O estudo e ao Comparativo (substitui a antiga "primeira rodada").
- **Siglas por extenso inline (O003)**: 1ª ocorrência de cada sigla técnica agora traz o nome por extenso no próprio texto dos caps 00–13 (46 expansões aplicadas; casos que quebravam a leitura foram tratados manualmente). O `<abbr>` continua cobrindo todas as demais ocorrências.
- **IA (A3)**: agente **Claude Code (Anthropic)** — revisão editorial (4 sub-editores em paralelo p/ 14–17) sob as regras "preserve o conteúdo; não invente fontes"; curadoria humana.

### Edição 0.24 — 2026-07-28 · PDF do livro (E08)
- **Feature spec-kit oficial `029-pdf-livro`**: novo gerador **`publicar/pdf.mjs`** — produz o **PDF completo do livro** (`docs/engenharia-de-harness.pdf`) a partir do site construído: folha de rosto (capa, autor+co-autoria de IA, versão, data, DOI), todas as partes e capítulos na ordem do sumário, CSS de impressão (A4, quebras por capítulo, rodapé com paginação). Uso: `node build.mjs && node pdf.mjs`. O PDF é artefato gerado (não versionado); pode ser anexado a cada Release/DOI.
- **IA (A3)**: agente **Claude Code (Anthropic)** — implementação; curadoria humana.

### Edição 0.23 — 2026-07-28 · Apêndice "O estudo" + fork/commit por harness + citações→Bibliografia
- **Feature spec-kit oficial `028-estudo-citacoes`** (E01+E03+E04 da auditoria): nova página **Apêndice — O estudo** (`livro/apendice-estudo.md`), no aparato: os **16 harnesses avaliados** com **origem**, versão/snapshot, **fork GHDaru + commit lido** (a data de corte materializada — reprodutibilidade do método, cap. 01 §6), data/rodada e link para a **avaliação completa** de cada um; mais o template (`HARNESS_EVAL`/`FRAMEWORK_EVAL`) e a ponte para o Comparativo.
- **Citações (MVP)**: o motor agora converte menções textuais `arXiv NNNN.NNNNN` em **link para a Bibliografia** (que linka as fontes). Decisão e evolução planejada em `adr/0004`.
- **IA (A3)**: agente **Claude Code (Anthropic)** — extração dos metadados reais das avaliações e implementação; curadoria humana.

### Edição 0.22 — 2026-07-28 · ilustração esquemática do harness (E02)
- **Feature spec-kit oficial `027-ilustracao-harness`**: o cap. 00 ganhou uma **figura esquemática (SVG flat, estilo bloco)** — o **modelo no centro** e, em volta, os seis blocos do harness (loop, contexto, ferramentas, memória, permissões, verificação) numa moldura "HARNESS (o andaime)", com o mundo (arquivos/APIs/terminal) à direita. **Theme-aware** (herda as cores do tema via CSS vars), acessível (`<title>`/`alt`/`figcaption`), sem binário (SVG versionável).
- **IA (A3)**: agente **Claude Code (Anthropic)** — desenho e integração; direção do autor ("menos futurista, mais bloco").

### Edição 0.21 — 2026-07-28 · companion: sugestões dos leitores (E05)
- **Feature spec-kit oficial `026-companion-sugestoes`**: o leitor agora pode **enviar sugestões ao autor pelo chat** (botão 💡 no widget). O backend persiste em `suggestions` (Postgres/memória) **antes** de qualquer coisa e envia **email** ao autor quando SMTP está configurado (env; instruções no `.env.example` — Gmail com App Password). Sem SMTP, o autor lê via `GET /suggestions?token=` (`ADMIN_TOKEN`). Rate-limit aplicado; nenhuma sugestão se perde por falha de email.
- **IA (A3)**: agente **Claude Code (Anthropic)** — implementação e testes (9/9 verdes); curadoria humana.

### Edição 0.20 — 2026-07-28 · Fundamentos reescrito com história e método (rigor)
- **Feature spec-kit oficial `025-fundamentos-rigor`** (a pedido do editor: "fundamentos fraco; falta rigor metodológico/científico"): o **cap. 01** foi reescrito em 9 seções — definição (com *scaffolding* = **andaime** traduzido e introduzido), **o que havia antes** (sistemas especialistas, RPA, chatbots, Copilot-autocomplete e por que não eram agentes), a **linhagem técnica** (CoT → **ReAct** → function calling → AutoGPT/BabyAGI e sua lição → CLIs de código → protocolos MCP/A2A/AGENTS.md) com **linha do tempo**, a definição constitutiva (4 elementos), a **proveniência do corpus** (3 arquétipos + teste de inclusão), e a nova seção **"O método do estudo"**: casos múltiplos (Yin) + Mining Software Repositories (Hassan 2008) + GQM (Basili) + feature analysis DESMET (Kitchenham 1997) + benchmarking científico (Sim et al. 2003) + Design Science (Hevner 2004; Peffers 2007) + **tabela de ameaças à validade** (Cook & Campbell), em que a cláusula de expiração vira mitigação declarada.
- **Bibliografia**: novas seções "História e proveniência" e "Metodologia do estudo" com fontes **✓ verificadas** por pesquisa dedicada (ReAct arXiv 2210.03629; anúncios primários de Copilot/function calling/MCP/A2A; Hassan; Runeson & Höst; DESMET; Sim; Stol; Peffers) e itens **⏳** a confirmar explicitamente marcados (Princípio I).
- **Decisão registrada**: `adr/0003-fundamentos-rigor.md` (alternativas avaliadas e justificativa).
- **IA (A3)**: agente **Claude Code (Anthropic)** — pesquisa (2 frentes verificadas) e redação; direção editorial humana.

### Edição 0.19 — 2026-07-27 · foto + LinkedIn do autor; LinkedIn na capa
- **Feature spec-kit oficial `024-autor-linkedin`** (E06+E07 da auditoria): a página "Sobre o autor" ganhou a **foto** do autor (`assets/autor.png`, flutuando à direita, responsiva) e a **tela-capa** passou a incluir o link do **LinkedIn** nos créditos (repositório é público).
- **IA (A3)**: agente **Claude Code (Anthropic)** — implementação; foto enviada pelo autor.

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
