# Guia Editorial — regras operacionais do livro

> Versão operacional das orientações pedagógicas. O parecer completo (com fundamentação) está em [`estudos/2026-07-25-parecer-editorial-plano-pedagogico.md`](../estudos/2026-07-25-parecer-editorial-plano-pedagogico.md). Este guia é o que se consulta **enquanto escreve**.

## 1. O framework pedagógico em quatro linhas

| Framework | O que dita no livro |
|---|---|
| **Backward Design** | Todo capítulo se projeta de trás para frente: objetivos → evidências (verificação/prática) → só então o conteúdo |
| **4C/ID** | Etapas do harness-zero = tarefas inteiras; capítulos = informação de apoio; boxes no código = just-in-time; katas = treino de parte |
| **Diátaxis** | Quatro tipos de texto, nunca misturados na mesma seção: capítulo=explanation, harness-zero=tutorial, templates/benchmark=reference, "o que roubar"=how-to |
| **Carga Cognitiva** | Worked examples antes de exercício; exercícios são "complete", não "crie do zero"; andaime diminui etapa a etapa; uma ideia nova por vez |

## 2. Esqueleto v3 de capítulo (obrigatório; piloto: cap. 04)

**Regra de edição (v3):** ao abrir cada tema, buscar também **material comercial/industrial** (docs oficiais de vendors, blogs de engenharia, posts de praticantes) além do científico. A fonte-base continua sendo **o código dos repositórios**. O corpo do capítulo recebe **o estado da arte** (o que está mais moderno, sintetizado de todas as rodadas do benchmark + indústria); o tratamento detalhado **por repositório vai para o Apêndice do arquivo** — que fica na versão online como complementação e é atualizado a cada rodada.

1. **Objetivos** — 3–5, verbos de Bloom (explicar, comparar, implementar, avaliar)
2. **O problema** — por que a dimensão existe
3. **Fundamentos científicos** — 2–4 papers *traduzidos para decisões*; ponteiro para `bibliografia.md`
4. **Fontes da indústria** — docs de vendor e posts de engenharia relevantes, com a mesma regra de tradução ("o vendor recomenda X porque Y")
5. **O estado da arte** — o corpo principal: padrões consolidados + o que há de mais moderno, citando repositórios apenas como exemplos nominais (o detalhe fica no apêndice)
6. **Mão na massa** — a etapa correspondente do harness-zero
7. **Síntese + "o que roubar"** — leitura executiva e ideias exportáveis
8. **Verificação** — 2–3 perguntas que testam exatamente os objetivos do item 1
9. **Apêndice A — Como cada repositório trata** — a evidência por harness com paths, expandida a cada rodada do benchmark (material de complementação online)

## 2.1 Camada didática v4 (obrigatória; piloto: cap. 02)

> Decidida na [spec 097](../specs/097-reescrita-didatica/spec.md). O v4 **não substitui** o esqueleto v3: a estrutura permanece, a prosa muda.

O v3 acertou a estrutura e deixou a escrita como dossiê — denso, correto e ilegível para quem veio aprender. Medição do corpo dos 18 capítulos antes da spec 097: **22,0 travessões por 1.000 palavras**, frase média de **26,1 palavras**, 51 frases acima de 60 palavras e **zero exemplos trabalhados**, num livro cujo §1 manda "worked examples antes de exercício". Descrever um método pedagógico sem aplicá-lo é a falha que o Princípio I acusa nos outros.

### As sete regras de reescrita

1. **Porta de entrada narrativa** — o capítulo abre com uma cena concreta (uma falha, uma decisão, um número que não fecha) antes de qualquer definição.
2. **Um exemplo trabalhado por capítulo** — código resolvido na frente do leitor, com o raciocínio visível, **antes** do exercício.
3. **Conceito antes de nome** — a ideia primeiro, o rótulo depois, na mesma frase.
4. **Uma ideia nova por parágrafo** — dois conceitos inéditos são dois parágrafos.
5. **Nome de repositório sai do corpo** — a varredura "quem faz o quê" é o Apêndice A, que já existe para isso.
6. **Verificação sem gabarito na mesma linha** — as respostas vão para uma seção `## Respostas da verificação` no fim, depois do Apêndice A.
7. **Travessão com orçamento** — cada corte força uma escolha: virar frase, virar parêntese, ou a ideia sair.

### Os limites, medidos no build

