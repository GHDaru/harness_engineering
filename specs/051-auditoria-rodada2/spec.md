# Spec 051: Auditoria editorial — rodada 2

**Feature Branch**: `051-auditoria-rodada2` · **Criada em**: 2026-07-29

## Contexto

A rodada 1 (spec 020) gerou as melhorias E01–E08. Desde então o livro mudou de forma: template 043 (C01/C08/N02), citações ligadas (028), glossário e siglas (023), rigor do cap. 01 (025), links do Awesome (046), bibliografia 100% verificada (050). Uma segunda passada de leitura completa procura o que o novo formato expôs.

## Método

- 4 auditores (subagentes) em paralelo, um por fatia: 00–04 · 05–09 · 10–14 · 15–17+aparato (glossário, apêndice do estudo, guia).
- Só achados **concretos e verificáveis** (fato interno, link, português, terminologia, truncamento, desvio estrutural acidental); proibido inventar fonte ou propor reescrita de estilo.
- Cada achado é **conferido pelo editor-chefe** (este agente) contra o arquivo antes de corrigir; correções mínimas.

## Requisitos

- FR-001: todo achado confirmado é corrigido no fonte; achados rejeitados ficam registrados aqui com o motivo.
- FR-002: build + link-check + portão por capítulo verdes após as correções; corpus regenerado.


## Resultado (4 auditores · 27 achados confirmados e corrigidos)

**Grave** — `02-loop-do-agente.md` estava **truncado no meio do Apêndice A** desde a reescrita v3 (commit b8a3a90; sem versão íntegra no git): a entrada do IronClaw parava em "`crates/ironclaw_agent_loop`: p" e faltavam Aider, OpenHands, ohmo, n8n e frameworks. Reconstruído a partir da evidência real do benchmark (`benchmark/avaliacoes/*.md`), no padrão dos caps. 03/04.

**Consistência factual**: cap. 01 §5 dizia "três arquétipos" com exemplos fora do corpus (Claude Code, Cline, SWE-agent, ADK, Deep Agents) — realinhado aos quatro arquétipos e à lista real do estudo; cap. 00 ganhou os caps. 15–17 na "Estrutura do livro" e teve dois parágrafos duplicados sobre a coleção Awesome fundidos; URL da coleção unificada para o repositório do autor; cap. 10 desambiguou ACP-IBM×A2A; cap. 14 marcou como superada a divergência de evals comportamentais e a "fila" do Codex; cap. 17 corrigiu a contagem (11 harnesses + 4 frameworks) e abriu as siglas na 1ª ocorrência.

**Livro ↔ harness-zero** (5): exercícios/descrições dos caps. 05, 06, 07, 09 e 12 realinhados ao que as etapas 2/7/6/8/11 realmente implementam (tools reais, servidor de exemplo, veredictos da política, PLAN.md no propor, hooks in-process com retorno como canal); `SessionPort`→`StorePort` nos caps. 08 e 13.

**Glossário**: listas "Aparece em" de LSP, RPC, MAST, GPT e HTTP verificadas por `grep -w` e corrigidas.

**Português/consistência**: parêntese não fechado (cap. 11), "especificam-gaming"→"specification gaming", "reda"→"redação", "a harness"→"o harness" (2×), "sub-agentes"→"subagentes", "não-confiável"→"não confiável", concordância "reúnem" (cap. 07), citação do Hermes alinhada à fonte (cap. 16), link errado do princípio aberto-fechado removido (cap. 12), espaçamentos do apêndice do estudo.

**Nenhum achado rejeitado.** Divergências de contagem do glossário foram rearbitradas por `grep -w` (mesma fronteira de palavra do motor de siglas).
