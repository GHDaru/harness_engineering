# 05 — Design de Ferramentas

## O problema

As ferramentas são as "mãos" do agente: o contrato pelo qual o modelo age sobre o mundo. Design de ferramentas é decidir **quais** existem, **como** seus parâmetros são descritos ao modelo (schema), **como** os resultados (e erros) retornam, e **quando** cada uma está disponível. Uma tool mal descrita gera chamadas erradas; um arsenal grande demais dilui a atenção do modelo; um arsenal pequeno demais força gambiarras via shell.

Decisões de projeto recorrentes:
- Schema escrito à mão ou derivado de tipos (Pydantic, Effect Schema, classes declarativas)?
- O conjunto de tools é fixo, ou varia por modelo, modo e configuração?
- Como distinguir tools seguras (read-only) de tools com efeito colateral?

## O núcleo consensual

Os três harnesses convergem num núcleo de ~10 tools que pode ser considerado o **kit mínimo de um agente de código**: ler arquivo, escrever, editar, glob, grep, shell, web fetch, web search, todo list, e delegação a subagente. Em volta desse núcleo, cada projeto expande conforme seu arquétipo.

## Como os harnesses estudados implementam

### opencode — schemas Effect, seleção por modelo
~14 tools principais + 3 experimentais em `packages/opencode/src/tool/`, definidas via `Tool.define(id, Effect.gen(...))` com parâmetros em Effect Schema (que gera o JSON Schema para o LLM); cada tool tem um `.txt` de descrição ao lado (prompt e código separados). O registro central (`registry.ts`) faz **seleção por modelo**: famílias GPT recebem `apply_patch` em vez de `edit`/`write` — reconhecimento explícito de que modelos diferentes editam melhor com formatos diferentes. Ripgrep é embutido no binário. Tools experimentais: `lsp`, `plan_exit`, `code-mode`.

### gemini-cli — classes declarativas com registro filtrado
~20–25 tools em `packages/core/src/tools/`, uma classe por tool estendendo `BaseDeclarativeTool` com schema JSON e um objeto `Invocation`; registradas via `maybeRegister(...)` em `config/config.ts`, respeitando allow/deny lists. As declarações podem **variar por família de modelo** (`definitions/model-family-sets/`). Extras notáveis: shell com processos em background (listar/ler output de processos longos), web search com grounding do Google, e um conjunto opcional de 6 tools de "tracker" (tarefas com dependências e visualização) atrás de feature flag.

### OpenHarness — o maior arsenal, schemas Pydantic
**43+ tools** em `src/openharness/tools/` (um arquivo por tool), herdando `BaseTool` com `input_model` Pydantic — `to_api_schema()` deriva o JSON Schema automaticamente. O método `is_read_only()` alimenta a decisão de paralelismo do loop (cap. 02). Além do núcleo consensual, categorias que os outros não têm como built-in: multimodal (geração de imagem, image-to-text), agendamento (cron), times de agentes (`team_create/delete`, `send_message`), gestão de tasks em background e `tool_search` (descoberta de tools sob demanda).

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Quantidade | ~14 + 3 exp. | ~20–25 + 6 opcionais | 43+ |
| Definição de schema | Effect Schema | classes declarativas + JSON Schema | Pydantic |
| Varia por modelo | sim (`apply_patch` p/ GPT) | sim (model-family-sets) | não |
| Read-only explícito | por permissão | `Kind` na classe | `is_read_only()` → paralelismo |
| Distintivo | descrições `.txt` separadas | background processes, tracker | multimodal, cron, times |

Duas lições emergem. Primeira: **schema derivado de tipos venceu** — ninguém escreve JSON Schema à mão; a fonte de verdade é o sistema de tipos da linguagem. Segunda: a fronteira do design de tools está na **variação por modelo** — opencode e gemini-cli aceitam que a interface ideal de edição depende da família de modelo, o que complica o harness mas melhora o resultado. Mais tools ≠ melhor harness: o arsenal de 43+ do OpenHarness serve seu arquétipo de plataforma pessoal/multi-agente, enquanto o núcleo enxuto do opencode serve o arquétipo de produto focado.
