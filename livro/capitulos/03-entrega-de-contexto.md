# 03 — Entrega de Contexto

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](../HISTORICO.md)
>
> Camada didática v4 — ver [Guia Editorial §2.1](../GUIA-EDITORIAL.md).
> andaime: completo
>
> Esqueleto v3 — corpo com o estado da arte; tratamento por repositório no Apêndice A (complementação online).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Explicar** por que contexto é um orçamento gerenciado em runtime, não um depósito, e o que é *context rot*;
2. **Compor** um system prompt em camadas ordenadas por volatilidade, ciente de cache;
3. **Projetar** uma cascata de arquivos de contexto (global → projeto → pacote → pessoal) com precedência declarada;
4. **Implementar** o montador de contexto do harness-zero (etapa 3) com um arquivo de regras de projeto;
5. **Avaliar** um arquivo AGENTS.md real contra as práticas de autoria: enxuto, comandos executáveis, crescido por evidência de falha.

## A fatura que quadruplicou sem ninguém mudar nada

Duas semanas de uso tranquilo. Na terceira, a fatura do agente quadruplica.

Ninguém mudou o modelo, ninguém mudou o volume de trabalho, ninguém acrescentou ferramenta. O time procura vazamento, procura loop infinito, procura alguém rodando eval em produção. Nada.

O que mudou foi uma linha. Alguém achou útil que o agente soubesse a hora e acrescentou, no topo do system prompt:

```
Data e hora: 2026-08-12T14:07:33
```

Uma linha, no lugar errado. O cache do provedor funciona **por prefixo**: ele reaproveita o começo idêntico entre chamadas e cobra pouco por ele. Um valor que muda a cada segundo, colocado no topo, garante que **nenhuma** chamada compartilhe prefixo com a anterior. O cache nunca acerta, e tudo passa a ser cobrado como novo.

Não é um detalhe de otimização. A **ordem** em que o contexto é montado é uma decisão de custo, e este capítulo é sobre montar essa ordem de propósito.

## O problema

O modelo só sabe o que o harness mostra.

Entrega de contexto é a engenharia de decidir **o que** entra em cada chamada — system prompt, regras do projeto, estado do ambiente, memórias, instruções de servidores externos —, **em que ordem**, e **como isso muda** no meio de uma conversa sem quebrar o cache do provedor nem confundir o modelo.

Os sub-problemas clássicos são três: onde vivem as regras do projeto e como são descobertas; se o prompt de sistema deve variar por modelo; e como informar mudanças de estado no meio da conversa sem invalidar o prefixo cacheado.

## Fundamentos científicos

