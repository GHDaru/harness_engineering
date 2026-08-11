# 02 — Loop do Agente

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-11 · [histórico e registro de expiração](../HISTORICO.md)
>
> Esqueleto v3 com camada didática v4 — corpo com o estado da arte; tratamento por repositório no Apêndice A (complementação online).

## Objetivos de aprendizagem

1. **Explicar** o ciclo prompt→decisão→ferramenta→resultado e o critério de parada estrutural;
2. **Comparar** os dois contratos de terminação da indústria (ausência de tool call × `output_type` satisfeito);
3. **Implementar** um loop com freios (turnos, orçamento) e trace observável (etapa 1 do harness-zero);
4. **Projetar** retry em duas camadas (dentro do passo × replay do loop) e reconhecer o que exige idempotência;
5. **Avaliar** a durabilidade de um loop real (o que sobrevive a um crash?).

## O turno que não terminava

Na segunda-feira você pediu ao agente: "o teste `test_login` falhou, corrija". Ele rodou o teste, leu o erro, editou o arquivo, rodou de novo e anunciou o conserto. Quarenta segundos. Você fechou o terminal satisfeito.

Na quarta-feira, o mesmo pedido, em outro repositório. Vinte minutos depois o agente continua trabalhando. Nada travou. Nenhum erro apareceu na tela. Olhando o histórico, você vê a mesma chamada repetida sessenta e três vezes: rodar o teste, ler o mesmo erro, editar o mesmo arquivo, rodar o teste. O modelo não estava confuso. Estava fazendo exatamente o que o loop mandava: continuar enquanto houvesse o que pedir.

A diferença entre segunda e quarta não está no modelo. Está no que o harness combinou sobre **quando parar**.

Este capítulo é sobre essa combinação. O ciclo em si cabe em vinte linhas de código e você vai escrevê-lo daqui a pouco. As perguntas difíceis vêm depois: quem tem autoridade para encerrar o turno, quanto isso pode custar antes de alguém intervir, o que acontece se a máquina morrer no meio, e como um erro volta ao modelo sem derrubar tudo.

## O problema

O loop é o coração do harness. Ele envia contexto ao modelo, recebe uma decisão, executa o que foi decidido, realimenta o resultado e repete.

A decisão do modelo vem em duas formas. Pode ser texto, dirigido a você. Pode ser uma **tool call**: um pedido estruturado de ação, no formato "execute tal ferramenta com tais argumentos". A segunda forma é o que dá braços ao agente.

**Um turno completo, em câmera lenta.** Você digita: "o teste `test_login` falhou, corrija".

1. O harness monta o contexto (regras do projeto mais a sua mensagem) e chama o modelo;
2. O modelo não responde com texto. Responde com uma tool call: `executar_shell("pytest test_login")`;
3. O harness executa de verdade e devolve a saída, o traceback do erro, ao modelo, como se fosse uma nova mensagem;
4. O modelo agora *viu* o erro e emite outra tool call: `editar_arquivo("auth.py", …)`;
5. O harness executa (talvez pedindo sua aprovação, assunto do cap. 07) e devolve o resultado;
6. Nova chamada ao modelo, que pede o teste outra vez. Desta vez passa;
7. O modelo responde **só com texto**: "corrigido, era o cookie expirado".

O passo 7 é o que encerra o turno. Sem tool call, o loop para.

Sete passos, três chamadas ao modelo, duas execuções reais. Repare que o harness nunca decidiu *o que* fazer. Ele decidiu *quando continuar*, e isso é uma responsabilidade diferente.

## Na prática: o loop em vinte linhas, e o que falta nele

Escrito no essencial, o ciclo é este:

```python
def rodar_turno(mensagens, tools):
    while True:
        resposta = modelo.chamar(mensagens, tools=tools)
        mensagens.append(resposta)

        if not resposta.tool_calls:          # parada estrutural
            return resposta.texto

        for chamada in resposta.tool_calls:
            resultado = executar(chamada)
            mensagens.append(resultado)      # o resultado volta como mensagem
```

São nove linhas de lógica e elas já produzem um agente que funciona. Vale ler devagar, porque três decisões de projeto estão escondidas aí.