`publicar/mede-prosa.mjs` roda no `npm run build` e reporta todos os capítulos; **reprova** apenas os já marcados como v4, para que o portão não nasça vermelho e vire ruído.

| Métrica | Limite | Antes da spec 097 |
|---|---|---|
| Travessões / 1.000 palavras | ≤ 8 | 22,0 |
| Frase média | ≤ 20 palavras | 26,1 |
| Frases acima de 60 palavras | 0 | 51 no livro |
| Exemplo trabalhado no corpo | ≥ 1 bloco de código | 0 |
| Gabarito em seção própria | obrigatório | 0 |

Os limiares vêm do `writing_quality_check` da suíte [academic-research-skills](https://github.com/Imbad0202/academic-research-skills), **recalibrados para prosa didática em português**: o travessão é pontuação normal em pt-BR, e o que se combate é o empilhamento de apostos numa frase só, não o sinal. O que não se importa de lá: IMRaD, APA e os portões de integridade de pesquisa — este livro não é um paper, e o revisor de manuscrito mediria a coisa errada.

## 2.2 Livro vivo: datação e histórico (obrigatório)

Este é um **livro vivo** — coerência com a própria tese (a cláusula de expiração: o que descrevemos é temporário). Três regras:

1. **Todo capítulo v3 declara a data de captura no cabeçalho**: `> **Estado da arte capturado em AAAA-MM** · última revisão AAAA-MM-DD · [histórico](../HISTORICO.md)`. Isso diz ao leitor se a seção "Estado da arte" está fresca — o que a data do *evento* (no corpo) não faz.
2. **Distinguir três datas** (ver `HISTORICO.md`): data do evento (no corpo — fato histórico, imutável), data de captura (no cabeçalho — quando fotografamos), rodada do benchmark (nas avaliações — versão da foto de cada repo). Reavaliar = nova rodada, nunca sobrescrever.
3. **Toda edição atualiza `livro/HISTORICO.md`**: o changelog de edições, a tabela de snapshot por capítulo, e — o mais importante — o **registro de expiração** (o placar das previsões: cada cláusula de expiração pontuada 🔵/🟡/🟢/🔴 contra a realidade, com evidência datada). Uma linha que muda de estado é a notícia mais importante de uma nova edição.

Regra de escrita associada: quando uma afirmação for sensível ao tempo ("hoje", "ainda não", "o consenso de 2026"), ela está implicitamente sob a data de captura do cabeçalho — não precisa datar cada frase, mas evite absolutos atemporais ("nunca", "sempre") a menos que sejam do tipo não-expira (fronteira com o mundo).

## 3. Regras de escrita permanentes

- **Evidência por caminho de arquivo** para qualquer afirmação sobre um harness; **status ✓** para qualquer citação científica (skill `academic-research` tem o fluxo).
- Notas 0–3 só comparam dentro da mesma categoria do benchmark.
- Cada componente descrito deve, quando possível, declarar sua **cláusula de expiração**.
- Prosa em português; termos técnicos consagrados (harness, loop, tool, prompt) **sem tradução**.
- Tabelas para fatos enumeráveis; explicação vive na prosa, não nas células.

## 4. Regras do harness-zero (as 4 condições do parecer)

1. **DDD leve** — linguagem ubíqua = glossário do livro; padrão tático só onde paga; DDD aparece como consequência nomeada no código.
2. **Arquitetura por refatoração** — cada porta nasce da dor do capítulo correspondente; nunca estrutura antecipada.
3. **Anti-apodrecimento** — modelo atrás de `LLMPort`; etapas autocontidas e executáveis; erros didáticos deliberados são **comentados como tal** no código.
4. **Chat congelado** — HTML+JS servido pelo backend; só evolui quando uma dimensão exigir superfície nova.

## 5. Ferramentas do repositório

- **spec-kit** (`.specify/` + comandos `/speckit-*`): para features novas do harness-zero ou seções grandes do livro, o fluxo é `/speckit-specify` → `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` (com `/speckit-clarify` antes do plano quando o pedido for ambíguo). A constitution do projeto vive em `.specify/memory/`.
- **Skill `academic-research`** (`.claude/skills/`): fluxo de localizar → validar → registrar → integrar referências científicas.
- **`scripts/sync-forks.ps1`**: sincronização local dos forks com upstreams.

## 6. Estudo: processos e metodologias de escrita editorial e acadêmica (tradicionais e da era-IA)

> **Atualizado em 2026-07** · livro vivo (as práticas de IA têm data de expiração). Fontes na seção "Guia — Metodologias de escrita" de `bibliografia.md`.

Um livro sobre engenharia — a disciplina de instrumentar bem um processo — precisa expor o próprio processo de produção, ou contradiz o que ensina. Esta seção é um *survey* das metodologias de escrita editorial e acadêmica (as consagradas e as da era-IA) e, ao fim, torna explícito e datado o método com que este livro é escrito. É texto de **referência/explicação** (Diátaxis), não um capítulo — por isso não segue o esqueleto v3.

### 6.A — Metodologias tradicionais

**Estrutura da escrita científica.** O **IMRaD** (Introdução, Métodos, Resultados, Discussão) não foi inventado por um autor: [Sollaci & Pereira (2004)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC442179/) mostram que foi "imposto por decantação", virando padrão nos anos 1980. O clássico [Gopen & Swan, "The Science of Scientific Writing" (1990)](https://www.jstor.org/stable/29774235) estabelece o princípio da *expectativa do leitor* — o sentido nasce da posição estrutural (topic/stress positions), não só das palavras. A codificação prática está em *How to Write and Publish a Scientific Paper* (Day & Gastel).

**A escrita como processo cognitivo.** [Flower & Hayes (1981)](https://doi.org/10.58680/ccc198115885) modelam a escrita como processos **recursivos** (planejar/traduzir/revisar) guiados por objetivos, não etapas lineares; [Sommers (1980)](https://doi.org/10.2307/356588) mostra que escritores experientes revisam *re-vendo o sentido*, enquanto novatos trocam palavras na superfície — "escrever é reescrever".

**Craft e estilo.** A tradição vai do minimalismo prescritivo de *The Elements of Style* (Strunk & White) à teoria *principiada* da clareza de *Style: Toward Clarity and Grace* (Williams — personagens=sujeitos, ações=verbos, velho-antes-de-novo), passando pela voz autêntica de *On Writing Well* (Zinsser); os padrões editoriais/citação são o *Chicago Manual of Style* (17ª ed.) e o *APA Publication Manual* (7ª ed.).

**Craft of research e argumento.** *The Craft of Research* (Booth, Colomb & Williams) enquadra pesquisa como **fazer um argumento a um leitor** (problema → pergunta → *claim* → razões → evidência; o "So what?"); o [modelo de Toulmin (1958)](https://www.cambridge.org/core/books/uses-of-argument/26CF801BC12004587B66778297D5567C) dá a anatomia do argumento (claim, grounds, warrant, backing, qualifier, rebuttal).

**Revisão por pares e fluxo editorial.** [Spier (2002)](https://doi.org/10.1016/S0167-7799(02)01985-6) traça a história do peer review; a historiografia ([Baldwin, ETHOS](https://ethos.lps.library.cmu.edu/article/id/19/)) lembra que o refereeing universal é construto do séc. XX. E a divisão de trabalho editorial — *developmental editing* (reestruturar visão/discurso) × *copyediting* (preparo de sentença) — é o eixo do fluxo (Norton, *Developmental Editing*).

**Design instrucional (o que este livro já usa).** Backward Design (Wiggins & McTighe), [4C/ID (van Merriënboer et al., 2002)](https://doi.org/10.1007/BF02504993), [carga cognitiva (Sweller, 1988)](https://doi.org/10.1207/s15516709cog1202_4) e [Diátaxis (Procida)](https://diataxis.fr/) — a base pedagógica do Princípio III.

### 6.B — Metodologias da era-IA

**Co-escrita humano-IA.** Estudos de HCI tratam a co-escrita como interação **observável**, não caixa-preta: [CoAuthor (Lee, Liang, Yang, 2022)](https://doi.org/10.1145/3491102.3502030) registra a interação em nível de keystroke; [Wordcraft (Yuan et al., 2022)](https://doi.org/10.1145/3490099.3511105) decompõe a escrita em *moves* (continuar/infill/elaborar/reescrever) ligados à intenção. **Cautela** medida: [Jakesch et al. (2023)](https://doi.org/10.1145/3544548.3581196) mostram que um assistente enviesado desloca o que o usuário escreve *e pensa* ("persuasão latente").

**Spec-driven / structured authoring / docs-as-code.** Escrever a intenção primeiro e deixá-la dirigir a geração: [GitHub Spec Kit](https://github.com/github/spec-kit) (spec → plan → tasks → implement) e [Amazon Kiro](https://kiro.dev/) formalizam isso; a comunidade de documentação já adota workflow de engenharia para prosa ([docs-as-code, SIGDOC '24](https://doi.org/10.1145/3641237.3691677); [DITA/topic-based](https://dita-lang.org/)).

**Pesquisa aumentada por agentes e recuperação.** [RAG (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401) ancora a geração em fontes recuperadas em vez da memória do modelo; a fronteira agêntica decompõe o *survey* em papéis (buscar/sintetizar/verificar) — tendência ilustrada por trabalhos de auto-survey (⏳ a confirmar).

**Verificação e proveniência.** [RARR (Gao et al., 2023)](https://arxiv.org/abs/2210.08726) faz atribuição/checagem *após* a geração; [Liu, Zhang & Liang (2023)](https://arxiv.org/abs/2304.09848) medem que só **51,5%** das afirmações de motores de busca generativos são totalmente suportadas por citação — julgar por *citation precision/recall*; [watermarking (Kirchenbauer et al., 2023)](https://arxiv.org/abs/2301.10226) embute proveniência (frágil a paráfrase).

**Integridade acadêmica e autoria.** O consenso das políticas: **um LLM não pode ser autor** (não responde pelo conteúdo) e o uso deve ser **divulgado** — [ICMJE](https://www.icmje.org/recommendations/browse/artificial-intelligence/), [COPE (2023)](https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools), [*Science* (Thorp, 2023)](https://doi.org/10.1126/science.adg7879), [*Nature* (2023)](https://www.nature.com/articles/d41586-023-00191-1). E a divulgação, na prática, é [amplamente violada (Academ-AI, 2024)](https://arxiv.org/abs/2411.15218).

### 6.C — Tensões e síntese (tradicional × IA)

O ganho da assistência de IA (velocidade, alcance de pesquisa, estrutura) vem com quatro tensões que uma edição acadêmica não pode ignorar:

- **Fontes fabricadas.** [Walters & Wilder (2023)](https://doi.org/10.1038/s41598-023-41032-5) mediram **55%** de citações fabricadas no GPT-3.5 (18% no GPT-4) e erros substantivos nas reais — daí a regra deste livro: **verificar toda referência** contra a fonte primária, por busca cruzada.
- **Verifiabilidade.** Texto que *parece* citado frequentemente não é suportado (os 51,5% de Liu et al.) — a citação precisa ser conferida, não confiada.
- **Reprodutibilidade.** Saídas de LLM são não-determinísticas; logar prompt, versão de modelo e contexto é parte do rigor.
- **Homogeneização e "cognitive debt".** A IA converge estilo e ideias ([homogeneização, 2024](https://arxiv.org/abs/2402.01536)) e o uso acrítico associa-se a menor engajamento/propriedade ([Kosmyna et al., 2025](https://arxiv.org/abs/2506.08872)) — razão para a IA *ampliar*, não *substituir*, o julgamento do autor.

A síntese do livro: usar a IA como **prótese de pesquisa e estruturação sob verificação humana**, não como autor. As metodologias tradicionais (argumento, clareza, revisão) permanecem o padrão de qualidade; as de IA aceleram o caminho até ele, desde que cercadas de verificação.

### 6.D — O método deste livro, declarado

Este livro pratica o que descreve. Cada prática liga-se a um princípio da constituição e tem evidência no próprio repositório:

- **Evidência acima de retórica** (Princ. I) — nenhuma afirmação sobre um harness sem *path* no código; nenhuma citação sem status validado. Fontes verificadas por busca cruzada; lacunas registradas, não preenchidas com fonte fraca.
- **A fonte-base é o código** (Princ. II) — o corpo nasce da leitura do código dos harnesses; ciência e indústria contextualizam. O tratamento por repositório (com paths) é o **Apêndice A** de cada capítulo.
- **Método pedagógico combinado** (Princ. III) — Backward Design + 4C/ID + Diátaxis + carga cognitiva; o esqueleto v3 é a materialização.
- **Pesquisa dupla verificada** — ao abrir cada tema, agentes de pesquisa em paralelo levantam material **científico** e **de indústria**; cada fonte é confirmada por ≥2 menções independentes antes de entrar (a regra que a era-IA torna ao mesmo tempo possível e obrigatória, à luz de Walters & Wilder).
- **Ciclo spec-driven** (Princ. VII) — toda melhoria passa por `spec → plan → tasks → implement` (spec-kit), em branch própria; *esta seção* foi produzida assim (`specs/010-estudo-metodologias-escrita/`), com o ciclo oficial e seus gates (Constitution Check, análise cross-artefato).
- **Livro vivo** (Princ. IV) — datação e `HISTORICO.md`; as previsões têm um placar (registro de expiração).

**Divulgação de autoria (transparência).** Coerente com as políticas acima e com o Princípio I, declaramos abertamente: este livro é **co-escrito com um agente de IA (Claude Code, da Anthropic)** operando sob **autoria, curadoria e responsabilidade humanas**. O agente executa pesquisa, redação e o ciclo spec-kit; o autor humano define o escopo, decide (via `/speckit-clarify` e revisão), verifica as fontes e responde pelo conteúdo. Seguindo [ICMJE](https://www.icmje.org/recommendations/browse/artificial-intelligence/)/[COPE](https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools)/[*Nature*](https://www.nature.com/articles/d41586-023-00191-1)/[*Science*](https://doi.org/10.1126/science.adg7879), a IA **não** é listada como autora — não pode ser responsável — e seu uso é divulgado aqui, no método.

### 6.E — Fluxo repetível para um contribuidor

Para levar um capítulo ou seção ao padrão do livro:

1. **Abrir o tema** — pesquisa dupla (comercial/industrial + científica), verificada por busca cruzada; registrar lacunas.
2. **Reunir a fonte-base** — ler o código dos harnesses; anotar paths (vira Apêndice A).
3. **Escrever** — no esqueleto v3 (capítulos) ou no tipo Diátaxis correto (guia/benchmark = referência); um tipo de texto por seção; termos técnicos sem tradução.
4. **Revisar (developmental)** — re-ver estrutura e sentido antes do copyedit de superfície: o argumento fecha? a ordem serve ao leitor? há redundância ou lacuna? "Escrever é reescrever" (§6.A; portão de qualidade da constituição).
5. **Verificar fontes** — nenhuma URL/ID inventado; não-confirmado marcado `⏳`; sincronizar `bibliografia.md`.
6. **Gate de build** — `node publicar/build.mjs` verde (sem link interno quebrado).
7. **Datar** — selo de captura no capítulo e entrada no `HISTORICO.md` — **com a versão do modelo de IA usada** — se o estado da arte mudou.

Salvaguardas de uso de IA: a IA pesquisa e rascunha; o humano decide, verifica e assina. Toda fonte trazida por um agente é conferida antes de entrar no corpo.

## Siglas e glossário (política)

- **Toda sigla técnica é apresentada por extenso na 1ª ocorrência** de um capítulo — "Model Context Protocol (MCP)" — e, dali em diante, o texto pode usar só a sigla.
- O motor de publicação reforça isso: **envolve automaticamente cada sigla conhecida em `<abbr>`**, de modo que passar o mouse revela o significado em qualquer ocorrência, sem poluir o texto-fonte. O mapa de siglas vive em `publicar/build.mjs` e é espelhado na página **[Glossário](glossario.md)** (`livro/glossario.md`).
- O **Glossário** dá o **por extenso**, uma explicação curta e **em que capítulos** cada sigla aparece. Ao introduzir uma sigla nova, adicione-a nos dois lugares (mapa do motor + glossário) e **confira a expansão na fonte** (Princípio I).

## Cadência do livro vivo

> Política decidida no [ADR 0007](../adr/0007-cadencia-livro-vivo.md) (alternativas e justificativa lá).

- **Janela trimestral** (próxima: **2026-10**): re-sync dos 16 forks (`scripts/sync-forks.ps1`), diff dirigido pelas dimensões do benchmark, atualização dos Apêndices A afetados, do placar de expiração e das datas de revisão; edição minor no [Histórico](HISTORICO.md).
- **Gatilho extraordinário**: qualquer evento que **invalide uma "Leitura executiva"** (mudança de protocolo, capacidade migrando para o provedor, harness do corpus arquivado) dispara revisão pontual do capítulo afetado, sem esperar a janela.
- A data "estado da arte capturado em" de cada capítulo continua sendo a verdade exposta ao leitor — a cadência existe para que ela nunca minta por omissão.
