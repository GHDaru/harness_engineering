# Spec 006 — Cap. 10 (Subagentes e Orquestração) ao esqueleto v3

> Parte da iniciativa spec 003. Ciclo spec-kit completo, na branch `003-reescrita-editorial-v3`; merge ao fim. Princípios I–IV.

## Problema

O capítulo 10 está em pré-v3. O conteúdo atual capta bem a rodada 1 e as **três filosofias** (subagente-como-ferramenta · como-serviço · como-colega) e as decisões de projeto (isolamento, permissões, comunicação, alcance). Falta: estrutura v3; fundamentos científicos (AutoGen, MetaGPT, CAMEL, ChatDev, surveys de MAS + estudos de falha); fontes da indústria (subagents, orchestrator-worker, "Don't Build Multi-Agents", frameworks, A2A/ACP); e o Apêndice A com as rodadas 2 (Codex `multi_agents_v2` + agent-graph-store; OpenClaw `sessions_spawn` push-based + ACP; Hermes Kanban; Goose orchestrator/SubRecipes; IronClaw child-runs deny-filtrado em prod; n8n agente-como-tool).

## Escopo

Reescrever `livro/capitulos/10-subagentes-orquestracao.md` no esqueleto v3 e sincronizar `livro/bibliografia.md` (Cap. 10 + linha de indústria).

## Critérios de aceitação

- [ ] Selo de captura (2026-07); Objetivos (Bloom) ↔ Verificação 1:1.
- [ ] Fundamentos científicos verificados, traduzidos em decisões (papéis/SOPs; falha de MAS; custo/benefício vs single-agent).
- [ ] Fontes da indústria verificadas (subagents, multi-agent research system × Don't Build Multi-Agents, frameworks, A2A/ACP), com regra de tradução.
- [ ] Estado da arte: as três filosofias + a tensão paralelizar × contexto único; isolamento (worktree/depth); a virada A2A/ACP (orquestrar harnesses de vendors diferentes).
- [ ] Mão na massa: etapa 9 do harness-zero (`09-subagentes` — tool `task` com sessão-filha).
- [ ] Síntese + "o que roubar"; Apêndice A por repositório (rodadas 1+2+frameworks).
- [ ] Build sem erros; nenhuma URL/ID inventado; não-verificados marcados.

## Não-objetivos
- Não alterar notas do benchmark. Não mesclar para main.
