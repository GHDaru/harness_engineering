# 02 — Loop do Agente

## O problema

O loop é o coração do harness: o ciclo que envia o contexto ao modelo, recebe uma decisão (texto, tool-call ou ambos), executa as ferramentas solicitadas, realimenta os resultados e repete — até que alguém decida parar. As perguntas de projeto são poucas, mas cada uma tem consequências profundas:

1. **Quem decide quando parar?** O modelo (deixou de chamar tools), uma heurística, um contador de turnos, ou outro modelo?
2. **Como os resultados voltam?** Streaming ou blocos completos? Como erros de tool são apresentados?
3. **O que acontece quando dá errado?** Retry, backoff, troca de provedor, detecção de loop repetitivo?
4. **O loop é durável?** Sobrevive a reinício de processo, ou uma queda perde a tarefa?

## Padrões de implementação

- **Parada por ausência de tool-call** — o padrão universal: se a resposta do modelo não contém chamadas de ferramenta, o turno acabou.
- **Limite de turnos/passos** — proteção contra runaway (contadores como `MAX_TURNS`).
- **Next-speaker check** — um mini-prompt barato pergunta a um modelo "quem fala agora, usuário ou modelo?" para decidir se o agente continua sozinho.
- **Detecção de loop** — identificar o agente repetindo a mesma ação e abortar/recuperar.
- **Paralelismo seletivo** — executar em paralelo apenas tools sem efeito colateral (read-only), serializando as demais.
- **Durabilidade** — persistir a admissão do prompt e os eventos do loop, permitindo replay e retomada.

## Como os harnesses estudados implementam

### opencode — loop como stream, com durabilidade projetada
O loop vive em `packages/opencode/src/session/processor.ts`: a resposta do LLM é consumida como um `Stream` do Effect-TS (`Stream.tap(handleEvent)` → `Stream.takeUntil(needsCompaction)` → `Stream.runDrain`), e cada evento (texto, tool-call, reasoning) passa por um handler que executa e realimenta. O loop retorna um veredito explícito — `continue | stop | compact` — integrando a compactação ao próprio ciclo. Há retry por provedor (`SessionRetry.policy`) e limite de passos. A arquitetura V2 (documentada em `CONTEXT.md`) formaliza o loop como "Session Drain": prompts entram numa inbox durável, eventos são persistidos e replayáveis com cursores — o loop sobrevive a reinício de processo.

### gemini-cli — o loop que sabe quando calar
O loop está em `packages/core/src/core/client.ts` (com `MAX_TURNS = 100`) e cada turno é uma abstração própria (`core/turn.ts`). O diferencial é o **next-speaker check** (`utils/nextSpeakerChecker.ts`): após cada resposta, um mini-prompt com schema JSON `{reasoning, next_speaker: user|model}` decide se o modelo deve continuar automaticamente (ex.: a resposta termina em "Next, I will…") ou devolver o controle ao usuário — se `model`, o stream é re-invocado recursivamente. Complementa com um `LoopDetectionService` (`services/loopDetectionService.ts`) que aborta loops repetitivos. A separação é limpa: `packages/core` orquestra, `packages/cli` só renderiza.

### OpenHarness — loop legível com paralelismo read-only
O loop é um `while` async explícito em `src/openharness/engine/query.py` (`run_query`, ~39 KB de código): faz streaming da API, encerra quando `final_message.tool_uses` está vazio, e respeita `max_turns`. O detalhe mais interessante: se **todas** as tools solicitadas no turno são read-only, executa em paralelo via `asyncio.gather`; qualquer tool com efeito colateral serializa o lote. Cada execução passa pela sequência PreToolUse hook → verificação de permissão → execução → PostToolUse hook. Por ser um port declarado do Claude Code em Python, é o melhor código para *estudar* a anatomia de um loop de produção.

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Parada | sem tool-call + veredito `continue/stop/compact` | sem tool-call + next-speaker check (LLM) | sem tool-call + `max_turns` |
| Anti-runaway | limite de passos, retry por provedor | `MAX_TURNS=100` + LoopDetectionService | `max_turns` + retry/backoff |
| Paralelismo de tools | — (serial por evento de stream) | scheduler dedicado | paralelo se todas read-only |
| Durabilidade | inbox durável + eventos replayáveis (V2) | sessão persistida (não replay de loop) | sessão persistida |

A divergência mais interessante é **quem decide continuar**: opencode usa o veredito estrutural do próprio loop, gemini-cli gasta uma chamada de modelo extra para decidir (next-speaker), e OpenHarness confia na convenção pura. É um trade-off custo × fluidez: o next-speaker check torna o agente mais "insistente" em terminar tarefas sem intervenção, ao custo de uma inferência por turno.
