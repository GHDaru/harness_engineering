# 04 — Compactação

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](../HISTORICO.md)
>
> Camada didática v4 — ver [Guia Editorial §2.1](../GUIA-EDITORIAL.md).
> andaime: completo
>
> **Capítulo-piloto do esqueleto v3** — corpo com o estado da arte; tratamento por repositório no Apêndice A (complementação online, atualizado a cada rodada do benchmark).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Explicar** por que a compactação existe e quais restrições ela equilibra (fidelidade × custo × cache);
2. **Comparar** as quatro camadas da escada de agressividade e **justificar** a ordem entre elas;
3. **Analisar** a implementação de compactação de um harness real e localizar suas escolhas na escada (Apêndice A como gabarito);
4. **Implementar** truncamento com preservação de bordas e sumarização com tail preservado (etapa 5 do harness-zero);
5. **Avaliar** quando uma compactação falhou (perda de decisão, de estado de arquivo ou de objetivo) — e **antecipar** o que muda quando o provedor compacta por você.

## O agente que desfez o próprio conserto

Turno 38. O agente já achou o bug, editou `auth.py`, rodou o teste e viu passar. Falta ajustar dois arquivos vizinhos e acabou.

Turno 40. A janela lota. O harness compacta: resume os 39 turnos anteriores em meia página e continua.

Turno 41. O agente abre `auth.py`, olha, e **desfaz o conserto**. Ele reescreve a função para a versão de antes, roda o teste, vê falhar, e começa a investigar de novo o bug que já tinha resolvido.

O resumo dizia, com toda honestidade: *"editei auth.py para corrigir o cookie expirado"*. Está correto. O que ele não dizia era **como** ficou o arquivo depois da edição — e o modelo, sem essa informação, fez o que qualquer um faria: foi conferir, leu um código que não reconhecia como seu, e "consertou".

A compactação não perdeu a conversa. Perdeu o **estado**. E o pior é que ela não tinha como saber: um resumo em prosa livre não tem campo obrigatório para "situação atual dos arquivos".

Este capítulo é sobre o que se joga fora quando não cabe mais tudo, e sobre por que a ordem em que se joga fora importa mais que a taxa de compressão.

## O problema

Toda conversa de agente cresce até não caber na janela de contexto do modelo. A compactação é o conjunto de estratégias para continuar trabalhando quando isso acontece — sem perder o que importa. É a dimensão onde os harnesses avaliados mais convergem: todos chegaram, independentemente, à mesma arquitetura em camadas.

As restrições em tensão:
- **Fidelidade**: o resumo não pode perder decisões, estado de arquivos ou o objetivo da tarefa.
- **Custo**: sumarizar via LLM (Large Language Model) é caro; truncar é barato mas destrutivo.
- **Cache**: compactar invalida o prefixo cacheado — deve acontecer o mínimo possível e em momentos controlados.

## Fundamentos científicos

