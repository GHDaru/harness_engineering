# Plano — spec 073 (rodada ext-2)

1. **Avaliações em paralelo** (2 agentes leitores, um por repo): leitura sistemática do
   código no clone congelado (`/workspace/qm` @ 7f2c916, `/workspace/kimi-code` @ e22479a),
   template `benchmark/template/HARNESS_EVAL.md`, referência de estilo/profundidade:
   `avaliacoes/pi.md` e `avaliacoes/grok-build.md`. Saída: o próprio arquivo em
   `benchmark/avaliacoes/` + resumo com notas.
2. **Integração** (eu): notas.json (validação sum==total), comparativo.md (tabela + leitura
   ext-2), Apêndice A (livro/apendice-estudo.md), contagens 18→20 nos caps. 00/01,
   radar/AGENTE.md e RADAR.md (status promovido).
3. **Delta EN**: espelhar as mudanças de livro/ nos EN afetados + hashes (selo de sincronia).
4. **Verificação**: `npm run build` (4 passos) local; corpus do companion regenerado.
5. **Publicação**: HISTORICO 0.67 (A3), merge --no-ff, push, CI verde.

Riscos: tamanho dos repos (qm 16M src TS; kimi-code 50M monorepo pnpm) — agentes orientados
a medir (wc/grep) e citar paths, não a ler tudo; nada de API externa.