A primeira está no `if`. O critério de parada é **estrutural**, não semântico: o loop não pergunta se a tarefa foi cumprida, ele observa se o modelo pediu mais alguma coisa. Isso é robusto porque não depende de interpretar linguagem. E é ingênuo pelo mesmo motivo.

A segunda está no `mensagens.append(resultado)`. A saída da ferramenta entra na conversa como mais uma mensagem. É assim que o modelo "vê" o mundo: ele não observa o sistema de arquivos, ele lê o relato de quem observou. Todo o cap. 03 sai dessa frase.

A terceira é a que não está escrita. Não há limite de iterações, não há custo contabilizado, não há nada persistido. É exatamente o loop de quarta-feira.

Agora acrescente os freios:

```python
def rodar_turno(mensagens, tools, max_turnos=50, teto_usd=2.00):
    gasto = 0.0
    for turno in range(max_turnos):
        resposta = modelo.chamar(mensagens, tools=tools)
        gasto += resposta.custo_usd
        mensagens.append(resposta)

        if not resposta.tool_calls:
            return Fim("sucesso", resposta.texto, turno, gasto)
        if gasto >= teto_usd:
            return Fim("teto_de_custo", None, turno, gasto)

        for chamada in resposta.tool_calls:
            try:
                resultado = executar(chamada)
            except Exception as erro:
                resultado = f"ERRO: {erro}"   # erro é dado, não exceção
            mensagens.append(resultado)

    return Fim("max_turnos", None, max_turnos, gasto)
```

Três mudanças, e cada uma carrega uma tese.

O `for` no lugar do `while` transforma "roda até parar" em "roda no máximo tantas vezes". O limite deixa de ser esperança e vira invariante.

O `try` devolve o erro **como texto ao modelo** em vez de propagá-lo. Isso parece descuido e é o oposto: uma exceção derruba o turno e joga fora tudo que já foi feito, enquanto um erro na conversa é informação com a qual o modelo pode se corrigir. Um comando que não existe, um arquivo sem permissão, um teste que quebra: são observações, não catástrofes.

E o retorno agora é um `Fim` com rótulo. Sucesso, teto de custo e esgotamento de turnos são três desfechos diferentes, e quem chamou o loop precisa distinguir os três. Devolver `None` para os dois últimos apaga a informação mais útil que o turno produziu.

Esses vinte linhas são o piso. O estado da arte é o que a indústria colocou em cima delas.

## Fundamentos científicos

