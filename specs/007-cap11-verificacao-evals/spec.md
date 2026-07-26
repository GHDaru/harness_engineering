# Spec 007 — Cap. 11 (Verificação e Evals) ao esqueleto v3

> Parte da iniciativa spec 003. Ciclo spec-kit completo, na branch `003-reescrita-editorial-v3`; merge ao fim. Princípios I–IV.

## Problema

O capítulo 11 está em pré-v3. O conteúdo atual capta bem a rodada 1 e as **três perguntas** (o harness funciona? · o agente se comporta? · o trabalho está certo?) com três campeões (OpenHarness testa o harness, gemini-cli testa o agente, opencode verifica o trabalho via LSP). Falta: estrutura v3; fundamentos científicos (SWE-bench, LLM-as-judge e seus vieses, self-correction, reward hacking); fontes da indústria (benchmarks agênticos, evals model-graded, verificação no loop, frameworks de eval); e o Apêndice A com rodadas 2, que trazem dados fortes: eval comportamental **deixou de ser luxo** (Goose Harbor com leaderboard, Codex snapshots, OpenClaw Personal Agent Benchmark Pack, Hermes verify-on-stop, n8n Evaluations) e benchmarks **por categoria** surgiram.

## Escopo

Reescrever `livro/capitulos/11-verificacao-evals.md` no esqueleto v3 e sincronizar `livro/bibliografia.md` (Cap. 11 + linha de indústria).

## Critérios de aceitação

- [ ] Selo de captura (2026-07); Objetivos (Bloom) ↔ Verificação 1:1.
- [ ] Fundamentos científicos verificados, traduzidos em decisões (SWE-bench/held-out; vieses do juiz LLM; limites da auto-correção; reward hacking).
- [ ] Fontes da indústria verificadas (SWE-bench Verified, terminal-bench, evals model-graded, verificação no loop, frameworks), com regra de tradução.
- [ ] Estado da arte: as três perguntas; eval comportamental como table-stakes; verify-on-stop; snapshots/replay; benchmarks por categoria; isolamento como cidadão de teste.
- [ ] Mão na massa: etapa 10 do harness-zero (`10-evals` — suíte de evals do próprio harness: juiz + respostas gravadas).
- [ ] Síntese + "o que roubar"; Apêndice A por repositório (rodadas 1+2+frameworks).
- [ ] Build sem erros; nenhuma URL/ID inventado; não-verificados marcados.

## Não-objetivos
- Não alterar notas do benchmark. Não mesclar para main.