- **Contexto degrada com posição e com volume** — *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)): a informação no meio de contextos longos é mal utilizada. A consequência de projeto é direta: o que importa vai para as bordas, com o system prompt no início e a tarefa atual no fim, e "mandar tudo" é anti-padrão com base empírica.
- **Context engineering como disciplina** — o survey [arXiv 2507.13334](https://arxiv.org/abs/2507.13334) sistematiza a área (RAG, memória, tool-integrated reasoning) e legitima o termo que a indústria adotou.
- **Menos contexto, agentes melhores** — [arXiv 2606.10209](https://arxiv.org/abs/2606.10209) mede, em agentes de longa duração, o que a Anthropic chama de *context rot*: curadoria agressiva supera janelas cheias.

(Bibliografia completa: `livro/bibliografia.md`.)

## Fontes da indústria

- **[Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** (Anthropic Engineering): batiza a sucessão da prompt engineering. O trabalho é **curar o conjunto ótimo de tokens em tempo de inferência**, e o texto nomeia *context rot* como fato de engenharia. A decisão que dele decorre: a janela é orçamento, e a meta é o menor conjunto de tokens de alto sinal.
- **[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)** + **[Lessons from building Claude Code: prompt caching is everything](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything)**: o cache é **por prefixo**, então a ordem de montagem é decisão de custo. O relato lista os invalidadores clássicos — timestamp no topo, request ID na lista de tools, reserialização do histórico — e trata **cache hit rate como métrica de primeira classe do harness**, com cerca de 59% de redução de input cobrado.
- **[AGENTS.md](https://agents.md/)** + **[Agentic AI Foundation](https://openai.com/index/agentic-ai-foundation/)**: o "README para agentes" foi **doado à Linux Foundation** em dezembro de 2025, com OpenAI, Anthropic e Block como co-fundadores, e mais de 60 mil projetos o usam. Contexto por arquivo de repositório virou infraestrutura neutra e portável, então investir nesse pipeline é seguro.
- **[How Claude remembers your project](https://code.claude.com/docs/en/memory)**: formaliza a **cascata** global → projeto → local, com o arquivo mais próximo vencendo e o pessoal fora do versionamento.
- **[AGENTS.md Field Guide 2026](https://www.iuriio.com/blog/posts/2026/05/agents-md-field-guide-2026)** (praticante): a parte de autoria. Começar com cerca de 30 linhas, teto de 150 a 200 na raiz, comandos exatos antes de prosa, aninhar por pacote em monorepo, e **crescer só por evidência de falha reincidente** do agente. O erro comum é tratá-lo como documentação.
- **Consulte também**: a coleção viva [Awesome Harness Engineering — Context Delivery & Compaction](https://github.com/GHDaru/awesome-harness-engineering#context-delivery--compaction) reúne mais recursos desta dimensão, curados por problema.

## Na prática: montar por volatilidade, e provar que funcionou

O montador ingênuo concatena o que for aparecendo:

```python
def montar_contexto(tarefa: str) -> str:
    return "\n".join([
        f"Data e hora: {datetime.now().isoformat()}",   # ← muda a cada chamada
        LEIA("identidade.md"),
        f"Diretório: {os.getcwd()}",
        LEIA("AGENTS.md"),
        tarefa,
    ])
```

Está correto e é caro. A primeira linha invalida tudo o que vem depois dela.

A correção não é remover o timestamp: às vezes o agente precisa mesmo saber a hora. A correção é **ordenar por volatilidade** — o que quase nunca muda primeiro, o que muda a cada turno por último:

```python
CAMADAS = [
    ("identidade", lambda _: LEIA("identidade.md")),         # muda em release
    ("ambiente",   lambda _: f"SO: {platform.system()}"),    # muda por máquina
    ("projeto",    lambda _: cascata_agents_md()),           # muda em commit
    ("memoria",    lambda s: memorias_relevantes(s)),        # muda por sessão
    ("volatil",    lambda _: f"Agora: {datetime.now():%H:%M}"),  # muda sempre
]

def montar_contexto(sessao) -> str:
    return "\n\n".join(f"## {nome}\n{fn(sessao)}" for nome, fn in CAMADAS)
```

O timestamp continua lá, agora **no fim**. Tudo acima dele é byte-a-byte idêntico entre turnos, e é exatamente esse "tudo acima" que o cache cobra barato.

Agora a parte que quase ninguém faz: **provar**. Estabilidade de prefixo é uma invariante, e invariante sem teste é esperança.

```python
def test_prefixo_estavel():
    a = montar_contexto(sessao)
    time.sleep(1.1)                      # tempo passa: o volátil muda
    b = montar_contexto(sessao)

    comum = os.path.commonprefix([a, b])
    assert comum, "os dois contextos divergem já no primeiro byte"

    # o prefixo comum precisa cobrir tudo, menos a camada volátil
    corte = a.index("## volatil")
    assert len(comum) >= corte, (
        f"prefixo divergiu em {len(comum)}, antes do esperado ({corte}).\n"
        f"a partir daqui: {a[len(comum):len(comum)+80]!r}"
    )
```

A mensagem de erro é a parte útil. Quando alguém acrescentar um `request_id` no meio da montagem daqui a seis meses, o teste não dirá apenas "falhou": ele imprime **o offset onde os dois contextos divergiram e os 80 caracteres seguintes**, que é o nome do culpado.

Foi o que faltou na cena de abertura. Aquele time descobriu a linha depois de três semanas e uma fatura; com essa asserção, teria descoberto no commit.

## O estado da arte

### 1. Contexto é orçamento gerenciado, e a recuperação virou just-in-time

O consenso moderno inverteu o instinto de "quanto mais contexto, melhor". O harness administra ativamente a janela: poda por regra, consciência de quanto resta, recuperação sob demanda.

Duas materializações se destacam no benchmark. Uma delas dá ao modelo a estrutura de um repositório inteiro por cerca de mil tokens, construída por análise sintática e ranqueamento de grafo, sem nenhum agente explorador — recuperação estática just-in-time. A outra carrega regras por subdiretório **conforme o agente navega**, em vez de tudo de antemão.

### 2. Estabilidade de prefixo virou requisito arquitetural

É a seção "Na prática" promovida a princípio. Cache-awareness deixou de ser otimização e reorganizou a montagem: camadas por volatilidade, serialização determinística, zero conteúdo volátil no topo.

As duas formalizações mais rigorosas do corpus tratam o prefixo como **baseline imutável**, entregando mudanças de estado apenas em fronteiras seguras de turno, e declaram as três camadas do exemplo acima com esses nomes. Uma delas leva a ideia adiante: o fork que faz curadoria de skills **herda o prefixo do pai**, economizando cerca de 26%.

### 3. O arquivo de regras padronizou, e virou cascata

A fragmentação de nomes do início da disciplina está resolvida por governança neutra. O formato portável é lido nativamente por quase todo o corpus, com os nomes proprietários virando alias.

O padrão maduro é a **cascata com precedência declarada**: global, projeto, pacote e pessoal, com o mais próximo vencendo e o pessoal fora do versionamento. Há composição por importação, e há a prática de autoria que separa arquivo útil de documentação morta — crescer **por evidência de falha**, como código cresce por bug.

### 4. As fronteiras novas

Três movimentos recentes ainda não viraram consenso.

**Prompt por família de modelo**, com um harness mantendo cerca de dez variantes e outro levando ao extremo com instruções **vindas do servidor**: o backend entrega o prompt-base por modelo, com até personalidade configurável.

**Separação entre persona e regras**, contribuição da categoria de agentes pessoais: um arquivo para voz e identidade, outro para o operacional.

**Contexto com classe de confiança**: conteúdo pessoal ou injetado viaja em envelopes que preservam a origem, de modo que o harness saiba o que é instrução sua e o que é texto de terceiro. É a entrega de contexto encontrando a segurança do cap. 07.

> **O contraponto: o harness mínimo (Pi)** — *adendo da rodada ext-1, 2026-07-31.* Enquanto este capítulo descreve montadores cada vez mais ricos, o [Pi](https://github.com/badlogic/pi-mono) aposta na direção oposta: system prompt base **medido em ~460 tokens**, derivado do tool set (cada ferramenta contribui seu snippet, e guidelines entram só se a ferramenta correspondente está ativa), com skills anunciadas **só por nome e descrição** — o corpo é carregado pelo próprio modelo quando a tarefa pede.
>
> A honestidade editorial exige as duas ressalvas que a leitura de código revelou. Primeira: o mesmo montador concatena os `AGENTS.md` da cascata **sem orçamento**, o que no próprio repositório do Pi adiciona cerca de 2.700 tokens, seis vezes o slogan — a minimalidade é do harness, não do contexto. Segunda: minimalismo não é ausência de engenharia, e a compactação do Pi é a mais completa do corpus (ver [avaliação](../../benchmark/avaliacoes/pi.md)).
>
> A aposta subjacente é falsificável e vale acompanhar: **modelos melhores precisariam de menos harness**. Se for verdade, parte deste capítulo expira. Se a janela continuar cara, a falta de orçamento cobra juros.

### Leitura executiva

O que está mais moderno: orçamento e recuperação just-in-time em vez de volume; prefixo estável como requisito, com cache hit rate tratado como indicador; arquivo de regras em cascata sob governança neutra; e as três fronteiras (prompt por modelo, persona separada, classe de confiança). O contraponto minimalista mostra o outro extremo do espectro e prova que a tensão entre orçamento e riqueza segue aberta.

**O que roubar:**

- **O mapa de repositório**, como alternativa barata à exploração por agente.
- **As três camadas por volatilidade** na montagem do system prompt.
- **A disciplina de crescer o arquivo de regras só por falha reincidente.**
- **O snippet de prompt acoplado à definição da ferramenta**, que impede prompt e tool set de dessincronizarem.
- **O teste de estabilidade de prefixo** da seção "Na prática". É a peça mais barata deste capítulo.

## Mão na massa — harness-zero, etapa 3

Na etapa 3 (`harness-zero/etapas/03-contexto/`) você constrói o montador do harness-zero: system prompt em camadas ordenadas por volatilidade, descoberta de um `AGENTS.md` na raiz do projeto-alvo, a janela `/contexto` para ver o que foi montado, e o teste de estabilidade de prefixo escrito acima.

Exercício de completude: a função de descoberta em cascata vem esqueletada com um nível só. Você implementa a precedência global → projeto → pacote → pessoal, com o mais próximo vencendo.

E fique com esta pendência anotada, porque o próximo capítulo a cobra: o `read_file` desta etapa lê **qualquer** caminho que o modelo pedir. A ferida é aberta aqui e fechada no cap. 07.

## Verificação

1. Por que um timestamp no topo do system prompt é caro, e onde ele deveria ficar?
2. Seu agente ignora uma convenção do projeto de forma reincidente. Qual é a resposta certa segundo a prática de autoria moderna, e qual é a errada?
3. Um harness quer informar ao modelo que a data mudou no meio de uma conversa longa. Descreva duas estratégias com custos de cache diferentes.
4. O teste de estabilidade de prefixo passa hoje. Alguém acrescenta um contador de tokens gastos na camada de ambiente. O teste continua passando? Por quê?

---

## Apêndice A — Como cada repositório trata a entrega de contexto

> Evidência por harness, com paths — complementação online, expandida a cada rodada do benchmark.

### opencode (rodada 1) — álgebra tipada e Context Epochs
`packages/opencode/src/session/system.ts` monta environment + skills + instruções MCP (Model Context Protocol); **~10 prompts por família de modelo** em `session/prompt/*.txt` (anthropic, gpt, codex, gemini, kimi, beast...), selecionados por substring do model id; `AGENTS.md` globais/ascendentes agregados por `session/instruction.ts`. A V2 (`CONTEXT.md`) formaliza o contexto como álgebra de "Context Sources" com snapshots, **Context Epochs** (baseline de cache) e mensagens de sistema mid-conversation só em fronteiras seguras.

### gemini-cli (rodada 1) — hierarquia com @imports
`prompts/promptProvider.ts` monta por modo/tools/modelo (snippets modernos × legados); `GEMINI.md` hierárquico (`memoryDiscovery.ts`: global → pais → subpastas) com `@imports` (`memoryImportProcessor.ts`) e `flattenMemory`; override total via `GEMINI_SYSTEM_MD`; injeção just-in-time (`tools/jit-context.ts`).

### OpenHarness (rodada 1) — agregação com memória relevante
`src/openharness/prompts/context.py`: base + ambiente + `CLAUDE.md` + **memórias selecionadas por relevância** (`memory/relevance.py`, com `usage.py` rastreando uso) + skills + contexto de repo ativo; `-s/--append-system-prompt` na CLI.

### Codex CLI (rodada 2) — AGENTS.md central + prompts server-driven
`core/src/agents_md.rs`: descoberta hierárquica com merge do project-root ao cwd; system prompt **varia por modelo e vem do backend** (`ModelInfo.base_instructions` via `models-manager`, com template e `Personality::Friendly/Pragmatic`); contexto ambiental via `WorldState`.

### Goose (rodada 2) — hints incrementais e hardening
`SystemPromptBuilder` com override + extras; hints multi-arquivo (**`.goosehints` E `AGENTS.md`**, `CLAUDE.md` via config) respeitando `.gitignore`; **`SubdirectoryHintTracker`** carrega hints de subdiretório conforme o agente navega; sanitização anti prompt-injection de tags Unicode; "top of mind" por turno.

### Aider (rodada 2) — o repo-map ⭐
`aider/repomap.py`: tags de definição/referência via tree-sitter (queries `.scm` por linguagem) → grafo arquivo→arquivo → **PageRank personalizado** (chat files e idents mencionados enviesam o ranking; multiplicadores ×10/×50/×0.1) → renderização sob orçamento com busca binária (~1024 tokens; `map_mul_no_files=8` sem arquivos no chat) → cache por mtime. O caminho context-first inteiro em um arquivo.

### OpenHands/Canvas (rodada 2) — skills organizacionais
`app_conversation/skill_loader.py`: skills auto-descobertas de repositórios convencionais **`owner/.openhands` e `owner/.agents`** em todas as organizações do usuário (GitHub/GitLab/Azure), com KeywordTrigger/TaskTrigger e marketplace — contexto de time versionado e carregado para todos os membros.

### OpenClaw (rodada 2) — workspace de identidade com orçamentos
`buildAgentSystemPrompt` injeta `SOUL.md` (persona), `AGENTS.md` (regras), `USER.md`, `IDENTITY.md`, `TOOLS.md`, `MEMORY.md`, `HEARTBEAT.md`, `BOOTSTRAP.md` — com orçamentos (20k chars/arquivo, 60k total) e truncamento marcado; contribuições provider-aware **acima/abaixo do cache boundary**.

### Hermes (rodada 2) — três camadas por volatilidade ⭐
`agent/system_prompt.py` + `prompt_builder.py`: `stable` (identidade/SOUL.md + guidance + índice de skills) → `context` (AGENTS.md/.cursorrules do projeto) → `volatile` (memória, USER.md, timestamp) — desenho explícito para prefix-cache; persona migrável do OpenClaw.

### IronClaw (rodada 2) — contexto como decisão de política
`LoopPromptPort` (crates/ironclaw_loop_host): resolve identidade, contexto pessoal (**opt-in por run profile, não por canal**), skills e segurança; conteúdo injetado/pessoal viaja em **prompt envelopes** com trust class inforjável — separação entre o que o loop pede e o que o host permite ver.

### ohmo (rodada 2.5) — a versão mínima correta
`ohmo/prompts.py`: concatenação ordenada base → soul → identity → user → BOOTSTRAP → workspace → memória; decisão rigorosa `include_project_memory=False` (o agente pessoal não lê CLAUDE.md de projeto — testado).

### Pi (rodada ext-1) — o prompt derivado do tool set ⭐
`core/system-prompt.ts`: base **medida em ~460 tokens**, montada dos `promptSnippet` das próprias tool definitions com dedup e guidelines condicionais ao conjunto ativo (desativou a tool, o prompt encolhe); skills anunciadas só como `<name/description/location>` e carregadas pelo modelo via `read` (bloco omitido se `read` não está ativa); cascata `AGENTS.md`/`CLAUDE.md` global→raiz→cwd com dedup de worktrees aninhadas (`resource-loader.ts`) — porém concatenada **sem orçamento** (ver caixa no corpo do capítulo); override total via `.pi/SYSTEM.md`.

### n8n (rodada 2) — o mínimo do embutido
`ToolsAgent/common.ts`: `ChatPromptTemplate` com system message livre + histórico + binários ricos (imagens/PDF); sem arquivo de regras nem hierarquia — o contexto vem mapeado do workflow pelo autor.

### Frameworks (rodada frameworks) — aberto por design
LangGraph e Agents SDK (Software Development Kit) deixam a montagem por conta do dev (instructions estáticas ou callable); CrewAI impõe role/goal/backstory como contexto estrutural; o software-agent-sdk dá preset Jinja com escape hatch documentado (`prompt_dir` + `_prompt_preset() -> None`).

---

## Respostas da verificação

**1.** Porque o cache do provedor é **por prefixo**: ele reaproveita o começo idêntico entre chamadas. Um valor que muda a cada segundo no topo garante que nenhuma chamada compartilhe prefixo com a anterior, e o contexto inteiro passa a ser cobrado como novo. O lugar dele é a **última camada**, depois de tudo que é estável, para que a parte invalidada seja só a que precisa mudar. O mesmo raciocínio vale para request ID em lista de tools e para qualquer reserialização não determinística do histórico.

**2.** A resposta certa é **acrescentar uma regra específica ao arquivo de projeto, por causa daquela falha**, com o comando ou a convenção exata, e nada além. A errada é despejar documentação: transformar o arquivo em manual do projeto. O motivo é de orçamento e de sinal. Cada linha do arquivo entra em **toda** chamada, então documentação genérica compete com a tarefa por espaço e dilui as instruções que importam. O arquivo de regras cresce como código cresce: por incidente reproduzido, não por vontade de ser completo.

**3.** A cara: **reescrever o prefixo**, atualizando a data onde ela estiver e invalidando o cache dali para a frente. A barata: entregar a mudança **no fim**, como mensagem de estado numa fronteira de turno, deixando o prefixo intacto. A segunda é o padrão do corpus e tem nome nos harnesses que a formalizam — o prefixo é tratado como baseline imutável, e mudanças de estado só entram em pontos seguros. A escolha entre elas é um trade-off entre imediatismo e custo, e o caso em que a cara se justifica é quando a informação **precisa** ser lida antes do que já está no contexto.

**4.** **Continua passando, e esse é o problema.** O teste assevera que o prefixo comum cobre tudo até a camada volátil; um contador de tokens dentro da camada de *ambiente* fica **antes** desse corte, então a divergência acontece cedo e a asserção `len(comum) >= corte` falha... desde que o valor mude entre as duas montagens. Se o contador for igual nos dois turnos do teste — e num teste sintético ele costuma ser —, o prefixo permanece idêntico e o teste passa, enquanto em produção quebra a cada turno. É a limitação honesta desta verificação: ela prova estabilidade **para as variações que o teste provoca**, não para todas. A defesa é a mesma do cap. 11: o teste mede o que alguém decidiu variar, e é por isso que a asserção imprime o offset da divergência — para que a investigação seja barata quando a fatura, e não o teste, der o alarme.
