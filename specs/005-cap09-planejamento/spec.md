# Spec 005 — Cap. 09 (Planejamento) ao esqueleto v3

> Parte da iniciativa spec 003. Ciclo spec-kit completo do capítulo, na branch `003-reescrita-editorial-v3`; merge da branch ao fim da iniciativa. Princípios I–IV.

## Problema

O capítulo 09 está em formato pré-v3. O conteúdo atual capta bem a rodada 1 e a descoberta central — **plan mode = modo de permissão** (cap. 07) — e os três instrumentos (plan mode · todo list · decomposição). Falta: estrutura v3; fundamentos científicos (ReAct, plan-and-solve, ToT, surveys de planejamento); fontes da indústria (plan mode, todo/TodoWrite, think tool, spec-driven — Spec Kit/Kiro); e o Apêndice A com as rodadas 2, que trazem dados fortes: **planejamento é a dimensão mais fraca da indústria** (confirmado em todas as rodadas) e a **estratificação tática×durável** do OpenClaw (Goals + Task Flow), além do sinal do n8n (Plan-and-Execute depreciado em favor de planejamento implícito/ReAct).

## Escopo

Reescrever `livro/capitulos/09-planejamento.md` no esqueleto v3 e sincronizar `livro/bibliografia.md` (Cap. 09 já tem sementes: survey 2402.02716, PLANET 2504.14773, Beyond Entangled 2601.07577 — confirmar e enriquecer + linha de indústria).

## Critérios de aceitação

- [ ] Selo de captura (2026-07); Objetivos (Bloom) ↔ Verificação 1:1.
- [ ] Fundamentos científicos verificados, traduzidos em decisões (ReAct vs plan-then-execute; decomposição hierárquica; surveys/benchmarks).
- [ ] Fontes da indústria verificadas (plan mode, todo, think tool, spec-driven), com regra de tradução.
- [ ] Estado da arte: as três garantias (read-only imposto · artefato persistido · aprovação); a estratificação tática×durável; e o dado "planejamento = dimensão mais fraca".
- [ ] Mão na massa: etapa 8 do harness-zero (`08-plan` — plan mode imposto por permissões).
- [ ] Síntese + "o que roubar"; Apêndice A por repositório (rodadas 1+2+frameworks).
- [ ] Build sem erros; nenhuma URL/ID inventado; não-verificados marcados.

## Não-objetivos
- Não alterar notas do benchmark. Não mesclar para main.