**ReAct** ([arXiv 2210.03629](https://arxiv.org/abs/2210.03629)) é o paper seminal: intercalar raciocínio e ação com feedback do ambiente supera raciocínio puro. É a justificativa científica de o loop existir.

O survey de **frameworks de raciocínio agêntico** ([arXiv 2508.17692](https://arxiv.org/abs/2508.17692)) sistematiza as variantes do ciclo (ReAct, plan-and-act, reflexão) e serve de mapa do território.

A fronteira é treinada, não programada. Surveys de **agentic search com aprendizado por reforço** ([arXiv 2510.16724](https://arxiv.org/abs/2510.16724)) mostram o loop deixando de ser só orquestração e virando objeto de treinamento. Quando o modelo é treinado *no* loop, parte do harness migra para os pesos, tese que o cap. 15 retoma.

(Bibliografia completa: `livro/bibliografia.md`.)

## O estado da arte

### 1. Parada virou contrato, não condição

O critério estrutural continua universal e continua insuficiente sozinho. O que a indústria fez foi transformar "quando parar" numa combinação declarada de eixos.

Um limite de turnos, como no seu código. Um **teto de orçamento em dinheiro**, a novidade real de 2025–26, que em alguns harnesses é propagado também aos subagentes: o filho não pode gastar o que o pai não tem. E um **rótulo tipado de terminação**, que é o `Fim` do exemplo levado a sério: sucesso, erro, estouro de turnos e estouro de orçamento viram caminhos de código distintos e obrigatórios, documentados no [loop canônico do Claude Agent SDK (Software Development Kit)](https://code.claude.com/docs/en/agent-sdk/agent-loop).

Existe um segundo contrato, e ele é conceitualmente diferente. Em vez de parar por ausência de pedido, o agente para quando produz **uma saída do tipo declarado**, validável por schema ([OpenAI Agents SDK](https://openai.github.io/openai-agents-python/running_agents/)). A pergunta "acabou?" deixa de ser observação e vira verificação. Isso só funciona quando o resultado tem forma conhecida de antemão, o que exclui conversa aberta e inclui quase toda automação séria.

Dois refinamentos aparecem no benchmark. Um deles gasta uma inferência barata só para decidir se o modelo deve continuar falando sozinho, em vez de devolver o turno ao humano. O outro dá a um hook o poder de **vetar o fim do turno**: o loop anuncia que terminou, um verificador discorda, e o turno recomeça com o feedback anexado. Note o que isso significa. A autoridade de encerrar saiu do modelo e virou algo que o harness pode negar.

### 2. Anti-runaway: do contador ao detector

Todo loop maduro tem um `MAX_TURNS`. Ele resolve o caso do agente que trabalha para sempre e não resolve o caso de quarta-feira, porque sessenta e três repetições cabem folgadas dentro de um limite de cem.

O que resolve é detectar a **repetição**, não a duração. A técnica de campo é simples: guarde um hash de `(ferramenta, argumentos)` numa janela deslizante e interrompa quando o mesmo par reaparecer além de um limiar. Vários harnesses do corpus têm serviços dedicados a isso, com nomes diferentes e a mesma ideia, incluindo estados intermediários que distinguem "lento" de "travado".

Vale o aviso de proveniência: a técnica circula entre praticantes e não tem documentação de fornecedor que a normatize. É citável como prática observada no código, não como norma.

### 3. Durabilidade virou propriedade do loop

Um turno de agente pode durar minutos ou horas. Processos morrem nesse intervalo. A pergunta deixou de ser se o loop sobrevive a um reinício e passou a ser quanto ele repete quando volta.

O consenso de 2026 é **journaling por passo mais replay**: cada passo concluído é registrado antes do próximo começar, e a retomada reexecuta a partir do último registro. Nos repositórios isso aparece como arquivos `jsonl` de rollout, como logs de eventos append-only com estado derivado por leitura, e como filas de entrada com cursor.

Um desenho leva a ideia ao extremo: o executor nunca muta estado. Ele devolve apenas **referências duráveis** ao que deveria acontecer, e um aplicador separado valida a evidência antes de efetivar qualquer coisa. Separar decidir de aplicar é o que torna o replay seguro.

Daí sai um corolário que muda o projeto das ferramentas: se um passo pode ser reexecutado, **idempotência deixa de ser virtude e vira requisito**. Uma tool que cria um recurso a cada chamada é uma bomba de replay. O cap. 05 volta a isso do lado do contrato da ferramenta.

Retry, aliás, são duas coisas que costumam receber o mesmo nome. Repetir a chamada ao provedor depois de um erro de rede acontece **dentro** do passo, com backoff, e é barato. Reexecutar um passo inteiro depois de um crash acontece **fora**, no replay, e só é seguro sob idempotência. Confundir os dois produz cobrança dupla e arquivo duplicado.

### 4. O loop não é o perímetro

A lição arquitetural mais importante da rodada 2 é uma frase deixada no código de um dos harnesses: *"the loop is intentionally not the security perimeter"*. O loop pede efeitos por portas. Quem autoriza é outra camada, e o cap. 07 é inteiro sobre ela.

A mesma disciplina aparece fora do contexto de segurança, na separação entre **política** e **mecânica**. A mecânica é o passo: montar a visão, chamar o modelo, despachar as chamadas. A política é o que decide continuar, pedir confirmação ou desistir. Quando as duas moram na mesma função, trocar o motor de execução exige reescrever as regras de parada. Quando estão separadas, não exige.

### Leitura executiva

O que está mais moderno: terminação tipada com orçamento em dinheiro; juiz separado e endereçável em vez de heurística no prompt; durabilidade por journaling e replay; separação entre política e mecânica.

**O que roubar:** o rótulo tipado de terminação; o orçamento propagado a subagentes; hooks de parada com poder de veto; o executor que devolve referências duráveis em vez de mutar estado.

## Mão na massa — harness-zero, etapa 1

A etapa 1 (`harness-zero/etapas/01-loop/`) é o segundo bloco de código deste capítulo virando programa que roda: parada estrutural, `MAX_TURNS` como freio, erro de tool voltando como texto, e o trace das ações visível no chat.

Dois exercícios de extensão, ambos de completar, não de criar do zero:

- **(a)** o rótulo de terminação vem com dois valores (`sucesso` e `max_turnos`). Acrescente o terceiro, de teto de orçamento, e faça o chat exibir qual deles encerrou o turno.
- **(b)** implemente o detector de repetição da seção 2 com uma janela de cinco chamadas. Teste-o provocando o caso de quarta-feira: uma tool que sempre falha do mesmo jeito.

## Verificação

1. "O modelo respondeu sem tool calls" é um bom default de parada. Por que ele é insuficiente sozinho?
2. Seu agente chamou a mesma tool com os mesmos argumentos cinco vezes seguidas. Liste duas defesas de naturezas diferentes e diga o que cada uma detecta.
3. O processo morreu no meio do turno 7. O que o seu loop precisa ter persistido para retomar sem repetir efeitos colaterais?
4. Um mesmo turno faz retry duas vezes: uma por erro de rede, outra depois de um crash da máquina. Por que só a segunda exige idempotência das tools?

---

## Apêndice A — Como cada repositório trata o loop

> Evidência por harness, com paths — complementação online, expandida a cada rodada.

### opencode (rodada 1)
`packages/opencode/src/session/processor.ts`: resposta consumida como `Stream` do Effect (`Stream.tap(handleEvent)` → `takeUntil(needsCompaction)` → `runDrain`); veredito explícito `continue | stop | compact`; retry por provedor (`SessionRetry.policy`); V2 (`CONTEXT.md`): inbox durável e eventos replayáveis com cursores.

### gemini-cli (rodada 1)
`packages/core/src/core/client.ts` (`MAX_TURNS=100`) + `turn.ts`; **next-speaker check** (`utils/nextSpeakerChecker.ts`: mini-prompt `{reasoning, next_speaker}` re-invoca o stream se `model`); `LoopDetectionService`; separação core/cli limpa.

### OpenHarness (rodada 1)
`src/openharness/engine/query.py` (`run_query`): `while` async até `max_turns` ou sem tool-uses; **paralelismo quando todas as tools do turno são read-only** (`asyncio.gather`); PreToolUse → permissão → execução → PostToolUse por chamada; retry com backoff e cost tracking.

### Codex CLI (rodada 2)
`core/src/session/turn.rs` (`run_turn`, 2.581 linhas) sobre `SessionTask` trait (Regular/Review/Compact/UserShell); streaming SSE (Server-Sent Events) **e WebSocket com fallback WS→HTTPS**; `CancellationToken` hierárquico; cada turno persistido em rollout jsonl; sem detector de repetição explícito (mitigado por budgets).

### Goose (rodada 2)
`crates/goose/src/agents/agent.rs` (`reply` → `BoxStream<AgentEvent>`): dois níveis de retry (transiente por provedor + `RetryManager` de recipe com `SuccessCheck` que reseta a conversa); `DEFAULT_MAX_TURNS=1000`; `RepetitionInspector`; `MAX_EMPTY_TURN_RETRIES=3`.

### OpenClaw (rodada 2)
`src/system-agent/agent-turn.ts` + `gateway/agent-*.ts`: runs serializados por *session lane* com write-lock file-based inter-processo; três streams de eventos (lifecycle/assistant/tool); watchdogs `stalled/stuck`; hooks duplos (Gateway + plugins).

### Hermes (rodada 2)
`agent/conversation_loop.py` (~6.5k linhas) com fases separadas (turn_context/tool_executor/turn_finalizer); `iteration_budget`; **interrupt-and-redirect** (`/steer` drenado pré-API e pós-tool); nudges para respostas vazias; reparo de alternância de papéis; **verify-on-stop nudge**.

### IronClaw (rodada 2) ⭐
`crates/ironclaw_agent_loop`: pipeline de estágios selados (input → prompt → model → capability → gate/checkpoint → stop), cada estágio uma strategy privada; o executor devolve um `LoopExit` contendo **apenas referências duráveis** — nunca muta estado — e o `LoopExitApplier` valida evidência host-owned antes de aplicar (tese explícita da arquitetura: *"the loop is intentionally not the security perimeter"*). Estado resumível por checkpoints; máquina de estados Queued→Running→Blocked→Completed com leases/heartbeats; "one active run per canonical thread".

### Aider (rodada 2)
`aider/coders/base_coder.py`: não é um loop de tool-calling — é REPL de chat + edição direta. O único mecanismo iterativo é a **reflexão** (`reflected_message`, máx. 3): arquivos pedidos fora do chat, erros de linter ou testes falhando disparam nova rodada, sempre com confirmação humana. Auto-correção reativa por design, não autonomia.

### OpenHands/Canvas (rodada 2)
`app_server/event/`: o event-stream persiste cada `Event` como JSON por conversa (paginação, filtros, export de trajetória) — mas o loop ação/observação roda no `openhands-agent-server` (SDK); o app consome eventos, não os gera. O núcleo está no software-agent-sdk (abaixo).

### ohmo (rodada 2.5)
Loop herdado do `QueryEngine` do OpenHarness; o que é próprio: **pool multi-sessão** (`ohmo/gateway/runtime.py`: um `RuntimeBundle` por `session_key`, recriado quando o cwd muda) e **interrupção real por mensagem nova** (`bridge.py`: cada mensagem é uma asyncio.Task; mensagem nova da mesma sessão cancela a anterior) — poucos concorrentes cancelam corretamente.

### n8n (rodada 2)
A V2 usa o `AgentExecutor` clássico do LangChain (`maxIterations` default 10); a **V3** mantém o `createToolCallingAgent` só para *decidir* — as tool calls viram `EngineRequest` devolvidos ao **motor de workflow do n8n**, que agenda os nós-tool e reentra com `EngineResponse` (`ToolsAgent/V3/helpers/runAgent.ts`). O n8n reinternalizou o loop de execução: decisão do framework, execução do engine.

### Frameworks (rodada frameworks) — quatro respostas à mesma pergunta
**LangGraph**: a primitiva real é **Pregel/BSP** (supersteps + channels + reducers), com retry/cache/timeout por nó — e o agente pronto (`create_react_agent`) formalmente deprecado (migrou para `langchain.agents`). **OpenAI Agents SDK (Software Development Kit)**: loop explícito em `run.py` (output_type termina · handoff troca agente · `max_turns` com handlers), sobre um `AgentRunner` substituível. **CrewAI**: executor **100% próprio, zero LangChain** (`crew_agent_executor.py`), com dispatch duplo — tool-calling nativo ou fallback ReAct com `json_repair`. **software-agent-sdk**: `LocalConversation.run()` (política: parar, confirmar, desistir) separado de `Agent.step()` (mecânica stateless view → LLM → dispatch), event log append-only com `View` derivada e hooks `Stop` com poder de **veto** sobre o término.

---

## Respostas da verificação

**1.** Porque ele observa a forma da resposta, não o estado do trabalho. O modelo pode parar de pedir ferramentas por ter concluído, por ter desistido ou por ter se convencido de algo falso, e os três casos produzem a mesma resposta sem tool call. Por isso o critério estrutural entra num contrato com outros eixos: turnos, orçamento, tipo de saída validável e, quando existe, um verificador com poder de veto.

**2.** Um teto (de turnos ou de dinheiro) detecta *duração*: ele encerra qualquer coisa que passe do limite, incluindo trabalho legítimo e demorado. Um detector de repetição detecta *falta de progresso*: ele compara chamadas recentes por ferramenta e argumentos e interrompe quando o par se repete. As duas defesas são de naturezas diferentes porque o loop de quarta-feira passa folgado no teto e é pego pelo detector, enquanto uma tarefa longa e produtiva é pega pelo teto e ignorada pelo detector.

**3.** O registro do último passo concluído, com o resultado que ele produziu, gravado **antes** de o passo seguinte começar. Sem isso a retomada não sabe onde parou. E as ferramentas mutantes precisam ser idempotentes, ou uma chave de deduplicação por chamada, porque a retomada pode reexecutar o passo que já tinha surtido efeito antes do crash.

**4.** Porque o retry de rede acontece antes de o efeito existir: a chamada falhou no caminho de ida, nada foi executado, e repetir é seguro por construção. O retry por replay acontece depois de um crash que pode ter interrompido o processo *entre* o efeito e o registro dele. Nesse caso o harness não tem como saber se o arquivo foi criado, e a única defesa é que criá-lo duas vezes dê no mesmo.
