# 04 — Compactação

## O problema

Toda conversa de agente cresce até não caber na janela de contexto do modelo. A compactação é o conjunto de estratégias para continuar trabalhando quando isso acontece — sem perder o que importa. É a dimensão onde os três harnesses estudados mais convergem: todos chegaram, independentemente, à mesma arquitetura em camadas.

As restrições em tensão:
- **Fidelidade**: o resumo não pode perder decisões, estado de arquivos ou o objetivo da tarefa.
- **Custo**: sumarizar via LLM é caro; truncar é barato mas destrutivo.
- **Cache**: compactar invalida o prefixo cacheado — deve acontecer o mínimo possível e em momentos controlados.

## O padrão universal: escada de agressividade

Os harnesses estudados aplicam as estratégias em escada, da mais barata à mais cara:

1. **Truncar saídas de tools na origem** — limitar linhas/bytes do output antes mesmo de entrar no histórico, preservando início e fim.
2. **Prune / microcompact** — apagar o *conteúdo* de resultados de tools antigas (o modelo raramente relê um `cat` de 30 turnos atrás), mantendo o registro de que a chamada existiu.
3. **Sumarização via LLM (full compact)** — quando as anteriores não bastam, um modelo resume a porção antiga do histórico, preservando um "rabo" recente intacto.
4. **Disparo automático por limiar** — tudo isso orquestrado por um gatilho de percentual da janela, mais um caminho reativo para quando a API devolve "prompt too long".

## Como os harnesses estudados implementam

### opencode — três mecanismos + arquivos gerenciados
Em `packages/opencode/src/session/compaction.ts` (+ `overflow.ts`, `summary.ts`): (a) sumarização automática em overflow, que seleciona um tail recente sob orçamento de tokens (`preserveRecentBudget`, 2k–8k) e gera o resumo com um **agente dedicado `compaction`**, iniciando um novo Context Epoch com auto-continue opcional; (b) **prune** que percorre o histórico de trás para frente e marca como `compacted` saídas de tools além de 40k tokens (`PRUNE_PROTECT`), protegendo skills; (c) truncamento de output (`tool/truncate.ts`) que preserva início+fim e move o texto completo para "Managed Tool Output Files" — o conteúdo não é perdido, vira arquivo referenciável.

### gemini-cli — compressão + destilação + mascaramento
`packages/core/src/context/chatCompressionService.ts` dispara quando os tokens excedem **50% do limite do modelo** (`DEFAULT_COMPRESSION_TOKEN_THRESHOLD = 0.5`), preserva os últimos ~30% do histórico (`COMPRESSION_PRESERVE_THRESHOLD = 0.3`) e sumariza o resto com um prompt dedicado — com orçamento específico para respostas de função (50k tokens) e salvamento de outputs truncados. Além da compressão clássica, há duas camadas que os outros não têm: **tool distillation** (`toolDistillationService.ts`) e **output masking** (`toolOutputMaskingService.ts`). Comando manual `/compress`, evento `ChatCompressed`, hooks `PreCompressTrigger`.

### OpenHarness — a tradução fiel do Claude Code
`src/openharness/services/compact/__init__.py` (1.725 linhas — o módulo mais denso do projeto) declara no docstring: "Faithfully translated from Claude Code's compaction system". Três estratégias: **microcompact** (limpa resultados de tools listadas em `COMPACTABLE_TOOLS`: read/bash/grep/glob/web/edit/write), **full compact** (resumo estruturado via LLM) e **auto-compact** (limiar `auto_compact_threshold_tokens`). Mais um quarto caminho que os outros tratam implicitamente: compactação **reativa** quando a API retorna erro de prompt too long (`_is_prompt_too_long_error`). Hooks `PRE_COMPACT`/`POST_COMPACT` em volta. Por ser um port comentado, é a melhor documentação viva de como o Claude Code compacta.

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Truncamento na origem | sim (+ arquivos gerenciados) | sim (saved truncated output) | via microcompact |
| Prune de tools antigas | sim (40k protect) | distillation + masking | microcompact |
| Sumarização LLM | agente dedicado | prompt dedicado | full compact |
| Disparo | overflow detectado | 50% da janela | limiar configurável + **reativo a erro** |
| O que é preservado | tail 2k–8k tokens + skills | últimos 30% + orçamento p/ function responses | task state + logs de canal |

A convergência aqui é quase total — evidência de que a "escada de agressividade" já é o padrão da indústria. As diferenças que restam são refinamentos: o gemini-cli adiciona camadas intermediárias (destilação, mascaramento), o opencode nunca descarta conteúdo (move para arquivos), e o OpenHarness cobre o caso de borda reativo. Esta é também a dimensão com a **cláusula de expiração** mais clara do livro: se janelas de contexto crescerem ordens de magnitude com custo marginal baixo, boa parte deste capítulo vira história.