- **A janela não é uniforme**. *Lost in the Middle* ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)) mostrou que modelos usam melhor o início e o fim do contexto e degradam no meio. É a base empírica de duas práticas da escada: preservar o *tail* recente intacto e truncar outputs mantendo início+fim.
- **Contexto como memória virtual**. *MemGPT* ([arXiv 2310.08560](https://arxiv.org/abs/2310.08560)) formulou a analogia com sistemas operacionais: a janela é a "RAM", o armazenamento externo é o "disco", e o harness pagina entre eles. Trabalhos recentes levam a analogia ao limite literal (*demand paging*, [arXiv 2603.09023](https://arxiv.org/abs/2603.09023)).
- **Compactar é decisão de orçamento**. *ContextBudget* ([arXiv 2604.01664](https://arxiv.org/abs/2604.01664)) trata a gestão de contexto como alocação explícita por tipo de conteúdo — o que os produtos implementam como limiares e budgets.

(Bibliografia completa e status de validação: `livro/bibliografia.md`.)

## Fontes da indústria

- **[Compaction — Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/compaction)** (Anthropic, oficial): a compactação chegou **ao nível da API** (beta `compact-2026-01-12`) — o provedor sumariza automaticamente ao atingir o limiar configurado e devolve um "compaction block". É a confirmação de vendor da tendência central deste capítulo (ver Estado da arte).
- **Práticas de operação do Claude Code** ([CometAPI](https://www.cometapi.com/what-is-auto-compact-in-claude-code/), [okhlopkov](https://okhlopkov.com/claude-code-compaction-explained/), [hyperdev](https://hyperdev.matsuoka.com/p/how-claude-code-got-better-by-protecting)): a recomendação convergente dos praticantes é a mesma que os harnesses codificam — **o que precisa sobreviver à compactação não deve morar na conversa**: convenções vão para o arquivo de contexto (CLAUDE.md/AGENTS.md, reinjetado a cada sessão) e estado de progresso vai para arquivos que o agente relê depois do compact. A compactação define, por exclusão, o que merece persistência.
- **Consulte também**: a coleção viva [Awesome Harness Engineering — Context Delivery & Compaction](https://github.com/GHDaru/awesome-harness-engineering#context-delivery--compaction) reúne mais recursos consultáveis desta dimensão (padrões, artigos e implementações), curados por problema.

## Na prática: a escada, com os números de cada degrau

A escada de agressividade é uma sequência de tentativas, da mais barata à mais cara, e cada degrau só roda se o anterior não bastou. Escrita, ela cabe numa função:

```python
ORCAMENTO = 100_000        # tokens que o modelo pode ver

def compactar(historico: list[Message]) -> list[Message]:
    """Devolve a VISÃO enviada ao modelo. O registro persistido não muda."""
    v = truncar_saidas(historico)          # 1. barato, local, sem LLM
    if custa(v) <= ORCAMENTO:
        return v

    v = podar_resultados_antigos(v)        # 2. barato, apaga conteúdo velho
    if custa(v) <= ORCAMENTO:
        return v

    return sumarizar(v)                    # 3. caro: uma chamada de LLM
```

Os dois primeiros degraus custam microssegundos; o terceiro custa uma chamada de modelo e alguns segundos. Só isso já justificaria a ordem. Mas há um motivo melhor, e é de **destrutividade**.

```python
def truncar_saidas(h, teto=4_000):
    """Corta a saída da tool preservando as duas bordas: o começo diz o que é,
    o fim diz como terminou. O meio de um log raramente decide alguma coisa."""
    out = []
    for m in h:
        if m.papel == "tool" and len(m.conteudo) > teto:
            cabeca, cauda = m.conteudo[: teto // 2], m.conteudo[-teto // 2 :]
            ref = arquivar(m.conteudo)     # o integral vai para disco, não para o lixo
            m = m.com(conteudo=f"{cabeca}\n… [{ref}] …\n{cauda}")
        out.append(m)
    return out
```

Repare no `arquivar`. O refinamento moderno da camada 1 não é cortar melhor, é **não descartar**: o conteúdo íntegro vai para um arquivo referenciável, e o modelo pode pedi-lo de volta se precisar. Truncar deixa de ser perda e vira paginação.

O terceiro degrau é onde a cena da abertura acontece, e é onde a forma do resumo decide tudo:

```python
def sumarizar(h, cauda=8):
    antigos, recentes = h[:-cauda], h[-cauda:]     # a cauda vai intacta
    resumo = llm.completar(
        PROMPT_DE_RESUMO, antigos,
        formato={                                   # campos OBRIGATÓRIOS
            "objetivo_do_usuario": str,             # por que estamos aqui
            "decisoes": list[str],                  # o que já foi decidido
            "estado_dos_arquivos": dict[str, str],  # ← o que faltou no turno 40
            "pendencias": list[str],                # o que falta fazer
        })
    return [Message("system", render(resumo)), *recentes]
```

O `estado_dos_arquivos` é a diferença entre o resumo que salva e o resumo que sabota. Um resumo em prosa livre escreve *"editei auth.py"*; um resumo com campo obrigatório é forçado a escrever *"auth.py: `max_age` corrigido para 3600, teste passando"*. O primeiro é verdade e não impede o agente de desfazer; o segundo impede.

A cauda intacta tem a mesma natureza. Os últimos turnos vão **sem resumir**, porque são os que contêm o trabalho em curso, e resumir o que está acontecendo agora é o jeito mais rápido de perder o fio.

E a invariante que atravessa os três degraus está no comentário da primeira função: a compactação altera a **visão** enviada ao modelo, **nunca** o registro persistido do cap. 08. Quem confunde as duas coisas descobre, no primeiro incidente, que compactou a única cópia.

## O estado da arte

### O padrão consolidado: a escada de agressividade

Os harnesses aplicam as estratégias em escada, da mais barata à mais cara — este é o consenso da indústria, verificado em todas as rodadas do benchmark:

1. **Truncar saídas de tools na origem**: limitar linhas/bytes antes de entrar no histórico, preservando início e fim (*Lost in the Middle* justifica as bordas). O refinamento moderno: **não descartar** — mover o conteúdo integral para arquivos referenciáveis (opencode) ou manter o bruto fora da view do modelo mas visível na UI (Goose).
2. **Prune / microcompact**: apagar o *conteúdo* de resultados de tools antigas (o modelo raramente relê um `cat` de 30 turnos atrás), mantendo o registro da chamada. Camadas intermediárias mais novas: *tool distillation* e *output masking* (gemini-cli).
3. **Sumarização via LLM (full compact)**: resumir a porção antiga preservando um tail intacto (tipicamente 20–30% ou um orçamento de 2k–20k tokens). O estado da arte tem três refinamentos: **resumo estruturado** com campos obrigatórios (intenção do usuário, tarefas pendentes, estado de código — Goose e software-agent-sdk), **modelo auxiliar barato** para o resumo (Hermes), e **flush de memória antes de compactar** — salvar notas duráveis antes de perder o contexto (OpenClaw).
4. **Disparo automático + caminho reativo**: gatilho por percentual da janela (50–90% conforme o projeto) e, cobrindo a falha, compactação **reativa** ao erro "prompt too long" da API (OpenHarness, OpenClaw).

### As duas fronteiras modernas

**1. Compactação auditável, com tombstones.** A implementação mais avançada medida no benchmark não muta o histórico. O log é append-only e o esquecimento é um **evento**, um tombstone no mesmo sentido que bancos distribuídos dão à palavra.

A visão do modelo é derivada aplicando os tombstones. Nada se perde para auditoria, e as invariantes formais viram **código testável**: pareamento entre chamada e resultado, atomicidade de lote.

Daí sai uma distinção que vale roubar, entre gatilho **suave** e **duro**. Se compactar agora violaria uma invariante, o gatilho suave espera o próximo turno; o duro força um reset explícito. Um refinamento correlato é o **circuit-breaker de efetividade**: comparar o tamanho antes e depois e desistir da compactação que não compactou.

**2. A compactação está migrando para o provedor.** O cache também virou contrato de protocolo: a spec MCP 2026-07-28 acrescentou `ttlMs` e `cacheScope` às respostas de `tools/list`, com o protocolo assumindo o que antes era heurística do harness.

Há dois sinais independentes no mesmo ano. Um harness do corpus implementa **compactação remota**, com o backend compactando; e a compactação apareceu como recurso **da própria API** ([docs](https://platform.claude.com/docs/en/build-with-claude/compaction), beta `compact-2026-01-12`).

É a cláusula de expiração em movimento, com uma inversão interessante. Em vez de o componente desaparecer quando o modelo melhora, ele **muda de dono**: sai do harness e vai para a plataforma.

O que resta ao harness quando o provedor compacta são três coisas concretas. Decidir *o que proteger*, como skills, estado de tarefa e arquivos de memória. Decidir *quando confiar*, auditando a qualidade do resumo. E manter o caminho reativo para quando a compactação remota falhar.

> **Adendo (2026-07-31, texto integral verificado): a terceira via, compactação aprendida no treino.** O preprint [CompactionRL](https://arxiv.org/abs/2607.05378) (Tsinghua/Z.AI, 06-jul-2026) propõe o passo seguinte da migração: treinar o modelo por RL **com a compactação dentro do loop**.
>
> Nas palavras do paper, *"CompactionRL incorporates compaction into rollout collection, and reconstructs the agent context from a summary once context budget is exhausted"* (§1), e a sumarização vira *"a learned part of the model rather than an inference-time heuristic"*, com recompensa de nível de **tarefa**. Os números da Tabela 2 são medidos sempre contra o mesmo modelo *já com compactação de inferência*, que é a comparação honesta.
>
> Se a linha se confirmar, a compactação não muda só de dono: muda de **camada**, do harness para os pesos.

### A terceira fronteira: a compactação deixa de ser involuntária (rodada ext-4, 2026-08)

O lançamento do **Prime Agent** (ago/2026) veio com uma acusação direta a este capítulo: *"fixed tool-calling schemas and context compaction force the model to work around its own scaffolding instead of leveraging it"*.

A leitura do código ([avaliação completa](../../benchmark/avaliacoes/prime-agent.md)) mostra que **a acusação é retórica e o código diz outra coisa**. A diferença entre as duas é o achado.

A compactação **não foi eliminada nem enfraquecida**. O Prime Agent é construído sobre o Pi, e as 1.398 linhas de `core/compaction/` estão lá intactas, com corte seguro, split de turnos, arquivos cumulativos e recuperação reativa de estouro, ainda melhoradas com instruções customizadas.

O que mudou é **quem manda**. As funções de compactar e de consultar o estado (`skills/compact/`) viraram chamáveis **pelo próprio agente**, com um handler que **agenda em vez de executar**, porque executar na hora abortaria a célula do REPL que pediu a compactação. E elas rodam mesmo com a compactação automática desligada, sob doze casos de teste.

A ressalva a registrar é, portanto, precisa: **a compactação deixa de ser um evento involuntário do harness e passa a ser um mecanismo entre outros, disponível ao agente**. Ela ganha ainda um papel novo, o de gatilho de destilação: toda compactação vira oportunidade de o agente extrair aprendizado do que está prestes a ser resumido.

O que a escada não previa não é a própria obsolescência, é a **inversão do controle**. Até aqui, o harness compacta *no* agente; aqui, o agente compacta *a si mesmo*.

E a lacuna que a leitura encontrou é reveladora. O anúncio menciona um subagente atuando como coletor de lixo do REPL, e **não existe nada disso no código**: a busca por `garbage`, `prune` e `evict` nos diretórios de código não retorna nada. O contexto como variável resolve o acesso ao passado; ele **não** resolve o crescimento do namespace que ele mesmo cria.

### Leitura executiva

A convergência na escada é quase total. O padrão está consolidado, e um harness novo que não a implemente precisa justificar.

As diferenças que restam são refinamentos de fidelidade: estruturar o resumo, auditar a qualidade dele, nunca descartar. E a grande questão em aberto é de **arquitetura de mercado**: quanto da escada sobrevive no harness quando a plataforma oferece compactação como serviço. O adendo acima agudiza a pergunta, porque depois de migrar para o provedor a compactação começa a migrar para os **pesos**.

**O que roubar:**

- **Tombstones sobre log append-only**, com a visão derivada e nada perdido para auditoria.
- **Flush de memória antes de compactar**: salve as notas duráveis enquanto o contexto ainda existe.
- **Resumo estruturado** com campos obrigatórios, sobretudo o estado dos arquivos.
- **Circuit-breaker de efetividade**: se compactar não encolheu, não adianta compactar de novo.
- **Cauda intacta**, porque o trabalho em curso não sobrevive a um resumo.

> **Ressalva de edição (2026-08-06).** Esta Leitura executiva foi confrontada na rodada ext-4 e **mantida**, com a qualificação da seção anterior: a escada continua sendo o padrão, mas a *autoridade* sobre quando aplicá-la começou a migrar para o agente. Se o padrão se repetir em outros harnesses, a síntese muda, e este parágrafo será reescrito, não emendado.

## Mão na massa — harness-zero, etapa 5

Na etapa 5 do projeto `harness-zero/` (`harness-zero/etapas/05-compactacao/`) você implementa a escada da seção "Na prática" no seu próprio harness, nesta ordem:

1. truncamento de saída de tool com preservação de início e fim;
2. prune de resultados de tools antigas, além de um orçamento;
3. sumarização via LLM da cabeça do histórico, preservando a cauda;
4. disparo automático por limiar de tokens estimados.

Some-se um **indicador visível no chat** quando a compactação acontece: é a janela de observação do leitor, e sem ela a compactação é invisível justamente quando mais importa entendê-la.

Exercício de completude: o esqueleto da função de prune vem pronto. Você escreve a seleção do que proteger.

## Verificação

1. Por que truncar saídas de tools **antes** de sumarizar via LLM, e não o contrário?
2. Um harness sumarizou o histórico e o agente, no turno seguinte, reescreveu um arquivo que já estava correto. Qual informação a compactação provavelmente perdeu, e qual mecanismo do estado da arte previne isso?
3. Seu provedor passou a oferecer compactação na API. Quais responsabilidades da escada você **transfere** e quais **mantém** no harness?
4. A compactação roda pela segunda vez na mesma sessão. Que classe de defeito só aparece aí, e por quê?

---

## Apêndice A — Como cada repositório trata a compactação

> Evidência por harness, com paths — material de complementação (versão online), expandido a cada rodada do benchmark. Fonte-base do capítulo: o código destes repositórios.

### opencode (rodada 1) — três mecanismos + arquivos gerenciados
`packages/opencode/src/session/compaction.ts` (+ `overflow.ts`, `summary.ts`): (a) sumarização automática em overflow com **agente dedicado `compaction`**, tail sob orçamento (`preserveRecentBudget`, 2k–8k tokens), novo Context Epoch e auto-continue opcional; (b) **prune** de trás para frente marcando `compacted` saídas de tools além de 40k tokens (`PRUNE_PROTECT`), protegendo skills; (c) truncamento na origem (`tool/truncate.ts`) preservando início+fim e movendo o texto completo para "Managed Tool Output Files".

### gemini-cli (rodada 1) — compressão + destilação + mascaramento
`packages/core/src/context/chatCompressionService.ts`: dispara a 50% do limite (`DEFAULT_COMPRESSION_TOKEN_THRESHOLD = 0.5`), preserva os últimos 30% (`COMPRESSION_PRESERVE_THRESHOLD`), orçamento próprio para function responses (50k) e salvamento de outputs truncados. Camadas extras: `toolDistillationService.ts` e `toolOutputMaskingService.ts`. `/compress` manual, evento `ChatCompressed`, hooks `PreCompressTrigger`.

### OpenHarness (rodada 1) — a tradução fiel do Claude Code
`src/openharness/services/compact/__init__.py` (1.725 linhas; docstring: "Faithfully translated from Claude Code's compaction system"): **microcompact** (limpa `COMPACTABLE_TOOLS`), **full compact** (resumo LLM), **auto-compact** (limiar) e compactação **reativa** a "prompt too long" (`_is_prompt_too_long_error`). Hooks `PRE_COMPACT`/`POST_COMPACT`; preserva task state e logs de canal.

### Codex CLI (rodada 2) — local + remota v1/v2
`core/src/compact.rs`, `compact_remote_v2.rs`, `compact_token_budget.rs`: auto-compact a ~90% da janela; três estratégias — local (`SUMMARIZATION_PROMPT`) e **remota v1/v2** (o backend compacta, via `ResponsesStreamRequest::RemoteCompactionV2`, com retry próprio); janelas versionadas com prefill tracking; injeção controlada pré/mid-turn; `TruncationPolicy` para outputs.

### Goose (rodada 2) — resumo estruturado + middle-out
`crates/goose/src/context_mgmt/mod.rs`: limiar 0.8 da janela; `StructuredSummary` (user_intent, files, pending_tasks, current_work); se a sumarização estoura, **remoção progressiva "middle-out"** de tool-responses (0→100%); **sumarização incremental de pares tool-call/response** em batches de 10 protegendo os N últimos; metadados de visibilidade preservam o bruto na UI; respeita `provider.manages_own_context()`.

### OpenClaw (rodada 2) — safeguard + memory flush
`src/context-engine/` + `docs/concepts/compaction.md`: auto por limiar e reativa (reconhece dezenas de strings de erro de overflow de múltiplos provedores), split preservando pares tool-call/result; modo `safeguard` com **auditoria de qualidade do resumo**; **memory flush silencioso antes de compactar**; `keepRecentTokens` 20k; providers de compactação plugáveis; distinção compaction (semântica) × pruning (trim in-memory).

### Hermes (rodada 2) — engine plugável + modelo auxiliar
`agent/context_engine.py` (interface `should_compact`/`compress`/`prune`) + `trajectory_compressor.py` (~1.6k linhas): sumarização de tool-responses antigas via **modelo auxiliar barato** (default Gemini Flash, até 50 requisições concorrentes); `/compress` manual; `/usage` e `/insights` expõem a janela.

### IronClaw (rodada 2) — política pura + circuit-breaker
`crates/ironclaw_agent_loop/src/strategies/compaction.rs` (+ `active_task_compaction.rs`): a estratégia é **política pura** (retorna Skip ou o limite `drop_through_seq`; mutação só no host); `PromptContextTokenBudget` com `preserve_tail_tokens`; **circuit-breaker de efetividade** (compara estimativa pós-compactação contra `CompactionEffectivenessBaseline`); variante que preserva a tarefa ativa; o host rejeita compactar através de mensagens não-usuário.

### software-agent-sdk (rodada frameworks) — tombstones + invariantes testáveis ⭐
`openhands-sdk/openhands/sdk/context/condenser/`: esquecimento por **tombstones** (`Condensation` event) sobre log append-only; disparo por três razões (REQUEST/TOKENS/EVENTS) com **hard/soft** (`condensation_requirement`) e `hard_context_reset()` para o caso patológico; `keep_first` + re-sumarização recursiva de sumários; prompt estruturado (`summarizing_prompt.j2`: USER_CONTEXT, TASK_TRACKING com IDs exatos, CODE_STATE, TESTS, CHANGES); invariantes em `context/view/properties/` (tool_call_matching, batch_atomicity...) **testadas contra LLMs reais** (`tests/integration/tests/c01..c05`); `pipeline_condenser` para compor.

### Aider (rodada 2) — sumarização clássica bem-feita
`aider/history.py` (`ChatSummary`): mantém a cauda (~metade do orçamento), sumariza a cabeça via LLM com split após mensagem `assistant`, **recursivo** até profundidade 3, com lista de modelos com fallback.

### n8n (rodada 2) — a ausência que confirma a categoria
Sem compactação no loop (`contextWindowLength` dos memory sub-nodes + `maxTokensFromMemory` apenas) — coerente com execuções curtas acionadas por evento; é o teto da categoria "harness embutido" para tarefas longas.

### LangGraph / OpenAI Agents SDK / CrewAI (rodada frameworks) — a linha divisória
LangGraph: **zero suporte nativo** (uma docstring sugerindo `pre_model_hook`); Agents SDK (Software Development Kit): apenas `OpenAIResponsesCompactionSession` como session opcional; CrewAI: nada. A compactação é a dimensão que mais separa "framework" de "harness pronto".

---

## Respostas da verificação

**1.** Por custo e por destrutividade, e a segunda razão é a que decide. Truncar é local, não chama modelo nenhum e, no refinamento moderno, **não perde nada**: o conteúdo íntegro vai para um arquivo referenciável. Sumarizar custa uma chamada de LLM, leva segundos e é **irreversível na visão** — o que o resumo não capturou não volta. Rodar o caro antes do barato significa pagar mais para perder mais, e ainda por cima resumir megabytes de saída de tool que o truncamento teria eliminado de graça. A escada é ordenada por dano crescente, e o custo apenas acompanha.

**2.** A compactação perdeu o **estado dos arquivos**: ela guardou que uma edição aconteceu e não guardou como o arquivo ficou. É o que o resumo em prosa livre faz de pior, porque a frase *"editei auth.py"* é verdadeira e inútil. O mecanismo do estado da arte que previne isso é o **resumo estruturado com campos obrigatórios**, em que o modelo é forçado a preencher o estado atual do código, as decisões tomadas e as pendências. Um campo obrigatório não pode ser esquecido por elegância de redação. A defesa complementar é a **cauda intacta**: os últimos turnos vão sem resumir, e é neles que o trabalho em curso está descrito com precisão.

**3.** Transfere-se o degrau **caro**: a sumarização, que é onde o provedor tem vantagem real, porque ele enxerga a conversa inteira do lado dele e pode compactar sem uma ida e volta extra. Mantêm-se os degraus **baratos e locais** — truncar saída de tool na origem e podar resultados antigos —, porque eles dependem de conhecimento que só o harness tem: quais saídas são de ferramentas suas, o que já foi arquivado em disco, qual é o orçamento do seu produto. E mantém-se, sobretudo, a **invariante do registro**: o provedor compacta a visão dele; o log durável continua sendo seu, e é dele que sai auditoria, retomada e reversão. Terceirizar a compactação sem manter o registro é ficar sem a única cópia.

**4.** A classe de defeito é o **resultado órfão**: um resultado de ferramenta cuja chamada correspondente já saiu do histórico. Na primeira compactação, chamada e resultado costumam estar no mesmo bloco resumido, e o par se mantém coerente. Na segunda, o resumo da primeira passada já substituiu parte do histórico, e o pareamento pode quebrar: sobra o resultado sem a chamada, ou a chamada sem o resultado, e o modelo recebe um histórico que não é sequer sintaticamente válido para a API. É um caso datado e real no corpus, e ele expõe o que o capítulo por muito tempo não discutiu: a compactação é uma operação **repetida**, e o que quebra não é compactar, é **compactar o que já foi compactado**.
