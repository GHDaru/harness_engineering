# Spec 004 — Cap. 08 (Memória e Estado) ao esqueleto v3

> Parte da iniciativa spec 003 (reescrita editorial v3). Por decisão do autor, cada capítulo roda o **ciclo spec-kit completo** (spec → plan → tasks → implement), todos na branch `003-reescrita-editorial-v3`, com **merge da branch ao fim da iniciativa** (não por capítulo). Sob os Princípios I (evidência), II (fonte-base é código), III (método pedagógico), IV (livro vivo).

## Problema

O capítulo 08 está em formato pré-v3 (curto; sem objetivos de Bloom, sem fundamentos científicos, sem fontes da indústria, sem Apêndice A, sem selo de datação). O conteúdo atual cobre bem a rodada 1 (opencode, gemini-cli, OpenHarness) e a moldura de **três camadas** (estado de sessão · memória de longo prazo · estado do workspace), mas precisa: (a) da estrutura v3; (b) da literatura científica de memória de agentes (MemGPT, CoALA, Generative Agents, etc.), que existe e é rica; (c) das fontes da indústria (docs de sessão/checkpoint/memory-tool, produtos de memória: Letta, mem0, Zep, LangMem); (d) do Apêndice A expandido com as rodadas 2 (Aider ⭐ git-native, Hermes ⭐ `session_search`, Codex rollout jsonl, OpenHands event-stream, IronClaw checkpoints).

## Escopo

Reescrever `livro/capitulos/08-memoria-estado.md` no esqueleto v3 e sincronizar `livro/bibliografia.md` (seção Cap. 08 + linha de fontes da indústria).

## Critérios de aceitação

- [ ] Selo de captura (2026-07) no cabeçalho.
- [ ] Objetivos (3–5, Bloom) mapeados 1:1 à Verificação.
- [ ] Fundamentos científicos: papers reais traduzidos em decisões (a fórmula recência×importância×relevância; OS-paging; forgetting curve; episodic/semantic/procedural).
- [ ] Fontes da indústria: docs de sessão/checkpoint/memory-tool + produtos de memória, com regra de tradução; distinção **memória × RAG**.
- [ ] Estado da arte no corpo: as três camadas + o que há de mais moderno (memory tool client-side, reversão via git/checkpoint, session_search, providers plugáveis).
- [ ] Mão na massa: etapa 4 do harness-zero (`04-sessoes` — persistência SQLite + `/resume`).
- [ ] Síntese + "o que roubar"; Apêndice A por repositório com paths (rodadas 1+2+frameworks).
- [ ] Build sem erros (link-check verde); nenhuma URL/ID inventado; não-verificados marcados.

## Não-objetivos

- Não alterar notas do benchmark. Não mesclar para main (fica para o fim da iniciativa).
