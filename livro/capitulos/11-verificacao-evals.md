# 11 — Verificação e Evals

## O problema

Como saber se o agente funciona? A pergunta se desdobra em três, com respostas técnicas diferentes:

1. **O harness funciona?** — testes de software clássicos sobre o código do harness (loop, tools, permissões).
2. **O agente se comporta bem?** — evals: o comportamento emergente (usa as tools certas? é frugal? respeita o plan mode? resiste a injection?) sob teste de regressão.
3. **O trabalho do agente está certo?** — verificação em runtime: sinais (LSP, testes, lint) realimentados ao modelo durante a tarefa.

A segunda é a mais difícil e a mais negligenciada: comportamento de agente é estocástico, caro de testar e muda silenciosamente a cada troca de modelo ou de prompt.

## Padrões de implementação

- **Testes determinísticos com respostas gravadas** — gravar as respostas do LLM e replay em CI: E2E barato e estável.
- **Evals com juiz LLM** — um modelo avalia se o comportamento do agente atende critérios qualitativos.
- **Baselines de regressão** — memória/CPU/startup comparados contra valores de referência versionados, em execução nightly.
- **Verificação em runtime via LSP** — diagnósticos de linguagem após cada edição, devolvidos ao modelo no mesmo turno.
- **Política anti-mock** — testar contra o comportamento real (APIs, filesystem), não contra dublês que mentem.

## Como os harnesses estudados implementam

### gemini-cli — comportamento sob regressão contínua
O regime mais rigoroso dos três, com **quatro suítes separadas**: (1) `evals/` — ~45 testes comportamentais com **juiz LLM** (`llm-judge.ts`) cobrindo frugalidade de leitura, memória hierárquica, plan mode, delegação a subagentes, segurança de shell, **prompt injection via MCP** e recuperação de sandbox; (2) `integration-tests/` — E2E determinísticos que reproduzem **respostas gravadas** (arquivos `.responses`); (3) `memory-tests/` — regressão de uso de memória contra `baselines.json`, nightly; (4) `perf-tests/` — regressão de CPU/startup (cold-startup, idle-cpu, long-chat), nightly. O comportamento do agente é tratado como superfície de regressão de primeira classe — nenhum outro harness estudado faz isso.

### opencode — verificação durante a tarefa
Dois diferenciais. Primeiro, **LSP em runtime** (`packages/opencode/src/lsp/`): mapeia dezenas de linguagens a servidores (typescript, pyright...), e **edições disparam diagnósticos realimentados ao modelo** — o agente descobre que quebrou a tipagem no turno seguinte, não no CI. Segundo, cultura de teste com **política anti-mock** explícita (o `AGENTS.md` de `packages/opencode/test/` proíbe mocks) e um `http-recorder` que grava/replaya chamadas HTTP para testar provedores reais com determinismo. Typecheck obrigatório (`bun typecheck`); guard impedindo rodar testes da raiz.

### OpenHarness — E2E com modelo real
121 arquivos de teste em `tests/`, ~31 subpastas espelhando cada subsistema (engine, tools, mcp, permissions, swarm, memory, sandbox, hooks...). O traço próprio: suítes E2E com **chamadas reais de modelo** (`scripts/test_harness_features.py` valida retry, skills, paralelismo e permissões contra API de verdade) e testes contra artefatos reais do ecossistema (`test_real_skills_plugins.py` roda skills do anthropics/skills e plugins do claude-code) — a compatibilidade declarada com o ecossistema Claude Code é testada, não só prometida. Uma skill `harness-eval` empacota a validação E2E como comando.

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Testes do harness | anti-mock + http-recorder | preflight + integração gravada | 121 arquivos por subsistema |
| Evals comportamentais | — | ~45 c/ juiz LLM | E2E com modelo real |
| Baselines de regressão | e2e de performance | memória + perf, nightly | — |
| Verificação em runtime | **LSP → diagnósticos ao modelo** | — | tool `lsp` |
| Segurança testada | — | injection via MCP, shell safety | permissões em E2E |

As três respostas do problema receberam três campeões: OpenHarness testa melhor *o harness* (cobertura por subsistema), gemini-cli testa melhor *o agente* (evals + baselines), opencode verifica melhor *o trabalho* (LSP em runtime). A lacuna comum é reveladora: só um dos três testa comportamento sob ataque. À medida que harnesses ganham autonomia (cap. 10), evals comportamentais deixam de ser luxo — um harness sem evals não sabe o que perdeu no último ajuste de prompt.
